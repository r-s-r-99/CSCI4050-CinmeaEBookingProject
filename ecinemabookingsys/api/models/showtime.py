from models.base import BaseModel


class Showtime(BaseModel):
    """
    Showtime domain model - represents a scheduled movie showing.

    1-to-1 relationship with Showroom (unidirectional)
    1-to-many relationship with Seat (bidirectional)
    """

    def __init__(self, showtime_id, movie_id, room_id, show_date, show_time):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.room_id = room_id
        self.show_date = show_date
        self.show_time = show_time

        # Optional: populated by repository when needed
        self.movie = None  # Movie object
        self.showroom = None  # Showroom object
        self.seats = []  # List of Seat objects (1-to-many)

    def to_dict(self):
        return {
            'showtimeId': self.showtime_id,
            'movieId': self.movie_id,
            'roomId': self.room_id,
            'showDate': str(self.show_date) if self.show_date else None,
            'showTime': str(self.show_time) if self.show_time else None,
            'movie': self.movie.to_dict() if self.movie else None,
            'showroom': self.showroom.to_dict() if self.showroom else None,
            'seats': [s.to_dict() for s in self.seats] if self.seats else [],
        }
