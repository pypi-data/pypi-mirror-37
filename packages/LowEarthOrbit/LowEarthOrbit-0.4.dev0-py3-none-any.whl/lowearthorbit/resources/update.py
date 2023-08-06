import logging
import sys
import time

import botocore
import click

from lowearthorbit.resources.capabilities import get as get_capabilities
from lowearthorbit.resources.parameters import gather as gather_parameters

log = logging.getLogger(__name__)


def stack_continue_rollback_waiter(stack_name, cfn_client):
    """Boto3 does not have a waiter for creating rolling back a stack completely, this is a custom one"""

    log.debug('Stack is rolling back')

    stack_continue_rollback_counter = 0
    stack_continue_rollback = True

    while stack_continue_rollback:
        stack_details = cfn_client.describe_stacks(StackName=stack_name)['Stacks'][0]
        if stack_details['StackStatus'] in 'UPDATE_ROLLBACK_COMPLETE':
            stack_continue_rollback = False

        elif stack_details['StackStatus'] in 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS':
            if stack_continue_rollback_counter == 120:
                click.echo("\n{}".format(stack_details['StatusReason']))
                sys.exit("Something went wrong while trying to rollback the stack. Please check the console.")
            else:
                stack_continue_rollback_counter += 1
                time.sleep(15)

        elif stack_details['StackStatus'] in 'UPDATE_ROLLBACK_FAILED':
            sys.exit(
                "Rolling back for {} has failed. Please check the console.".format(stack_details['StackName']))


def change_set_delete_waiter(change_set_id, cfn_client):
    """Boto3 does not have a waiter for deleting a change set, this is a custom one"""

    log.debug('Deleting change set')

    try:
        change_set_deletion_counter = 0
        change_set_deletion_bool = True

        # Custom change set deletion waiter
        while change_set_deletion_bool:
            change_set_details = cfn_client.describe_change_set(ChangeSetName=change_set_id)
            if change_set_details['Status'] in 'DELETE_COMPLETE':
                pass
                change_set_deletion_bool = False

            elif change_set_details['Status'] in 'FAILED':
                click.echo("\n{}".format(change_set_details['StatusReason']))
                sys.exit("Change set {} deletion has failed. Please check the console.".format(
                    change_set_details['StackName']))

            else:
                if change_set_deletion_counter == 120:
                    click.echo("\n{}".format(change_set_details['StatusReason']))
                    sys.exit(
                        "Something went wrong while deleting the change set. Please check the console.")
                else:
                    change_set_deletion_counter += 1
                    time.sleep(15)

    except botocore.exceptions.ClientError:
        # Change set is already deleted therefore the waiter is no longer needed.
        pass


def change_log(changes):
    """Prints out all the possible changes to the CloudFormation stack"""

    data = []
    for change in changes:
        try:
            replacement = change['ResourceChange']['Replacement']
        except KeyError:
            replacement = "None"

        try:
            phyresid = change['ResourceChange']['PhysicalResourceId']
        except KeyError:
            phyresid = "None"

        data.append(["Action: {}".format(change['ResourceChange']['Action']),
                     "Logical ID: {}".format(change['ResourceChange']['LogicalResourceId']),
                     "Physical ID: {}".format(phyresid),
                     "Resource Type: {}".format(change['ResourceChange']['ResourceType']),
                     "Replacement: {}".format(replacement)])
    return data


def apply_changes(cfn_client, update_stack_name, past_failures, change_set_name, change_set):
    click.echo("Executing change set: {}...".format(change_set_name))
    cfn_client.execute_change_set(ChangeSetName=change_set['Id'], StackName=update_stack_name)

    try:
        cfn_client.get_waiter('stack_update_complete').wait(StackName=update_stack_name)
    except botocore.exceptions.WaiterError:
        resource_failures = []
        for event in cfn_client.describe_stack_events(StackName=update_stack_name)['StackEvents']:
            if event['ResourceStatus'] in ['CREATE_FAILED', 'UPDATE_FAILED']:
                resource_failures.append(event)
        if resource_failures:
            for failures in resource_failures:
                if failures not in past_failures:
                    click.echo("%s has failed to be updated because: '%s'" % (
                        failures['LogicalResourceId'], failures['ResourceStatusReason']))
        else:
            click.echo("Please check console for why some resources failed to update.")

        stack_status = cfn_client.describe_stacks(StackName=update_stack_name)['Stacks'][0]['StackStatus']
        if stack_status == 'UPDATE_ROLLBACK_FAILED':
            click.echo("Attempting to restore former state...")
            cfn_client.continue_update_rollback(StackName=update_stack_name)
            stack_continue_rollback_waiter(stack_name=update_stack_name, cfn_client=cfn_client)

        sys.exit("Stopped update because of %s's updating failure." % update_stack_name)


