from pathlib import Path
from backend.services.cv_parser import load_candidate_from_cv


def test_default_cv_parses_when_present():
    path = Path("data/cv/DEFAULT_CV.pdf")

    if not path.exists():
        return

    candidate = load_candidate_from_cv(str(path))

    assert candidate.name is not None
    assert candidate.name.strip() != ""

    assert candidate.years_experience >= 0

    assert isinstance(candidate.skills, list)
    assert len(candidate.skills) > 0

    assert all(
        isinstance(skill, str) and skill.strip()
        for skill in candidate.skills
    )