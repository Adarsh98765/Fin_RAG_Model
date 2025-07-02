from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import tempfile, requests

from Model_3.rag.qa_chain import answer_query

app = FastAPI()

# Model service URLs
MODEL_1_URL = "http://localhost:8001/upload_pdf/"
MODEL_2_URL = "http://localhost:8002/analyze_pdf/"

@app.get("/")
def root():
    return {"message": "Model 3 API is running."}

@app.post("/ask")
async def ask_question(
    pdf: UploadFile = File(...),
    question: str = Form(...)
):
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

        return {
            "status": "success",
            "document_id": doc_id,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def upload_to_model_1(file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(MODEL_1_URL, files={"file": f})

    if response.status_code != 200:
        raise Exception(f"Upload to Model_1 failed: {response.status_code} - {response.text}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Could not parse JSON from Model_1: {e} - {response.text}")

    if "document_id" not in data:
        raise Exception(f"No document_id in response: {data}")

    return data["document_id"]


def analyze_with_model_2(doc_id: str):
    response = requests.post(MODEL_2_URL, json={"document_id": doc_id})
    if response.status_code != 200:
        raise Exception(f"Model_2 analysis failed: {response.status_code} - {response.text}")
