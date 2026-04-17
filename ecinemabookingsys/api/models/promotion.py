from models.base import BaseModel


class Promotion(BaseModel):
    """
    Promotion domain model - represents a discount code.

    Can be optionally applied to a Booking (1-to-0..1 unidirectional).
    """

    def __init__(self, promotion_id, code, discount_percentage, start_date, end_date, tickets_available=None):
        self.promotion_id = promotion_id
        self.code = code
        self.discount_percentage = discount_percentage
        self.start_date = start_date
        self.end_date = end_date
        self.tickets_available = tickets_available

    def to_dict(self):
        return {
            'promotionId': self.promotion_id,
            'code': self.code,
            'discountPercentage': self.discount_percentage,
            'startDate': str(self.start_date) if self.start_date else None,
            'endDate': str(self.end_date) if self.end_date else None,
            'ticketsAvailable': self.tickets_available,
        }
