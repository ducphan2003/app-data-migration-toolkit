import uuid
from app.repositories.migrate import MigrateRepository
from app.utils.redis_helper import RedisHelper

class MigrateService:
    def __init__(
        self, 
        migrate_repo: MigrateRepository
    ):
        self.migrate_repo = migrate_repo
