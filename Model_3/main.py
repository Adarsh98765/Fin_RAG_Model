from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import tempfile, requests
import plotly.io as pio

from Model_3.graph.plot_generator import generate_comparison_chart
from Model_3.db.crud import get_summaries
from Model_3.rag.qa_chain import answer_query

app = FastAPI()

MODEL_1_URL = "http://localhost:8001/upload_pdf/"
MODEL_2_URL = "http://localhost:8002/analyze_pdf/"

@app.get("/")
def root():
    return {"message": "Model 3 API is running."}

# ----------------------
# 🔍 Compare API
# ----------------------
@app.post("/compare")
async def compare_pdfs(pdf_1: UploadFile = File(...), pdf_2: UploadFile = File(...)):
    try:
        # Step 1: Save PDFs temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
            tmp1.write(await pdf_1.read())
            tmp1_path = tmp1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
            tmp2.write(await pdf_2.read())
            tmp2_path = tmp2.name

        # Step 2: Upload both to Model_1
        doc_id_1 = upload_to_model_1(tmp1_path)
        doc_id_2 = upload_to_model_1(tmp2_path)

        # Step 3: Trigger Model_2 summarization
        analyze_with_model_2(doc_id_1)
        analyze_with_model_2(doc_id_2)

        # Step 4: Load both summaries
        summary1, summary2 = get_summaries(doc_id_1, doc_id_2)
        if not summary1 or not summary2:
            raise HTTPException(status_code=404, detail="Summary not found for one or both PDFs")

        # Step 5: Generate Plotly comparison chart
        fig = generate_comparison_chart(summary1, summary2, label1=pdf_1.filename, label2=pdf_2.filename)

        return {"status": "success", "chart": pio.to_json(fig)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# 🤖 QnA API
# ----------------------
@app.post("/ask")
async def ask_question(pdf: UploadFile = File(...), question: str = Form(...)):
    try:
        # Step 1: Save PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await pdf.read())
            tmp_path = tmp.name

        # Step 2: Upload to Model_1
        doc_id = upload_to_model_1(tmp_path)

        # Step 3: Trigger Model_2 summarization
        analyze_with_model_2(doc_id)

        # Step 4: Run QA using Model_3 logic
        answer = answer_query(doc_id, question)

        return {"status": "success", "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def upload_to_model_1(file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(MODEL_1_URL, files={"file": f})
    if response.status_code != 200:
        raise Exception("Upload to Model_1 failed")
    return response.json().get("document_id")

def analyze_with_model_2(doc_id: str):
    response = requests.post(MODEL_2_URL, json={"document_id": doc_id})
    if response.status_code != 200:
        raise Exception(f"Model_2 analysis failed for doc_id: {doc_id}")
