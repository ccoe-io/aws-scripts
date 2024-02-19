import boto3

def session_generator(session, accounts, regions): 
    for account in accounts:
        for region in regions:
            print(account["Id"] + "  " + account["Name"], end="   ")
            print("Region: " + region)
            yield assume_role(session, account["Id"], region)


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