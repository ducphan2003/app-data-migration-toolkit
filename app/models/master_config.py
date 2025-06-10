from ast import In
from datetime import datetime
from re import I
from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.utils import Base, PG_TABLE_MASTER_CONFIG
from app.utils.const import MASTER_CONFIG_STATUS_PUBLISHED


class MasterConfig(Base):
    __tablename__ = PG_TABLE_MASTER_CONFIG
    id = Column(Integer, primary_key=True)
    public_id = Column(String)
    description = Column(String)
    value = Column(JSON, default=None)
    created_at = Column(DateTime)
    status = Column(Integer)

    def __init__(
        self, 
        id: int, 
        public_id: str, 
        description: str, 
        value: dict = None, 
        created_at: datetime = datetime.now(), 
        status: int = MASTER_CONFIG_STATUS_PUBLISHED
    ):
        self.id = id
        self.public_id = public_id
        self.description = description
        self.value = value
        self.created_at = created_at
        self.status = status

    @staticmethod
    def table_name():
        return PG_TABLE_MASTER_CONFIG
