from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config, models

SQLALCHEMY_DATABASE_URL = config.DATABASE_CONNECTION_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initial_db():
    models.Base.metadata.create_all(bind=engine)