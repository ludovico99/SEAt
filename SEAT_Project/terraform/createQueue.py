import boto3
import json

def createQueue ():
    # Create SQS client
    sqs = boto3.client('sqs',region_name='us-east-1')

    # Create a SQS queue
    queue_name = "service_registry_queue"
    try:
        response = sqs.get_queue_url(QueueName=queue_name)
        queue = str(response['QueueUrl']).split('/')     
        print(json.dumps({"queue":queue[-1]}))
    except sqs.exceptions.QueueDoesNotExist:
        response = sqs.create_queue(
                QueueName=queue_name,
                Attributes={
                    'DelaySeconds': '60',
                    'MessageRetentionPeriod': '86400'
                }
            )
        queue = str(response['QueueUrl']).split('/')
        print(json.dumps({"queue":queue[-1]}))
   
createQueue()
        