# Hermes Campus Agent Development Workflow

This document defines how to use agent skills and project-management artifacts while building Hermes Campus Agent as a solo, AI-assisted project.

## Operating Model

Use a lightweight spec-first loop for anything that changes product behavior, architecture, data shape, permissions, or user-facing workflow. Use direct edits only for small documentation fixes, obvious bug fixes, or narrow implementation cleanup.

Default stack direction:

- TypeScript for Web, BFF, workflow state, and first-release application code.
- Python for Hermes core, RAG/document-processing workers, ingestion pipelines, and library-heavy NLP tasks.
- WeCom as a lightweight messaging entry, not the complete workbench.
- Deterministic state and code validation for business workflows. LLMs handle language understanding, drafting, summarization, and retrieval support.

## Skill Routing

Use OpenSpec for major project changes:

- `/opsx:explore` when the problem is unclear.
- `/opsx:new` before a feature, integration, workflow, or architecture change.
- `/opsx:apply` after the change is specified.
- `/opsx:verify` before marking the work done.
- `/opsx:archive` after shipped changes settle.

Use Matt Pocock skills for engineering discipline:

- `grill-me`: pressure-test a vague plan before it becomes a spec.
- `grill-with-docs`: align a plan with `CONTEXT.md`, `PRODUCT.md`, ADRs, and existing language.
- `prototype`: answer a UI, state-machine, or workflow question with throwaway code.
- `to-prd`: turn resolved context into a PRD when a feature is larger than one issue.
- `to-issues`: break an approved PRD/spec into vertical-slice GitHub issues.
- `triage`: classify issue backlog and separate agent-ready work from human-required work.
- `tdd`: implement critical workflow/state logic and bug fixes with red-green-refactor.
- `diagnose`: reproduce, minimize, instrument, fix, and regression-test hard bugs.
- `improve-codebase-architecture`: look for deeper structural problems after several real features exist.
- `zoom-out`: regain architectural context before editing unfamiliar parts of Hermes.
- `handoff`: compact context before switching sessions.

Use design and frontend skills for Web work:

- `impeccable shape`: define UX and visual direction before building a significant screen.
- `impeccable craft`: build a scoped UI feature after shape is clear.
- `impeccable critique`, `audit`, `polish`, `harden`: review screens before considering them done.
- `design-md`: update or synthesize `DESIGN.md` when the design system changes.
- `enhance-prompt` and `taste-design`: refine vague UI prompts and keep design-system output non-generic.
- `frontend-design`: create high-quality product UI consistent with `PRODUCT.md` and `DESIGN.md`.
- `frontend-patterns`, `vercel-react-best-practices`, `next-best-practices`, and `vercel-composition-patterns`: guide React/Next implementation.
- `web-design-guidelines`: audit accessibility, UX, and frontend quality before merge.
- `shadcn-ui`: use only when the frontend stack actually adopts shadcn/ui; do not import a component system casually.

## Standard Feature Flow

1. Clarify scope.
   Read `CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, and the initial campus plan. Use `grill-me` or `grill-with-docs` if assumptions are weak.

2. Write or update the spec.
   Use OpenSpec for major work. Keep capability changes small enough for one developer to ship.

3. Prototype only when a question needs evidence.
   Use `prototype` for throwaway UI variants, workflow state machines, or interaction models. Mark prototype code clearly and delete or absorb it after the decision.

4. Design before implementation.
   For Web screens, run an Impeccable shaping pass and keep `DESIGN.md` aligned. Avoid generic SaaS dashboards, decorative AI visuals, and chat-only surfaces.

5. Implement in vertical slices.
   Prefer a slice that includes UI, state, API boundary, fixture data, tests, and docs over a wide horizontal layer.

6. Verify.
   Use targeted tests first. For shared Hermes behavior, use `scripts/run_tests.sh`. For frontend, run type checks, lint, unit tests, and browser verification when a UI exists.

7. Review safety.
   Check source citation behavior, permission boundary, audit trail, human confirmation states, and error handling for campus workflows.

8. Record decisions.
   Add ADRs under `docs/adr/` for durable architecture decisions. Update `CONTEXT.md`, `PRODUCT.md`, or `DESIGN.md` when the project language changes.

## First-Release Work Breakdown

Start with these slices:

1. Web shell and role-aware navigation for teaching administrator and teacher.
2. Knowledge-base ingestion and source-cited Q&A with local fixtures.
3. Draft-generation workspace for notices, meeting materials, lesson plans, assignments, and rubrics.
4. Teaching task ledger with review states and reminders.
5. WeCom adapter for Q&A, task reminders, and Web deep links.
6. One deterministic workflow prototype, such as schedule-change consultation or make-up exam consultation.

## Review Gates

Do not mark a feature done until these are true:

- The user scenario is visible in a spec, issue, or doc.
- Sensitive actions require human confirmation.
- Knowledge answers cite sources or admit insufficient evidence.
- Generated official text is visibly a draft.
- Tests or manual verification steps are recorded.
- UI has passed an accessibility and responsive pass.
- Any prototype has been deleted, absorbed, or clearly documented as temporary.

## Anti-Patterns

- Building a chat-only product and calling it a platform.
- Letting an LLM decide campus business rules.
- Adding write integrations before read-only value is proven.
- Designing for all school roles in the first release.
- Creating complex multi-agent automation before the first workflow state model is observable.
- Keeping throwaway prototypes in the main product path.
- Installing a UI library without first proving it matches the product's operational design needs.

