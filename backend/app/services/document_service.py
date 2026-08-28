import os
import pymupdf
from docx import Document


def extract_pdf_text(file_path):

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()
        text += "\n"

    document.close()

    return text.strip()


def extract_docx_text(file_path):

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text += paragraph.text
            text += "\n"

    return text.strip()


def extract_txt_text(file_path):

    with open(file_path, "r", encoding="utf-8") as file:

        return file.read().strip()


def extract_text_from_file(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        return extract_pdf_text(file_path)

    elif extension == ".docx":

        return extract_docx_text(file_path)

    elif extension == ".txt":

        return extract_txt_text(file_path)

    else:

        raise ValueError(
            "Only PDF, DOCX and TXT files are supported."
        )