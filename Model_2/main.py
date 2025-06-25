from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from Model_2.analyzer import analyze_document
from Model_1.db.models import SummaryRecord
from Model_1.db.crud import SessionLocal

app = FastAPI()

class AnalyzeRequest(BaseModel):
    document_id: str

@app.post("/analyze_pdf/")
def analyze_pdf(request: AnalyzeRequest):
    db = SessionLocal()
    try:
        summary = analyze_document(request.document_id)

        if not summary or len(summary.strip()) == 0:
            raise HTTPException(status_code=400, detail="Generated summary is empty")

        record = SummaryRecord(doc_id=request.document_id, summary=summary)
        db.merge(record)
        db.commit()

        return {"status": "success", "summary": summary}

    except SQLAlchemyError as db_err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad input: {str(ve)}")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected server error.")

    finally:
        db.close()
