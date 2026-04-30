"""
Password Reset Service - Business logic for password reset operations.

Handles:
- Initiating password reset flow
- Validating reset tokens
- Resetting passwords with security
"""

import secrets
import bcrypt
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository, PasswordResetTokenRepository
from email_utils import send_reset_email


class PasswordResetService:
    """Service for password reset operations."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.token_repo = PasswordResetTokenRepository()

    def initiate_password_reset(self, email):
        """
        Initiate password reset flow for an email.

        Args:
            email: Email address to reset password for

        Returns:
            dict: {'success': bool, 'user': user_dict or None}
        """
        # Check if user exists
        user = self.user_repo.find_by_email(email)
        if not user:
            # Return success anyway to avoid email enumeration
            return {'success': True, 'user': None}

        try:
            # Create reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)

            # Store token in database
            self.token_repo.create_token(user['user_id'], token, expires_at)

            # Send email
            send_reset_email(email, user['first_name'], token)

            return {'success': True, 'user': user}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def validate_and_reset_password(self, token, new_password):
        """
        Validate reset token and reset the password.

        Args:
            token: Password reset token
            new_password: New password (plain text)

        Returns:
            dict: {'success': bool, 'error': str or None}
        """
        if not token or not new_password:
            return {'success': False, 'error': 'Token and password are required'}

        # Validate token
        token_record = self.token_repo.find_by_token(token)
        if not token_record:
            return {'success': False, 'error': 'Invalid or expired token'}

        # Check token expiration
        if datetime.utcnow() > token_record['expires_at']:
            return {'success': False, 'error': 'Token has expired'}

        try:
            # Hash new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Update password
            self.user_repo.update_password(token_record['user_id'], hashed_password)

            # Delete token to prevent reuse
            self.token_repo.delete_by_token(token)

            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
