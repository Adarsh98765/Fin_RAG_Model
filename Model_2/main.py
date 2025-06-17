from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Model_2.analyzer import analyze_document
from Model_1.db.models import SummaryRecord
from Model_1.db.crud import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

class AnalyzeRequest(BaseModel):
    document_id: str

@app.post("/analyze_pdf/")
def analyze_pdf(request: AnalyzeRequest):
    try:
        # Step 1: Run the CoT analysis
        summary = analyze_document(request.document_id)

        # Step 2: Save the summary to DB
        db = SessionLocal()
        record = SummaryRecord(doc_id=request.document_id, summary=summary)
        db.merge(record)  # Inserts new or updates existing
        db.commit()
        db.close()

        return {"status": "success", "summary": summary}

    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_err)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
