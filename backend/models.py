from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str = "Hamza Zahid Butt"
    years_experience: float = 7.0
    target_roles: List[str] = Field(default_factory=lambda: [
        "Backend Engineer",
        "AI Engineer",
        "Automation Engineer",
        "Data Engineer",
        "Software Engineer",
    ])
    skills: List[str] = Field(default_factory=lambda: [
        "Python", "FastAPI", "JavaScript", "TypeScript", "Node.js", "React",
        "Docker", "AWS", "PostgreSQL", "SQL", "MongoDB", "Redis",
        "Playwright", "Selenium", "Cypress", "REST API", "GitHub Actions",
        "CI/CD", "Linux", "Web Scraping", "Pandas"
    ])
    languages: List[str] = Field(default_factory=lambda: ["English", "Urdu", "German"])

class JobAnalysisRequest(BaseModel):
    job_description: str = Field(min_length=40)
    candidate: Optional[CandidateProfile] = None

class ParsedJob(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    minimum_years_experience: Optional[float] = None
    language_requirements: List[str] = Field(default_factory=list)
    summary: str

class JobAnalysisResponse(BaseModel):
    parsed_job: ParsedJob
    match_score: int = Field(ge=0, le=100)
    matching_skills: List[str]
    missing_skills: List[str]
    warnings: List[str]
    recommendation: Literal["Apply", "Maybe Apply", "Low Match"]
    explanation: str

class CoverLetterRequest(BaseModel):
    job_description: str = Field(min_length=40)
    candidate: Optional[CandidateProfile] = None
    tone: Literal["professional", "concise", "confident"] = "professional"

class CoverLetterResponse(BaseModel):
    cover_letter: str

class ApplicationCreate(BaseModel):
    company: str
    role: str
    match_score: int = Field(ge=0, le=100)
    status: str = "Reviewed"
    notes: Optional[str] = None

class ApplicationOut(ApplicationCreate):
    id: int
    created_at: str
