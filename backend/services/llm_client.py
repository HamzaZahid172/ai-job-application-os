import json
import re
from typing import Optional
import httpx

from backend.config import settings
from backend.models import ParsedJob, CandidateProfile

KNOWN_SKILLS = [
    "Python", "FastAPI", "Django", "Flask", "Java", "Spring Boot", "Kotlin",
    "JavaScript", "TypeScript", "Node.js", "React", "Angular", "Vue", "CSS", "Next.js",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQL",
    "Playwright", "Selenium", "Cypress", "Pytest", "REST API", "GraphQL",
    "GitHub Actions", "Jenkins", "CI/CD", "Linux", "Pandas", "NumPy",
    "Machine Learning", "LLM", "RAG", "LangChain", "OpenAI", "Ollama",
    "Kafka", "RabbitMQ", "Airflow", "Microservices", "Web Scraping"
]

def _fallback_parse(text: str) -> ParsedJob:
    lowered = text.lower()
    skills = [skill for skill in KNOWN_SKILLS if skill.lower() in lowered]

    title_match = re.search(
        r"(?:job title|position|role)\s*[:\-]\s*([^\n]+)", text, re.IGNORECASE
    )
    if title_match:
        title = title_match.group(1).strip()
    else:
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        title = first_line[:80] if first_line else "Software Engineering Role"

    company_match = re.search(r"(?:company)\s*[:\-]\s*([^\n]+)", text, re.IGNORECASE)
    company = company_match.group(1).strip() if company_match else None

    location_match = re.search(r"(?:location)\s*[:\-]\s*([^\n]+)", text, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else None

    years = None
    exp = re.search(r"(\d+(?:\.\d+)?)\+?\s+years?", lowered)
    if exp:
        years = float(exp.group(1))

    language_requirements = []
    for language in ["English", "German", "French", "Spanish"]:
        if language.lower() in lowered:
            language_requirements.append(language)

    return ParsedJob(
        title=title,
        company=company,
        location=location,
        required_skills=skills,
        preferred_skills=[],
        minimum_years_experience=years,
        language_requirements=language_requirements,
        summary="Structured from the supplied job description.",
    )

async def parse_job_with_ollama(text: str) -> Optional[ParsedJob]:
    if not settings.use_llm:
        return None

    prompt = f"""
You extract job requirements from job descriptions.
Return ONLY valid JSON with this exact structure:
{{
  "title": "string",
  "company": "string or null",
  "location": "string or null",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "minimum_years_experience": 0,
  "language_requirements": ["string"],
  "summary": "short string"
}}

Rules:
- Do not invent missing information.
- minimum_years_experience must be null if not stated.
- Keep skills concise and normalized.
- Output JSON only.

JOB DESCRIPTION:
{text}
"""

    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            raw = response.json().get("response", "")
            data = json.loads(raw)
            return ParsedJob(**data)
    except Exception:
        return None

async def parse_job(text: str) -> ParsedJob:

    parsed = await parse_job_with_ollama(text)

    if parsed:
        print("✅ JOB PARSER: OLLAMA LLM USED")
        return parsed

    print("⚠️ JOB PARSER: FALLBACK PARSER USED")

    return _fallback_parse(text)

async def generate_cover_letter(
    job_description: str,
    candidate: CandidateProfile,
    tone: str = "professional",
) -> str:
    prompt = f"""
Write a {tone} cover letter for this candidate.

Candidate:
Name: {candidate.name}
Years of experience: {candidate.years_experience}
Skills: {", ".join(candidate.skills)}
Target roles: {", ".join(candidate.target_roles)}

Job description:
{job_description}

Requirements:
- 250 to 350 words.
- Use only experience or skills explicitly present in the candidate profile.
- Do not fabricate employer names, metrics, degrees, or achievements.
- Mention 3 to 5 relevant skills.
- Keep it natural and specific.
- Return only the cover letter text.
"""

    if settings.use_llm:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/generate",
                    json={
                        "model": settings.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                    },
                )
                response.raise_for_status()
                text = response.json().get("response", "").strip()
                if text:
                    return text
        except Exception:
            pass

    parsed = _fallback_parse(job_description)
    relevant = [s for s in parsed.required_skills if s in candidate.skills][:5]
    skills_text = ", ".join(relevant) if relevant else ", ".join(candidate.skills[:5])

    return f"""Dear Hiring Team,

I am writing to express my interest in the {parsed.title} position. I bring {candidate.years_experience:g} years of software engineering experience with a strong focus on backend development, automation, and reliable software delivery.

My background includes hands-on work with {skills_text}. I am comfortable building maintainable services, integrating APIs, automating repetitive workflows, and working with modern engineering practices such as containerization and CI/CD. I also have experience working across testing and development responsibilities, which helps me approach software quality from both implementation and reliability perspectives.

This role is particularly interesting to me because it aligns with my current focus on backend engineering, automation, and AI-enabled software systems. I value practical solutions, clear ownership, and systems that are easy to operate and improve over time.

I would welcome the opportunity to discuss how my experience can contribute to your team. Thank you for considering my application.

Kind regards,
{candidate.name}"""
