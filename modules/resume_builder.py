

import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    HRFlowable
)
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Inches, Pt, RGBColor


# ==========================================
# PDF GENERATOR
# ==========================================

def generate_pdf(data, photo=None):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    accent = (
        colors.HexColor("#2563EB")
        if data["template"] == "Modern"
        else colors.HexColor("#172554")
    )

    title_style = ParagraphStyle(
        "ResumeTitle",
        parent=styles["Title"],
        fontSize=23,
        textColor=accent,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "ResumeHeading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=accent,
        spaceBefore=12,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=5
    )

    elements = []

    if photo is not None:

        photo.seek(0)

        elements.append(
            Image(
                photo,
                width=0.9 * inch,
                height=0.9 * inch
            )
        )

        elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(data["name"], title_style)
    )

    contact = " | ".join(
        value for value in [
            data["email"],
            data["phone"],
            data["location"]
        ] if value
    )

    elements.append(
        Paragraph(contact, body_style)
    )

    links = " | ".join(
        value for value in [
            data["linkedin"],
            data["github"]
        ] if value
    )

    if links:
        elements.append(Paragraph(links, body_style))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=accent
        )
    )

    sections = [
        ("PROFESSIONAL SUMMARY", data["summary"]),
        (
            "EDUCATION",
            "\n".join(filter(None, [
                data["degree"],
                data["college"],
                data["graduation_year"],
                data["cgpa"]
            ]))
        ),
        ("TECHNICAL SKILLS", data["technical_skills"]),
        ("SOFT SKILLS", data["soft_skills"]),
        (
            "PROJECTS",
            "\n".join(filter(None, [
                data["project_name"],
                data["project_description"],
                data["project_technologies"]
            ]))
        ),
        (
            "EXPERIENCE",
            "\n".join(filter(None, [
                data["job_role"],
                data["company"],
                data["experience_description"]
            ]))
        )
    ]

    for heading, content in sections:

        if content.strip():

            elements.append(
                Paragraph(heading, heading_style)
            )

            safe_content = (
                content
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>")
            )

            elements.append(
                Paragraph(safe_content, body_style)
            )

    pdf.build(elements)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# DOCX GENERATOR
# ==========================================

def generate_docx(data, photo=None):

    document = Document()

    accent = (
        RGBColor(37, 99, 235)
        if data["template"] == "Modern"
        else RGBColor(23, 37, 84)
    )

    section = document.sections[0]

    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)

    if photo is not None:

        photo.seek(0)

        document.add_picture(
            photo,
            width=Inches(1)
        )

    title = document.add_heading(
        data["name"],
        level=0
    )

    title.alignment = 1

    for run in title.runs:
        run.font.color.rgb = accent

    contact = " | ".join(
        value for value in [
            data["email"],
            data["phone"],
            data["location"]
        ] if value
    )

    document.add_paragraph(contact)

    links = " | ".join(
        value for value in [
            data["linkedin"],
            data["github"]
        ] if value
    )

    if links:
        document.add_paragraph(links)

    sections = [
        ("PROFESSIONAL SUMMARY", data["summary"]),
        (
            "EDUCATION",
            "\n".join(filter(None, [
                data["degree"],
                data["college"],
                data["graduation_year"],
                data["cgpa"]
            ]))
        ),
        ("TECHNICAL SKILLS", data["technical_skills"]),
        ("SOFT SKILLS", data["soft_skills"]),
        (
            "PROJECTS",
            "\n".join(filter(None, [
                data["project_name"],
                data["project_description"],
                data["project_technologies"]
            ]))
        ),
        (
            "EXPERIENCE",
            "\n".join(filter(None, [
                data["job_role"],
                data["company"],
                data["experience_description"]
            ]))
        )
    ]

    for heading, content in sections:

        if content.strip():

            heading_paragraph = document.add_heading(
                heading,
                level=2
            )

            for run in heading_paragraph.runs:
                run.font.color.rgb = accent

            document.add_paragraph(content)

    buffer = BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# RESUME BUILDER INTERFACE
# ==========================================

