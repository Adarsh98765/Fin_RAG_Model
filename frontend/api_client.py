import requests

MODEL_3_URL = "http://localhost:8003/compare"

def compare_pdfs(file1, file2):
    files = {
        "pdf_1": ("file1.pdf", file1, "application/pdf"),
        "pdf_2": ("file2.pdf", file2, "application/pdf")
    }
    response = requests.post(MODEL_3_URL, files=files)
    if response.status_code == 200:
        return response.json()["chart"]
    else:
        raise Exception(f"Model_3 API error: {response.status_code} - {response.text}")
