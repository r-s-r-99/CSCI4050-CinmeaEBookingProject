from abc import ABC, abstractmethod
from models.base import BaseModel
import bcrypt

class User(BaseModel, ABC):
    def __init__(self, user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status, **kwargs):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.role = role
        self.promo_subscribed = promo_subscribed
        self.account_status = account_status

    @abstractmethod
    def to_dict(self):
        pass

    def check_password(self, password):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM User WHERE user_id = %s", (self.user_id,))
                row = cursor.fetchone()
            return bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8'))
        finally:
            conn.close()

    def update_password(self, new_password):
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE User SET password = %s WHERE user_id = %s", (hashed, self.user_id))
                conn.commit()
        finally:
            conn.close()

    def activate(self):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE User SET account_status = 'Active' WHERE user_id = %s", (self.user_id,))
                conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_email(cls, email):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User WHERE email = %s
                """, (email,))
                row = cursor.fetchone()
            if not row:
                return None
            # Return the correct subclass based on role
            if row['role'] == 'admin':
                return Admin(**row)
            return Customer(**row)
        finally:
            conn.close()