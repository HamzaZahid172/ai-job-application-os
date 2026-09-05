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

The final project structure, scoring logic, error-handling approach, test expectations, CV workflow, and human-approval flow were reviewed and owned by the developer.

AI-generated suggestions were not treated as automatically correct. Code and documentation were reviewed, tested, and adjusted before inclusion.

## Changes made after review and evaluation

The project changed in several important ways during development:

- Replaced AI-only match scoring with deterministic and explainable scoring.
- Added structured validation around LLM output.
- Added a deterministic fallback when the local LLM is unavailable.
- Added real PDF CV parsing instead of relying only on a hardcoded candidate profile.
- Added browser-based CV upload with a default-CV fallback.
- Added duplicate protection for application records.
- Kept human approval before saving an application.
- Added automated Pytest coverage and a repeatable evaluation suite.
- Added GitHub Actions CI to run tests and verify the Docker image builds on pushes and pull requests.

## Evaluation-driven improvement

The initial deterministic evaluation produced 7/10 expected recommendations. Review of the failures identified missing fallback skill vocabulary and an overly permissive Apply threshold.

The fallback vocabulary and recommendation threshold were updated, and the same evaluation was run again. The final deterministic evaluation produced 10/10 expected recommendations.

## Important limitation

The system must not claim experience, skills, or achievements that are not present in the candidate profile. Generated cover letters must be reviewed by a human before use.
