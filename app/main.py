from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import tempfile
import os
from app.services.llm_service import analyze_job_description
from app.services.project_matcher import analyze_project_match
from app.services.resume_parser import extract_text_from_pdf
from app.services.llm_service import analyze_resume
from app.models.schemas import (
    JobDescription,
    JobAnalysis,
    ResumeAnalysis
)
from app.services.experience_matcher import analyze_experience_match
from app.services.responsibility_matcher import analyze_responsibility_match
from app.services.education_matcher import analyze_education_match
from app.services.career_matcher import match_candidate


app = FastAPI(
    title="AI CareerPilot",
    description="AI-powered job and career automation agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI CareerPilot 🚀",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze-job", response_model=JobAnalysis)
def analyze_job(job: JobDescription):

    return analyze_job_description(
        job.job_description
    )

@app.post("/analyze-resume", response_model=ResumeAnalysis)
async def analyze_resume_endpoint(
    file: UploadFile = File(...)
):

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:

        resume_text = extract_text_from_pdf(
            temp_file_path
        )

        analysis = analyze_resume(
            resume_text
        )

        return analysis

    finally:

        os.remove(temp_file_path)

@app.post("/test-project-match")
def test_project_match():

    projects = [
        """
        RAG-Based AI Assistant for Document Question Answering.
        Built using Python, LangChain, RAG, FastAPI, FAISS, Docker
        and REST APIs. Built a complete RAG pipeline for document
        question answering and created FastAPI endpoints.
        """,

        """
        AI Chatbot Using Large Language Models.
        Built using Python, LLM APIs, FastAPI and Prompt Engineering.
        Developed a chatbot using LLM APIs and improved responses
        through prompt refinement.
        """,

        """
        End-to-End Data Engineering & AI Analytics Platform.
        Built using Python, SQL, ETL, Web Scraping, APIs, Power BI
        and an AI chatbot. Built a data pipeline and dashboards.
        """
    ]

    project_requirements = [
        "Building RAG applications",
        "Developing REST APIs",
        "Integrating LLMs into applications",
        "Creating scalable backend services",
        "Deploying applications using Docker",
        "Deploying applications using AWS"
    ]

    results = analyze_project_match(
        projects,
        project_requirements
    )

    return {
        "project_matches": results
    }

@app.post("/test-experience-match")
def test_experience_match():

    experience = [
        """
        Software Developer, E-Whiz Global Solutions Ltd., Pune
        Aug 2025 – Present.

        Build and maintain REST APIs and backend services.
        Build data validation and cleaning pipelines.
        Write optimized SQL queries and improve API/database
        performance.
        Automate repetitive business tasks and build backend
        services supporting AI/ML features.
        """,

        """
        AI Intern, AlmaBetter, Pune
        Jan 2025 – Jul 2025.

        Built an intern-allocation platform using Streamlit
        and Django.
        Built a Training Management System.
        Automated Excel-based attendance tracking.
        Cleaned and validated data for reporting.
        """
    ]

    required_experience = (
        "1-2 years of experience building AI applications"
    )

    responsibilities = [
        "Build RAG-based AI applications",
        "Develop REST APIs",
        "Integrate LLMs",
        "Create scalable backend services",
        "Deploy AI applications using Docker and AWS"
    ]

    results = analyze_experience_match(
        experience,
        required_experience,
        responsibilities
    )

    return {
        "experience_matches": results
    }

@app.post("/test-responsibility-match")
def test_responsibility_match():

    responsibilities = [
        "Build RAG-based AI applications",
        "Develop REST APIs",
        "Integrate LLMs",
        "Create scalable backend services",
        "Deploy AI applications using Docker and AWS"
    ]

    experience = [
        """
        Software Developer, E-Whiz Global Solutions Ltd., Pune
        Aug 2025 – Present.

        Build and maintain REST APIs and backend services.
        Build data validation and cleaning pipelines.
        Write optimized SQL queries and improve API/database
        performance.
        Automate repetitive business tasks and build backend
        services supporting AI/ML features.
        """,

        """
        AI Intern, AlmaBetter, Pune
        Jan 2025 – Jul 2025.

        Built an intern-allocation platform using Streamlit
        and Django.
        Built a Training Management System.
        Automated Excel-based attendance tracking.
        Cleaned and validated data for reporting.
        """
    ]

    projects = [
        """
        RAG-Based AI Assistant for Document Question Answering.
        Built using Python, LangChain, RAG, FastAPI, FAISS,
        Docker and REST APIs.
        Built a complete RAG pipeline and FastAPI endpoints.
        """,

        """
        AI Chatbot Using Large Language Models.
        Built using Python, LLM APIs, FastAPI and Prompt Engineering.
        """,

        """
        End-to-End Data Engineering & AI Analytics Platform.
        Built using Python, SQL, ETL, Web Scraping, APIs,
        Power BI and an AI chatbot.
        """
    ]

    results = analyze_responsibility_match(
        responsibilities,
        experience,
        projects
    )

    return {
        "responsibility_matches": results
    }

@app.post("/test-education-match")
def test_education_match():

    education = [
        "B.Tech in Artificial Intelligence and Data Science"
    ]

    certifications = [
        "AWS Cloud Practitioner",
        "Advanced Data Science Training"
    ]

    job_description = """
    We are looking for an AI Engineer with 1-2 years of experience.

    Required skills:
    Python, FastAPI, RAG, LangChain, Docker and AWS.

    Responsibilities:
    Build RAG-based AI applications,
    develop REST APIs,
    integrate LLMs,
    create scalable backend services,
    and deploy AI applications using Docker and AWS.

    Bachelor's degree in Computer Science,
    Artificial Intelligence, Data Science or a related field
    is preferred.
    """

    result = analyze_education_match(
        education,
        certifications,
        job_description
    )

    return result

@app.post("/test-career-match")
def test_career_match():

    job_description = """
    We are looking for an AI Engineer with 1-2 years of experience
    building AI applications.

    Required skills:
    Python, FastAPI, RAG, LangChain, Docker and AWS.

    Responsibilities:
    Build RAG-based AI applications,
    develop REST APIs,
    integrate LLMs,
    create scalable backend services,
    and deploy AI applications using Docker and AWS.

    Experience with LLM applications, vector databases,
    and document question-answering systems is preferred.

    Bachelor's degree in Computer Science,
    Artificial Intelligence, Data Science or a related field
    is preferred.
    """

    resume_text = """
    ALok Sarwade

    Skills:
    LLMs, RAG, LangChain, LangGraph, Prompt Engineering,
    AI Chatbots, Vector Embeddings, FAISS, NLP, Python,
    SQL, FastAPI, Django, Flask, Streamlit, REST APIs,
    MySQL, PostgreSQL, Docker, Git/GitHub,
    AWS Cloud Essentials, Pandas, NumPy, Power BI.

    Education:
    B.Tech in Artificial Intelligence and Data Science.

    Experience:

    Software Developer, E-Whiz Global Solutions Ltd.
    Aug 2025 - Present.

    Build and maintain REST APIs and backend services.
    Build data validation and cleaning pipelines.
    Write optimized SQL queries and improve API/database
    performance.
    Automate repetitive business tasks and build backend
    services supporting AI/ML features.

    AI Intern, AlmaBetter.
    Jan 2025 - Jul 2025.

    Built an intern-allocation platform using Streamlit
    and Django.
    Built a Training Management System.
    Automated Excel-based attendance tracking.
    Cleaned and validated data for reporting.

    Projects:

    RAG-Based AI Assistant for Document Question Answering.
    Built using Python, LangChain, RAG, FastAPI, FAISS,
    Docker and REST APIs.
    Built a complete RAG pipeline and FastAPI endpoints.

    AI Chatbot Using Large Language Models.
    Built using Python, LLM APIs, FastAPI and Prompt Engineering.

    End-to-End Data Engineering & AI Analytics Platform.
    Built using Python, SQL, ETL, Web Scraping, APIs,
    Power BI and an AI chatbot.

    Certifications:
    AWS Cloud Practitioner.
    Advanced Data Science Training.
    """

    result = match_candidate(
        resume_text=resume_text,
        job_description=job_description
    )

    return result

@app.post("/match-job")
async def match_job(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded resume is empty."
        )

    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name

        resume_text = extract_text_from_pdf(temp_file_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF."
            )

        result = match_candidate(
            resume_text=resume_text,
            job_description=job_description
        )

        return result

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)