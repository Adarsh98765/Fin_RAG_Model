from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model_1.db.models import SummaryRecord, GraphData, Base

# Database URL
DATABASE_URL = "sqlite:///files.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
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

def get_graph_data(doc_id: str) -> list[dict]:
    """
    Returns a list of structured metrics:
    [
        { "metric_name": ..., "value": ..., "notes": ... },
        ...
    ]
    """
    db = SessionLocal()
    try:
        records = db.query(GraphData).filter(GraphData.doc_id == doc_id).all()
        return [
            {
                "metric_name": r.metric_name,
                "value": r.value,
                "notes": r.notes
            } for r in records
        ]
    finally:
        db.close()
