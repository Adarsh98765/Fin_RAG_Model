import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from config import DATABASE_URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from Model_1.db.models import Base, FileRecord, SummaryRecord, GraphData

# --- DB Engine and Session ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

# --- File Metadata Functions ---
def is_file_processed(file_hash: str) -> bool:
    db = SessionLocal()
    result = db.query(FileRecord).filter(FileRecord.id == file_hash).first()
    db.close()
    return result is not None

def save_file_metadata(file_hash: str, filename: str):
    db = SessionLocal()
    record = FileRecord(id=file_hash, filename=filename)
    db.add(record)
    db.commit()
    db.close()

# --- Summary Functions ---
def get_summary(db: Session, doc_id: str) -> str:
    record = db.query(SummaryRecord).filter(SummaryRecord.doc_id == doc_id).first()
    return record.summary if record else None

def save_summary(db: Session, doc_id: str, summary_text: str):
    record = SummaryRecord(doc_id=doc_id, summary=summary_text)
    db.merge(record)
    db.commit()

# --- Graph Data Functions ---
def get_graph_data(db: Session, doc_id: str) -> str:
    record = db.query(GraphData).filter(GraphData.doc_id == doc_id).first()
    return record.graph_text if record else None

def save_graph_data(db: Session, doc_id: str, graph_text: str):
    record = GraphData(doc_id=doc_id, graph_text=graph_text)
    db.merge(record)
    db.commit()
