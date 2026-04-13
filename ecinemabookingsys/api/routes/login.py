from flask import Blueprint, request, jsonify, session
from models.user import User
from db import get_db
import bcrypt

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def validate_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"[LOGIN] Attempting login for: {email}")

    user, error = User.login(email, password)
    if error:
        status = 403 if 'verify' in error or 'suspended' in error.lower() else 401
        return jsonify({'success': False, 'error': error}), status

    session['user_id'] = user.user_id
    session['role'] = user.role
    print(f"[LOGIN] Session set: user_id={user.user_id}, role={user.role}")

    return jsonify({'success': True, 'role': user.role}), 200

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