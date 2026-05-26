# Triage Labels

Use the default five-role triage vocabulary.

| Role | Label | Meaning |
| --- | --- | --- |
| Needs evaluation | `needs-triage` | A maintainer needs to decide what this is and whether it belongs in scope. |
| Waiting on reporter | `needs-info` | More context is required before a human or agent can act. |
| Ready for agent | `ready-for-agent` | The issue is specific enough for an AI-assisted implementation pass. |
| Ready for human | `ready-for-human` | The issue needs human judgment, approval, credentials, stakeholder input, or institutional context. |
| Will not fix | `wontfix` | The work will not be actioned in this repository. |

## Campus-Specific Triage Notes

Use `ready-for-human` instead of `ready-for-agent` whenever a task touches:

- official school policy interpretation without an approved source;
- grade, discipline, scholarship, personnel, psychological, financial, or official publication decisions;
- production credentials or write operations to school systems;
- ambiguous institutional responsibility.

Prefer `needs-info` when the issue lacks the target user, source document, workflow state, or verification path.

