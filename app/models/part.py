from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger, JSON, ForeignKey, UUID
from app.utils import Base
from app.utils.const import PG_TABLE_PART

class Part(Base):
    __tablename__ = PG_TABLE_PART

    id = Column(Integer, primary_key=True)
    sort = Column(Integer)
    user_created = Column(UUID)
    date_created = Column(DateTime(timezone=True))
    date_updated = Column(DateTime(timezone=True))
    title = Column(String(255))
    order = Column(Integer)
    content = Column(Text)
    quiz = Column(Integer)
    time = Column(Integer)
    passage = Column(Integer, default=0)
    simplified_content = Column(Text)
    question_count = Column(SmallInteger, default=0)
    listen_from = Column(Integer)
    listen_to = Column(Integer)
    instruction = Column(Integer)
    task_instruction = Column(Text)
    transcription = Column(JSON)
    file_id = Column(UUID)

    def __repr__(self):
        return f'<Part {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'quiz': self.quiz,
            'time': self.time,
            'question_count': self.question_count,
            'task_instruction': self.task_instruction,
            'transcription': self.transcription
        } 
