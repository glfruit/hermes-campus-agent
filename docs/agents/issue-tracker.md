# Issue Tracker

This repository uses GitHub Issues for project work:

- Repository: `glfruit/hermes-campus-agent`
- Remote: `git@github.com:glfruit/hermes-campus-agent.git`
- Preferred CLI: `gh`

## How Agent Skills Should Use It

- `to-prd` may turn resolved product context into a PRD issue or issue-linked document.
- `to-issues` should break approved plans into vertical-slice GitHub issues.
- `triage` should classify incoming ideas, bugs, and tasks using the label vocabulary in `docs/agents/triage-labels.md`.
- `diagnose` may create or update an issue only after it has reproduced and minimized the bug.

## Issue Shape

Issues should be small enough for one focused agent session or one human work block. Prefer vertical slices that include UI, API, state, test, and documentation touchpoints when the feature crosses layers.

Each implementation issue should include:

- User or operational scenario.
- Files or modules likely involved.
- Acceptance criteria.
- Safety, source citation, permission, or audit requirements.
- Verification command or manual verification path.

## Local Notes

Use `.scratch/` only for temporary exploration notes that are not ready to become GitHub issues. Do not treat `.scratch/` as the source of truth for committed project planning.

