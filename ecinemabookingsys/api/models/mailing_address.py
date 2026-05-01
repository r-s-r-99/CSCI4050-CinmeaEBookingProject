from models.base import BaseModel
from services.mailing_address_service import MailingAddressService


class MailingAddress(BaseModel):
    def __init__(self, user_id, house_number, street, apt, zip):
        self.user_id = user_id
        self.house_number = house_number
        self.street = street
        self.apt = apt
        self.zip = zip

    def to_dict(self):
        return {
            'houseNumber': self.house_number,
            'street':      self.street,
            'apt':         self.apt,
            'zip':         self.zip,
        }

    @classmethod
    def get_by_user(cls, user_id):
        row = MailingAddressService.get_address_by_user(user_id)
        return cls(**row) if row else None

    def save(self):
        MailingAddressService.save_address(
            self.user_id, self.house_number, self.street, self.apt, self.zip
        )
