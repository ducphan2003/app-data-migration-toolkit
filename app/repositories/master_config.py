from re import S
from typing import Any
from sqlalchemy.orm import Session
from app.models.master_config import MasterConfig
from app.repositories.base import BaseRepository


class MasterConfigRepository(BaseRepository[MasterConfig]):
    def __init__(
        self, 
        session: Session
    ):
        super().__init__(MasterConfig, session)

    def get_error_label_by_public_id(
        self, 
        public_id: str, 
        error_name: str
    ) -> tuple[tuple, Exception]:
        try:
            result = self.session.query(MasterConfig).filter_by(public_id=public_id).first()
            error_id = [
                (error["id"], error["error_type"]) 
                for error in result.value 
                if error["error_name"].lower().strip() == error_name.lower().strip()
            ]
            if len(error_id) > 0:
                return error_id[0], None
            return (None, None), None
        except Exception as e:
            return (None, None), e
