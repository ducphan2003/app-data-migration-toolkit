from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from app.models.migrate_process import MigrateProcess

class MigrateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_migrate_process(self, quiz_id: str, user_id: str) -> MigrateProcess:
        """Tạo mới một migrate process"""
        migrate_process = MigrateProcess(
            quiz_id=quiz_id,
            status="processing",
            user_created=user_id,
            date_created=datetime.utcnow(),
            prepare_data_status="pending",
            mapping_structure_status="pending", 
            validate_data_status="pending"
        )
        
        self.db.add(migrate_process)
        self.db.commit()
        self.db.refresh(migrate_process)
        
        return migrate_process

    def get_migrate_process_by_id(self, migrate_process_id: int) -> Optional[MigrateProcess]:
        """Lấy thông tin migrate process theo ID"""
        return self.db.query(MigrateProcess).filter(
            MigrateProcess.id == migrate_process_id
        ).first()

    def update_prepare_data_result(self, migrate_process_id: int, result: Dict[str, Any]) -> None:
        """Cập nhật kết quả step 1 - prepare data"""
        migrate_process = self.get_migrate_process_by_id(migrate_process_id)
        if migrate_process:
            migrate_process.prepare_data_status = "completed"
            migrate_process.prepare_data_result = json.dumps(result)
            migrate_process.date_updated = datetime.utcnow()
            self.db.commit()

    def update_mapping_structure_result(self, migrate_process_id: int, result: Dict[str, Any]) -> None:
        """Cập nhật kết quả step 2 - mapping structure"""
        migrate_process = self.get_migrate_process_by_id(migrate_process_id)
        if migrate_process:
            migrate_process.mapping_structure_status = "completed"
            migrate_process.mapping_structure_result = json.dumps(result)
            migrate_process.date_updated = datetime.utcnow()
            self.db.commit()

    def update_validate_data_result(self, migrate_process_id: int, result: Dict[str, Any]) -> None:
        """Cập nhật kết quả step 3 - validate data"""
        migrate_process = self.get_migrate_process_by_id(migrate_process_id)
        if migrate_process:
            migrate_process.validate_data_status = "completed"
            migrate_process.validate_data_result = json.dumps(result)
            migrate_process.date_updated = datetime.utcnow()
            self.db.commit()

    def update_final_result(self, migrate_process_id: int, result: Dict[str, Any]) -> None:
        """Cập nhật kết quả cuối cùng và đánh dấu hoàn thành"""
        migrate_process = self.get_migrate_process_by_id(migrate_process_id)
        if migrate_process:
            migrate_process.status = "completed"
            migrate_process.final_result = json.dumps(result)
            migrate_process.date_updated = datetime.utcnow()
            self.db.commit()

    def update_error(self, migrate_process_id: int, error_message: str) -> None:
        """Cập nhật lỗi và đánh dấu failed"""
        migrate_process = self.get_migrate_process_by_id(migrate_process_id)
        if migrate_process:
            migrate_process.status = "failed"
            migrate_process.error_message = error_message
            migrate_process.date_updated = datetime.utcnow()
            self.db.commit()

    def get_migrate_processes_by_user(self, user_id: str, limit: int = 10) -> List[MigrateProcess]:
        """Lấy danh sách migrate processes của user"""
        return self.db.query(MigrateProcess).filter(
            MigrateProcess.user_created == user_id
        ).order_by(desc(MigrateProcess.date_created)).limit(limit).all() 