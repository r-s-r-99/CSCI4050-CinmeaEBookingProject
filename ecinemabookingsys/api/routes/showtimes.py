from flask import Blueprint, request, jsonify, session
from services.showtime_service import ShowtimeService
from services.showroom_service import ShowroomService
from repositories.movie_repository import MovieRepository
from repositories.booking_repository import TicketRepository
from repositories.seat_repository import SeatRepository
from repositories.seat_reservation_repository import SeatReservationRepository
from utils.auth import require_admin

showtimes_bp = Blueprint('showtimes', __name__)
showtime_service = ShowtimeService()
showroom_service = ShowroomService()
movie_repo = MovieRepository()
ticket_repo = TicketRepository()
seat_repo = SeatRepository()
seat_reservation_repo = SeatReservationRepository()


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
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/<int:movie_id>')
def get_showtimes_by_movie(movie_id):
    """Get all showtimes for a specific movie."""
    try:
        decorated = showtime_service.get_showtimes_by_movie_decorated(movie_id)
        return jsonify({'showtimes': decorated}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching showtimes for movie {movie_id}: {e}")
        import traceback
        traceback.print_exc()
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


@showtimes_bp.route('/api/showtimes/<int:showtime_id>/booked-seats', methods=['GET'])
def get_booked_seats(showtime_id):
    """Get all booked and reserved seat numbers for a specific showtime."""
    try:
        # Get showtime to find the room_id
        showtime = showtime_service.showtime_repo.find_by_id(showtime_id)
        if not showtime:
            return jsonify({'error': 'Showtime not found'}), 404

        room_id = showtime.room_id

        # Get booked seat IDs
        booked_seat_ids = ticket_repo.find_booked_seats_by_showtime(showtime_id)
        reserved_seat_ids = seat_reservation_repo.get_reserved_seats(showtime_id)

        # Convert seat IDs to seat numbers
        booked_seat_numbers = []
        for seat_id in booked_seat_ids + reserved_seat_ids:
            seat = seat_repo.find_by_id(seat_id)
            if seat:
                booked_seat_numbers.append(seat.seat_number)

        return jsonify({'booked_seats': booked_seat_numbers}), 200
    except Exception as e:
        print(f"[SHOWTIME] Error fetching booked seats for showtime {showtime_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/<int:showtime_id>/reserve-seats', methods=['POST'])
def reserve_seats(showtime_id):
    """Reserve seats for the user during checkout process."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        seat_numbers = data.get('seat_ids', []) if data else []

        if not seat_numbers:
            print(f"[RESERVE_SEATS] No seats provided. Data: {data}")
            return jsonify({'error': 'No seats provided'}), 400

        # Get showtime to find the room_id
        showtime = showtime_service.showtime_repo.find_by_id(showtime_id)
        if not showtime:
            print(f"[RESERVE_SEATS] Showtime {showtime_id} not found")
            return jsonify({'error': 'Showtime not found'}), 404

        room_id = showtime.room_id
        user_id = session['user_id']

        # Release any existing reservations for this user on this showtime first
        seat_reservation_repo.release_all_reservations(user_id, showtime_id)

        # Convert seat numbers (like "B6") to actual seat_ids
        seat_ids = []
        for seat_number in seat_numbers:
            seat = seat_repo.find_by_number_and_room(seat_number, room_id)
            if seat:
                seat_ids.append(seat.seat_id)
            else:
                print(f"[RESERVE_SEATS] Could not find seat {seat_number} in room {room_id}")

        if not seat_ids:
            print(f"[RESERVE_SEATS] Could not find any valid seats. Requested: {seat_numbers}, Room: {room_id}")
            return jsonify({'error': 'Could not find requested seats'}), 400

        reservations = seat_reservation_repo.reserve_seats(
            user_id=user_id,
            showtime_id=showtime_id,
            seat_ids=seat_ids,
            duration_minutes=5
        )

        return jsonify({
            'status': 'success',
            'message': f'Reserved {len(reservations)} seat(s) for 5 minutes',
            'reservations': reservations
        }), 201

    except Exception as e:
        print(f"[RESERVE_SEATS] Error reserving seats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@showtimes_bp.route('/api/showtimes/<int:showtime_id>/release-seats', methods=['POST'])
def release_seats(showtime_id):
    """Release seat reservations (called when user completes booking or cancels)."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        user_id = session['user_id']
        seat_reservation_repo.release_all_reservations(user_id, showtime_id)

        return jsonify({
            'status': 'success',
            'message': 'Seat reservations released'
        }), 200

    except Exception as e:
        print(f"[SHOWTIME] Error releasing seats: {e}")
        return jsonify({'error': str(e)}), 500
