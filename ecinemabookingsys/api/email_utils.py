import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')       # your gmail
SMTP_PASS = os.getenv('SMTP_PASS')       # your app password
BASE_URL  = os.getenv('BASE_URL', 'http://localhost:5000')

def send_confirmation_email(to_email: str, first_name: str, token: str):
    confirm_url = f"{BASE_URL}/api/confirm-email/{token}"

    html = f"""
    <html>
      <body>
        <h2>Welcome to CineBook, {first_name}!</h2>
        <p>Thanks for registering. Click the button below to activate your account:</p>
        <a href="{confirm_url}" 
           style="background-color:#dc2626;color:white;padding:12px 24px;
                  text-decoration:none;border-radius:8px;display:inline-block;">
          Confirm Email
        </a>
        <p>This link expires in 24 hours.</p>
        <p>If you did not register, ignore this email.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Confirm your CineBook account'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())