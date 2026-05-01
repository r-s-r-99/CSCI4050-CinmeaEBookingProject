from flask import Blueprint, request, jsonify
from services.showtime_service import ShowtimeService
from services.showroom_service import ShowroomService
from repositories.movie_repository import MovieRepository
from repositories.seat_reservation_repository import SeatReservationRepository
from utils.auth import require_admin
from datetime import datetime, timedelta
import uuid

showtimes_bp = Blueprint('showtimes', __name__)
showtime_service = ShowtimeService()
showroom_service = ShowroomService()
movie_repo = MovieRepository()
seat_reservation_repo = SeatReservationRepository()

# Lock duration in minutes
SEAT_LOCK_DURATION = 5


@showtimes_bp.route('/api/showtimes/available-dates')
def get_available_dates():
    """Get all unique dates where showtimes exist."""
    try:
        dates = showtime_service.get_available_dates()
        print(f"[DEBUG] Available dates from service: {dates}")
        return jsonify({'dates': dates}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching available dates: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/available-times')
def get_available_times():
    """Get all unique times for a specific date.

    Query params:
    - date: YYYY-MM-DD format (required)
    """
    try:
        show_date = request.args.get('date')
        if not show_date:
            return jsonify({'error': 'Missing date parameter'}), 400

        times = showtime_service.get_available_times_for_date(show_date)
        return jsonify({'times': times}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching available times: {e}")
        return jsonify({'error': str(e)}), 500


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


# ============== Seat Reservation / Locking Endpoints ==============

@showtimes_bp.route('/api/seats/lock', methods=['POST'])
def lock_seats():
    """
    Lock seats for a showtime for 5 minutes.
    
    Request body:
    - showtime_id: ID of the showtime
    - seat_ids: Array of seat IDs to lock
    - session_token: Optional existing session token to reuse
    
    Returns:
    - session_token: Token to manage the reservation
    - expires_at: When the lock expires
    - reserved_seats: Array of successfully locked seats
    """
    try:
        data = request.get_json()
        showtime_id = data.get('showtime_id')
        seat_ids = data.get('seat_ids', [])
        existing_session_token = data.get('session_token')  # Optional: reuse existing session

        if not showtime_id or not seat_ids:
            return jsonify({'error': 'Missing showtime_id or seat_ids'}), 400

        # Use existing session token if provided, otherwise generate new one
        session_token = existing_session_token or str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=SEAT_LOCK_DURATION)

        # Try to reserve each seat
        reserved_seats = []
        failed_seats = []

        for seat_id in seat_ids:
            # Check if seat is already reserved
            existing = seat_reservation_repo.find_by_seat_and_showtime(seat_id, showtime_id)
            if existing:
                # Check if it's locked by the same session
                if existing_session_token and existing.get('session_token') == existing_session_token:
                    # Already locked by this session - that's fine, include it
                    reserved_seats.append(seat_id)
                else:
                    # Locked by different session or no session
                    failed_seats.append(seat_id)
                continue

            # Create the reservation
            success = seat_reservation_repo.create_reservation(
                showtime_id, [seat_id], session_token, expires_at
            )
            if success:
                reserved_seats.append(seat_id)
            else:
                failed_seats.append(seat_id)

        if not reserved_seats:
            return jsonify({
                'error': 'No seats could be reserved',
                'failed_seats': failed_seats
            }), 409

        return jsonify({
            'session_token': session_token,
            'expires_at': expires_at.isoformat(),
            'reserved_seats': reserved_seats,
            'failed_seats': failed_seats,
            'lock_duration_minutes': SEAT_LOCK_DURATION
        }), 200

    except Exception as e:
        print(f"[SEAT_LOCK] Error locking seats: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/seats/release', methods=['POST'])
def release_seats():
    """
    Release locked seats for a session.
    
    Request body:
    - session_token: Token of the reservation session
    """
    try:
        data = request.get_json()
        session_token = data.get('session_token')

        if not session_token:
            return jsonify({'error': 'Missing session_token'}), 400

        seat_reservation_repo.release_by_session(session_token)

        return jsonify({'message': 'Seats released successfully'}), 200

    except Exception as e:
        print(f"[SEAT_LOCK] Error releasing seats: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/seats/extend', methods=['POST'])
def extend_seat_lock():
    """
    Extend the lock time for reserved seats.
    
    Request body:
    - session_token: Token of the reservation session
    """
    try:
        data = request.get_json()
        session_token = data.get('session_token')

        if not session_token:
            return jsonify({'error': 'Missing session_token'}), 400

        # Extend by the same duration
        new_expires_at = datetime.now() + timedelta(minutes=SEAT_LOCK_DURATION)
        seat_reservation_repo.extend_reservation(session_token, new_expires_at)

        return jsonify({
            'expires_at': new_expires_at.isoformat(),
            'lock_duration_minutes': SEAT_LOCK_DURATION
        }), 200

    except Exception as e:
        print(f"[SEAT_LOCK] Error extending lock: {e}")
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/seats/locked/<int:showtime_id>', methods=['GET'])
def get_locked_seats(showtime_id):
    """
    Get all currently locked seats for a showtime.
    
    Returns:
    - locked_seats: Array of locked seat IDs with expiration info
    """
    try:
        reservations = seat_reservation_repo.find_active_by_showtime(showtime_id)
        
        locked_seats = []
        for res in reservations:
            locked_seats.append({
                'seat_id': res['seat_id'],
                'expires_at': res['expires_at'].isoformat() if res['expires_at'] else None
            })

        return jsonify({'locked_seats': locked_seats}), 200

    except Exception as e:
        print(f"[SEAT_LOCK] Error getting locked seats: {e}")
        return jsonify({'error': str(e)}), 500
