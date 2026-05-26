# Paper Roadmap

This roadmap turns Hermes Campus Agent development into publishable research without letting paper ambitions distort the product.

## Research Positioning

The strongest research angle is not "we built a campus chatbot." That is too generic and easy to dismiss.

The stronger claim is:

> A lightweight, source-cited, human-reviewable campus AI workbench can combine agent orchestration with deterministic workflow state to support teaching administration and teacher daily work while preserving institutional responsibility.

This project should collect evidence around that claim.

## Installed Research Skills

Codex-specific:

- `academic-research-suite` in `~/.codex/skills/`: preferred Codex router for research scoping, literature review, paper planning, drafting, review, citation checking, and experiment planning.

Shared agent skills:

- `academic-pipeline`: end-to-end research-to-paper workflow.
- `deep-research`: literature review, systematic review, fact-checking, and research-question refinement.
- `academic-paper`: outline, abstract, draft, revision, citation formatting, and disclosure.
- `academic-paper-reviewer`: simulated peer review and re-review.
- `literature-review`: focused literature synthesis.
- `scholar-evaluation`: scholarly critique of papers, proposals, methods, or evidence.
- `citation-audit`: citation existence and claim-source alignment checks.
- `stop-slop`: English prose cleanup for AI-writing tells.
- `humanizer-zh`: Chinese prose cleanup for AI-writing tells.
- `pdf`, `docx`, `baoyu-translate`, `baoyu-format-markdown`: paper input/output and translation support.

Use these as assistants, not authorities. Every citation, standard, policy, and factual claim must be verified against primary or authoritative sources.

## Candidate Papers

### Paper 1: Architecture / Design Science

Working title:

> A Lightweight Human-Reviewable Agent Architecture for Teaching Administration Workflows

Core question:

> How can a campus AI platform combine agent orchestration, source-cited retrieval, and deterministic workflow state to support teaching administration without delegating institutional decisions to an LLM?

Likely contribution:

- A reference architecture based on Hermes Agent, Web workbench, WeCom entry, RAG, workflow state, permission checks, and audit logs.
- A design pattern separating language tasks from business-rule execution.
- A first-release case study around one teaching-administration workflow.

Evidence to collect:

- Architecture decision records.
- Workflow state diagrams.
- Latency/cost observations.
- Failure cases from pure RAG, pure workflow, and free-form agent approaches.
- Human-review and audit examples.

Target venues:

- Education technology conference or journal.
- Information systems / design science venue.
- Chinese higher-education digital transformation venue.

### Paper 2: Knowledge Base / Source-Cited QA

Working title:

> Source-Cited Knowledge Support for Department-Level Teaching Management

Core question:

> What design and evaluation methods improve trustworthiness of AI answers over school policies, teaching notices, and departmental documents?

Likely contribution:

- A source-citation UI and response format for campus policy Q&A.
- A small evaluation protocol for citation coverage, answer faithfulness, abstention, and correction workflow.
- A practical ingestion and document-governance model.

Evidence to collect:

- Document taxonomy.
- Retrieval test set with synthetic or approved documents.
- Citation accuracy and unsupported-claim rates.
- User correction logs.
- Examples where the model correctly refuses or asks for more evidence.

Target venues:

- Educational informatization.
- Knowledge management.
- Applied NLP/RAG workshop or practitioner venue.

### Paper 3: Human-AI Collaboration / Workflow Study

Working title:

> Human-in-the-Loop AI Assistance for Teaching Department Routine Work

Core question:

> Which routine teaching-management and teacher tasks benefit from AI assistance, and where must human review remain explicit?

Likely contribution:

- A task taxonomy for teaching department deputy administrator and teacher workflows.
- A human-review state model for drafts, reminders, policy interpretations, and workflow consultations.
- A small formative study or diary study design.

Evidence to collect:

- Task inventory.
- Before/after time and quality proxies.
- Review actions: accepted, edited, rejected, escalated.
- Interview or diary notes after anonymization.
- Error categories and user trust boundaries.

Target venues:

- HCI in education.
- Educational management.
- Human-centered AI workshop.

### Paper 4: Developer Methodology / AI-Assisted Solo Development

