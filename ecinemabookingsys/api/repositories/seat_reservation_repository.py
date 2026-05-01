"""
Seat Reservation Repository - Manages temporary seat locks for booking process.

Handles reserving seats during the booking workflow and automatic expiration.
"""

from datetime import datetime, timedelta
from repositories.base_repository import CRUDRepository


class SeatReservationRepository(CRUDRepository):
    """Repository for managing temporary seat reservations/locks."""

    def reserve_seats(self, user_id, showtime_id, seat_ids, duration_minutes=5):
        """Reserve seats for a user during booking process.

        Args:
            user_id: User making the reservation
            showtime_id: Showtime for which seats are reserved
            seat_ids: List of seat IDs to reserve
            duration_minutes: How long to lock seats (default 5 minutes)

        Returns: List of reservation records
        """
        expires_at = datetime.now() + timedelta(minutes=duration_minutes)
        reservations = []

        for seat_id in seat_ids:
            query = """
                INSERT INTO SeatReservation (user_id, showtime_id, seat_id, expires_at)
                VALUES (%s, %s, %s, %s)
            """
            try:
                self.execute_insert_get_id(
                    query,
                    (user_id, showtime_id, seat_id, expires_at)
                )
                reservations.append({
                    'seat_id': seat_id,
                    'user_id': user_id,
                    'showtime_id': showtime_id,
                    'expires_at': expires_at.isoformat()
                })
            except Exception as e:
                print(f"[SEAT_RESERVATION] Error reserving seat {seat_id}: {e}")

        return reservations

    def get_reserved_seats(self, showtime_id):
        """Get all currently reserved (non-expired) seat IDs for a showtime."""
        query = """
            SELECT DISTINCT seat_id
            FROM SeatReservation
            WHERE showtime_id = %s AND expires_at > NOW()
        """
        rows = self.execute_query(query, (showtime_id,))
        return [row["seat_id"] for row in rows]

    def get_user_reservations(self, user_id, showtime_id):
        """Get all active reservations for a user on a specific showtime."""
        query = """
            SELECT seat_id, expires_at
            FROM SeatReservation
            WHERE user_id = %s AND showtime_id = %s AND expires_at > NOW()
        """
        rows = self.execute_query(query, (user_id, showtime_id))
        return [
            {
                'seat_id': row["seat_id"],
                'expires_at': row["expires_at"].isoformat() if row["expires_at"] else None
            }
            for row in rows
        ]

    def release_reservation(self, user_id, showtime_id, seat_id):
        """Release a single seat reservation."""
        query = """
            DELETE FROM SeatReservation
            WHERE user_id = %s AND showtime_id = %s AND seat_id = %s
        """
        self.execute_update(query, (user_id, showtime_id, seat_id))
        return True

    def release_all_reservations(self, user_id, showtime_id):
        """Release all reservations for a user on a showtime."""
        query = """
            DELETE FROM SeatReservation
            WHERE user_id = %s AND showtime_id = %s
        """
        self.execute_update(query, (user_id, showtime_id))
        return True

    def cleanup_expired_reservations(self):
        """Remove all expired reservations (called periodically)."""
        query = "DELETE FROM SeatReservation WHERE expires_at <= NOW()"
        self.execute_update(query)
        return True

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

    def save(self, reservation):
        """Save a reservation (not typically used - use reserve_seats instead)."""
        pass

    def delete(self, reservation):
        """Delete a reservation (not typically used - use release_reservation instead)."""
        pass
