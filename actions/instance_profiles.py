from botocore.exceptions import ClientError


def check_instance_profiles(session, account, dry_run):
    iam_client = session.client('iam')
    admin_profiles = {}
    # Get all instance profiles
    paginator = iam_client.get_paginator('list_instance_profiles')
    for page in paginator.paginate():
        for instance_profile in page['InstanceProfiles']:
            profile_name = instance_profile['InstanceProfileName']
            # print(f"\nChecking instance profile: {profile_name}")

            # Get roles associated with the profile and check for AdminstratorAccess
            admin_roles = []
            try:
                for associated_role in instance_profile['Roles']:
                    role_name = associated_role['RoleName']
                    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
                    for policy in attached_policies['AttachedPolicies']:
                        if policy['PolicyArn'] == 'arn:aws:iam::aws:policy/AdministratorAccess':
                            admin_roles.append(role_name)
                            break  # Stop checking policies once AdminstratorAccess is found
            except ClientError as error:
                print(f"Error checking roles for profile {profile_name}: {error}")
            admin_profiles[profile_name] = admin_roles
    print(f"--------- {account['Name']} ---------")
    for profile, roles in admin_profiles.items():
        print(f"{profile}: {roles}")