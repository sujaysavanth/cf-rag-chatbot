# cf-rag-chatbot 🤖

An internal AI chatbot powered by **Retrieval-Augmented Generation (RAG)**, 
built entirely on the Cloudflare developer platform. Designed to demonstrate 
production-grade AI pipeline architecture with document ingestion, 
semantic search, and LLM evaluation.

## Architecture

User Query → Cloudflare Worker → Vectorize (semantic search) 
         → Workers AI (LLM) → AI Gateway (monitoring) → Response

## Stack

| Layer            | Technology                        |
|------------------|-----------------------------------|
| Runtime          | Cloudflare Workers (Python beta)  |
| Embeddings + LLM | Cloudflare Workers AI             |
| Vector Search    | Cloudflare Vectorize              |
| Metadata Storage | Cloudflare D1                     |
| Monitoring       | Cloudflare AI Gateway             |

## Features

- **Document ingestion pipeline** — chunk, embed, and store documents
- **Semantic search** — retrieve relevant context via cosine similarity
- **RAG query pipeline** — ground LLM responses in retrieved context
- **LLM evaluation layer** — score responses for relevance and accuracy
- **Edge-native** — zero cold starts, globally distributed

## Getting Started

### Prerequisites
- Cloudflare account (free tier)
- Node.js (for Wrangler CLI)
- Python 3.11+

### Setup

```bash
# Install Wrangler
npm install -g wrangler
wrangler login

# Clone the repo
git clone https://github.com/sujaysavanth/cf-rag-chatbot.git
cd cf-rag-chatbot

# Create Cloudflare services
wrangler d1 create rag-metadata
wrangler vectorize create rag-vectors --dimensions=768 --metric=cosine
```

### Deploy

```bash
wrangler deploy
```

## Project Structure