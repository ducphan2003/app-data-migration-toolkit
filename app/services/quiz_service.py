from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.repositories.quiz_repository import QuizRepository
from app.schemas.quiz_schema import CreateQuizSchema, QuizResponseSchema
from app.utils.exceptions import NotFoundException, ValidationError

class QuizService:
    def __init__(self, quiz_repo: QuizRepository):
        self.quiz_repo = quiz_repo

    def create_quiz(self, quiz_data: CreateQuizSchema, user_id: str) -> Dict[str, Any]:
        """
        Tạo mới một quiz
        """
        try:
            # Validate dữ liệu
            self._validate_quiz_data(quiz_data)
            
            # Convert quiz_data to dict and handle special fields
            quiz_dict = quiz_data.model_dump()
            
            # Handle instruction_audio
            if not quiz_dict.get('instruction_audio'):
                quiz_dict['instruction_audio'] = None
                
            # Convert enums to their values
            quiz_dict['type'] = quiz_data.type.value
            
            for part in quiz_dict['parts']:
                for qset in part['question_sets']:
                    qset['question_type'] = qset['question_type'].value
                    for question in qset['questions']:
                        question['question_type'] = question['question_type'].value
                
            quiz = self.quiz_repo.create_quiz(quiz_dict, user_id)
            # Lấy thông tin chi tiết của quiz vừa tạo
            quiz_detail = self.quiz_repo.get_quiz_with_details(quiz.id)
            return quiz_detail
        except Exception as e:
            self.quiz_repo.db.rollback()
            raise e

    def get_quiz(self, quiz_id: int) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết của một quiz
        """
        quiz_detail = self.quiz_repo.get_quiz_with_details(quiz_id)
        if not quiz_detail:
            raise NotFoundException(f"Không tìm thấy quiz với id {quiz_id}")
        return quiz_detail

    def _validate_quiz_data(self, quiz_data: CreateQuizSchema) -> None:
        """
        Validate dữ liệu quiz trước khi tạo
        """
        errors = []

        # Validate parts
        if not quiz_data.parts:
            errors.append("Quiz phải có ít nhất một part")
        
        for part_idx, part in enumerate(quiz_data.parts, 1):
            # Validate question sets
            if not part.question_sets:
                errors.append(f"Part {part_idx} phải có ít nhất một question set")
            
            for qset_idx, qset in enumerate(part.question_sets, 1):
                # Validate questions
                if not qset.questions:
                    errors.append(f"Question set {qset_idx} trong part {part_idx} phải có ít nhất một câu hỏi")
                
                # Validate question type consistency
                for q_idx, question in enumerate(qset.questions, 1):
                    # Validate specific question types
                    if question.question_type.value == "MULTIPLE_CHOICE_ONE":
                        if not question.correct_answer:
                            errors.append(
                                f"Câu hỏi multiple choice {q_idx} trong question set {qset_idx} "
                                f"(part {part_idx}) phải có correct_answer"
                            )

                    elif question.question_type.value == "MULTIPLE_SELECTION":
                        if not question.correct_answers or len(question.correct_answers) == 0:
                            errors.append(
                                f"Câu hỏi multiple selection {q_idx} trong question set {qset_idx} "
                                f"(part {part_idx}) phải có ít nhất một correct_answers"
                            )

                    elif question.question_type.value == "GAP_FILLING":
                        if not question.correct_answers or len(question.correct_answers) == 0:
                            errors.append(
                                f"Câu hỏi gap filling {q_idx} trong question set {qset_idx} "
                                f"(part {part_idx}) phải có correct_answers"
                            )

                    elif question.question_type.value == "MATCHING_INFO":
                        if not question.correct_answer:
                            errors.append(
                                f"Câu hỏi matching info {q_idx} trong question set {qset_idx} "
                                f"(part {part_idx}) phải có correct_answer"
                            )

        if errors:
            raise ValidationError(errors) 