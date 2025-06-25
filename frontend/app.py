import streamlit as st
import requests
import json
import plotly.graph_objects as go

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="FinRAG Dashboard", layout="wide")
st.title("📊 Financial Report Analyzer")

mode = st.radio("Select Mode", ["Compare Two Companies", "Ask a Question"])

# ------------------------
# Mode 1: Compare
# ------------------------
if mode == "Compare Two Companies":
    st.subheader("Upload Two Financial PDFs")

    col1, col2 = st.columns(2)
    with col1:
        pdf_1 = st.file_uploader("Company 1 PDF", type="pdf", key="pdf1")
    with col2:
        pdf_2 = st.file_uploader("Company 2 PDF", type="pdf", key="pdf2")

    if st.button("🔍 Compare"):
        if pdf_1 and pdf_2:
            with st.spinner("Processing and comparing..."):
                files = {"pdf_1": pdf_1, "pdf_2": pdf_2}
                response = requests.post(f"{BACKEND_URL}/compare", files=files)

                if response.status_code == 200:
                    chart_json = response.json()["chart"]
                    fig = go.Figure(json.loads(chart_json))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Comparison failed: " + response.text)
        else:
            st.warning("Please upload two PDFs first.")

# ------------------------
# Mode 2: Ask a Question
# ------------------------
elif mode == "Ask a Question":
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
                    data=data  # send question as form field
                )
                if response.status_code == 200:
                    st.success("Answer:")
                    st.write(response.json()["answer"])
                else:
                    st.error("Question answering failed: " + response.text)
        else:
            st.warning("Please upload a PDF and enter a question.")
