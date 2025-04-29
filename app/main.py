import json
import logging
import time
import signal
import sys

from app.services.database_service import init_db, save_newsletter
from app.services.sqs_service import receive_messages, delete_message
from app.services.sns_service import send_email_notification
from app.config import SQS_POLLING_INTERVAL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

running = True

def signal_handler(sig, frame):
    """Handle termination signals"""
    global running
    logger.info("Shutdown signal received. Gracefully shutting down...")
    running = False
    sys.exit(0)

def process_message(message):
    """
    Process a message from the queue

    Args:
        message (dict): The message received from SQS
    """
    try:
        message_body = json.loads(message['Body'])

        email = message_body.get('email')
        content = message_body.get('message')
        image_url = message_body.get('image_url')

        logger.info(f"Processing newsletter for: {email}")

        newsletter = save_newsletter(content, email, image_url)

        send_email_notification(newsletter.id, email)

        delete_message(message['ReceiptHandle'])

        logger.info(f"Newsletter processed successfully: ID={newsletter.id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main():
    """Main application entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Newsletter processor starting up...")

    init_db()

    logger.info(f"Listening for messages on SQS queue. Polling interval: {SQS_POLLING_INTERVAL} seconds")

    while running:
        try:
            messages = receive_messages()

            if messages:
                logger.info(f"Received {len(messages)} messages")

                for message in messages:
                    process_message(message)
            else:
                logger.debug("No messages received")

            time.sleep(SQS_POLLING_INTERVAL)

        except Exception as e:
            logger.error(f"Error in main processing loop: {e}")
            time.sleep(SQS_POLLING_INTERVAL)

if __name__ == "__main__":
    main()
