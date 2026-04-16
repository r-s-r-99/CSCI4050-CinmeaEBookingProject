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

    @classmethod
    def get_by_number_and_room(cls, seat_number, room_id):
        """Get seat by seat_number (e.g., 'A1') and room_id"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM Seat
                    WHERE seat_number = %s AND room_id = %s
                """, (seat_number, room_id))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, seat_id):
        """Get seat by seat_id"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Seat WHERE seat_id = %s", (seat_id,))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()

    @classmethod
    def get_by_room(cls, room_id):
        """Get all seats in a room"""
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Seat WHERE room_id = %s ORDER BY seat_number", (room_id,))
                rows = cursor.fetchall()
            return [cls(**row) for row in rows]
        finally:
            conn.close()
