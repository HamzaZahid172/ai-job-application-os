# AI Job Application OS

A local-first AI-assisted application that reads a candidate CV, analyzes a job description, calculates an explainable match score, identifies skill gaps, generates a tailored cover letter, and stores approved applications.

## What this project demonstrates

- PDF CV parsing
- Default CV fallback when no new CV is uploaded
- Uploading a different PDF CV from the browser UI
- Local LLM job-description parsing with Ollama
- Deterministic fallback parsing when Ollama is unavailable
- Explainable CV-to-job matching
- Matching and missing skills
- Experience and language warnings
- Apply / Maybe Apply / Low Match recommendations
- Cover-letter generation using candidate + job context
- Human approval before saving an application
- SQLite persistence
- Duplicate-application protection
- FastAPI backend and Swagger docs
- Dockerized backend runtime
- Unit tests with Pytest
- Repeatable evaluation scenarios

## Architecture

```text
PDF CV -----------------------> CV Parser ------------------+
                                                            |
                                                            v
                                                     Candidate Profile
                                                            |
Job Description -> Ollama LLM -> Structured Job Data -------+
                  |                                         |
                  +-> fallback parser if LLM fails          v
                                                   Deterministic Matcher
                                                            |
                          +---------------------------------+------------------+
                          |                                 |                  |
                          v                                 v                  v
                     Match Score                      Skill Gaps        Recommendation
                                                                                |
                                                                                v
                                                                     Cover Letter Generator
                                                                                |
                                                                                v
                                                                        Human Approval
                                                                                |
                                                                                v
                                                                              SQLite
```

Docker packages and runs the FastAPI application in a reproducible environment. Ollama can run locally on the host machine and is accessed by the backend.

## Project structure

```text
ai-job-application-os/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   ├── database.py
│   └── services/
│       ├── cv_parser.py
│       ├── llm_client.py
│       └── matcher.py
├── frontend/
│   └── index.html
├── data/
│   └── cv/
│       └── .gitkeep
├── tests/
│   ├── conftest.py
│   ├── test_cv_parser.py
│   └── test_matcher.py
├── evaluation/
│   ├── test_cases.json
│   ├── run_evaluation.py
│   └── results.md
├── CASE_STUDY.md
├── AI_COLLABORATION.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

# Quick start

## 1. Prerequisites

Install:

- Python 3.11+
- Git
- Ollama if you want local LLM support
- Docker Desktop if you want to run the containerized version

## 2. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

```bash
cp .env.example .env
```

Example local configuration:

```env
APP_NAME=AI Job Application OS
DATABASE_URL=sqlite:///./data/applications.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
USE_LLM=true
```

To test deterministic behavior without an LLM:

```env
USE_LLM=false
```

## 5. Start Ollama

Check installed models:

```bash
ollama list
```

If the configured model is not installed:

```bash
ollama pull llama3.2:3b
```

Start the Ollama server:

```bash
ollama serve
```

Optional direct health test:

```bash
curl http://localhost:11434/api/tags
```

## 6. Start the FastAPI application

```bash
uvicorn backend.main:app --reload
```

Open:

```text
http://localhost:8000
```

Swagger API docs:

```text
http://localhost:8000/docs
```

# CV behavior

## Default CV

If no CV has been uploaded through the UI, the application uses the configured/default PDF CV from `data/cv/`.

Use **Show Current Candidate** in the UI to confirm which candidate profile is active.

## Upload another CV

In the browser UI:

1. Click **Choose File**.
2. Select a PDF CV.
3. Click **Upload & Parse CV**.
4. Click **Show Current Candidate** to verify extracted data.
5. Analyze the same job again to demonstrate that a different CV can produce a different match score.

This is a useful demo because it proves the system is using the active CV rather than a fixed hardcoded profile.

# How the score works

The current matching formula is deterministic:

```text
Final Score = Skill Fit × 80% + Experience Fit × 20%
```

Typical recommendation thresholds:

```text
85-100  -> Apply
60-84   -> Maybe Apply
0-59    -> Low Match
```

The LLM does not directly invent the final percentage. The LLM helps structure the job description; the matcher computes the score.

# Manual demo test cases

For exact/repeatable score testing, set:

```env
USE_LLM=false
```

Restart the backend after changing `.env`.

## Test A: Strong match

```text
Role: Automation Engineer

