from flask import Blueprint, request, jsonify, session
from db import get_db
import bcrypt
from email_utils import send_profile_update_email
from cryptography.fernet import Fernet
import os

fernet = Fernet(os.environ.get('ENCRYPTION_KEY').encode())

def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()

def get_user_email_and_name(cursor, user_id):
    cursor.execute("SELECT email, first_name FROM User WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

profile_bp = Blueprint('profile', __name__)

def get_user_id():
    """Helper to get user_id from session or return None."""
    return session.get('user_id')

@profile_bp.route('/api/retrieve-edit-profile', methods=['GET'])
def get_profile_main():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT first_name, last_name, email, phone_number, promo_subscribed
                FROM User 
                WHERE user_id = %s
            """, (user_id,))
            profile = cursor.fetchone()

        if not profile:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'firstName':   profile['first_name'],
            'lastName':    profile['last_name'],
            'email':       profile['email'],
            'phoneNumber': profile['phone_number'],
            'promotions':  profile['promo_subscribed'],
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/update-profile', methods=['POST'])
def update_profile_main():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    first_name   = data.get('firstName')
    last_name    = data.get('lastName')
    phone_number = data.get('phoneNumber')
    promo_subscribed = data.get('promotions')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE User 
                SET first_name = %s, last_name = %s, phone_number = %s, promo_subscribed = %s
                WHERE user_id = %s
            """, (first_name, last_name, phone_number, promo_subscribed, user_id))
            conn.commit()
        
            user = get_user_email_and_name(cursor, user_id)
            send_profile_update_email(user['email'], user['first_name'], 'personal information')
            
        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/retrieve-mailing-address', methods=['GET'])
def get_profile_address():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT house_number, street, apt, zip 
                FROM MailingAddress 
                WHERE user_id = %s
            """, (user_id,))
            address = cursor.fetchone()

        if not address:
            return jsonify({}), 200  # no address yet, not an error

        return jsonify({
            'houseNumber': address['house_number'],
            'street':      address['street'],
            'apt':         address['apt'],
            'zip':         address['zip'],
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/update-mailing-address', methods=['POST'])
def update_profile_address():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Upsert — insert if no address exists, otherwise update
            cursor.execute("SELECT user_id FROM MailingAddress WHERE user_id = %s", (user_id,))
            exists = cursor.fetchone()

            if exists:
                cursor.execute("""
                    UPDATE MailingAddress 
                    SET house_number = %s, street = %s, apt = %s, zip = %s 
                    WHERE user_id = %s
                """, (data.get('houseNumber'), data.get('street'), data.get('apt'), data.get('zipCode'), user_id))
            else:
                cursor.execute("""
                    INSERT INTO MailingAddress (user_id, house_number, street, apt, zip) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, data.get('houseNumber'), data.get('street'), data.get('apt'), data.get('zipCode')))

            conn.commit()
            
            user = get_user_email_and_name(cursor, user_id)
            send_profile_update_email(user['email'], user['first_name'], 'mailing address')
            
        return jsonify({'message': 'Address updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/retrieve-payment-cards', methods=['GET'])
def get_profile_payment():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT card_id, card_name, card_number, cvv, expiration_date
                FROM PaymentCard
                WHERE user_id = %s
            """, (user_id,))
            cards = cursor.fetchall()

        def safe_decrypt(value):
            """Return decrypted string, or '' if value is None or not Fernet-encoded."""
            if not value:
                return ''
            try:
                return decrypt(value)
            except Exception:
                return ''

        return jsonify([{
            'cardId':         c['card_id'],
            'cardName':       c['card_name'] or '',
            'cardNumber':     safe_decrypt(c['card_number']),
            'cvv':            safe_decrypt(c['cvv']),
            'expirationDate': str(c['expiration_date']) if c['expiration_date'] else '',
        } for c in cards]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/update-payment-cards', methods=['POST'])
def update_profile_payment():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    card_id         = data.get('cardId')   # None for brand-new cards
    card_name       = data.get('cardName', '')
    card_number     = data.get('cardNumber', '').replace(' ', '')
    expiration_date = data.get('expirationDate')
    cvv             = data.get('cvv', '')

    # Convert MM/YY → YYYY-MM-DD for MySQL DATE column
    if expiration_date and '/' in expiration_date:
        month, year = expiration_date.split('/')
        expiration_date = f"20{year.strip()}-{month.strip()}-01"

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            if card_id is None:
                # Brand-new card — check user doesn't already have 3
                cursor.execute("SELECT COUNT(*) AS cnt FROM PaymentCard WHERE user_id = %s", (user_id,))
                row = cursor.fetchone()
                if row['cnt'] >= 3:
                    return jsonify({'error': 'Maximum of 3 cards allowed.'}), 400
                cursor.execute("""
                    INSERT INTO PaymentCard (user_id, card_name, card_number, cvv, expiration_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, card_name, encrypt(card_number), encrypt(cvv), expiration_date))
            else:
                # Existing card — update it
                cursor.execute("""
                    UPDATE PaymentCard 
                    SET card_name = %s, card_number = %s, cvv = %s, expiration_date = %s 
                    WHERE card_id = %s AND user_id = %s
                """, (card_name, encrypt(card_number), encrypt(cvv), expiration_date, card_id, user_id))
        
        conn.commit()
        return jsonify({'message': 'Payment card saved successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/delete-payment-card', methods=['POST'])
def delete_payment_card():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    card_id = data.get('cardId')
    if not card_id:
        return jsonify({'error': 'cardId required'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'DELETE FROM PaymentCard WHERE card_id = %s AND user_id = %s',
                (card_id, user_id)
            )
        conn.commit()
        return jsonify({'message': 'Card deleted'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/favorites', methods=['POST'])
def toggle_favorite():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    movie_id = data.get('movieId')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT favorite_id FROM Favorite
                WHERE user_id = %s AND movie_id = %s
            """, (user_id, movie_id))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    DELETE FROM Favorite WHERE user_id = %s AND movie_id = %s
                """, (user_id, movie_id))
                action = 'removed'
            else:
                cursor.execute("""
                    INSERT INTO Favorite (user_id, movie_id) VALUES (%s, %s)
                """, (user_id, movie_id))
                action = 'added'

            conn.commit()
            return jsonify({'action': action}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@profile_bp.route('/api/retrieve-favorites', methods=['GET'])
def retrieve_favorites():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.movie_id, m.title, m.poster_url, m.genre, m.rating, m.description, m.trailer_url, m.status, f.date_added
                FROM Favorite f
                JOIN Movie m ON f.movie_id = m.movie_id
                WHERE f.user_id = %s
                ORDER BY f.date_added DESC
            """, (user_id,))
            favorites = cursor.fetchall()
            return jsonify({'favorites': favorites}), 200
    except Exception as e:
        print(f"Error: {e}")  # check your terminal for the actual message
        return jsonify({'error': str(e)}), 500
    
@profile_bp.route('/api/verify-password', methods=['POST'])
def verify_password():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    current_password = data.get('password')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password FROM User WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()

        if not user or not bcrypt.checkpw(current_password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'valid': False}), 200

        return jsonify({'valid': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/api/change-password', methods=['POST'])
def change_password():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    new_password = data.get('password')

    conn = get_db()
    try:
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with conn.cursor() as cursor:
            cursor.execute("UPDATE User SET password = %s WHERE user_id = %s", (hashed, user_id))
            conn.commit()
            
            user = get_user_email_and_name(cursor, user_id)
            send_profile_update_email(user['email'], user['first_name'], 'password')
            
        return jsonify({'message': 'Password changed successfully.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


        