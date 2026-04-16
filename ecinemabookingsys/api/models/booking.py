from models.base import BaseModel
from datetime import datetime

class Booking(BaseModel):
    def __init__(self, booking_id, user_id, showtime_id, total_price, booking_date, card_id=None, promotion_id=None, movie=None, showtime=None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.total_price = total_price
        self.booking_date = booking_date
        self.card_id = card_id
        self.promotion_id = promotion_id
        self.tickets = []
        self.movie = movie
        self.showtime = showtime

    def to_dict(self):
        return {
            'id': self.booking_id,
            'bookingId': self.booking_id,
            'userId': self.user_id,
            'showtimeId': self.showtime_id,
            'totalPrice': self.total_price,
            'bookingDate': str(self.booking_date),
            'cardId': self.card_id,
            'promotionId': self.promotion_id,
            'tickets': self.tickets,
            'movie': self.movie,
            'showtime': self.showtime,
        }

    @classmethod
    def get_by_id(cls, booking_id):
        """Get booking with associated tickets, movie, and showtime"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                # Get booking with movie and showtime details
                cursor.execute("""
                    SELECT b.booking_id, b.user_id, b.showtime_id, b.total_price, b.booking_date,
                           b.card_id, b.promotion_id,
                           m.movie_id, m.title, m.genre, m.rating, m.description, m.poster_url, m.trailer_url, m.status,
                           s.show_date, s.show_time, sr.room_id
                    FROM Booking b
                    JOIN Showtime s ON b.showtime_id = s.showtime_id
                    LEFT JOIN Movie m ON s.movie_id = m.movie_id
                    LEFT JOIN Showroom sr ON s.room_id = sr.room_id
                    WHERE b.booking_id = %s
                """, (booking_id,))
                row = cursor.fetchone()

            if not row:
                return None

            booking = cls(
                booking_id=row['booking_id'],
                user_id=row['user_id'],
                showtime_id=row['showtime_id'],
                total_price=row['total_price'],
                booking_date=row['booking_date'],
                card_id=row['card_id'],
                promotion_id=row['promotion_id'],
                movie={
                    'id': row['movie_id'],
                    'title': row['title'],
                    'genre': row['genre'],
                    'rating': row['rating'],
                    'description': row['description'],
                    'poster_url': row['poster_url'],
                    'trailer_url': row['trailer_url'],
                    'status': row['status'],
                },
                showtime={
                    'id': str(row['showtime_id']),
                    'date': row['show_date'].strftime('%A, %B %d, %Y') if row['show_date'] else 'N/A',
                    'time': str(row['show_time']) if row['show_time'] else 'N/A',
                    'theater': f"Theater {row['room_id']}" if row['room_id'] else 'N/A',
                }
            )

            # Get associated tickets
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT ticket_id, seat_id, ticket_type, show_date, ticket_price
                    FROM Ticket WHERE booking_id = %s
                """, (booking_id,))
                tickets = cursor.fetchall()
                booking.tickets = [dict(t) for t in tickets]

            return booking
        finally:
            conn.close()

    @classmethod
    def get_all_by_user(cls, user_id):
        """Get all bookings for a user with movie, showtime, and seat details"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT b.booking_id, b.user_id, b.showtime_id, b.total_price, b.booking_date,
                           b.card_id, b.promotion_id,
                           m.movie_id, m.title, m.genre, m.rating, m.description, m.poster_url, m.trailer_url, m.status,
                           s.show_date, s.show_time, sr.room_id
                    FROM Booking b
                    JOIN Showtime s ON b.showtime_id = s.showtime_id
                    LEFT JOIN Movie m ON s.movie_id = m.movie_id
                    LEFT JOIN Showroom sr ON s.room_id = sr.room_id
                    WHERE b.user_id = %s
                    ORDER BY b.booking_date DESC
                """, (user_id,))
                rows = cursor.fetchall()

            bookings = []
            for row in rows:
                booking = cls(
                    booking_id=row['booking_id'],
                    user_id=row['user_id'],
                    showtime_id=row['showtime_id'],
                    total_price=row['total_price'],
                    booking_date=row['booking_date'],
                    card_id=row['card_id'],
                    promotion_id=row['promotion_id'],
                    movie={
                        'id': row['movie_id'],
                        'title': row['title'],
                        'genre': row['genre'],
                        'rating': row['rating'],
                        'description': row['description'],
                        'poster_url': row['poster_url'],
                        'trailer_url': row['trailer_url'],
                        'status': row['status'],
                    },
                    showtime={
                        'id': str(row['showtime_id']),
                        'date': row['show_date'].strftime('%A, %B %d, %Y') if row['show_date'] else 'N/A',
                        'time': str(row['show_time']) if row['show_time'] else 'N/A',
                        'theater': f"Theater {row['room_id']}" if row['room_id'] else 'N/A',
                    }
                )

                # Get tickets for this booking with seat information
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT t.ticket_id, t.seat_id, t.ticket_type, t.show_date, t.ticket_price,
                               se.seat_number
                        FROM Ticket t
                        LEFT JOIN Seat se ON t.seat_id = se.seat_id
                        WHERE t.booking_id = %s
                    """, (booking.booking_id,))
                    tickets = cursor.fetchall()
                    booking.tickets = [dict(t) for t in tickets]

                bookings.append(booking)

            return bookings
        finally:
            conn.close()

    @classmethod
    def count_by_user(cls, user_id):
        """Count total bookings for a user"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt FROM Booking WHERE user_id = %s", (user_id,))
                return cursor.fetchone()['cnt']
        finally:
            conn.close()

    @classmethod
    def create(cls, user_id, showtime_id, total_price, card_id=None, promotion_id=None):
        """Create a new booking and return booking_id"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Booking (user_id, showtime_id, total_price, card_id, promotion_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, showtime_id, total_price, card_id, promotion_id))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()


class Ticket(BaseModel):
    def __init__(self, ticket_id, booking_id, seat_id, ticket_type, ticket_price, show_date=None):
        self.ticket_id = ticket_id
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.ticket_type = ticket_type
        self.ticket_price = ticket_price
        self.show_date = show_date

    def to_dict(self):
        return {
            'ticketId': self.ticket_id,
            'bookingId': self.booking_id,
            'seatId': self.seat_id,
            'ticketType': self.ticket_type,
            'ticketPrice': self.ticket_price,
            'showDate': str(self.show_date) if self.show_date else None,
        }

    @classmethod
    def get_by_booking(cls, booking_id):
        """Get all tickets for a booking"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT ticket_id, booking_id, seat_id, ticket_type, ticket_price, show_date
                    FROM Ticket WHERE booking_id = %s
                """, (booking_id,))
                rows = cursor.fetchall()
            return [cls(**row) for row in rows]
        finally:
            conn.close()

    @classmethod
    def create_batch(cls, booking_id, seats_with_types_and_prices):
        """
        Create multiple tickets for a booking

        Args:
            booking_id: The booking ID
            seats_with_types_and_prices: List of dicts like:
                [
                    {'seat_id': 123, 'ticket_type': 'Adult', 'ticket_price': 12.00, 'show_date': '2026-04-20'},
                    {'seat_id': 124, 'ticket_type': 'Child', 'ticket_price': 6.00, 'show_date': '2026-04-20'},
                ]
        """
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                for seat_data in seats_with_types_and_prices:
                    cursor.execute("""
                        INSERT INTO Ticket (booking_id, seat_id, ticket_type, ticket_price, show_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        booking_id,
                        seat_data['seat_id'],
                        seat_data['ticket_type'],
                        seat_data['ticket_price'],
                        seat_data.get('show_date'),
                    ))
                conn.commit()
        finally:
            conn.close()

    @classmethod
    def create(cls, booking_id, seat_id, ticket_type, ticket_price, show_date=None):
        """Create a single ticket"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Ticket (booking_id, seat_id, ticket_type, ticket_price, show_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (booking_id, seat_id, ticket_type, ticket_price, show_date))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()
