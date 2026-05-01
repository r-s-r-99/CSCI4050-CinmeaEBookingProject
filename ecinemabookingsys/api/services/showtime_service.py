"""
Showtime Service - Business logic for managing showtimes.

Handles:
- Creating showtimes with conflict detection
- Retrieving showtimes with decoration (conflict status)
- Validation and constraint checking
"""

from datetime import date, datetime
from os import times
from repositories.showtime_repository import ShowtimeRepository
from repositories.showroom_repository import ShowroomRepository
from repositories.movie_repository import MovieRepository
from models.showtime import Showtime


class ShowtimeService:
    """Service for showtime management with conflict detection."""

    def __init__(self):
        self.showtime_repo = ShowtimeRepository()
        self.showroom_repo = ShowroomRepository()
        self.movie_repo = MovieRepository()

    def check_conflict(self, room_id, show_date, show_time):
        """
        Check if there's a scheduling conflict for a showtime.

        A conflict exists if another showtime is scheduled in the same room
        at the exact same time.

        Args:
            room_id: Showroom ID
            show_date: Date of the showtime (YYYY-MM-DD)
            show_time: Time of the showtime (HH:MM)

        Returns:
            dict: {'has_conflict': bool, 'conflicting_showtimes': []}
        """
        from db import get_db

        conn = get_db()
        try:
            # Convert show_time to minutes for easier comparison
            show_time_obj = datetime.strptime(show_time, '%H:%M')
            show_time_minutes = show_time_obj.hour * 60 + show_time_obj.minute

            # Get all showtimes in this room on this date
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT s.showtime_id, s.movie_id, m.title, s.show_time
                    FROM Showtime s
                    JOIN Movie m ON s.movie_id = m.movie_id
                    WHERE s.room_id = %s AND s.show_date = %s
                """, (room_id, show_date))
                existing = cursor.fetchall()

            conflicts = []
            # Check each existing showtime for conflicts
            for row in existing:
                # Convert show_time to string if needed
                existing_time = row['show_time']
                if isinstance(existing_time, str):
                    time_str = existing_time
                else:
                    time_str = str(existing_time)

                # Extract HH:MM if it's HH:MM:SS format
                if len(time_str) > 5:
                    time_str = time_str[:5]

                existing_time_obj = datetime.strptime(time_str, '%H:%M')
                existing_time_minutes = existing_time_obj.hour * 60 + existing_time_obj.minute

                # Movies typically run 90-180 minutes, check 2-hour buffer
                time_diff = abs(show_time_minutes - existing_time_minutes)
                if time_diff == 0:  # Exact same time
                    conflicts.append({
                        'showtime_id': row['showtime_id'],
                        'movie_title': row['title'],
                        'show_time': time_str,
                    })

            return {
                'has_conflict': len(conflicts) > 0,
                'conflicting_showtimes': conflicts
            }
        finally:
            conn.close()

    def create_showtime(self, movie_id, show_date, show_time, room_id):
        """
        Create a new showtime with conflict checking.

        Args:
            movie_id: Movie ID
            show_date: Date (YYYY-MM-DD)
            show_time: Time (HH:MM)
            room_id: Showroom ID

        Returns:
            dict: {'success': bool, 'showtime': Showtime or None, 'error': str or None}
        """
        # Validate movie exists
        movie = self.movie_repo.find_by_id(movie_id)
        if not movie:
            return {'success': False, 'error': 'Movie not found', 'showtime': None}

        # Validate showroom exists
        showroom = self.showroom_repo.find_by_id(room_id)
        if not showroom:
            return {'success': False, 'error': 'Showroom not found', 'showtime': None}

        # Check for conflicts
        conflict_check = self.check_conflict(room_id, show_date, show_time)
        if conflict_check['has_conflict']:
            return {
                'success': False,
                'error': f"Scheduling conflict detected. {len(conflict_check['conflicting_showtimes'])} existing showtime(s) in this room too close to this time.",
                'showtime': None,
                'conflicts': conflict_check['conflicting_showtimes']
            }

        # Create the showtime
        try:
            showtime = Showtime(
                showtime_id=None,
                movie_id=movie_id,
                room_id=room_id,
                show_date=show_date,
                show_time=show_time
            )
            saved_showtime = self.showtime_repo.save(showtime)

            return {
                'success': True,
                'showtime': saved_showtime,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'showtime': None
            }

    def get_all_showtimes_decorated(self):
        """
        Get all showtimes with conflict information decorated.

        Returns: List of showtime dicts with conflict info
        """
        showtimes = self.showtime_repo.get_all()

        decorated = []
        for st in showtimes:
            # Get movie title
            movie = self.movie_repo.find_by_id(st.movie_id)
            movie_title = movie.title if movie else "Unknown"

            # Get showroom number
            showroom = self.showroom_repo.find_by_id(st.room_id)
            room_number = showroom.room_number if showroom else st.room_id

            # Convert show_time to string if it's a time object
            show_time_str = str(st.show_time) if st.show_time else ""
            if show_time_str and len(show_time_str) > 5:  # HH:MM:SS format
                show_time_str = show_time_str[:5]  # Keep only HH:MM

            # Convert show_date to string if it's a date object
            show_date_str = str(st.show_date) if st.show_date else ""

            decorated.append({
                'showtime_id': st.showtime_id,
                'movie_id': st.movie_id,
                'movie_title': movie_title,
                'show_date': show_date_str,
                'show_time': show_time_str,
                'room_id': st.room_id,
                'room_number': room_number,
            })

        return decorated

    def get_showtimes_by_movie_decorated(self, movie_id):
        """
        Get all showtimes for a specific movie with decoration.

        Args:
            movie_id: Movie ID to get showtimes for

        Returns: List of showtime dicts decorated with movie and room info
        """
        showtimes = self.showtime_repo.find_by_movie(movie_id)

        decorated = []
        for st in showtimes:
            # Get movie title
            movie = self.movie_repo.find_by_id(st.movie_id)
            movie_title = movie.title if movie else "Unknown"

            # Get showroom number
            showroom = self.showroom_repo.find_by_id(st.room_id)
            room_number = showroom.room_number if showroom else st.room_id

            # Convert show_time to string if it's a time object
            show_time_str = str(st.show_time) if st.show_time else ""
            if show_time_str and len(show_time_str) > 5:  # HH:MM:SS format
                show_time_str = show_time_str[:5]  # Keep only HH:MM

            # Convert show_date to string if it's a date object
            show_date_str = str(st.show_date) if st.show_date else ""

            decorated.append({
                'showtime_id': st.showtime_id,
                'movie_id': st.movie_id,
                'movie_title': movie_title,
                'show_date': show_date_str,
                'show_time': show_time_str,
                'room_id': st.room_id,
                'room_number': room_number,
            })

        return decorated





