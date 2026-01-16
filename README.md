# 🧠 CodeBase Intelligence RAG

An intelligent RAG system that understands entire codebases. Upload any GitHub repo and chat with it.

## 🎯 Features

- **AST-based Chunking**: Understands code structure (functions, classes, imports)
- **Dependency Graph**: Visualize how files connect
- **Multi-file Context**: Pulls related files automatically when answering
- **Hybrid Search**: BM25 + Dense embeddings + Reranking
- **Code-aware Generation**: Responses with line numbers and file references

## 📁 Project Structure

```
codebase-rag/
├── src/
│   ├── ingestion/          # GitHub cloning & file parsing
│   │   ├── __init__.py
│   │   ├── github_loader.py    # Clone repos from GitHub
│   │   ├── file_parser.py      # Parse different file types
│   │   └── ast_parser.py       # Python AST extraction
│   │
│   ├── chunking/           # Code-aware chunking strategies
│   │   ├── __init__.py
│   │   ├── base_chunker.py     # Base chunking interface
│   │   ├── ast_chunker.py      # AST-based chunking (functions/classes)
│   │   └── semantic_chunker.py # Semantic chunking fallback
│   │
│   ├── embeddings/         # Embedding generation
│   │   ├── __init__.py
│   │   ├── code_embedder.py    # Code-specific embeddings
│   │   └── hybrid_embedder.py  # Dense + Sparse hybrid
│   │
│   ├── retrieval/          # Search & retrieval
│   │   ├── __init__.py
│   │   ├── vector_store.py     # ChromaDB operations
│   │   ├── bm25_retriever.py   # BM25 sparse retrieval
│   │   ├── hybrid_retriever.py # Combine dense + sparse
│   │   └── reranker.py         # Cross-encoder reranking
│   │
│   ├── generation/         # LLM response generation
│   │   ├── __init__.py
│   │   ├── context_builder.py  # Build multi-file context
│   │   ├── prompts.py          # Code-aware prompts
│   │   └── generator.py        # LLM integration (Groq)
│   │
│   ├── evaluation/         # RAG evaluation
│   │   ├── __init__.py
│   │   └── evaluator.py        # Custom evaluation metrics
│   │
│   ├── api/                # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app
│   │   ├── routes.py           # API endpoints
│   │   └── schemas.py          # Pydantic models
│   │
│   └── utils/              # Utilities
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       ├── logger.py           # Logging setup
│       └── dependency_graph.py # Build import graphs
│
├── tests/                  # Unit tests
├── data/
│   ├── repos/              # Cloned repositories
│   └── vectors/            # ChromaDB storage
├── configs/
│   └── config.yaml         # Configuration file
├── scripts/
│   └── setup.sh            # Setup script
├── docs/                   # Documentation
├── app.py                  # Gradio UI
├── cli.py                  # CLI interface
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone this repo
git clone https://github.com/yourusername/codebase-rag.git
cd codebase-rag

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 3. Run the App

```bash
# Option 1: Web UI
python app.py

# Option 2: CLI
python cli.py ingest https://github.com/username/repo
python cli.py query "How does the authentication work?"

# Option 3: API
uvicorn src.api.main:app --reload
```

## 📖 Usage Examples

### Ingest a Repository

```python
from src.ingestion import GitHubLoader
from src.chunking import ASTChunker
from src.retrieval import VectorStore

# Load repo
loader = GitHubLoader()
files = loader.clone_repo("https://github.com/fastapi/fastapi")

# Chunk code
chunker = ASTChunker()
chunks = chunker.chunk_files(files)

# Store in vector DB
store = VectorStore()
store.add_chunks(chunks)
```

### Query the Codebase

```python
from src.retrieval import HybridRetriever
from src.generation import Generator

# Search
retriever = HybridRetriever()
results = retriever.search("How does dependency injection work?")

# Generate answer
generator = Generator()
answer = generator.generate(query, results)
print(answer)
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | LlamaIndex / Custom |
| Embeddings | sentence-transformers (code models) |
| Vector DB | ChromaDB |
| Sparse Search | BM25 (rank_bm25) |
| Reranking | Cross-encoder |
| LLM | Groq (Llama 3.3 70B) |
| Backend | FastAPI |
| Frontend | Gradio |

## 📊 Evaluation

Run evaluation on a test repo:

```bash
python -m src.evaluation.evaluator --repo fastapi/fastapi
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📄 License

MIT License
