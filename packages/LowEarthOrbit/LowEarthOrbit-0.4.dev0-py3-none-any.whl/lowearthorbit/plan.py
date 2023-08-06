def plan_deployment(Session,Bucket,Prefix,JobIdentifier):
    s3_client = Session.client('s3')
    cfn_client = Session.client('cloudformation')
    cfn_ext = ('.json', '.template', '.txt', 'yaml', 'yml')

    for object in s3_client.list_objects_v2(
            Bucket=Bucket,
            Prefix=Prefix
    )['Contents']:
        if object['Key'].endswith(cfn_ext):
            for stack in cfn_client.describe_stacks()['Stacks']:
                if stack['StackName'] == "%s-%s" % (JobIdentifier, object['Key'].split('.')[0]):
                    template_url = s3_client.generate_presigned_url('get_object',
                                                                    Params={'Bucket': Bucket,
                                                                            'Key': object['Key']},
                                                                    ExpiresIn=60)



