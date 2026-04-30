from flask import Blueprint, request, jsonify, redirect
import os
from services.registration_service import RegistrationService

register_bp = Blueprint('register', __name__)
registration_service = RegistrationService()


@register_bp.route('/api/register', methods=['POST'])
def registration():
    """Register a new user with optional address and payment cards."""
    try:
        data = request.get_json()

        # Extract required fields
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        phone_number = data.get('phoneNumber')
        promo_subscribed = data.get('promotions', False)

        # Extract optional address fields
        address_data = {
            'address': data.get('address'),
            'zip_code': data.get('zipCode'),
            'house_number': data.get('houseNumber'),
            'apt_number': data.get('aptNumber'),
            'city': data.get('city'),
            'state': data.get('state'),
        }

        # Extract optional payment cards
        payment_cards = data.get('paymentCards', [])

        # Register user
        result = registration_service.register_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            promo_subscribed=promo_subscribed,
            address_data=address_data,
            payment_cards=payment_cards
        )

        if result['success']:
            return jsonify({
                'message': 'Registration successful. Please check your email to activate your account.'
            }), 201
        else:
            # Check if it's a duplicate email error
            if 'already registered' in result['error']:
                return jsonify({'error': result['error']}), 409
            return jsonify({'error': result['error']}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@register_bp.route('/api/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    """Confirm user email with token."""
    try:
        result = registration_service.confirm_email(token)

        if result['success']:
            return redirect(f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/login?confirmed=true")
        else:
            error_code = result['error']
            return redirect(f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/login?error={error_code}")

    except Exception as e:
        return redirect(f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/login?error=server_error")
