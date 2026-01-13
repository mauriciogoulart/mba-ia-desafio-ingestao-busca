# PDF Semantic Search with LangChain and PostgreSQL

This project demonstrates how to build a semantic ingestion and search system using **LangChain**, **PostgreSQL** with **pgVector**, and **LLMs**.
Users can ingest a PDF document and ask questions via a Command Line Interface (CLI), receiving answers strictly based on the document content.

## 📌 Project Objective

Build software capable of:

- **PDF Ingestion**: Read a PDF file, split its content into chunks, generate embeddings, and store them in a PostgreSQL database using the `pgVector` extension.
- **Semantic Search & Q&A**: Allow users to ask questions via CLI and receive answers based only on the content of the ingested PDF.
- **Out-of-context Handling**: If the answer is not present in the PDF, the system must explicitly state that it does not have enough information.

## 💬 CLI Example

Ask your question:

```text
QUESTION: What is the revenue of SuperTechIABrazil?
ANSWER: The revenue was 10 million reais.
```

Out-of-context question:

```text
QUESTION: How many customers do we have in 2024?
ANSWER: I do not have enough information to answer this question.
```

## 🧱 Project Architecture

```text
├── docker-compose.yml
├── requirements.txt      # Dependências
├── .env.example          # Template da variável OPENAI_API_KEY
├── src/
│   ├── ingest.py         # Script de ingestão do PDF
│   ├── search.py         # Script de busca
│   ├── chat.py           # CLI para interação com usuário
├── document.pdf          # PDF para ingestão
└── README.md             # Instruções de execução
```

## 🛠️ Required Technologies

- **Language**: Python
- **Framework**: LangChain
- **Database**: PostgreSQL + pgVector
- **Database Execution**: Docker & Docker Compose

## 📦 Recommended LangChain Packages

- **Text Splitter**: `RecursiveCharacterTextSplitter`
- **PDF Loader**: `PyPDFLoader`
- **Vector Store**: `PGVector`
- **Search Method**: `similarity_search_with_score(query, k=10)`

## 🤖 LLM & Embeddings Configuration

### OpenAI
- **Embeddings Model**: `text-embedding-3-small`
- **LLM Model**: `gpt-5-nano`
- *Requires an OpenAI API Key*

### Gemini (Google)
- **Embeddings Model**: `models/embedding-001`
- **LLM Model**: `gemini-2.5-flash-lite`
- *Requires a Google API Key*

### Ollama 
- **Embeddings Model**: `text-embedding-004`
- **LLM Model**: `llama3.2:3b`
- *Uses the Gemini embeddings*

## ⚙️ Functional Requirements

### 1. PDF Ingestion
- Split the PDF into chunks of **1000 characters**.
- Use an overlap of **150 characters**.
- Generate embeddings for each chunk.
- Store vectors in PostgreSQL using `pgVector`.

### 2. CLI Query Flow
When a user submits a question:
1. Vectorize the question.
2. Retrieve the top 10 most relevant chunks (`k=10`).
3. Build the prompt using retrieved context.
4. Call the LLM.
5. Return the answer to the user.

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have installed:
- Docker
- Docker Compose
- Python 3.10+

### 2. Environment Variables
Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Add your API key:
```ini
OPENAI_API_KEY=your_openai_api_key_here
# or
GOOGLE_API_KEY=your_google_api_key_here
```

Configure the MODEL_PROVIDER openai, gemini or ollama.

### 3. Start PostgreSQL with pgVector
```bash
docker compose up -d
```
This will start a PostgreSQL instance with pgVector enabled.

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Ingest the PDF
```bash
python src/ingest.py
```
This step:
- Loads the PDF
- Splits it into chunks
- Generates embeddings
- Stores vectors in PostgreSQL

### 6. Run the CLI Chat
```bash
python src/chat.py
```
You can now interact with the system and ask questions about the PDF content.

## 📚 Learning Goals

This project is intended for study purposes and covers:
- Document ingestion pipelines
- Vector databases with PostgreSQL
- Semantic search
- Retrieval-Augmented Generation (RAG)
- CLI-based LLM applications