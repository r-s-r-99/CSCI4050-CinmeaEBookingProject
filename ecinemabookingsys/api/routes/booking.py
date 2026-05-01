from flask import Blueprint, request, jsonify, session
from services.booking_service import BookingService
from services.email_service import EmailService
import secrets
from datetime import datetime, timedelta
import pymysql

booking_bp = Blueprint('booking', __name__)

# Initialize services
booking_service = BookingService()
email_service = EmailService()




@booking_bp.route('/api/bookings/create-temporary', methods=['POST'])
def create_temporary_booking():
    """
    Create temporary booking session before payment.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['showtime_id', 'seats', 'email', 'total_price']):
            return jsonify({'error': 'Missing required fields (showtime_id, seats, email, total_price)'}), 400

        # Store booking data in session for later retrieval during payment/verification
        session['temp_booking'] = {
            'user_id': session['user_id'],
            'showtime_id': data['showtime_id'],
            'seats': data['seats'],
            'email': data['email'],
            'total_price': data['total_price'],
        }
        session.modified = True

        # Use service to create temporary booking
        result = booking_service.create_temporary_booking(
            user_id=session['user_id'],
            showtime_id=data['showtime_id'],
            seats=data['seats'],
            email=data['email'],
            total_price=data['total_price']
        )

        return jsonify({
            'status': 'success',
            'temp_booking_token': result['temp_booking_token'],
            'expires_at': result['expires_at'],
        }), 200

    except Exception as e:
        print(f"[BOOKING] Error creating temporary booking: {e}")
        return jsonify({'error': str(e)}), 500




@booking_bp.route('/api/bookings/process-payment', methods=['POST'])
def process_payment():
    """
    Process placeholder payment and send verification email.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService and EmailService

    Accepts either:
    - card_data: New card information
    - card_id: ID of a saved card from user's account
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        if 'temp_booking_token' not in data:
            return jsonify({'error': 'Missing booking token'}), 400

        token = data['temp_booking_token']
        card_data = data.get('card_data')
        card_id = data.get('card_id')

        # Validate that either card_data or card_id is provided
        if not card_data and not card_id:
            return jsonify({'error': 'Missing card data or card ID'}), 400

        # Validate card data
        booking_service.process_payment(token, card_data, card_id, session['user_id'])

        # Get booking data from session (for email details)
        temp_booking = session.get('temp_booking')
        if not temp_booking:
            return jsonify({'error': 'Booking session not found'}), 400

        # Store card_id in session if using a saved card
        if card_id:
            temp_booking['card_id'] = card_id
            session.modified = True

        # Fetch movie and showtime details to include in email
        try:
            from db import get_db
            conn = get_db()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Fetch showtime and movie details
                cursor.execute("""
                    SELECT s.show_date, s.show_time, m.title, sr.room_number
                    FROM Showtime s
                    LEFT JOIN Movie m ON s.movie_id = m.movie_id
                    LEFT JOIN Showroom sr ON s.room_id = sr.room_id
                    WHERE s.showtime_id = %s
                """, (temp_booking.get('showtime_id'),))
                result = cursor.fetchone()
            

            if result:
                show_date = result['show_date']
                show_time = result['show_time']
                movie_title = result['title'] or 'Movie'
                room_number = result['room_number'] or 'N/A'

                # Format date
                from datetime import datetime
                formatted_date = datetime.strptime(str(show_date), '%Y-%m-%d').strftime('%m/%d/%Y')

                # Add movie details to temp_booking for email
                temp_booking['movie_details'] = {
                    'title': movie_title,
                    'showtime': f"{formatted_date} at {show_time} (Room {room_number})"
                }
                print(f"[BOOKING] Added movie_details: {temp_booking['movie_details']}")
            else:
                print(f"[BOOKING] No showtime found for showtime_id: {temp_booking.get('showtime_id')}")
        except Exception as e:
            print(f"[BOOKING] Error fetching movie details for email: {e}")
            import traceback
            traceback.print_exc()
            # Continue anyway with fallback values

        # Send verification email
        print(f"[BOOKING] Sending email with booking_data: {temp_booking}")
        email_service.send_booking_confirmation(
            to_email=temp_booking.get('email'),
            token=token,
            booking_data=temp_booking
        )

        return jsonify({
            'status': 'payment_processed',
            'message': 'Payment processed successfully. Check your email to confirm your booking.',
            'verification_link_sent': True,
        }), 200

    except ValueError as e:
        # Payment validation failed
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[PAYMENT] Error processing payment: {e}")
        return jsonify({'error': str(e)}), 500




@booking_bp.route('/api/bookings/verify/<token>', methods=['GET'])
def verify_booking(token):
    """
    Verify booking via email token and create booking+tickets in database.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService
    """
    # Note: This endpoint can be called without authentication (email links)
    # But we still need the user_id from the token record

    try:
        # Get temp booking from session - this has the booking data
        temp_booking = session.get('temp_booking')

        # Use service to verify and finalize the booking
        booking = booking_service.verify_booking(
            token=token,
            booking_data=temp_booking,
            user_id=session.get('user_id')
        )

        if not booking:
            return jsonify({'error': 'Could not create booking'}), 500

        booking_id_str = str(booking.booking_id)
        return jsonify({
            'status': 'verified',
            'booking_id': booking_id_str,
            'booking': booking.to_dict(),
            'message': 'Booking confirmed!',
            'redirect_url': f'/confirmation?booking_id={booking_id_str}',
        }), 200

    except ValueError as e:
        # Validation error
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[VERIFY] Error verifying booking: {e}")
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/api/bookings/my-bookings', methods=['GET'])
def get_my_bookings():
    """
    Get all bookings for authenticated user.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        bookings = booking_service.get_user_bookings(session['user_id'])

        return jsonify({
            'status': 'success',
            'bookings': [b.to_dict() for b in bookings],
        }), 200

    except Exception as e:
        print(f"[BOOKINGS] Error fetching user bookings: {e}")
        return jsonify({'error': str(e)}), 500



@booking_bp.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    Get specific booking with tickets (authenticated).

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Use service to get booking (enforces authorization)
        booking = booking_service.get_booking(booking_id, session['user_id'])

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        print(f"[BOOKING] Error getting booking: {e}")
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/api/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Delete a booking (cancel) - authenticated user only.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService

    Authorization: User can only delete their own bookings
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Use service to cancel booking (enforces authorization)
        success = booking_service.cancel_booking_with_auth(booking_id, session['user_id'])

        if not success:
            return jsonify({'error': 'Booking not found or unauthorized'}), 404

        return jsonify({
            'status': 'deleted',
            'message': 'Booking cancelled successfully',
            'booking_id': booking_id,
        }), 200

    except ValueError as e:
        # Validation error (e.g., booking cannot be cancelled)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[DELETE] Error deleting booking: {e}")
        return jsonify({'error': str(e)}), 500


