# File: app/database.py (Phiên bản mới)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Import đối tượng settings từ file config
from app.core.config import settings

# Sử dụng DATABASE_URL từ đối tượng settings
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()