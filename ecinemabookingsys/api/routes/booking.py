from flask import Blueprint, request, jsonify, session
from models.booking import Booking, Ticket
from models.seat import Seat
from models.user import User
from email_utils import send_confirmation_email
import secrets
from datetime import datetime, timedelta
from db import get_db

booking_bp = Blueprint('booking', __name__)

# Helper function to send booking confirmation email
def send_booking_confirmation_email(to_email, first_name, token, booking_details):
    """Send booking confirmation email with verification link"""
    from email_utils import SMTP_HOST, SMTP_PORT, SMTP_USER, BASE_URL
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from dotenv import load_dotenv
    import os

    load_dotenv()
    SMTP_PASS = os.getenv('SMTP_PASS')

    verify_url = f"{BASE_URL}/api/bookings/verify/{token}"

    movie_title = booking_details.get('movie_title', 'N/A')
    showtime = booking_details.get('showtime', 'N/A')
    total_price = booking_details.get('total_price', 0)
    seat_count = booking_details.get('seat_count', 0)

    html = f"""
    <html>
      <body>
        <h2>Booking Confirmation Required</h2>
        <p>Hi {first_name}, thank you for your booking!</p>
        <div style="background-color:#f3f4f6; padding:16px; border-radius:8px; margin:16px 0;">
          <p><strong>Movie:</strong> {movie_title}</p>
          <p><strong>Showtime:</strong> {showtime}</p>
          <p><strong>Seats:</strong> {seat_count}</p>
          <p><strong>Total Price:</strong> ${total_price:.2f}</p>
        </div>
        <p>Please click the button below to confirm your booking:</p>
        <a href="{verify_url}"
           style="background-color:#dc2626;color:white;padding:12px 24px;
                  text-decoration:none;border-radius:8px;display:inline-block;">
          Confirm Booking
        </a>
        <p>This link expires in 24 hours.</p>
        <p>If you did not make this booking, ignore this email.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Confirm your CineBook booking - {movie_title}'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[EMAIL] Error sending booking confirmation: {e}")
        return False


@booking_bp.route('/api/bookings/create-temporary', methods=['POST'])
def create_temporary_booking():
    """Create temporary booking session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['showtime_id', 'seats', 'email', 'total_price', 'movie_details']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create verification token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)

        # Prepare booking data
        booking_data = {
            'user_id': session['user_id'],
            'showtime_id': data['showtime_id'],
            'seats': data['seats'],  # List of dicts: [{'seat_id': X, 'ticket_type': 'Adult', 'price': 12}]
            'email': data['email'],
            'total_price': data['total_price'],
            'movie_details': data['movie_details'],
            'token': token,
            'expires_at': expires_at.isoformat(),
        }

        # Store temporary booking in session
        session['temp_booking'] = booking_data
        session.modified = True

        # Store in database for persistence across sessions/browsers
        import json
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                # Insert token for email verification
                cursor.execute("""
                    INSERT INTO PasswordResetToken (user_id, token, expires_at, type)
                    VALUES (%s, %s, %s, 'booking_verification')
                """, (session['user_id'], token, expires_at))

                # Try to insert into temporary_bookings table if it exists
                try:
                    cursor.execute("""
                        INSERT INTO temporary_bookings (token, user_id, booking_data, expires_at)
                        VALUES (%s, %s, %s, %s)
                    """, (token, session['user_id'], json.dumps(booking_data), expires_at))
                except Exception as e:
                    # Table might not exist - log and continue
                    print(f"[BOOKING] Note: temporary_bookings table not found. Using session storage only: {e}")

                conn.commit()
        finally:
            conn.close()

        return jsonify({
            'status': 'success',
            'temp_booking_token': token,
            'expires_at': expires_at.isoformat(),
        }), 200

    except Exception as e:
        print(f"[BOOKING] Error creating temporary booking: {e}")
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/api/bookings/process-payment', methods=['POST'])
def process_payment():
    """Process placeholder payment and send verification email"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        if 'temp_booking_token' not in data or 'card_data' not in data:
            return jsonify({'error': 'Missing booking token or card data'}), 400

        # Get temporary booking from session or database
        temp_booking = session.get('temp_booking')

        if not temp_booking or temp_booking['token'] != data['temp_booking_token']:
            return jsonify({'error': 'Invalid or expired booking session'}), 400

        # Verify token not expired
        expires_at = datetime.fromisoformat(temp_booking['expires_at'])
        if expires_at < datetime.utcnow():
            return jsonify({'error': 'Booking session expired'}), 400

        # Placeholder payment processing
        # In a real app, you would call Stripe or another payment processor here
        print(f"[PAYMENT] Processing payment for user {session['user_id']}: ${temp_booking['total_price']}")

        # Send verification email
        booking_details = {
            'movie_title': temp_booking['movie_details'].get('title', 'Movie'),
            'showtime': temp_booking['movie_details'].get('showtime', 'N/A'),
            'total_price': temp_booking['total_price'],
            'seat_count': len(temp_booking['seats']),
        }

        email_sent = send_booking_confirmation_email(
            temp_booking['email'],
            temp_booking.get('first_name', 'Customer'),
            temp_booking['token'],
            booking_details
        )

        if not email_sent:
            return jsonify({'error': 'Failed to send confirmation email'}), 500

        return jsonify({
            'status': 'payment_processed',
            'message': 'Payment processed successfully. Check your email to confirm your booking.',
            'verification_link_sent': True,
        }), 200

    except Exception as e:
        print(f"[PAYMENT] Error processing payment: {e}")
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/api/bookings/verify/<token>', methods=['GET'])
def verify_booking(token):
    """Verify booking via email token and create booking+tickets in database"""
    from flask import session as flask_session
    import json

    try:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                # Verify token exists and is of correct type
                cursor.execute("""
                    SELECT user_id, expires_at, used
                    FROM PasswordResetToken
                    WHERE token = %s AND type = 'booking_verification'
                """, (token,))
                record = cursor.fetchone()

                if not record:
                    return jsonify({'error': 'Invalid verification token'}), 400

                if record['used']:
                    return jsonify({'error': 'Token already used'}), 400

                if record['expires_at'] < datetime.utcnow():
                    return jsonify({'error': 'Verification token expired'}), 400

                user_id = record['user_id']

                # Retrieve temporary booking data
                booking_data = None

                # Try temporary_bookings table first (if it exists)
                try:
                    cursor.execute("""
                        SELECT booking_data FROM temporary_bookings
                        WHERE token = %s AND user_id = %s
                    """, (token, user_id))
                    temp_record = cursor.fetchone()
                    if temp_record:
                        booking_data = json.loads(temp_record['booking_data'])
                    else:
                        booking_data = None
                except Exception as db_err:
                    # temporary_bookings table doesn't exist or other DB error
                    print(f"[VERIFY] Skipping temporary_bookings lookup: {db_err}")
                    booking_data = None

                # If not found in database, check Flask session
                if not booking_data:
                    temp_booking = flask_session.get('temp_booking')
                    if temp_booking and temp_booking.get('token') == token:
                        booking_data = temp_booking
                    else:
                        conn.close()
                        return jsonify({'error': 'Booking session not found. Please try the checkout process again.'}), 400

                # Get showtime to retrieve room_id for seat lookup
                cursor.execute("""
                    SELECT room_id FROM Showtime WHERE showtime_id = %s
                """, (booking_data['showtime_id'],))
                showtime_record = cursor.fetchone()

                if not showtime_record:
                    conn.close()
                    return jsonify({'error': 'Showtime not found'}), 400

                room_id = showtime_record['room_id']

                # Create booking in database
                booking_id = Booking.create(
                    user_id=user_id,
                    showtime_id=booking_data['showtime_id'],
                    total_price=booking_data['total_price'],
                    card_id=booking_data.get('card_id'),
                    promotion_id=booking_data.get('promotion_id'),
                )

                # Create tickets for this booking
                seats_with_prices = booking_data.get('seats', [])
                if seats_with_prices:
                    resolved_seats = []
                    for seat_data in seats_with_prices:
                        seat_identifier = seat_data.get('seat_id')

                        # Look up actual seat_id from database using seat_number and room_id
                        cursor.execute("""
                            SELECT seat_id FROM Seat
                            WHERE seat_number = %s AND room_id = %s
                        """, (seat_identifier, room_id))
                        seat_record = cursor.fetchone()

                        if seat_record:
                            resolved_seats.append({
                                'seat_id': seat_record['seat_id'],
                                'ticket_type': seat_data.get('ticket_type'),
                                'ticket_price': seat_data.get('ticket_price'),
                            })
                        else:
                            print(f"[VERIFY] Warning: Seat {seat_identifier} not found in room {room_id}")

                    if resolved_seats:
                        Ticket.create_batch(booking_id, resolved_seats)

                # Mark token as used
                cursor.execute("""
                    UPDATE PasswordResetToken SET used = TRUE
                    WHERE token = %s
                """, (token,))

                # Try to delete temporary booking record if table exists
                try:
                    cursor.execute("""
                        DELETE FROM temporary_bookings WHERE token = %s
                    """, (token,))
                except Exception:
                    # Table doesn't exist, skip
                    pass

                conn.commit()

                # Return booking details and redirect to confirmation
                booking = Booking.get_by_id(booking_id)
                booking_id_str = str(booking_id)
                return jsonify({
                    'status': 'verified',
                    'booking_id': booking_id_str,
                    'booking': booking.to_dict() if booking else {},
                    'message': 'Booking confirmed!',
                    'redirect_url': f'/confirmation?booking_id={booking_id_str}',
                }), 200

        finally:
            conn.close()

    except Exception as e:
        print(f"[VERIFY] Error verifying booking: {e}")
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get specific booking with tickets (authenticated)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        booking = Booking.get_by_id(booking_id)

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        if booking.user_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        print(f"[BOOKING] Error getting booking: {e}")
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/api/bookings/my-bookings', methods=['GET'])
def get_my_bookings():
    """Get all bookings for logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        bookings = Booking.get_all_by_user(session['user_id'])
        return jsonify({
            'bookings': [b.to_dict() for b in bookings],
            'count': len(bookings),
        }), 200

    except Exception as e:
        print(f"[BOOKINGS] Error getting user bookings: {e}")
        return jsonify({'error': str(e)}), 500
