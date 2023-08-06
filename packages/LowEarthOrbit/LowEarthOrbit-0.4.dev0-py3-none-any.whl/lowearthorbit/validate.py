from __future__ import print_function

import logging

import botocore
import click

log = logging.getLogger(__name__)


def validate_templates(**kwargs):
    """"Attempts to validate every file in the bucket subdirectory with every known CloudFormation extension."""

    log.debug("Validating templates")

    validate_parameters = {}
    if 'bucket' in kwargs:
        validate_parameters.update({'Bucket': kwargs['bucket']})
    if 'prefix' in kwargs:
        validate_parameters.update({'Prefix': kwargs['prefix']})
    else:
        validate_parameters.update({'Delimiter': '/'})

    session = kwargs['session']

    s3_client = session.client('s3')
    cf_client = session.client('cloudformation')
    cfn_ext = ('.json', '.template', '.txt', 'yaml', 'yml')

    validation_errors = []
    try:
        for s3_object in s3_client.list_objects_v2(**validate_parameters
                                                )['Contents']:
            if s3_object['Key'].endswith(cfn_ext):
                template_url = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': kwargs['bucket'],
                                                                        'Key': s3_object['Key']},
                                                                ExpiresIn=60)
                try:
                    cf_client.validate_template(TemplateURL=template_url)
                    click.echo("Validated %s" % s3_object['Key'])

                except botocore.exceptions.ClientError as e:
                    validation_errors.append({'Template': s3_object['Key'], 'Error': e})
    except KeyError:
        log.error("The specified key does not exist in %s" % kwargs['bucket'])

    return validation_errors
