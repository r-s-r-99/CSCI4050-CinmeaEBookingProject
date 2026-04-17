from models.base import BaseModel


class Showroom(BaseModel):
    """
    Showroom domain model - represents a cinema theater/auditorium.

    1-to-many composition relationship with Seat (owns seats)
    """

    def __init__(self, room_id, room_number, number_of_seats):
        self.room_id = room_id
        self.room_number = room_number
        self.number_of_seats = number_of_seats
        self.seats = []  # Composition: owns multiple Seat objects

    def to_dict(self):
        return {
            'roomId': self.room_id,
            'roomNumber': self.room_number,
            'numberOfSeats': self.number_of_seats,
            'seats': [s.to_dict() for s in self.seats] if self.seats else [],
        }
