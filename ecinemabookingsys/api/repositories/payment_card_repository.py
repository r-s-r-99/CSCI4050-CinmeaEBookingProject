"""
PaymentCard Repository - Data access for PaymentCard entities.

Extracted from models/payment_card.py - handles all database queries for payment cards.
Returns PaymentCard domain objects, never dicts.
Handles encryption/decryption of sensitive card data.
"""

from repositories.base_repository import CRUDRepository
from encryption import encrypt, decrypt


class PaymentCardRepository(CRUDRepository):
    """
    Repository for PaymentCard entities.

    Responsibilities:
    - Find cards by ID or user
    - Save/delete cards with encrypted data
    - Always returns PaymentCard domain objects, never dicts
    - Handles encryption/decryption in database layer
    """

    def find_by_id(self, card_id):
        """
        Find payment card by ID.

        Returns: PaymentCard object or None
        """
        from models.payment_card import PaymentCard

        query = "SELECT * FROM PaymentCard WHERE card_id = %s"
        row = self.execute_query_one(query, (card_id,))
        return PaymentCard(**row) if row else None

    def find_by_user(self, user_id):
        """
        Find all payment cards for a user.

        Args:
            user_id: User ID

        Returns: List of PaymentCard objects
        """
        from models.payment_card import PaymentCard

        query = "SELECT * FROM PaymentCard WHERE user_id = %s"
        rows = self.execute_query(query, (user_id,))
        return [PaymentCard(**row) for row in rows]

    def count_by_user(self, user_id):
        """
        Count payment cards for a user.

        Used to validate card limits, etc.

        Args:
            user_id: User ID

        Returns: Number of cards
        """
        query = "SELECT COUNT(*) AS cnt FROM PaymentCard WHERE user_id = %s"
        row = self.execute_query_one(query, (user_id,))
        return row['cnt'] if row else 0

    def get_all(self):
        """
        Get all payment cards (admin use).

        Returns: List of PaymentCard objects
        """
        from models.payment_card import PaymentCard

        query = "SELECT * FROM PaymentCard ORDER BY user_id, card_id"
        rows = self.execute_query(query)
        return [PaymentCard(**row) for row in rows]

    # Abstract method implementations (required by BaseRepository)
    def save(self, card):
        """
        Save payment card (insert or update).

        Handles both PaymentCard objects and dicts for backward compatibility.
        Encrypts card_number and cvv before storing.

        Args:
            card: PaymentCard domain object or dict

        Returns: The saved card with ID populated (if insert)
        """
        from models.payment_card import PaymentCard

        # Handle both PaymentCard objects and dicts
        card_id = getattr(card, 'card_id', None) or card.get('card_id')
        user_id = getattr(card, 'user_id', None) or card.get('user_id')
        card_name = getattr(card, 'card_name', None) or card.get('card_name')
        card_number = getattr(card, 'card_number', None) or card.get('card_number')
        cvv = getattr(card, 'cvv', None) or card.get('cvv')
        expiration_date = getattr(card, 'expiration_date', None) or card.get('expiration_date')

        if card_id:
            # Update
            query = """
                UPDATE PaymentCard
                SET card_name = %s, card_number = %s, cvv = %s, expiration_date = %s
                WHERE card_id = %s AND user_id = %s
            """
            self.execute_update(
                query,
                (
                    card_name,
                    encrypt(card_number),
                    encrypt(cvv),
                    expiration_date,
                    card_id,
                    user_id,
                ),
            )
        else:
            # Insert
            query = """
                INSERT INTO PaymentCard (user_id, card_name, card_number, cvv, expiration_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            card_id = self.execute_insert_get_id(
                query,
                (
                    user_id,
                    card_name,
                    encrypt(card_number),
                    encrypt(cvv),
                    expiration_date,
                ),
            )
            if isinstance(card, PaymentCard):
                card.card_id = card_id
            elif isinstance(card, dict):
                card['card_id'] = card_id

        return card

    def delete(self, card):
        """
        Delete payment card.

        Handles both PaymentCard objects and dicts.

        Args:
            card: PaymentCard domain object or dict

        Returns: True if successful
        """
        card_id = getattr(card, 'card_id', None) or card.get('card_id')
        user_id = getattr(card, 'user_id', None) or card.get('user_id')

        query = "DELETE FROM PaymentCard WHERE card_id = %s AND user_id = %s"
        self.execute_update(query, (card_id, user_id))
        return True
