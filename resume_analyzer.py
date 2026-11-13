

import streamlit as st
import ollama
import pymupdf
from docx import Document
from io import BytesIO


# ==========================================
# CONFIGURATION
# ==========================================

MODEL_NAME = "qwen2.5:3b"

MAX_RESUME_CHARS = 18000
MAX_OUTPUT_TOKENS = 900


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_pdf_text(file):

    pdf_bytes = file.read()
    text = ""

    pdf = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    try:
        for page in pdf:
            text += page.get_text() + "\n"
    finally:
        pdf.close()

    return text.strip()


# ==========================================
# DOCX TEXT EXTRACTION
# ==========================================

def extract_docx_text(file):

    document = Document(
        BytesIO(file.read())
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    # Extract table content too
    for table in document.tables:

        for row in table.rows:

            row_text = [
                cell.text.strip()
                for cell in row.cells
            ]

            paragraphs.append(
                " | ".join(row_text)
            )

    return "\n".join(paragraphs).strip()


# ==========================================
# RESUME ANALYSIS PROMPT
# ==========================================

def build_analysis_prompt(resume_text):

    return f"""
You are Shree AI, an expert professional resume reviewer
and career consultant.

Analyze the following resume carefully.

Give an honest, specific and actionable report.

Use these sections:

1. PROFESSIONAL SUMMARY
Briefly describe the candidate's profile.

2. TOP 5 STRENGTHS
Identify the strongest points.

3. TOP 5 WEAKNESSES
Identify areas that need improvement.

4. TECHNICAL SKILLS ASSESSMENT
Evaluate the technical skills mentioned.

5. PROJECT AND EXPERIENCE REVIEW
Review projects, internships and work experience.

6. ATS IMPROVEMENTS
Suggest improvements for ATS compatibility.

7. MISSING RESUME SECTIONS
Identify important sections that appear to be missing.

8. SUITABLE ENTRY-LEVEL JOB ROLES
Suggest realistic job roles based on actual skills.

9. RECOMMENDED SKILLS TO LEARN
Suggest useful skills to improve employability.

10. FINAL VERDICT AND ACTION PLAN
Give a concise professional assessment and
prioritize the next steps.

IMPORTANT RULES:

- Never invent qualifications or work experience.
- Do not assume a skill is known unless it appears
  in the resume.
- Distinguish missing information from weak information.
- Give practical suggestions.
- Do not guarantee job selection.
- Do not invent an ATS score.

Keep the report concise, professional and useful.

RESUME CONTENT:

{resume_text}
"""


# ==========================================
# AI RESUME ANALYSIS
# ==========================================

def analyze_resume(resume_text):

    if not resume_text.strip():
        raise ValueError(
            "No readable resume content was found."
        )

    # Limit input length for faster processing
    resume_text = resume_text[:MAX_RESUME_CHARS]

    prompt = build_analysis_prompt(resume_text)

    response = ollama.chat(
        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0.2,
            "num_predict": MAX_OUTPUT_TOKENS
        }
    )

    answer = response["message"]["content"]

    if not answer.strip():
        raise ValueError(
            "The AI returned an empty response."
        )

    return answer


# ==========================================
# RESUME ANALYZER INTERFACE
# ==========================================

def show_resume_analyzer():

    st.title("📄 Resume Analyzer")

    st.write(
        "Get professional AI-powered feedback "
        "on your resume."
    )

    st.caption(
        "Powered by Shree AI | Local Ollama Model"
    )

    st.divider()

    st.info(
        "Upload a PDF or DOCX resume. Shree AI will "
        "review your profile and suggest improvements."
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        key="resume_analyzer_upload"
    )

    if uploaded_file is not None:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🔍 Analyze My Resume",
            type="primary",
            use_container_width=True,
            key="analyze_resume_button"
        ):

            try:

                # Extract resume content
                with st.spinner(
                    "Reading your resume..."
                ):

                    if uploaded_file.name.lower().endswith(".pdf"):

                        resume_text = extract_pdf_text(
                            uploaded_file
                        )

                    else:

                        resume_text = extract_docx_text(
                            uploaded_file
                        )

                if not resume_text:

                    st.error(
                        "No readable text found. "
                        "Please upload a text-based PDF or DOCX."
                    )

                    return

                # Generate AI report
                with st.spinner(
                    "Shree AI is analyzing your resume..."
                ):

                    result = analyze_resume(
                        resume_text
                    )

                # Save report in current session
                st.session_state.resume_analysis = result

                st.session_state.resume_analysis_filename = (
                    uploaded_file.name
                )

                st.success(
                    "Resume analysis completed successfully!"
                )

            except ollama.ResponseError as error:

                st.error(
                    "Ollama could not process your request."
                )

                st.caption(
                    f"Technical details: {error}"
                )

            except Exception as error:

                st.error(
                    "Unable to analyze the resume."
                )

                st.caption(
                    f"Technical details: {error}"
                )

    # ======================================
    # DISPLAY ANALYSIS REPORT
    # ======================================

    if st.session_state.get("resume_analysis"):

        st.divider()

        st.header(
            "📊 Your Resume Analysis Report"
        )

        st.caption(
            "Resume: "
            + st.session_state.get(
                "resume_analysis_filename",
                "Uploaded resume"
            )
        )

        st.markdown(
            st.session_state.resume_analysis
        )

        st.divider()

        # Download report
        st.download_button(
            label="⬇️ Download Analysis Report",
            data=st.session_state.resume_analysis,
            file_name="Shree_AI_Resume_Analysis.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button(
            "🗑️ Clear Analysis",
            use_container_width=True
        ):

            st.session_state.pop(
                "resume_analysis",
                None
            )

            st.session_state.pop(
                "resume_analysis_filename",
                None
            )

            st.rerun()
