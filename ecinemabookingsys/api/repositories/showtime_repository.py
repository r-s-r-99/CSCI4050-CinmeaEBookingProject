"""
Showtime Repository - Data access for Showtime entities.

Handles fetching showtime data with movie and room information.
Returns Showtime domain objects, never dicts.
"""

from repositories.base_repository import CRUDRepository


class ShowtimeRepository(CRUDRepository):
    """Repository for Showtime entities."""

    def find_by_id(self, showtime_id):
        """Find showtime by ID with associated movie and room."""
        from models.showtime import Showtime

        query = """
            SELECT s.showtime_id, s.movie_id, s.show_date, s.show_time, s.room_id
            FROM Showtime s
            WHERE s.showtime_id = %s
        """
        row = self.execute_query_one(query, (showtime_id,))
        if not row:
            return None

        return Showtime(**row)

    def find_by_movie(self, movie_id, limit=None):
        """Get all showtimes for a movie."""
        from models.showtime import Showtime

        query = """
            SELECT showtime_id, movie_id, show_date, show_time, room_id
            FROM Showtime
            WHERE movie_id = %s
            ORDER BY show_date, show_time
        """

        if limit:
            query += f" LIMIT {limit}"

        rows = self.execute_query(query, (movie_id,))
        return [Showtime(**row) for row in rows]

    def find_available_by_movie(self, movie_id):
        """Get available showtimes for a movie."""
        from models.showtime import Showtime

        query = """
            SELECT showtime_id, movie_id, show_date, show_time, room_id
            FROM Showtime
            WHERE movie_id = %s
            ORDER BY show_date, show_time
        """
        rows = self.execute_query(query, (movie_id,))
        return [Showtime(**row) for row in rows]

    def get_room_id(self, showtime_id):
        """Get the room_id for a showtime (useful for seat lookups)."""
        query = "SELECT room_id FROM Showtime WHERE showtime_id = %s"
        row = self.execute_query_one(query, (showtime_id,))
        return row["room_id"] if row else None

    def save(self, showtime):
        """Save showtime (insert or update)."""
        from models.showtime import Showtime

        if showtime.showtime_id:
            # Update
            query = """
                UPDATE Showtime
                SET movie_id = %s, show_date = %s, show_time = %s, room_id = %s
                WHERE showtime_id = %s
            """
            self.execute_update(
                query,
                (
                    showtime.movie_id,
                    showtime.show_date,
                    showtime.show_time,
                    showtime.room_id,
                    showtime.showtime_id,
                ),
            )
            return showtime
        else:
            # Insert
            query = """
                INSERT INTO Showtime (movie_id, show_date, show_time, room_id)
                VALUES (%s, %s, %s, %s)
            """
            showtime_id = self.execute_insert_get_id(
                query,
                (
                    showtime.movie_id,
                    showtime.show_date,
                    showtime.show_time,
                    showtime.room_id,
                ),
            )
            # Return a new Showtime object with the generated ID
            return Showtime(
                showtime_id=showtime_id,
                movie_id=showtime.movie_id,
                room_id=showtime.room_id,
                show_date=showtime.show_date,
                show_time=showtime.show_time
            )

    def delete(self, showtime):
        """Delete showtime."""
        query = "DELETE FROM Showtime WHERE showtime_id = %s"
        self.execute_update(query, (showtime.showtime_id,))
        return True

    def get_all(self):
        """Get all showtimes."""
        from models.showtime import Showtime

        query = "SELECT * FROM Showtime ORDER BY show_date, show_time"
        rows = self.execute_query(query)
        return [Showtime(**row) for row in rows]

