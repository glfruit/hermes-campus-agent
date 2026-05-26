## ADDED Requirements

### Requirement: Reviewable draft generation
The system SHALL generate draft materials from selected role context, user request, and source-cited knowledge context.

#### Scenario: User generates a notice draft
- **WHEN** the user asks to generate a teaching notice or meeting material from cited knowledge
- **THEN** the system SHALL create a draft marked as requiring human review

### Requirement: Draft source basis
The system SHALL show the source basis and assumptions used to create a draft.

#### Scenario: User reviews generated draft
- **WHEN** a generated draft is displayed
- **THEN** the system SHALL show linked source references and assumptions next to the draft content

### Requirement: No automatic official publication
The system SHALL NOT publish, approve, or send generated official text automatically.

#### Scenario: User creates official-looking content
- **WHEN** a generated output resembles a notice, policy interpretation, meeting material, or official communication
- **THEN** the system SHALL keep it in a draft/review state and SHALL require human action outside the MVP to publish it
