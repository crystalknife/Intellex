# Intellex Development Guide

> Building Intellex is about building systems, not just features.

This guide defines the engineering principles, workflow, coding standards, and development practices followed throughout the project.

If you're contributing to Intellex, read this document before making architectural changes.

---

# Engineering Philosophy

Intellex is built around one simple idea:

> **Every feature should reduce complexity rather than introduce it.**

Software should become easier to maintain as it grows.

Whenever multiple solutions exist, prefer the one that is:

- Easier to understand
- Easier to test
- Easier to extend
- Easier to maintain

---

# Project Goals

Intellex is designed to become a modern News Intelligence Operating System.

Development should always prioritize:

- Reliability
- Maintainability
- Modularity
- Performance
- Developer Experience

Never sacrifice long-term maintainability for short-term convenience.

---

# Development Workflow

Every feature follows the same lifecycle.

```
Issue

↓

Discussion

↓

Feature Branch

↓

Implementation

↓

Testing

↓

Pull Request

↓

Review

↓

Merge

↓

Release
```

Do not develop directly on the `main` branch.

---

# Branch Naming

Use descriptive branch names.

Examples:

```
feature/ai-workspace

feature/timeline

feature/search-improvements

fix/rss-parser

fix/event-clustering

docs/readme-update

refactor/ingestion-service
```

---

# Commit Messages

Follow Conventional Commits whenever possible.

Examples:

```
feat: add timeline view

fix: improve RSS parsing

docs: update architecture guide

refactor: simplify event clustering

test: add API integration tests

chore: update dependencies
```

Avoid generic messages such as:

```
update

fix

changes

done

temp
```

---

# Architecture Rules

Intellex follows a modular architecture.

Business logic should remain independent from presentation.

Responsibilities should remain clearly separated.

```
Frontend

↓

REST API

↓

Services

↓

Repositories

↓

Database
```

Avoid bypassing architectural layers.

---

# Backend Guidelines

Prefer:

- Small services
- Clear responsibilities
- Dependency injection where appropriate
- Type hints
- Stateless APIs

Avoid:

- Business logic inside API routes
- Large utility files
- Circular dependencies

---

# Frontend Guidelines

Use:

- Functional React components
- TypeScript
- Reusable UI components
- Composition over duplication

Prefer:

- Small components
- Shared hooks
- Predictable state

Avoid:

- Deep prop drilling
- Duplicate UI
- Large page components

---

# Folder Organization

Each directory should have a single responsibility.

Example:

```
backend/

api/

services/

repositories/

processors/

models/

database/
```

```
frontend/

app/

components/

hooks/

services/

lib/
```

Keep files close to the functionality they belong to.

---

# API Design

The backend is API-first.

Frontend components should never communicate directly with the database.

Every interaction should flow through the REST API.

Future versions may introduce GraphQL, but REST remains the primary interface.

---

# Error Handling

Errors should be:

- Informative
- Predictable
- Logged
- Recoverable when possible

Never silently ignore failures.

---

# Logging

Logs should help answer:

- What happened?
- Why did it happen?
- How can it be reproduced?

Avoid excessive logging.

Log meaningful events.

---

# Performance

Optimize only after measuring.

Prioritize:

- Readability
- Correctness
- Reliability

before micro-optimizations.

When optimization is necessary:

- Measure first.
- Optimize.
- Measure again.

---

# Testing

Every major feature should include testing.

Future testing strategy:

- Unit tests
- Integration tests
- API tests
- End-to-end tests

Critical processing pipelines should always be tested before release.

---

# Documentation

Documentation is considered part of the product.

Whenever a significant architectural change is introduced:

Update:

- README
- Architecture
- Development Guide
- API Documentation
- Roadmap (if applicable)

Documentation should evolve alongside the codebase.

---

# Design Consistency

Before creating new UI components, review:

```
docs/DESIGN_SYSTEM.md
```

Every interface should follow the established design language.

---

# Future Engineering Goals

As Intellex grows, the architecture will expand to include:

- Background workers
- PostgreSQL
- Vector databases
- Knowledge Graphs
- Semantic Search
- AI Workspace
- Plugin architecture
- Cloud deployment

The engineering principles in this document should continue to guide those additions.

---

# Guiding Principle

> **Good software is easier to change than to rewrite.**

Every architectural decision should make future development simpler—not harder.

The best feature is one that fits naturally into the system without increasing unnecessary complexity.