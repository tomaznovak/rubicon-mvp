from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

connector = Connector()

def getconn():
    return connector.connect(
        instance_connection_string=settings.database_hostname,
        driver="pg8000",
        user=settings.database_username,
        password=settings.database_password,
        db=settings.database_name
    )

engine = create_engine("postgresql+pg8000://",
                       creator=getconn,
                       pool_size=5,
                       max_overflow=2
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()