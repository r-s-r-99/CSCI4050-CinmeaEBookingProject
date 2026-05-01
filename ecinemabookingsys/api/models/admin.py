from models.user import User


class Admin(User):
    def to_dict(self):
        return {
            'userId':        self.user_id,
            'email':         self.email,
            'firstName':     self.first_name,
            'lastName':      self.last_name,
            'phoneNumber':   self.phone_number,
            'role':          self.role,
            'accountStatus': self.account_status,
        }