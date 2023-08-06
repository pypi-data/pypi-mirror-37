from __future__ import print_function

import unittest
import subprocess

import boto3


class ResourceTesting(unittest.TestCase):
    def setUp(self):
        self.bucket = ''
        self.key = ''
        self.session = boto3.session.Session()
        self.cfn_client = boto3.session('cloudformation')
        self.s3_client = boto3.session('s3')
        self.url = self.s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': self.bucket,
                                                                 'Key': self.key},
                                                         ExpiresIn=60)
        self.template_details = self.cfn_client.get_template_summary(TemplateURL=self.url)
        self.job_identifier = ''
        self.parameters = []
        self.tags = []
        self.gated = True

    def tearDown(self):
        pass

    def test_deploy(self):
        deploy_cmd = "leo deploy --bucket %s --job-identifier %s --gated %s --parameters '%s'" % (
        self.bucket, self.job_identifier, self.gated, self.parameters)

        deploy_run = subprocess.run(deploy_cmd.split(),capture_output = True)

        with self.assertRaises():
            print(deploy_run)


0