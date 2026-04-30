from flask import Blueprint, request, jsonify
<<<<<<< HEAD
=======
from db import get_db
>>>>>>> 71ce8228cdca01547b0fbe6cc6cd62bed67a9343
from repositories.movie_repository import MovieRepository
from models.movie import Movie
from services.movie_decorator import MovieDecorator
from utils.auth import require_admin, get_user_role_from_session

movies_bp = Blueprint('movies', __name__)
movie_repo = MovieRepository()
movie_decorator = MovieDecorator(movie_repo)


@movies_bp.route('/api/movies', methods=['POST'])
def create_movie():
    """Create a new movie (admin only)."""
    is_admin, error_response = require_admin()
    if not is_admin:
        return error_response

    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'genre', 'description', 'poster_url', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Create Movie domain object
        movie = Movie(
            movie_id=None,
            title=data['title'],
            genre=data['genre'],
            rating=data.get('rating', ''),
            description=data['description'],
            poster_url=data['poster_url'],
            trailer_url=data.get('trailer_url', ''),
            status=data['status']
        )

        # Save movie via repository
        saved_movie = movie_repo.save(movie)

        return jsonify({
            'status': 'success',
            'message': 'Movie created successfully',
            'movie_id': saved_movie.movie_id,
            'movie': saved_movie.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[MOVIE] Error creating movie: {e}")
        return jsonify({'error': str(e)}), 500


@movies_bp.route('/api/movies')
def get_movies():
    """Get all movies with role-specific decoration.

    Query params:
    - force_customer_view: If 'true', shows customer view even for admins
    """
    user_role = get_user_role_from_session()
    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'

    all_movies = movie_repo.find_all()
    decorated_movies = movie_decorator.get_decorated_movies(all_movies, user_role, force_customer_view=force_customer_view)
    return {"movies": decorated_movies}


@movies_bp.route('/api/movies/now-showing')
def get_now_showing():
    """Get movies currently showing.

    Query params:
    - force_customer_view: If 'true', shows customer view even for admins
    """
    user_role = get_user_role_from_session()
    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'

    movies = movie_repo.find_by_status('Currently Running')
    decorated_movies = movie_decorator.get_decorated_movies(movies, user_role, force_customer_view=force_customer_view)
    return {"movies": decorated_movies}


@movies_bp.route('/api/movies/coming-soon')
def get_coming_soon():
    """Get movies coming soon.

    Query params:
    - force_customer_view: If 'true', shows customer view even for admins
    """
    user_role = get_user_role_from_session()
    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'
<<<<<<< HEAD

    movies = movie_repo.find_by_status('Coming Soon')
    decorated_movies = movie_decorator.get_decorated_movies(movies, user_role, force_customer_view=force_customer_view)
    return {"movies": decorated_movies}


@movies_bp.route('/api/movies/<int:movie_id>')
def get_movies_details(movie_id):
    """Get single movie with role-specific decoration.

    Query params:
    - force_customer_view: If 'true', shows customer view even for admins
    """
    user_role = get_user_role_from_session()
    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'

    decorated_movie = movie_decorator.get_decorated_movie(movie_id, user_role, force_customer_view=force_customer_view)
    if not decorated_movie:
        return jsonify({'error': 'Movie not found'}), 404
    return {"movie": decorated_movie}


@movies_bp.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Update an existing movie (admin only)."""
    is_admin, error_response = require_admin()
    if not is_admin:
        return error_response

    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'genre', 'description', 'poster_url', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Find existing movie
        existing_movie = movie_repo.find_by_id(movie_id)
        if not existing_movie:
            return jsonify({'error': 'Movie not found'}), 404

        # Update Movie domain object
        existing_movie.title = data['title']
        existing_movie.genre = data['genre']
        existing_movie.rating = data.get('rating', existing_movie.rating)
        existing_movie.description = data['description']
        existing_movie.poster_url = data['poster_url']
        existing_movie.trailer_url = data.get('trailer_url', existing_movie.trailer_url)
        existing_movie.status = data['status']

        # Save updated movie via repository
        updated_movie = movie_repo.save(existing_movie)

        return jsonify({
            'status': 'success',
            'message': 'Movie updated successfully',
            'movie_id': updated_movie.movie_id,
            'movie': updated_movie.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[MOVIE] Error updating movie: {e}")
        return jsonify({'error': str(e)}), 500


@movies_bp.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """Delete a movie (admin only)."""
    is_admin, error_response = require_admin()
    if not is_admin:
        return error_response

    try:
        # Find existing movie
        existing_movie = movie_repo.find_by_id(movie_id)
        if not existing_movie:
            return jsonify({'error': 'Movie not found'}), 404

        # Delete movie via repository
        movie_repo.delete(existing_movie)

        return jsonify({
            'status': 'success',
            'message': 'Movie deleted successfully',
        }), 200

    except Exception as e:
        print(f"[MOVIE] Error deleting movie: {e}")
        return jsonify({'error': str(e)}), 500
=======
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT movie_id, title, genre, rating, description, poster_url, trailer_url, status FROM Movie WHERE status = 'Coming Soon'")
        rows = cursor.fetchall()
    conn.close()
    return {"movies": movies}

@movies_bp.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Movie (title, genre, rating, description, poster_url, trailer_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('title'),
            data.get('genre'),
            data.get('rating'),
            data.get('description'),
            data.get('poster_url'),
            data.get('trailer_url'),
            data.get('status'),
        ))
    conn.commit()
    conn.close()
    return {"message": "Movie successfully added"}



>>>>>>> 71ce8228cdca01547b0fbe6cc6cd62bed67a9343
