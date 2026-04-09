from db import get_db

class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_db(cls):
        return get_db()

    def to_dict(self):
        raise NotImplementedError