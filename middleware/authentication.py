from flask_jwt_extended import verify_jwt_in_request
from functools import wraps
from flask import jsonify, g as _global

from app.models.user import UserClaims


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            claim: UserClaims = verify_jwt_in_request()
            if claim == None:
                return jsonify({"msg": "Error"}), 401
            _global.user_claims = claim
        except Exception as e:
            return jsonify({"msg": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function