from flask import Blueprint, jsonify
from db import get_db

showtimes_bp = Blueprint('showtimes', __name__)

@showtimes_bp.route('/api/showtimes/detail/<int:showtime_id>')
def get_showtime_by_id(showtime_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Showtime WHERE showtime_id = %s", (showtime_id,))
        showtime = cursor.fetchone()
    conn.close()
    if showtime.get('show_time'):
        total_seconds = int(showtime['show_time'].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        showtime['show_time'] = f"{hours:02d}:{minutes:02d}"
    return {"showtime": showtime}

@showtimes_bp.route('/api/showtimes/<int:movie_id>')
def get_showtimes(movie_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Showtime WHERE movie_id = %s", (movie_id,))
        showtimes = cursor.fetchall()
    conn.close()

    # Convert timedelta to string
    for showtime in showtimes:
        if showtime.get('show_time'):
            total_seconds = int(showtime['show_time'].total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            showtime['show_time'] = f"{hours:02d}:{minutes:02d}"

    return {"showtimes": showtimes}

