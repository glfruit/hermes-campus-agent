## ADDED Requirements

### Requirement: Role-aware campus workbench shell
The system SHALL provide a Web workbench shell with explicit role context for teaching administrator and teacher workflows.

#### Scenario: User switches role context
- **WHEN** the user selects the teaching administrator or teacher role
- **THEN** the workbench SHALL update navigation, suggested actions, and workspace context for that role

#### Scenario: User opens the workbench
- **WHEN** the user visits the campus Web app
- **THEN** the first screen SHALL be the operational workbench rather than a marketing or landing page

### Requirement: Operational layout
The system SHALL use a workbench layout that exposes conversation/work content, source detail, draft status, and task context without relying on a chat-only interface.

#### Scenario: User reviews an answer
- **WHEN** a knowledge answer is displayed
- **THEN** the system SHALL show the answer, supporting sources, and available follow-up actions in the same work surface

### Requirement: No production data dependency
The system SHALL run locally with fixture data and without production credentials.

#### Scenario: Developer starts the MVP app
- **WHEN** the developer runs the campus Web app locally
- **THEN** the app SHALL render the core workbench using local fixture data only
