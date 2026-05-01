"""
SeatReservationRepository - Data access for seat reservations.

Handles locking seats for a limited time during the booking process.
"""

from repositories.base_repository import CRUDRepository
from datetime import datetime, timedelta
import json


class SeatReservationRepository(CRUDRepository):
    """Repository for seat reservations (temporary locks)."""

    def _ensure_table(self):
        """Create the seat_reservations table if it doesn't exist."""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS seat_reservations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    showtime_id INT NOT NULL,
                    seat_id VARCHAR(10) NOT NULL,
                    session_token VARCHAR(64) NOT NULL,
                    reserved_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NOT NULL,
                    INDEX idx_showtime_expires (showtime_id, expires_at),
                    INDEX idx_session_token (session_token),
                    UNIQUE KEY unique_seat_showtime (showtime_id, seat_id)
                )
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error creating table: {e}")

    def find_active_by_showtime(self, showtime_id):
        """
        Get all active (non-expired) seat reservations for a showtime.
        
        Args:
            showtime_id: ID of the showtime
            
        Returns:
            List of active seat reservations
        """
        self._ensure_table()
        
        try:
            query = """
                SELECT seat_id, reserved_at, expires_at, session_token
                FROM seat_reservations
                WHERE showtime_id = %s AND expires_at > NOW()
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (showtime_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error fetching active reservations: {e}")
            return []

    def find_by_seat_and_showtime(self, seat_id, showtime_id):
        """
        Find an active reservation for a specific seat and showtime.
        
        Args:
            seat_id: ID of the seat
            showtime_id: ID of the showtime
            
        Returns:
            Reservation dict or None
        """
        self._ensure_table()
        
        try:
            query = """
                SELECT seat_id, reserved_at, expires_at, session_token
                FROM seat_reservations
                WHERE seat_id = %s AND showtime_id = %s AND expires_at > NOW()
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (seat_id, showtime_id))
                return cursor.fetchone()
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error fetching reservation: {e}")
            return None

    def create_reservation(self, showtime_id, seat_ids, session_token, expires_at):
        """
        Create seat reservations for a session.
        
        Args:
            showtime_id: ID of the showtime
            seat_ids: List of seat IDs to reserve
            session_token: Unique token for this reservation session
            expires_at: When the reservation expires
            
        Returns:
            True if successful, False otherwise
        """
        self._ensure_table()
        
        try:
            query = """
                INSERT INTO seat_reservations (showtime_id, seat_id, session_token, reserved_at, expires_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                for seat_id in seat_ids:
                    cursor.execute(
                        query,
                        (showtime_id, seat_id, session_token, datetime.now(), expires_at),
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error creating reservation: {e}")
            return False

    def release_by_session(self, session_token):
        """
        Release all reservations for a session token.
        
        Args:
            session_token: The session token to release
            
        Returns:
            True if successful
        """
        self._ensure_table()
        
        try:
            query = """
                DELETE FROM seat_reservations
                WHERE session_token = %s
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (session_token,))
                conn.commit()
            return True
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error releasing reservation: {e}")
            return False

    def extend_reservation(self, session_token, new_expires_at):
        """
        Extend the expiration time for a session's reservations.
        
        Args:
            session_token: The session token
            new_expires_at: New expiration time
            
        Returns:
            True if successful
        """
        self._ensure_table()
        
        try:
            query = """
                UPDATE seat_reservations
                SET expires_at = %s
                WHERE session_token = %s AND expires_at > NOW()
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query, (new_expires_at, session_token))
                conn.commit()
            return True
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error extending reservation: {e}")
            return False

    def cleanup_expired(self):
        """
        Clean up expired reservations (can be called periodically).
        
        Returns:
            Number of reservations cleaned up
        """
        self._ensure_table()
        
        try:
            query = """
                DELETE FROM seat_reservations
                WHERE expires_at <= NOW()
            """
            from db import get_db

            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"[SEAT_RESERVATION] Error cleaning up: {e}")
            return 0
    def delete(self, reservation):
        """Delete a reservation (not typically used - use release_reservation instead)."""
        pass
    def save(self, reservation):
        """Save a reservation (not typically used - use reserve_seats instead)."""
        pass
    def get_all(self):
        """Get all reservations (required by abstract interface)."""
        query = "SELECT * FROM SeatReservation"
        rows = self.execute_query(query)
        return rows

    def find_by_id(self, reservation_id):
        """Find a reservation by ID."""
        query = "SELECT * FROM SeatReservation WHERE reservation_id = %s"
        row = self.execute_query_one(query, (reservation_id,))
        return row
