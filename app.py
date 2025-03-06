import streamlit as st
from agents.query_agent import QueryAgent
from agents.summarization_agent import SummarizationAgent
from utils.memory_store import ConversationMemory
from utils.document_loader import DocumentLoader
from utils.vector_store import VectorStore
import traceback
from datetime import datetime, timezone

# Constants
DOCUMENT_PATHS = {
    "Guide to Litigation in India": "data/guide_to_litigation_india.pdf",
    "Legal Compliance & Corporate Laws": "data/legal_compliance_corporate_laws.pdf"
}

def get_current_utc():
    """Get current UTC time in specified format"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def initialize_session_state():
    """Initialize session state variables"""
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'query_agent' not in st.session_state:
        st.session_state.query_agent = None
    if 'summarization_agent' not in st.session_state:
        st.session_state.summarization_agent = None
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def validate_api_key(api_key):
    """Simple validation of API key format"""
    if not api_key:
        return False
    # Basic check for Gemini API key format
    return api_key.startswith('AI') and len(api_key) > 10

def load_default_documents():
    """Load the default legal documents from the data folder"""
    loader = DocumentLoader()
    documents = []
    
    for doc_name, doc_path in DOCUMENT_PATHS.items():
        try:
            doc = loader.load_local_document(doc_path, doc_name)
            if doc:  # Only add if document contains valid content
                documents.extend(doc)
                st.sidebar.success(f"Successfully loaded: {doc_name}")
        except FileNotFoundError:
            st.error(f"Document not found: {doc_name}")
            return None
        except ValueError as e:
            st.error(f"Error processing {doc_name}: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error processing {doc_name}: {str(e)}")
            return None
    
    if not documents:
        st.error("No valid documents were loaded. Please check the document files.")
        return None
        
    return documents

def main():
    st.title("Legal Information Multi-Agent Chatbot")
    
    initialize_session_state()
    
    # Sidebar for API key and info
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey",
            key="api_key_input"
        )
        
        if api_key:
            if validate_api_key(api_key):
                st.session_state.api_key = api_key
                st.success("API Key validated!")
            else:
                st.error("Invalid API Key format. Please check your key.")
        
        st.divider()
        
        # Session Info
        st.header("Session Info")
        st.markdown(f"""
        - **User**: {st.session_state.get('user', 'srikrishnavansi')}
        - **Date**: {get_current_utc()} UTC
        """)
        
        st.divider()
        
        # Available Documents
        st.header("Available Legal Documents")
        st.write("1. Guide to Litigation in India")
        st.write("2. Legal Compliance & Corporate Laws by ICAI")
        
        # Document Status
        if st.session_state.documents_loaded:
            st.success("Documents loaded and ready!")
        
        # Load Documents Button
        if not st.session_state.documents_loaded:
            if st.button("Load Documents"):
                if not st.session_state.api_key:
                    st.error("Please enter your API key first!")
                else:
                    with st.spinner("Loading legal documents..."):
                        try:
                            documents = load_default_documents()
                            if documents:
                                # Initialize vector store with API key
                                vector_store = VectorStore(st.session_state.api_key)
                                vector_store.add_documents(documents)
                                st.session_state.vector_store = vector_store
                                
                                # Initialize agents with API key
                                st.session_state.query_agent = QueryAgent(vector_store, st.session_state.api_key)
                                st.session_state.summarization_agent = SummarizationAgent(st.session_state.api_key)
                                
                                st.session_state.documents_loaded = True
                                st.success("Legal documents loaded successfully!")
                        except Exception as e:
                            st.error(f"Error initializing the system: {str(e)}")
                            st.error(f"Stack trace: {traceback.format_exc()}")

    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know about legal matters?"):
        if not st.session_state.api_key:
            st.error("Please enter your API key in the sidebar first!")
            return
            
        if not st.session_state.documents_loaded:
            st.error("Please load the legal documents first!")
            return

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the query
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Query Agent processes the request
                    relevant_info = st.session_state.query_agent.process_query(prompt)
                    
                    # Summarization Agent creates the response
                    response = st.session_state.summarization_agent.summarize(
                        prompt,
                        relevant_info,
                        st.session_state.memory.get_context()
                    )
                    
                    # Store the interaction in memory
                    st.session_state.memory.add_interaction(prompt, response)
                    
                    # Display response
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"Error processing your request: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()