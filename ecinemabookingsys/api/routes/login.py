from flask import Blueprint, request, jsonify, session
from db import get_db
import bcrypt

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def validate_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"[LOGIN] Attempting login for: {email}")

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, email, password, account_status, role 
                FROM User 
                WHERE email = %s
            """, (email,))
            user = cursor.fetchone()

        print(f"[LOGIN] User found: {user is not None}")
        print(f"[LOGIN] Account status: {user['account_status'] if user else 'N/A'}")

        if not user:
            return jsonify({ 'success': False, 'error': 'Invalid credentials.' }), 401

        if user['account_status'] == 'Inactive':
            return jsonify({ 'success': False, 'error': 'Please verify your email before logging in.' }), 403

        if user['account_status'] == 'Suspended':
            return jsonify({ 'success': False, 'error': 'Your account has been suspended.' }), 403

        password_match = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
        print(f"[LOGIN] Password match: {password_match}")

        if not password_match:
            return jsonify({ 'success': False, 'error': 'Invalid credentials.' }), 401

        session['user_id'] = user['user_id']
        session['role'] = user['role']
        print(f"[LOGIN] Session set: {dict(session)}")

        return jsonify({ 'success': True, 'role': user['role'] }), 200

    except Exception as e:
        print(f"[LOGIN] Exception: {e}")
        return jsonify({ 'success': False, 'error': str(e) }), 500
    finally:
        conn.close()


@login_bp.route('/api/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({}), 401
    return jsonify({
        'user_id': user_id,
        'role': session.get('role')
    }), 200


@login_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True}), 200