import logging

import boto3
import click

from lowearthorbit.delete import delete_stacks
from lowearthorbit.deploy import deploy_templates
from lowearthorbit.upload import upload_templates
from lowearthorbit.validate import validate_templates

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)


class Config(object):
    def __init__(self):
        self.session = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


def parse_args(arguments):
    argument_parameters = {}
    for key, value in arguments.items():
        if value is not None:
            argument_parameters.update({key: value})

    return argument_parameters


@click.group()
@click.option('--aws-access-key-id', type=click.STRING,
              help='AWS access key ID')
@click.option('--aws-secret-access-key', type=click.STRING,
              help='AWS secret access key')
@click.option('--aws_session_token', type=click.STRING,
              help='AWS temporary session token')
@click.option('--botocore-session', type=click.STRING,
              help='Use this Botocore session instead of creating a new default one')
@click.option('--profile', type=click.STRING,
              help='The name of a profile to use. If not given, then the default profile is used')
@click.option('--region', type=click.STRING,
              help='Region when creating new connections')
@click.option('--debug', is_flag=True,
              help='Shows debug output')
@pass_config
def cli(config, aws_access_key_id, aws_secret_access_key, aws_session_token, botocore_session, profile, region, debug):
    """Creates the connection to AWS with the specified session arguments"""
    try:
        if debug:
            log.setLevel(logging.DEBUG)

        session_arguments = parse_args(arguments=locals())

        # Not boto3 session arguments
        del session_arguments['debug']
        del session_arguments['config']

        log.debug('Passing session arguments')
        config.session = boto3.session.Session(**session_arguments)
    except Exception as e:
        log.exception('Error: %s', e)
        exit(1)


@cli.command()
@click.option('--job-identifier', type=click.STRING, required=True,
              help='Prefix that is used to identify stacks to delete')
@pass_config
def delete(config, job_identifier):
    """Deletes all stacks with the given job identifier"""

    delete_arguments = locals()
    del delete_arguments['config']
    delete_arguments.update({'session': config.session})
    try:
        exit(delete_stacks(**delete_arguments))
    except Exception as e:
        log.exception('Error: %s', e)
        exit(1)


@cli.command()
@click.option('--bucket', type=click.STRING, required=True,
              help="S3 bucket that has the CloudFormation templates.")
@click.option('--prefix', type=click.STRING,
              help='Prefix or bucket subdirectory where CloudFormation templates are located.')
@click.option('--gated', type=click.BOOL, default=False,
              help='Checks with user before deploying an update')
@click.option('--job-identifier', type=click.STRING, required=True,
              help='Prefix that is added on to the deployed stack names')
@click.option('--parameters', type=click.STRING, default=[],
              help='All parameters that are needed to deploy with. '
                   'Can either be from a JSON file or typed JSON that must be in quotes')
@click.option('--rollback-configuration', type=click.STRING,
              help='The rollback triggers for AWS CloudFormation to monitor during stack creation '
                   'and updating operations, and for the specified monitoring period afterwards.')
@click.option('--tags', type=click.STRING,
              help='Tags added to all deployed stacks')
@pass_config
def deploy(config, bucket, prefix, gated, job_identifier, parameters, rollback_configuration, tags):
    """Creates or updates cloudformation stacks"""

    deploy_arguments = parse_args(arguments=locals())
    del deploy_arguments['config']
    deploy_arguments.update({'session': config.session})

    try:
        exit(deploy_templates(**deploy_arguments))
    except Exception as e:
        log.exception('Error: %s', e)
        exit(1)


@cli.command()
def plan():
    click.echo("plan")


@cli.command()
@click.option('--bucket', type=click.STRING, required=True,
              help="S3 bucket that the CloudFormation templates will be uploaded to.")
@click.option('--prefix', type=click.STRING,
              help='Prefix or bucket subdirectory where CloudFormation templates will be uploaded to.')
@click.option('--local-path', type=click.Path(exists=True), required=True,
              help='Local path where CloudFormation templates are located.')
@pass_config
def upload(config, bucket, prefix, local_path):
    """Uploads all templates to S3"""

    upload_arguments = parse_args(arguments=locals())

    del upload_arguments['config']
    upload_arguments.update({'session': config.session})

    try:
        exit(upload_templates(**upload_arguments))
    except Exception as e:
        log.exception('Error: %s', e)
        exit(1)


@cli.command()
@click.option('--bucket', type=click.STRING, required=True,
              help="S3 bucket that has the CloudFormation templates.")
@click.option('--prefix', type=click.STRING,
              help='Prefix or bucket subdirectory where CloudFormation templates are located.')
@pass_config
def validate(config, bucket, prefix):
    """Validates all templates"""
    validate_arguments = parse_args(arguments=locals())

    del validate_arguments['config']
    validate_arguments.update({'session': config.session})

    try:
        validation_errors = validate_templates(**validate_arguments)

        if validation_errors:
            click.echo("Following errors occurred when validating templates:")
            for error in validation_errors:
                click.echo('%s: %s' % (error['Template'], error['Error']))
    except Exception as e:
        log.exception('Error: %s', e)
        exit(1)
