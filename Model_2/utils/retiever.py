from typing import List
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL_NAME

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def retrieve_chunks(doc_id: str, query: str = "financial analysis", top_k: int = 100) -> List[str]:
    """
    Retrieves the most relevant chunks for a given document ID from ChromaDB.

    Applies keyword-based filtering to prioritize financial data.

    Args:
        doc_id (str): The unique document identifier.
        query (str): Search query to guide similarity search.
        top_k (int): Number of top results to retrieve.

    Returns:
        List[str]: A list of relevant chunk strings.
    """
    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embedding_model
    )
    results = vectordb.similarity_search(query=query, k=top_k, filter={"doc_id": doc_id})

    keywords = ["revenue", "profit", "loss", "assets", "liabilities", "EPS", "cash", "debt", "equity", "expense"]
    filtered_chunks = [doc.page_content for doc in results if any(kw.lower() in doc.page_content.lower() for kw in keywords)]

    return filtered_chunks if filtered_chunks else [doc.page_content for doc in results]
