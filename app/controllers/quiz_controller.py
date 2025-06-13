from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.repositories.quiz_repository import QuizRepository
from app.services.quiz_service import QuizService
from app.schemas.quiz_schema import CreateQuizSchema

def create_quiz_controllers(quiz_repository: QuizRepository) -> Blueprint:
    quiz_controller = Blueprint('quiz', __name__)
    quiz_service = QuizService(quiz_repository)
    
    @quiz_controller.route('/quizzes', methods=['POST'])
    @jwt_required()
    def create_quiz():
        """
        API endpoint để tạo mới một quiz
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
            quiz_data = CreateQuizSchema(**data)

            result = quiz_service.create_quiz(quiz_data, current_user_id)

            return jsonify({
                'message': 'Tạo quiz thành công',
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

    @quiz_controller.route('/quizzes/<int:quiz_id>', methods=['GET'])
    @jwt_required()
    def get_quiz(quiz_id: int):
        """
        API endpoint để lấy thông tin chi tiết của một quiz
        """
        try:
            result = quiz_service.get_quiz(quiz_id)

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

    return quiz_controller 