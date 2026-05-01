import bcrypt
from db import get_db


class CustomerRepository:
    @staticmethod
    def create_customer(email, password, first_name, last_name, phone_number, promo_subscribed):
        """Create a new customer with hashed password."""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO User (email, password, first_name, last_name, phone_number, promo_subscribed, account_status, role)
                VALUES (%s, %s, %s, %s, %s, %s, 'Inactive', 'customer')
            """, (email, hashed, first_name, last_name, phone_number, promo_subscribed))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_profile(user_id, first_name, last_name, phone_number, promo_subscribed=None):
        """Update customer profile."""
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE User SET first_name = %s, last_name = %s, phone_number = %s, promo_subscribed = %s
                WHERE user_id = %s
            """, (first_name, last_name, phone_number, promo_subscribed, user_id))
            conn.commit()

