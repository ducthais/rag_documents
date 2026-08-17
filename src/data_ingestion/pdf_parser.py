# pyrefly: ignore [missing-import]
from langchain_community.document_loaders  import PyPDFLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

#Read pdf and split to chunk
def process_pdf(file_path: str):
    print(f"Loading PDF file: {file_path}")
    # Read pdf
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split to chunk
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size = 1000, # max char
        chunk_overlap = 200, # context memory
        separators=["\n\n", "\n", ".", " "] # firt to split
    )

    chunks = text_spliter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

if __name__ == "__main__":
    # Test
    chunks = process_pdf(r"..\..\data\raw\promt.pdf")
    print(chunks[0].page_content)

