
def delete_iam_role(session, name):
    # Create a CloudFormation client
    client = session.client('iam')
    
    # Delete the IAM role
    response = client.delete_role(RoleName=name)
    
    # Return the response
    return response