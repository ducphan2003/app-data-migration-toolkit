from sqlalchemy.orm import Session
from app.models.remote_config import Remote_Config
from app.repositories.base import BaseRepository
import redis
from app.utils import const
from app.utils.error import CustomError
from sqlalchemy.exc import SQLAlchemyError
from app.utils import db_session


class ConfigRepository(BaseRepository[Remote_Config]):
    def __init__(
        self, 
        session: Session, 
        redis_client: redis.Redis
    ):

        super().__init__(Remote_Config, session)
        self.redis_client = redis_client
    
    def get_from_redis(
        self, 
        key:str
    ):
        try:
            return self.redis_client.get(key), None
        except redis.RedisError as e:
            return None, e
        except Exception as e:
            return None, CustomError(str(e))
        
    def save_to_redis(
        self, 
        key: str, 
        value: str, 
        expired_time:int = const.DEFAULT_CACHE_TIME
    ):
        try:
            self.redis_client.set(key, value, ex=expired_time)
            return True, None
        except redis.RedisError as e:
            return False, e
        except Exception as e:
            return False, CustomError(str(e))
            
    def get_from_pg(
        self, 
        key:str, 
        status:int = 1
    ):
        try:
            with db_session() as session:
                result = session.query(Remote_Config).filter_by(key=key).filter_by(status=status).first()
                return result, None
        except SQLAlchemyError as e:
            return None, e
        except Exception as e:
            return None, CustomError(str(e))
    
    def get_default_from_config_file(
        self, 
        key: str, 
        config_json: dict
    ):
        value = config_json.get(key)
        if value is not None:
            return value
        else:
            return None
