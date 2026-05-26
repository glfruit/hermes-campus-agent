# PRODUCT.md

## Product

Hermes Campus Agent is a lightweight, extensible AI campus work platform built on Hermes Agent.

## Register

product

## Primary Users

- Teaching department deputy administrator: responsible for teaching operations, quality monitoring, meeting materials, notices, task tracking, policy interpretation, and routine data analysis.
- Teacher: responsible for lesson preparation, course materials, assignments, rubrics, student communication drafts, and teaching policy lookup.
- System maintainer: configures knowledge sources, roles, audit rules, and integration adapters.

## Product Purpose

The platform helps a teaching department use AI in daily work without replacing institutional responsibility. It should assist with retrieval, drafting, summarization, planning, reminder generation, and structured analysis. It must not silently make high-stakes academic, personnel, disciplinary, psychological, or financial decisions.

## First Release Scope

- Web workbench for teaching administrator and teacher workflows.
- WeCom entry for lightweight Q&A, reminders, and links back to Web.
- Knowledge-base Q&A with source citations.
- Document upload, parsing, summarization, and draft generation.
- Teaching task ledger and reminder support.
- Hermes Agent integration for multi-step reasoning and tool orchestration.
- Deterministic flow-state layer for one teaching workflow prototype, such as schedule-change consultation or make-up exam consultation.

## Out of Scope for First Release

- Direct grade modification.
- Automatic official notice publication without human approval.
- Automatic disciplinary, scholarship, psychological, financial, or personnel decisions.
- Full-campus student/personnel data access.
- Write operations to academic affairs, OA, finance, HR, or student-affairs systems.

## Product Principles

1. AI assists; institutional rules decide.
2. Hermes orchestrates tools and reasoning but does not own final business authorization.
3. Every policy answer should cite sources.
4. Every sensitive tool call should be auditable.
5. Web is the primary workspace; WeCom is the lightweight mobile surface.
6. Keep the first version small enough for one developer to maintain.

## Voice

Calm, precise, responsible, and work-focused. Avoid promotional language. Prefer clear next actions, visible sources, and explicit uncertainty.

## Anti-References

- Generic SaaS landing pages with oversized hero sections.
- Decorative AI dashboards that hide the actual work.
- Chat-only products with no task state, source trace, or audit trail.
- Overly colorful education apps that feel playful instead of operational.
- Black-box agent flows that cannot explain why a recommendation was made.

## Design Direction

Operational product UI. Dense but readable. Source-aware. Task-oriented. The interface should feel closer to a quiet command center for teaching operations than a marketing website or student social app.
