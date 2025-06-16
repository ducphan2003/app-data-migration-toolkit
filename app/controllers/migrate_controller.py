from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.repositories.migrate_repository import MigrateRepository
from app.services.migrate_service import MigrateService

def create_migrate_controllers(migrate_repository: MigrateRepository) -> Blueprint:
    migrate_controller = Blueprint('migrate', __name__)
    migrate_service = MigrateService(migrate_repository)
    
    @migrate_controller.route('/migrate-data', methods=['POST'])
    @jwt_required()
    def migrate_data():
        """
        API endpoint để migrate data từ cấu trúc cũ sang cấu trúc mới
        """
        try:
            # Lấy current user
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Bạn cần đăng nhập để thực hiện hành động này'
                }), 401

            # Parse và validate request data
            data = request.get_json()
            
            # Validate input data
            if not data or "id" not in data:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Invalid input data. Missing "id" field.'
                }), 400

            # Tạo migrate process
            result = migrate_service.create_migrate_process(data, current_user_id)

            return jsonify({
                'message': 'Migration process started successfully',
                'data': result
            }), 201

        except ValueError as e:
            return jsonify({
                'error': 'Validation Error',
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @migrate_controller.route('/migrate-data/<int:migrate_process_id>', methods=['GET'])
    @jwt_required()
    def get_migrate_status(migrate_process_id: int):
        """
        API endpoint để frontend polling theo dõi tiến độ migrate
        """
        try:
            result = migrate_service.get_migrate_status(migrate_process_id)

            return jsonify({
                'data': result
            }), 200

        except ValueError as e:
            return jsonify({
                'error': 'Not Found',
                'message': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    return migrate_controller 