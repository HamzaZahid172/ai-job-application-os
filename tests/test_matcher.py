from backend.models import CandidateProfile, ParsedJob
from backend.services.matcher import analyze_match

def test_high_match():
    candidate = CandidateProfile(
        skills=["Python", "FastAPI", "Docker", "AWS"],
        years_experience=7
    )
    job = ParsedJob(
        title="Backend Engineer",
        required_skills=["Python", "FastAPI", "Docker", "AWS"],
        preferred_skills=[],
        minimum_years_experience=5,
        language_requirements=["English"],
        summary="Backend role"
    )
    result = analyze_match(job, candidate)
    assert result.match_score == 100
    assert result.recommendation == "Apply"

def test_missing_experience_adds_warning():
    candidate = CandidateProfile(
        skills=["Python", "FastAPI"],
        years_experience=3
    )
    job = ParsedJob(
        title="Senior Backend Engineer",
        required_skills=["Python", "FastAPI"],
        preferred_skills=[],
        minimum_years_experience=7,
        language_requirements=[],
        summary="Senior role"
    )
    result = analyze_match(job, candidate)
    assert result.warnings
    assert result.match_score < 100

def test_low_match():
    candidate = CandidateProfile(
        skills=["Python"],
        years_experience=7
    )
    job = ParsedJob(
        title="Java Engineer",
        required_skills=["Java", "Spring Boot", "Kubernetes", "Terraform"],
        preferred_skills=[],
        minimum_years_experience=5,
        language_requirements=[],
        summary="Java role"
    )
    result = analyze_match(job, candidate)
    assert result.recommendation == "Low Match"
