import bcrypt
from repositories.user_repository import UserRepository
from email_utils import send_profile_update_email


class UserService:
    @staticmethod
    def change_password(user_id, email, new_password, first_name='there'):
        """
        Change user password with validation and email notification.

        Args:
            user_id: User ID
            email: User email
            new_password: New plain text password
            first_name: User first name for email
        """
        if not user_id:
            raise ValueError('User ID is required.')
        if not new_password or len(new_password) < 6:
            raise ValueError('Password must be at least 6 characters.')

        try:
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            repo = UserRepository()
            repo.update_password(user_id, hashed)
            send_profile_update_email(email, first_name, 'password')
        except Exception as e:
            raise e

    @staticmethod
    def login(email, password):
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns: (User object, error_message) tuple
        """
        if not email or not email.strip():
            raise ValueError('Email is required.')
        if not password or not password.strip():
            raise ValueError('Password is required.')

        try:
            repo = UserRepository()
            row = repo.find_for_login(email)

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

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns: User object or None
        """
        if not user_id:
            raise ValueError('User ID is required.')

        try:
            repo = UserRepository()
            row = repo.find_by_id_full(user_id)

            if not row:
                return None

            from models.customer import Customer
            from models.admin import Admin

            if row['role'] == 'admin':
                return Admin(**row)
            return Customer(**row)

        except Exception as e:
            print(f"[GET_USER_BY_ID] Exception: {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email.

        Args:
            email: User email

        Returns: User object or None
        """
        if not email or not email.strip():
            raise ValueError('Email is required.')

        try:
            repo = UserRepository()
            row = repo.find_by_email_full(email)

            if not row:
                return None

            from models.customer import Customer
            from models.admin import Admin

            if row['role'] == 'admin':
                return Admin.find_by_id(row['user_id'])
            return Customer.find_by_id(row['user_id'])

        except Exception as e:
            print(f"[GET_USER_BY_EMAIL] Exception: {e}")
            return None

    @staticmethod
    def activate_user(user_id):
        """
        Activate user account.

        Args:
            user_id: User ID
        """
        if not user_id:
            raise ValueError('User ID is required.')

        try:
            repo = UserRepository()
            repo.activate_user(user_id)
        except Exception as e:
            raise e
