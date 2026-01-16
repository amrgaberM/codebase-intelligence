# CodeLens

**AI-Powered Codebase Intelligence System**

CodeLens is an advanced Retrieval-Augmented Generation (RAG) system designed specifically for understanding codebases. Point it at any GitHub repository and instantly gain the ability to ask natural language questions about the code, understand complex architectures, and discover patterns across the entire codebase.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Technical Details](#technical-details)
- [Benchmarks](#benchmarks)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Traditional code search tools rely on keyword matching, missing the semantic relationships that make code understandable. CodeLens combines multiple retrieval strategies with large language models to provide intelligent, context-aware answers about any codebase.

### What Makes CodeLens Different

| Approach | Traditional Search | CodeLens |
|----------|-------------------|----------|
| Search Method | Keyword matching | Hybrid semantic + keyword |
| Code Understanding | Text-based | AST-aware structure |
| Context | Single file | Multi-file with dependencies |
| Results | File list | Natural language explanations |
| Learning Curve | Know exact terms | Ask in plain English |

---

## Key Features

### Intelligent Code Understanding

- **AST-Based Chunking**: Parses code using Abstract Syntax Trees, preserving function and class boundaries instead of arbitrary text splits
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust, C/C++, and more
- **Dependency Analysis**: Tracks imports and builds a dependency graph to understand code relationships

### Advanced Retrieval

- **Hybrid Search**: Combines dense vector search (semantic understanding) with BM25 (exact keyword matching)
- **Reciprocal Rank Fusion**: Merges results from multiple retrieval strategies for optimal relevance
- **Dependency Expansion**: Automatically includes related files based on import relationships
- **Reranking**: Refines results using cross-encoder models or lightweight heuristics

### Smart Features

- **Natural Language Q&A**: Ask questions about the codebase in plain English
- **Function Explanation**: Get detailed explanations of any function including purpose, parameters, and logic
- **Similar Code Search**: Find patterns similar to a provided code snippet
- **Auto-Documentation**: Generate documentation for files and modules
- **Usage Analysis**: Find where functions and classes are defined, imported, and called

### Production Ready

- **Web Interface**: Clean Streamlit-based UI with real-time progress
- **REST API**: FastAPI backend for integration with other tools
- **CLI Tool**: Command-line interface for scripting and automation
- **Time Estimation**: Predicts indexing time based on repository size

---

## Architecture

```
                                 CodeLens Architecture
                                 
    +------------------------------------------------------------------+
    |                        User Interfaces                            |
    |  +----------------+  +----------------+  +--------------------+   |
    |  |   Streamlit    |  |   FastAPI      |  |       CLI          |   |
    |  |   (Web UI)     |  |   (REST API)   |  |    (Terminal)      |   |
    +--+-------+--------+--+-------+--------+--+---------+----------+---+
               |                   |                     |
               +-------------------+---------------------+
                                   |
    +------------------------------v-------------------------------+
    |                      Ingestion Layer                          |
    |  +------------------+  +------------------+  +--------------+ |
    |  |  GitHub Loader   |  |   AST Parser     |  | File Filter  | |
    |  |  - Clone repos   |  |  - Python AST    |  | - Extensions | |
    |  |  - Read files    |  |  - Extract code  |  | - Patterns   | |
    +--+------------------+--+------------------+--+--------------+-+
                                   |
    +------------------------------v-------------------------------+
    |                      Chunking Layer                           |
    |  +------------------+  +------------------+  +--------------+ |
    |  |   AST Chunker    |  | Semantic Chunker |  |  CodeChunk   | |
    |  |  - Functions     |  |  - Text fallback |  |  - Metadata  | |
    |  |  - Classes       |  |  - Paragraphs    |  |  - Context   | |
    +--+------------------+--+------------------+--+--------------+-+
                                   |
    +------------------------------v-------------------------------+
    |                      Embedding Layer                          |
    |  +----------------------------------------------------------+ |
    |  |                    Code Embedder                          | |
    |  |  - HuggingFace Inference API (primary)                   | |
    |  |  - Local SentenceTransformers (fallback)                 | |
    |  |  - Model: all-MiniLM-L6-v2 (384 dimensions)             | |
    +--+----------------------------------------------------------+-+
                                   |
    +------------------------------v-------------------------------+
    |                      Retrieval Layer                          |
    |  +-------------+  +-------------+  +------------------------+ |
    |  | VectorStore |  |    BM25     |  |   Hybrid Retriever     | |
    |  | (ChromaDB)  |  |  (Sparse)   |  |  - RRF Fusion          | |
    |  | - Dense     |  |  - Keywords |  |  - Dependency Expand   | |
    |  +-------------+  +-------------+  +------------------------+ |
    |  +-------------+  +-------------+  +------------------------+ |
    |  |  Reranker   |  |   Query     |  |  Dependency Graph      | |
    |  | - Scoring   |  |  Expander   |  |  - Import tracking     | |
    +--+-------------+--+-------------+--+------------------------+-+
                                   |
    +------------------------------v-------------------------------+
    |                      Generation Layer                         |
    |  +-------------+  +-------------+  +------------------------+ |
    |  |  Generator  |  |   Prompts   |  |  Code Intelligence     | |
    |  | - Groq API  |  |  - System   |  |  - Explain function    | |
    |  | - Llama 3.3 |  |  - Context  |  |  - Find similar        | |
    |  | - Streaming |  |  - Format   |  |  - Generate docs       | |
    +--+-------------+--+-------------+--+------------------------+-+
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/codelens.git
cd codelens
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key" > .env
echo "HF_TOKEN=your_huggingface_token" >> .env
```

### Getting API Keys

**Groq API Key** (Required for LLM):
1. Visit https://console.groq.com
2. Create an account and generate an API key

**HuggingFace Token** (Optional, for faster embeddings):
1. Visit https://huggingface.co/settings/tokens
2. Create a read-access token

---

## Quick Start

### Web Interface

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser.

### CLI

```bash
# Index a repository
python cli.py ingest https://github.com/tiangolo/typer

# Ask a question
python cli.py query "How do I create a CLI command?"

# Interactive chat mode
python cli.py chat
```

### API

```bash
# Start the API server
uvicorn src.api.main:app --reload

# Index a repository
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/tiangolo/typer"}'

# Query the codebase
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does argument parsing work?"}'
```

---

## Usage

### Indexing a Repository

1. Enter a GitHub repository URL in the sidebar
2. Click "Estimate Time" to see how long indexing will take
3. Click "Index" to begin processing
4. Wait for completion (progress shown in real-time)

### Asking Questions

Once indexed, use the Chat tab to ask questions:

- "How does authentication work in this codebase?"
- "What does the process_data function do?"
- "Where is error handling implemented?"
- "Show me how the API routes are structured"

### Using Features

**Explain Function Tab**:
Enter a function or class name to get a detailed explanation including:
- Purpose and behavior
- Parameters and return values
- Step-by-step logic
- Dependencies and usage examples

**Find Similar Tab**:
Paste a code snippet to find similar patterns in the codebase. Useful for:
- Finding code duplication
- Learning coding patterns
- Discovering related implementations

**Documentation Tab**:
Select a file to auto-generate documentation including:
- Module overview
- Class and function descriptions
- Parameter documentation
- Usage examples

**Analyze Tab**:
Get high-level codebase statistics:
- Total files and code chunks
- Classes and functions list
- Find usages of any symbol

---

## API Reference

### Endpoints

#### POST /api/v1/ingest
Index a GitHub repository.

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "branch": "main",
  "force": false
}
```

**Response:**
```json
{
  "success": true,
  "repo_name": "owner_repo",
  "files_processed": 45,
  "chunks_created": 312,
  "message": "Successfully indexed 312 chunks from 45 files"
}
```

#### POST /api/v1/query
Query the indexed codebase.

**Request:**
```json
{
  "query": "How does the login function work?",
  "top_k": 5,
  "use_reranking": true,
  "filter_file": null
}
```

**Response:**
```json
{
  "query": "How does the login function work?",
  "answer": "The login function in auth.py handles user authentication...",
  "sources": [
    {
      "chunk_id": "auth_py_function_login_15",
      "file_path": "src/auth.py",
      "chunk_type": "function",
      "name": "login",
      "start_line": 15,
      "end_line": 45,
      "score": 0.89
    }
  ],
  "retrieval_time_ms": 45.2,
  "generation_time_ms": 1234.5
}
```

#### GET /api/v1/stats
Get system statistics.

**Response:**
```json
{
  "collection_name": "codebase",
  "total_chunks": 312,
  "repos_indexed": ["owner_repo"]
}
```

#### DELETE /api/v1/collection
Delete all indexed data and reset the system.

---

## Configuration

### config.yaml

```yaml
# LLM Settings
llm:
  provider: "groq"
  model: "llama-3.3-70b-versatile"
  temperature: 0.1
  max_tokens: 4096

# Embedding Settings
embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  dimension: 384

# Chunking Settings
chunking:
  strategy: "ast"
  max_chunk_size: 1500
  chunk_overlap: 200

# Retrieval Settings
retrieval:
  top_k: 10
  rerank_top_k: 5
  use_hybrid: true
  bm25_weight: 0.3
  dense_weight: 0.7

# Supported File Extensions
supported_extensions:
  - ".py"
  - ".js"
  - ".ts"
  - ".java"
  - ".go"
  - ".rs"
  - ".md"

# Ignore Patterns
ignore_patterns:
  - "node_modules"
  - "__pycache__"
  - ".git"
  - "venv"
```

---

## Technical Details

### AST-Based Chunking

Unlike text-based chunking that splits at arbitrary character boundaries, CodeLens uses Abstract Syntax Trees to understand code structure:

```
Text Chunking (Problem):
  Chunk 1: "def process(data):\n    result = []\n    for item in da"
  Chunk 2: "ta:\n        result.append(item)\n    return result"
  
AST Chunking (Solution):
  Chunk 1: Complete process() function with full context
```

Benefits:
- Preserves function and class boundaries
- Maintains code integrity
- Includes relevant context (docstrings, decorators)

### Hybrid Retrieval

CodeLens combines two retrieval strategies:

1. **Dense Retrieval** (Vector Search):
   - Converts code to embeddings
   - Finds semantically similar chunks
   - Understands meaning, not just keywords

2. **Sparse Retrieval** (BM25):
   - Traditional keyword matching
   - Handles exact function names
   - Fast and precise

Results are merged using Reciprocal Rank Fusion (RRF):
```
RRF_score = sum(weight / (k + rank)) for each system
```

### Dependency Graph

CodeLens builds a graph of file dependencies by analyzing imports:

```
utils.py
    |
    +-- imports --> config.py
    |
    +-- imported by --> main.py
                   --> api.py
```

When retrieving context, related files are automatically included to give the LLM a complete picture.

---

## Benchmarks

Performance on the Typer repository (605 files, 2117 chunks):

| Metric | Value |
|--------|-------|
| Ingestion Time | ~50 seconds |
| Avg Retrieval Time | 38ms |
| Avg Generation Time | 2 seconds |
| Memory Usage | ~500MB |

### Sample Evaluation Results

```json
{
  "question": "How do I create a CLI command?",
  "retrieval_time_ms": 65,
  "generation_time_ms": 2300,
  "retrieved_files": [
    "docs/tutorial/commands/index.md",
    "docs_src/commands/tutorial001.py",
    "typer/main.py"
  ]
}
```

---

## Project Structure

```
codelens/
+-- src/
|   +-- api/                 # FastAPI REST API
|   |   +-- main.py          # App initialization
|   |   +-- routes.py        # API endpoints
|   |   +-- schemas.py       # Pydantic models
|   |
|   +-- ingestion/           # Repository loading
|   |   +-- github_loader.py # Clone and read repos
|   |   +-- ast_parser.py    # Python AST parsing
|   |
|   +-- chunking/            # Code splitting
|   |   +-- ast_chunker.py   # AST-based chunking
|   |   +-- base_chunker.py  # Chunk data structures
|   |
|   +-- embeddings/          # Vector generation
|   |   +-- code_embedder.py # Embedding model wrapper
|   |
|   +-- retrieval/           # Search components
|   |   +-- vector_store.py  # ChromaDB operations
|   |   +-- bm25_retriever.py# Sparse retrieval
|   |   +-- hybrid_retriever.py # Combined search
|   |   +-- reranker.py      # Result refinement
|   |   +-- query_expander.py# Query enhancement
|   |
|   +-- generation/          # LLM integration
|   |   +-- generator.py     # Groq API wrapper
|   |   +-- prompts.py       # Prompt templates
|   |   +-- code_intelligence.py # Smart features
|   |
|   +-- evaluation/          # Testing
|   |   +-- evaluator.py     # RAG metrics
|   |
|   +-- utils/               # Utilities
|       +-- config.py        # Configuration
|       +-- logger.py        # Logging
|       +-- dependency_graph.py # Import analysis
|
+-- streamlit_app.py         # Web interface
+-- cli.py                   # Command-line interface
+-- api.py                   # Standalone API
+-- benchmark.py             # Performance testing
+-- requirements.txt         # Dependencies
+-- config.yaml              # Configuration file
+-- Dockerfile               # Container build
+-- docker-compose.yml       # Container orchestration
```

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Submit a pull request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest black isort

# Run tests
pytest tests/ -v

# Format code
black src/
isort src/
```

---

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments

- [Groq](https://groq.com) for fast LLM inference
- [ChromaDB](https://www.trychroma.com) for vector storage
- [HuggingFace](https://huggingface.co) for embedding models
- [Streamlit](https://streamlit.io) for the web interface