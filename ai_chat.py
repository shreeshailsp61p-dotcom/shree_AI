

import streamlit as st
import ollama

from services.chat_history import (
    initialize_database,
    create_conversation,
    save_message,
    get_messages,
)


# =========================================================
# 1. CONFIGURATION
# =========================================================

MODEL_NAME = "qwen2.5:3b"

SYSTEM_PROMPT = """
You are Shree AI, a professional and intelligent AI assistant.

Your responsibilities:

1. Help users with Python, SQL, Data Science and Generative AI.
2. Explain technical concepts from beginner to advanced level.
3. Help users build practical software and AI projects.
4. Support resume preparation and interview preparation.
5. Give accurate, clear and useful answers.
6. Use headings, bullet points and code examples when helpful.
7. Be professional, friendly and straightforward.
8. If you are uncertain, be honest.

Always focus on the user's actual question.
"""


# =========================================================
# 2. SESSION STATE
# =========================================================

def initialize_chat():

    initialize_database()

    defaults = {
        "chat_messages": [],
        "active_conversation_id": None,
        "pending_chat_prompt": None,
        "chat_error": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# 3. START NEW CHAT
# =========================================================

def start_new_chat():

    st.session_state.active_conversation_id = None
    st.session_state.chat_messages = []
    st.session_state.pending_chat_prompt = None
    st.session_state.chat_error = None

    st.rerun()


# =========================================================
# 4. OPEN PREVIOUS CONVERSATION
# =========================================================

def open_conversation(conversation_id):

    messages = get_messages(conversation_id)

    st.session_state.active_conversation_id = conversation_id

    st.session_state.chat_messages = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in messages
    ]

    st.session_state.pending_chat_prompt = None
    st.session_state.chat_error = None

    st.rerun()


# =========================================================
# 5. CHAT STYLING
# =========================================================

def apply_chat_style():

    st.markdown(
        """
        <style>

        .shree-chat-title {
            text-align: center;
            font-size: 32px;
            font-weight: 750;
            color: #F1EAFF;
            margin-bottom: 5px;
        }

        .shree-chat-subtitle {
            text-align: center;
            color: #B6A5E8;
            font-size: 14px;
            margin-bottom: 30px;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 14px;
        }

        div[data-testid="stForm"] {
            border: 1px solid rgba(160, 120, 255, 0.4);
            border-radius: 16px;
            padding: 12px;
            background: rgba(25, 20, 45, 0.5);
        }

        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(
                135deg,
                #7545D6,
                #9B63F5
            );
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            color: white;
            border: 1px solid #C3A5FF;
        }

        div[data-testid="stButton"] button {
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 6. WELCOME SCREEN
# =========================================================

def show_welcome_screen():

    st.markdown(
        "## ✦ Welcome to Shree AI",
        text_alignment="center",
    )

    st.markdown(
        "Your intelligent workspace for learning, creating, and solving problems.",
        text_alignment="center",
    )

    st.write("")

    st.markdown("### What would you like to explore?")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🐍 Learn Python",
            use_container_width=True,
            key="welcome_python",
        ):

            st.session_state.pending_chat_prompt = (
                "Teach me Python from basics with practical examples."
            )

            st.rerun()

    with col2:

        if st.button(
            "📊 Data Science",
            use_container_width=True,
            key="welcome_datascience",
        ):

            st.session_state.pending_chat_prompt = (
                "Explain the complete Data Science learning roadmap."
            )

            st.rerun()

    with col3:

        if st.button(
            "🤖 Generative AI",
            use_container_width=True,
            key="welcome_genai",
        ):

            st.session_state.pending_chat_prompt = (
                "Explain Generative AI and how I can build AI projects."
            )

            st.rerun()


# =========================================================
# 7. CHAT COMPOSER
# =========================================================

def show_chat_composer():

    with st.form(
        key="shree_ai_chat_form",
        clear_on_submit=True,
    ):

        user_prompt = st.text_input(
            "Message Shree AI",
            placeholder="Ask anything...",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "Send  ➤",
            use_container_width=True,
        )

        if submitted and user_prompt.strip():

            st.session_state.pending_chat_prompt = (
                user_prompt.strip()
            )

            st.session_state.chat_error = None

            st.rerun()


# =========================================================
# 8. SAVE USER MESSAGE
# =========================================================

def save_user_message(user_prompt):

    conversation_id = (
        st.session_state.active_conversation_id
    )

    if conversation_id is None:

        title = user_prompt[:45]

        if len(user_prompt) > 45:
            title += "..."

        conversation_id = create_conversation(title)

        st.session_state.active_conversation_id = (
            conversation_id
        )

    save_message(
        conversation_id,
        "user",
        user_prompt,
    )

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )


# =========================================================
# 9. GENERATE AI RESPONSE
# =========================================================

def generate_ai_response():

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for message in st.session_state.chat_messages:

        messages.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
    )

    answer = response["message"]["content"]

    if not answer or not answer.strip():
        raise RuntimeError("Ollama returned an empty response.")

    return answer


# =========================================================
# 10. PROCESS PENDING MESSAGE
# =========================================================

def process_pending_message():

    user_prompt = st.session_state.pending_chat_prompt

    if not user_prompt:
        return False

    # Clear the pending prompt before processing.
    st.session_state.pending_chat_prompt = None
    st.session_state.chat_error = None

    try:

        # Save user message.
        save_user_message(user_prompt)

        # Generate AI response.
        with st.spinner("✦ Shree AI is thinking..."):

            answer = generate_ai_response()

        conversation_id = (
            st.session_state.active_conversation_id
        )

        # Save assistant response.
        save_message(
            conversation_id,
            "assistant",
            answer,
        )

        # Update chat display.
        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return True

    except Exception as error:

        st.session_state.chat_error = str(error)

        return False


# =========================================================
# 11. DISPLAY CHAT MESSAGES
# =========================================================

def display_chat_messages():

    for message in st.session_state.chat_messages:

        role = message["role"]

        # Use supported built-in avatars.
        avatar = "user" if role == "user" else "assistant"

        with st.chat_message(
            role,
            avatar=avatar,
        ):

            st.markdown(message["content"])


# =========================================================
# 12. DISPLAY ERRORS
# =========================================================

def display_chat_error():

    error = st.session_state.chat_error

    if error:

        st.error(
            f"Shree AI Error: {error}"
        )

        st.caption(
            "Check your VS Code terminal for additional details."
        )


# =========================================================
# 13. MAIN AI CHAT FUNCTION
# =========================================================

def show_ai_chat():

    initialize_chat()

    apply_chat_style()

    # Main heading.
    st.markdown(
        "## ✦ Shree AI",
        text_alignment="center",
    )

    st.markdown(
        "Cosmic Intelligence • Your AI Workspace",
        text_alignment="center",
    )

    st.divider()

    # Display welcome screen or chat history.
    if not st.session_state.chat_messages:

        show_welcome_screen()

    else:

        display_chat_messages()

    # Display any previous error.
    display_chat_error()

    # Display message composer.
    show_chat_composer()

    # Process submitted message.
    if st.session_state.pending_chat_prompt:

        success = process_pending_message()

        if success:

            # Rerun to display the new AI response.
            st.rerun()

        else:

            # Do not rerun here.
            # Keep the error visible on the page.
            display_chat_error()

    # Footer.
    st.caption(
        "Shree AI can make mistakes. Verify important information."
    )
