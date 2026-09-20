from pathlib import Path

from pypdf import PdfReader
import chromadb

from backend.rag.embeddings import embedding_function


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

CHROMA_PATH = BASE_DIR / "chroma_db"


# ============================================================
# CHROMADB CLIENT
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


collection = client.get_or_create_collection(
    name="industrial_maintenance",
    metadata={
        "description": (
            "Industrial maintenance knowledge base"
        )
    },
    embedding_function=embedding_function
)


# ============================================================
# EXTRACT TEXT FROM PDF
# ============================================================

def extract_pdf_text(pdf_path: Path):

    reader = PdfReader(
        str(pdf_path)
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        try:

            text = page.extract_text()

        except Exception as error:

            print(
                f"Could not read page "
                f"{page_number}: {error}"
            )

            continue

        if text:

            text = text.strip()

            if text:

                pages.append(
                    {
                        "page": page_number,
                        "text": text
                    }
                )

    return pages


# ============================================================
# SPLIT TEXT INTO CHUNKS
# ============================================================

def split_text(
    text,
    chunk_size=800,
    overlap=150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks


# ============================================================
# INGEST ONE PDF
# ============================================================

def ingest_pdf(pdf_path: Path):

    print()
    print("=" * 60)

    print(
        f"Processing: {pdf_path.name}"
    )

    print(
        f"Category: {pdf_path.parent.name}"
    )

    print("=" * 60)

    pages = extract_pdf_text(
        pdf_path
    )

    if not pages:

        print(
            "No readable text found."
        )

        return 0

    all_chunks = []

    all_metadata = []

    all_ids = []

    chunk_counter = 0

    category = pdf_path.parent.name

    for page_data in pages:

        page_number = page_data[
            "page"
        ]

        text = page_data[
            "text"
        ]

        chunks = split_text(
            text
        )

        for chunk in chunks:

            chunk_id = (
                f"{pdf_path.stem}_"
                f"page_{page_number}_"
                f"chunk_{chunk_counter}"
            )

            all_chunks.append(
                chunk
            )

            all_metadata.append(
                {
                    "source": pdf_path.name,
                    "page": page_number,
                    "category": category
                }
            )

            all_ids.append(
                chunk_id
            )

            chunk_counter += 1

    if not all_chunks:

        print(
            "No chunks were generated."
        )

        return 0

    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        metadatas=all_metadata
    )

    print(
        f"Pages extracted: {len(pages)}"
    )

    print(
        f"Chunks added: {len(all_chunks)}"
    )

    return len(all_chunks)


# ============================================================
# INGEST ALL PDF FILES
# ============================================================

def ingest_all_pdfs():

    pdf_files = list(
        KNOWLEDGE_BASE.rglob(
            "*.pdf"
        )
    )

    print()
    print("=" * 60)
    print(
        "INDUSTRIAL MAINTENANCE RAG"
    )
    print(
        "KNOWLEDGE BASE INGESTION"
    )
    print("=" * 60)

    print(
        f"PDF files found: {len(pdf_files)}"
    )

    if not pdf_files:

        print(
            "ERROR: No PDF files found."
        )

        return

    total_chunks = 0

    successful_files = 0

    failed_files = 0

    for pdf_file in pdf_files:

        try:

            chunks = ingest_pdf(
                pdf_file
            )

            if chunks > 0:

                successful_files += 1

                total_chunks += chunks

            else:

                failed_files += 1

        except Exception as error:

            failed_files += 1

            print()
            print(
                f"ERROR processing "
                f"{pdf_file.name}"
            )

            print(error)

    print()
    print("=" * 60)
    print(
        "RAG INGESTION COMPLETE"
    )
    print("=" * 60)

    print(
        f"Total PDFs found: {len(pdf_files)}"
    )

    print(
        f"Successfully processed: "
        f"{successful_files}"
    )

    print(
        f"Failed: {failed_files}"
    )

    print(
        f"Total chunks: {total_chunks}"
    )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    ingest_all_pdfs()