from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.vector_stores = {}  # pdf_id -> FAISS store

    async def add_document(self, pdf_id: str, text: str):
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create vector store for this PDF
        vector_store = FAISS.from_texts(
            chunks,
            self.embeddings
        )
        self.vector_stores[pdf_id] = vector_store

    async def get_relevant_chunks(self, pdf_id: str, query: str, k: int = 3):
        if pdf_id not in self.vector_stores:
            raise ValueError("PDF not indexed")
            
        vector_store = self.vector_stores[pdf_id]
        results = vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results] 