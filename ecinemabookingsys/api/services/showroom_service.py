"""
Showroom Service - Business logic for showroom operations.

Handles showroom queries and decoration.
"""

from repositories.showroom_repository import ShowroomRepository


class ShowroomService:
    """Service for showroom operations."""

    def __init__(self):
        self.showroom_repo = ShowroomRepository()

    def get_all_showrooms_decorated(self):
        """
        Get all showrooms with decoration for API response.

        Returns: List of showroom dicts
        """
        showrooms = self.showroom_repo.get_all()
        return [
            {
                'room_id': sr.room_id,
                'room_number': sr.room_number,
                'number_of_seats': sr.number_of_seats,
            }
            for sr in showrooms
        ]
