from backend.models import CandidateProfile, ParsedJob, JobAnalysisResponse

ALIASES = {
    "node": "node.js",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "js": "javascript",
    "ts": "typescript",
    "rest": "rest api",
    "ml": "machine learning",
}

def normalize(value: str) -> str:
    cleaned = value.strip().lower()
    return ALIASES.get(cleaned, cleaned)

def analyze_match(job: ParsedJob, candidate: CandidateProfile) -> JobAnalysisResponse:
    candidate_skills = {normalize(s): s for s in candidate.skills}
    required = [s for s in job.required_skills if s.strip()]

    matching = []
    missing = []

    for skill in required:
        key = normalize(skill)
        if key in candidate_skills:
            matching.append(candidate_skills[key])
        else:
            missing.append(skill)

    if required:
        skill_score = round(len(matching) / len(required) * 100)
    else:
        skill_score = 50

    warnings = []

    experience_score = 100
    if job.minimum_years_experience is not None:
        if candidate.years_experience < job.minimum_years_experience:
            gap = job.minimum_years_experience - candidate.years_experience
            experience_score = max(0, round(100 - gap * 20))
            warnings.append(
                f"Role requests {job.minimum_years_experience:g}+ years; "
                f"candidate profile has {candidate.years_experience:g} years."
            )

    language_lower = {l.lower() for l in candidate.languages}
    for language in job.language_requirements:
        if language.lower() not in language_lower:
            warnings.append(f"Language requirement may be missing: {language}.")

    score = round(skill_score * 0.8 + experience_score * 0.2)
    score = max(0, min(100, score))

    if score >= 85:
        recommendation = "Apply"
    elif score >= 60:
        recommendation = "Maybe Apply"
    else:
        recommendation = "Low Match"

    explanation = (
        f"Matched {len(matching)} of {len(required)} explicitly detected required skills. "
        f"Skill fit contributes 80% of the score and experience fit contributes 20%. "
        "The score is advisory and the final application decision remains with the user."
    )

    return JobAnalysisResponse(
        parsed_job=job,
        match_score=score,
        matching_skills=matching,
        missing_skills=missing,
        warnings=warnings,
        recommendation=recommendation,
        explanation=explanation,
    )
