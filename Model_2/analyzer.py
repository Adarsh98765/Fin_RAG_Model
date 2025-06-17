import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL_NAME

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# Load vector store chunks filtered by doc_id
def load_chunks_for_doc(doc_id: str) -> List[str]:
    vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embedding_model)
    all_docs = vectordb.similarity_search(query="financial analysis", k=100, filter={"doc_id": doc_id})

    # Keyword-based filtering (optional enhancement)
    keywords = ["revenue", "profit", "loss", "assets", "liabilities", "EPS", "cash", "debt", "equity", "expense"]
    filtered_chunks = [doc.page_content for doc in all_docs if any(kw.lower() in doc.page_content.lower() for kw in keywords)]

    return filtered_chunks or [doc.page_content for doc in all_docs]  # fallback to all if filter is empty

# CoT Prompt Template
COT_TEMPLATE = """
You are a senior financial analyst AI assistant.

Your task is to read raw extracted financial data and convert it into a highly compressed, investment-focused set of insights.

Think step-by-step like a professional analyst. Follow these instructions strictly:

---

Step 1: Carefully extract **only the most essential financial metrics** for performance and valuation. Prioritize:
- Revenue from operations
- Net profit / PAT
- EPS (basic and diluted)
- EBITDA and EBIT margins
- ROE and ROCE
- Total debt and debt/equity ratio
- Cash flow from operations
- Current ratio / liquidity ratios
- P/E ratio or valuation-relevant metrics

Step 2: Identify **YoY or QoQ trends** for the above metrics. Avoid copying entire tables. Pick key periods only (e.g., FY22 vs FY23).

Step 3: Discard non-essential or repetitive text. Avoid MD&A, segment-level noise, or CEO statements. Compress wherever possible.

Step 4: Structure the output in the following format (plain text, no markdown):

Metric: <Metric Name>  
Period: <e.g., FY23 or Q3 FY24>  
Value: <e.g., ₹123 Cr, 15.2%, etc.>  
Notes: <Optional insight if significant>

---

Your final output should be concise, stripped of all filler, and ready for downstream visualization or chatbot-based analysis.

Here is the raw extracted financial data:

{content}

Begin your step-by-step extraction now:

DO NOT repeat the instructions. Begin directly with extracted metrics.

"""

# Function to run CoT-style analysis
def analyze_document(doc_id: str) -> str:
    chunks = load_chunks_for_doc(doc_id)
    limited_content = "\n\n".join(chunks[:100])  # token-safe (basic truncation)

    prompt = PromptTemplate.from_template(COT_TEMPLATE)
    llm = ChatOpenAI(model="llama3-70b-8192", base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"content": limited_content})
