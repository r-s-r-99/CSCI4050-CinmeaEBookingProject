from models.base import BaseModel
from models.ticket import Ticket
from datetime import datetime

class Booking(BaseModel):
    def __init__(self, booking_id, user_id, showtime_id, total_price, booking_date,
                 card_id=None, promotion_id=None, movie=None, showtime=None,
                 payment_card=None, promotion=None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.total_price = total_price
        self.booking_date = booking_date
        self.card_id = card_id  # Keep for backward compatibility
        self.promotion_id = promotion_id  # Keep for backward compatibility
        self.tickets = []
        self.movie = movie  # For convenience (from Showtime)
        self.showtime = showtime  # Showtime domain object
        self.payment_card = payment_card  # PaymentCard domain object
        self.promotion = promotion  # Promotion domain object

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
            'tickets': [t.to_dict() for t in self.tickets] if self.tickets else [],
            'movie': self.movie,
            'showtime': self.showtime.to_dict() if self.showtime else None,
            'paymentCard': self.payment_card.to_dict() if self.payment_card else None,
            'promotion': self.promotion.to_dict() if self.promotion else None,
        }