def show_resume_builder():

    st.title("📝 Smart Resume Builder")

    st.caption(
        "Create professional resumes with Shree AI."
    )

    st.divider()

    # Personal information
    st.header("1. Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")

    with col2:

        location = st.text_input("Location")
        linkedin = st.text_input("LinkedIn URL")
        github = st.text_input("GitHub URL")

    photo = st.file_uploader(
        "Upload profile photo (optional)",
        type=["png", "jpg", "jpeg"]
    )

    summary = st.text_area(
        "Professional Summary",
        placeholder="Write your professional introduction..."
    )

    st.divider()

    # Education
    st.header("2. Education")

    degree = st.text_input("Degree")
    college = st.text_input("College / University")

    col1, col2 = st.columns(2)

    with col1:
        graduation_year = st.text_input("Graduation Year")

    with col2:
        cgpa = st.text_input("CGPA / Percentage")

    st.divider()

    # Skills
    st.header("3. Skills")

    technical_skills = st.text_area(
        "Technical Skills",
        placeholder="Python, SQL, Power BI..."
    )

    soft_skills = st.text_area(
        "Soft Skills",
        placeholder="Communication, Teamwork..."
    )

    st.divider()

    # Projects
    st.header("4. Projects")

    project_name = st.text_input("Project Name")

    project_description = st.text_area(
        "Project Description"
    )

    project_technologies = st.text_input(
        "Technologies Used"
    )

    st.divider()

    # Experience
    st.header("5. Experience / Internship")

    company = st.text_input("Company Name")

    job_role = st.text_input("Job Role")

    experience_description = st.text_area(
        "Responsibilities / Work Description"
    )

    st.divider()

    # Template
    st.header("6. Resume Design")

    template = st.selectbox(
        "Choose Template",
        [
            "Professional",
            "Modern",
            "Minimal"
        ]
    )

    # Generate
    if st.button(
        "Generate Resume",
        type="primary",
        use_container_width=True
    ):

        if not full_name.strip():
            st.error("Please enter your full name.")

        elif not email.strip():
            st.error("Please enter your email address.")

        else:

            resume_data = {
                "name": full_name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "summary": summary,
                "degree": degree,
                "college": college,
                "graduation_year": graduation_year,
                "cgpa": cgpa,
                "technical_skills": technical_skills,
                "soft_skills": soft_skills,
                "project_name": project_name,
                "project_description": project_description,
                "project_technologies": project_technologies,
                "company": company,
                "job_role": job_role,
                "experience_description": experience_description,
                "template": template
            }

            photo_bytes = photo.getvalue() if photo else None

            st.session_state.resume_builder_data = resume_data
            st.session_state.resume_builder_photo = photo_bytes

            st.success("Resume information saved!")

    # Preview and downloads
    if st.session_state.get("resume_builder_data"):

        data = st.session_state.resume_builder_data

        photo_bytes = st.session_state.get(
            "resume_builder_photo"
        )

        st.divider()

        st.header("7. Resume Preview")

        if photo_bytes:
            st.image(photo_bytes, width=120)

        st.title(data["name"])

        st.write(
            " | ".join(
                value for value in [
                    data["email"],
                    data["phone"],
                    data["location"]
                ] if value
            )
        )

        if data["linkedin"]:
            st.write("LinkedIn:", data["linkedin"])

        if data["github"]:
            st.write("GitHub:", data["github"])

        preview_sections = [
            ("Professional Summary", data["summary"]),
            ("Education", "\n".join(filter(None, [
                data["degree"],
                data["college"],
                data["graduation_year"],
                data["cgpa"]
            ]))),
            ("Technical Skills", data["technical_skills"]),
            ("Soft Skills", data["soft_skills"]),
            ("Projects", "\n".join(filter(None, [
                data["project_name"],
                data["project_description"],
                data["project_technologies"]
            ]))),
            ("Experience", "\n".join(filter(None, [
                data["job_role"],
                data["company"],
                data["experience_description"]
            ])))
        ]

        for heading, content in preview_sections:

            if content.strip():

                st.subheader(heading)
                st.write(content)

        st.divider()

        st.header("8. Download Your Resume")

        photo_file = (
            BytesIO(photo_bytes)
            if photo_bytes
            else None
        )

        pdf_file = generate_pdf(
            data,
            photo_file
        )

        docx_photo = (
            BytesIO(photo_bytes)
            if photo_bytes
            else None
        )

        docx_file = generate_docx(
            data,
            docx_photo
        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "⬇️ Download PDF",
                data=pdf_file,
                file_name="Shree_AI_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:

            st.download_button(
                "⬇️ Download Word",
                data=docx_file,
                file_name="Shree_AI_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
