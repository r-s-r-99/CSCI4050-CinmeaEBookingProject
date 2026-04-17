"""
Showroom Repository - Data access for Showroom entities.

Handles all database queries for cinema showrooms/theaters.
Returns Showroom domain objects, never dicts.
"""

from repositories.base_repository import CRUDRepository


class ShowroomRepository(CRUDRepository):
    """
    Repository for Showroom entities.

    Responsibilities:
    - Find showrooms by ID or room number
    - Fetch all showrooms
    - Always returns Showroom domain objects, never dicts
    """

    def find_by_id(self, room_id):
        """
        Find showroom by ID.

        Returns: Showroom object or None
        """
        from models.showroom import Showroom

        query = "SELECT room_id, room_number, number_of_seats FROM Showroom WHERE room_id = %s"
        row = self.execute_query_one(query, (room_id,))
        return Showroom(**row) if row else None

    def find_by_room_number(self, room_number):
        """
        Find showroom by room number.

        Args:
            room_number: Room number (e.g., 1, 2, 3, 4)

        Returns: Showroom object or None
        """
        from models.showroom import Showroom

        query = "SELECT room_id, room_number, number_of_seats FROM Showroom WHERE room_number = %s"
        row = self.execute_query_one(query, (room_number,))
        return Showroom(**row) if row else None

    def get_all(self):
        """
        Get all showrooms.

        Returns: List of Showroom objects
        """
        from models.showroom import Showroom

        query = "SELECT room_id, room_number, number_of_seats FROM Showroom ORDER BY room_number"
        rows = self.execute_query(query)
        return [Showroom(**row) for row in rows]

    # Abstract method implementations (required by BaseRepository)
    def save(self, showroom):
        """
        Save showroom (insert or update).

        Args:
            showroom: Showroom domain object

        Returns: The saved showroom with ID populated
        """
        if showroom.room_id:
            # Update
            query = """
                UPDATE Showroom
                SET room_number = %s, number_of_seats = %s
                WHERE room_id = %s
            """
            self.execute_update(
                query,
                (showroom.room_number, showroom.number_of_seats, showroom.room_id),
            )
        else:
            # Insert
            query = """
                INSERT INTO Showroom (room_number, number_of_seats)
                VALUES (%s, %s)
            """
            room_id = self.execute_insert_get_id(
                query,
                (showroom.room_number, showroom.number_of_seats),
            )
            showroom.room_id = room_id

        return showroom

    def delete(self, showroom):
        """
        Delete showroom.

        Args:
            showroom: Showroom domain object

        Returns: True if successful
        """
        query = "DELETE FROM Showroom WHERE room_id = %s"
        self.execute_update(query, (showroom.room_id,))
        return True
