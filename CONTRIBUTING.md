# Contributing to Intellex

First of all, thank you for your interest in contributing to Intellex.

Whether you're fixing bugs, improving documentation, proposing new features, or refining the user experience, your contributions help move the project forward.

Intellex aims to become a modern **News Intelligence Operating System**, and thoughtful contributions are always welcome.

---

# Before You Start

Please take a few minutes to read the following documents before contributing:

- `README.md`
- `ROADMAP.md`
- `docs/ARCHITECTURE.md`

Understanding the project vision and architecture will make it much easier to contribute effectively.

---

# Development Philosophy

Intellex follows a few guiding principles.

## Build for clarity

Every feature should make information easier to understand.

---

## Prefer simplicity

Simple solutions are usually easier to maintain than clever ones.

---

## Keep components modular

Avoid tightly coupling unrelated systems.

Each component should have a clear responsibility.

---

## Design before implementation

Architecture and user experience should guide implementation—not the other way around.

---

## Quality over quantity

A small number of well-designed features is more valuable than many unfinished ones.

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/crystalknife/Intellex.git

cd Intellex
```

---

## Backend

```bash
cd intellex-backend

python -m venv venv

venv\Scripts\activate

pip install -r backend/requirements.txt

copy backend/.env.example backend/.env

uvicorn backend.app.api.app:app --reload --app-dir .
```

---

## Frontend

Open a new terminal.

```bash
cd intellex-frontend/frontend

npm install

npm run dev
```

---

# Branch Strategy

Please do **not** work directly on the `main` branch.

Create a feature branch.

Example:

```bash
git checkout -b feature/event-timeline
```

or

```bash
git checkout -b fix/api-timeout
```

---

# Commit Messages

Use clear, descriptive commit messages.

Examples:

```text
feat: add semantic search

fix: improve RSS ingestion reliability

docs: update architecture guide

refactor: simplify clustering service

test: add API integration tests
```

Avoid messages like:

```text
update

fix

changes

done

temp
```

---

# Pull Requests

A good pull request should:

- Focus on a single feature or fix
- Include a clear description
- Reference related issues when applicable
- Keep changes as small and reviewable as possible

---

# Coding Guidelines

## Backend

- Follow PEP 8
- Prefer type hints
- Keep services modular
- Avoid business logic inside API routes

---

## Frontend

- Use TypeScript
- Prefer reusable components
- Keep styling consistent with the design system
- Avoid unnecessary state

---

# Reporting Bugs

When opening a bug report, please include:

- Operating system
- Browser (if applicable)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if relevant)

---

# Suggesting Features

Feature requests are welcome.

Please explain:

- The problem you're trying to solve
- Why it matters
- Your proposed solution
- Possible alternatives

---

# Project Roadmap

Future work is tracked through:

- GitHub Issues
- `ROADMAP.md`

If you're planning to work on a large feature, consider opening an issue first so the approach can be discussed.

---

# Code of Conduct

By participating in this project, you agree to follow the project's `CODE_OF_CONDUCT.md`.

---

# Thank You

Intellex is an evolving project, and every thoughtful contribution helps improve it.

Whether you're fixing a typo, improving documentation, or implementing a major feature, thank you for helping build Intellex.