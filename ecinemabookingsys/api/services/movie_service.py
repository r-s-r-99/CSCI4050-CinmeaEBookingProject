from repositories.movie_repository import MovieRepository


class MovieService:
    @staticmethod
    def get_all_movies(limit=None):
        """
        Get all movies.

        Args:
            limit: Optional limit on number of movies

        Returns: List of Movie objects
        """
        try:
            repo = MovieRepository()
            return repo.find_all(limit)
        except Exception as e:
            raise e

    @staticmethod
    def get_movie_by_id(movie_id):
        """
        Get movie by ID.

        Args:
            movie_id: Movie ID

        Returns: Movie object or None
        """
        if not movie_id:
            raise ValueError('Movie ID is required.')

        try:
            repo = MovieRepository()
            return repo.find_by_id(movie_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_movie_by_showtime(showtime_id):
        """
        Get movie for a specific showtime.

        Args:
            showtime_id: Showtime ID

        Returns: Movie object or None
        """
        if not showtime_id:
            raise ValueError('Showtime ID is required.')

        try:
            repo = MovieRepository()
            return repo.find_by_showtime(showtime_id)
        except Exception as e:
            raise e
