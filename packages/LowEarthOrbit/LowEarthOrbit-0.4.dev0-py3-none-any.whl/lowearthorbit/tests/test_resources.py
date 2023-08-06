import unittest
import boto3

import lowearthorbit



class ResourceTesting(unittest.TestCase):
    def setUp(self):
        self.bucket = ''
        self.key= ''
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


    def tearDown(self):
        



    def test_deploy(self):



    @unittest.skipUnless()
    def test_capabilities(self):
        self.assertIs(lowearthorbit.resources.capabilities(template_url = self.url,
                                                           cfn_client = self.cfn_client ), list)
    def test_create(self):
        self.assertIs(lowearthorbit.resources.create(template_url=self.url,
                             template_details=self.template_summary,
                             parameters=self.parameters,
                             bucket=self.bucket,
                             cfn_client=self.cfn_client,
                             s3_client=self.s3_client,
                             key_object=object['Key'],
                             tags=self.tags,
                             job_identifier=self.job_identifier), str)
    def test_jobidentifier(self):
        self.assertIs(lowearthorbit.resources.jobidentifier(JobIdentifier=self.job_identifier), str)




