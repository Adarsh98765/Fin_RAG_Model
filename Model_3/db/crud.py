from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model_1.db.models import SummaryRecord
from Model_1.db.models import Base  # in case you want to auto-create schema

# Update this if you're using a different DB
DATABASE_URL = "sqlite:///files.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Optional: Auto-create tables
Base.metadata.create_all(bind=engine)

def get_summary(doc_id: str) -> str:
    db = SessionLocal()
    try:
        record = db.query(SummaryRecord).filter(SummaryRecord.doc_id == doc_id).first()
        return record.summary if record else None
    finally:
        db.close()

def get_summaries(doc_id_1: str, doc_id_2: str) -> tuple[str, str]:
    db = SessionLocal()
    try:
        record1 = db.query(SummaryRecord).filter(SummaryRecord.doc_id == doc_id_1).first()
        record2 = db.query(SummaryRecord).filter(SummaryRecord.doc_id == doc_id_2).first()
        return (record1.summary if record1 else None,
                record2.summary if record2 else None)
    finally:
        db.close()
