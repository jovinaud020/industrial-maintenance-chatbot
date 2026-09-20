from pathlib import Path
import hashlib

import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.embeddings import embedding_function

BASE_DIR = Path(__file__).resolve().parents[2]
PDF_PATH = BASE_DIR / "knowledge_base" / "motors" / "Electric Motors and Drives.pdf"
CHROMA_PATH = BASE_DIR / "chroma_db"

def make_id(source, page, chunk_index, text):
    raw = f"{source}|{page}|{chunk_index}|{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def main():
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
        return

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_collection(name="industrial_maintenance")

    reader = PdfReader(str(PDF_PATH))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    documents, metadatas, ids = [], [], []
    source = PDF_PATH.name

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue

        for chunk_index, chunk in enumerate(splitter.split_text(text)):
            chunk = chunk.strip()
            if not chunk:
                continue

            documents.append(chunk)
            metadatas.append({
                "source": source,
                "page": page_number,
                "category": "motors",
            })
            ids.append(make_id(source, page_number, chunk_index, chunk))

    print(f"Prepared {len(documents)} chunks.")

    for start in range(0, len(documents), 64):
        end = start + 64
        embeddings = embedding_function.embed_documents(documents[start:end])
        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            embeddings=embeddings,
        )
        print(f"Processed {min(end, len(documents))}/{len(documents)} chunks")

    print("\nSUCCESS")
    print(f"Pages read: {len(reader.pages)}")
    print(f"Chunks added/updated: {len(documents)}")
    print(f"Collection total: {collection.count()}")
    print("Existing ChromaDB was preserved.")
    print("The original 11 PDFs were NOT re-ingested.")

if __name__ == "__main__":
    main()
