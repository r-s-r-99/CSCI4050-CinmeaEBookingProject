from models.user import User
from models.payment_card import PaymentCard
from models.favorite import Favorite
from services.customer_service import CustomerService


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
        return CustomerService.create_customer(email, password, first_name, last_name, phone_number, promo_subscribed)

    def update_profile(self, first_name, last_name, phone_number, promo_subscribed=None):
        CustomerService.update_customer_profile(self.user_id, first_name, last_name, phone_number, promo_subscribed)

    def get_favorites(self):
        return Favorite.get_by_user(self.user_id)

    def get_payment_cards(self):
        return PaymentCard.get_by_user(self.user_id)