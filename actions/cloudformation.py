def delete_stacks_with_name(session, name):
    # Create a CloudFormation client
    client = session.client('cloudformation')

    # Create a paginator for listing stacks
    paginator = client.get_paginator('list_stacks')

    # List all CloudFormation stacks
    response_iterator = paginator.paginate(StackStatusFilter=['ROLLBACK_COMPLETE', 'CREATE_COMPLETE', 'UPDATE_COMPLETE'])

    # Iterate over the stacks and delete the ones with the specified name
    for page in response_iterator:
        for stack in page['StackSummaries']:
            print(stack['StackName'])
            if name in stack['StackName']:
                client.delete_stack(StackName=stack['StackName'])
                print(f"Deleted stack: {stack['StackName']}")


def terminate_provisioned_products_with_name(session, name):
    # Create a Service Catalog client
    client = session.client('servicecatalog')

    # Scan all provisioned products at the account level
    response = client.scan_provisioned_products(AccessLevelFilter={'Key': 'Account', 'Value': 'self'})
    # Iterate over the provisioned products and terminate the ones with the specified name
    for product in response['ProvisionedProducts']:
        if name in product['Name']:
            client.terminate_provisioned_product(
                ProvisionedProductName=product['Name'],
                TerminateToken='terminate_token'
            )
            print(f"Terminated provisioned product: {product['Name']}")
