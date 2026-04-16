from flask import Blueprint, request, jsonify, session
from services.booking_service import BookingService
from services.email_service import EmailService
import secrets
from datetime import datetime, timedelta

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
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        if 'temp_booking_token' not in data or 'card_data' not in data:
            return jsonify({'error': 'Missing booking token or card data'}), 400

        token = data['temp_booking_token']
        card_data = data['card_data']

        # Validate card data
        booking_service.process_payment(token, card_data)

        # Get booking data from session (for email details)
        temp_booking = session.get('temp_booking')
        if not temp_booking:
            return jsonify({'error': 'Booking session not found'}), 400

        # Send verification email
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


@booking_bp.route('/api/bookings/my-bookings', methods=['GET'])
def get_my_bookings():
    """
    Get all bookings for logged-in user.

    Route handler: Thin request/response adapter
    Business logic: Handled by BookingService
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Use service to get bookings
        bookings = booking_service.get_user_bookings(session['user_id'])

        return jsonify({
            'bookings': [b.to_dict() for b in bookings],
            'count': len(bookings),
        }), 200

    except Exception as e:
        print(f"[BOOKINGS] Error getting user bookings: {e}")
        return jsonify({'error': str(e)}), 500

