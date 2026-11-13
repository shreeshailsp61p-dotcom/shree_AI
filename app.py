

import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# =========================================================
# 1. ENVIRONMENT CONFIGURATION
# =========================================================

load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")

# =========================================================
# 2. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Shree AI | Cosmic Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 3. COSMIC VIOLET DESIGN
# =========================================================

st.markdown("""
<style>

/* Main application */

.stApp {
    background:
        radial-gradient(
            circle at 75% 5%,
            rgba(103, 58, 183, 0.12),
            transparent 30%
        ),
        #090817;
    color: #F1EDFF;
}

/* Fix top header clipping */

[data-testid="stAppViewContainer"] section.main > div.block-container {
    max-width: 1500px;
    padding-top: 4rem !important;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #100D20 0%,
        #0C0A19 100%
    );
    border-right: 1px solid rgba(167, 139, 250, 0.15);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] .block-container {
    padding: 1rem 1rem 2rem 1rem !important;
}

/* Branding */

.shree-logo {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: 1px;
    line-height: 1.5;
    color: #F4EEFF;
    padding-top: 5px;
    overflow: visible;
}

.shree-tagline {
    color: #A78BFA;
    font-size: 10px;
    letter-spacing: 2.2px;
    font-weight: 700;
    margin-top: 3px;
}

.sidebar-label {
    color: #A78BFA;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 18px;
    margin-bottom: 8px;
}

.sidebar-status {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.22);
    border-radius: 10px;
    padding: 10px;
    color: #86EFAC;
    font-size: 12px;
}

/* Sidebar buttons */

[data-testid="stSidebar"] .stButton > button {
    border-radius: 9px;
    min-height: 40px;
    text-align: left;
    font-size: 13px;
}

[data-testid="stSidebar"] .stTextInput input {
    background: #19142B !important;
    border: 1px solid rgba(167, 139, 250, 0.25) !important;
    border-radius: 9px !important;
    color: #F4EEFF !important;
}

/* Sidebar feature navigation */

[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 10px 12px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(139, 92, 246, 0.10);
    border-color: rgba(167, 139, 250, 0.22);
}

[data-testid="stSidebar"] div[role="radiogroup"]
label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(124, 58, 237, 0.25),
        rgba(124, 58, 237, 0.08)
    );
    border: 1px solid rgba(167, 139, 250, 0.35);
}

/* Main header */

.main-title {
    color: #F4EEFF;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.6px;
    line-height: 1.5;
    padding-top: 5px;
    overflow: visible;
}

.main-subtitle {
    color: #A69BBF;
    font-size: 13px;
    margin-top: 4px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(34, 197, 94, 0.08);
    color: #86EFAC;
    border: 1px solid rgba(34, 197, 94, 0.22);
    border-radius: 30px;
    padding: 7px 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    color: white;
    border: none;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.25);
}

/* Inputs */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #151126 !important;
    border-color: rgba(167, 139, 250, 0.22) !important;
    border-radius: 10px !important;
}

/* Chat messages */

[data-testid="stChatMessage"] {
    background: rgba(25, 20, 43, 0.65);
    border: 1px solid rgba(167, 139, 250, 0.12);
    border-radius: 14px;
    padding: 14px;
}

/* Chat input */

[data-testid="stChatInput"] {
    border: 1px solid rgba(167, 139, 250, 0.30);
    border-radius: 15px;
    background: #151126;
}

/* Dividers */

hr {
    border-color: rgba(167, 139, 250, 0.14) !important;
}

/* Guest notice */

.guest-notice {
    background: rgba(139, 92, 246, 0.07);
    border: 1px solid rgba(167, 139, 250, 0.18);
    border-radius: 10px;
    padding: 10px 14px;
    color: #C4B5FD;
    font-size: 12px;
    margin-bottom: 15px;
}

/* Footer */

.footer-text {
    color: #756B91;
    font-size: 11px;
    text-align: center;
    padding-top: 15px;
}

/* Responsive */

@media (max-width: 900px) {
    [data-testid="stAppViewContainer"] section.main > div.block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 3rem !important;
    }

    .main-title {
        font-size: 23px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. OPTIONAL SUPABASE CONNECTION
# =========================================================

supabase = None
supabase_error = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        if "supabase_client" not in st.session_state:
            st.session_state.supabase_client = create_client(
                SUPABASE_URL,
                SUPABASE_KEY
            )

        supabase = st.session_state.supabase_client

    except Exception as error:
        supabase_error = str(error)

else:
    supabase_error = "Supabase configuration not found."


# =========================================================
# 5. SESSION STATE
# =========================================================

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "auth_session" not in st.session_state:
    st.session_state.auth_session = None

if "is_guest" not in st.session_state:
    st.session_state.is_guest = False

if "main_navigation" not in st.session_state:
    st.session_state.main_navigation = "💬 AI Chat"


# =========================================================
# 6. AUTHENTICATION PAGE
# =========================================================

def show_auth_page():

    st.markdown("""
    <div style="text-align:center; padding-top:55px;">
        <div style="font-size:55px;color:#C4B5FD;">✦</div>
        <div style="font-size:34px;font-weight:800;color:#F4EEFF;">
            SHREE AI
        </div>
        <div class="shree-tagline" style="text-align:center;">
            COSMIC INTELLIGENCE
        </div>
        <br>
        <div style="color:#A69BBF;font-size:14px;">
            Your intelligent workspace for thinking, learning and creating.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.subheader("Enter your workspace")

        st.write(
            "Continue as a guest or sign in to your Shree AI account."
        )

        if st.button(
            "✦  Continue as Guest",
            type="primary",
            use_container_width=True,
            key="continue_as_guest"
        ):
            st.session_state.is_guest = True
            st.session_state.auth_user = None
            st.rerun()

        st.divider()

        login_tab, signup_tab = st.tabs(
            ["Login", "Create Account"]
        )

        if supabase is None:
            st.info(
                "Account features are temporarily unavailable. "
                "You can still continue as a guest."
            )

        with login_tab:

            st.subheader("Welcome Back")

            with st.form("login_form"):

                login_email = st.text_input(
                    "Email Address",
                    placeholder="Enter your email"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_submit = st.form_submit_button(
                    "Login",
                    use_container_width=True,
                    disabled=(supabase is None)
                )

            if login_submit:

                if not login_email.strip() or not login_password:
                    st.warning("Please enter both email and password.")

                else:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": login_email.strip().lower(),
                            "password": login_password
                        })

                        st.session_state.auth_user = response.user
                        st.session_state.auth_session = response.session
                        st.session_state.is_guest = False

                        st.success("Login successful!")
                        st.rerun()

                    except Exception:
                        st.error(
                            "Login failed. Check your email, password "
                            "and email confirmation status."
                        )

        with signup_tab:

            st.subheader("Create Your Account")

            with st.form("signup_form"):

                signup_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your name"
                )

                signup_email = st.text_input(
                    "Email Address",
                    placeholder="Enter your email"
                )

                signup_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="Minimum 6 characters"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                signup_submit = st.form_submit_button(
                    "Create Account",
                    use_container_width=True,
                    disabled=(supabase is None)
                )

            if signup_submit:

                if not signup_name.strip() or not signup_email.strip():
                    st.warning("Please complete all the fields.")

                elif len(signup_password) < 6:
                    st.error("Password must contain at least 6 characters.")

                elif signup_password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": signup_email.strip().lower(),
                            "password": signup_password,
                            "options": {
                                "data": {
                                    "full_name": signup_name.strip()
                                }
                            }
                        })

                        if response.session:
                            st.session_state.auth_user = response.user
                            st.session_state.auth_session = response.session
                            st.session_state.is_guest = False

                            st.success("Account created successfully!")
                            st.rerun()

                        else:
                            st.success("Account created successfully!")
                            st.info(
                                "Check your email and click the "
                                "confirmation link. Then return here "
                                "and log in."
                            )

                    except Exception:
                        st.error(
                            "Account creation failed. "
                            "Please check your details and try again."
                        )

    st.markdown("""
    <div class="footer-text">
        © 2026 SHREE AI · COSMIC INTELLIGENCE
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 7. LOGOUT
# =========================================================

def logout():

    if supabase is not None and st.session_state.auth_user:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

    st.session_state.auth_user = None
    st.session_state.auth_session = None
    st.session_state.is_guest = False

    st.session_state.pop("main_navigation", None)

    st.rerun()


# =========================================================
# 8. AUTHENTICATION GATE
# =========================================================

if (
    st.session_state.auth_user is None
    and not st.session_state.is_guest
):
    show_auth_page()
    st.stop()


# =========================================================
# 9. IMPORT EXISTING MODULES
# =========================================================

from modules.ai_chat import (
    show_ai_chat,
    initialize_chat,
    start_new_chat,
    open_conversation
)

from modules.resume_analyzer import show_resume_analyzer
from modules.ats_checker import show_ats_checker
from modules.resume_builder import show_resume_builder
from modules.mock_interview import show_mock_interview

from services.chat_history import get_all_conversations


# =========================================================
# 10. INITIALIZE CHAT DATABASE AND STATE
# =========================================================

initialize_chat()


# =========================================================
# 11. FEATURE DEFINITIONS
# =========================================================

features = [
    "💬 AI Chat",
    "📄 Resume Analyzer",
    "🎯 ATS Score Checker",
    "📝 Smart Resume Builder",
    "🎤 AI Mock Interview"
]


# =========================================================
# 12. SIDEBAR
# =========================================================

with st.sidebar:

    # Branding
    st.markdown("""
    <div style="padding:5px 0 18px 0;">
        <div class="shree-logo">✦ SHREE AI</div>
        <div class="shree-tagline">COSMIC INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-status">● &nbsp; Local AI Workspace</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # New Chat
    if st.button(
        "＋  New Chat",
        use_container_width=True,
        key="sidebar_new_chat"
    ):
        start_new_chat()
        st.session_state.main_navigation = features[0]
        st.rerun()

    # Search History
    st.markdown(
        '<div class="sidebar-label">SEARCH HISTORY</div>',
        unsafe_allow_html=True
    )

    history_search = st.text_input(
        "Search conversations",
        placeholder="🔍 Search your chats...",
        label_visibility="collapsed",
        key="history_search"
    )

    # Conversation history
    try:

        conversations = get_all_conversations()

        if not conversations:
            st.caption("No previous conversations yet.")

        else:

            matching_conversations = [
                conversation
                for conversation in conversations
                if history_search.strip().lower()
                in conversation.get("title", "").lower()
            ]

            if not matching_conversations:
                st.caption("No matching conversations.")

            for conversation in matching_conversations:

                conversation_id = conversation["id"]
                title = conversation.get("title", "New Chat")

                is_active = (
                    conversation_id
                    == st.session_state.active_conversation_id
                )

                if st.button(
                    ("● " if is_active else "💬 ") + title,
                    key=f"history_chat_{conversation_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    open_conversation(conversation_id)
                    st.session_state.main_navigation = features[0]
                    st.rerun()

                with st.popover(
                    "⋯",
                    use_container_width=True,
                    key=f"history_options_{conversation_id}"
                ):

                    st.markdown("**Conversation options**")

                    new_title = st.text_input(
                        "Rename conversation",
                        value=title,
                        key=f"rename_input_{conversation_id}"
                    )

                    if st.button(
                        "Save name",
                        key=f"rename_button_{conversation_id}",
                        use_container_width=True
                    ):

                        if new_title.strip():
                            from services.chat_history import rename_conversation

                            rename_conversation(
                                conversation_id,
                                new_title.strip()
                            )
                            st.rerun()

                    if st.button(
                        "Delete conversation",
                        key=f"delete_button_{conversation_id}",
                        use_container_width=True
                    ):

                        from services.chat_history import delete_conversation

                        delete_conversation(conversation_id)

                        if (
                            st.session_state.active_conversation_id
                            == conversation_id
                        ):
                            start_new_chat()

                        st.rerun()

    except Exception as error:
        st.caption("Unable to load conversation history.")
        st.caption(str(error))

    st.divider()

    # Feature navigation
    st.markdown(
        '<div class="sidebar-label">YOUR WORKSPACE</div>',
        unsafe_allow_html=True
    )

    selected_feature = st.radio(
        "Navigation",
        features,
        key="main_navigation",
        label_visibility="collapsed"
    )

    st.divider()

    # Account
    st.markdown(
        '<div class="sidebar-label">ACCOUNT</div>',
        unsafe_allow_html=True
    )

    if st.session_state.is_guest:

        st.caption("You are using Guest Mode.")

        if st.button(
            "Login / Sign Up",
            use_container_width=True,
            key="sidebar_login"
        ):
            st.session_state.is_guest = False
            st.rerun()

    else:

        user_email = getattr(
            st.session_state.auth_user,
            "email",
            "User"
        )

        st.caption(f"Signed in as {user_email}")

        if st.button(
            "Sign Out",
            use_container_width=True,
            key="sidebar_logout"
        ):
            logout()

    st.divider()

    st.markdown("""
    <div style="
        color:#82789D;
        font-size:11px;
        line-height:1.8;
        padding-bottom:10px;">
        <b style="color:#B69AFF;">SHREE AI</b><br>
        Think. Create. Learn. Build.<br>
        Powered by local intelligence.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 13. MAIN HEADER
# =========================================================

header_left, header_right = st.columns(
    [3, 1],
    vertical_alignment="center"
)

with header_left:

    st.markdown(
        '<div class="main-title">✦ Shree AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Your personal intelligent workspace'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div style="text-align:right;">'
        '<span class="status-pill">● Ollama · Local AI</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.write("")

if st.session_state.is_guest:

    st.markdown("""
    <div class="guest-notice">
        ✦ Guest Mode · You can use Shree AI without an account.
    </div>
    """, unsafe_allow_html=True)

st.divider()


# =========================================================
# 14. FEATURE ROUTING
# =========================================================

if selected_feature == "💬 AI Chat":

    show_ai_chat()

elif selected_feature == "📄 Resume Analyzer":

    st.markdown("## Resume Intelligence")
    st.caption(
        "Understand your resume, identify weaknesses "
        "and discover opportunities."
    )

    show_resume_analyzer()

elif selected_feature == "🎯 ATS Score Checker":

    st.markdown("## ATS Intelligence")
    st.caption(
        "Check resume compatibility and improve "
        "your applicant tracking score."
    )

    show_ats_checker()

elif selected_feature == "📝 Smart Resume Builder":

    st.markdown("## Career Studio")
    st.caption(
        "Build a professional resume that represents your skills."
    )

    show_resume_builder()

elif selected_feature == "🎤 AI Mock Interview":

    st.markdown("## Interview Studio")
    st.caption(
        "Practise interviews, improve your answers "
        "and build confidence."
    )

    show_mock_interview()


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer-text">
    ✦ SHREE AI · COSMIC INTELLIGENCE ·
    BUILT WITH PYTHON, STREAMLIT AND OLLAMA
</div>
""", unsafe_allow_html=True)



import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# =========================================================
