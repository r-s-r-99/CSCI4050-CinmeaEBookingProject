from models.base import BaseModel
from services.favorite_service import FavoriteService


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
        return FavoriteService.get_favorites_by_user(user_id)

    @classmethod
    def toggle(cls, user_id, movie_id):
        return FavoriteService.toggle_favorite(user_id, movie_id)
