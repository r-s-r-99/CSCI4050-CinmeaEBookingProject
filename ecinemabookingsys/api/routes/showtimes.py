from flask import Blueprint, jsonify
from db import get_db

showtimes_bp = Blueprint('showtimes', __name__)

@showtimes_bp.route('/api/showtimes/<int:movie_id>')
def get_showtimes(movie_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Showtime WHERE movie_id = %s", (movie_id,))
        showtimes = cursor.fetchall()
    conn.close()
    return jsonify(showtimes)