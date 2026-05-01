"""
User Repository - Data access for User entities and password reset tokens.

Handles user queries and password reset token management.
"""

import bcrypt
from repositories.base_repository import CRUDRepository


class UserRepository(CRUDRepository):
    """Repository for User entities."""

    def find_by_email(self, email):
        """Find user by email. Returns dict with user_id and first_name or None."""
        query = "SELECT user_id, first_name FROM User WHERE email = %s"
        return self.execute_query_one(query, (email,))

    def find_by_id(self, user_id):
        """Find user by ID."""
        query = "SELECT user_id, email, first_name, last_name, role FROM User WHERE user_id = %s"
        return self.execute_query_one(query, (user_id,))

    def find_by_id_full(self, user_id):
        """Find user by ID with all fields."""
        query = """
            SELECT user_id, password, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
            FROM User WHERE user_id = %s
        """
        return self.execute_query_one(query, (user_id,))

    def find_by_email_full(self, email):
        """Find user by email with password and role for login."""
        query = """
            SELECT user_id, password, role, email
            FROM User WHERE email = %s
        """
        return self.execute_query_one(query, (email,))

    def find_for_login(self, email):
        """Find user for login with account status."""
        query = """
            SELECT user_id, email, password, account_status, role
            FROM User WHERE email = %s
        """
        return self.execute_query_one(query, (email,))

    def create_user(self, email, password, first_name, last_name, phone_number, promo_subscribed=False):
        """
        Create a new user with hashed password.

        Args:
            email: User email
            password: Plain text password (will be hashed)
            first_name: First name
            last_name: Last name
            phone_number: Phone number
            promo_subscribed: Whether user subscribed to promotions

        Returns: user_id of created user
        """
        # Check if email already exists
        existing = self.find_by_email(email)
        if existing:
            raise ValueError('Email already registered.')

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert user
        query = """
            INSERT INTO User (email, password, first_name, last_name, phone_number, promo_subscribed, account_status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Inactive')
        """
        user_id = self.execute_insert_get_id(
            query,
            (email, hashed_password, first_name, last_name, phone_number, promo_subscribed)
        )
        return user_id

    def update_password(self, user_id, hashed_password):
        """Update user's password."""
        query = "UPDATE User SET password = %s WHERE user_id = %s"
        return self.execute_update(query, (hashed_password, user_id))

    def activate_user(self, user_id):
        """Activate user account."""
        query = "UPDATE User SET account_status = 'Active' WHERE user_id = %s"
        return self.execute_update(query, (user_id,))

    def save(self, entity):
        """Not implemented for User (use specific update methods)."""
        raise NotImplementedError("Use update_password() or specific user update methods")

    def delete(self, entity):
        """Not implemented for User."""
        raise NotImplementedError("User deletion not supported")

    def get_all(self):
        """Not implemented - use specific queries."""
        raise NotImplementedError("Use specific query methods")


class PasswordResetTokenRepository(CRUDRepository):
    """Repository for password reset tokens."""

    def create_token(self, user_id, token, expires_at, token_type='password_reset'):
        """
        Create a new token (for password reset or email confirmation).

        Args:
            user_id: User ID
            token: Token string
            expires_at: Expiration datetime
            token_type: 'password_reset' or 'email_confirmation'
        """
        query = """
            INSERT INTO PasswordResetToken (user_id, token, expires_at, type)
            VALUES (%s, %s, %s, %s)
        """
        self.execute_update(query, (user_id, token, expires_at, token_type))

    def find_by_token(self, token, token_type=None):
        """
        Find token record by token string.

        Args:
            token: Token string
            token_type: Optional filter by type ('password_reset' or 'email_confirmation')

        Returns: Dict with user_id, expires_at, used, type or None
        """
        if token_type:
            query = """
                SELECT user_id, expires_at, used, type
                FROM PasswordResetToken
                WHERE token = %s AND type = %s
            """
            return self.execute_query_one(query, (token, token_type))
        else:
            query = """
                SELECT user_id, expires_at, used, type
                FROM PasswordResetToken
                WHERE token = %s
            """
            return self.execute_query_one(query, (token,))

    def mark_as_used(self, token):
        """Mark token as used."""
        query = "UPDATE PasswordResetToken SET used = TRUE WHERE token = %s"
        return self.execute_update(query, (token,))

    def delete_by_token(self, token):
        """Delete a reset token."""
        query = "DELETE FROM PasswordResetToken WHERE token = %s"
        return self.execute_update(query, (token,))

    def find_by_id(self, token_id):
        """Not implemented."""
        raise NotImplementedError()

    def save(self, entity):
        """Not implemented."""
        raise NotImplementedError()

    def delete(self, entity):
        """Not implemented."""
        raise NotImplementedError()

    def get_all(self):
        """Not implemented."""
        raise NotImplementedError()

