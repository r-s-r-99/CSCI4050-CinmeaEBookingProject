from flask import Blueprint, request, jsonify
from db import get_db
import secrets
from datetime import datetime, timedelta
from email_utils import send_reset_email
import bcrypt

forgotpassword_bp = Blueprint('forgotpassword', __name__)

@forgotpassword_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, first_name FROM User WHERE email = %s", (email,))
            user = cursor.fetchone()

        if not user:
            # Return success anyway to avoid exposing which emails are registered
            return jsonify({'message': 'If that email exists, a reset link has been sent.'}), 200

        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PasswordResetToken (user_id, token, expires_at, type)
                VALUES (%s, %s, %s, 'password_reset')
            """, (user['user_id'], token, expires_at))
            conn.commit()

        send_reset_email(email, user['first_name'], token)

        return jsonify({'message': 'If that email exists, a reset link has been sent.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
        
@forgotpassword_bp.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required.'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Validate token
            cursor.execute("""
                SELECT user_id, expires_at 
                FROM PasswordResetToken 
                WHERE token = %s
            """, (token,))
            record = cursor.fetchone()

        if not record:
            return jsonify({'error': 'Invalid or expired token.'}), 400

        if datetime.utcnow() > record['expires_at']:
            return jsonify({'error': 'Token has expired.'}), 400

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE User SET password = %s WHERE user_id = %s
            """, (hashed_password, record['user_id']))

            # Delete token so it can't be reused
            cursor.execute("""
                DELETE FROM PasswordResetToken WHERE token = %s
            """, (token,))

            conn.commit()

        return jsonify({'message': 'Password reset successful.'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()