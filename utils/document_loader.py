from PyPDF2 import PdfReader
from langchain.docstore.document import Document
import io

class DocumentLoader:
    def __init__(self):
        pass
    
    def clean_text(self, text):
        """Clean and validate the extracted text"""
        if not text or not text.strip():
            return None
        # Remove excessive whitespace
        text = " ".join(text.split())
        return text
    
    def load_local_document(self, file_path, doc_name):
        """Load a document from local file system"""
        documents = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Clean and validate the text
                cleaned_text = self.clean_text(text)
                
                if cleaned_text:  # Only create document if text is not empty
                    # Create Document object
                    doc = Document(
                        page_content=cleaned_text,
                        metadata={
                            "source": doc_name,
                            "page": page_num + 1
                        }
                    )
                    documents.append(doc)
        print(documents)
        if not documents:
            raise ValueError(f"No valid text content found in document: {doc_name}")
        
        return documents