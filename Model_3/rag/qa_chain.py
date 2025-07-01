import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from Model_3.db.crud import get_summary

load_dotenv()

QA_TEMPLATE = """
You are a financial analyst AI assistant.

Your task is to answer the user's question **only** based on the provided summary.
Be precise and helpful. Include insights or analysis if relevant.

---

📄 Summary:
{summary}

❓ User Question:
{question}

💬 Answer:
"""

def get_prompt():
    return PromptTemplate(
        input_variables=["summary", "question"],
        template=QA_TEMPLATE.strip()
    )

def answer_query(doc_id: str, question: str) -> str:
    summary = get_summary(doc_id)
    if not summary:
        return "❌ No summary found for the given document ID."

    prompt = get_prompt()
    llm = ChatOpenAI(
        model="llama3-70b-8192",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"summary": summary, "question": question})
