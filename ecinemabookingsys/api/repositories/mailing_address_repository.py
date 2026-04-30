"""
MailingAddress Repository - Data access for MailingAddress entities.

Handles mailing address queries and operations.
"""

from repositories.base_repository import CRUDRepository


class MailingAddressRepository(CRUDRepository):
    """Repository for MailingAddress entities."""

    def find_by_id(self, address_id):
        """Find mailing address by ID."""
        query = "SELECT * FROM MailingAddress WHERE address_id = %s"
        row = self.execute_query_one(query, (address_id,))
        if not row:
            return None
        return row

    def find_by_user(self, user_id):
        """Find mailing address for a user."""
        query = "SELECT * FROM MailingAddress WHERE user_id = %s"
        return self.execute_query_one(query, (user_id,))

    def create_address(self, user_id, house_number, street, apt, zip_code):
        """
        Create a new mailing address.

        Args:
            user_id: User ID
            house_number: House number
            street: Street address
            apt: Apartment number
            zip_code: ZIP code

        Returns: address_id
        """
        query = """
            INSERT INTO MailingAddress (user_id, house_number, street, apt, zip)
            VALUES (%s, %s, %s, %s, %s)
        """
        address_id = self.execute_insert_get_id(
            query,
            (user_id, house_number, street, apt, zip_code)
        )
        return address_id

    def update_address(self, address_id, house_number, street, apt, zip_code):
        """Update a mailing address."""
        query = """
            UPDATE MailingAddress
            SET house_number = %s, street = %s, apt = %s, zip = %s
            WHERE address_id = %s
        """
        return self.execute_update(query, (house_number, street, apt, zip_code, address_id))

    def save(self, entity):
        """Not implemented - use specific methods."""
        raise NotImplementedError()

    def delete(self, entity):
        """Not implemented - use specific methods."""
        raise NotImplementedError()

    def get_all(self):
        """Not implemented - use find_by_user."""
        raise NotImplementedError()
