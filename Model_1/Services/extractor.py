import camelot
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_chunks_from_pdf(file_path: str) -> list:
    try:
        tables = camelot.read_pdf(file_path, pages="all", flavor="lattice")
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)
        chunks = []

        for table in tables:
            text = table.df.to_string(index=False)
            split_chunks = splitter.split_text(text)
            chunks.extend(split_chunks)

        return chunks

    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {e}")
