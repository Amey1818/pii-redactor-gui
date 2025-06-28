import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    doc = fitz.open(filepath)
    texts = [page.get_text() for page in doc]
    return texts, doc
