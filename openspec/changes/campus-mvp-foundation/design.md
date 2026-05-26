## Context

The fork currently contains the upstream Hermes Agent runtime and project planning documents, but no campus-specific application surface. The first development step needs to prove a product slice without binding the project to real school systems, real personal data, or a premature multi-service architecture.

The first users are a teaching department deputy administrator and a teacher. Their early value comes from source-cited policy/material lookup, reviewable draft generation, and routine task tracking. Hermes will eventually orchestrate model and tool calls, but the first app must keep campus state, review status, and permission boundaries outside unconstrained model reasoning.

## Goals / Non-Goals

**Goals:**

- Add a standalone `apps/campus-web` Next.js/TypeScript app for the first-phase workbench.
- Build the first vertical slice with local fixture data and deterministic service functions.
- Represent knowledge sources, citations, drafts, tasks, roles, and Hermes bridge inputs/outputs as typed domain models.
- Make source citations, abstention, draft review state, and task state visible in the UI.
- Keep the app easy for one developer to run and inspect.
- Preserve a clean boundary for future Hermes API, WeCom, Postgres, pgvector, and document worker integrations.

**Non-Goals:**

- Do not modify upstream Hermes core runtime behavior.
- Do not connect to real教务/OA/人事/财务/学工 systems.
- Do not ingest real student, staff, grade, disciplinary, psychological, personnel, or financial data.
- Do not implement authentication, real multi-tenant authorization, or production deployment in this change.
- Do not implement a full vector database or document parsing worker yet.
- Do not automate official publication, approval, grade changes, or other high-stakes institutional decisions.

## Decisions

### Decision 1: Build a separate campus Web app under `apps/campus-web`

The campus MVP will live under `apps/campus-web` instead of being embedded in Hermes core or the existing Hermes dashboard.

Rationale:

- Keeps upstream Hermes runtime easier to merge from upstream.
- Lets the campus product evolve as a product app rather than a CLI/dashboard feature.
- Supports later deployment as a Web+BFF surface that calls Hermes, WeCom, and storage adapters.

Alternatives considered:

- Modify the existing `web/` dashboard: rejected because the Hermes dashboard is a runtime/admin surface, not the campus product UI.
- Add a Hermes plugin first: rejected because the first risk is product workflow clarity, not plugin mechanics.

### Decision 2: Use typed fixtures before RAG infrastructure

The first Q&A implementation will search local fixture documents and excerpts with deterministic TypeScript functions.

Rationale:

- Proves the UI and source-citation contract before investing in pgvector and ingestion pipelines.
- Allows repeatable tests and demos.
- Avoids accidental use of real internal school documents.

Alternatives considered:

- Add Postgres + pgvector immediately: deferred until the citation and task UX is proven.
- Call an LLM directly for retrieval: rejected for the MVP because source selection and abstention must be inspectable.

### Decision 3: Introduce a `HermesBridge` interface with local implementation

The MVP will define `HermesBridge` interfaces for asking, drafting, and later tool orchestration, but the first implementation will be local and deterministic/mockable.

Rationale:

- Separates campus app state from Hermes runtime details.
- Lets UI, tasks, and citation behavior stabilize before model behavior is introduced.
- Provides a clear seam for future Hermes API Server integration.

Alternatives considered:

- Call Hermes from the first commit: deferred because it would mix product UX, runtime integration, and model reliability risks.
- Build a custom agent loop in TypeScript: rejected because Hermes is intended to remain the agent runtime.

### Decision 4: Human review state is part of the domain model

Generated drafts and AI-assisted outputs will carry explicit review state such as `draft`, `reviewing`, `confirmed`, or `done`.

Rationale:

- The product must visually distinguish generated draft text from approved official content.
- Review state becomes the basis for audit and workflow rules later.

Alternatives considered:

- Treat drafts as plain text output: rejected because it hides institutional responsibility and increases misuse risk.

### Decision 5: Product UI follows the existing `DESIGN.md`

The workbench will use a restrained operational interface: dense but readable, with split panes, visible sources, task state, and draft review status.

Rationale:

- The first audience is doing repeated administrative work, not evaluating a marketing page.
- The UI should make source traceability and review obligations harder to miss.

Alternatives considered:

- Chat-only UI: rejected because the project is a workbench, not just a chatbot.
- Decorative dashboard: rejected because it hides the actual work.

## Risks / Trade-offs

- Fixture search may feel less intelligent than a real RAG system -> Mitigation: label it as a local MVP and keep the `HermesBridge`/knowledge API ready for replacement.
- Adding a separate app increases repo surface area -> Mitigation: keep dependencies minimal and avoid touching Hermes core.
- Mock Hermes behavior may diverge from real model behavior -> Mitigation: keep output schemas strict and add integration tests when the real bridge is added.
- Users may over-trust draft text -> Mitigation: visually mark every draft as requiring human review and show source basis near generated text.
- Lack of real authentication means no real deployment readiness -> Mitigation: keep the MVP local-only and document auth as a later capability.

## Migration Plan

1. Add `apps/campus-web` with local-only fixture data and service functions.
2. Add source-cited Q&A, draft workspace, and task ledger UI.
3. Verify with local type checks and a browser pass.
4. Later changes can replace local services with Hermes API, Postgres/pgvector, and WeCom adapters without changing the first UI concepts.

Rollback is simple: remove `apps/campus-web` and the OpenSpec change artifacts. No persistent data migrations or external integrations are introduced.

## Open Questions

- Which deterministic workflow should become the first state-machine prototype: schedule-change consultation or make-up exam consultation?
- Should the first real storage step use SQLite for speed or Postgres immediately for pgvector alignment?
- Which Hermes API mode should become the first real bridge target?
- Which WeCom callback mode will be used in the deployment environment?
