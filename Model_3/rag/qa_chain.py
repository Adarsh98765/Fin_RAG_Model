import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_template import get_prompt
from db.crud import get_summary

# Load LLM
llm = ChatOpenAI(
    model="llama3-70b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def answer_query(doc_id: str, user_query: str) -> str:
    summary = get_summary(doc_id)
    if not summary:
        return "❌ No summary found for the given document ID."

    prompt = get_prompt()
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"summary": summary, "question": user_query})
