import logging

import botocore
import click

log = logging.getLogger(__name__)


def delete_stacks(**kwargs):
    """Deletes all stacks with the specified job-identifier"""

    log.debug('Deleting stacks')

    session = kwargs['session']
    job_identifier = kwargs['job_identifier']

    cfn_client = session.client('cloudformation')

    identified_stacks = []
    for stack in cfn_client.describe_stacks()['Stacks']:
        try:
            if "{}-".format(job_identifier) in stack['StackName']:
                identified_stacks.append(stack['StackName'])
        except IndexError:
            # Non-Leo stacks
            pass

    for identified_stack in identified_stacks:
        cfn_client.delete_stack(StackName=identified_stack)
        try:
            cfn_client.get_waiter('stack_delete_complete').wait(StackName=identified_stack)
            click.echo("Deleted {}.".format(identified_stack))
        except botocore.exceptions.WaiterError as waiter_error:
            click.echo("{} failed to delete. {}".format(identified_stack, waiter_error))
            click.echo("Stopped stack deletion.")
            break
