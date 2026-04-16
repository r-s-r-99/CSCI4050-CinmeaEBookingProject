from models.base import BaseModel


class Ticket(BaseModel):
    """
    Ticket domain object - represents a single ticket for a booking.

    Aggregation: One Booking contains many Tickets (1-to-many relationship)
    """

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
