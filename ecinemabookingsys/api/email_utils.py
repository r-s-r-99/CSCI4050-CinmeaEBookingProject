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
FLASK_URL = os.getenv('FLASK_URL', 'http://localhost:5001')

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
        
def send_reset_email(to_email: str, first_name: str, token: str):
    reset_url = f"{BASE_URL}/reset-password?token={token}"

    html = f"""
    <html>
      <body>
        <h2>Reset your CineBook password</h2>
        <p>Hi {first_name}, we received a request to reset your password.</p>
        <a href="{reset_url}" 
           style="background-color:#dc2626;color:white;padding:12px 24px;
                  text-decoration:none;border-radius:8px;display:inline-block;">
          Reset Password
        </a>
        <p>This link expires in 1 hour.</p>
        <p>If you did not request a password reset, ignore this email.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Reset your CineBook password'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        
def send_profile_update_email(to_email: str, first_name: str, updated_section: str):
    html = f"""
    <html>
      <body>
        <h2>Profile Updated</h2>
        <p>Hi {first_name}, your <strong>{updated_section}</strong> has been updated on your CineBook account.</p>
        <p>If you did not make this change, please reset your password immediately or contact support.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your CineBook profile was updated'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())