from db import get_db


class FavoriteRepository:
    @staticmethod
    def get_by_user(user_id):
        """Get all favorite movies for a user."""
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.movie_id, m.title, m.poster_url, m.genre, m.rating,
                       m.description, m.trailer_url, m.status, f.date_added,
                       f.favorite_id, f.user_id
                FROM Favorite f
                JOIN Movie m ON f.movie_id = m.movie_id
                WHERE f.user_id = %s
                ORDER BY f.date_added DESC
            """, (user_id,))
            return cursor.fetchall()

    @staticmethod
    def check_favorite(user_id, movie_id):
        """Check if a movie is favorited by user."""
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT favorite_id FROM Favorite
                WHERE user_id = %s AND movie_id = %s
            """, (user_id, movie_id))
            return cursor.fetchone()

    @staticmethod
    def add_favorite(user_id, movie_id):
        """Add a movie to user's favorites."""
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Favorite (user_id, movie_id)
                VALUES (%s, %s)
            """, (user_id, movie_id))
        conn.commit()

    @staticmethod
    def remove_favorite(user_id, movie_id):
        """Remove a movie from user's favorites."""
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Favorite
                WHERE user_id = %s AND movie_id = %s
            """, (user_id, movie_id))
        conn.commit()

