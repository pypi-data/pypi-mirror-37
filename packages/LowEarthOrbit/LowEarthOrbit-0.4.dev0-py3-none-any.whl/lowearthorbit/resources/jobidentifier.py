import logging
import sys

log = logging.getLogger(__name__)


def check(job_identifier):
    """Checks if the job identifier is up to CloudFormation's naming requirements."""

    if not job_identifier:
        sys.exit("job_identifier must have a value.")

    if not job_identifier.isalnum():
        sys.exit("The job identifier must be alpha-numeric.")

    log.debug('Checked job identifier: %s' % job_identifier)

    return job_identifier
