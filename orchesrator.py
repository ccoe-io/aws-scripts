from jmespath import search
import boto3
from organization import Organization 
from session_manager import session_generator
from actions.iam_role import delete_iam_role, iam_role_exists
from actions.cloudformation import delete_stacks_with_name, terminate_provisioned_products_with_name

REGIONS = ['us-east-1', 'eu-west-1', 'eu-central-1', 'ca-central-1', 'ap-southeast-1']
REGIONS = ['eu-west-1']
# ACCOUNTS = ['103660497589', '183931331824', '423038675222', '515497923579', '']


def main():
    session = boto3.Session()
    organization = Organization(session)
    accounts = organization.get_member_accounts(ou_id="ou-5f7m-biuvthab")
    # accounts = ACCOUNTS
    for target_session in session_generator(session, accounts, REGIONS):
        # clean_kms_keys(target_session)
        # delete_stacks_with_name(target_session, "StackSet-core-deployments-servicecatalog-role")
        if iam_role_exists(target_session, "service-catalog-platform-exec"):
            # approve = input("Delete IAM role? (y/n): ")
            # if approve == "y":
            print("Deleting IAM role")
            # delete_iam_role(target_session, "service-catalog-platform-exec")    
            delete_stacks_with_name(target_session, "StackSet-core-deployments-servicecatalog-role")
        # print("Cloudformation stack")
        # terminate_provisioned_products_with_name(target_session, "default-kms-cmk")

if __name__ == '__main__':
    main()