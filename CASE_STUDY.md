# Case Study: AI Job Application OS

## 1. Problem

Software engineers can spend significant time repeatedly reading job descriptions, checking required skills against their CV, preparing tailored application material, and tracking applications.

The workflow is repetitive, inconsistent, and difficult to scale when many vacancies must be reviewed.

## 2. Target User

The target user is a software engineer applying for backend, AI, automation, data, or general software engineering roles.

## 3. Existing Workflow

1. Find a vacancy.
2. Read the complete job description.
3. Identify required skills and experience.
4. Compare the role with the candidate profile.
5. Decide whether to apply.
6. Write a tailored cover letter.
7. Submit the application.
8. Track the application status.

## 4. Goal

Create an AI-assisted workflow that reduces repetitive manual effort while keeping the final decision with the user.

Success criteria:

- Extract important job information.
- Compare required skills with the candidate profile.
- Produce a transparent match score.
- Identify missing skills and warnings.
- Generate a tailored cover letter.
- Handle incomplete or malformed input.
- Prevent duplicate saved applications.
- Keep a human approval step before saving an application.

## 5. Architecture

Job Description
→ Validation
→ Job Parser (local Ollama or deterministic fallback)
→ Structured Job Data
→ Rule-Based Match Engine
→ Recommendation + Warnings
→ Cover Letter Generator
→ Human Approval
→ SQLite Application Tracker

## 6. Why This Architecture

The project deliberately separates AI tasks from deterministic business logic.

AI is used for unstructured text extraction and cover-letter drafting.

The matching score is deterministic and auditable. This avoids making a high-impact decision based only on an opaque model response.

If the local LLM is unavailable, the parser falls back to rule-based extraction, so the application remains usable.

## 7. Reliability Measures

- Pydantic validation for API inputs and outputs.
- Minimum job-description length.
- Structured JSON requested from the local LLM.
- Deterministic fallback if the LLM request fails.
- Duplicate application protection in SQLite.
- Transparent score calculation.
- Human approval before an application record is stored.

## 8. Evaluation

Ten representative job scenarios are included in `evaluation/test_cases.json`.

The evaluation checks whether the system produces the expected recommendation for:

- Strong backend match
- Partial AI-engineering match
- Frontend role
- Java role
- QA automation role
- Data engineering role
- DevOps role
- Experience gap
- Language warning
- General software-engineering role

Run:

```bash
python evaluation/run_evaluation.py
```

Record the real output before submission. Do not report results that have not been executed.

## 9. Limitations

- The fallback parser is keyword-based and may miss uncommon technologies.
- Match quality depends on how clearly the job description states requirements.
- The scoring model currently gives 80% weight to required-skill fit and 20% to experience fit.
- Soft skills and company culture are not deeply modeled.
- Generated cover letters must be reviewed before use.
- The application does not auto-submit jobs because final submission should remain under human control.

## 10. Future Improvements

- CV upload and parsing.
- Multiple saved candidate profiles.
- Embedding-based semantic skill matching.
- Application analytics dashboard.
- Recruiter follow-up reminders.
- Multilingual cover-letter generation.
- Browser automation after explicit user approval.
- Configurable scoring weights.
