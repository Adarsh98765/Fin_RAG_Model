import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from Model_3.db.crud import get_summary, get_graph_data

load_dotenv()

# 🧠 Prompt Template for RAG QnA with memory
QA_TEMPLATE = """
You are a financial analyst AI assistant.

Your task is to answer the user's question based on the provided summary, financial metrics, and the ongoing conversation.
Be precise and helpful. Include insights or analysis if relevant.

---

📄 Summary:
{summary}

📊 Financial Metrics:
{graph_data}

💬 Conversation so far:
{chat_history}

❓ Current Question:
{question}

💬 Answer:
"""

def get_prompt():
    return PromptTemplate(
        input_variables=["summary", "graph_data", "chat_history", "question"],
        template=QA_TEMPLATE.strip()
    )

def build_graph_text(graph_data: list[dict]) -> str:
    """
    Converts structured financial metrics into readable text.
    """
    if not graph_data:
        return "Graph data not available."

    lines = [
        f"{item['metric_name']} = {item['value']}" + 
        (f". Notes: {item['notes']}" if item.get("notes") else "")
        for item in graph_data
    ]
    return "\n".join(lines)

def build_chat_history(chat_history: list[dict]) -> str:
    """
    Formats the past chat into a readable history block.
    """
    if not chat_history:
        return "No previous conversation."

    return "\n".join([
        f"User: {turn['user']}\nAssistant: {turn['bot']}"
        for turn in chat_history
    ])

def answer_query(doc_id: str, question: str, chat_history: list[dict]) -> str:
    """
    Builds a memory-aware prompt using summary, financials, past conversation, and current question.
    """
    summary = get_summary(doc_id)
    graph_data = get_graph_data(doc_id)

    if not summary:
        return "❌ No summary found for the given document ID."

    graph_text = build_graph_text(graph_data)
    history_text = build_chat_history(chat_history)

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
        "chat_history": history_text,
        "question": question
    })
