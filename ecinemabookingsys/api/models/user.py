from abc import ABC, abstractmethod
from email_utils import send_profile_update_email
from models.base import BaseModel
import bcrypt

class User(BaseModel, ABC):
    def __init__(self, user_id=None, password=None, email=None, **kwargs):
        self.user_id = user_id
        self.password = password
        self.email = email

        # Handle extra fields
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    @abstractmethod
    def to_dict(self):
        pass

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def change_password(self, new_password, first_name='there'):
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE User SET password = %s WHERE user_id = %s", (hashed, self.user_id))
                conn.commit()
            self.password = hashed
            send_profile_update_email(self.email, first_name, 'password')
        finally:
            conn.close()

    @classmethod
    def login(cls, email, password):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, password, account_status, role
                    FROM User WHERE email = %s
                """, (email,))
                row = cursor.fetchone()

            print(f"[LOGIN] User found: {row is not None}")
            print(f"[LOGIN] Account status: {row['account_status'] if row else 'N/A'}")

            if not row:
                return None, 'Invalid credentials.'

            if row['account_status'] == 'Inactive':
                return None, 'Please verify your email before logging in.'

            if row['account_status'] == 'Suspended':
                return None, 'Your account has been suspended.'

            password_match = bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8'))
            print(f"[LOGIN] Password match: {password_match}")

            if not password_match:
                return None, 'Invalid credentials.'

            from models.customer import Customer
            from models.admin import Admin

            if row['role'] == 'admin':
                user = Admin.find_by_id(row['user_id'])
            else:
                user = Customer.find_by_id(row['user_id'])

            return user, None

        except Exception as e:
            print(f"[LOGIN] Exception: {e}")
            return None, str(e)
        finally:
            conn.close()

    @staticmethod
    def logout(session):
        session.clear()

    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID and return the appropriate subclass instance (Admin or Customer)"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, password, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User WHERE user_id = %s
                """, (user_id,))
                row = cursor.fetchone()

            if not row:
                return None

            from models.customer import Customer
            from models.admin import Admin

            if row['role'] == 'admin':
                return Admin(**row)
            return Customer(**row)

        finally:
            conn.close()

    @classmethod
    def find_by_email(cls, email):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, password, role, email
                    FROM User WHERE email = %s
                """, (email,))
                row = cursor.fetchone()

            if not row:
                return None

            from models.customer import Customer
            from models.admin import Admin

            if row['role'] == 'admin':
                return Admin.find_by_id(row['user_id'])
            return Customer.find_by_id(row['user_id'])

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