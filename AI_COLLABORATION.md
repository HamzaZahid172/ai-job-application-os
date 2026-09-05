# AI Collaboration Note

AI tools were used as an engineering assistant during the project.

## AI-assisted activities

- Brainstorming the project scope.
- Reviewing system architecture.
- Drafting implementation ideas.
- Generating test-case ideas.
- Improving documentation.
- Identifying failure scenarios.
- Reviewing code structure.

## Human-owned decisions

The final project structure, scoring logic, error-handling approach, test expectations, and human-approval workflow were reviewed and owned by the developer.

AI-generated suggestions were not treated as automatically correct. Code and documentation were reviewed before inclusion.

## Manual corrections

Examples of changes that should be documented during the real build:

- Removing AI-only match scoring in favor of deterministic scoring.
- Adding structured validation around LLM output.
- Adding a fallback when the LLM is unavailable.
- Adding duplicate protection for application records.
- Keeping human approval before saving or submitting an application.

## Important limitation

The system must not claim experience, skills, or achievements that are not present in the candidate profile. Generated cover letters must be reviewed before use.
