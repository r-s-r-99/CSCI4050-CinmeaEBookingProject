"""
BookingService - Business logic orchestrator for booking operations.

This service coordinates repositories, models, and email sending to implement
the complete booking workflow. Routes should call service methods, not repositories directly.
"""

import secrets
from datetime import datetime, timedelta
from db import get_db
from repositories.booking_repository import BookingRepository, TicketRepository
from repositories.movie_repository import MovieRepository
from repositories.showtime_repository import ShowtimeRepository
from repositories.seat_repository import SeatRepository
from models.ticket import Ticket


class BookingService:
    """
    Service for managing bookings.

    Responsibilities:
    - Orchestrate repositories for booking operations
    - Implement the booking state machine (temporary -> payment -> verified)
    - Handle email notifications
    - Enforce business rules
    """

    def __init__(self):
        """Initialize service with repositories."""
        self.booking_repo = BookingRepository()
        self.ticket_repo = TicketRepository()
        self.movie_repo = MovieRepository()
        self.showtime_repo = ShowtimeRepository()
        self.seat_repo = SeatRepository()

    def create_temporary_booking(self, user_id, showtime_id, seats, email, total_price):
        """
        Create a temporary booking session (before payment).

        Args:
            user_id: ID of user making booking
            showtime_id: ID of showtime
            seats: List of seat objects with category
            email: Email for booking confirmation
            total_price: Total booking cost

        Returns:
            Dictionary with temp_booking_token and expiration time
        """
        # Generate secure token
        token = secrets.token_urlsafe(32)

        # Calculate expiration (24 hours from now)
        expires_at = datetime.now() + timedelta(hours=24)

        # Store in session for now (will persist to DB if temporary_bookings table exists)
        booking_data = {
            "user_id": user_id,
            "showtime_id": showtime_id,
            "seats": seats,
            "email": email,
            "total_price": total_price,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
        }

        # Try to store in database if table exists
        try:
            query = """
                INSERT INTO temporary_bookings (token, user_id, booking_data, expires_at)
                VALUES (%s, %s, %s, %s)
            """
            conn = get_db()
            try:
                with conn.cursor() as cursor:
                    import json

                    cursor.execute(
                        query,
                        (token, user_id, json.dumps(booking_data), expires_at),
                    )
                    conn.commit()
            finally:
                conn.close()
        except Exception as e:
            # Table doesn't exist - that's okay, session storage is fallback
            print(f"[BOOKING] Could not store in DB: {e}. Using session storage.")

        return {
            "temp_booking_token": token,
            "expires_at": expires_at.isoformat(),
        }

    def verify_temporary_booking(self, token, booking_data_from_session):
        """
        Verify temporary booking exists and hasn't expired.

        Returns: Booking data if valid, raises exception if invalid/expired
        """
        import json as json_lib

        # Try database first
        query = """
            SELECT booking_data, expires_at
            FROM temporary_bookings
            WHERE token = %s AND expires_at > NOW()
        """

        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (token,))
                row = cursor.fetchone()

            if row:
                # Found valid token in database
                booking_data = json_lib.loads(row["booking_data"])
                return booking_data, True  # Found in DB
        finally:
            conn.close()

        # Fallback to session data
        if booking_data_from_session:
            # Verify token matches
            if booking_data_from_session.get("token") == token:
                return booking_data_from_session, False  # From session, not DB
            else:
                raise ValueError("Invalid booking session")

        raise ValueError("Booking session not found or expired")

    def process_payment(self, token, card_data):
        """
        Process placeholder payment.

        In production, this would integrate with payment gateway.
        Returns: True if successful

        Args:
            token: Temporary booking token
            card_data: Card information (placeholder validation only)
        """
        # Validate card format (basic checks)
        card_number = card_data.get("cardNumber", "").replace(" ", "")
        if not card_number or len(card_number) < 13:
            raise ValueError("Invalid card number")

        expiry = card_data.get("expiry", "")  # Frontend sends 'expiry', not 'expirationDate'
        if not expiry or "/" not in expiry:
            raise ValueError("Invalid expiration date format (MM/YY required)")

        cvc = card_data.get("cvc", "")
        if not cvc or len(cvc) < 3:
            raise ValueError("Invalid CVC")

        name_on_card = card_data.get("nameOnCard", "")
        if not name_on_card or not name_on_card.strip():
            raise ValueError("Name on card is required")

        # Placeholder: In real system, call payment gateway
        print(f"[PAYMENT] Processing payment for token: {token}")
        print(f"[PAYMENT] Card: {card_number[-4:].rjust(16, '*')}")

        return True

    def verify_booking(self, token, booking_data, user_id):
        """
        Finalize booking after email verification.

        Creates actual Booking and Ticket records in database.

        Args:
            token: Verification token
            booking_data: Data from temporary booking
            user_id: User ID

        Returns: Booking domain object
        """
        from models.booking import Booking

        # Extract data
        showtime_id = booking_data.get("showtime_id")
        seats = booking_data.get("seats", [])
        total_price = booking_data.get("total_price")

        # Get room_id for seat lookups
        showtime_repo = ShowtimeRepository()
        room_id = showtime_repo.get_room_id(showtime_id)

        # Create Booking record
        booking = Booking(
            booking_id=None,  # Will be generated
            user_id=user_id,
            showtime_id=showtime_id,
            total_price=total_price,
            booking_date=datetime.now(),
        )
        booking = self.booking_repo.save(booking)

        # Create Ticket records
        tickets_to_create = []

        for seat in seats:
            # Use repository to lookup seat by seat number and room
            seat_obj = self.seat_repo.find_by_number_and_room(
                seat.get("id"), room_id
            )  # e.g., "A1" -> Seat object
            seat_id = seat_obj.seat_id if seat_obj else None

            if not seat_id:
                print(f"[WARNING] Could not find seat {seat.get('id')} in room {room_id}")
                continue

            # Create Ticket objects (not dicts)
            ticket = Ticket(
                ticket_id=None,  # Will be generated by DB
                booking_id=booking.booking_id,
                seat_id=seat_id,
                ticket_type=seat.get("category", "adult"),
                ticket_price=self._get_ticket_price(seat.get("category", "adult")),
                show_date=booking_data.get("show_date")
            )
            tickets_to_create.append(ticket)

        # Batch create tickets
        if tickets_to_create:
            self.ticket_repo.create_batch(tickets_to_create)

        # Delete temporary booking record if it exists
        try:
            conn = get_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM temporary_bookings WHERE token = %s", (token,)
                    )
                    conn.commit()
            finally:
                conn.close()
        except Exception as e:
            print(f"[BOOKING] Could not delete temp booking: {e}")

        # Reload booking with tickets and related data
        return self.booking_repo.find_by_id(booking.booking_id)

    def get_booking(self, booking_id, user_id=None):
        """
        Get booking details.

        Args:
            booking_id: Booking ID
            user_id: Optional - if provided, verify authorization

        Returns: Booking domain object or None
        """
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            return None

        # Verify ownership if user_id provided
        if user_id and booking.user_id != user_id:
            return None  # Unauthorized

        return booking

    def get_user_bookings(self, user_id):
        """Get all bookings for a user."""
        return self.booking_repo.find_all_by_user(user_id)

    def cancel_booking(self, booking_id):
        """Cancel a booking."""
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            return False

        return self.booking_repo.delete(booking)

    # Helper methods
    @staticmethod
    def _get_ticket_price(category):
        """Get price for ticket category."""
        prices = {
            "adult": 12,
            "senior": 8,
            "child": 6,
        }
        return prices.get(category, 12)
