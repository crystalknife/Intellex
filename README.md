# Intellex

<p align="center">

<img src="assets/logo/logo.png" alt="Intellex Logo" width="160"/>

</p>

<h1 align="center">
Intellex
</h1>

<p align="center">
<b>Transform Information into Intelligence.</b>
</p>

<p align="center">

A modern, open-source <b>News Intelligence Operating System</b> that transforms fragmented information into structured, searchable intelligence.

</p>

---

## Overview

Intellex is an AI-powered News Intelligence Operating System designed to help users understand information instead of simply consuming it.

Traditional news platforms present isolated articles in chronological order.

Intellex continuously collects information from multiple sources, normalizes it, extracts meaningful entities and keywords, clusters related stories into events, and presents them through a calm, intelligence-focused interface.

Rather than asking:

> **"What was published today?"**

Intellex helps answer:

> **"What is actually happening?"**

---

## Vision

Intellex is built around one simple idea:

> **Transform Information into Intelligence.**

Information alone is not intelligence.

Understanding emerges when information is organized, connected, and explored through relationships.

Intellex aims to become an operating system for intelligence—not simply another news reader.

Read the complete vision:

➡️ **[Project Vision](docs/PROJECT_VISION.md)**

---

# Features

Current v0.1 includes:

- Multi-source RSS ingestion
- Event clustering
- Document normalization
- Entity extraction
- Keyword extraction
- Search
- Source management
- Dynamic RSS feed configuration
- Manual ingestion trigger
- Responsive Intelligence Dashboard
- Event detail pages
- Document browser
- Source analytics
- Settings page
- REST API powered by FastAPI
- Modern Next.js frontend

---

# Screenshots

> Screenshots will be added in future releases.

```
assets/screenshots/
```

---

# Architecture

```
RSS Sources
      │
      ▼
Collection
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
SQLite Database
      │
      ▼
FastAPI Backend
      │
      ▼
Next.js Frontend
```

A more detailed explanation is available here:

➡️ **[Architecture Documentation](docs/ARCHITECTURE.md)**

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Feedparser
- spaCy
- APScheduler

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- TanStack Query
- Axios
- Framer Motion
- shadcn/ui

---

# Repository Structure

```
Intellex/

├── assets/
│   ├── banners/
│   ├── diagrams/
│   ├── logo/
│   └── screenshots/
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN_SYSTEM.md
│   ├── DEVELOPMENT.md
│   └── PROJECT_VISION.md
│
├── intellex-backend/
│
├── intellex-frontend/
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── README.md
```

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/crystalknife/Intellex.git

cd Intellex
```

---

# Backend Setup

```bash
cd intellex-backend

python -m venv venv

venv\Scripts\activate

pip install -r backend/requirements.txt

copy backend\.env.example backend\.env

uvicorn backend.app.api.app:app --reload --app-dir .
```

The backend will be available at:

```
http://localhost:8000
```

---

# Frontend Setup

```bash
cd intellex-frontend/frontend

npm install

npm run dev
```

The frontend will be available at:

```
http://localhost:3000
```

---

# API Documentation

Once the backend is running:

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

Additional API documentation:

➡️ **[API Documentation](docs/API.md)**

---

# Documentation

Project documentation is available inside the **docs/** directory.

- 📘 [Architecture](docs/ARCHITECTURE.md)
- 🎨 [Design System](docs/DESIGN_SYSTEM.md)
- 🛠️ [Development Guide](docs/DEVELOPMENT.md)
- 🌐 [API Documentation](docs/API.md)
- 🚀 [Project Vision](docs/PROJECT_VISION.md)

---

# Roadmap

Upcoming milestones include:

- AI Workspace
- Timeline Intelligence
- Collections
- Semantic Search
- Knowledge Graph
- Vector Search
- Authentication
- User Accounts
- Plugin Architecture
- PostgreSQL Support
- Docker Deployment
- Cloud Deployment

Complete roadmap:

➡️ **[ROADMAP.md](ROADMAP.md)**

---

# Contributing

Contributions, ideas, bug reports, and feature requests are welcome.

Before contributing, please read:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

# Security

If you discover a security issue, please review:

➡️ **[SECURITY.md](SECURITY.md)**

---

# Changelog

Project history is maintained in:

➡️ **[CHANGELOG.md](CHANGELOG.md)**

---

# Design Philosophy

Intellex follows one guiding principle:

> **Designed. Never Decorated. Quiet Confidence.**

The interface should disappear behind the information.

Every design decision prioritizes clarity over decoration.

---

# Project Status

**Current Release**

```
v0.1.0
```

Current focus:

- Stabilizing the MVP
- Improving ingestion quality
- Expanding intelligence features
- Preparing for AI-powered workflows

---

# License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

# Acknowledgements

Intellex draws inspiration from modern engineering and design practices found in projects such as:

- Apple
- Linear
- Vercel
- GitHub
- Notion
- Stripe

while maintaining its own product philosophy and long-term vision.

---

# Final Thought

The internet produces more information every day.

Intellex exists to help people make sense of it.

> **Transform Information into Intelligence.**