
def delete_iam_role(session, name):
    # Create a CloudFormation client
    client = session.client('iam')
    
    # Delete the IAM role
    response = client.delete_role(RoleName=name)
    
    # Return the response
    return response

def iam_role_exists(session, name):
    # Create an IAM client
    client = session.client('iam')
    
    # List all IAM roles using pagination
    paginator = client.get_paginator('list_roles')
    response_iterator = paginator.paginate()
    
    # Check if the role exists
    for response in response_iterator:
        for role in response['Roles']:
            if role['RoleName'] == name:
                return True
    
    return False