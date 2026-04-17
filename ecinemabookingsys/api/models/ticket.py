from models.base import BaseModel


class Ticket(BaseModel):
    """
    Ticket domain object - represents a single ticket for a booking.

    Aggregation: One Booking contains many Tickets (1-to-many relationship)
    Composition: Each Ticket references one Seat object
    """

    def __init__(self, ticket_id, booking_id, seat_id, ticket_type, ticket_price, show_date=None, seat=None):
        self.ticket_id = ticket_id
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.ticket_type = ticket_type
        self.ticket_price = ticket_price
        self.show_date = show_date
        self.seat = seat  # Optional: Seat domain object with seat_number, room_id

    def to_dict(self):
        return {
            'ticketId': self.ticket_id,
            'bookingId': self.booking_id,
            'seatId': self.seat_id,
            'seatNumber': self.seat.seat_number if self.seat else None,
            'ticketType': self.ticket_type,
            'ticketPrice': self.ticket_price,
            'showDate': str(self.show_date) if self.show_date else None,
            'seat': self.seat.to_dict() if self.seat else None,
        }
