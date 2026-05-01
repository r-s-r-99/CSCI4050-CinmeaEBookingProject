from repositories.favorite_repository import FavoriteRepository


class FavoriteService:
    @staticmethod
    def get_favorites_by_user(user_id):
        """
        Get all favorite movies for a user.

        Args:
            user_id: User ID

        Returns: List of favorite movie records
        """
        if not user_id:
            raise ValueError('User ID is required.')

        try:
            return FavoriteRepository.get_by_user(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def toggle_favorite(user_id, movie_id):
        """
        Toggle a movie as favorite (add if not favorited, remove if favorited).

        Args:
            user_id: User ID
            movie_id: Movie ID

        Returns: 'added' or 'removed'
        """
        if not user_id:
            raise ValueError('User ID is required.')
        if not movie_id:
            raise ValueError('Movie ID is required.')

        try:
            existing = FavoriteRepository.check_favorite(user_id, movie_id)

            if existing:
                FavoriteRepository.remove_favorite(user_id, movie_id)
                return 'removed'
            else:
                FavoriteRepository.add_favorite(user_id, movie_id)
                return 'added'
        except Exception as e:
            raise e
