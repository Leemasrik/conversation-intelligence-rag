# Conversation Intelligence System

## Overview

Conversation Intelligence System is an offline Retrieval-Augmented Generation (RAG) application that analyzes conversational data to extract user information, retrieve relevant memories, and answer natural language questions. The system processes conversations chronologically, creates topic checkpoints and message checkpoints, extracts user personas, detects persona drift across conversations, classifies user intent using an offline machine learning model, and resolves conflicting memories during retrieval.

The project was developed as part of the KaStack AI/ML Engineer assignment with a focus on building an explainable, lightweight, and CPU-friendly conversational memory system.

---

## Features

### Round 1

* Chronological conversation processing
* Topic checkpoint generation
* Topic-wise summarization
* Message chunk retrieval
* FAISS vector database for semantic search
* User persona extraction
* Interactive Streamlit chatbot

### Round 2

* Persona Drift Detection across conversations
* Offline Intent Classification (TF-IDF + Logistic Regression)
* Conflict-aware Retrieval
* Timeline-based memory organization
* Emotion-aware ranking of retrieved memories
* Contradiction detection between retrieved memories

---

## System Architecture

```
User Query
      │
      ▼
Streamlit Interface
      │
      ▼
Query Router
      │
 ┌────┴──────────────┐
 │                   │
 ▼                   ▼
Intent Classifier    Conflict Resolver
 │                   │
 └────────────┬──────┘
              ▼
          FAISS Retriever
              │
      ┌───────┴────────┐
      ▼                ▼
Topic Checkpoints   Message Chunks
      │                │
      └──────┬─────────┘
             ▼
      Answer Generator
             │
             ▼
      Final Response
```

---

## Technologies Used

* Python
* Streamlit
* FAISS
* Sentence Transformers
* scikit-learn
* TF-IDF Vectorizer
* Logistic Regression
* NumPy
* Pandas
* JSON

---

## Project Structure

```
conversation-intelligence-rag/

│
├── app.py
├── build_pipeline.py
│
├── summaries/
├── persona/
├── drift/
├── vectorstore/
├── models/
├── training/
├── utils/
│
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## How It Works

1. Conversations are parsed chronologically.
2. Topic checkpoints are created whenever the discussion changes.
3. Every 100 messages, checkpoint summaries are generated.
4. Topic summaries and message chunks are embedded using Sentence Transformers.
5. Embeddings are stored in a FAISS vector index.
6. User personas are extracted from conversation history.
7. Persona drift is detected across conversations.
8. User queries are classified using an offline intent classifier.
9. Relevant memories are retrieved.
10. Conflict resolution ranks memories, detects inconsistencies, and generates the final response.

---

## Design Decisions
* Offline-first architecture
* Lightweight ML model for intent classification
* CPU-only inference
* FAISS for efficient semantic retrieval
* Modular pipeline with separate retrieval, routing, persona, and conflict resolution components
* Structured JSON storage for persona and drift information

---

## Limitations

* Persona extraction is rule-based and may miss implicit user traits.
* Contradiction detection uses lightweight heuristics and may produce false positives.
* Intent classifier is trained on a lightweight dataset and can misclassify rare intents.

---

## Future Improvements

* Transformer-based persona extraction
* Natural Language Inference (NLI) for semantic contradiction detection
* Incremental vector index updates
* Better emotion detection
* Online synchronization across devices
* LLM-assisted answer generation

---

## Demo

**Live Application:**
(Add deployed Streamlit URL)

**GitHub Repository:**
https://github.com/Leemasrik/conversation-intelligence-rag

**Loom Walkthrough:**
https://www.loom.com/share/1cf951385e5a42d69e7e390c7f195bc9

---

## Author

Leema