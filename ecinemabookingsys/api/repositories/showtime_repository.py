"""
Showtime Repository - Data access for Showtime entities.

Handles fetching showtime data with movie and room information.
"""

from repositories.base_repository import CRUDRepository


class ShowtimeRepository(CRUDRepository):
    """Repository for Showtime entities."""

    def find_by_id(self, showtime_id):
        """Find showtime by ID with associated movie and room."""
        query = """
            SELECT s.showtime_id, s.movie_id, s.show_date, s.show_time, s.room_id,
                   m.title, m.genre, m.rating,
                   sr.room_id, sr.max_capacity
            FROM Showtime s
            LEFT JOIN Movie m ON s.movie_id = m.movie_id
            LEFT JOIN Showroom sr ON s.room_id = sr.room_id
            WHERE s.showtime_id = %s
        """
        row = self.execute_query_one(query, (showtime_id,))
        if not row:
            return None

        return {
            "showtime_id": row["showtime_id"],
            "movie_id": row["movie_id"],
            "show_date": row["show_date"],
            "show_time": row["show_time"],
            "room_id": row["room_id"],
            "max_capacity": row["max_capacity"],
        }

    def find_by_movie(self, movie_id, limit=None):
        """Get all showtimes for a movie."""
        query = """
            SELECT showtime_id, movie_id, show_date, show_time, room_id
            FROM Showtime
            WHERE movie_id = %s AND show_date >= CURDATE()
            ORDER BY show_date, show_time
        """

        if limit:
            query += f" LIMIT {limit}"

        rows = self.execute_query(query, (movie_id,))
        return [dict(row) for row in rows]

    def find_available_by_movie(self, movie_id):
        """Get available showtimes for a movie (future dates only)."""
        query = """
            SELECT showtime_id, movie_id, show_date, show_time, room_id
            FROM Showtime
            WHERE movie_id = %s AND show_date >= CURDATE()
            ORDER BY show_date, show_time
        """
        rows = self.execute_query(query, (movie_id,))
        return [dict(row) for row in rows]

    def get_room_id(self, showtime_id):
        """Get the room_id for a showtime (useful for seat lookups)."""
        query = "SELECT room_id FROM Showtime WHERE showtime_id = %s"
        row = self.execute_query_one(query, (showtime_id,))
        return row["room_id"] if row else None

    def save(self, showtime):
        """Save showtime (insert or update)."""
        if showtime.get("showtime_id"):
            # Update
            query = """
                UPDATE Showtime
                SET movie_id = %s, show_date = %s, show_time = %s, room_id = %s
                WHERE showtime_id = %s
            """
            self.execute_update(
                query,
                (
                    showtime.get("movie_id"),
                    showtime.get("show_date"),
                    showtime.get("show_time"),
                    showtime.get("room_id"),
                    showtime["showtime_id"],
                ),
            )
        else:
            # Insert
            query = """
                INSERT INTO Showtime (movie_id, show_date, show_time, room_id)
                VALUES (%s, %s, %s, %s)
            """
            showtime_id = self.execute_insert_get_id(
                query,
                (
                    showtime.get("movie_id"),
                    showtime.get("show_date"),
                    showtime.get("show_time"),
                    showtime.get("room_id"),
                ),
            )
            showtime["showtime_id"] = showtime_id

        return showtime

    def delete(self, showtime):
        """Delete showtime."""
        query = "DELETE FROM Showtime WHERE showtime_id = %s"
        self.execute_update(query, (showtime["showtime_id"],))
        return True

    def get_all(self):
        """Get all showtimes."""
        query = "SELECT * FROM Showtime ORDER BY show_date, show_time"
        rows = self.execute_query(query)
        return [dict(row) for row in rows]
