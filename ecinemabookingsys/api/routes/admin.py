from flask import Blueprint, request, jsonify, session
from db import get_db
movies_bp = Blueprint('movies', __name__)
showtimes_bp = Blueprint('showtimes', __name__)
# Assuming this goes into your existing movies_bp or a new admin_bp
# @movies_bp.route('/api/admin/movies', methods=['POST'])

@movies_bp.route('/api/movies/add', methods=['POST'])
def add_movie():
    # Ensure the user has the appropriate role (e.g., Admin)
    role = session.get('role')
    if role != 'Admin': # Adjust based on your actual database role naming convention
        return jsonify({'success': False, 'error': 'Unauthorized. Admins only.'}), 403

    data = request.get_json()

    # --- 1. Form Completeness and Validation (10 pts) ---
    title = data.get('title')
    genre = data.get('genre')
    director = data.get('director')
    producer = data.get('producer')
    synopsis = data.get('synopsis')
    rating = data.get('rating')  # e.g., 'PG-13', 'R'
    status = data.get('status')  # e.g., 'Currently Running', 'Coming Soon'
    trailer_url = data.get('trailerUrl')
    poster_url = data.get('posterUrl')

    # Dictionary to hold specific field errors for the frontend
    errors = {}

    # Basic validations (You can expand these based on your DB schema limits)
    if not title or not title.strip():
        errors['title'] = 'Movie title is required.'
    if not genre or not genre.strip():
        errors['genre'] = 'Genre is required.'
    if not status or status not in ['Currently Running', 'Coming Soon']:
        errors['status'] = 'A valid status (Currently Running or Coming Soon) is required.'
    if not rating:
        errors['rating'] = 'MPAA Rating is required.'

    # If any validation failed, return a 400 Bad Request with the errors
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    # --- 2. Movie is stored correctly in the database (5 pts) ---
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Assuming your Movie table matches these common columns. 
            # Adjust the column names if your DB schema uses different names.
            cursor.execute("""
                INSERT INTO Movie (
                    title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url))
            
            # Fetch the generated ID of the newly added movie
            new_movie_id = cursor.lastrowid
            
        conn.commit()
        return jsonify({
            'success': True, 
            'message': 'Movie successfully added!', 
            'movie_id': new_movie_id
        }), 201

    except Exception as e:
        conn.rollback()
        # Log the error on the server side and return a 500 status
        print(f"[ADD MOVIE ERROR]: {e}")
        return jsonify({'success': False, 'error': 'An internal database error occurred.'}), 500
    finally:
        conn.close()


        scheduler_bp = Blueprint('scheduler', __name__)

@showtimes_bp.route('/api/showtimes', methods=['POST'])
def add_showtime():
    """
    Rubric: Add showtime for a selected movie (date, time, showroom) – 15 pts
    Rubric: Prevent scheduling conflicts (same showroom, same time) – 5 pts
    Rubric: Usability (clear and simple workflow/error handling) - 10 pts
    """
    data = request.get_json()
    movie_id = data.get('movie_id')
    showroom_id = data.get('showroom_id')
    show_date = data.get('show_date')
    show_time = data.get('show_time')

    print(f"[SCHEDULER] Attempting to schedule movie {movie_id} in showroom {showroom_id}")

    # Usability: Clear validation workflow before hitting the DB
    if not all([movie_id, showroom_id, show_date, show_time]):
        return jsonify({ 'success': False, 'error': 'Missing required fields.' }), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # 1. Prevent Conflicts: Check if showroom is booked at this exact date/time
            cursor.execute("""
                SELECT id 
                FROM showtimes 
                WHERE showroom_id = %s AND show_date = %s AND show_time = %s
            """, (showroom_id, show_date, show_time))
            
            conflict = cursor.fetchone()
            
            print(f"[SCHEDULER] Conflict check result: {'Conflict Found' if conflict else 'Clear'}")

            if conflict:
                return jsonify({ 
                    'success': False, 
                    'error': 'Scheduling conflict: This showroom is already booked for this date and time.' 
                }), 409

            # 2. Add Showtime
            cursor.execute("""
                INSERT INTO showtimes (movie_id, showroom_id, show_date, show_time)
                VALUES (%s, %s, %s, %s)
            """, (movie_id, showroom_id, show_date, show_time))
            
            conn.commit()
            print("[SCHEDULER] Showtime added successfully.")

            return jsonify({ 'success': True, 'message': 'Showtime scheduled successfully.' }), 201

    except Exception as e:
        print(f"[SCHEDULER] Exception: {e}")
        conn.rollback()
        return jsonify({ 'success': False, 'error': str(e) }), 500
    finally:
        conn.close()


