from app.services.llm_service import client
from google.genai import types


def analyze_education_match(
    education: list[str],
    certifications: list[str],
    job_description: str
):
    prompt = f"""
You are an expert technical recruiter.

Evaluate how well the candidate's education and certifications
match the target job requirements.

Candidate Education:
{education}

Candidate Certifications:
{certifications}

Job Description:
{job_description}

Rules:

1. Identify whether the job has an explicit education requirement.
2. Identify whether the job has certification requirements.
3. Compare the candidate's education and certifications
   against those requirements.
4. Give an education/certification score from 0 to 100.
5. If the job has NO education or certification requirement,
   give a score of 100 because there is no educational
   requirement to penalize.
6. Do not assume a certification or degree that is not present.
7. Do not give credit for unrelated qualifications.

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
                    "score": {
                        "type": "number"
                    },
                    "education_requirements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "certification_requirements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "matched_requirements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "missing_requirements": {
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
                    "score",
                    "education_requirements",
                    "certification_requirements",
                    "matched_requirements",
                    "missing_requirements",
                    "reason"
                ]
            }
        )
    )

    return response.parsed