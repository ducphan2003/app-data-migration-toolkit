from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.utils import Base, PG_TABLE_MIGRATE_PROCESS
from app.utils.const import MASTER_CONFIG_STATUS_PUBLISHED

class MigrateProcess(Base):
    __tablename__ = PG_TABLE_MIGRATE_PROCESS

    id = Column(Integer, primary_key=True)
    quiz_id = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=MASTER_CONFIG_STATUS_PUBLISHED)  # pending, processing, completed, failed
    
    # Kết quả và trạng thái của từng bước
    prepare_data_status = Column(String(50), nullable=False, default='pending')  # pending, processing, completed, failed
    prepare_data_result = Column(JSON, nullable=True)
    prepare_data_error = Column(String(1000), nullable=True)
    
    mapping_structure_status = Column(String(50), nullable=False, default='pending')
    mapping_structure_result = Column(JSON, nullable=True)
    mapping_structure_error = Column(String(1000), nullable=True)
    
    validate_data_status = Column(String(50), nullable=False, default='pending')
    validate_data_result = Column(JSON, nullable=True)
    validate_data_error = Column(String(1000), nullable=True)
    
    # Kết quả cuối cùng
    result = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    
    date_created = Column(DateTime(timezone=True))
    date_updated = Column(DateTime(timezone=True))

    def __repr__(self):
        return f'<MigrateProcess {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'status': self.status,
            'prepare_data': {
                'status': self.prepare_data_status,
                'result': self.prepare_data_result,
                'error': self.prepare_data_error
            },
            'mapping_structure': {
                'status': self.mapping_structure_status,
                'result': self.mapping_structure_result,
                'error': self.mapping_structure_error
            },
            'validate_data': {
                'status': self.validate_data_status,
                'result': self.validate_data_result,
                'error': self.validate_data_error
            },
            'result': self.result,
            'error_message': self.error_message,
            'date_created': self.date_created,
            'date_updated': self.date_updated
        } 