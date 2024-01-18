
from docx import Document
import fitz # Here's the link to the license of the library: https://www.gnu.org/licenses/agpl-3.0.html
from io import BytesIO
import pandas as pd
import json
import streamlit as st


def read_docx(file):
    with BytesIO(file.read()) as doc_file:
        document = Document(doc_file)
        result = "\n".join([para.text for para in document.paragraphs])
        return result
def text_from_pdf_file(pdf_file):
    # Limitations:  Only works for PDFs with text, not images.
    # Can't properly processing footers and headers.
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text

def text_from_pdf_file_path(pdf_file_path):
    # Limitations: Only works for PDFs with text, not scanned images.
    # Might not properly process footers and headers.
    with fitz.open(pdf_file_path) as doc:  # Use the file path directly
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            report = text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            report = read_docx(uploaded_file)
        elif uploaded_file.type == 'text/plain':
            # Decode the byte content to string
            report = str(uploaded_file.read(), 'utf-8')
        return uploaded_file.name, report
    else:
        return None, None