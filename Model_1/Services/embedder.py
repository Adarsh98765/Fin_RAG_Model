from config import EMBEDDING_MODEL_NAME, CHROMA_PERSIST_DIR
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def store_embeddings(doc_id: str, chunks: List[str]):
    """
    Converts chunks into LangChain Document objects and stores them in ChromaDB with embeddings.

    Args:
        doc_id (str): Unique document identifier (usually file hash)
        chunks (List[str]): List of text chunks extracted from the PDF
    """
    # Wrap each chunk into a LangChain Document
    docs = [
        Document(page_content=chunk, metadata={"doc_id": doc_id})
        for chunk in chunks
    ]

    # Embed and store in ChromaDB
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=CHROMA_PERSIST_DIR
    )
    vectordb.persist()
