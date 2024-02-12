import boto3
from organization import Organization 
from session_manager import session_generator
from actions.iam_role import delete_iam_role

REGIONS = ['us-east-1', 'eu-west-1', 'eu-central-1', 'ca-central-1', 'ap-southeast-1']
REGIONS = ['eu-west-1']

def main():
    session = boto3.Session()
    organization = Organization(session)
    accounts = organization.get_member_accounts(ou_id="ou-5f7m-biuvthab")
    print(accounts)
    for target_session in session_generator(session, accounts, REGIONS):
        print("action")
        # clean_kms_keys(target_session)
        # delete_stacks_with_name(target_session, "StackSet-core-deployments-servicecatalog-role")
        approve = input("Delete IAM role? (y/n): ")
        if approve == "y":
            print("Deleting IAM role")
            delete_iam_role(target_session, "mfs-devops-ci-role")    

if __name__ == '__main__':
    main()