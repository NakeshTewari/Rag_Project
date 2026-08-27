# RAG Project

A Retrieval-Augmented Generation (RAG) application that allows users to query information from their own documents using semantic search and a Large Language Model.

The system processes documents, splits them into smaller chunks, converts those chunks into vector embeddings, stores them in a FAISS vector database, retrieves the most relevant information for a user query, and generates a context-aware answer using a Groq-powered LLM.

---

## Overview

Large Language Models can generate useful answers, but they do not automatically have access to your private documents.

This project solves that problem using **Retrieval-Augmented Generation (RAG)**.

Instead of sending an entire document to the LLM, the system:

1. Loads documents from the local data directory.
2. Splits documents into smaller chunks.
3. Converts chunks into vector embeddings.
4. Stores embeddings in a FAISS vector database.
5. Converts the user's question into an embedding.
6. Retrieves the most relevant document chunks.
7. Sends the retrieved context to an LLM.
8. Generates an answer based only on the retrieved information.

---

# Architecture

```text
                ┌──────────────────┐
                │   Documents      │
                │  PDF / DOCX      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Document Loader  │
                │   LangChain      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Text Chunking    │
                │ Recursive Splitter│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Embedding Model  │
                │ all-MiniLM-L6-v2 │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  FAISS Vector DB │
                └────────┬─────────┘
                         │
                         │ User Query
                         ▼
                ┌──────────────────┐
                │ Similarity Search│
                │    Top-K Chunks  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Groq LLM      │
                │ openai/gpt-oss-20b│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Generated Answer │
                └──────────────────┘
```

---

# Features

* Document-based question answering
* PDF document support
* DOCX document support
* Recursive text chunking
* Semantic vector embeddings
* FAISS vector storage
* Persistent vector database
* Similarity search
* Top-K document retrieval
* Context-aware LLM responses
* Groq LLM integration
* Environment variable support using `.env`

---

# Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| Python                | Core programming language            |
| LangChain             | Document loading and text processing |
| Sentence Transformers | Generating vector embeddings         |
| FAISS                 | Vector similarity search             |
| Groq                  | LLM inference                        |
| LangChain Groq        | Groq integration                     |
| PyPDF                 | PDF document processing              |
| python-dotenv         | Environment variable management      |

---

# Project Structure

```text
Rag_Project/
│
├── data/
│   └── pdfs/
│       └── Your documents
│
├── faiss_store/
│   ├── faiss.index
│   └── metadata.pkl
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── embedding.py
│   ├── vectorstore.py
│   └── search.py
│
├── app.py
├── main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# RAG Pipeline

## 1. Document Loading

The application loads documents from the `data/` directory.

Currently implemented document loaders include:

* PDF
* DOCX

The project uses LangChain document loaders to convert files into document objects.

---

## 2. Document Chunking

Large documents are split into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

Default configuration:

```text
Chunk Size: 1000
Chunk Overlap: 200
```

Chunking helps preserve context while ensuring that document sections can be efficiently embedded and retrieved.

---

## 3. Embedding Generation

The project uses the following Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

Each document chunk is converted into a numerical vector representation.

These vectors allow the system to perform semantic search.

For example, a query such as:

> What is the attention mechanism?

can retrieve relevant information even when the exact words do not appear in the document.

---

## 4. FAISS Vector Store

Generated embeddings are stored using FAISS.

The vector store persists:

```text
faiss_store/
├── faiss.index
└── metadata.pkl
```

The FAISS index stores the embeddings, while the metadata file stores the corresponding document text.

---

## 5. Semantic Search

When a user asks a question:

1. The query is converted into an embedding.
2. FAISS searches for similar document vectors.
3. The most relevant chunks are retrieved.
4. The retrieved chunks are combined into context.

Example:

```python
results = store.query(
    "What is attention mechanism?",
    top_k=3
)
```

---

## 6. Answer Generation

The retrieved context is passed to a Groq-powered LLM.

The system instructs the model to:

* Answer using only the provided context.
* Avoid hallucinating information.
* Clearly explain the answer.
* Mention when information is not available in the documents.

The default LLM configuration uses:

```text
openai/gpt-oss-20b
```

through Groq.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/NakeshTewari/Rag_Project.git
```

