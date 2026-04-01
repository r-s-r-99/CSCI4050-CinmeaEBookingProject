from flask import Blueprint, request, jsonify
from db import get_db
import bcrypt
import secrets
from datetime import datetime, timedelta
from email_utils import send_confirmation_email

register_bp = Blueprint('register', __name__)

@register_bp.route('/api/register', methods=['POST'])
def registration():
    data = request.get_json()

    # Required fields
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone_number = data.get('phoneNumber', None)

    # Optional fields
    promo_subscribed = data.get('promotions', False)

    # Optional mailing address
    address = data.get('address', None)
    zip_code = data.get('zipCode', None)
    house_number = data.get('houseNumber', None)
    apt_number = data.get('aptNumber', None)
    city = data.get('city', None)
    state = data.get('state', None)

    # Optional payment cards (list)
    payment_cards = data.get('paymentCards', [])

    # Basic validation
    if not all([email, password, phone_number, first_name, last_name]):
        return jsonify({ 'error': 'Email, password, phone, first name and last name are required.' }), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT user_id FROM User WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({ 'error': 'Email already registered.' }), 409

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insert user
            cursor.execute("""
                INSERT INTO User (email, password, first_name, last_name, phone_number, promo_subscribed, account_status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Inactive')
            """, (email, hashed_password, first_name, last_name, phone_number, promo_subscribed))

            user_id = cursor.lastrowid

            # Insert mailing address if any address field is provided
            if any([address, zip_code, house_number, apt_number, city, state]):
                cursor.execute("""
                    INSERT INTO MailingAddress (user_id, house_number, street, apt, zip)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, house_number, address, apt_number, zip_code))

            # Insert payment cards (max 3)
            for card in payment_cards[:3]:
                card_number = card.get('cardNumber', '').replace(' ', '')  # strip spaces
                card_name = card.get('cardName', '')
                expiry = card.get('expiryDate', '')                        # MM/YY
                cvv = card.get('cvv', '')
                # Convert MM/YY to a DATE (YYYY-MM-DD) for MySQL
                if expiry and '/' in expiry:
                    month, year = expiry.split('/')
                    expiration_date = f"20{year}-{month}-01"
                else:
                    expiration_date = None

                cursor.execute("""
                    INSERT INTO PaymentCard (user_id, card_name, card_number, expiration_date, cvv)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, card_name, card_number, expiration_date, cvv))

            # Generate confirmation token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)

            cursor.execute("""
                INSERT INTO PasswordResetToken (user_id, token, expires_at, type)
                VALUES (%s, %s, %s, 'email_confirmation')
            """, (user_id, token, expires_at))

            conn.commit()

            # Send confirmation email
            send_confirmation_email(email, first_name, token)

            return jsonify({ 'message': 'Registration successful. Please check your email to activate your account.' }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({ 'error': str(e) }), 500
    finally:
        conn.close()
        
@register_bp.route('/api/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Find the token
            cursor.execute("""
                SELECT user_id, expires_at, used 
                FROM PasswordResetToken 
                WHERE token = %s AND type = 'email_confirmation'
            """, (token,))
            record = cursor.fetchone()

            if not record:
                return jsonify({ 'error': 'Invalid confirmation link.' }), 404

            if record['used']:
                return jsonify({ 'error': 'Link already used.' }), 400

            if datetime.utcnow() > record['expires_at']:
                return jsonify({ 'error': 'Confirmation link has expired.' }), 400

            # Activate the account
            cursor.execute("""
                UPDATE User SET account_status = 'Active' 
                WHERE user_id = %s
            """, (record['user_id'],))

            # Mark token as used
            cursor.execute("""
                UPDATE PasswordResetToken SET used = TRUE 
                WHERE token = %s
            """, (token,))

            conn.commit()

            # Redirect to login page
            return jsonify({ 'message': 'Account activated! You can now log in.' }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({ 'error': str(e) }), 500
    finally:
        conn.close()