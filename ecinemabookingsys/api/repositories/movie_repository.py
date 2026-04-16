"""
Movie Repository - Data access for Movie entities.

Handles fetching movie data with proper domain object composition.
"""

from repositories.base_repository import CRUDRepository


class MovieRepository(CRUDRepository):
    """Repository for Movie entities."""

    def find_by_id(self, movie_id):
        """Find movie by ID. Returns Movie domain object or None."""
        from models.movie import Movie

        query = """
            SELECT movie_id, title, genre, rating, description, poster_url, trailer_url, status
            FROM Movie WHERE movie_id = %s
        """
        row = self.execute_query_one(query, (movie_id,))
        if not row:
            return None

        return Movie(
            movie_id=row["movie_id"],
            title=row["title"],
            genre=row["genre"],
            rating=row["rating"],
            description=row["description"],
            poster_url=row["poster_url"],
            trailer_url=row["trailer_url"],
            status=row["status"],
        )

    def find_all(self, limit=None):
        """
        Get all movies.

        Returns: List of Movie domain objects
        """
        from models.movie import Movie

        query = """
            SELECT movie_id, title, genre, rating, description, poster_url, trailer_url, status
            FROM Movie
            WHERE status = 'showing'
            ORDER BY title
        """

        if limit:
            query += f" LIMIT {limit}"

        rows = self.execute_query(query)
        return [
            Movie(
                movie_id=row["movie_id"],
                title=row["title"],
                genre=row["genre"],
                rating=row["rating"],
                description=row["description"],
                poster_url=row["poster_url"],
                trailer_url=row["trailer_url"],
                status=row["status"],
            )
            for row in rows
        ]

    def find_by_showtime(self, showtime_id):
        """Get movie for a specific showtime."""
        from models.movie import Movie

        query = """
            SELECT m.movie_id, m.title, m.genre, m.rating, m.description,
                   m.poster_url, m.trailer_url, m.status
            FROM Movie m
            JOIN Showtime s ON m.movie_id = s.movie_id
            WHERE s.showtime_id = %s
        """
        row = self.execute_query_one(query, (showtime_id,))
        if not row:
            return None

        return Movie(
            movie_id=row["movie_id"],
            title=row["title"],
            genre=row["genre"],
            rating=row["rating"],
            description=row["description"],
            poster_url=row["poster_url"],
            trailer_url=row["trailer_url"],
            status=row["status"],
        )

    def save(self, movie):
        """Save movie (insert or update)."""
        if hasattr(movie, "movie_id") and movie.movie_id:
            # Update
            query = """
                UPDATE Movie
                SET title = %s, genre = %s, rating = %s, description = %s,
                    poster_url = %s, trailer_url = %s, status = %s
                WHERE movie_id = %s
            """
            self.execute_update(
                query,
                (
                    movie.title,
                    movie.genre,
                    movie.rating,
                    movie.description,
                    movie.poster_url,
                    movie.trailer_url,
                    movie.status,
                    movie.movie_id,
                ),
            )
        else:
            # Insert
            query = """
                INSERT INTO Movie (title, genre, rating, description, poster_url, trailer_url, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            movie_id = self.execute_insert_get_id(
                query,
                (
                    movie.title,
                    movie.genre,
                    movie.rating,
                    movie.description,
                    movie.poster_url,
                    movie.trailer_url,
                    movie.status,
                ),
            )
            movie.movie_id = movie_id

        return movie

    def delete(self, movie):
        """Delete movie."""
        query = "DELETE FROM Movie WHERE movie_id = %s"
        self.execute_update(query, (movie.movie_id,))
        return True

    def get_all(self):
        """Get all movies (required by abstract interface)."""
        return self.find_all()
