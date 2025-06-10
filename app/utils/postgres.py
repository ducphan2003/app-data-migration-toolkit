from math import e
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import app_config
from contextlib import contextmanager

DATABASE_URL = f"postgresql://{app_config.POSTGRES__USER}:{app_config.POSTGRES__PASS}@{app_config.POSTGRES__HOST}/{app_config.POSTGRES__DB}"
engine = create_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=1800, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db(app):
    Base.metadata.create_all(bind=engine)


@contextmanager
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
