"""
EmailService - Handles email operations for bookings and other domains.

Centralizes email logic so it's not scattered across routes and services.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


class EmailService:
    """Service for sending emails."""

    def __init__(self):
        """Initialize email service with SMTP configuration."""
        from email_utils import SMTP_HOST, SMTP_PORT, SMTP_USER, BASE_URL

        self.SMTP_HOST = SMTP_HOST
        self.SMTP_PORT = SMTP_PORT
        self.SMTP_USER = SMTP_USER
        self.SMTP_PASS = os.getenv("SMTP_PASS")
        self.BASE_URL = BASE_URL

    def send_booking_confirmation(self, to_email, token, booking_data):
        """
        Send booking confirmation email with verification link.

        Args:
            to_email: Email address to send to
            token: Verification token (for email link)
            booking_data: Dictionary with booking details
        """
        verify_url = f"{self.BASE_URL}/api/bookings/verify/{token}"

        movie_title = booking_data.get("movie_details", {}).get("title", "Movie")
        showtime = booking_data.get("movie_details", {}).get("showtime", "N/A")
        total_price = booking_data.get("total_price", 0)
        seat_count = len(booking_data.get("seats", []))

        html = f"""
        <html>
          <body>
            <h2>Booking Confirmation Required</h2>
            <p>Hi there, thank you for your booking!</p>
            <div style="background-color:#f3f4f6; padding:16px; border-radius:8px; margin:16px 0;">
              <p><strong>Movie:</strong> {movie_title}</p>
              <p><strong>Showtime:</strong> {showtime}</p>
              <p><strong>Seats:</strong> {seat_count}</p>
              <p><strong>Total Price:</strong> ${total_price:.2f}</p>
            </div>
            <p>Please click the button below to confirm your booking:</p>
            <a href="{verify_url}"
               style="background-color:#dc2626;color:white;padding:12px 24px;
                      text-decoration:none;border-radius:8px;display:inline-block;">
              Confirm Booking
            </a>
            <p>This link expires in 24 hours.</p>
            <p>If you did not make this booking, ignore this email.</p>
          </body>
        </html>
        """

        return self._send_email(
            to_email=to_email,
            subject=f"Confirm your CineBook booking - {movie_title}",
            html_content=html,
        )

    def _send_email(self, to_email, subject, html_content):
        """
        Send email via SMTP.

        Returns: True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.SMTP_USER
            msg["To"] = to_email
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.SMTP_USER, self.SMTP_PASS)
                server.sendmail(self.SMTP_USER, to_email, msg.as_string())

            print(f"[EMAIL] Booking confirmation sent to {to_email}")
            return True

        except Exception as e:
            print(f"[EMAIL] Error sending email to {to_email}: {e}")
            return False
