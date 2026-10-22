
import requests
import streamlit as st
# st.success("CareerPilot UI loaded successfully!")

API_URL = "http://127.0.0.1:8000/match-job"

st.set_page_config(
    page_title="AI CareerPilot",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 AI CareerPilot")
st.subheader("AI-powered Resume & Job Match Analyzer")
st.write(
    "Upload your resume and compare your skills, projects, "
    "and experience with a target job."
)

st.divider()

# -----------------------------
# Input section
# -----------------------------

left, right = st.columns(2, gap="large")

with left:
    st.markdown("### 📄 Your Resume")

    uploaded_file = st.file_uploader(
        "Upload resume (PDF only)",
        type=["pdf"],
        help="Choose your resume in PDF format.",
    )

    if uploaded_file:
        st.success(f"Selected: {uploaded_file.name}")

with right:
    st.markdown("### 💼 Target Job")

    job_description = st.text_area(
        "Paste the complete job description",
        height=260,
        placeholder=(
            "Example: We are looking for an AI Engineer "
            "with Python, FastAPI, RAG, LangChain, Docker "
            "and AWS experience..."
        ),
    )

st.divider()

# -----------------------------
# Analyze button
# -----------------------------

if st.button(
    "🚀 Analyze My Match",
    type="primary",
    use_container_width=True,
):
    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner(
                "Analyzing your resume and matching it "
                "against the job description..."
            ):
                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    },
                    data={
                        "job_description": job_description
                    },
                    timeout=180,
                )

            if response.status_code == 200:
                result = response.json()
                st.session_state["career_result"] = result
                st.success("Analysis completed successfully!")

            else:
                st.session_state.pop("career_result", None)

                if response.status_code == 429:
                    st.error(
                        "The API rate limit was reached. "
                        "Please wait and try again."
                    )
                else:
                    try:
                        detail = response.json().get(
                            "detail",
                            response.text,
                        )
                    except ValueError:
                        detail = response.text

                    st.error(
                        f"Analysis failed "
                        f"(HTTP {response.status_code}): {detail}"
                    )

        except requests.exceptions.Timeout:
            st.error(
                "The analysis took too long. "
                "Please try again later."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the FastAPI server. "
                "Make sure your backend is running."
            )

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")

        except ValueError:
            st.error("The server returned an invalid response.")

# -----------------------------
# Results section
# -----------------------------

result = st.session_state.get("career_result")

