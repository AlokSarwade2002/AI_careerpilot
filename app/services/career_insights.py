def generate_career_insights(
    skill_score: float,
    project_score: float,
    experience_score: float,
    responsibility_score: float,
    education_score: float,
    matched_skills: list[str],
    missing_skills: list[str],
    project_matches: list[dict],
    responsibility_matches: list[dict]
):

    strengths = []
    gaps = []

    # -----------------------------
    # Skill strengths
    # -----------------------------

    if skill_score >= 80:
        strengths.append(
            "Strong alignment with the required technical skills."
        )
    elif skill_score >= 60:
        strengths.append(
            "Good alignment with the required technical skills."
        )

    # -----------------------------
    # Project strengths
    # -----------------------------

    if project_score >= 80:
        strengths.append(
            "Strong project experience relevant to the target role."
        )
    elif project_score >= 60:
        strengths.append(
            "Relevant project experience demonstrates several "
            "requirements of the target role."
        )

    # -----------------------------
    # Responsibility strengths
    # -----------------------------

    if responsibility_score >= 80:
        strengths.append(
            "Strong evidence of performing the responsibilities "
            "required for the role."
        )

    # -----------------------------
    # Education
    # -----------------------------

    if education_score >= 90:
        strengths.append(
            "Education background aligns well with the role."
        )

    # -----------------------------
    # Missing skills
    # -----------------------------

    if missing_skills:
        gaps.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    # -----------------------------
    # Project gaps
    # -----------------------------

    weak_projects = [
        project
        for project in project_matches
        if project["relevance_score"] < 60
    ]

    if weak_projects:
        gaps.append(
            "Some projects have limited relevance to the target role."
        )

    # -----------------------------
    # Responsibility gaps
    # -----------------------------

    weak_responsibilities = [
        item
        for item in responsibility_matches
        if item["evidence_score"] < 60
    ]

    for item in weak_responsibilities:

        gaps.append(
            f"Limited evidence for: "
            f"{item['responsibility']}"
        )

    # -----------------------------
    # Experience
    # -----------------------------

    if experience_score < 60:
        gaps.append(
            "Professional experience has limited direct "
            "alignment with the target role."
        )

    return {
        "strengths": strengths,
        "gaps": gaps
    }