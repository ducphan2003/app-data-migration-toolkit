import json
import redis
from flask import current_app

class RedisHelper:
    def __init__(self):
        self.redis = redis.from_url(current_app.config['REDIS_URL'])
    
    def set_migration_status(self, process_id: str, status: dict):
        key = f'migration:{process_id}'
        self.redis.set(key, json.dumps(status))
        # Set expiration to 24 hours
        self.redis.expire(key, 86400)
    
    def get_migration_status(self, process_id: str) -> dict:
        key = f'migration:{process_id}'
        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data) 