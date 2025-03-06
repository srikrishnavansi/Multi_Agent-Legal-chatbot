# Legal Information Multi-Agent Chatbot: Technical Architecture 🤖⚖️

A sophisticated multi-agent system for legal information retrieval and processing, built with LangChain and Gemini API.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.0-orange.svg)
![FAISS](https://img.shields.io/badge/FAISS-1.7.4-purple.svg)
![Last Updated](https://img.shields.io/badge/last%20updated-2025--03--06-green.svg)

## Core Architecture

```mermaid
graph TB
    subgraph User_Interface
        UI[Streamlit Interface]
        API[API Key Management]
        DOCS[Document Management]
    end

    subgraph Document_Processing
        DL[Document Loader]
        TE[Text Extraction]
        CH[Content Handler]
    end

    subgraph Vector_Operations
        EMB[Gemini Embeddings]
        VS[FAISS Vector Store]
        SIM[Similarity Search]
    end

    subgraph Agent_System
        QA[Query Agent]
        SA[Summarization Agent]
        MEM[Memory Store]
    end

    UI --> API
    UI --> DOCS
    DOCS --> DL
    DL --> TE
    TE --> CH
    CH --> EMB
    EMB --> VS
    VS --> SIM
    SIM --> QA
    QA --> SA
    SA --> MEM
    MEM --> SA
```

## Technical Components

### 1. Vector Store Implementation
```python
class VectorStore:
    def __init__(self, api_key):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model="models/embedding-001"
        )
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
```

### 2. Information Flow Architecture

```mermaid
sequenceDiagram
    participant UI as Interface
    participant DL as DocLoader
    participant VS as VectorStore
    participant QA as QueryAgent
    participant SA as SumAgent
    participant MEM as Memory

    UI->>DL: Load Document
    DL->>VS: Process & Embed
    UI->>QA: Query
    QA->>VS: Search
    VS-->>QA: Relevant Docs
    QA->>SA: Context
    SA->>MEM: Get History
    MEM-->>SA: Context
    SA-->>UI: Response
```

## Core Technical Approaches

### 1. Document Processing Pipeline

```mermaid
flowchart LR
    A[PDF Input] -->|PyPDF2| B[Text Extraction]
    B -->|Clean & Validate| C[Text Chunks]
    C -->|Gemini API| D[Embeddings]
    D -->|FAISS| E[Vector DB]
    E -->|Similarity Search| F[Query Results]
```

### 2. Agent Communication System

```mermaid
graph TD
    A[User Query] -->|Process| B[Query Agent]
    B -->|Vector Search| C{FAISS Store}
    C -->|Retrieved Docs| D[Context]
    D -->|Format| E[Summarization Agent]
    E -->|Check| F{Memory Store}
    F -->|Get Context| E
    E -->|Generate| G[Response]
```

## Technical Specifications

### Document Processing
- **Chunk Size**: 1000 tokens
- **Overlap**: 200 tokens
- **Embedding Dimension**: 768
- **Similarity Metric**: Cosine Similarity

```python
# Example Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_DIM = 768
```

### Vector Store Configuration
```python
# FAISS Index Configuration
index = faiss.IndexFlatIP(EMBEDDING_DIM)
index.train(embeddings)
```

### Memory Management
```python
class ConversationMemory:
    def __init__(self):
        self.buffer_size = 10
        self.context_window = 5
        self.conversations = []
```

## Performance Optimizations

### 1. Caching System
```mermaid
flowchart TB
    A[Query] -->|Hash| B{Cache Check}
    B -->|Hit| C[Return Cached]
    B -->|Miss| D[Process New]
    D -->|Store| E[Cache]
    C -->F[Response]
    E -->F
```

### 2. Query Processing Pipeline
```python
@st.cache_data(ttl=3600)
def process_query(query, context):
    # Query processing logic
    pass
```

## System Requirements

```text name=requirements.txt
streamlit>=1.31.1
langchain>=0.1.0
langchain-google-genai>=0.0.5
faiss-cpu>=1.7.4
PyPDF2>=3.0.0
```

## Memory Architecture

```mermaid
graph LR
    A[Short-term Memory] -->|Recent Queries| B((Memory Store))
    C[Context Window] -->|Active Context| B
    D[Vector Cache] -->|Embeddings| B
    B -->|Retrieval| E[Response Generation]
```

## Query Processing Flow

```mermaid
stateDiagram-v2
    [*] --> QueryReceived
    QueryReceived --> Preprocessing
    Preprocessing --> VectorSearch
    VectorSearch --> ContextGeneration
    ContextGeneration --> ResponseFormulation
    ResponseFormulation --> MemoryUpdate
    MemoryUpdate --> [*]
```

## Technical Deployment Architecture

```mermaid
graph TB
    subgraph Cloud_Infrastructure
        ST[Streamlit Cloud]
        FAISS[FAISS Index]
        MEM[Memory Store]
    end

    subgraph External_Services
        GEMINI[Gemini API]
        PDF[PDF Service]
    end

    subgraph Security
        API_KEY[API Key Manager]
        VAL[Input Validator]
    end

    ST --> API_KEY
    API_KEY --> GEMINI
    ST --> FAISS
    FAISS --> MEM
    ST --> PDF
```

## Performance Metrics

| Operation | Average Time | Memory Usage |
|-----------|--------------|--------------|
| Document Loading | 2.5s | 150MB |
| Embedding Generation | 1.2s | 300MB |
| Query Processing | 0.8s | 100MB |
| Response Generation | 1.5s | 200MB |

## Implementation Details

### Vector Store Implementation
```python
def similarity_search(self, query, k=3):
    query_vector = self.embeddings.embed_query(query)
    results = self.vector_store.similarity_search_by_vector(query_vector, k)
    return self._process_results(results)
```

## Current System Status
- **Last Updated**: 2025-03-06 15:53:07 UTC
- **Maintainer**: @srikrishnavansi
- **Status**: Production

---
Built with 🚀 by [Sri Krishna Vamsi](https://github.com/srikrishnavansi)
