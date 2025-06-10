from typing import Optional

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.controllers import (
    create_migrate_controllers,
)

from app.repositories import (
    MigrateRepository,
)

from app.utils import (
    init_db, 
    db_session,
    const
)
from app.utils.redis_client import get_redis_client
from config.config import app_config


def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": ["*"],
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })

    app.config['JWT_SECRET_KEY'] = app_config.JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_IDENTITY_CLAIM'] = 'id'

    JWTManager(app)

    with app.app_context():
        init_db(app)

    @app.route('/<path:path>', methods=['OPTIONS'])
    def options(path):
        response = jsonify({'status': 'OK'})
        response.status_code = 200
        return response
    
    redis_client = get_redis_client()


    with db_session() as session:
        migrate_repo = MigrateRepository(session, redis_client)

        #Initialize services
        app.register_blueprint(
            create_migrate_controllers(migrate_repo), 
            url_prefix=const.URL_PREFIX
        )

    return app
