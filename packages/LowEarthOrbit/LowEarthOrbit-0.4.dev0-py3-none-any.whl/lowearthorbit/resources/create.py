import json
import logging
import sys
import time

import botocore
import click

from lowearthorbit.resources.capabilities import get as get_capabilities
from lowearthorbit.resources.parameters import gather as gather_parameters

log = logging.getLogger(__name__)

STACK_LIST = []


def get_stack_name(job_identifier, obj):
    """Formats the stack name and make sure it meets CloudFormations naming requirements."""

    stack_name = "{}-{}".format(job_identifier, obj)
    stack_name_parts = []  # Below checks if the stack_name meets all requirements.
    if not stack_name[0].isalpha():
        stack_name = "s-" + stack_name
    if len(stack_name) > 255:
        stack_name = stack_name[:255]
    for s in stack_name:
        if not s.isalnum():
            s = s.replace(s, "-")
            stack_name_parts.append(s)
        else:
            stack_name_parts.append(s)
    stack_name = "".join(stack_name_parts)

    log.debug('Created stack name: %s' % stack_name)

    return stack_name


def transform_template(cfn_client, stack_name, template_url, stack_parameters, deploy_parameters):
    """Handles templates that transform, such as templates that are using SAM."""

    # Gathering capabilities is a bit wacky with templates that transform
    click.echo("Gathering information needed to transform the template")
    transform_stack_details = cfn_client.create_change_set(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=stack_parameters,
        ChangeSetName='change set-{}-{}'.format(stack_name, int(time.time())),
        Description="Transformation details change set for {} created by Leo".format(
            stack_name),
        ChangeSetType='CREATE',
        **deploy_parameters
    )

    cfn_client.get_waiter('change_set_create_complete').wait(
        ChangeSetName=transform_stack_details['Id']
    )

    new_template = cfn_client.get_template(
        ChangeSetName=transform_stack_details['Id']
    )

    new_template_capabilities = cfn_client.get_template_summary(
        TemplateBody=str(json.loads(json.dumps(new_template['TemplateBody'])))  # Check what on earth is going on here
    )
    cfn_client.delete_change_set(
        ChangeSetName=transform_stack_details['Id']
    )

    click.echo("Transforming template")
    transform_stack = cfn_client.create_change_set(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=stack_parameters,
        Capabilities=new_template_capabilities['Capabilities'],
        ChangeSetName='change set-{}-{}'.format(stack_name, int(time.time())),
        Description="Transformation change set for {} created by Leo".format(
            stack_name),
        ChangeSetType='CREATE',
        **deploy_parameters
    )

    cfn_client.get_waiter('change_set_create_complete').wait(
        ChangeSetName=transform_stack['Id']
    )
    cfn_client.execute_change_set(
        ChangeSetName=transform_stack['Id'],
        StackName=stack_name
    )
    log.debug('Executing change set')

    return cfn_client.describe_stacks(StackName=stack_name)['Stacks'][0]


def create_stack(**kwargs):
    """Creates the stack and handles rollback conditions"""

    session = kwargs['session']
    key_object = kwargs['key_object']
    bucket = kwargs['bucket']
    job_identifier = kwargs['job_identifier']
    parameters = kwargs['parameters']
    deploy_parameters = kwargs['deploy_parameters']

    cfn_client = session.client('cloudformation')
    s3_client = session.client('s3')

    template_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': key_object},
                                                    ExpiresIn=60)
    template_summary = cfn_client.get_template_summary(TemplateURL=template_url)

    stack_name = get_stack_name(job_identifier=job_identifier, obj=str(key_object).split("/")[-1].split(".")[0])
    stack_capabilities = get_capabilities(template_url=template_url, session=session)

    stack_parameters = gather_parameters(session=session,
                                         key_object=key_object, parameters=parameters, bucket=bucket,
                                         job_identifier=job_identifier)

    try:
        if 'DeclaredTransforms' not in template_summary:
            log.debug('Creating stack')
            current_stack = cfn_client.create_stack(StackName=stack_name,
                                                    TemplateURL=template_url,
                                                    Parameters=stack_parameters,
                                                    Capabilities=stack_capabilities,
                                                    DisableRollback=False,
                                                    TimeoutInMinutes=123,
                                                    **deploy_parameters)
        else:
            current_stack = transform_template(cfn_client=cfn_client,
                                               stack_name=stack_name,
                                               template_url=template_url,
                                               stack_parameters=stack_parameters,
                                               deploy_parameters=deploy_parameters)

        STACK_LIST.append({'StackId': current_stack['StackId'], 'StackName': stack_name})
        stack_description = cfn_client.describe_stacks(StackName=current_stack['StackId'])['Stacks'][0]['Description']
        click.echo("\nCreating {}...".format(stack_name))
        click.echo("Description of {}: \n\t{}".format(stack_name, stack_description))
        try:
            cfn_client.get_waiter('stack_create_complete').wait(StackName=current_stack['StackId'])
            click.echo("Created {}.".format(stack_name))

            return {'StackName': stack_name}
        except botocore.exceptions.WaiterError:
            click.echo("\n{} is currently rolling back.".format(stack_name))
            resource_failures = [{'LogicalResourceId': event['LogicalResourceId'],
                                  'ResourceStatusReason': event['ResourceStatusReason']} for event in
                                 cfn_client.describe_stack_events(StackName=current_stack['StackId'])['StackEvents']
                                 if event['ResourceStatus'] == 'CREATE_FAILED']

            if resource_failures:
                for failures in resource_failures:
                    click.echo("%s has failed to be created because: '%s'" % (
                        failures['LogicalResourceId'], failures['ResourceStatusReason']))
            else:
                click.echo("Please check console for why some resources failed to create.")

            sys.exit()

    except botocore.exceptions.ClientError as e:
        raise e
