import boto3
from organization import Organization 
from kms import clean_kms_keys

REGIONS = ['us-east-1', 'eu-west-1', 'eu-central-1', 'ca-central-1', 'ap-southeast-1']

def main():
    session = boto3.Session()
    organization = Organization(session)
    accounts = organization.get_member_accounts()
    for target_session in session_generator(session, accounts):
        print(target_session.client('sts').get_caller_identity())
        clean_kms_keys(target_session)

def session_generator(session, accounts): 
    for account in accounts:
        for region in REGIONS:
            yield assume_role(session, account, region)

def assume_role(session, account_id, region):
    # Role ARN for AWSControlTowerExecution
    role_arn = f"arn:aws:iam::{account_id}:role/AWSControlTowerExecution"

    # Create a session using the assumed role
    sts_client = session.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AssumedRoleSession'
    )

    # Create a new session using the assumed role credentials
    assumed_session = boto3.Session(
        aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
        aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
        aws_session_token=assumed_role['Credentials']['SessionToken'],
        region_name=region
    )

    return assumed_session
