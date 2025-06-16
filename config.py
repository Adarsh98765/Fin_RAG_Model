import os
from dotenv import load_dotenv
load_dotenv()

#M_1_Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

#Vector db
CHROMA_PERSIST_DIR = "./chroma_store"

# Database 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./files.db")  # fallback if not set

#API Keys 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
