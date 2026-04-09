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

    @classmethod
    def get_by_user(cls, user_id):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM PaymentCard WHERE user_id = %s", (user_id,))
                rows = cursor.fetchall()
            return [cls(**row) for row in rows]
        finally:
            conn.close()

    @classmethod
    def count_by_user(cls, user_id):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt FROM PaymentCard WHERE user_id = %s", (user_id,))
                return cursor.fetchone()['cnt']
        finally:
            conn.close()

    @classmethod
    def create(cls, user_id, card_name, card_number, cvv, expiration_date):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PaymentCard (user_id, card_name, card_number, cvv, expiration_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, card_name, encrypt(card_number), encrypt(cvv), expiration_date))
                conn.commit()
        finally:
            conn.close()

    def update(self, card_name, card_number, cvv, expiration_date):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE PaymentCard
                    SET card_name = %s, card_number = %s, cvv = %s, expiration_date = %s
                    WHERE card_id = %s AND user_id = %s
                """, (card_name, encrypt(card_number), encrypt(cvv), expiration_date, self.card_id, self.user_id))
                conn.commit()
        finally:
            conn.close()

    def delete(self):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM PaymentCard WHERE card_id = %s", (self.card_id,))
                conn.commit()
        finally:
            conn.close()