Working title:

> Spec-First Solo Development of a Campus AI Platform with Agent Skills

Core question:

> How can one developer use AI agents, skills, OpenSpec, design-system constraints, and review gates to build a maintainable AI campus platform?

Likely contribution:

- A reproducible solo-development workflow.
- Skill routing rules and quality gates.
- An audit of where AI-assisted development helped, failed, or created risk.

Evidence to collect:

- Git history.
- OpenSpec changes.
- ADRs.
- Prompt/skill usage notes when safe to disclose.
- Bugs caught by review, tests, or UI audits.
- Cost and time logs if available.

Target venues:

- Software engineering education.
- AI-assisted software engineering workshop.
- Practitioner article rather than formal journal if evidence remains informal.

## Recommended Sequence

Phase 0: Research hygiene now.

- Create ADRs for architecture decisions.
- Keep synthetic fixtures separate from real school data.
- Log evaluation cases under a future `docs/research/evaluation/` directory.
- Record why each workflow requires human confirmation.

Phase 1: Write Paper 1 after the first deterministic workflow prototype.

- Use `academic-research-suite` in Socratic mode to narrow the final RQ.
- Use `deep-research` or `literature-review` for related work on LLM agents, RAG, workflow/state machines, human-in-the-loop AI, and higher-education administration systems.
- Use `academic-paper` for outline and draft.
- Use `academic-paper-reviewer` and `citation-audit` before sharing.

Phase 2: Write Paper 2 after source-cited QA has an evaluation set.

- Build a small benchmark with approved or synthetic campus documents.
- Track answer faithfulness, citation support, abstention, and correction behavior.
- Avoid claims about real institutional effectiveness unless evaluated in a real deployment.

Phase 3: Write Paper 3 only after real users or controlled proxy users interact with the platform.

- Prepare consent, anonymization, and data-retention rules first.
- Do not collect sensitive student/personnel details.
- Treat this as a formative study unless sample size and protocol justify stronger claims.

Phase 4: Write Paper 4 as a reflective engineering report if the development process itself becomes interesting.

- This is lower academic priority but useful for community sharing.

## Data And Ethics Rules

Do:

- Use synthetic, public, or formally approved documents for experiments.
- Keep raw research notes out of the app database.
- Separate product logs from research datasets.
- Document anonymization and exclusion rules.
- Mark AI-assisted writing and analysis transparently when required.

Do not:

- Use identifiable student, teacher, staff, personnel, disciplinary, psychological, financial, or grade data in papers.
- Publish screenshots containing internal school documents or identities.
- Claim measured improvement without a defined baseline and evaluation protocol.
- Let paper goals push the product toward over-automation.

## Research Artifact Layout

Recommended future structure:

```text
docs/research/
├── paper-roadmap.md
├── literature/
│   ├── search-log.md
│   ├── bibliography.bib
│   └── matrix.md
├── evaluation/
│   ├── qa-fixtures.md
│   ├── workflow-cases.md
│   └── metrics.md
├── papers/
│   ├── 01-architecture/
│   ├── 02-source-cited-qa/
│   ├── 03-human-ai-workflow/
│   └── 04-solo-ai-development/
└── ethics/
    ├── anonymization.md
    └── consent-notes.md
```

Do not commit private datasets, raw interviews, internal policies, or credentials.

## Skill Use By Stage

Scoping:

- Codex: `academic-research-suite` with Socratic narrowing.
- Shared: `deep-research`, `grill-with-docs`, `zoom-out`.

Literature review:

- `deep-research` for broad source discovery and synthesis.
- `literature-review` for a focused narrative review.
- `citation-audit` for reference existence and claim-source alignment.

Writing:

- `academic-paper` for outline, abstract, drafting, revision, and format conversion.
- `stop-slop` for English prose.
- `humanizer-zh` for Chinese prose.

Review:

- `academic-paper-reviewer` for simulated peer review.
- `scholar-evaluation` for methods and evidence critique.
- `citation-audit` before any external sharing.

Project linkage:

- `to-prd`, `to-issues`, OpenSpec, and ADRs should connect paper evidence to implementation decisions.

