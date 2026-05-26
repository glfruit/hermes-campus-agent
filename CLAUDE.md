# Hermes Campus Agent Instructions

用中文回答项目问题，除非用户明确要求英文。

This repository is a fork of Hermes Agent for building Hermes Campus Agent. The upstream Hermes development guide remains in `AGENTS.md`, but this campus overlay takes precedence for product direction.

## Project Focus

- First release users: teaching department deputy administrator and teacher.
- Entrypoints: Web workbench plus WeCom.
- Main backend direction: TypeScript for Web/BFF/workflow state; Python remains for Hermes, RAG ingestion, and document-processing workers when needed.
- Hermes is the agent runtime and orchestration layer, not the final authority for campus business rules.
- Strong-rule workflows need structured state, code-level validation, permissions, audit logs, and human confirmation.

## Required Context

Before product or UI work, read:

- `PRODUCT.md`
- `DESIGN.md`
- `docs/campus/2026-05-26-initial-plan.md`

For major changes, use OpenSpec:

- `/opsx:new` to start a structured change.
- `/opsx:continue` to continue artifacts.
- `/opsx:apply` to implement approved tasks.
- `/opsx:verify` before completion.

For frontend work, use:

- `impeccable` for UI shaping, critique, polish, and design-system discipline.
- `design-md` when generating or updating `DESIGN.md`.
- `frontend-design` and `frontend-patterns` for implementation guidance.
- Matt Pocock skills for plan review, architecture pressure-testing, TDD, triage, handoff, and throwaway prototypes.
- Vercel and Stitch skills for React/Next.js best practices, web design audits, shadcn/ui guidance, and design prompt refinement.

## Agent skills

### Issue tracker

Work is tracked in GitHub Issues for `glfruit/hermes-campus-agent`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-role triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This repo uses a single-context domain layout with root `CONTEXT.md` and root `docs/adr/`. See `docs/agents/domain.md`.

## Development Workflow

Follow `docs/campus/development-workflow.md` for project workflow, skill routing, prototype rules, and review gates.

## Research Workflow

Use `docs/research/paper-roadmap.md` when project work may become paper material. For Codex, prefer the `academic-research-suite` router when scoping, writing, reviewing, or checking papers. For shared-agent workflows, use `academic-pipeline`, `deep-research`, `academic-paper`, `academic-paper-reviewer`, `literature-review`, `scholar-evaluation`, and `citation-audit` as appropriate.

## Guardrails

- Do not automate grade changes, disciplinary decisions, scholarship decisions, psychological risk handling, personnel decisions, finance payments, or official notice publication.
- Do not add business-system write actions without explicit human approval and audit design.
- Keep first-release architecture small enough for one developer to maintain.
- Prefer source-cited answers, visible assumptions, and human review states over polished but untraceable AI output.
