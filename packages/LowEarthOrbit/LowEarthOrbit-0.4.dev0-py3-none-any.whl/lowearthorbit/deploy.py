import logging

from lowearthorbit.resources.create import create_stack
from lowearthorbit.resources.update import update_stack

log = logging.getLogger(__name__)


def deploy_type(stack_name, cfn_client):
    """Checks if the CloudFormation stack should be created or updated"""

    log.debug('Gathering deploy type')

    for stack in cfn_client.describe_stacks()['Stacks']:
        cfn_stack_name = stack['StackName'].split('-')
        leo_stack_name = stack_name.split('-')
        try:
            if cfn_stack_name[0] == leo_stack_name[0] and cfn_stack_name[2] == leo_stack_name[2]:
                if stack['StackStatus'] in ('CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE'):
                    return {'Update': True, 'UpdateStackName': stack['StackName']}
        except IndexError:  # For non-Leo stack names
            pass

    return {'Update': False}


def deploy_templates(**kwargs):
    """Creates or updates CloudFormation stacks"""

    log.debug('Deploying templates')

    objects_parameters = {}
    objects_parameters.update({'Bucket': kwargs['bucket']})
    if 'prefix' in kwargs:
        objects_parameters.update({'Prefix': kwargs['prefix']})

    deploy_parameters = {}
    if 'tags' in kwargs:
        deploy_parameters.update({'tags': kwargs['tags']})
    if 'rollback_configuration' in kwargs:
        deploy_parameters.update({'rollback_configuration': kwargs['rollback_configuration']})

    session = kwargs['session']
    s3_client = session.client('s3')
    cfn_client = session.client('cloudformation')

    cfn_ext = ('.json', '.template', '.txt', '.yaml', '.yml')

    stack_archive = []

    stack_counter = 0
    for s3_object in s3_client.list_objects_v2(**objects_parameters)['Contents']:
        if s3_object['Key'].endswith(cfn_ext) and s3_object['Key'].split('/')[-1].startswith('%02d' % stack_counter):
            stack_name = "{}-{}".format(kwargs['job_identifier'], str(s3_object['Key'].split('/')[-1]).rsplit('.', 1)[0])

            check = deploy_type(stack_name=stack_name,
                                cfn_client=cfn_client)

            if check['Update']:
                try:
                    stack = exit(update_stack(update_stack_name=check['UpdateStackName'],
                                              key_object=s3_object['Key'],
                                              bucket=objects_parameters['Bucket'],
                                              job_identifier=kwargs['job_identifier'],
                                              parameters=kwargs['parameters'],
                                              gated=kwargs['gated'],
                                              session=kwargs['session'],
                                              deploy_parameters=deploy_parameters))

                    stack_archive.append({'StackName': stack['StackName']})
                except Exception as e:
                    log.exception('Error: %s', e)
                    exit(1)



            else:
                try:
                    stack = exit(create_stack(key_object=s3_object['Key'],
                                              bucket=objects_parameters['Bucket'],
                                              job_identifier=kwargs['job_identifier'],
                                              parameters=kwargs['parameters'],
                                              gated=kwargs['gated'],
                                              session=kwargs['session'],
                                              deploy_parameters=deploy_parameters))

                    stack_archive.append({'StackName': stack['StackName']})
                except Exception as e:
                    log.exception('Error: %s', e)
                    exit(1)

            stack_counter += 1
