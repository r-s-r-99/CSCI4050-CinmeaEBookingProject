from repositories.mailing_address_repository import MailingAddressRepository


class MailingAddressService:
    @staticmethod
    def get_address_by_user(user_id):
        """
        Get mailing address for a user.

        Args:
            user_id: User ID

        Returns: MailingAddress data or None
        """
        if not user_id:
            raise ValueError('User ID is required.')

        try:
            repo = MailingAddressRepository()
            return repo.find_by_user(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def save_address(user_id, house_number, street, apt, zip_code):
        """
        Save or update mailing address for a user.

        Args:
            user_id: User ID
            house_number: House number
            street: Street address
            apt: Apartment number
            zip_code: ZIP code
        """
        # Validate inputs
        if not user_id:
            raise ValueError('User ID is required.')
        if not house_number or not str(house_number).strip():
            raise ValueError('House number is required.')
        if not street or not street.strip():
            raise ValueError('Street is required.')
        if not zip_code or not str(zip_code).strip():
            raise ValueError('ZIP code is required.')

        try:
            repo = MailingAddressRepository()
            repo.save_or_update(user_id, house_number, street, apt, zip_code)
        except Exception as e:
            raise e
