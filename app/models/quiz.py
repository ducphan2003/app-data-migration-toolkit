from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, SmallInteger, UUID, CheckConstraint
from app.utils import Base
from app.utils.const import PG_TABLE_QUIZ, MASTER_CONFIG_STATUS_PUBLISHED

class Quiz(Base):
    __tablename__ = PG_TABLE_QUIZ

    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False, default=MASTER_CONFIG_STATUS_PUBLISHED)
    sort = Column(Integer)
    user_created = Column(UUID)
    date_created = Column(DateTime(timezone=True))
    user_updated = Column(UUID)
    date_updated = Column(DateTime(timezone=True))
    type = Column(Integer)
    content = Column(Text)
    title = Column(String(255))
    order = Column(Integer)
    time = Column(Integer)
    listening = Column(UUID)
    description = Column(Text)
    instruction = Column(Integer)
    quiz_code = Column(String(255))
    limit_submit = Column(Integer)
    question = Column(Text)
    samples = Column(Text)
    thumbnail = Column(UUID)
    vote_count = Column(Integer, nullable=False, default=0)
    quiz_type = Column(SmallInteger)
    full_id = Column(Integer)
    is_test = Column(Boolean)
    mode = Column(SmallInteger, default=0)
    simplified_id = Column(Integer)
    mock_test_id = Column(Integer)
    mock_test_type = Column(Integer)
    total_submitted = Column(Integer, default=0)
    short_description = Column(Text)
    practice_listing_priority = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)
    writing_task_type = Column(Integer)
    meta = Column(JSON)
    prompt_set_id = Column(Integer)
    speaking_part_type = Column(Integer)
    speaking_topic_id = Column(Integer)
    instruction_audio = Column(UUID)

    __table_args__ = (
        CheckConstraint('vote_count >= 0', name='quiz_vote_count_check'),
    )

    def __repr__(self):
        return f'<Quiz {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'title': self.title,
            'content': self.content,
            'quiz_type': self.quiz_type,
            'is_test': self.is_test,
            'is_public': self.is_public,
            'meta': self.meta
        } 