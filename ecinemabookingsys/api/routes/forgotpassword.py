from flask import Blueprint, request, jsonify
from services.password_reset_service import PasswordResetService

forgotpassword_bp = Blueprint('forgotpassword', __name__)
password_reset_service = PasswordResetService()


@forgotpassword_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """Initiate password reset flow."""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email is required.'}), 400

        result = password_reset_service.initiate_password_reset(email)

        if result['success']:
            # Return same message regardless of whether email exists (security best practice)
            return jsonify({'message': 'If that email exists, a reset link has been sent.'}), 200
        else:
            return jsonify({'error': result.get('error', 'An error occurred')}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@forgotpassword_bp.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Reset password using a valid token."""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')

        result = password_reset_service.validate_and_reset_password(token, new_password)

        if result['success']:
            return jsonify({'message': 'Password reset successful.'}), 200
        else:
            return jsonify({'error': result['error']}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
