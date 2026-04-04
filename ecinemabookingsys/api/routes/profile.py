from flask import Blueprint, request, jsonify, session
from models.users import User
from models.payment_card import PaymentCard
from models.favorite import Favorite
from models.mailing_address import MailingAddress
from email_utils import send_profile_update_email

profile_bp = Blueprint('profile', __name__)

def get_user_id():
    return session.get('user_id')

@profile_bp.route('/api/retrieve-edit-profile', methods=['GET'])
def get_profile_main():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200


@profile_bp.route('/api/update-profile', methods=['POST'])
def update_profile_main():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        user.update_profile(
            data.get('firstName'),
            data.get('lastName'),
            data.get('phoneNumber'),
            data.get('promotions')
        )
        send_profile_update_email(user.email, user.first_name, 'personal information')
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/retrieve-mailing-address', methods=['GET'])
def get_profile_address():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    address = MailingAddress.get_by_user(user_id)
    if not address:
        return jsonify({}), 200

    return jsonify(address.to_dict()), 200


@profile_bp.route('/api/update-mailing-address', methods=['POST'])
def update_profile_address():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    try:
        address = MailingAddress(
            user_id=user_id,
            house_number=data.get('houseNumber'),
            street=data.get('street'),
            apt=data.get('apt'),
            zip=data.get('zipCode')
        )
        address.save()

        user = User.find_by_id(user_id)
        send_profile_update_email(user.email, user.first_name, 'mailing address')
        return jsonify({'message': 'Address updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/retrieve-payment-cards', methods=['GET'])
def get_profile_payment():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        cards = PaymentCard.get_by_user(user_id)
        return jsonify([card.to_dict() for card in cards]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/update-payment-cards', methods=['POST'])
def update_profile_payment():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    card_id         = data.get('cardId')
    card_name       = data.get('cardName', '')
    card_number     = data.get('cardNumber', '').replace(' ', '')
    expiration_date = data.get('expirationDate')
    cvv             = data.get('cvv', '')

    if expiration_date and '/' in expiration_date:
        month, year = expiration_date.split('/')
        expiration_date = f"20{year.strip()}-{month.strip()}-01"

    try:
        if card_id is None:
            if PaymentCard.count_by_user(user_id) >= 3:
                return jsonify({'error': 'Maximum of 3 cards allowed.'}), 400
            PaymentCard.create(user_id, card_name, card_number, cvv, expiration_date)
        else:
            card = PaymentCard(
                card_id=card_id,
                user_id=user_id,
                card_name=card_name,
                card_number=card_number,
                cvv=cvv,
                expiration_date=expiration_date
            )
            card.update(card_name, card_number, cvv, expiration_date)

        user = User.find_by_id(user_id)
        send_profile_update_email(user.email, user.first_name, 'payment cards')
        return jsonify({'message': 'Payment card saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/delete-payment-card', methods=['POST'])
def delete_payment_card():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    card_id = data.get('cardId')
    if not card_id:
        return jsonify({'error': 'cardId required'}), 400

    try:
        card = PaymentCard(
            card_id=card_id,
            user_id=user_id,
            card_name=None,
            card_number=None,
            cvv=None,
            expiration_date=None
        )
        card.delete()
        return jsonify({'message': 'Card deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/favorites', methods=['POST'])
def toggle_favorite():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    movie_id = data.get('movieId')

    try:
        action = Favorite.toggle(user_id, movie_id)
        return jsonify({'action': action}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/retrieve-favorites', methods=['GET'])
def retrieve_favorites():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        favorites = Favorite.get_by_user(user_id)
        return jsonify({'favorites': favorites}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/verify-password', methods=['POST'])
def verify_password():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        valid = user.check_password(data.get('password'))
        return jsonify({'valid': valid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/api/change-password', methods=['POST'])
def change_password():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        user.update_password(data.get('password'))
        send_profile_update_email(user.email, user.first_name, 'password')
        return jsonify({'message': 'Password changed successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500