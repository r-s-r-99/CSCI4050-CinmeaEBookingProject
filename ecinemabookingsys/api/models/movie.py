from models.base import BaseModel

class Movie(BaseModel):
    def __init__(self, movie_id, title, genre, rating, description, poster_url, trailer_url, status):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.rating = rating
        self.description = description
        self.poster_url = poster_url
        self.trailer_url = trailer_url
        self.status = status

    def to_dict(self):
        return {
            'id':          self.movie_id,
            'title':       self.title,
            'genre':       self.genre,
            'rating':      self.rating,
            'description': self.description,
            'poster_url':  self.poster_url,
            'trailer_url': self.trailer_url,
            'status':      self.status,
        }

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Movie")
                rows = cursor.fetchall()
            return [cls(**row) for row in rows]
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, movie_id):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Movie WHERE movie_id = %s", (movie_id,))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()