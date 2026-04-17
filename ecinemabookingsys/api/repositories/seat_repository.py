"""
Seat Repository - Data access for Seat entities.

Extracted from models/seat.py - handles all database queries for seats.
Returns Seat domain objects, never dicts.
"""

from repositories.base_repository import CRUDRepository


class SeatRepository(CRUDRepository):
    """
    Repository for Seat entities.

    Responsibilities:
    - Find seats by ID, number/room, or room
    - Always returns Seat domain objects, never dicts
    """

    def find_by_id(self, seat_id):
        """
        Find seat by ID.

        Returns: Seat object or None
        """
        from models.seat import Seat

        query = "SELECT * FROM Seat WHERE seat_id = %s"
        row = self.execute_query_one(query, (seat_id,))
        return Seat(**row) if row else None

    def find_by_number_and_room(self, seat_number, room_id):
        """
        Find seat by seat number (e.g., 'A1') and room ID.

        Args:
            seat_number: Seat number string (e.g., 'A1')
            room_id: ID of the room

        Returns: Seat object or None
        """
        from models.seat import Seat

        query = """
            SELECT * FROM Seat
            WHERE seat_number = %s AND room_id = %s
        """
        row = self.execute_query_one(query, (seat_number, room_id))
        return Seat(**row) if row else None

    def find_by_room(self, room_id):
        """
        Find all seats in a room.

        Args:
            room_id: ID of the room

        Returns: List of Seat objects
        """
        from models.seat import Seat

        query = "SELECT * FROM Seat WHERE room_id = %s ORDER BY seat_number"
        rows = self.execute_query(query, (room_id,))
        return [Seat(**row) for row in rows]

    # Abstract method implementations (required by BaseRepository)
    def save(self, seat):
        """Save seat (insert or update). Not typically used for seats."""
        raise NotImplementedError("Seat repository is read-only")

    def delete(self, seat):
        """Delete seat. Not typically used for seats."""
        raise NotImplementedError("Seat repository is read-only")

    def get_all(self):
        """Get all seats. Use find_by_room() instead."""
        raise NotImplementedError("Use find_by_room() to get seats in a specific room")
