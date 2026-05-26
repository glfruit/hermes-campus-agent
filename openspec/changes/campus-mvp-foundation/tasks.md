## 1. App Scaffold

- [x] 1.1 Create `apps/campus-web` Next.js/TypeScript project files.
- [x] 1.2 Add package scripts, TypeScript config, Next config, and lint config for local development.
- [x] 1.3 Add app-level CSS tokens that follow `DESIGN.md`.

## 2. Domain Models And Fixtures

- [x] 2.1 Define TypeScript models for roles, knowledge sources, citations, answers, drafts, tasks, and Hermes bridge inputs/outputs.
- [x] 2.2 Add local campus knowledge fixtures with metadata and excerpts.
- [x] 2.3 Add deterministic knowledge search and answer generation services.
- [x] 2.4 Add deterministic draft generation and task ledger services.

## 3. Workbench UI

- [x] 3.1 Build the role-aware workbench shell and navigation.
- [x] 3.2 Build source-cited Q&A interaction with abstention behavior.
- [x] 3.3 Build source detail panel with visible metadata and excerpts.
- [x] 3.4 Build reviewable draft panel with assumptions and review status.
- [x] 3.5 Build teaching task ledger panel with task creation from answer/draft context.

## 4. Hermes Boundary

- [x] 4.1 Define `HermesBridge` interface.
- [x] 4.2 Add local/mock bridge implementation that uses deterministic fixture services.
- [x] 4.3 Keep real Hermes API integration documented but disabled for this MVP.

## 5. Verification

- [x] 5.1 Add a local type-check/build verification command.
- [x] 5.2 Verify the app renders in a browser with desktop and mobile viewport checks.
- [x] 5.3 Verify no real credentials, private data, or business-system write operations are introduced.
- [x] 5.4 Update project documentation with how to run the campus MVP.
