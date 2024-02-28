import boto3

def session_generator(session, accounts, regions, role): 
    for account in accounts:
        for region in regions:
            target_session = assume_role(session, account["Id"], region, role)
            yield target_session, account, region

def assume_role(session, account_id, region, role):
    role_arn = f"arn:aws:iam::{account_id}:role/{role}"
    try:
        sts_client = session.client('sts')
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='AssumedRoleSession'
        )
        assumed_session = boto3.Session(
            aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
            aws_session_token=assumed_role['Credentials']['SessionToken'],
            region_name=region
        )
    except Exception as e:
        print(e)
        return

    return assumed_session