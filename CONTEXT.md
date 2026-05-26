# Hermes Campus Agent Context

## Domain

Hermes Campus Agent is a campus operations assistant built on Hermes Agent. The first release focuses on two concrete user groups: a teaching department deputy administrator and an individual teacher.

The product is not a general education chatbot. It is an operational workbench for policy lookup, source-cited drafting, document summarization, task tracking, teaching-material assistance, and controlled workflow support.

## Language

- "Teaching department deputy administrator" means a department-level manager responsible for teaching operations, meetings, notices, quality monitoring, and coordination work.
- "Teacher" means a course instructor who needs help with lesson preparation, assignment design, rubric drafting, student communication drafts, and policy lookup.
- "Knowledge base" means school policies, teaching rules, meeting materials, course documents, notices, templates, and approved department documents with traceable sources.
- "Workflow" means a structured business process with explicit state, validation, permission checks, and audit trail. It is not just a prompt chain.
- "Draft" means AI-generated text requiring human review before publication or official use.
- "Source-cited answer" means an answer that links claims to document title, department, version/date, and relevant excerpt.

## Architecture Posture

Hermes remains the agent runtime and orchestration layer. Campus business rules must live in deterministic code, structured state, permission checks, and human approval gates.

Use TypeScript as the default direction for the first-release Web/BFF/workflow layer. Keep Python where it already belongs: Hermes itself, document processing, RAG ingestion, and worker tasks that benefit from Python libraries.

## First Release Constraints

- One developer should be able to understand and maintain the system.
- Web is the primary workspace. WeCom is a lightweight entry for Q&A, reminders, and deep links back to Web.
- The first workflow should be narrow and observable before broader automation is attempted.
- Every sensitive or official action needs a human confirmation state.

## Non-Negotiable Guardrails

Do not automate grade changes, disciplinary decisions, scholarship decisions, psychological risk handling, personnel decisions, finance payments, or official notice publication.

Do not add write access to school business systems without explicit approval, permission design, audit logs, rollback strategy, and a manual confirmation step.

Do not present generated drafts as approved policy, official notice, or final decision.

