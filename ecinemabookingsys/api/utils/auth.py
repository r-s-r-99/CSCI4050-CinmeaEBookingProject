"""
Admin Authorization Utility - Shared across routes.

Provides helper functions for checking admin authorization.
"""

from flask import session, jsonify
from repositories.user_repository import UserRepository


def get_user_role_from_session():
    """Get user role from session. Returns role string or None if not authenticated."""
    if 'user_id' not in session:
        return None

    user_repo = UserRepository()
    user = user_repo.find_by_id(session['user_id'])
    return user.get('role') if user else None


def require_admin():
    """
    Check if user is admin. Returns (is_admin, error_response).

    Returns:
        tuple: (is_admin: bool, error_response: tuple or None)
    """
    if 'user_id' not in session:
        return False, (jsonify({'error': 'Unauthorized'}), 401)

    role = get_user_role_from_session()
    if role != 'admin':
        return False, (jsonify({'error': 'Only admins can access this resource'}), 403)

    return True, None
