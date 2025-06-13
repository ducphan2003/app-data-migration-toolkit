from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, UUID
from app.utils import Base
from app.utils.const import PG_TABLE_QUESTION_SET

class QuestionSet(Base):
    __tablename__ = PG_TABLE_QUESTION_SET

    id = Column(Integer, primary_key=True)
    part_id = Column(Integer)
    user_created = Column(UUID, nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False)
    user_updated = Column(UUID)
    date_updated = Column(DateTime(timezone=True))
    question_type = Column(Text, nullable=False)
    question_count = Column(Integer, nullable=False)
    title = Column(Text)
    description = Column(Text, nullable=False)
    content = Column(Text)
    option_title = Column(Text)
    options = Column(JSON)
    allow_reuse = Column(Boolean)
    max_selections = Column(Integer)
    sort = Column(Integer)

    def __repr__(self):
        return f'<QuestionSet {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'part_id': self.part_id,
            'question_type': self.question_type,
            'question_count': self.question_count,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'options': self.options,
            'allow_reuse': self.allow_reuse,
            'max_selections': self.max_selections
        } 