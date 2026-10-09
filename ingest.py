# ingest.py
import os
from pathlib import Path
from dotenv import load_dotenv
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

DOCS_DIR = "./policies"
COLLECTION = "compliance_docs"

def load_pdf(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def ingest():
    texts, metadatas = [], []
    for pdf in Path(DOCS_DIR).glob("*.pdf"):
        print(f"Loading: {pdf.name}")
        content = load_pdf(str(pdf))
        texts.append(content)
        metadatas.append({"source": pdf.name, "type": "policy"})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    docs = splitter.create_documents(texts, metadatas=metadatas)
    print(f"Created {len(docs)} chunks from {len(texts)} documents")

    # Free local embedding model — no API key needed
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = QdrantVectorStore.from_documents(
        docs,
        embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION,
    )
    print(f"Ingested into Qdrant collection: {COLLECTION}")

if __name__ == "__main__":
    ingest()