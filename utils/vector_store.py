import chromadb
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class VectorStore:
    def __init__(self, api_key):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model="models/embedding-001"
        )
        self.vector_store = None
    
    def add_documents(self, documents):
        """Add documents to the vector store"""
        if not documents:
            raise ValueError("No documents provided for embedding")
        
        # Filter out any documents with empty content
        valid_documents = [doc for doc in documents if doc.page_content.strip()]
        
        if not valid_documents:
            raise ValueError("No valid documents found with content")
        
        self.vector_store = Chroma.from_documents(
            documents=valid_documents,
            embedding=self.embeddings
        )
    
    def similarity_search(self, query, k=3):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        return self.vector_store.similarity_search(query, k=k)