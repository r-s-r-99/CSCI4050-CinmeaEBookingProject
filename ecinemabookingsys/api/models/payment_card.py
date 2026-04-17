from models.base import BaseModel
from encryption import encrypt, decrypt

class PaymentCard(BaseModel):
    def __init__(self, card_id, user_id, card_name, card_number, cvv, expiration_date):
        self.card_id = card_id
        self.user_id = user_id
        self.card_name = card_name
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date

    def to_dict(self):
        return {
            'cardId':         self.card_id,
            'cardName':       self.card_name,
            'cardNumber':     decrypt(self.card_number),
            'cvv':            decrypt(self.cvv),
            'expirationDate': str(self.expiration_date),
        }
