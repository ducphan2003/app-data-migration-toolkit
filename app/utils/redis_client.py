import redis
from config.config import app_config


def get_redis_client():
    return redis.Redis(
        host=app_config.REDIS__HOST,
        port=app_config.REDIS__PORT,
        db=app_config.REDIS__DB
    )


redis_client = get_redis_client()
