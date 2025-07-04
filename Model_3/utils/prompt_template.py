from langchain_core.prompts import PromptTemplate

QA_TEMPLATE = """
You are a financial analyst AI assistant.

Your job is to answer user questions based **only** on the provided financial summary.
Do not make assumptions. If the answer isn't in the summary, say you don't know.

Use the ongoing conversation to understand the user's intent better.

---

📄 Summary:
{summary}

💬 Conversation so far:
{chat_history}

❓ Current Question:
{question}

💬 Answer:
"""

def get_prompt():
    return PromptTemplate(
        input_variables=["summary", "chat_history", "question"],
        template=QA_TEMPLATE.strip()
    )
