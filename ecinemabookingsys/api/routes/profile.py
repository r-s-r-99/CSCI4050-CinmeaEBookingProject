from flask import Blueprint, request, jsonify, session
from db import get_db

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
                SELECT first_name, last_name, email, phone_number 
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

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE User 
                SET first_name = %s, last_name = %s, phone_number = %s 
                WHERE user_id = %s
            """, (first_name, last_name, phone_number, user_id))
        conn.commit()
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
                """, (data.get('houseNumber'), data.get('street'), data.get('apt'), data.get('zip'), user_id))
            else:
                cursor.execute("""
                    INSERT INTO MailingAddress (user_id, house_number, street, apt, zip) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, data.get('houseNumber'), data.get('street'), data.get('apt'), data.get('zip')))

        conn.commit()
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
                SELECT card_id, card_number, expiration_date 
                FROM PaymentCard 
                WHERE user_id = %s
            """, (user_id,))
            cards = cursor.fetchall()

        return jsonify([{
            'cardId':         c['card_id'],
            'cardNumber':     c['card_number'],
            'expirationDate': str(c['expiration_date']),
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
    card_id         = data.get('cardId')
    card_number     = data.get('cardNumber', '').replace(' ', '')
    expiration_date = data.get('expirationDate')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE PaymentCard 
                SET card_number = %s, expiration_date = %s 
                WHERE card_id = %s AND user_id = %s
            """, (card_number, expiration_date, card_id, user_id))
        conn.commit()
        return jsonify({'message': 'Payment card updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()