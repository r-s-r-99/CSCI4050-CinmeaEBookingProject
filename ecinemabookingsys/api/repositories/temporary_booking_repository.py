"""
TemporaryBookingRepository - Data access for temporary booking sessions.

Handles all database operations for temporary bookings that expire after payment.
"""

from repositories.base_repository import CRUDRepository
import json


class TemporaryBookingRepository(CRUDRepository):
    """Repository for temporary booking sessions."""

    def find_by_token(self, token):
        """
        Find temporary booking by token if it hasn't expired.

        Args:
            token: Temporary booking token

        Returns:
            Dictionary with booking_data, or None if not found or expired
        """
        try:
            query = """
                SELECT booking_data, expires_at
                FROM temporary_bookings
                WHERE token = %s AND expires_at > NOW()
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (token,))
                row = cursor.fetchone()

            if row:
                booking_data = json.loads(row["booking_data"])
                return booking_data
            return None
        except Exception as e:
            print(f"[TEMP_BOOKING] Could not find temp booking: {e}")
            return None

    def save(self, token, user_id, booking_data, expires_at):
        """
        Save temporary booking to database.

        Args:
            token: Unique temporary booking token
            user_id: ID of user
            booking_data: Dictionary with showtime_id, seats, email, total_price
            expires_at: datetime when this booking expires

        Returns:
            True if saved successfully, False if table doesn't exist
        """
        try:
            query = """
                INSERT INTO temporary_bookings (token, user_id, booking_data, expires_at)
                VALUES (%s, %s, %s, %s)
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (token, user_id, json.dumps(booking_data), expires_at),
                )
                conn.commit()
            return True

        except Exception as e:
            # Table doesn't exist - that's okay, session storage is fallback
            print(f"[TEMP_BOOKING] Could not store in DB: {e}. Using session storage.")
            return False

    def delete(self, token):
        """
        Delete temporary booking record.

        Args:
            token: Temporary booking token to delete

        Returns:
            True if deleted successfully
        """
        try:
            query = "DELETE FROM temporary_bookings WHERE token = %s"
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (token,))
                conn.commit()
            return True

        except Exception as e:
            print(f"[TEMP_BOOKING] Could not delete temp booking: {e}")
            return False

    # Abstract method implementations (not used for temporary bookings)
    def find_by_id(self, temp_booking_id):
        """Find temporary booking by ID (not typically used)."""
        raise NotImplementedError("Use token-based lookup instead")

    def get_all(self):
        """Get all temporary bookings (not typically used)."""
        raise NotImplementedError("Not implemented for temporary bookings")
