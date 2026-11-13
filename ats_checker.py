
import streamlit as st
import re
import pymupdf
from docx import Document
from io import BytesIO


# ==========================================
# RESUME TEXT EXTRACTION
# ==========================================

def extract_resume_text(uploaded_file):

    if uploaded_file.name.lower().endswith(".pdf"):

        pdf = pymupdf.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        try:
            text = "\n".join(
                page.get_text()
                for page in pdf
            )
        finally:
            pdf.close()

        return text.strip()

    document = Document(
        BytesIO(uploaded_file.read())
    )

    paragraphs = [
        p.text.strip()
        for p in document.paragraphs
        if p.text.strip()
    ]

    for table in document.tables:
        for row in table.rows:
            paragraphs.append(
                " ".join(cell.text for cell in row.cells)
            )

    return "\n".join(paragraphs).strip()


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    return re.sub(
        r"[^a-z0-9+#.]",
        " ",
        text.lower()
    )


def extract_keywords(text):

    normalized = normalize_text(text)

    words = set(normalized.split())

    stop_words = {
        "the", "and", "for", "with", "from",
        "this", "that", "you", "your", "are",
        "was", "were", "will", "have", "has",
        "our", "their", "they", "job", "role",
        "work", "years", "year", "using",
        "ability", "strong", "good", "excellent",
        "required", "preferred", "candidate"
    }

    return {
        word for word in words
        if len(word) > 2 and word not in stop_words
    }


# ==========================================
# ATS SCORE CALCULATION
# ==========================================

def calculate_ats_score(resume_text, job_description):

    resume_keywords = extract_keywords(resume_text)

    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        raise ValueError(
            "Please enter a valid job description."
        )

    matched = resume_keywords.intersection(
        job_keywords
    )

    missing = job_keywords - resume_keywords

    keyword_score = (
        len(matched) / len(job_keywords)
    ) * 60

    # Check important resume sections
    lower_resume = resume_text.lower()

    sections = {
        "Contact information": any(
            term in lower_resume
            for term in ["email", "phone", "linkedin"]
        ),
        "Education": any(
            term in lower_resume
            for term in ["education", "degree", "university"]
        ),
        "Skills": any(
            term in lower_resume
            for term in ["skills", "technical skills"]
        ),
        "Experience or projects": any(
            term in lower_resume
            for term in ["experience", "projects", "internship"]
        ),
    }

    section_score = (
        sum(sections.values()) / len(sections)
    ) * 25

    # Basic readability check
    word_count = len(resume_text.split())

    if word_count >= 100:
        readability_score = 15
    elif word_count >= 50:
        readability_score = 10
    else:
        readability_score = 5

    total_score = round(
        keyword_score +
        section_score +
        readability_score
    )

    return {
        "score": min(total_score, 100),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "sections": sections,
        "keyword_score": round(keyword_score),
        "section_score": round(section_score),
        "readability_score": readability_score,
        "word_count": word_count
    }


# ==========================================
# ATS CHECKER INTERFACE
# ==========================================

def show_ats_checker():

    st.title("📊 ATS Score Checker")

    st.write(
        "Check how closely your resume matches "
        "a specific job description."
    )

    st.caption(
        "Shree AI | Rule-based ATS-style assessment"
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        key="ats_resume_upload"
    )

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Paste the complete job description here..."
        )
    )

    if st.button(
        "Calculate ATS Score",
        type="primary",
        use_container_width=True
    ):

        if uploaded_file is None:
            st.error("Please upload your resume.")

        elif not job_description.strip():
            st.error("Please enter a job description.")

        else:

            try:

                with st.spinner(
                    "Checking your resume..."
                ):

                    resume_text = extract_resume_text(
                        uploaded_file
                    )

                    if not resume_text:
                        st.error(
                            "No readable text found in the resume."
                        )
                        return

                    result = calculate_ats_score(
                        resume_text,
                        job_description
                    )

                    st.session_state.ats_result = result

                st.success("ATS assessment completed!")

            except Exception as error:

                st.error(
                    f"Unable to check resume: {error}"
                )

    # ======================================
    # DISPLAY RESULTS
    # ======================================

    result = st.session_state.get("ats_result")

    if result:

        st.divider()

        st.header("Your ATS Assessment")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "ATS-style Match Score",
                f"{result['score']}/100"
            )

        with col2:
            st.metric(
                "Resume Word Count",
                result["word_count"]
            )

        st.progress(result["score"] / 100)

        st.caption(
            "This is an indicative score based on "
            "Shree AI's rubric, not a score from an "
            "employer's actual ATS."
        )

        st.subheader("Score Breakdown")

        st.write(
            f"Keyword match: {result['keyword_score']}/60"
        )

        st.write(
            f"Resume sections: {result['section_score']}/25"
        )

        st.write(
            f"Readability: {result['readability_score']}/15"
        )

        st.subheader("Matched Keywords")

        if result["matched"]:
            st.write(", ".join(result["matched"]))
        else:
            st.warning("No matching keywords found.")

        st.subheader("Missing Keywords")

        if result["missing"]:
            st.write(", ".join(result["missing"]))
        else:
            st.success("All extracted job keywords matched.")

        st.subheader("Resume Section Checklist")

        for section, found in result["sections"].items():

            if found:
                st.success(f"✓ {section}")
            else:
                st.warning(f"Missing or unclear: {section}")

        report = f"""
SHREE AI - ATS ASSESSMENT

ATS-style Match Score: {result['score']}/100

Keyword Score: {result['keyword_score']}/60
Section Score: {result['section_score']}/25
Readability Score: {result['readability_score']}/15

Resume Word Count: {result['word_count']}

Matched Keywords:
{', '.join(result['matched'])}

Missing Keywords:
{', '.join(result['missing'])}

Resume Sections:
{result['sections']}

Note: This is an indicative assessment,
not an employer's actual ATS score.
"""

        st.download_button(
            "Download ATS Report",
            data=report,
            file_name="Shree_AI_ATS_Report.txt",
            mime="text/plain"
        )
