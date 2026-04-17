"""
Promotion Repository - Data access for Promotion entities.

Handles all database queries for discount promotions/promo codes.
Returns Promotion domain objects, never dicts.
"""

from datetime import datetime
from repositories.base_repository import CRUDRepository


class PromotionRepository(CRUDRepository):
    """
    Repository for Promotion entities.

    Responsibilities:
    - Find promotions by ID or promo code
    - Find active promotions (within date range)
    - Always returns Promotion domain objects, never dicts
    """

    def find_by_id(self, promotion_id):
        """
        Find promotion by ID.

        Returns: Promotion object or None
        """
        from models.promotion import Promotion

        query = """
            SELECT promotion_id, code, discount_percentage, start_date, end_date, tickets_available
            FROM Promotion
            WHERE promotion_id = %s
        """
        row = self.execute_query_one(query, (promotion_id,))
        return Promotion(**row) if row else None

    def find_by_code(self, code):
        """
        Find promotion by promo code.

        Used during booking validation to apply promo codes.

        Args:
            code: Promo code string (e.g., 'WELCOME10')

        Returns: Promotion object or None
        """
        from models.promotion import Promotion

        query = """
            SELECT promotion_id, code, discount_percentage, start_date, end_date, tickets_available
            FROM Promotion
            WHERE code = %s
        """
        row = self.execute_query_one(query, (code,))
        return Promotion(**row) if row else None

    def find_active(self):
        """
        Find all currently valid promotions.

        Returns promotions where:
        - start_date <= today <= end_date
        - tickets_available > 0 (if specified)

        Returns: List of Promotion objects
        """
        from models.promotion import Promotion

        query = """
            SELECT promotion_id, code, discount_percentage, start_date, end_date, tickets_available
            FROM Promotion
            WHERE (start_date IS NULL OR start_date <= CURDATE())
              AND (end_date IS NULL OR end_date >= CURDATE())
            ORDER BY discount_percentage DESC
        """
        rows = self.execute_query(query)
        return [Promotion(**row) for row in rows]

    def get_all(self):
        """
        Get all promotions (active and inactive).

        Returns: List of Promotion objects
        """
        from models.promotion import Promotion

        query = """
            SELECT promotion_id, code, discount_percentage, start_date, end_date, tickets_available
            FROM Promotion
            ORDER BY start_date DESC
        """
        rows = self.execute_query(query)
        return [Promotion(**row) for row in rows]

    # Abstract method implementations (required by BaseRepository)
    def save(self, promotion):
        """
        Save promotion (insert or update).

        Args:
            promotion: Promotion domain object

        Returns: The saved promotion with ID populated
        """
        if promotion.promotion_id:
            # Update
            query = """
                UPDATE Promotion
                SET code = %s, discount_percentage = %s, start_date = %s, end_date = %s, tickets_available = %s
                WHERE promotion_id = %s
            """
            self.execute_update(
                query,
                (
                    promotion.code,
                    promotion.discount_percentage,
                    promotion.start_date,
                    promotion.end_date,
                    promotion.tickets_available,
                    promotion.promotion_id,
                ),
            )
        else:
            # Insert
            query = """
                INSERT INTO Promotion (code, discount_percentage, start_date, end_date, tickets_available)
                VALUES (%s, %s, %s, %s, %s)
            """
            promotion_id = self.execute_insert_get_id(
                query,
                (
                    promotion.code,
                    promotion.discount_percentage,
                    promotion.start_date,
                    promotion.end_date,
                    promotion.tickets_available,
                ),
            )
            promotion.promotion_id = promotion_id

        return promotion

    def delete(self, promotion):
        """
        Delete promotion.

        Args:
            promotion: Promotion domain object

        Returns: True if successful
        """
        query = "DELETE FROM Promotion WHERE promotion_id = %s"
        self.execute_update(query, (promotion.promotion_id,))
        return True
