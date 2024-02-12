import boto3

def disable_securityhub_control(session, control_name):
    securityhub_client = session.client('securityhub')
    
    response = securityhub_client.batch_disable_standards(
        StandardsSubscriptionRequests=[
            {
                'StandardsArn': 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0',
                'ControlId': control_name
            }
        ]
    )
    
    return response
