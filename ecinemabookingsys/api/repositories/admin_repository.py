from db import get_db
from models.admin import Admin
from models.customer import Customer


class AdminRepository:
    @staticmethod
    def get_all_users():
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User
                """)
                rows = cursor.fetchall()
            return [Customer(**row) if row['role'] == 'customer' else Admin(**row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def add_movie(title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url):
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Movie (
                        title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url))

                new_movie_id = cursor.lastrowid

            conn.commit()
            return new_movie_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def check_showtime_conflict(showroom_id, show_date, show_time):
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id
                    FROM showtimes
                    WHERE showroom_id = %s AND show_date = %s AND show_time = %s
                """, (showroom_id, show_date, show_time))

                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def add_showtime(movie_id, showroom_id, show_date, show_time):
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO showtimes (movie_id, showroom_id, show_date, show_time)
                    VALUES (%s, %s, %s, %s)
                """, (movie_id, showroom_id, show_date, show_time))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
