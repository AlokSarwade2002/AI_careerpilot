from app.services.llm_service import client
from google.genai import types


def analyze_project_match(
    projects: list[str],
    project_requirements: list[str]
):
    prompt = f"""
You are an expert technical recruiter.

Determine how relevant each candidate project is
to the requirements of the target job.

Candidate Projects:
{projects}

Job Project Requirements:

{chr(10).join(
    f"{i}: {requirement}"
    for i, requirement in enumerate(project_requirements)
)}

For each project:

1. Give a relevance score from 0 to 100.
2. Identify which job requirements the project satisfies.
3. Return the INDEX numbers of those requirements.
4. Explain why the project is relevant.

IMPORTANT:

- Only select requirement indexes that are actually supported
  by the project description.
- Do not infer unsupported technologies.
- A project can match multiple requirements.
- Use the exact requirement indexes provided above.

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
                    "project_matches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "project": {
                                    "type": "string"
                                },
                                "relevance_score": {
                                    "type": "number"
                                },
                                "matched_requirement_indexes": {
                                    "type": "array",
                                    "items": {
                                        "type": "integer"
                                    }
                                },
                                "reason": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "project",
                                "relevance_score",
                                "matched_requirement_indexes",
                                "reason"
                            ]
                        }
                    }
                },
                "required": [
                    "project_matches"
                ]
            }
        )
    )

    return response.parsed["project_matches"]