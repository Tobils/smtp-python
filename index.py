import boto3
from botocore.exceptions import ClientError
import os 
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body, recipients:list, from_email, cc_recipients: list):
    # AWS SES configuration
    region_name = os.getenv("AWS_SES_REGION_NAME")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Create an SES client
    ses_client = boto3.client('ses', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Specify the sender's and recipient's email addresses
    sender = from_email

    # Specify the email headers
    subject = subject

    # Create the email body
    body_text = body
    body_html = f'<html><head></head><body><p>{body}</p></body></html>'

    # Specify the character set for the email
    charset = 'UTF-8'

    try:
        # Send the email
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipients],
                'CcAddresses': [cc_recipients]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")

# Example usage
send_email(
    subject='Hello from AWS SES',
    body='This is a test email sent using AWS SES and Python.',
    recipients=['suhada@gmail.com'],
    cc_recipients=['suhada@mail.com'],
    from_email=os.getenv("DEFAULT_FROM_EMAIL")
)

