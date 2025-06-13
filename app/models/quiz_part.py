from sqlalchemy import Column, Integer
from app.utils import Base, PG_TABLE_QUIZ_PART

class QuizPart(Base):
    __tablename__ = PG_TABLE_QUIZ_PART

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer)
    part_id = Column(Integer)
    sort = Column(Integer, default=0)

    def __repr__(self):
        return f'<QuizPart {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'part_id': self.part_id,
            'sort': self.sort
        } 