# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import CSVLoader
import os 

def process_csv(file_path: str):
    print(f"Loading CSV file: {file_path}")
    #Read csv
    loader = CSVLoader(
        file_path = file_path,
        encoding = "utf-8",
        csv_args = {
            'delimiter': ','
        })
    chunk = loader.load()
    print(f"Loaded {len(chunk)} chunks")
    return chunk
    
if __name__ == "__main__":
    chunks = process_csv("../../data/raw/data.csv")
    print(chunks[0].page_content)
    