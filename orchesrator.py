from jmespath import search
import boto3
from organization import Organization 
from session_manager import session_generator
from actions.iam_role import delete_iam_role, iam_role_exists
from actions.cloudformation import delete_stacks_with_name, terminate_provisioned_products_with_name
from actions.alias import set_account_alias

REGIONS = ['us-east-1', 'eu-west-1', 'eu-central-1', 'ca-central-1', 'ap-southeast-1']
REGIONS = ['eu-west-1']
# ACCOUNTS = ['103660497589', '183931331824', '423038675222', '515497923579', '']


def main():
    session = boto3.Session()
    organization = Organization(session)
    accounts = organization.get_member_accounts()
    for target_session, account in session_generator(session, accounts, REGIONS):
        if target_session is None:
            continue
        set_account_alias(target_session, account) 

if __name__ == '__main__':
    main()