def update_stack(**kwargs):
    """Updates stack if there is a stack by the same name"""

    session = kwargs['session']
    key_object = kwargs['key_object']
    stack_name = kwargs['update_stack_name']
    bucket = kwargs['bucket']
    job_identifier = kwargs['job_identifier']
    parameters = kwargs['parameters']
    gated = kwargs['gated']
    deploy_parameters = kwargs['deploy_parameters']

    cfn_client = session.client('cloudformation')
    s3_client = session.client('s3')

    template_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': key_object},
                                                    ExpiresIn=60)

    click.echo("\nCreating change set for {}...".format(stack_name))

    change_set_name = 'change set-{}-{}'.format(stack_name, int(time.time()))
    stack_capabilities = get_capabilities(template_url=template_url, session=session)
    stack_parameters = gather_parameters(session=session,
                                         key_object=key_object, parameters=parameters, bucket=bucket,
                                         job_identifier=job_identifier)

    try:
        change_set = cfn_client.create_change_set(
            StackName=stack_name,
            TemplateURL=template_url,
            Parameters=stack_parameters,
            Capabilities=stack_capabilities,
            ChangeSetName=change_set_name,
            Description="Change set for {} created by Leo".format(stack_name),
            **deploy_parameters
        )
    except botocore.exceptions.ClientError as ChangeSetCreationError:
        raise ChangeSetCreationError

    try:
        cfn_client.get_waiter('change_set_create_complete').wait(ChangeSetName=change_set['Id'])
    except botocore.exceptions.WaiterError as change_set_creation_error:
        long_string_err = "The submitted information didn't contain changes. " \
                          "Submit different information to create a change set."

        if str(cfn_client.describe_change_set(ChangeSetName=change_set['Id'])['StatusReason']) in \
                (long_string_err, "No updates are to be performed."):
            click.echo(cfn_client.describe_change_set(ChangeSetName=change_set['Id'])['StatusReason'])
            pass
        else:
            raise change_set_creation_error

    # Checks for the changes
    change_set_details = cfn_client.describe_change_set(ChangeSetName=change_set['Id'])
    change_set_changes = change_set_details['Changes']

    if change_set_changes:
        click.echo("Gathering changes for change set: {}...".format(change_set_name))
        for change in change_log(changes=change_set_changes):
            # Dynamically gathers the length of each change in order to display information better
            action = sorted([len(item[0]) for item in change])[-1]
            logical = sorted([len(item[1]) for item in change])[-1]
            physical = sorted([len(item[2]) for item in change])[-1]
            resource = sorted([len(item[3]) for item in change])[-1]
            replacement = sorted([len(item[4]) for item in change])[-1]

            click.echo('{0: <{col1}}  {1:<{col2}}  {2:<{col3}}  {3:<{col4}}  {4:<{col5}}'.format(*change,
                                                                                                 col1=action,
                                                                                                 col2=logical,
                                                                                                 col3=physical,
                                                                                                 col4=resource,
                                                                                                 col5=replacement))
            click.echo("\t")

        # Acts as a filter on past resource failures
        past_failures = [stack_event for stack_event in
                         cfn_client.describe_stack_events(StackName=stack_name)['StackEvents'] if
                         stack_event['ResourceStatus'] in ['CREATE_FAILED', 'UPDATE_FAILED']]

        if not gated:
            apply_changes(change_set_name=change_set['Id'], change_set=change_set, cfn_client=cfn_client,
                          update_stack_name=stack_name, past_failures=past_failures)
            return {'StackName': stack_name}
        else:
            click.echo("Would you like to execute these changes?")
            while True:
                execute_changes = click.prompt("Answer: ")
                if execute_changes.lower() in ('yes', 'ya', 'y', 'yea', 'yup', 'yeah'):
                    apply_changes(change_set_name=change_set['Id'], change_set=change_set, cfn_client=cfn_client,
                                  update_stack_name=stack_name, past_failures=past_failures)

                    return {'StackName': stack_name}

                if execute_changes.lower() in ('no', 'na', 'n', 'nah', 'nope'):
                    click.echo("Moving on from executing {}".format(change_set_name))
                    click.echo("Deleting change set {}...".format(change_set_name))
                    cfn_client.delete_change_set(ChangeSetName=change_set['Id'],
                                                 StackName=stack_name)
                    # Check if still needed
                    change_set_delete_waiter(change_set_id=change_set['Id'], cfn_client=cfn_client)
                    break

    else:
        # If there are no changes it passes and deletes the change set
        click.echo("No changes found for {}".format(stack_name))
        click.echo("Deleting change set for {}...".format(change_set_name))
        cfn_client.delete_change_set(ChangeSetName=change_set['Id'], StackName=stack_name)
        change_set_delete_waiter(change_set_id=change_set['Id'], cfn_client=cfn_client)
