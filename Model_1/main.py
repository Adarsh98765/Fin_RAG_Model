from fastapi import FastAPI, UploadFile, File
from Model_1.Services.extractor import extract_chunks_from_pdf
from Model_1.Services.embedder import store_embeddings
from Model_1.db.crud import is_file_processed, save_file_metadata

import hashlib
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Model 1 API is running."}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    file_hash = hashlib.md5(contents).hexdigest()

    if is_file_processed(file_hash):
        return {"status": "exists", "document_id": file_hash}

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    try:
        chunks = extract_chunks_from_pdf(temp_path)
        if not chunks:
            return {"status": "error", "message": "No table data found in the PDF."}
        store_embeddings(file_hash, chunks)
        save_file_metadata(file_hash, file.filename)
        return {"status": "success", "document_id": file_hash}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
