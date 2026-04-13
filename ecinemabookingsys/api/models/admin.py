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

    def get_all_users(self):
        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, email, first_name, last_name, phone_number, role, promo_subscribed, account_status
                    FROM User
                """)
                rows = cursor.fetchall()
            from models.customer import Customer
            return [Customer(**row) if row['role'] == 'customer' else Admin(**row) for row in rows]
        finally:
            conn.close()