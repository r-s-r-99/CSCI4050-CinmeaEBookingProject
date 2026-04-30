from flask import Blueprint, request, jsonify
from services.showtime_service import ShowtimeService
from services.showroom_service import ShowroomService
from repositories.movie_repository import MovieRepository
from utils.auth import require_admin

showtimes_bp = Blueprint('showtimes', __name__)
showtime_service = ShowtimeService()
showroom_service = ShowroomService()
movie_repo = MovieRepository()


@showtimes_bp.route('/api/showtimes/detail/<int:showtime_id>')
def get_showtime_detail(showtime_id):
    """Get a single showtime's details."""
    try:
        showtime = showtime_service.showtime_repo.find_by_id(showtime_id)
        if not showtime:
            return jsonify({'error': 'Showtime not found'}), 404

        decorated = showtime_service.get_all_showtimes_decorated()
        # Find the matching showtime in decorated list
        matching = next((st for st in decorated if st['showtime_id'] == showtime_id), None)

        if not matching:
            return jsonify({'error': 'Showtime not found'}), 404

        return jsonify({'showtime': matching}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching showtime detail {showtime_id}: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/<int:movie_id>')
def get_showtimes_by_movie(movie_id):
    """Get all showtimes for a specific movie."""
    try:
        decorated = showtime_service.get_showtimes_by_movie_decorated(movie_id)
        return jsonify({'showtimes': decorated}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching showtimes for movie {movie_id}: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes', methods=['GET'])
def get_showtimes():
    """Get all showtimes with movie and room info."""
    try:
        decorated = showtime_service.get_all_showtimes_decorated()
        return jsonify({'showtimes': decorated}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching showtimes: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/check-conflict', methods=['POST'])
def check_conflict():
    """Check for scheduling conflicts before creating a showtime."""
    is_admin, error_response = require_admin()
    if not is_admin:
        return error_response

    try:
        data = request.get_json()
        room_id = data.get('room_id')
        show_date = data.get('show_date')
        show_time = data.get('show_time')

        if not all([room_id, show_date, show_time]):
            return jsonify({'error': 'Missing required fields'}), 400

        result = showtime_service.check_conflict(room_id, show_date, show_time)
        return jsonify(result), 200

    except Exception as e:
        print(f"[SHOWTIME] Error checking conflict: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes', methods=['POST'])
def create_showtime():
    """Create a new showtime with conflict detection."""
    is_admin, error_response = require_admin()
    if not is_admin:
        return error_response

    try:
        data = request.get_json()
        movie_id = data.get('movie_id')
        show_date = data.get('show_date')
        show_time = data.get('show_time')
        room_id = data.get('room_id')

        if not all([movie_id, show_date, show_time, room_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        result = showtime_service.create_showtime(movie_id, show_date, show_time, room_id)

        if result['success']:
            return jsonify({
                'status': 'success',
                'message': 'Showtime created successfully',
                'showtime': result['showtime'].to_dict() if hasattr(result['showtime'], 'to_dict') else result['showtime']
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'error': result['error'],
                'conflicts': result.get('conflicts', [])
            }), 400

    except Exception as e:
        print(f"[SHOWTIME] Error creating showtime: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showrooms', methods=['GET'])
def get_showrooms():
    """Get all available showrooms."""
    try:
        showrooms = showroom_service.get_all_showrooms_decorated()
        return jsonify({'showrooms': showrooms}), 200
    except Exception as e:
        print(f"[SHOWROOM] Error fetching showrooms: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/movies-for-showtimes', methods=['GET'])
def get_movies_for_showtimes():
    """Get all movies available for scheduling showtimes."""
    try:
        all_movies = movie_repo.find_all()
        decorated = [
            {
                'id': m.movie_id,
                'title': m.title,
                'genre': m.genre,
            }
            for m in all_movies
        ]
        return jsonify({'movies': decorated}), 200
    except Exception as e:
        print(f"[MOVIE] Error fetching movies: {e}")
        return jsonify({'error': str(e)}), 500
