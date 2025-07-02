from sqlalchemy import Column, String , Text
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()

class FileRecord(Base):
    """
    Table to store uploaded file metadata.
    Each row represents one unique file (by hash).
    """
    __tablename__ = "file_records"

    id = Column(String, primary_key=True)       # file hash (document_id)
    filename = Column(String)                   # original filename

# --- Model 2 Table ---
class SummaryRecord(Base):
    __tablename__ = "summaries"

    doc_id = Column(String, primary_key=True, index=True)
    summary = Column(Text)

class GraphData(Base):
    __tablename__ = "graphs"
    id = Column(String, primary_key=True)  # you can use a UUID or auto-generated ID
    doc_id = Column(String, index=True)
    metric_name = Column(String)
    value = Column(String)
    notes = Column(Text)