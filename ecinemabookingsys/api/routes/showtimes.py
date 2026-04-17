from flask import Blueprint, request, jsonify, session
from db import get_db
from services.showtime_service import ShowtimeService
from repositories.movie_repository import MovieRepository
from repositories.showroom_repository import ShowroomRepository

showtimes_bp = Blueprint('showtimes', __name__)
showtime_service = ShowtimeService()
movie_repo = MovieRepository()
showroom_repo = ShowroomRepository()


def require_admin():
    """Check if user is admin. Returns (is_admin, error_response)."""
    if 'user_id' not in session:
        return False, (jsonify({'error': 'Unauthorized'}), 401)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT role FROM User WHERE user_id = %s", (session['user_id'],))
            user = cursor.fetchone()
        if not user or user.get('role') != 'admin':
            return False, (jsonify({'error': 'Only admins can manage showtimes'}), 403)
    finally:
        conn.close()

    return True, None


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
        showrooms = showroom_repo.get_all()
        decorated = [
            {
                'room_id': sr.room_id,
                'room_number': sr.room_number,
                'number_of_seats': sr.number_of_seats,
            }
            for sr in showrooms
        ]
        return jsonify({'showrooms': decorated}), 200

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
