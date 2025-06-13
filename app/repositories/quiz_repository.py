from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.quiz import Quiz
from app.models.part import Part
from app.models.question_set import QuestionSet
from app.models.question import Question
from app.models.quiz_part import QuizPart
from app.schemas.quiz_schema import CreateQuizSchema, QuestionType

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_quiz(self, quiz_data: Dict[str, Any], user_id: str) -> Quiz:
        """Tạo mới một quiz"""
        # Tạo quiz
        quiz = Quiz(
            title=quiz_data['title'],
            type=quiz_data['type'],
            time=quiz_data['time'],
            instruction_audio=quiz_data['instruction_audio'],
            is_public=quiz_data['is_public'],
            is_test=quiz_data['is_test'],
            user_created=user_id,
            date_created=datetime.now(),
            status='published',
            # Thêm các trường mặc định
            sort=quiz_data['sort'],
            user_updated=user_id,
            date_updated=datetime.now(),
            content=quiz_data['content'],
            order=quiz_data['order'],
            listening=quiz_data['listening'],
            description=quiz_data['description'],
            instruction=quiz_data['instruction'],
            quiz_code=quiz_data['quiz_code'],
            limit_submit=quiz_data['limit_submit'],
            question=quiz_data['question'],
            samples=quiz_data['samples'],
            thumbnail=quiz_data['thumbnail'],
            vote_count=0,
            quiz_type=quiz_data['quiz_type'],
            full_id=quiz_data['full_id'],
            mode=quiz_data['mode'],
            simplified_id=quiz_data['simplified_id'],
            mock_test_id=quiz_data['mock_test_id'],
            mock_test_type=quiz_data['mock_test_type'],
            total_submitted=0,
            short_description=quiz_data['short_description'],
            practice_listing_priority=0,
            writing_task_type=quiz_data['writing_task_type'],
            meta=quiz_data['meta'],
            prompt_set_id=quiz_data['prompt_set_id'],
            speaking_part_type=quiz_data['speaking_part_type'],
            speaking_topic_id=None
        )
        self.db.add(quiz)
        self.db.flush()  # Để lấy quiz.id

        # Tạo parts và questions
        for part_idx, part_data in enumerate(quiz_data['parts'], 1):
            # Lấy instruction_id từ instruction dictionary nếu có
            instruction_id = None
            if part_data.get('instruction') and isinstance(part_data['instruction'], dict):
                instruction_id = part_data['instruction'].get('id')

            part = Part(
                title=part_data['title'],
                content=part_data['content'],
                instruction=instruction_id,
                file_id=part_data['file_id'] if part_data['file_id'] else None,
                sort=part_idx,
                user_created=user_id,
                date_created=datetime.now(),
                passage=part_data['passage'],
                simplified_content=part_data['simplified_content'],
                # Thêm các trường mặc định
                date_updated=datetime.now(),
                order=part_data['order'],
                quiz=quiz.id,
                time=part_data['time'],
                question_count=0,
                listen_from=part_data['listen_from'],
                listen_to=part_data['listen_to'],
                task_instruction=part_data['task_instruction'],
                transcription=part_data['transcription']
            )
            self.db.add(part)
            self.db.flush()  # Để lấy part.id

            # Tạo quiz_part relationship
            quiz_part = QuizPart(
                quiz_id=quiz.id,
                part_id=part.id,
                sort=part_idx
            )
            self.db.add(quiz_part)

            # Tạo question sets và questions
            for qset_idx, qset_data in enumerate(part_data['question_sets'], 1):
                question_set = QuestionSet(
                    part_id=part.id,
                    title=qset_data['title'],
                    description=qset_data['description'],
                    question_type=qset_data['question_type'],
                    content=qset_data['content'],
                    options=qset_data['options'],
                    option_title=qset_data['option_title'],
                    allow_reuse=qset_data['allow_reuse'],
                    max_selections=qset_data['max_selections'],
                    sort=qset_idx,
                    user_created=user_id,
                    date_created=datetime.now(),
                    question_count=len(qset_data['questions']),
                    # Thêm các trường mặc định
                    user_updated=user_id,
                    date_updated=datetime.now()
                )
                self.db.add(question_set)
                self.db.flush()  # Để lấy question_set.id

                # Tạo questions
                for q_idx, q_data in enumerate(qset_data['questions'], 1):
                    question = Question(
                        question_set_id=question_set.id,
                        title=q_data['title'],
                        content=q_data['content'],
                        question_type=q_data['question_type'],
                        options=q_data['options'],
                        correct_answer=q_data['correct_answer'],
                        correct_answers=q_data['correct_answers'],
                        listen_from=q_data['listen_from'],
                        explain=q_data['explain'],
                        sort=q_idx,
                        user_created=user_id,
                        date_created=datetime.now(),
                        status='published',
                        time_limit=q_data['time_limit'],
                        locate_info=q_data['locate_info'],
                        # Thêm các trường mặc định
                        user_updated=user_id,
                        date_updated=datetime.now(),
                        type=q_data['type'],
                        single_choice_radio=q_data['single_choice_radio'],
                        selection=q_data['selection'],
                        mutilple_choice=q_data['mutilple_choice'],
                        gap_fill_in_blank=q_data['gap_fill_in_blank'],
                        selection_option=q_data['selection_option'],
                        locate=q_data['locate'],
                        order=q_data['order'],
                        description=q_data['description'],
                        content_writing=q_data['content_writing'],
                        time_to_think=q_data['time_to_think'],
                        instruction=q_data['instruction'],
                        writing_graph_image=q_data['writing_graph_image'],
                        writing_graph_description=q_data['writing_graph_description'],
                        writing_graph_type=q_data['writing_graph_type'],
                        audio_url=q_data['audio_url'],
                        max_words=q_data['max_words'],
                        min_words=q_data['min_words'],
                        text=q_data['text']
                    )
                    self.db.add(question)

        self.db.commit()
        return quiz

    def get_quiz_by_id(self, quiz_id: int) -> Optional[Quiz]:
        """Lấy thông tin quiz theo ID"""
        return self.db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def get_quiz_with_details(self, quiz_id: int) -> Dict[str, Any]:
        """Lấy thông tin chi tiết của quiz bao gồm parts và questions"""
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            return None

        # Lấy parts của quiz
        quiz_parts = self.db.query(QuizPart).filter(QuizPart.quiz_id == quiz_id).order_by(QuizPart.sort).all()
        parts = []
        
        for quiz_part in quiz_parts:
            part = self.db.query(Part).filter(Part.id == quiz_part.part_id).first()
            if part:
                # Lấy question sets của part
                question_sets = self.db.query(QuestionSet).filter(
                    QuestionSet.part_id == part.id
                ).order_by(QuestionSet.sort).all()
                
                part_data = part.to_dict()
                part_data['question_sets'] = []
                
                for qset in question_sets:
                    # Lấy questions của question set
                    questions = self.db.query(Question).filter(
                        Question.question_set_id == qset.id
                    ).order_by(Question.sort).all()
                    
                    qset_data = qset.to_dict()
                    qset_data['questions'] = [q.to_dict() for q in questions]
                    part_data['question_sets'].append(qset_data)
                
                parts.append(part_data)

        return {
            **quiz.to_dict(),
            'parts': parts
        } 