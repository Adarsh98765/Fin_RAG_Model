import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from Model_3.db.crud import get_summary, get_graph_data  # ✅ Added get_graph_data

load_dotenv()

QA_TEMPLATE = """
You are a financial analyst AI assistant.

Your task is to answer the user's question **only** based on the provided summary and financial metrics.
Be precise and helpful. Include insights or analysis if relevant.

---

📄 Summary:
{summary}

📊 Financial Metrics:
{graph_data}

❓ User Question:
{question}

💬 Answer:
"""

def get_prompt():
    return PromptTemplate(
        input_variables=["summary", "graph_data", "question"],
        template=QA_TEMPLATE.strip()
    )

def build_graph_text(graph_data: list[dict]) -> str:
    if not graph_data:
        return "Graph data not available."

    lines = [
        f"{item['company_name']} has {item['metric_name']} = {item['value']}"
        for item in graph_data
    ]
    return "\n".join(lines)

def answer_query(doc_id: str, question: str) -> str:
    summary = get_summary(doc_id)
    graph_data = get_graph_data(doc_id)
    
    if not summary:
        return "❌ No summary found for the given document ID."

    graph_text = build_graph_text(graph_data)
    
    prompt = get_prompt()
    llm = ChatOpenAI(
        model="llama3-70b-8192",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "summary": summary,
        "graph_data": graph_text,
        "question": question
    })
