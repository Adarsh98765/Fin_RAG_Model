from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from Model_2.analyzer import analyze_document_summary, analyze_graph_metrics
from Model_1.db.models import SummaryRecord, GraphData
from Model_1.db.crud import SessionLocal

app = FastAPI()

class AnalyzeRequest(BaseModel):
    document_id: str

@app.post("/analyze_pdf/")
def analyze_pdf(request: AnalyzeRequest):
    db = SessionLocal()
    try:
        # Step 1: Analyze financial summary
        summary = analyze_document_summary(request.document_id)
        if not summary or len(summary.strip()) == 0:
            raise HTTPException(status_code=400, detail="Generated summary is empty")

        # Step 2: Analyze graph-friendly data
        graph_data = analyze_graph_metrics(request.document_id)
        if not graph_data or len(graph_data.strip()) == 0:
            raise HTTPException(status_code=400, detail="Generated graph data is empty")

        # Save both into DB
        db.merge(SummaryRecord(doc_id=request.document_id, summary=summary))
        db.merge(GraphData(doc_id=request.document_id, graph_text=graph_data))
        db.commit()

        return {
            "status": "success",
            "summary": summary,
            "graph_data": graph_data
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad input: {str(ve)}")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")

    finally:
        db.close()
