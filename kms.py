import boto3

def clean_kms_keys(session):
    for key in list_keys(session, '/core/kms/default'):
        print(f"Schedule deletion KMS key: {key['Name']}")
        reset_key_policy(session, key['KeyId'])
        delete_key(session, key['KeyId'])

def list_keys(session, path):
    kms_client = session.client('kms')
    ssm_client = session.client('ssm')
    kms_keys = kms_client.list_keys()['Keys']
    ssm_params = ssm_client.get_parameters_by_path(
        Path=path,
        Recursive=True
    )['Parameters']
    keys_without_ssm = [
        key for key in kms_keys if key['KeyId'] not in [
            param['Value'] for param in ssm_params]]
    return keys_without_ssm

def reset_key_policy(session, key_id):
    # Create KMS client using the session
    kms_client = session.client('kms')

    # Update KMS key policy with default root policy
    policy = '''
    {
        "Version": "2012-10-17",
        "Id": "key-default-root-policy",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::ACCOUNT_ID:root"
                },
                "Action": "kms:*",
                "Resource": "*"
            }
        ]
    }
    '''
    response = kms_client.put_key_policy(
            KeyId=key_id,
            PolicyName='default',
            Policy=policy
    )

def delete_key(session, key_id):
    # Create KMS client using the session
    kms_client = session.client('kms')

    # Delete KMS key with one week retention
    response = kms_client.schedule_key_deletion(
            KeyId=key_id,
            PendingWindowInDays=7
    )