Required skills:
Python
JavaScript
TypeScript
Playwright
Selenium
Cypress
Docker
AWS

Minimum 5 years experience.
English required.
```

Expected behavior for a CV containing all listed skills:

```text
Very high score, normally close to 100%
Recommendation: Apply
```

## Test B: Medium match

```text
Role: Senior Software Engineer

Required skills:
Python
JavaScript
TypeScript
Node.js
Docker
AWS
Kubernetes
Terraform

Minimum 5 years experience.
English required.
```

If 6 of 8 skills match and experience is satisfied:

```text
Skill fit = 75%
75 × 0.80 = 60
Experience contribution = 20
Final score = 80%
Recommendation: Maybe Apply
```

## Test C: Around 60%

```text
Role: Backend Platform Engineer

Required skills:
Python
JavaScript
Docker
AWS
Kubernetes
Terraform
Kafka
Redis

Minimum 5 years experience.
English required.
```

If 4 of 8 skills match:

```text
Skill fit = 50%
50 × 0.80 = 40
Experience contribution = 20
Final score = 60%
Recommendation: Maybe Apply
```

## Test D: Low match

```text
Role: Java Cloud Engineer

Required skills:
Java
Spring Boot
Kotlin
Kubernetes
Terraform
Kafka
Azure
GCP

Minimum 5 years experience.
English required.
```

For a CV with very few of these skills:

```text
Low score
Recommendation: Low Match
```

## Test E: Experience-gap test

```text
Role: Principal Automation Architect

Required skills:
Python
JavaScript
TypeScript
Playwright
Selenium
Docker
AWS
CI/CD

Minimum 12 years experience.
English required.
```

A candidate can have a strong skill match but still receive an experience warning. This demonstrates that the score is not based only on keywords.

# LLM demo test

Set:

```env
USE_LLM=true
```

Use a natural job description instead of a rigid list:

```text
We are looking for a senior engineer to join our automation platform team.
The successful candidate will build internal tools using Python and TypeScript,
create browser automation workflows with Playwright, deploy containerized
services using Docker, and maintain cloud infrastructure in AWS.
The engineer will also work with REST APIs and CI/CD pipelines.
Candidates should have at least five years of professional software engineering
experience. English is the primary working language. The role is based in Berlin.
```

The important demo point is that the LLM converts unstructured text into structured job requirements before matching.

If your backend includes logging such as:

```text
JOB PARSER: OLLAMA LLM USED
```

show that briefly in the demo.

# Cover-letter test

After analyzing a job, click **Generate Cover Letter**.

Check that the letter:

- uses skills present in the active CV
- relates those skills to the job description
- does not invent employers, degrees, achievements, or technologies not supported by the candidate profile

# Persistence and reliability test

Save an application once through **Approve & Save Application**.

Save the same company + role again.

Expected behavior:

```text
409 Conflict
```

This demonstrates duplicate-application protection.

# Unit tests

Activate the virtual environment first:

```bash
source .venv/bin/activate
```

Run concise tests:

```bash
pytest -q
```

For a presentation-friendly output:

```bash
pytest -v
```

The CV parser test should verify that a PDF can be parsed and produces a valid candidate profile. It should not assume every CV contains a particular technology such as Python.

# Evaluation suite

For a repeatable evaluation run, disable LLM variability:

```bash
USE_LLM=false python evaluation/run_evaluation.py
```

or set `USE_LLM=false` in `.env` and restart the app.

The evaluation package covers scenarios such as:

- strong Python/backend match
- AI engineer partial match
- frontend role
- Java role
- QA automation role
- data engineer role
- DevOps role
- experience gap
- language requirement
- mixed software-engineering role

Record the real output from your machine before submission. Do not claim a test result you did not run.

# Docker

## Why Docker is used

Docker packages the backend code, Python runtime, and dependencies into a reproducible container. A reviewer can run the same environment without manually recreating your Python setup.

## Run with Docker

```bash
docker compose down
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

