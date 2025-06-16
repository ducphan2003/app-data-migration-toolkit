from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json
from typing import Dict, Any, Optional

Base = declarative_base()

class MigrateProcess(Base):
    __tablename__ = 'migrate_process'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(String(50), nullable=False, comment="ID của quiz cần migrate")
    status = Column(String(20), nullable=False, default="processing", comment="Trạng thái tổng thể: processing, completed, failed")
    
    # Step 1: Prepare Data
    prepare_data_status = Column(String(20), default="pending", comment="Trạng thái step 1: pending, processing, completed, failed")
    prepare_data_result = Column(Text, nullable=True, comment="Kết quả step 1 (JSON)")
    
    # Step 2: Mapping Structure  
    mapping_structure_status = Column(String(20), default="pending", comment="Trạng thái step 2: pending, processing, completed, failed")
    mapping_structure_result = Column(Text, nullable=True, comment="Kết quả step 2 (JSON)")
    
    # Step 3: Validate Data
    validate_data_status = Column(String(20), default="pending", comment="Trạng thái step 3: pending, processing, completed, failed")
    validate_data_result = Column(Text, nullable=True, comment="Kết quả step 3 (JSON)")
    
    # Final result
    final_result = Column(Text, nullable=True, comment="Kết quả cuối cùng (JSON)")
    error_message = Column(Text, nullable=True, comment="Thông báo lỗi nếu có")
    
    # Audit fields
    user_created = Column(String(50), nullable=False, comment="User tạo")
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Ngày tạo")
    date_updated = Column(DateTime, nullable=True, comment="Ngày cập nhật cuối")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        result = {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'status': self.status,
            'prepare_data_status': self.prepare_data_status,
            'mapping_structure_status': self.mapping_structure_status,
            'validate_data_status': self.validate_data_status,
            'error_message': self.error_message,
            'user_created': self.user_created,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }
        
        # Parse JSON results
        if self.prepare_data_result:
            try:
                result['prepare_data_result'] = json.loads(self.prepare_data_result)
            except json.JSONDecodeError:
                result['prepare_data_result'] = None
                
        if self.mapping_structure_result:
            try:
                result['mapping_structure_result'] = json.loads(self.mapping_structure_result)
            except json.JSONDecodeError:
                result['mapping_structure_result'] = None
                
        if self.validate_data_result:
            try:
                result['validate_data_result'] = json.loads(self.validate_data_result)
            except json.JSONDecodeError:
                result['validate_data_result'] = None
                
        if self.final_result:
            try:
                result['final_result'] = json.loads(self.final_result)
            except json.JSONDecodeError:
                result['final_result'] = None
        
        return result 