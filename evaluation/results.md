# Evaluation Results

Evaluation mode: deterministic fallback (`USE_LLM=false`) for reproducibility.

| # | Scenario | Expected | Actual | Score | Result |
|---|---|---|---|---:|---|
| 1 | Python backend strong match | Apply | Apply | 100 | PASS |
| 2 | AI engineer partial match | Maybe Apply | Maybe Apply | 74 | PASS |
| 3 | Frontend role | Maybe Apply | Maybe Apply | 60 | PASS |
| 4 | Java role | Low Match | Low Match | 20 | PASS |
| 5 | QA automation role | Apply | Apply | 89 | PASS |
| 6 | Data engineer | Maybe Apply | Maybe Apply | 74 | PASS |
| 7 | DevOps role | Maybe Apply | Maybe Apply | 60 | PASS |
| 8 | Experience gap | Maybe Apply | Maybe Apply | 80 | PASS |
| 9 | German language requirement | Apply | Apply | 100 | PASS |
| 10 | Mixed software role | Apply | Apply | 100 | PASS |

**Result: 10/10 scenarios passed.**

## Evaluation Notes

The initial baseline produced 7/10 expected recommendations. The evaluation exposed three weaknesses:

1. CSS and Next.js were not included in the fallback skill vocabulary, causing the frontend role to appear stronger than intended.
2. Airflow was missing from the fallback skill vocabulary, causing the data-engineering role to appear stronger than intended.
3. An 80-point score was treated as an automatic Apply even when a large experience gap existed.

Corrections made:

- Added CSS, Next.js, and Airflow to the fallback vocabulary.
- Increased the Apply threshold from 80 to 85, keeping 60–84 as Maybe Apply.

After these changes, all ten deterministic evaluation scenarios matched their expected recommendation.

These results test recommendation behavior only. They do not prove that every real-world job description will be parsed perfectly, especially when an LLM is used. Human review remains required.
