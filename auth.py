

import streamlit as st

# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from modules.ai_chat import show_ai_chat
from modules.resume_analyzer import show_resume_analyzer
from modules.ats_checker import show_ats_checker
from modules.resume_builder import show_resume_builder
from modules.mock_interview import show_mock_interview
from modules.auth import show_auth

from services.supabase_client import get_supabase_client


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Shree AI | Career Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# SESSION STATE
# ==========================================

if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .shree-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0 16px 0;
    }

    .shree-brand {
        font-size: 27px;
        font-weight: 750;
        color: var(--text-color);
        white-space: nowrap;
    }

    .shree-status {
        background: rgba(22, 163, 74, 0.13);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 8px 13px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        white-space: nowrap;
    }

    div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
    }

    div[role="radiogroup"] label {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 9px 13px;
        transition: 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        border-color: #6366f1;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    .stDownloadButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    @media (max-width: 900px) {
        .shree-brand {
            font-size: 21px;
        }

        div[role="radiogroup"] {
            gap: 5px;
        }

        div[role="radiogroup"] label {
            padding: 7px 9px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# AUTHENTICATION GATE
# ==========================================

if st.session_state.user is None:

    show_auth()

    st.stop()


# ==========================================
# LOGOUT FUNCTION
# ==========================================

def logout_user():

    st.session_state.user = None
    st.session_state.access_token = None

    st.session_state.pop("main_navigation", None)

    st.rerun()


# ==========================================
# TOP HEADER
# ==========================================

header_col1, header_col2, header_col3 = st.columns(
    [2, 1, 1],
    vertical_alignment="center"
)

with header_col1:

    st.markdown(
        """
        <div class="shree-header">
            <div class="shree-brand">🤖 Shree AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:

    st.markdown(
        """
        <div style="display:flex; justify-content:center;">
            <span class="shree-status">
                ● Ollama: Local AI
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col3:

    user = st.session_state.user

    user_email = getattr(user, "email", "User")

    st.caption(f"👤 {user_email}")

    if st.button(
        "Logout",
        use_container_width=True,
        key="shree_logout"
    ):

        logout_user()


st.divider()


# ==========================================
# HORIZONTAL NAVIGATION
# ==========================================

features = [
    "💬 AI Chat",
    "📄 Resume Analyzer",
    "🎯 ATS Score Checker",
    "📝 Smart Resume Builder",
    "🎤 AI Mock Interview"
]

if "main_navigation" not in st.session_state:

    st.session_state.main_navigation = features[0]

selected_feature = st.radio(
    "Navigation",
    features,
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation"
)


st.divider()


# ==========================================
# MAIN APPLICATION HEADER
# ==========================================

st.caption(
    "Your intelligent assistant for career development, "
    "resume improvement and interview preparation."
)


# ==========================================
# FEATURE ROUTING
# ==========================================

if selected_feature == "💬 AI Chat":

    show_ai_chat()


elif selected_feature == "📄 Resume Analyzer":

    show_resume_analyzer()


elif selected_feature == "🎯 ATS Score Checker":

    show_ats_checker()


elif selected_feature == "📝 Smart Resume Builder":

    show_resume_builder()


elif selected_feature == "🎤 AI Mock Interview":

    show_mock_interview()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 Shree AI | Built with Python, Streamlit and Ollama."
)
