## ADDED Requirements

### Requirement: Source-cited campus knowledge answers
The system SHALL answer campus knowledge questions using retrieved source snippets and visible citation metadata.

#### Scenario: Question has matching evidence
- **WHEN** the user asks a question covered by fixture knowledge documents
- **THEN** the system SHALL provide an answer with citations that include source title, department, version or effective date, and excerpt

### Requirement: Evidence abstention
The system SHALL avoid unsupported answers when available sources do not contain enough evidence.

#### Scenario: Question lacks matching evidence
- **WHEN** the user asks a question not supported by the available knowledge fixtures
- **THEN** the system SHALL state that the current knowledge base is insufficient and SHALL NOT fabricate policy details

### Requirement: Source visibility
The system SHALL make supporting source excerpts inspectable near the generated answer.

#### Scenario: User inspects citations
- **WHEN** an answer includes citations
- **THEN** the system SHALL show each cited source excerpt and metadata without requiring hover-only interaction
