from models.base import BaseModel

class User(BaseModel):
    def __init__(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            'userId':        self.user_id
        }