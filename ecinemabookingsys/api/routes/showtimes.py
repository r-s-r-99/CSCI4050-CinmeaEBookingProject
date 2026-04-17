from flask import Blueprint, request, jsonify
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

@showtimes_bp.route('/api/showtimes/<int:showtime_id>', methods=['DELETE'])
def delete_showtime(showtime_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Showtime WHERE showtime_id = %s", (showtime_id,))
    conn.commit()
    conn.close()
    return {"message": "Showtime successfully deleted"}

@showtimes_bp.route('/api/showtimes', methods=['POST'])
def add_showtime():
    data = request.get_json()
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Showtime (movie_id, room_id, show_date, show_time)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get('movie_id'),
            data.get('room_id'),
            data.get('show_date'),
            data.get('show_time'),
        ))

    conn.commit()
    conn.close()

    return {"message": "The showtime was successfully added."}, 201
