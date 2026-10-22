from app.services.llm_service import client
from google.genai import types


def analyze_experience_match(
    experience: list[str],
    required_experience: str,
    responsibilities: list[str]
):

    prompt = f"""
You are an expert technical recruiter.

Evaluate how well the candidate's professional experience
matches the experience requirements and responsibilities
of the target job.

Candidate Experience:
{experience}

Required Experience:
{required_experience}

Job Responsibilities:
{responsibilities}

For each experience entry:

1. Give a relevance score from 0 to 100.
2. Identify relevant responsibilities.
3. Explain the relevance.
4. Do not give credit for experience that is not supported
   by the candidate's actual experience description.

Return only valid JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "experience_matches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "experience": {
                                    "type": "string"
                                },
                                "relevance_score": {
                                    "type": "number"
                                },
                                "matched_responsibilities": {
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
                                "experience",
                                "relevance_score",
                                "matched_responsibilities",
                                "reason"
                            ]
                        }
                    }
                },
                "required": [
                    "experience_matches"
                ]
            }
        )
    )

    return response.parsed["experience_matches"]