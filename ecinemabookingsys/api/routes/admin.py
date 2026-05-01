from flask import Blueprint, request, jsonify, session
from services.admin_service import AdminService

movies_bp = Blueprint('movies', __name__)
showtimes_bp = Blueprint('showtimes', __name__)


@movies_bp.route('/api/movies/add', methods=['POST'])
def add_movie():
    role = session.get('role')
    if role != 'Admin':
        return jsonify({'success': False, 'error': 'Unauthorized. Admins only.'}), 403

    data = request.get_json()

    # Validate input
    errors = AdminService.validate_movie_data(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    try:
        movie_id = AdminService.add_movie(data)
        return jsonify({
            'success': True,
            'message': 'Movie successfully added!',
            'movie_id': movie_id
        }), 201
    except Exception as e:
        print(f"[ADD MOVIE ERROR]: {e}")
        return jsonify({'success': False, 'error': 'An internal database error occurred.'}), 500


@showtimes_bp.route('/api/showtimes', methods=['POST'])
def add_showtime():
    data = request.get_json()

    # Validate input
    errors = AdminService.validate_showtime_data(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    movie_id = data.get('movie_id')
    showroom_id = data.get('showroom_id')
    show_date = data.get('show_date')
    show_time = data.get('show_time')

    print(f"[SCHEDULER] Attempting to schedule movie {movie_id} in showroom {showroom_id}")

    try:
        AdminService.add_showtime(movie_id, showroom_id, show_date, show_time)
        print("[SCHEDULER] Showtime added successfully.")

        return jsonify({
            'success': True,
            'message': 'Showtime scheduled successfully.'
        }), 201
    except ValueError as e:
        print(f"[SCHEDULER] Conflict: {e}")
        return jsonify({'success': False, 'error': str(e)}), 409
    except Exception as e:
        print(f"[SCHEDULER] Exception: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
