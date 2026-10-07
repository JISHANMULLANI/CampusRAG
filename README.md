# CampusRAG

A hybrid AI assistant that retrieves relevant information from uploaded college documents and the web, providing grounded answers with source citations.

## Features

- 📄 Upload and process PDF documents
- 🔎 Semantic search using vector embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- 🌐 Web fallback when uploaded documents don't contain sufficient information
- 🏫 Prioritizes official college websites for web-based college information
- 🔄 Cross-encoder reranking for more relevant results
- 📚 Source citations for retrieved information
- ⚡ FastAPI backend with a simple HTML/CSS/JavaScript frontend
- 🗄️ Qdrant vector database
- 🤖 Groq LLM integration

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **RAG:** LlamaIndex / custom RAG pipeline
- **Vector Database:** Qdrant
- **Embeddings:** Sentence Transformers
- **Reranker:** Cross-Encoder
- **Web Search:** Tavily
- **LLM:** Groq
- **PDF Processing:** PyMuPDF


## How It Works

```text
User Uploads PDF
       ↓
PDF Extraction & Chunking
       ↓
Embeddings
       ↓
Qdrant Vector Database
       ↓
User Question
       ↓
Retrieve Relevant Document Information
       ↓
Is the information sufficient?
    ↙              ↘
  Yes               No
   ↓                 ↓
Answer from PDF   Web Search
                     ↓
              Official College Website
                     ↓
                  Reranking
                     ↓
                    LLM
                     ↓
              Answer + Citations


## Project Structure

```text
college-rag-assistant/
│
├── backend/
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   ├── rag/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── uploads/
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CampusRAG.git
cd CampusRAG
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside `backend/`:

```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

TAVILY_API_KEY=your_tavily_api_key

GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

COLLECTION_NAME=college_documents
```

### 5. Start Qdrant

Make sure Docker Desktop is running, then from the project root:

```bash
docker compose up -d
```

Check that Qdrant is running:

```bash
docker ps
```

### 6. Start the backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Usage

1. Upload a college PDF.
2. Ask a question related to the uploaded document.
3. CampusRAG searches the uploaded document first.
4. If sufficient information is found, the answer is generated from the document.
5. If the document does not contain sufficient information, CampusRAG falls back to web retrieval.
6. For college-related information, official college websites are prioritized.
7. The final response includes relevant source citations.

## Environment Variables

| Variable | Description |
|---|---|
| `QDRANT_URL` | Local or cloud Qdrant URL |
| `QDRANT_API_KEY` | Qdrant API key, if using Qdrant Cloud |
| `TAVILY_API_KEY` | Tavily web search API key |
| `GROQ_API_KEY` | Groq API key |
| `LLM_MODEL` | Groq LLM model |
| `EMBEDDING_MODEL` | Sentence Transformer embedding model |
| `RERANKER_MODEL` | Cross-encoder reranking model |
| `COLLECTION_NAME` | Qdrant collection name |

## Future Improvements

- Automatic college website/domain detection
- Better retrieval confidence scoring
- Multi-document comparison
- Conversation history
- Authentication and user accounts
- Support for additional document formats
- Improved citation verification

## License

This project is developed as an academic/college project.

