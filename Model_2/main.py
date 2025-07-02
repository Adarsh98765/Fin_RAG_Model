from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
import uuid


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

        # Step 2: Analyze graph-friendly data (no company name now)
        graph_data = analyze_graph_metrics(request.document_id)
        if not graph_data or len(graph_data) == 0:
            raise HTTPException(status_code=400, detail="Generated graph data is empty")

        # Save summary
        db.merge(SummaryRecord(doc_id=request.document_id, summary=summary))

        # Save each graph data row
        for entry in graph_data:
            db.merge(GraphData(
                id=str(uuid.uuid4()),  # ✅ generate a unique primary key
                doc_id=request.document_id,
                metric_name=entry["metric_name"],
                value=entry["value"],
                notes=entry.get("notes", "")
        ))


        db.commit()

        return {
            "status": "success",
            "summary": summary,
            "graph_data": graph_data
        }

    except SQLAlchemyError as e:
        db.rollback()
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Database error occurred.")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad input: {str(ve)}")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")

    finally:
        db.close()
