import datetime
import os
import hashlib
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_openai import OpenAIEmbeddings
# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStoreManager:
    def __init__(self, persist_directory="./chroma_db", embedding_type="huggingface"):
        self.persist_directory = persist_directory

        # Set up embeddings
        if embedding_type == "openai":
            self.embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
            print("Currently use OpenAI Embeddings.")
        else:
            model_name = "BAAI/bge-m3"
            self.embeddings = HuggingFaceEmbeddings(model_name = model_name)
            print(f"Currently use HuggingFace Embeddings {model_name}.")
        
        # Create Chroma
        self.vector_store = Chroma(
            collection_name = "internal_docs",
            embedding_function = self.embeddings,
            persist_directory = self.persist_directory
        )
    
    def add_documents_to_db(self, chunks):
        print(f"Start encoding and save to Vector DB.")

        # Tạo ID dựa trên nội dung để chống trùng lặp
        ids = []
        for chunk in chunks:
            content_hash = hashlib.md5(chunk.page_content.encode()).hexdigest()
            source = chunk.metadata.get('source', 'unknown')
            page = chunk.metadata.get('page', 0)
            doc_id = f"{source}_p{page}_{content_hash[:12]}"
            ids.append(doc_id)

        self.vector_store.add_documents(chunks, ids=ids)
        print(f"Save successful: {len(chunks)} chunks to {self.persist_directory}")
    
    def search_similar_documents(self, query: str, k: int = 4):
        # Search K documents regarding prompt
        result = self.vector_store.similarity_search(query, k = k)
        return result

    def get_all_sources(self):
        """Lấy danh sách tất cả file nguồn đã upload"""
        collection = self.vector_store._collection
        result = collection.get(include=["metadatas"])
        sources = set()
        for meta in result["metadatas"]:
            if meta and "source" in meta:
                sources.add(meta["source"])
        return sorted(list(sources))

    def delete_by_source(self, source_name: str):
        """Xóa tất cả chunks thuộc một file nguồn"""
        collection = self.vector_store._collection
        collection.delete(where={"source": source_name})
        print(f"Deleted all chunks from: {source_name}")