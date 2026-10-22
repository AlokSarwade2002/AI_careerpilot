def calculate_skill_score(
    required_skills: list[str],
    resume_skills: list[str]
):
    required = {
        skill.strip().lower()
        for skill in required_skills
    }

    resume = {
        skill.strip().lower()
        for skill in resume_skills
    }

    matched = required.intersection(resume)
    missing = required - resume

    if not required:
        score = 0
    else:
        score = (
            len(matched) /
            len(required)
        ) * 100

    return {
        "score": round(score, 2),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }


def calculate_project_score(
    project_matches: list[dict],
    project_requirements: list[str]
):
    if not project_matches or not project_requirements:
        return 0

    requirement_scores = {
        index: 0
        for index in range(len(project_requirements))
    }

    for project in project_matches:

        relevance = max(
            0,
            min(100, project["relevance_score"])
        )

        for index in project["matched_requirement_indexes"]:

            if 0 <= index < len(project_requirements):
                requirement_scores[index] = max(
                    requirement_scores[index],
                    relevance
                )

    total_score = sum(
        requirement_scores.values()
    )

    score = (
        total_score /
        (len(project_requirements) * 100)
    ) * 100

    return round(score, 2)


def calculate_overall_score(
    skill_score: float,
    project_score: float,
    experience_score: float,
    responsibility_score: float,
    education_score: float
):
    overall = (
        skill_score * 0.35
        + project_score * 0.30
        + experience_score * 0.20
        + responsibility_score * 0.10
        + education_score * 0.05
    )

    return round(overall, 2)