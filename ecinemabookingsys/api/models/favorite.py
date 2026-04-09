from models.base import BaseModel

class Favorite(BaseModel):
    def __init__(self, favorite_id, user_id, movie_id, date_added):
        self.favorite_id = favorite_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.date_added = date_added

    def to_dict(self):
        return {
            'favoriteId': self.favorite_id,
            'userId':     self.user_id,
            'movieId':    self.movie_id,
            'dateAdded':  str(self.date_added),
        }

    @classmethod
    def get_by_user(cls, user_id):
        conn = cls.get_db()
        try:
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
        finally:
            conn.close()

    @classmethod
    def toggle(cls, user_id, movie_id):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT favorite_id FROM Favorite
                    WHERE user_id = %s AND movie_id = %s
                """, (user_id, movie_id))
                existing = cursor.fetchone()

                if existing:
                    cursor.execute("DELETE FROM Favorite WHERE user_id = %s AND movie_id = %s", (user_id, movie_id))
                    action = 'removed'
                else:
                    cursor.execute("INSERT INTO Favorite (user_id, movie_id) VALUES (%s, %s)", (user_id, movie_id))
                    action = 'added'

                conn.commit()
                return action
        finally:
            conn.close()