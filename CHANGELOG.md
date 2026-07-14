# Changelog

All notable changes to this project will be documented in this file.

This project follows the principles of [Keep a Changelog](https://keepachangelog.com/) and adheres to [Semantic Versioning](https://semver.org/).

---

# [v0.1.0] — Initial MVP Release

**Release Date:** July 2026

This release marks the first public milestone of Intellex following a complete architectural rewrite from the original AutoJourno project. The focus of this release was to establish a scalable foundation for a modern News Intelligence Operating System.

---

## 🚀 Added

### Core Platform

- Modular FastAPI backend
- Modern Next.js frontend
- SQLite persistence layer
- REST API
- Responsive dashboard
- Modular service architecture

### Intelligence Pipeline

- RSS feed ingestion
- Document normalization
- HTML entity decoding
- Keyword extraction
- Named Entity Recognition (spaCy)
- Event clustering
- Source attribution

### User Experience

- Intelligence dashboard
- Events explorer
- Event detail pages
- Documents explorer
- Search interface
- Sources management
- Settings page

### Feed Management

- Dynamic RSS feed management
- Enable/Disable feeds
- Feed persistence
- Manual ingestion trigger
- Pipeline status monitoring

---

## ♻️ Changed

### Architecture

- Complete rewrite of the original AutoJourno architecture.
- Migrated from article generation to intelligence-first event organization.
- Introduced a modular backend with clear separation of concerns.
- Rebuilt the frontend using Next.js and TypeScript.

### User Interface

- Redesigned navigation.
- Improved dashboard layout.
- Consistent routing across all pages.
- Better pagination and filtering experience.

---

## 🛠 Fixed

- Prevented API timeouts during long-running ingestion.
- Improved ingestion concurrency.
- Fixed HTML entity decoding issues.
- Corrected navigation inconsistencies.
- Improved pagination behavior.
- Enhanced feed management reliability.

---

## ⚠️ Known Limitations

The following features are planned for future releases:

- AI Workspace
- Collections
- Timeline View
- Semantic Search
- Knowledge Graph
- Retrieval-Augmented Generation (RAG)
- Docker deployment
- GitHub Actions CI/CD
- PostgreSQL support
- Authentication and user management

---

## ❤️ Acknowledgements

Intellex v0.1 establishes the foundation for a scalable intelligence platform focused on transforming large volumes of information into structured, searchable, and actionable knowledge.

For future development plans, see:

- `ROADMAP.md`