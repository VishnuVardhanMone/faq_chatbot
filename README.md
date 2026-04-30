# Context-Aware FAQ Chatbot

## Overview

This project implements a context-aware FAQ chatbot that retrieves answers using semantic similarity. It supports both direct questions and follow-up queries by maintaining conversational context and dynamically switching between intents.

---

## Features

* Semantic search using SentenceTransformers
* Intent-based grouping
* Context-aware follow-up handling
* Dynamic intent switching
* Fully dataset-driven responses

---

## Tech Stack

* Python
* SentenceTransformers
* NumPy

---

## How It Works (Detailed)

The chatbot follows a retrieval-based approach using semantic similarity and contextual understanding.

### 1. Data Preparation

The FAQ dataset is structured as a JSON file where each entry contains:

* An intent (topic)
* Multiple question-answer pairs

The data is flattened into:

* `questions`: all possible user queries
* `answers`: corresponding responses
* `intents`: intent label for each question

---

### 2. Text Embedding

Each question is converted into a numerical vector using a pre-trained SentenceTransformer model.

These embeddings capture semantic meaning, allowing the system to understand rephrased or similar queries.

---

### 3. Query Processing

When a user enters a query:

* The input is normalized (lowercased and trimmed)
* It is converted into an embedding vector

---

### 4. Similarity Search

#### Global Search

* Compares the query with all stored questions
* Finds the most similar match across all intents

#### Context-Based Search

* If a previous intent exists, the search is limited to that intent
* Helps handle follow-up queries like "when", "how", or "status"

---

### 5. Intent Selection

The system compares:

* Best match from global search
* Best match from context-based search

Decision logic:

* For short queries (e.g., "when", "how"), prioritize context
* Otherwise, select the result with the higher similarity score

This enables:

* Accurate follow-up handling
* Dynamic switching between topics

---

### 6. Score Adjustment

For short follow-up queries, the system slightly boosts the similarity score when the detected intent matches the previous intent.

This improves accuracy for conversational inputs.

---

### 7. Response Generation

Based on the final similarity score:

* High confidence → return the answer
* Medium confidence → suggest closest matching question
* Low confidence → return fallback response

---

### 8. Context Management

The chatbot maintains the last detected intent:

* High confidence → update context
* Low confidence → reset context

This allows:

* Multi-turn conversations
* Avoiding incorrect intent carryover

---

## Example Interaction

```
User: refund
Bot: Yes, we offer refunds

User: when
Bot: You will receive your refund in 5-7 days

User: delivery
Bot: Delivery takes 3-5 days

User: when
Bot: Your order will arrive in 3-5 days
```

---

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

---

## Future Improvements

* Add Flask API
* Build user interface
* Improve dataset coverage
