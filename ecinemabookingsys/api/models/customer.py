from models.user import User
from models.payment_card import PaymentCard
from models.favorite import Favorite
import bcrypt

class Customer(User):
    def to_dict(self):
        return {
            'userId':        self.user_id,
            'email':         self.email,
            'firstName':     self.first_name,
            'lastName':      self.last_name,
            'phoneNumber':   self.phone_number,
            'role':          self.role,
            'promotions':    self.promo_subscribed,
            'accountStatus': self.account_status,
        }

    @classmethod
    def create(cls, email, password, first_name, last_name, phone_number, promo_subscribed):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO User (email, password, first_name, last_name, phone_number, promo_subscribed, account_status, role)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Inactive', 'customer')
                """, (email, hashed, first_name, last_name, phone_number, promo_subscribed))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    def update_profile(self, first_name, last_name, phone_number, promo_subscribed=None):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE User SET first_name = %s, last_name = %s, phone_number = %s, promo_subscribed = %s
                    WHERE user_id = %s
                """, (first_name, last_name, phone_number, promo_subscribed, self.user_id))
                conn.commit()
        finally:
            conn.close()

    def get_favorites(self):
        return Favorite.get_by_user(self.user_id)

    def get_payment_cards(self):
        return PaymentCard.get_by_user(self.user_id)