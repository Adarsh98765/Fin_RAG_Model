from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Model_2.analyzer import analyze_document

app = FastAPI()

class AnalyzeRequest(BaseModel):
    document_id: str

@app.post("/analyze_pdf/")
def analyze_pdf(request: AnalyzeRequest):
    try:
        result = analyze_document(request.document_id)
        return {"status": "success", "summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
