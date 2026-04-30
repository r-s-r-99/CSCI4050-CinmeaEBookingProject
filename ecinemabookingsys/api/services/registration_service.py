"""
Registration Service - Business logic for user registration.

Handles:
- User registration with validation
- Creating mailing address
- Storing payment cards
- Generating email confirmation tokens
- Email sending
"""

import secrets
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository, PasswordResetTokenRepository
from repositories.mailing_address_repository import MailingAddressRepository
from repositories.payment_card_repository import PaymentCardRepository
from email_utils import send_confirmation_email
from encryption import encrypt


class RegistrationService:
    """Service for user registration operations."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.token_repo = PasswordResetTokenRepository()
        self.address_repo = MailingAddressRepository()
        self.card_repo = PaymentCardRepository()

    def register_user(self, email, password, first_name, last_name, phone_number,
                      promo_subscribed=False, address_data=None, payment_cards=None):
        """
        Register a new user with optional mailing address and payment cards.

        Args:
            email: User email
            password: Plain text password
            first_name: First name
            last_name: Last name
            phone_number: Phone number
            promo_subscribed: Whether user subscribed to promotions
            address_data: Dict with address fields (optional)
            payment_cards: List of payment card dicts (optional, max 3)

        Returns:
            dict: {'success': bool, 'user_id': int or None, 'error': str or None}
        """
        try:
            # Validate required fields
            if not all([email, password, phone_number, first_name, last_name]):
                return {
                    'success': False,
                    'error': 'Email, password, phone, first name and last name are required.'
                }

            # Create user
            user_id = self.user_repo.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                promo_subscribed=promo_subscribed
            )

            # Create mailing address if provided
            if address_data and any(address_data.values()):
                self.address_repo.create_address(
                    user_id=user_id,
                    house_number=address_data.get('house_number'),
                    street=address_data.get('address'),
                    apt=address_data.get('apt_number'),
                    zip_code=address_data.get('zip_code')
                )

            # Create payment cards if provided (max 3)
            if payment_cards:
                for card in payment_cards[:3]:
                    card_number = card.get('cardNumber', '').replace(' ', '')
                    card_name = card.get('cardName', '')
                    expiry = card.get('expiryDate', '')
                    cvv = card.get('cvv', '')

                    # Convert MM/YY to DATE (YYYY-MM-DD)
                    expiration_date = None
                    if expiry and '/' in expiry:
                        month, year = expiry.split('/')
                        expiration_date = f"20{year}-{month}-01"

                    # Save card with encryption
                    self.card_repo.save({
                        'user_id': user_id,
                        'card_name': card_name,
                        'card_number': card_number,
                        'cvv': cvv,
                        'expiration_date': expiration_date
                    })

            # Generate email confirmation token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            self.token_repo.create_token(user_id, token, expires_at, 'email_confirmation')

            # Send confirmation email
            send_confirmation_email(email, first_name, token)

            return {
                'success': True,
                'user_id': user_id
            }

        except ValueError as e:
            # Email already exists or other validation error
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def confirm_email(self, token):
        """
        Confirm email with token.

        Args:
            token: Email confirmation token

        Returns:
            dict: {'success': bool, 'error': str or None}
        """
        try:
            # Find and validate token
            record = self.token_repo.find_by_token(token, 'email_confirmation')
            if not record:
                return {'success': False, 'error': 'invalid_token'}

            if record.get('used'):
                return {'success': False, 'error': 'link_used'}

            if datetime.utcnow() > record['expires_at']:
                return {'success': False, 'error': 'link_expired'}

            # Activate user
            self.user_repo.activate_user(record['user_id'])

            # Mark token as used
            self.token_repo.mark_as_used(token)

            return {'success': True}

        except Exception as e:
            return {'success': False, 'error': 'server_error'}
