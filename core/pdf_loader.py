import fitz  # PyMuPDF
import os

def load_pdf(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        pages_content = []

        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                pages_content.append({"page_num": i + 1, "text": text})

        return {
            "filename": os.path.basename(file_path),
            "metadata": metadata,
            "pages": pages_content,
            "total_pages": len(doc)
        }
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return None
