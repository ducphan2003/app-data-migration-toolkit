from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.repositories.migrate_repository import MigrateRepository
from app.services.parallel_migrate_service import ParallelMigrateService
from app.schemas.migrate_schema import QuizMergeRequest

def create_parallel_migrate_controllers(migrate_repository: MigrateRepository) -> Blueprint:
    parallel_migrate_controller = Blueprint('parallel_migrate', __name__)
    parallel_migrate_service = ParallelMigrateService(migrate_repository)
    
    @parallel_migrate_controller.route('/migrate-quiz-parallel', methods=['POST'])
    @jwt_required()
    def migrate_quiz_parallel():
        """
        API endpoint để tách quiz thành 3 parts và xử lý song song
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

            if not data.get("parts") or len(data.get("parts", [])) != 3:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Quiz phải có đúng 3 parts để xử lý song song.'
                }), 400

            # Tách quiz thành các part requests
            part_requests = parallel_migrate_service.split_quiz_into_parts(data, current_user_id)
            
            # Xử lý các parts song song
            part_migrate_ids = parallel_migrate_service.process_parts_parallel(part_requests)

            return jsonify({
                'message': 'Quiz đã được tách thành 3 parts và đang xử lý song song',
                'data': {
                    'quiz_id': str(data["id"]),
                    'total_parts': 3,
                    'part_migrate_ids': part_migrate_ids,
                    'instructions': {
                        'next_step': 'Poll các part_migrate_ids để theo dõi tiến độ',
                        'poll_endpoints': {
                            'part_status': '/api/migrate-part-status/<part_migrate_id>',
                            'merge_quiz': '/api/merge-quiz-parts'
                        }
                    }
                }
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

    @parallel_migrate_controller.route('/migrate-part-status/<part_migrate_id>', methods=['GET'])
    @jwt_required()
    def get_part_migrate_status(part_migrate_id: str):
        """
        API endpoint để lấy trạng thái migrate của một part
        """
        try:
            result = parallel_migrate_service.get_part_migrate_status(part_migrate_id)

            return jsonify({
                'data': result.dict()
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

    @parallel_migrate_controller.route('/check-all-parts-status', methods=['POST'])
    @jwt_required()
    def check_all_parts_status():
        """
        API endpoint để kiểm tra trạng thái của tất cả parts
        """
        try:
            data = request.get_json()
            part_migrate_ids = data.get('part_migrate_ids', {})
            
            if not part_migrate_ids:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Missing part_migrate_ids'
                }), 400

            results = {}
            all_completed = True
            any_failed = False
            
            for part_name, part_migrate_id in part_migrate_ids.items():
                try:
                    part_status = parallel_migrate_service.get_part_migrate_status(part_migrate_id)
                    results[part_name] = part_status.dict()
                    
                    if part_status.status != 'completed':
                        all_completed = False
                    if part_status.status == 'failed':
                        any_failed = True
                        
                except Exception as e:
                    results[part_name] = {
                        'status': 'error',
                        'error_message': str(e)
                    }
                    all_completed = False
                    any_failed = True

            return jsonify({
                'data': {
                    'parts_status': results,
                    'summary': {
                        'all_completed': all_completed,
                        'any_failed': any_failed,
                        'ready_for_merge': all_completed and not any_failed
                    }
                }
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @parallel_migrate_controller.route('/merge-quiz-parts', methods=['POST'])
    @jwt_required()
    def merge_quiz_parts():
        """
        API endpoint để merge các parts đã migrate thành quiz hoàn chỉnh
        """
        try:
            # Lấy current user
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Bạn cần đăng nhập để thực hiện hành động này'
                }), 401

            # Parse request data
            data = request.get_json()
            
            # Validate input data
            required_fields = ['quiz_id', 'part_migrate_ids']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'error': 'Validation Error',
                        'message': f'Missing required field: {field}'
                    }), 400

            # Validate part_migrate_ids format
            part_migrate_ids = data['part_migrate_ids']
            if not isinstance(part_migrate_ids, dict) or len(part_migrate_ids) != 3:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'part_migrate_ids phải là dict với 3 parts'
                }), 400

            # Extract IDs list from dict
            part_ids_list = list(part_migrate_ids.values())

            # Tạo merge request
            merge_request = QuizMergeRequest(
                quiz_id=data['quiz_id'],
                part_migrate_ids=part_ids_list,
                user_id=current_user_id
            )

            # Bắt đầu merge process
            quiz_merge_id = parallel_migrate_service.merge_parts_to_quiz(merge_request)

            return jsonify({
                'message': 'Bắt đầu merge các parts thành quiz hoàn chỉnh',
                'data': {
                    'quiz_merge_id': quiz_merge_id,
                    'quiz_id': data['quiz_id'],
                    'status': 'processing',
                    'instructions': {
                        'next_step': 'Poll quiz_merge_id để theo dõi tiến độ merge',
                        'poll_endpoint': f'/api/merge-quiz-status/{quiz_merge_id}'
                    }
                }
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

    @parallel_migrate_controller.route('/merge-quiz-status/<quiz_merge_id>', methods=['GET'])
    @jwt_required()
    def get_quiz_merge_status(quiz_merge_id: str):
        """
        API endpoint để lấy trạng thái merge quiz
        """
        try:
            result = parallel_migrate_service.get_quiz_merge_status(quiz_merge_id)

            return jsonify({
                'data': result.dict()
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

    return parallel_migrate_controller 