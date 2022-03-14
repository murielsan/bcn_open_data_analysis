from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from datetime import date
from dotenv import load_dotenv
import re
import os
import base64

load_dotenv()

def send_email(dest, pdf_file):
    # First, validate email
    pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if not re.match(pattern, dest):
        return "Wrong email address"

    print("Passed validation")
    message = Mail(
            from_email=os.getenv("EMAIL"),
            to_emails=dest,
            subject='Streamlit exported charts',
            html_content='<strong>Please find attached the requested file</strong>')

    with open(pdf_file, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName(f"Output{date.today()}.pdf")
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('Display charts')
    message.attachment = attachment


    try:
        sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return("Email sent!")
    except Exception as e:
        return "Error sending mail"