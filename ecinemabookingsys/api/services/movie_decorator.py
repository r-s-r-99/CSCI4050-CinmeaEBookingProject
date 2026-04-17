"""
Movie Decorator - Adds role-specific behavior and metadata to Movie objects.

The decorator pattern enriches Movie domain objects with context-aware fields
based on user role (admin vs customer).
"""

from repositories.movie_repository import MovieRepository


class MovieDecorator:
    """Base decorator that adds role-specific fields to Movie objects."""

    def __init__(self, movie_repo=None):
        self.movie_repo = movie_repo or MovieRepository()

    def decorate_for_customer(self, movie):
        """Decorate movie for customer view (read-only)."""
        movie_dict = movie.to_dict()
        movie_dict.update({
            'isEditable': False,
            'actions': ['view'],
        })
        return movie_dict

    def decorate_for_admin(self, movie):
        """Decorate movie for admin view (with edit/delete capabilities)."""
        movie_dict = movie.to_dict()
        movie_dict.update({
            'isEditable': True,
            'actions': ['view', 'edit', 'delete'],
            'editUrl': f'/edit-movies/{movie.movie_id}',
        })
        return movie_dict

    def get_decorated_movie(self, movie_id, user_role=None, force_customer_view=False):
        """Get a single movie decorated based on user role.

        Args:
            movie_id: Movie ID to decorate
            user_role: User's role ('admin' or None for customer)
            force_customer_view: If True, always show customer view regardless of role
        """
        movie = self.movie_repo.find_by_id(movie_id)
        if not movie:
            return None

        if force_customer_view:
            return self.decorate_for_customer(movie)
        elif user_role == 'admin':
            return self.decorate_for_admin(movie)
        else:
            return self.decorate_for_customer(movie)

    def get_decorated_movies(self, movies, user_role=None, force_customer_view=False):
        """Decorate multiple movies based on user role.

        Args:
            movies: List of Movie objects to decorate
            user_role: User's role ('admin' or None for customer)
            force_customer_view: If True, always show customer view regardless of role
        """
        if force_customer_view:
            decorator_func = self.decorate_for_customer
        else:
            decorator_func = self.decorate_for_admin if user_role == 'admin' else self.decorate_for_customer
        return [decorator_func(movie) for movie in movies]
