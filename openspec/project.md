# Hermes Campus Agent OpenSpec Context

## Purpose

Build a lightweight AI campus work platform on top of Hermes Agent for teaching management and teacher daily workflows.

## First Release

- Web workbench.
- WeCom lightweight entry.
- Teaching administrator assistant.
- Teacher assistant.
- Knowledge-base Q&A with citations.
- Document upload and summarization.
- Teaching task ledger and reminders.
- Hermes Agent API integration.
- One deterministic teaching-flow prototype.

## Architecture Direction

- TypeScript app backend for Web/BFF/auth/tasks/WeCom/workflow state.
- Hermes Agent as an external runtime or local service.
- Python workers only where the TypeScript ecosystem is weak, such as document parsing, OCR, and RAG ingestion.
- Postgres plus pgvector is preferred once real multi-user permissions and audit are needed.

## Quality Attributes

- Source traceability.
- Permission-aware retrieval.
- Auditability.
- Human review for sensitive actions.
- Small operational footprint.
- Local-first development using Docker Compose where practical.

## Red Lines

- No automatic grade modification.
- No automatic high-stakes student, personnel, finance, or disciplinary decisions.
- No broad personal-data access by default.
- No business-system write tools exposed directly to unconstrained agent reasoning.
