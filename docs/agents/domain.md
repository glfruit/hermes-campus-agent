# Domain Docs

This repository uses a single-context domain layout.

## Files

- `CONTEXT.md`: domain language, first-release constraints, architecture posture, and guardrails.
- `PRODUCT.md`: product purpose, users, scope, principles, voice, and anti-references.
- `DESIGN.md`: visual system, layout rules, component style, and UI guardrails.
- `docs/campus/2026-05-26-initial-plan.md`: initial campus platform plan.
- `docs/adr/`: architectural decision records. Add an ADR when a decision changes long-term system shape.

## Consumer Rules

Before product, architecture, workflow, or UI work, read the relevant domain docs. Do not infer campus business rules from general education software patterns.

Before using Matt Pocock `improve-codebase-architecture`, `diagnose`, or `tdd`, load `CONTEXT.md` and check whether the task involves a campus guardrail.

Before using `impeccable`, `design-md`, or frontend design skills, load `PRODUCT.md` and `DESIGN.md`.

If project scope changes, update `CONTEXT.md` and `PRODUCT.md` before changing implementation plans.

