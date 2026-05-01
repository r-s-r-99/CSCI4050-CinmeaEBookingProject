from repositories.customer_repository import CustomerRepository


class CustomerService:
    @staticmethod
    def create_customer(email, password, first_name, last_name, phone_number, promo_subscribed):
        """
        Create a new customer with validation.

        Args:
            email: Customer email
            password: Plain text password
            first_name: First name
            last_name: Last name
            phone_number: Phone number
            promo_subscribed: Promotion subscription flag

        Returns: user_id of created customer
        """
        # Validate inputs
        if not email or not email.strip():
            raise ValueError('Email is required.')
        if not password or len(password) < 6:
            raise ValueError('Password must be at least 6 characters.')
        if not first_name or not first_name.strip():
            raise ValueError('First name is required.')
        if not last_name or not last_name.strip():
            raise ValueError('Last name is required.')
        if not phone_number or not phone_number.strip():
            raise ValueError('Phone number is required.')

        try:
            user_id = CustomerRepository.create_customer(
                email, password, first_name, last_name, phone_number, promo_subscribed
            )
            return user_id
        except Exception as e:
            raise e

    @staticmethod
    def update_customer_profile(user_id, first_name, last_name, phone_number, promo_subscribed=None):
        """
        Update customer profile with validation.

        Args:
            user_id: Customer user ID
            first_name: First name
            last_name: Last name
            phone_number: Phone number
            promo_subscribed: Promotion subscription flag
        """
        # Validate inputs
        if not first_name or not first_name.strip():
            raise ValueError('First name is required.')
        if not last_name or not last_name.strip():
            raise ValueError('Last name is required.')
        if not phone_number or not phone_number.strip():
            raise ValueError('Phone number is required.')

        try:
            CustomerRepository.update_profile(
                user_id, first_name, last_name, phone_number, promo_subscribed
            )
        except Exception as e:
            raise e
