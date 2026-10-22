from app.services.llm_service import client
from google.genai import types


def analyze_responsibility_match(
    responsibilities: list[str],
    experience: list[str],
    projects: list[str]
):

    prompt = f"""
You are an expert technical recruiter.

Determine how strongly the candidate demonstrates
each responsibility required by the target job.

Job Responsibilities:
{responsibilities}

Candidate Experience:
{experience}

Candidate Projects:
{projects}

For every responsibility:

1. Give an evidence score from 0 to 100.
2. Identify the evidence from the candidate's experience
   or projects.
3. Explain the reasoning.

IMPORTANT:

- Give high scores only when the resume explicitly
  demonstrates the responsibility.
- If the evidence is related but indirect, give a
  moderate score.
- If there is no evidence, give 0.
- Do not assume that a general AI/ML statement means
  the candidate built RAG or LLM systems.

Return only structured JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "responsibility_matches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "responsibility": {
                                    "type": "string"
                                },
                                "evidence_score": {
                                    "type": "number"
                                },
                                "evidence": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "reason": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "responsibility",
                                "evidence_score",
                                "evidence",
                                "reason"
                            ]
                        }
                    }
                },
                "required": [
                    "responsibility_matches"
                ]
            }
        )
    )

    return response.parsed["responsibility_matches"]