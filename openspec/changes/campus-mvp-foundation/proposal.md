## Why

Hermes Campus Agent needs a first usable vertical slice before deeper Hermes, RAG, WeCom, and workflow integrations are meaningful. The first release should prove the core product shape: a teaching-operations workbench that can answer from trusted campus materials, show sources, generate reviewable drafts, and turn outputs into tasks without automating institutional decisions.

## What Changes

- Add a new `apps/campus-web` TypeScript/Next.js application for the first-phase Web workbench.
- Provide role-aware navigation for the teaching administrator and teacher personas.
- Add fixture-backed campus knowledge documents with source metadata.
- Add a source-cited Q&A surface that can answer from local fixture snippets and visibly abstain when evidence is insufficient.
- Add a draft-generation workspace for notices, meeting materials, lesson plans, assignments, and rubrics, with every generated output marked as requiring human review.
- Add a teaching task ledger that can store tasks created manually or from Q&A/draft context.
- Add a `HermesBridge` boundary that starts with a deterministic/mock local implementation and can later connect to Hermes Agent API Server.
- Keep all first-phase business-system write operations out of scope.

## Capabilities

### New Capabilities

- `campus-web-workbench`: Role-aware Web workbench shell for teaching administrator and teacher workflows.
- `source-cited-knowledge-qa`: Fixture-backed source-cited campus knowledge Q&A with abstention behavior.
- `reviewable-draft-workspace`: Draft-generation workspace with explicit human-review state and visible source basis.
- `teaching-task-ledger`: Lightweight task ledger for teaching operations tasks and AI-assisted follow-up.

### Modified Capabilities

None.

## Impact

- Adds a new app under `apps/campus-web`; does not modify upstream Hermes core runtime paths.
- Introduces local fixture documents and TypeScript domain models for campus knowledge, drafts, tasks, and Hermes bridge responses.
- Adds a new local development command for the campus Web app.
- Establishes the UI and API boundary that WeCom, Hermes API integration, Postgres, and pgvector can reuse later.
- No production credential, school-system write adapter, real student data, or real personnel data is introduced in this change.
