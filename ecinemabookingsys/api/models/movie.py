from models.base import BaseModel
from services.movie_service import MovieService


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
        return MovieService.get_all_movies()

    @classmethod
    def find_by_id(cls, movie_id):
        return MovieService.get_movie_by_id(movie_id)
