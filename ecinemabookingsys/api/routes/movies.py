from flask import Blueprint, request, jsonify
from db import get_db
from repositories.movie_repository import MovieRepository
from models.movie import Movie
from services.movie_decorator import MovieDecorator
import pandas as pd

movies_bp = Blueprint('movies', __name__)
movie_repo = MovieRepository()
movie_decorator = MovieDecorator(movie_repo)

@movies_bp.route('/api/movies', methods=['POST'])
def create_movie():
    """
    Create a new movie (admin only).

    Route handler: Thin request/response adapter
    Business logic: Handled by MovieRepository
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Check if user is admin
    from db import get_db
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT role FROM User WHERE user_id = %s", (session['user_id'],))
            user = cursor.fetchone()
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Only admins can create movies'}), 403
    finally:
        conn.close()

    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'genre', 'description', 'poster_url', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Create Movie domain object
        movie = Movie(
            movie_id=None,  # Will be generated
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
    - force_customer_view: If 'true', shows customer view even for admins (useful for home page)
    """
    user_role = None
    if 'user_id' in session:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role FROM User WHERE user_id = %s", (session['user_id'],))
                user = cursor.fetchone()
                user_role = user.get('role') if user else None
        finally:
            conn.close()

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
    user_role = None
    if 'user_id' in session:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role FROM User WHERE user_id = %s", (session['user_id'],))
                user = cursor.fetchone()
                user_role = user.get('role') if user else None
        finally:
            conn.close()

    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT movie_id, title, genre, rating, description, poster_url, trailer_url, status FROM Movie WHERE status = 'Currently Running'")
        rows = cursor.fetchall()
    conn.close()

    movies = [Movie(
        movie_id=row['movie_id'],
        title=row['title'],
        genre=row['genre'],
        rating=row['rating'],
        description=row['description'],
        poster_url=row['poster_url'],
        trailer_url=row['trailer_url'],
        status=row['status']
    ) for row in rows]

    decorated_movies = movie_decorator.get_decorated_movies(movies, user_role, force_customer_view=force_customer_view)
    return {"movies": decorated_movies}


@movies_bp.route('/api/movies/coming-soon')
def get_coming_soon():
    """Get movies coming soon.

    Query params:
    - force_customer_view: If 'true', shows customer view even for admins
    """
    user_role = None
    if 'user_id' in session:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role FROM User WHERE user_id = %s", (session['user_id'],))
                user = cursor.fetchone()
                user_role = user.get('role') if user else None
        finally:
            conn.close()

    force_customer_view = request.args.get('force_customer_view', 'false').lower() == 'true'
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



