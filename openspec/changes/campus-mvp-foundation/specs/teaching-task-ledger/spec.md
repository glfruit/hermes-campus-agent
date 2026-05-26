## ADDED Requirements

### Requirement: Teaching task ledger
The system SHALL provide a lightweight task ledger for teaching operations and teacher follow-up work.

#### Scenario: User views tasks
- **WHEN** the workbench loads
- **THEN** the system SHALL show teaching tasks with title, role, status, optional due date, and origin

### Requirement: Create task from AI-assisted context
The system SHALL allow users to create a task from a knowledge answer or generated draft.

#### Scenario: User saves follow-up task
- **WHEN** the user chooses to save an answer or draft as a task
- **THEN** the task SHALL retain references to the originating source IDs or draft context

### Requirement: Human-review task states
The system SHALL represent task state in a way that separates draft, review, confirmed, and completed work.

#### Scenario: User sees draft-origin task
- **WHEN** a task is created from generated content
- **THEN** the task SHALL start in a draft or reviewing state rather than a completed or approved state
