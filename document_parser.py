import fitz  # PyMuPDF
from docx import Document
from pathlib import Path


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    document = fitz.open(file_path)

    text = []

    for page in document:
        page_text = page.get_text()
        if page_text.strip():
            text.append(page_text)

    document.close()

    return "\n".join(text)


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_text(file_path):
    """Extract text from PDF or DOCX."""

    file_extension = Path(file_path).suffix.lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX file."
        )