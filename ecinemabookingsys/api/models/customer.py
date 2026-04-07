from models.user import User
import bcrypt

class Customer(User):
    def __init__(self, user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status):
        super().__init__(user_id)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.role = role
        self.promo_subscribed = promo_subscribed
        self.account_status = account_status

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
    def find_by_id(cls, user_id):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User WHERE user_id = %s
                """, (user_id,))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_email(cls, email):
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User WHERE email = %s
                """, (email,))
                row = cursor.fetchone()
            return cls(**row) if row else None
        finally:
            conn.close()    

    @classmethod
    def create(cls, email, password, first_name, last_name, phone_number, promo_subscribed):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = cls.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO User (email, password, first_name, last_name, phone_number, promo_subscribed, account_status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Inactive')
                """, (email, hashed, first_name, last_name, phone_number, promo_subscribed))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    def update_profile(self, first_name, last_name, phone_number, promo_subscribed):
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

    def update_password(self, new_password):
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE User SET password = %s WHERE user_id = %s", (hashed, self.user_id))
                conn.commit()
        finally:
            conn.close()

    def check_password(self, password):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM User WHERE user_id = %s", (self.user_id,))
                row = cursor.fetchone()
            return bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8'))
        finally:
            conn.close()

    def activate(self):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE User SET account_status = 'Active' WHERE user_id = %s", (self.user_id,))
                conn.commit()
        finally:
            conn.close()