from pydantic import BaseModel


class JobDescription(BaseModel):
    job_description: str


class JobAnalysis(BaseModel):
    job_title: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    experience_required: str
    responsibilities: list[str]
    project_requirements: list[str]

class ResumeAnalysis(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]

class SkillMatchResult(BaseModel):
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[str]

class ProjectMatch(BaseModel):
    project: str
    relevance_score: float
    matched_requirements: list[str]
    reason: str

class CareerMatchResult(BaseModel):
    overall_score: float

    skill_score: float
    project_score: float
    experience_score: float
    responsibility_score: float
    education_score: float

    matched_skills: list[str]
    missing_skills: list[str]

    project_matches: list[ProjectMatch]

    strengths: list[str]
    gaps: list[str]