import boto3
import boto3

def get_admin_groups(session):
    accounts = []

    # Get all the accounts
    organizations = session.client('organizations')
    response = organizations.list_accounts()
    accounts = response['Accounts']

    # Iterate over each account
    for account in accounts:
        account_id = account['Id']
        account_name = account['Name']
        admin_groups = []

        # Get all the groups in the account
        identitystore = session.client('identitystore')
        response = identitystore.list_groups()
        groups = response['Groups']

        # Check if each group has admin access
        for group in groups:
            group_name = group['GroupName']
            # TODO: Add code to check if each group has admin access
            admin_groups.append(group_name)

        # Add the account and admin groups to the report
        accounts.append({
            'AccountName': account_name,
            'AdminGroups': admin_groups
        })

    return accounts

# Create a Boto3 session
session = boto3.Session()

# Get the report
report = get_admin_groups(session)

# Print the report
for account in report:
    print(f"Account: {account['AccountName']}")
    print("Admin Groups:")
    for group in account['AdminGroups']:
        print(f"- {group}")
    print()
    iam = session.client('iam')
    accounts = []

    # Get all the accounts
    organizations = session.client('organizations')
    response = organizations.list_accounts()
    accounts = response['Accounts']

    # Iterate over each account
    for account in accounts:
        account_id = account['Id']
        account_name = account['Name']
        admin_groups = []

        # Get all the groups in the account
        response = iam.list_groups()
        groups = response['Groups']

        # Check if each group has admin access
        for group in groups:
            group_name = group['GroupName']
            response = iam.list_attached_group_policies(GroupName=group_name)
            policies = response['AttachedPolicies']

            # Check if any policy has admin access
            for policy in policies:
                policy_arn = policy['PolicyArn']
                response = iam.get_policy(PolicyArn=policy_arn)
                policy_document = response['Policy']['Document']
                if 'AdministratorAccess' in policy_document['Statement']:
                    admin_groups.append(group_name)
                    break

        # Add the account and admin groups to the report
        accounts.append({
            'AccountName': account_name,
            'AdminGroups': admin_groups
        })

    return accounts

# Create a Boto3 session
session = boto3.Session()

# Get the report
report = get_admin_groups(session)

# Print the report
for account in report:
    print(f"Account: {account['AccountName']}")
    print("Admin Groups:")
    for group in account['AdminGroups']:
        print(f"- {group}")
    print()
