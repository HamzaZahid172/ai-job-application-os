import re
from pathlib import Path

from pypdf import PdfReader

from backend.models import CandidateProfile

KNOWN_CV_SKILLS = [
    "Python", "FastAPI", "Django", "Flask", "Java", "Spring Boot", "Kotlin",
    "JavaScript", "TypeScript", "Node.js", "React", "Angular", "Vue", "CSS",
    "Next.js", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQL", "Playwright", "Selenium",
    "Cypress", "WebDriverIO", "Puppeteer", "Pytest", "REST API", "GraphQL",
    "GitHub Actions", "GitLab CI", "Jenkins", "Bamboo", "CI/CD", "Linux",
    "Pandas", "NumPy", "Machine Learning", "LLM", "RAG", "LangChain", "OpenAI",
    "Ollama", "Kafka", "RabbitMQ", "Airflow", "Microservices", "Web Scraping",
    "ETL", "PDF Parsing", "Data Pipelines", "Postman", "Laravel", "HTML"
]


def extract_cv_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CV file not found: {file_path}")

    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    joined = "\n".join(pages).strip()
    if not joined:
        raise ValueError("No readable text was found in the uploaded PDF.")
    return joined


def _extract_name(text: str) -> str:
    for line in text.splitlines():
        value = line.strip()
        if value and len(value) <= 80 and not any(ch.isdigit() for ch in value):
            return value
    return "Candidate"


def _extract_years_experience(text: str) -> float:
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+(?:professional\s+)?experience",
        r"(\d+(?:\.\d+)?)\+?\s+years?\s+(?:professional\s+)?experience",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return 0.0


def _extract_languages(text: str) -> list[str]:
    supported = ["English", "German", "Urdu", "Punjabi", "French", "Spanish"]
    found = [lang for lang in supported if lang.lower() in text.lower()]
    return found or ["English"]


def _extract_target_roles(text: str) -> list[str]:
    roles = [
        "Backend Engineer", "AI Engineer", "Automation Engineer", "Data Engineer",
        "Software Engineer", "QA Automation Engineer", "Full Stack Engineer"
    ]
    found = [role for role in roles if role.lower() in text.lower()]
    return found or ["Software Engineer"]


def load_candidate_from_cv(file_path: str) -> CandidateProfile:
    text = extract_cv_text(file_path)
    lowered = text.lower()

    detected = [skill for skill in KNOWN_CV_SKILLS if skill.lower() in lowered]

    return CandidateProfile(
        name=_extract_name(text),
        years_experience=_extract_years_experience(text),
        target_roles=_extract_target_roles(text),
        skills=detected,
        languages=_extract_languages(text),
    )
