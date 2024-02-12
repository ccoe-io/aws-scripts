import boto3

def delete_stacks_with_name(name):
    # Create a CloudFormation client
    client = boto3.client('cloudformation')

    # List all CloudFormation stacks
    response = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])

    # Iterate over the stacks and delete the ones with the specified name
    for stack in response['StackSummaries']:
        if name in stack['StackName']:
            client.delete_stack(StackName=stack['StackName'])
            print(f"Deleted stack: {stack['StackName']}")

# Usage example
delete_stacks_with_name("StackSet-core-deployments-servicecatalog-role")