from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger, JSON, ARRAY, ForeignKey, UUID
from app.utils import Base
from app.utils.const import PG_TABLE_QUESTION, MASTER_CONFIG_STATUS_PUBLISHED

class Question(Base):
    __tablename__ = PG_TABLE_QUESTION

    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False, default=MASTER_CONFIG_STATUS_PUBLISHED)
    sort = Column(Integer)
    user_created = Column(UUID)
    date_created = Column(DateTime(timezone=True))
    user_updated = Column(UUID)
    date_updated = Column(DateTime(timezone=True))
    title = Column(String(255))
    content = Column(Text)
    type = Column(String(255))
    single_choice_radio = Column(JSON)
    selection = Column(JSON)
    mutilple_choice = Column(JSON)
    gap_fill_in_blank = Column(Text)
    quiz = Column(Integer)
    selection_option = Column(JSON)
    locate = Column(String(255))
    order = Column(Integer)
    explain = Column(Text)
    description = Column(Text)
    content_writing = Column(Text)
    part = Column(Integer)
    time_to_think = Column(Integer)
    listen_from = Column(Integer)
    question_type = Column(Text)
    instruction = Column(Text)
    writing_graph_image = Column(UUID)
    writing_graph_description = Column(Text)
    writing_graph_type = Column(SmallInteger)
    audio_url = Column(Text)
    time_limit = Column(Integer, default=30)
    max_words = Column(Integer)
    min_words = Column(Integer)
    question_set_id = Column(Integer)
    correct_answer = Column(Text)
    correct_answers = Column(ARRAY(Text))
    text = Column(Text)
    options = Column(JSON)
    locate_info = Column(JSON)

    def __repr__(self):
        return f'<Question {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'quiz': self.quiz,
            'part': self.part,
            'question_type': self.question_type,
            'correct_answer': self.correct_answer,
            'correct_answers': self.correct_answers,
            'options': self.options
        } 