if result:
    st.divider()
    st.header("📊 Your Career Match Results")

    score = float(result.get("overall_score", 0))

    score_col, message_col = st.columns([1, 2])

    with score_col:
        st.metric("Overall Match Score", f"{score:.2f}%")
        st.progress(
            max(0.0, min(1.0, score / 100))
        )

    with message_col:
        st.markdown("#### Match overview")

        if score >= 80:
            st.success(
                "Strong alignment with this job description."
            )
        elif score >= 60:
            st.info(
                "Moderate alignment. Review your gaps "
                "to improve your application."
            )
        else:
            st.warning(
                "Several areas may need improvement "
                "for this role."
            )

    # Component scores
    st.subheader("Component Scores")

    score_fields = [
        ("Skills", "skill_score"),
        ("Projects", "project_score"),
        ("Experience", "experience_score"),
        ("Responsibilities", "responsibility_score"),
        ("Education", "education_score"),
    ]

    cols = st.columns(5)

    for col, (label, key) in zip(cols, score_fields):
        value = float(result.get(key, 0) or 0)

        with col:
            st.metric(label, f"{value:.1f}%")
            st.progress(
                max(0.0, min(1.0, value / 100))
            )

    st.divider()

    # Skills
    st.subheader("🧠 Skills Analysis")

    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])

    skill_left, skill_right = st.columns(2)

    with skill_left:
        st.markdown("**Matched skills**")

        if matched:
            for skill in matched:
                st.markdown(f"- ✅ {skill}")
        else:
            st.write("No matched skills returned.")

    with skill_right:
        st.markdown("**Missing required skills**")

        if missing:
            for skill in missing:
                st.markdown(f"- ❌ {skill}")
        else:
            st.write("No missing skills reported.")

    # Projects
    st.divider()
    st.subheader("🛠️ Project Relevance")

    projects = result.get("project_matches", [])

    if projects:
        for index, project in enumerate(projects, start=1):
            relevance = float(
                project.get("relevance_score", 0) or 0
            )

            with st.expander(
                f"Project {index} — {relevance:.1f}% relevance"
            ):
                st.write(project.get("project", ""))
                st.progress(
                    max(0.0, min(1.0, relevance / 100))
                )
                st.markdown("**Reasoning**")
                st.write(project.get("reason", "Not provided."))

                st.markdown("**Matched requirement indexes**")
                st.write(
                    project.get(
                        "matched_requirement_indexes", []
                    )
                )
    else:
        st.info("No project matches were returned.")

    # Professional experience
    st.divider()
    st.subheader("💼 Experience Analysis")

    experiences = result.get("experience_matches", [])

    if experiences:
        for index, item in enumerate(experiences, start=1):
            relevance = float(
                item.get("relevance_score", 0) or 0
            )

            with st.expander(
                f"Experience {index} — {relevance:.1f}% relevance"
            ):
                st.write(item.get("experience", ""))
                st.progress(
                    max(0.0, min(1.0, relevance / 100))
                )
                st.markdown("**Matched responsibilities**")
                st.write(
                    item.get("matched_responsibilities", [])
                )
                st.markdown("**Reasoning**")
                st.write(item.get("reason", "Not provided."))

    # Responsibility evidence
    st.divider()
    st.subheader("📋 Responsibility Evidence")

    responsibilities = result.get(
        "responsibility_matches", []
    )

    if responsibilities:
        for item in responsibilities:
            evidence_score = float(
                item.get("evidence_score", 0) or 0
            )

            with st.expander(
                f"{item.get('responsibility', 'Responsibility')} "
                f"— {evidence_score:.1f}%"
            ):
                st.progress(
                    max(0.0, min(1.0, evidence_score / 100))
                )
                st.markdown("**Evidence from your resume**")

                evidence = item.get("evidence", [])

                if evidence:
                    for entry in evidence:
                        st.markdown(f"- {entry}")
                else:
                    st.write("No direct evidence returned.")

                st.markdown("**Reasoning**")
                st.write(item.get("reason", "Not provided."))

    # Education
    st.divider()
    st.subheader("🎓 Education & Certifications")

    education = result.get("education_analysis", {})

    st.metric(
        "Education score",
        f"{float(education.get('score', 0) or 0):.1f}%"
    )

    st.write(education.get("reason", "No explanation provided."))

    with st.expander("Education requirement details"):
        st.markdown("**Requirements**")
        st.write(education.get("education_requirements", []))

        st.markdown("**Matched requirements**")
        st.write(education.get("matched_requirements", []))

        st.markdown("**Missing requirements**")
        st.write(education.get("missing_requirements", []))

        st.markdown("**Certification requirements**")
        st.write(
            education.get("certification_requirements", [])
        )

    # Strengths and gaps
    st.divider()
    st.subheader("💡 Strengths & Improvement Areas")

    strength_col, gap_col = st.columns(2)

    with strength_col:
        st.markdown("#### ✅ Strengths")

        strengths = result.get("strengths", [])

        if strengths:
            for item in strengths:
                st.markdown(f"- {item}")
        else:
            st.write("No strengths returned.")

    with gap_col:
        st.markdown("#### 🎯 Gaps to address")

        gaps = result.get("gaps", [])

        if gaps:
            for item in gaps:
                st.markdown(f"- {item}")
        else:
            st.write("No gaps returned.")

    st.caption(
        "This score estimates alignment with the supplied job "
        "description. It is not a probability of getting hired."
    )
