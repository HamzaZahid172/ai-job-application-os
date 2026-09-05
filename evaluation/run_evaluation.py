import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.models import CandidateProfile
from backend.services.llm_client import parse_job
from backend.services.matcher import analyze_match

async def main():
    cases = json.loads(Path("evaluation/test_cases.json").read_text())
    candidate = CandidateProfile()
    rows = []

    for case in cases:
        parsed = await parse_job(case["job_description"])
        result = analyze_match(parsed, candidate)
        passed = result.recommendation == case["expected_recommendation"]
        rows.append({
            "name": case["name"],
            "expected": case["expected_recommendation"],
            "actual": result.recommendation,
            "score": result.match_score,
            "passed": passed,
        })

    passed_count = sum(1 for row in rows if row["passed"])
    print(json.dumps(rows, indent=2))
    print(f"\nPassed: {passed_count}/{len(rows)}")

if __name__ == "__main__":
    asyncio.run(main())
