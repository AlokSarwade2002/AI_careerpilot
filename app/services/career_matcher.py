from app.services.llm_service import (
    analyze_job_description,
    analyze_resume
)

from app.services.resume_parser import (
    extract_text_from_pdf
)

from app.services.project_matcher import (
    analyze_project_match
)

from app.services.experience_matcher import (
    analyze_experience_match
)

from app.services.responsibility_matcher import (
    analyze_responsibility_match
)

from app.services.education_matcher import (
    analyze_education_match
)

from app.services.score_engine import (
    calculate_skill_score,
    calculate_project_score,
    calculate_overall_score
)
from app.services.career_insights import (
    generate_career_insights
)




def match_candidate(
    resume_text: str,
    job_description: str
):

    # ------------------------------------------------
    # 1. Analyze Job
    # ------------------------------------------------

    job = analyze_job_description(
        job_description
    )

    # ------------------------------------------------
    # 2. Analyze Resume
    # ------------------------------------------------

    resume = analyze_resume(
        resume_text
    )

    # ------------------------------------------------
    # 3. Skill Matching
    # ------------------------------------------------

    skill_result = calculate_skill_score(
        job["required_skills"],
        resume["skills"]
    )

    # ------------------------------------------------
    # 4. Project Matching
    # ------------------------------------------------

    project_matches = analyze_project_match(
        resume["projects"],
        job["project_requirements"]
    )

    project_score = calculate_project_score(
        project_matches,
        job["project_requirements"]
    )

    # ------------------------------------------------
    # 5. Experience Matching
    # ------------------------------------------------

    experience_matches = analyze_experience_match(
        resume["experience"],
        job["experience_required"],
        job["responsibilities"]
    )

    # Use the strongest relevant experience
    if experience_matches:
        experience_score = max(
            item["relevance_score"]
            for item in experience_matches
        )
    else:
        experience_score = 0

    # ------------------------------------------------
    # 6. Responsibility Matching
    # ------------------------------------------------

    responsibility_matches = analyze_responsibility_match(
        job["responsibilities"],
        resume["experience"],
        resume["projects"]
    )

    if responsibility_matches:
        responsibility_score = sum(
            item["evidence_score"]
            for item in responsibility_matches
        ) / len(responsibility_matches)
    else:
        responsibility_score = 0

    responsibility_score = round(
        responsibility_score,
        2
    )

    # ------------------------------------------------
    # 7. Education / Certification
    # ------------------------------------------------

    education_result = analyze_education_match(
        resume["education"],
        resume["certifications"],
        job_description
    )

    education_score = education_result["score"]

    # ------------------------------------------------
    # 8. Overall Score
    # ------------------------------------------------

    overall_score = calculate_overall_score(
        skill_score=skill_result["score"],
        project_score=project_score,
        experience_score=experience_score,
        responsibility_score=responsibility_score,
        education_score=education_score
    )
    insights = generate_career_insights(
    skill_score=skill_result["score"],
    project_score=project_score,
    experience_score=experience_score,
    responsibility_score=responsibility_score,
    education_score=education_score,
    matched_skills=skill_result["matched"],
    missing_skills=skill_result["missing"],
    project_matches=project_matches,
    responsibility_matches=responsibility_matches
)

    # ------------------------------------------------
    # 9. Return Everything
    # ------------------------------------------------

    return {
        "overall_score": overall_score,

        "skill_score": skill_result["score"],

        "project_score": project_score,

        "experience_score": round(
            experience_score,
            2
        ),

        "responsibility_score": responsibility_score,

        "education_score": education_score,

        "matched_skills": skill_result["matched"],

        "missing_skills": skill_result["missing"],

        "project_matches": project_matches,

        "experience_matches": experience_matches,

        "responsibility_matches": responsibility_matches,

        "education_analysis": education_result, 
        "strengths": insights["strengths"],
        "gaps": insights["gaps"]
    }