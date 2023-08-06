from __future__ import print_function

import logging
import os

import click

log = logging.getLogger(__name__)


def format_path(**kwargs):
    """Creates a path type string"""
    objects = []
    for key, value in kwargs.items():
        objects.append(value)

    return '/'.join(objects)


def upload_templates(**kwargs):
    """Uploads files with the standard CloudFormation file extensions to the specific bucket in """

    log.debug('Uploading templates to S3')

    upload_parameters = {}

    if 'prefix' in kwargs:
        prefix = kwargs['prefix']
        if prefix[-1] == "/":
            prefix = prefix.rstrip("/")
        if prefix[0] == "/":
            prefix = prefix.lstrip("/")
        upload_parameters.update({'prefix': prefix})

    bucket = kwargs['bucket']
    local_path = kwargs['local_path']
    session = kwargs['session']

    s3_client = session.client('s3')
    cfn_ext = ('.json', '.template', '.txt', 'yaml', 'yml')

    for file_object in os.listdir(local_path):
        if file_object.lower().endswith(cfn_ext):
            upload_parameters.update({'file_object': file_object})
            s3_client.upload_file(format_path(obj_1=local_path, obj_2=file_object),
                                  bucket, format_path(**upload_parameters))

            s3_client.get_waiter('object_exists').wait(Bucket=bucket,
                                                       Key=format_path(**upload_parameters))
            click.echo('Uploaded %s' % file_object)
