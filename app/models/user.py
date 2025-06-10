from datetime import timedelta
from flask_jwt_extended import create_access_token, decode_token


class UserClaims:
    def __init__(
        self, 
        id, 
        role, 
        exp
    ):
        self.id = id
        self.role = role
        self.exp = exp

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "exp": self.exp
        }
