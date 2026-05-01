"""
Booking Repository - Data access for Booking and Ticket entities.

Extracted from models/booking.py - handles all database queries.
Returns Booking domain objects with composed Movie, Showtime, and Ticket objects.
"""

from repositories.base_repository import CRUDRepository


class BookingRepository(CRUDRepository):
    """
    Repository for Booking entities.

    Responsibilities:
    - Find bookings by ID, user, or other criteria
    - Save new bookings
    - Delete bookings
    - Always returns Booking domain objects, never dicts
    """

    def find_by_id(self, booking_id):
        """
        Find booking by ID with all related data.

        Returns: Booking object with showtime, payment_card, promotion, and tickets populated, or None
        """
        # Import here to avoid circular imports
        from models.booking import Booking
        from models.ticket import Ticket
        from models.showtime import Showtime
        from models.promotion import Promotion
        from models.payment_card import PaymentCard
        from models.seat import Seat

        query = """
            SELECT b.booking_id, b.user_id, b.showtime_id, b.total_price, b.booking_date,
                   b.card_id, b.promotion_id,
                   m.movie_id, m.title, m.genre, m.rating, m.description, m.poster_url, m.trailer_url, m.status,
                   s.showtime_id as st_showtime_id, s.movie_id as st_movie_id, s.room_id, s.show_date, s.show_time,
                   sr.room_id as sr_room_id, sr.room_number, sr.number_of_seats,
                   p.promotion_id as p_promotion_id, p.code, p.discount_percentage, p.start_date, p.end_date, p.tickets_available,
                   pc.card_id as pc_card_id, pc.user_id as pc_user_id, pc.card_name, pc.card_number, pc.cvv, pc.expiration_date
            FROM Booking b
            JOIN Showtime s ON b.showtime_id = s.showtime_id
            LEFT JOIN Movie m ON s.movie_id = m.movie_id
            LEFT JOIN Showroom sr ON s.room_id = sr.room_id
            LEFT JOIN Promotion p ON b.promotion_id = p.promotion_id
            LEFT JOIN PaymentCard pc ON b.card_id = pc.card_id
            WHERE b.booking_id = %s
        """

        row = self.execute_query_one(query, (booking_id,))
        if not row:
            return None

        # Create Showtime domain object
        showtime = Showtime(
            showtime_id=row.get("st_showtime_id"),
            movie_id=row.get("st_movie_id"),
            room_id=row.get("room_id"),
            show_date=row.get("show_date"),
            show_time=row.get("show_time"),
        )

        # Create Promotion domain object if exists
        promotion = None
        if row.get("p_promotion_id"):
            promotion = Promotion(
                promotion_id=row.get("p_promotion_id"),
                code=row.get("code"),
                discount_percentage=row.get("discount_percentage"),
                start_date=row.get("start_date"),
                end_date=row.get("end_date"),
                tickets_available=row.get("tickets_available"),
            )

        # Create PaymentCard domain object if exists
        payment_card = None
        if row.get("pc_card_id"):
            payment_card = PaymentCard(
                card_id=row.get("pc_card_id"),
                user_id=row.get("pc_user_id"),
                card_name=row.get("card_name"),
                card_number=row.get("card_number"),
                cvv=row.get("cvv"),
                expiration_date=row.get("expiration_date"),
            )

        # Create Booking domain object with composed objects
        booking = Booking(
            booking_id=row["booking_id"],
            user_id=row["user_id"],
            showtime_id=row["showtime_id"],
            total_price=row["total_price"],
            booking_date=row["booking_date"],
            card_id=row["card_id"],
            promotion_id=row["promotion_id"],
            movie={  # Movie data from joined Movie table
                "id": row["movie_id"],
                "title": row["title"],
                "genre": row["genre"],
                "rating": row["rating"],
                "description": row["description"],
                "poster_url": row["poster_url"],
                "trailer_url": row["trailer_url"],
                "status": row["status"],
            },
            showtime=showtime,  # Now a Showtime object
            payment_card=payment_card,  # Now a PaymentCard object or None
            promotion=promotion,  # Now a Promotion object or None
        )

        # Fetch and attach tickets with seat information
        ticket_query = """
            SELECT t.ticket_id, t.booking_id, t.seat_id, t.ticket_type, t.show_date, t.ticket_price,
                   s.seat_number, s.room_id
            FROM Ticket t
            LEFT JOIN Seat s ON t.seat_id = s.seat_id
            WHERE t.booking_id = %s
        """
        tickets_data = self.execute_query(ticket_query, (booking_id,))
        booking.tickets = []
        for t in tickets_data:
            # Create Seat domain object if seat data exists
            seat = None
            if t.get("seat_id"):
                seat = Seat(
                    seat_id=t.get("seat_id"),
                    seat_number=t.get("seat_number"),
                    room_id=t.get("room_id")
                )

            # Create Ticket with composed Seat object
            ticket = Ticket(
                ticket_id=t["ticket_id"],
                booking_id=t["booking_id"],
                seat_id=t["seat_id"],
                ticket_type=t["ticket_type"],
                ticket_price=t["ticket_price"],
                show_date=t["show_date"],
                seat=seat
            )
            booking.tickets.append(ticket)

        return booking



    def find_all_by_user(self, user_id):
        """
        Find all bookings for a user with full details.

        Returns: List of Booking objects with all composed data
        """
        from models.booking import Booking
        from models.ticket import Ticket
        from models.showtime import Showtime
        from models.promotion import Promotion
        from models.payment_card import PaymentCard
        from models.seat import Seat

        query = """
            SELECT b.booking_id, b.user_id, b.showtime_id, b.total_price, b.booking_date,
                   b.card_id, b.promotion_id,
                   m.movie_id, m.title, m.genre, m.rating, m.description, m.poster_url, m.trailer_url, m.status,
                   s.showtime_id as st_showtime_id, s.movie_id as st_movie_id, s.room_id, s.show_date, s.show_time,
                   sr.room_id as sr_room_id, sr.room_number, sr.number_of_seats,
                   p.promotion_id as p_promotion_id, p.code, p.discount_percentage, p.start_date, p.end_date, p.tickets_available,
                   pc.card_id as pc_card_id, pc.user_id as pc_user_id, pc.card_name, pc.card_number, pc.cvv, pc.expiration_date
            FROM Booking b
            LEFT JOIN Showtime s ON b.showtime_id = s.showtime_id
            LEFT JOIN Movie m ON s.movie_id = m.movie_id
            LEFT JOIN Showroom sr ON s.room_id = sr.room_id
            LEFT JOIN Promotion p ON b.promotion_id = p.promotion_id
            LEFT JOIN PaymentCard pc ON b.card_id = pc.card_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """

        rows = self.execute_query(query, (user_id,))
        bookings = []

        for row in rows:
            # Create Showtime domain object
            showtime = Showtime(
                showtime_id=row.get("st_showtime_id"),
                movie_id=row.get("st_movie_id"),
                room_id=row.get("room_id"),
                show_date=row.get("show_date"),
                show_time=row.get("show_time"),
            )

            # Create Promotion domain object if exists
            promotion = None
            if row.get("p_promotion_id"):
                promotion = Promotion(
                    promotion_id=row.get("p_promotion_id"),
                    code=row.get("code"),
                    discount_percentage=row.get("discount_percentage"),
                    start_date=row.get("start_date"),
                    end_date=row.get("end_date"),
                    tickets_available=row.get("tickets_available"),
                )

            # Create PaymentCard domain object if exists
            payment_card = None
            if row.get("pc_card_id"):
                payment_card = PaymentCard(
                    card_id=row.get("pc_card_id"),
                    user_id=row.get("pc_user_id"),
                    card_name=row.get("card_name"),
                    card_number=row.get("card_number"),
                    cvv=row.get("cvv"),
                    expiration_date=row.get("expiration_date"),
                )

            booking = Booking(
                booking_id=row["booking_id"],
                user_id=row["user_id"],
                showtime_id=row["showtime_id"],
                total_price=row["total_price"],
                booking_date=row["booking_date"],
                card_id=row["card_id"],
                promotion_id=row["promotion_id"],
                movie={
                    "id": row["movie_id"],
                    "title": row["title"],
                    "genre": row["genre"],
                    "rating": row["rating"],
                    "description": row["description"],
                    "poster_url": row["poster_url"],
                    "trailer_url": row["trailer_url"],
                    "status": row["status"],
                },
                showtime=showtime,  # Now a Showtime object
                payment_card=payment_card,  # Now a PaymentCard object or None
                promotion=promotion,  # Now a Promotion object or None
            )

            # Attach tickets with seat information for this booking
            ticket_query = """
                SELECT t.ticket_id, t.booking_id, t.seat_id, t.ticket_type, t.show_date, t.ticket_price,
                       s.seat_number, s.room_id
                FROM Ticket t
                LEFT JOIN Seat s ON t.seat_id = s.seat_id
                WHERE t.booking_id = %s
            """
            tickets_data = self.execute_query(ticket_query, (row["booking_id"],))
            booking.tickets = []
            for t in tickets_data:
                # Create Seat domain object if seat data exists
                seat = None
                if t.get("seat_id"):
                    seat = Seat(
                        seat_id=t.get("seat_id"),
                        seat_number=t.get("seat_number"),
                        room_id=t.get("room_id")
                    )

                # Create Ticket with composed Seat object
                ticket = Ticket(
                    ticket_id=t["ticket_id"],
                    booking_id=t["booking_id"],
                    seat_id=t["seat_id"],
                    ticket_type=t["ticket_type"],
                    ticket_price=t["ticket_price"],
                    show_date=t["show_date"],
                    seat=seat
                )
                booking.tickets.append(ticket)

            bookings.append(booking)

        return bookings


    def save(self, booking):
        """
        Save booking to database.

        Args: Booking domain object
        Returns: Booking with booking_id populated if new
        """
        if hasattr(booking, "booking_id") and booking.booking_id:
            # Update existing
            query = """
                UPDATE Booking
                SET user_id = %s, showtime_id = %s, total_price = %s,
                    card_id = %s, promotion_id = %s
                WHERE booking_id = %s
            """
            self.execute_update(
                query,
                (
                    booking.user_id,
                    booking.showtime_id,
                    booking.total_price,
                    booking.card_id,
                    booking.promotion_id,
                    booking.booking_id,
                ),
            )
        else:
            # Insert new
            query = """
                INSERT INTO Booking (user_id, showtime_id, total_price, card_id, promotion_id, booking_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            booking_id = self.execute_insert_get_id(
                query,
                (
                    booking.user_id,
                    booking.showtime_id,
                    booking.total_price,
                    booking.card_id,
                    booking.promotion_id,
                ),
            )
            booking.booking_id = booking_id

        return booking

    def delete(self, booking):
        """Delete booking and associated tickets."""
        # Delete tickets first (foreign key constraint)
        ticket_query = "DELETE FROM Ticket WHERE booking_id = %s"
        self.execute_update(ticket_query, (booking.booking_id,))

        # Delete booking
        booking_query = "DELETE FROM Booking WHERE booking_id = %s"
        self.execute_update(booking_query, (booking.booking_id,))

        return True

    def get_all(self):
        """Get all bookings (not used in practice, but required by abstract interface)."""
        query = "SELECT booking_id FROM Booking ORDER BY booking_date DESC"
        rows = self.execute_query(query)
        return [self.find_by_id(row["booking_id"]) for row in rows]

    def count_by_user(self, user_id):
        """Count total bookings for a user."""
        query = "SELECT COUNT(*) as count FROM Booking WHERE user_id = %s"
        row = self.execute_query_one(query, (user_id,))
        return row["count"] if row else 0


class TicketRepository(CRUDRepository):
    """
    Repository for Ticket entities.

    Handles creation and deletion of tickets.
    """

    def find_by_id(self, ticket_id):
        """Find ticket by ID."""
        from models.ticket import Ticket

        query = "SELECT * FROM Ticket WHERE ticket_id = %s"
        row = self.execute_query_one(query, (ticket_id,))
        return Ticket(**row) if row else None

    def save(self, ticket):
        """Save ticket (insert or update)."""
        if hasattr(ticket, "ticket_id") and ticket.ticket_id:
            # Update
            query = """
                UPDATE Ticket
                SET booking_id = %s, seat_id = %s, ticket_type = %s, show_date = %s, ticket_price = %s
                WHERE ticket_id = %s
            """
            self.execute_update(
                query,
                (
                    ticket.booking_id,
                    ticket.seat_id,
                    ticket.ticket_type,
                    ticket.show_date,
                    ticket.ticket_price,
                    ticket.ticket_id,
                ),
            )
        else:
            # Insert
            query = """
                INSERT INTO Ticket (booking_id, seat_id, ticket_type, show_date, ticket_price)
                VALUES (%s, %s, %s, %s, %s)
            """
            ticket_id = self.execute_insert_get_id(
                query,
                (
                    ticket.booking_id,
                    ticket.seat_id,
                    ticket.ticket_type,
                    ticket.show_date,
                    ticket.ticket_price,
                ),
            )
            ticket.ticket_id = ticket_id

        return ticket

    def create_batch(self, tickets_data):
        """Create multiple tickets at once. Accepts both Ticket objects and dicts."""
        query = """
            INSERT INTO Ticket (booking_id, seat_id, ticket_type, show_date, ticket_price)
            VALUES (%s, %s, %s, %s, %s)
        """

        conn = self.get_db()
        try:
            with conn.cursor() as cursor:
                for ticket_data in tickets_data:
                    # Handle both Ticket objects and dicts
                    if isinstance(ticket_data, dict):
                        # Dict format
                        booking_id = ticket_data.get("booking_id")
                        seat_id = ticket_data.get("seat_id")
                        ticket_type = ticket_data.get("ticket_type")
                        show_date = ticket_data.get("show_date")
                        ticket_price = ticket_data.get("ticket_price")
                    else:
                        # Ticket object format
                        booking_id = ticket_data.booking_id
                        seat_id = ticket_data.seat_id
                        ticket_type = ticket_data.ticket_type
                        show_date = ticket_data.show_date
                        ticket_price = ticket_data.ticket_price

                    cursor.execute(
                        query,
                        (booking_id, seat_id, ticket_type, show_date, ticket_price),
                    )
                conn.commit()
            return True
        finally:
            conn.close()

    def delete(self, ticket):
        """Delete ticket."""
        # Handle both Ticket objects and dicts
        ticket_id = ticket.ticket_id if hasattr(ticket, 'ticket_id') else ticket["ticket_id"]
        query = "DELETE FROM Ticket WHERE ticket_id = %s"
        self.execute_update(query, (ticket_id,))
        return True

    def get_all(self):
        """Get all tickets."""
        from models.ticket import Ticket

        query = "SELECT * FROM Ticket"
        rows = self.execute_query(query)
        return [Ticket(**dict(row)) for row in rows]

    def find_booked_seats_by_showtime(self, showtime_id):
        """Get all booked seat IDs for a specific showtime."""
        query = """
            SELECT DISTINCT t.seat_id
            FROM Ticket t
            JOIN Booking b ON t.booking_id = b.booking_id
            WHERE b.showtime_id = %s
        """
        rows = self.execute_query(query, (showtime_id,))
        return [row["seat_id"] for row in rows]

