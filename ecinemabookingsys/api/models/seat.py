from models.base import BaseModel

class Seat(BaseModel):
    def __init__(self, seat_id, seat_number, room_id):
        self.seat_id = seat_id
        self.seat_number = seat_number
        self.room_id = room_id

    def to_dict(self):
        return {
            'seat_id': self.seat_id,
            'seat_number': self.seat_number,
            'room_id': self.room_id,
        }

