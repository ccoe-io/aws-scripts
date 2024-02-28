import asyncio
import functools
from jmespath import search
import boto3
from aws.organization import Organization 
from aws.session_manager import session_generator

from actions.iam_role import delete_iam_role, iam_role_exists
from actions.cloudformation import delete_stacks_with_name, terminate_provisioned_products_with_name
from actions.alias import set_account_alias
from actions.read_sample import read_account_alias

REGIONS = ['us-east-1', 'eu-west-1', 'eu-central-1', 'ca-central-1', 'ap-southeast-1']
REGIONS = ['eu-west-1']
ACCOUNTS = []

TARGET_ROLE_NAME = 'AWSControlTowerExecution'

ACTION = read_account_alias
DRY_RUN = False



def process_account_region(target_session, account, region):
    print(' ')
    print(f'{account["Id"]} {region} {account["Name"]}', end="   ")
    if target_session is None:
        return
    try:
        ACTION(target_session, account, dry_run=DRY_RUN) 
    except Exception as e:
        print(f"Error: {e}")
        return

async def main():
    session = boto3.Session()
    organization = Organization(session)
    accounts = ACCOUNTS or organization.get_accounts(ou_id="ou-5f7m-mlujjh8x")
    # print(accounts) 
    loop = asyncio.get_running_loop()

    res = await asyncio.gather(
        *[
            loop.run_in_executor(None, functools.partial(process_account_region, target_session, account, region))
            for target_session, account, region in session_generator(session, accounts, REGIONS, TARGET_ROLE_NAME)
        ]
    ) 

if __name__ == '__main__':
    asyncio.run(main())