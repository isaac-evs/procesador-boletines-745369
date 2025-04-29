import boto3
import logging
from botocore.exceptions import ClientError

from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    SNS_TOPIC_ARN,
    EMAIL_SENDER,
    NEWSLETTER_VIEW_BASE_URL
)

logger = logging.getLogger(__name__)

def get_sns_client():
    return boto3.client(
        'sns',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

def send_email_notification(newsletter_id, recipient_email):
    sns_client = get_sns_client()

    # Newsletter view URL
    view_url = f"{NEWSLETTER_VIEW_BASE_URL}{newsletter_id}?email={recipient_email}"

    # Email subject and message
    subject = "New Newsletter Available"
    message = f"""
    Hello,

    A new newsletter has been generated for you. Click the link below to view it:

    {view_url}

    Thank you,
    Newsletter Service
    """

    try:
        # If we have a topic ARN, publish to the topic
        if SNS_TOPIC_ARN:
            response = sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject=subject,
                MessageAttributes={
                    'email': {
                        'DataType': 'String',
                        'StringValue': recipient_email
                    }
                }
            )
            logger.info(f"Notification sent to SNS topic for newsletter ID: {newsletter_id}")

        # Direct email to recipient
        else:
            response = sns_client.publish(
                TargetArn=f"arn:aws:sns:{AWS_REGION}:*:*",  # Will be replaced with actual ARN
                Message=message,
                Subject=subject,
                MessageStructure='string'
            )
            logger.info(f"Email notification sent directly to {recipient_email} for newsletter ID: {newsletter_id}")

        return response

    except ClientError as e:
        logger.error(f"Error sending SNS notification: {e}")
        raise
