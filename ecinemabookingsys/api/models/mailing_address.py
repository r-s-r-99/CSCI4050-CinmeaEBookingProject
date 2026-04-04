from models.base import BaseModel

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
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id,house_number, street, apt, zip FROM MailingAddress WHERE user_id = %s", (user_id,))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()

    def save(self):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id FROM MailingAddress WHERE user_id = %s", (self.user_id,))
                exists = cursor.fetchone()

                if exists:
                    cursor.execute("""
                        UPDATE MailingAddress
                        SET house_number = %s, street = %s, apt = %s, zip = %s
                        WHERE user_id = %s
                    """, (self.house_number, self.street, self.apt, self.zip, self.user_id))
                else:
                    cursor.execute("""
                        INSERT INTO MailingAddress (user_id, house_number, street, apt, zip)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (self.user_id, self.house_number, self.street, self.apt, self.zip))

                conn.commit()
        finally:
            conn.close()