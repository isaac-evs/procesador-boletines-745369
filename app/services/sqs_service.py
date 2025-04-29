import boto3
import json
import logging
from botocore.exceptions import ClientError

from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SQS_QUEUE_NAME

logger = logging.getLogger(__name__)

def get_sqs_client():
    return boto3.client(
        'sqs',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

def get_queue_url():
    sqs_client = get_sqs_client()
    try:
        response = sqs_client.get_queue_url(QueueName=SQS_QUEUE_NAME)
        return response['QueueUrl']
    except ClientError as e:
        logger.error(f"Error getting SQS queue URL: {e}")
        raise

def receive_messages():
    sqs_client = get_sqs_client()
    queue_url = get_queue_url()

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
            VisibilityTimeout=30
        )

        return response.get('Messages', [])

    except ClientError as e:
        logger.error(f"Error receiving messages from SQS: {e}")
        return []

def delete_message(receipt_handle):
    sqs_client = get_sqs_client()
    queue_url = get_queue_url()

    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        logger.info("Message deleted from SQS queue")
    except ClientError as e:
        logger.error(f"Error deleting message from SQS: {e}")
