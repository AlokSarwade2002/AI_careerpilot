import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_job_description(job_description: str):

    prompt = f"""
You are an expert technical recruiter and AI career analyst.

Analyze the following job description.

Extract:

1. job_title
2. required_skills
3. nice_to_have_skills
4. experience_required
5. responsibilities
6. project_requirements

For project_requirements, identify the types of projects,
technical work, or practical experience that would demonstrate
the candidate can perform this job.

For example:

- Building RAG applications
- Developing REST APIs
- Building LLM applications
- Deploying applications using Docker
- Building ML pipelines
- Creating data analytics dashboards

Do NOT invent requirements that are not supported by the job
description.

Job Description:

{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {

                    "job_title": {
                        "type": "string"
                    },

                    "required_skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "nice_to_have_skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "experience_required": {
                        "type": "string"
                    },

                    "responsibilities": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "project_requirements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },

                "required": [
                    "job_title",
                    "required_skills",
                    "nice_to_have_skills",
                    "experience_required",
                    "responsibilities",
                    "project_requirements"
                ]
            }
        )
    )

    return response.parsed

def analyze_resume(resume_text: str):

    prompt = f"""
You are an expert resume parser.

Analyze the following resume and extract structured information.

Extract:

- name
- email
- phone
- skills
- education
- experience
- projects
- certifications

Important:

- Extract education exactly from the resume.
- Extract certifications exactly from the resume.
- Do not invent education or certifications.
- If education is not present, return an empty list.
- If certifications are not present, return an empty list.

Resume:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"
                    },
                    "skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "education": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "experience": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "projects": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "certifications": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "name",
                    "email",
                    "phone",
                    "skills",
                    "education",
                    "experience",
                    "projects",
                    "certifications"
                ]
            }
        )
    )

    return response.parsed