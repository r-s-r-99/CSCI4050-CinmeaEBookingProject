from groq import Groq
from repositories.movie_repository import MovieRepository
from repositories.favorite_repository import FavoriteRepository
from services.booking_service import BookingService


class RecommendationService:
    """Service for movie recommendations."""

    def __init__(self):
        self.booking_service = BookingService()
        self.movie_repo = MovieRepository()
        self.favorite_repo = FavoriteRepository()
        self.groq_client = Groq()

    def get_recommendations(self, user_id):
        """Get AI-based recommendations using Groq."""
        booked_movies = self.booking_service.get_booked_movies(user_id)
        favorite_movies_raw = self.favorite_repo.get_by_user(user_id)
        all_movies = self.movie_repo.find_all()

        booked_movies_str = self._format_movies(booked_movies, is_dict=True)
        favorite_movies_str = self._format_movies_raw(favorite_movies_raw)
        all_movies_str = self._format_movies(all_movies, is_dict=False)

        ai_recommendations = self._get_ai_recommendations(
            all_movies_str, favorite_movies_str, booked_movies_str
        )

        return {
            "booked_movies": booked_movies,
            "favorite_movies": favorite_movies_raw,
            "all_movies": all_movies,
            "ai_recommendations": ai_recommendations,
        }

    def _format_movies(self, movies, is_dict=False):
        """Format movies for display."""
        result = []
        for movie in movies:
            if is_dict:
                result.append(
                    f"{movie['title']} | {movie['genre']} | Rating: {movie['rating']}\n"
                    f"Description: {movie['description']}"
                )
            else:
                result.append(
                    f"{movie.title} | {movie.genre} | Rating: {movie.rating}\n"
                    f"Description: {movie.description}"
                )
        return "\n\n".join(result)

    def _format_movies_raw(self, movies):
        """Format raw movie data (from database cursor) for display."""
        result = []
        for movie in movies:
            result.append(
                f"{movie['title']} | {movie['genre']} | Rating: {movie['rating']}\n"
                f"Description: {movie['description']}"
            )
        return "\n\n".join(result)

    def _get_ai_recommendations(
        self, all_movies_str, favorite_movies_str, booked_movies_str
    ):
        """Get AI recommendations using Groq."""
        try:
            client = Groq()
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a movie recommendation engine. You will be given a list of movies and their details, and you will recommend movies based on the user's favorites and bookings.",
                    },
                    {
                        "role": "system",
                        "content": "This is a list of all available movies:\n\n" + all_movies_str,
                    },
                    {
                        "role": "system",
                        "content": "This is a list of the user's favorite movies:\n\n" + favorite_movies_str,
                    },
                    {
                        "role": "system",
                        "content": "This is a list of movies booked by the user:\n\n" + booked_movies_str,
                    },
                    {
                        "role": "user",
                        "content": "Can you recommend 3 to 4 other movies from the list of all available movies that the user might like to watch based on their favorite movies and/or booked movies? Return just the movie titles, one per line.",
                    },
                ],
            )
            print(completion.choices[0].message.content)
            return completion.choices[0].message.content
        except Exception as e:
            print(f"[RECOMMENDATIONS] Error getting AI recommendations: {e}")
            return None


def booked_movies_to_string(user_id):
    service = BookingService()
    movies = service.get_booked_movies(user_id)
    return "\n".join([f"{movie['title']} | {movie['genre']} | Rating: {movie['rating']}\nDescription: {movie['description']}\n" for movie in movies])

def favorite_movies_to_string(user_id):
    repo = FavoriteRepository()
    movies = repo.get_by_id(user_id)
    return "\n".join([f"{movie.title} | {movie.genre} | Rating: {movie.rating}\nDescription: {movie.description}\n" for movie in movies])

def movies_to_string():
    repo = MovieRepository()
    movies = repo.find_all()
    return "\n".join([f"{movie.title} | {movie.genre} | Rating: {movie.rating}\nDescription: {movie.description}\n" for movie in movies])