```bash
cd Rag_Project
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Alternatively, if using `uv`:

```bash
uv sync
```

---

# Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The application loads environment variables using:

```python
load_dotenv()
```

Do not commit your `.env` file or API keys to GitHub.

---

# Adding Documents

Place your documents inside the `data/` directory.

Example:

```text
data/
├── pdfs/
│   ├── document1.pdf
│   └── document2.pdf
│
└── documents/
    └── example.docx
```

The application will load supported documents when building the vector store.

---

# Building the Vector Store

The vector store can be built from the documents using:

```python
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore

docs = load_all_documents("data")

store = FaissVectorStore("faiss_store")

store.build_from_documents(docs)
```

This process:

1. Loads documents.
2. Splits documents into chunks.
3. Generates embeddings.
4. Creates a FAISS index.
5. Saves the index locally.

---

# Querying the Vector Store

You can directly search the FAISS vector database:

```python
store.load()

results = store.query(
    "What is attention mechanism?",
    top_k=3
)

print(results)
```

---

# Running the RAG Application

Run:

```bash
python app.py
```

Example usage:

```python
from src.search import RAGSearch

rag_search = RAGSearch()

query = "What is Harbor framework?"

summary = rag_search.search_and_summarize(
    query,
    top_k=3
)

print(summary)
```

---

# Example Workflow

```text
User Question
      │
      ▼
"What is the attention mechanism?"
      │
      ▼
Convert Question to Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Retrieve Top-K Relevant Chunks
      │
      ▼
Provide Context to LLM
      │
      ▼
Generate Context-Aware Answer
```

---

# Key Components

## `data_loader.py`

Responsible for loading documents from the data directory.

Supported implementations include:

* PDF loading
* DOCX loading

---

## `embedding.py`

Responsible for:

* Splitting documents into chunks.
* Generating embeddings.
* Managing the Sentence Transformer model.

Embedding model:

```text
all-MiniLM-L6-v2
```

---

## `vectorstore.py`

Responsible for:

* Creating the FAISS index.
* Adding document embeddings.
* Saving the vector store.
* Loading the vector store.
* Performing similarity search.

---

## `search.py`

Contains the main RAG pipeline.

Responsibilities:

* Loading or creating the vector store.
* Retrieving relevant document chunks.
* Creating the LLM prompt.
* Sending the prompt to Groq.
* Returning the generated answer.

---

# Future Improvements

This project can be extended with several advanced RAG capabilities:

* [ ] Hybrid search using BM25 + vector search
* [ ] Reranking retrieved documents
* [ ] Query rewriting
* [ ] Multi-query retrieval
* [ ] Parent document retrieval
* [ ] Metadata filtering
* [ ] Source citations in responses
* [ ] Conversation memory
* [ ] Streaming responses
* [ ] Web interface using Streamlit
* [ ] FastAPI backend
* [ ] Support for more document formats
* [ ] Evaluation using RAGAS
* [ ] Retrieval quality metrics
* [ ] Advanced chunking strategies
* [ ] Multi-vector retrieval
* [ ] Agentic RAG workflows

---

# Why RAG?

Retrieval-Augmented Generation helps LLM applications answer questions using external knowledge.

Instead of relying entirely on the model's training data, RAG retrieves relevant information from your documents at query time.

This makes it useful for:

* Internal knowledge bases
* Research documents
* Technical documentation
* Company documents
* Educational material
* Legal documents
* Customer support systems
* Enterprise search

---

# License

This project is currently intended for learning and experimentation.

---

# Author

**Nakesh Tewari**

GitHub: [NakeshTewari](https://github.com/NakeshTewari?utm_source=chatgpt.com)

---

## Repository

[RAG Project on GitHub](https://github.com/NakeshTewari/Rag_Project?utm_source=chatgpt.com)
