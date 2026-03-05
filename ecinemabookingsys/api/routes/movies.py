from flask import Blueprint
from db import get_db
import pandas as pd

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/api/movies')
def get_movies():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie") 
        home_movies = cursor.fetchall()
    conn.close()
    return {"movies": home_movies}

@movies_bp.route('/api/movies/<int:movie_id>')
def get_movies_details(movie_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()
    conn.close()
    return {"movie": movie}

@movies_bp.route('/api/movies/now-showing')
def get_now_showing():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie WHERE status = 'Currently Running'")
        movies = cursor.fetchall()
    conn.close()
    return {"movies": movies}

@movies_bp.route('/api/movies/coming-soon')
def get_coming_soon():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie WHERE status = 'Coming Soon'")
        movies = cursor.fetchall()
    conn.close()
    return {"movies": movies}

@movies_bp.route('/api/movies/<string:genre>')
def get_movies_by_genre(genre):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie WHERE genre = %s", (genre,))
        movies = cursor.fetchall()
    conn.close()
    return {"movies": movies}
