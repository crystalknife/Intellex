# Intellex Architecture

> **Transform Information into Intelligence.**

This document describes the architecture, design principles, and internal workflow of Intellex.

It is intended for contributors, developers, and anyone interested in understanding how Intellex processes information from ingestion to presentation.

---

# Overview

Intellex is built as a modular News Intelligence Operating System.

Rather than treating articles as isolated pieces of content, Intellex transforms incoming information into structured intelligence through a multi-stage processing pipeline.

The system is designed around three core goals:

- Modular architecture
- Clear separation of concerns
- Extensibility for future AI capabilities

---

# High-Level Architecture

```
                    ┌──────────────────────────┐
                    │      RSS Sources         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      RSS Collector       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Normalization        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Entity & Keyword NLP    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Event Clustering      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      SQLite Database     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      FastAPI Backend     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Next.js Dashboard     │
                    └──────────────────────────┘
```

---

# System Components

## 1. RSS Ingestion

The ingestion layer continuously collects information from configured RSS feeds.

Responsibilities include:

- Downloading feeds
- Parsing articles
- Source validation
- Duplicate detection
- Initial metadata extraction

Future versions may support:

- News APIs
- Reddit
- YouTube
- Podcasts
- Government data
- Social media
- PDFs
- Enterprise data sources

---

## 2. Normalization

Incoming data is normalized before entering the intelligence pipeline.

Current responsibilities include:

- HTML entity decoding
- Content cleanup
- Timestamp normalization
- URL normalization
- Metadata standardization

This ensures downstream components operate on consistent data regardless of source.

---

## 3. Natural Language Processing

Intellex enriches documents using NLP before clustering.

Current capabilities include:

- Named Entity Recognition (NER)
- Keyword extraction
- Basic metadata enrichment

Current NLP engine:

- spaCy

Future capabilities include:

- Embeddings
- Summarization
- Classification
- Topic modeling
- Language detection
- Sentiment analysis

---

## 4. Event Clustering

Event clustering is the core intelligence layer.

Instead of storing unrelated articles independently, Intellex groups related documents into evolving events.

Each event represents a real-world topic rather than a single article.

Future improvements include:

- Semantic clustering
- Incremental clustering
- Event merging
- Event splitting
- Confidence scoring

---

## 5. Persistence Layer

Current database:

- SQLite

Responsibilities:

- Documents
- Events
- Sources
- Feed configuration

Future database support:

- PostgreSQL
- Vector databases
- Graph databases

---

## 6. Backend API

The backend exposes a REST API built with FastAPI.

Current responsibilities:

- Dashboard data
- Event retrieval
- Document retrieval
- Search
- Source management
- Feed management
- Settings

Future additions:

- Authentication
- GraphQL
- WebSockets
- Public API
- API keys

---

## 7. Frontend

The frontend is built with Next.js and TypeScript.

Current pages include:

- Dashboard
- Events
- Documents
- Search
- Sources
- Settings

Future pages include:

- AI Workspace
- Timeline
- Collections
- Entity Explorer
- Knowledge Graph

---

# Data Flow

The complete processing pipeline follows these stages:

```
RSS Feed
      │
      ▼
Collector
      │
      ▼
Normalization
      │
      ▼
Entity Extraction
      │
      ▼
Keyword Extraction
      │
      ▼
Event Clustering
      │
      ▼
Database
      │
      ▼
REST API
      │
      ▼
Frontend
```

Each stage has a single responsibility and can evolve independently.

---

# Project Structure

```
Intellex/

├── intellex-backend/
│   ├── backend/
│   ├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── processors/
│   ├── models/
│   └── database/
│
├── intellex-frontend/
│   └── frontend/
│       ├── app/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       ├── lib/
│       └── styles/
│
├── docs/
└── assets/
```

> The exact directory structure may evolve as Intellex grows, but the architectural boundaries will remain consistent.

---

# Design Principles

Intellex follows several architectural principles.

## Separation of Concerns

Each component has a single responsibility.

---

## Modular Services

Components should be replaceable without affecting unrelated parts of the system.

---

## API-First Design

The frontend communicates exclusively through the backend API.

This keeps the UI independent from business logic.

---

## Extensibility

Intellex is designed to support future additions such as:

- AI agents
- Knowledge Graphs
- RAG
- Semantic Search
- Enterprise connectors

without requiring architectural redesign.

---

# Future Architecture

The long-term architecture introduces additional layers.

```
External Sources

↓

Ingestion Workers

↓

Processing Pipeline

↓

Knowledge Graph

↓

Vector Database

↓

AI Workspace

↓

REST + GraphQL APIs

↓

Web Dashboard
```

These components are intentionally planned as independent services to improve scalability and maintainability.

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- feedparser
- spaCy

---

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- TanStack Query

---

## Development

- Git
- GitHub
- npm
- Uvicorn

---

# Philosophy

Intellex is designed around one central idea:

> **Information becomes valuable when it is organized into intelligence.**

Every architectural decision should support that principle.

The goal is not simply to collect more information.

The goal is to help people understand it.