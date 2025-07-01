from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import tempfile, requests
import plotly.io as pio

#from Model_3.graph.plot_generator import generate_comparison_chart
from Model_3.db.crud import get_summaries
from Model_3.rag.qa_chain import answer_query

app = FastAPI()

MODEL_1_URL = "http://localhost:8001/upload_pdf/"
MODEL_2_URL = "http://localhost:8002/analyze_pdf/"

@app.get("/")
def root():
    return {"message": "Model 3 API is running."}


@app.post("/default_graphs/")
def generate_default_graphs(doc_id: str):
    graph_data = get_graph_data(doc_id)
    if not graph_data:
        raise HTTPException(status_code=404, detail="No graph data found for this document.")

    fig = generate_graphs_from_text(graph_data)  # you'll define this in plot_generator
    return {"chart": fig.to_json()}

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
