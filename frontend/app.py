import streamlit as st
import requests

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="FinRAG Dashboard", layout="wide")
st.title("📊 Financial Report Analyzer")

st.subheader("Upload Financial PDF and Ask")

pdf = st.file_uploader("Upload PDF", type="pdf", key="qa_pdf")
question = st.text_input("Ask a question about this company's financials:")

if st.button("💬 Ask"):
    if pdf and question.strip():
        with st.spinner("Analyzing and generating answer..."):
            files = {"pdf": pdf}
            data = {"question": question}
            response = requests.post(
                f"{BACKEND_URL}/ask",
                files=files,
                data=data
            )
            if response.status_code == 200:
                st.success("Answer:")
                st.write(response.json()["answer"])
            else:
                st.error("Question answering failed: " + response.text)
    else:
        st.warning("Please upload a PDF and enter a question.")
