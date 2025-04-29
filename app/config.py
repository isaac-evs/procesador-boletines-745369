import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL","https://sqs.us-east-1.amazonaws.com/266735803756/cola-boletines")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "cola-boletines")
SQS_POLLING_INTERVAL = int(os.getenv("SQS_POLLING_INTERVAL", "10"))

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:266735803756:newsletter")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "no-reply@example.com")

DB_HOST = os.getenv("DB_HOST", "newsletter-postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "newsletter_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

NEWSLETTER_VIEW_BASE_URL = os.getenv("NEWSLETTER_VIEW_BASE_URL", "http://54.91.82.217:8000/newsletters/")
