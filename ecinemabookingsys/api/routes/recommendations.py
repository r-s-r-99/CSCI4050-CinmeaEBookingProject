from flask import Blueprint, jsonify, session
import traceback
from services.recommendation_service import RecommendationService

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get movie recommendations for the user including booked and favorite movies.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        user_id = session['user_id']
        recommendation_service = RecommendationService()
        recommendations = recommendation_service.get_recommendations(user_id)

        return jsonify({
            'status': 'success',
            'data': recommendations
        }), 200

    except Exception as e:
        print(f"[RECOMMENDATIONS] Error getting recommendations: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
