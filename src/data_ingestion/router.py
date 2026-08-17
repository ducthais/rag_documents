import os
from .pdf_parser import process_pdf
from .csv_parser import process_csv

def ingest_documents(file_path: str):
    if not os.path.exists(file_path):
        return FileNotFoundError(f"File not found: {file_path}")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        return process_pdf(file_path)
    elif file_extension.lower() == ".csv":
        return process_csv(file_path)
    else:
        return ValueError(f"Unsupported file type: {file_extension}")
