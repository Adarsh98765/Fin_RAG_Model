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

# Load chunks filtered by doc_id
def load_chunks_for_doc(doc_id: str) -> List[str]:
    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embedding_model
    )
    docs = vectordb.similarity_search(
        query="financial analysis",
        k=100,
        filter={"doc_id": doc_id}
    )
    return [doc.page_content for doc in docs]

# ------------------ TEMPLATES ------------------

SUMMARY_TEMPLATE = """
You are a senior financial analyst AI assistant.

Your job is to generate a highly compressed investment-oriented financial summary using raw extracted data from a company's report.

📌 Follow these strict steps:

Step 1️⃣: Extract **essential core metrics**:
- Revenue from operations
- EBITDA
- Net profit / PAT
- EPS (basic or diluted)
- ROE, ROCE
- Total debt, debt/equity ratio
- Cash flow from operations
- Current ratio
- Valuation metrics (P/E, EV/EBITDA if available)

Step 2️⃣: Include only key YoY or QoQ comparisons (e.g., FY23 vs FY22).

Step 3️⃣: Compress aggressively. Ignore management commentary, MD&A, and unnecessary details.

Step 4️⃣: Use this format (plain text, no markdown):

Metric: <Name>  
Period: <e.g., FY23 or Q3 FY24>  
Value: <e.g., ₹123 Cr or 15.2%>  
Notes: <Optional insight if meaningful>

Here is the financial text:

{content}

DO NOT repeat instructions. Start directly with extracted metrics.
"""

GRAPH_TEMPLATE = """
You are a financial analyst AI.

Your task is to extract **only reliable, numeric values** from raw financial report data to generate the following 7 critical investment graphs:

1️⃣ Revenue Trend → Net Sales or Operating Revenue  
2️⃣ EBITDA & EBITDA Margin → Both values  
3️⃣ Net Profit Trend → PAT  
4️⃣ EPS Trend → Earnings Per Share  
5️⃣ Operating Expense Split → Raw Material, Employee, Other Expenses  
6️⃣ Cash Balance Trend → Cash & Cash Equivalents  
7️⃣ Debt Profile → Finance Costs, Debt/Equity Ratio

📌 Very Important:
- ❌ Do NOT include any metric if the value is missing or cannot be confidently extracted.
- ❌ Do NOT return "Not available" or "Not possible to extract".
- ✅ Only include metrics where a number is clearly present (e.g., ₹123 Cr, 15.2%, ₹20.61).

🧠 Format for each metric:
Metric: <Name>  
Period: <e.g., FY22, Q3 FY24>  
Value: <e.g., ₹300 Cr or 12%>  
Notes: <Optional insight, derived remark, or comparison>

Here is the financial content:

{content}

Start now. Do not repeat instructions.
"""

# ------------------ LLM CALLS ------------------

def analyze_document_summary(doc_id: str) -> str:
    chunks = load_chunks_for_doc(doc_id)
    content = "\n\n".join(chunks[:100])

    prompt = PromptTemplate.from_template(SUMMARY_TEMPLATE)
    llm = ChatOpenAI(
        model="llama3-70b-8192",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"content": content})

def analyze_graph_metrics(doc_id: str) -> list[dict]:
    chunks = load_chunks_for_doc(doc_id)
    content = "\n\n".join(chunks[:100])

    prompt = PromptTemplate.from_template(GRAPH_TEMPLATE)
    llm = ChatOpenAI(
        model="llama3-70b-8192",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"content": content})

    # Parse the plain text into structured list of dicts
    parsed = []
    for block in result.strip().split("\n\n"):
        metric, period, value, notes = None, None, None, None
        for line in block.splitlines():
            if line.lower().startswith("metric:"):
                metric = line.split(":", 1)[1].strip()
            elif line.lower().startswith("period:"):
                period = line.split(":", 1)[1].strip()
            elif line.lower().startswith("value:"):
                value = line.split(":", 1)[1].strip()
            elif line.lower().startswith("notes:"):
                notes = line.split(":", 1)[1].strip()

        if metric and value:
            parsed.append({
                "metric_name": f"{metric} ({period})" if period else metric,
                "value": value,
                "notes": notes or ""
            })

    return parsed
