import os
from email.message import EmailMessage
import ssl
import smtplib

def send_email(subject: str, body: str, email_receiver: str = "estif78@live.com.mx"):
    """Send an email with the given subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        email_receiver (str): The recipient's email address. Defaults to 'estif78@live.com.mx'.
    """
    email_sender = os.environ.get("email")
    email_password = os.environ.get("emailpassword")

    if not email_sender or not email_password:
        raise ValueError("Environment variables 'email' or 'emailpassword' are not set.")

    # Create the email message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Secure connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

if __name__ == "__main__":
    subject = "variable subject"
    body = "variable body"
    send_email(subject, body)
