import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from config import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Model_1.db.models import Base, FileRecord


engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Create table(s) if not exist
Base.metadata.create_all(bind=engine)

def is_file_processed(file_hash: str) -> bool:
    """
    Checks if the file (by hash) already exists in the DB.
    """
    db = SessionLocal()
    result = db.query(FileRecord).filter(FileRecord.id == file_hash).first()
    db.close()
    return result is not None

def save_file_metadata(file_hash: str, filename: str):
    """
    Inserts a new file record into the DB.
    """
    db = SessionLocal()
    record = FileRecord(id=file_hash, filename=filename)
    db.add(record)
    db.commit()
    db.close()
