
# Maid Margaret Q&A System (RAG App)

This project is a **Retrieval-Augmented Generation (RAG)** application built using **Streamlit**, **LangChain**, and **ChromaDB**. It allows users to ask questions about the historical book *"Maid Margaret of Galloway"*, and receive intelligent, source-aware answers powered by language models.


## Project Purpose

The aim of this application is to enhance understanding of historical documents through natural language querying. By uploading or indexing a book and using a vector-based search engine, users can interactively ask questions about the content and retrieve accurate responses based on the actual text.


## Architecture Overview

```mermaid
graph TD
    A[User Interface - Streamlit] -->|User asks question| B[Query Handler - RAG Chain]
    B -->|Passes query| C[Retriever - ChromaDB]
    C -->|Fetches relevant chunks| D[Document Chunks]
    D -->|Passes to| E[LLM - Groq API via LangChain]
    E -->|Generates response| F[Answer]
    F -->|Displayed in UI| A

    subgraph Backend_Components
        C
        D
        E
    end

    subgraph Preprocessing_One_Time_Setup["Preprocessing: One-time Setup"]
        G[Preloaded Document - Maid Margaret Book] --> H[Text Splitter - Recursive]
        H --> I[Embeddings - HuggingFace]
        I --> C
    end

```


- **Streamlit** powers the web UI for asking questions and displaying history.
- **LangChain** handles the logic for query transformation, document retrieval, and integration with the LLM.
- **ChromaDB** stores vector embeddings of the book content.
- **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) are used to embed text chunks.
- **Groq API** provides fast, low-latency LLM inference.


## Chunking Strategy

- The book is preprocessed and split into **semantic chunks** using LangChain's default `RecursiveCharacterTextSplitter`.
- Each chunk is approximately **500 characters**, with an **overlap of 50**, to maintain context flow between chunks.


## Embedding Model

The default embedding model is:

- **Model Name**: `all-MiniLM-L6-v2`
- **Provider**: HuggingFace Sentence Transformers
- **Purpose**: Converts document chunks and queries into dense vectors for semantic search in Chroma.

## Getting Started (Local Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/ninamitchell23/rag_query23.git
```

### 2. Set Environment Variables

Create a `.env` file at the project root:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192  # or your preferred Groq model
```

> **❗DO NOT COMMIT YOUR `.env` FILE.**

---

### 3. Build Docker Images

```bash
docker compose build
```

### 4. Run the Application Stack

```bash
docker compose up
```

### 5. Access the App

Once the app is running, open your browser and go to:

```
http://localhost:8501
```

You’ll see a clean UI where you can:
- Ask questions about *Maid Margaret*
- View past questions in the sidebar


##  Project Structure

![Project Structure](images/project_structure.png)


##  Public Deployment

> **Live App:** 


## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://streamlit.io)
- [Chroma](https://www.trychroma.com/)
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Groq API](https://console.groq.com/)


## Future Improvements

- Add PDF upload support
- Advanced search filters (e.g., date, keyword)

---
> Built with ❤️ 
