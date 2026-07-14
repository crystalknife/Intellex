# Intellex API Documentation

> **Version:** v0.1.0

Intellex exposes a REST API built with **FastAPI** that powers the web dashboard and provides access to the intelligence pipeline.

This document provides a high-level overview of the available API groups in the current MVP.

---

# Base URL

Local development:

```
http://localhost:8000
```

---

# Interactive Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

These pages always represent the latest API and should be considered the authoritative reference for request and response schemas.

---

# API Overview

The API is organized around resources rather than pages.

```
Dashboard

↓

Events

↓

Documents

↓

Search

↓

Sources

↓

Feeds

↓

Ingestion

↓

Settings
```

---

# Dashboard

Provides summary information for the Intelligence Dashboard.

Typical information includes:

- Pipeline statistics
- Recent events
- Recent documents
- System overview

---

# Events

The Events API exposes clustered intelligence.

Typical capabilities include:

- List events
- Retrieve an individual event
- View related documents

Future versions will support:

- Event timelines
- Event relationships
- Semantic clustering

---

# Documents

The Documents API manages ingested articles.

Current capabilities include:

- Browse documents
- Pagination
- Source filtering
- Metadata retrieval

Future versions may include:

- Full-text search
- Entity filtering
- Similar document discovery

---

# Search

Provides search functionality across the intelligence database.

Current MVP supports searching available indexed content.

Future versions will include:

- Semantic Search
- Hybrid Search
- AI-assisted retrieval

---

# Sources

Provides information about configured news sources.

Typical information includes:

- Source list
- Document counts
- Source statistics

---

# Feed Management

Feeds can be managed dynamically through the API.

Current capabilities:

- List feeds
- Add feeds
- Enable feeds
- Disable feeds
- Delete feeds

The dashboard uses these endpoints to manage RSS sources without requiring code changes.

---

# Ingestion

Intellex supports manual ingestion during development.

Capabilities include:

- Trigger ingestion
- Monitor pipeline status

Scheduled ingestion is handled automatically by the backend.

---

# Response Format

API responses follow standard JSON conventions.

Typical successful response:

```json
{
  "success": true,
  "data": {}
}
```

Typical error response:

```json
{
  "detail": "Resource not found."
}
```

The exact schema varies by endpoint and is documented in the generated OpenAPI specification.

---

# Status Codes

Common HTTP status codes used by Intellex:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# API Design Principles

Intellex follows a small set of API principles:

- Resource-oriented endpoints
- Predictable JSON responses
- Consistent error handling
- Stateless requests
- Clear separation between frontend and backend

The frontend communicates exclusively through the REST API.

Business logic should never be implemented in frontend components.

---

# Authentication

Authentication is **not included** in v0.1.

It is planned for a future release and will include:

- User authentication
- Authorization
- API keys
- Role-based access control

---

# Versioning

Current API Version:

```
v0.1.0
```

As Intellex evolves, future API versions will maintain backward compatibility whenever practical.

Breaking changes will be documented in:

- CHANGELOG.md
- Release Notes

---

# Future API

Planned additions include:

- Semantic Search
- Knowledge Graph
- Timeline API
- AI Workspace API
- Collections API
- WebSocket support
- GraphQL exploration
- Plugin APIs

---

# Development

When developing against the API:

1. Start the backend.
2. Open the interactive Swagger UI.
3. Explore available endpoints.
4. Use generated schemas for request and response models.

The generated OpenAPI documentation should always be considered the source of truth.