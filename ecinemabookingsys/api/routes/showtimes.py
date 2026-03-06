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
    if showtime and showtime.get('show_time'):
        total_seconds = int(showtime['show_time'].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        period = 'AM' if hours < 12 else 'PM'
        hours_12 = hours % 12 or 12  # converts 0 to 12 for midnight, 13 to 1, etc.
        showtime['show_time'] = f"{hours_12}:{minutes:02d} {period}"
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
            period = 'AM' if hours < 12 else 'PM'
            hours_12 = hours % 12 or 12  # converts 0 to 12 for midnight, 13 to 1, etc.
            showtime['show_time'] = f"{hours_12}:{minutes:02d} {period}"

    return {"showtimes": showtimes}

