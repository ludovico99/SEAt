import boto3

# Create SQS client
sqs = boto3.client('sqs')

# Create a SQS queue
# response = sqs.list_queues()
# for queue in response['QueueUrl']:

response = sqs.create_queue(
    QueueName='service_registry_queue',
    Attributes={
        'DelaySeconds': '60',
        'MessageRetentionPeriod': '86400'
    }
)

print(response['QueueUrl'])