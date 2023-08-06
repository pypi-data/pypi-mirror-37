import logging

log = logging.getLogger(__name__)


def get(template_url, session):
    """Gets the needed capabilities for the CloudFormation stack """

    log.debug('Retrieving stack capabilities')

    cfn_client = session.client('cloudformation')

    template_details = cfn_client.get_template_summary(TemplateURL=template_url)

    try:
        stack_capabilities = template_details['Capabilities']
    except KeyError:
        stack_capabilities = []

    return stack_capabilities
