# Final Demo Script and Submission Checklist

Use this guide for the final 4–5 minute presentation video.

## Screen 1: GitHub repository / README

Say:

> Hello, this is my AI Job Application OS. The goal of this project is to help a job seeker compare a job description with a candidate CV, identify matching and missing skills, generate a tailored cover letter, and track approved applications. The system combines PDF CV parsing, a local LLM through Ollama, deterministic matching logic, FastAPI, SQLite, Docker, automated tests, and GitHub Actions.

## Screen 2: README architecture section

Say:

> The workflow starts with two main inputs: a candidate CV and a job description. The CV parser extracts the candidate profile, while Ollama converts an unstructured job description into structured job requirements. These two inputs are then passed to a deterministic matcher, which calculates the score, identifies skill gaps, and produces a recommendation. The LLM is used for language understanding, but the final percentage is calculated by transparent business logic.

## Screen 3: Docker Desktop or terminal

Show the running container and port 8000.

Say:

> The FastAPI backend is containerized with Docker. Docker is not doing the AI processing itself. Its purpose is to package the runtime and dependencies into a reproducible environment so another developer or reviewer can run the application consistently.

## Screen 4: Ollama terminal

Show `ollama serve` or a successful request in the logs.

Say:

> Ollama runs the local language model. The backend communicates with Ollama when it needs to understand a natural-language job description or generate a cover letter. This keeps the AI workflow local and avoids depending entirely on a paid cloud API.

## Screen 5: Application UI and default candidate

Click **Show Current Candidate**.

Say:

> If no new CV is uploaded, the system uses the configured default CV. The PDF is parsed into a candidate profile containing detected skills and experience. This means the matching result is based on CV content rather than a fixed score.

## Screen 6: Analyze a strong match

Paste this example:

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

Click **Analyze Job**.

Say:

> In this example, the role matches many of the candidate's skills. The application shows the overall match score, matching skills, missing skills, warnings, and the final recommendation. The score itself is deterministic, so the LLM does not invent the percentage.

## Screen 7: Upload another CV

Upload a second PDF CV, then click **Show Current Candidate**.

Say:

> The user can also upload another CV directly from the browser. Once uploaded, it becomes the active candidate profile. I can now analyze the same job again and demonstrate that a different CV can produce a different score and different skill gaps.

## Screen 8: Analyze the same job again

Use the same job description.

Say:

> I am using the same job description again, but with a different CV. The result changes because the system is matching against the active candidate profile rather than returning a fixed output.

## Screen 9: Generate a cover letter

Click **Generate Cover Letter**.

Say:

> After evaluating the job, the user can generate a tailored cover letter. The model receives the job description and candidate profile, and it is instructed not to fabricate unsupported skills or experience.

## Screen 10: Human approval and duplicate protection

Save one application, then try to save the same company and role again.

Say:

> The workflow keeps a human approval step before saving an application. The AI can recommend and generate content, but the final action remains with the user. Duplicate applications are also rejected instead of being stored silently.

## Screen 11: Unit tests

Run:

```bash
source .venv/bin/activate
pytest -v
```

Say:

> I created automated unit tests for the CV parser and matching logic. These tests verify successful CV parsing, strong and low match behavior, and experience-gap warnings.

## Screen 12: Evaluation suite

Run:

```bash
USE_LLM=false python evaluation/run_evaluation.py
```

Say:

> I also created a repeatable evaluation suite with ten job scenarios. For this evaluation, I disable the LLM so the same inputs produce consistent results. The current deterministic evaluation passes all ten expected recommendation scenarios. The LLM is demonstrated separately for natural-language understanding.

## Screen 13: GitHub Actions

Open the **Actions** tab and show the green CI run.

Say:

> I added GitHub Actions for continuous integration. On every push to main and on pull requests, GitHub installs the dependencies, runs the automated tests, and only after the tests pass does it build the Docker image. This helps catch regressions before code changes are accepted.

## Screen 14: Final screen

Return to the README or main application.

Say:

> In summary, this project combines CV parsing, local LLM processing, explainable deterministic matching, cover-letter generation, human approval, application persistence, automated testing, evaluation, Docker-based deployment, and continuous integration. The key design principle is to use AI where language understanding is useful while keeping scoring and final actions transparent, testable, and under user control.

# Final submission checklist

Before submitting:

- [ ] `pytest -v` passes locally.
- [ ] `USE_LLM=false python evaluation/run_evaluation.py` reports 10/10 expected scenarios.
- [ ] Docker container starts successfully on port 8000.
- [ ] Ollama works with `USE_LLM=true` for the live AI demo.
- [ ] Default CV flow works.
- [ ] Uploaded CV flow works and changes the candidate profile.
- [ ] Cover letter generation works.
- [ ] Duplicate application protection works.
- [ ] GitHub Actions CI is green.
- [ ] Final demo video is uploaded and accessible to reviewers.
- [ ] GitHub repository link is submitted.
- [ ] Case study and AI collaboration note are included.
- [ ] No `.env`, database file, personal CV, or secrets are committed.