When Ollama runs on the Mac host, the container can access it through:

```text
http://host.docker.internal:11434
```

Docker logs mainly prove that the container, Uvicorn server, and API requests are running. Ollama logs are separate because Ollama is the local LLM server.

# Suggested final demo flow

A 4-5 minute demo can follow this order:

1. **Problem**: explain why job evaluation is repetitive.
2. **Architecture**: CV parser + Ollama + matcher + cover letter + SQLite.
3. **Docker**: show the container running for 10-15 seconds.
4. **Default CV**: show the current candidate without uploading a new file.
5. **Strong/medium/low job tests**: show at least two different match levels.
6. **Ollama**: briefly show that the LLM handled a natural-language job description.
7. **Upload a second CV**: run the same job again and show that the result changes.
8. **Cover letter**: generate a tailored letter.
9. **Human approval**: save the application.
10. **Reliability**: demonstrate duplicate protection or fallback behavior.
11. **Tests**: show `pytest -v`.
12. **Evaluation**: show the evaluation script output.

# Suggested presentation explanation

Use this wording:

> The LLM is responsible for understanding unstructured job descriptions and generating application text. The final match score is calculated with deterministic logic so the result remains explainable and repeatable. The candidate keeps final approval before an application is stored.

For Docker:

> I containerized the FastAPI backend so the runtime and dependencies are reproducible on another machine.

For Ollama:

> Ollama runs the LLM locally, which allows the project to demonstrate AI functionality without depending on a paid cloud API.

# Submission checklist

Before submitting:

- [ ] Application runs locally
- [ ] Docker container starts successfully
- [ ] Ollama model is available
- [ ] Default CV parses correctly
- [ ] Uploaded CV parses correctly
- [ ] Same job produces different results for different CVs when appropriate
- [ ] Strong, medium, and low match scenarios are demonstrated
- [ ] Cover letter is generated without unsupported claims
- [ ] Duplicate application protection works
- [ ] `pytest -v` passes
- [ ] Evaluation script runs successfully
- [ ] README is complete
- [ ] CASE_STUDY.md is complete
- [ ] AI_COLLABORATION.md is complete
- [ ] Demo video is accessible
- [ ] GitHub repository is accessible to reviewers
- [ ] `.env`, personal CVs, and local database files are not accidentally committed

# GitHub safety

Recommended `.gitignore` entries:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
data/*.db
data/cv/*
!data/cv/.gitkeep
.DS_Store
```

Before pushing:

```bash
git status
```

Make sure personal CV PDFs, `.env`, and `applications.db` are not being committed.

# GitHub repository setup

Suggested repository name:

```text
ai-job-application-os
```

Example commands:

```bash
git init
git add .
git commit -m "Build AI Job Application OS"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-job-application-os.git
git push -u origin main
```

# Main technologies

- Python
- FastAPI
- Uvicorn
- Ollama
- Pydantic
- PyPDF
- SQLite
- HTML/CSS/JavaScript
- Pytest
- Docker

# Limitations

- PDF text extraction works best with text-based PDFs rather than scanned-image CVs.
- The fallback parser is keyword-based and may miss uncommon skills.
- Match quality depends on the quality of job-description extraction.
- The scoring weights are intentionally simple and should be tuned for production use.
- The generated cover letter must be reviewed by a human.
- The system does not automatically submit job applications.

# Future improvements

- LLM-assisted CV structuring
- semantic skill matching with embeddings
- multiple saved candidate profiles
- configurable score weights
- richer application analytics
- multilingual cover letters
- recruiter follow-up reminders
- optional browser automation after explicit human approval
