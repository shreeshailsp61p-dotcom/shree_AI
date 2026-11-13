
import streamlit as st
import ollama
import json
import re


MODEL_NAME = "qwen2.5:3b"


# ==========================================
# AI RESPONSE HELPER
# ==========================================

def ask_shree_ai(prompt):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.3,
            "num_predict": 1200
        }
    )

    return response["message"]["content"]


# ==========================================
# GENERATE INTERVIEW QUESTIONS
# ==========================================

def generate_questions(role, difficulty, count):

    prompt = f"""
You are a professional technical interviewer.

Generate exactly {count} interview questions for:

Job Role: {role}
Difficulty: {difficulty}

Requirements:
- Questions must be relevant to the selected role.
- Include technical and practical questions.
- Avoid duplicate questions.
- Adjust difficulty to the selected level.
- Return only a valid JSON array of strings.

Example:
[
    "Explain the difference between a list and tuple in Python.",
    "How would you handle missing values in a dataset?"
]
"""

    result = ask_shree_ai(prompt)

    try:

        match = re.search(
            r"\[[\s\S]*\]",
            result
        )

        if not match:
            raise ValueError("No JSON array found.")

        questions = json.loads(match.group())

        if (
            not isinstance(questions, list)
            or len(questions) != count
            or not all(
                isinstance(q, str) and q.strip()
                for q in questions
            )
        ):
            raise ValueError("Invalid question format.")

        return questions

    except (ValueError, json.JSONDecodeError):
        raise ValueError(
            "Shree AI could not generate valid questions. "
            "Please try again."
        )


# ==========================================
# ANSWER FEEDBACK
# ==========================================

def evaluate_answer(role, question, answer):

    prompt = f"""
You are an experienced interviewer evaluating a candidate.

Job Role: {role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer professionally.

Include:
1. Answer Quality: Strong, Average or Needs Improvement.
2. What Was Correct.
3. What Was Missing.
4. Technical Accuracy.
5. How to Improve the Answer.
6. Example of a Better Answer.

Be constructive, accurate and specific.
Do not assume information the candidate did not provide.
"""

    return ask_shree_ai(prompt)


# ==========================================
# FINAL INTERVIEW REPORT
# ==========================================

def generate_final_report(role, answers):

    conversation = ""

    for index, item in enumerate(answers, start=1):

        conversation += f"""
Question {index}: {item['question']}

Candidate Answer:
{item['answer']}

"""

    prompt = f"""
You are a professional interview evaluator.

Evaluate this interview for the role: {role}

Interview details:
{conversation}

Provide:

1. Overall Performance.
2. Technical Knowledge.
3. Communication Quality.
4. Strong Areas.
5. Areas Needing Improvement.
6. Recommended Topics to Study.
7. Five-Day Preparation Plan.
8. Final Interview Readiness Assessment.

Be honest and constructive.
Do not invent a numerical score without explaining
a consistent assessment basis.
"""

    return ask_shree_ai(prompt)


# ==========================================
# MOCK INTERVIEW INTERFACE
# ==========================================

def show_mock_interview():

    st.title("🎯 AI Mock Interview")

    st.write(
        "Practice interviews with Shree AI and "
        "improve your technical and communication skills."
    )

    st.caption(
        "Powered by Ollama | Local AI Interviewer"
    )

    st.divider()

    # ======================================
    # INTERVIEW SETTINGS
    # ======================================

    if "mock_started" not in st.session_state:
        st.session_state.mock_started = False

    if not st.session_state.mock_started:

        st.header("Configure Your Interview")

        role = st.selectbox(
            "Select Job Role",
            [
                "Data Analyst",
                "Python Developer",
                "SQL Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "AI Engineer",
                "Software Developer",
                "HR Interview"
            ]
        )

        difficulty = st.selectbox(
            "Select Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        count = st.selectbox(
            "Number of Questions",
            [5, 7, 10]
        )

        if st.button(
            "Start Mock Interview",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Shree AI is preparing your interview..."
                ):

                    questions = generate_questions(
                        role,
                        difficulty,
                        count
                    )

                st.session_state.mock_role = role
                st.session_state.mock_difficulty = difficulty
                st.session_state.mock_questions = questions
                st.session_state.mock_answers = []
                st.session_state.mock_index = 0
                st.session_state.mock_feedback = None
                st.session_state.mock_report = None
                st.session_state.mock_started = True

                st.rerun()

            except Exception as error:

                st.error(str(error))

    # ======================================
    # ACTIVE INTERVIEW
    # ======================================

    if st.session_state.mock_started:

        questions = st.session_state.mock_questions

        index = st.session_state.mock_index

        total = len(questions)

        st.subheader(
            f"{st.session_state.mock_role} Interview"
        )

        st.caption(
            f"Difficulty: {st.session_state.mock_difficulty}"
        )

        st.progress(
            (index + 1) / total
            if index < total
            else 1.0
        )

        # Show current question
        if index < total:

            st.markdown(
                f"### Question {index + 1} of {total}"
            )

            st.info(questions[index])

            answer = st.text_area(
                "Your Answer",
                height=180,
                placeholder="Type your answer here...",
                key=f"mock_answer_{index}"
            )

            if st.button(
                "Submit Answer",
                type="primary",
                use_container_width=True
            ):

                if not answer.strip():

                    st.warning(
                        "Please enter your answer first."
                    )

                else:

                    try:

                        with st.spinner(
                            "Shree AI is evaluating your answer..."
                        ):

                            feedback = evaluate_answer(
                                st.session_state.mock_role,
                                questions[index],
                                answer
                            )

                        st.session_state.mock_answers.append({
                            "question": questions[index],
                            "answer": answer,
                            "feedback": feedback
                        })

                        st.session_state.mock_feedback = feedback
                        st.session_state.mock_index += 1

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to evaluate answer: {error}"
                        )

        # Show last answer feedback
        if st.session_state.mock_feedback:

            st.subheader("Previous Answer Feedback")

            st.markdown(
                st.session_state.mock_feedback
            )

        # ==================================
        # FINAL REPORT
        # ==================================

        if st.session_state.mock_index >= total:

            st.success(
                "You have completed the interview!"
            )

            st.header("Final Interview Report")

            if st.button(
                "Generate Final Performance Report",
                type="primary",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Preparing your final report..."
                    ):

                        report = generate_final_report(
                            st.session_state.mock_role,
                            st.session_state.mock_answers
                        )

                    st.session_state.mock_report = report

                except Exception as error:

                    st.error(
                        f"Unable to generate report: {error}"
                    )

            if st.session_state.mock_report:

                st.markdown(
                    st.session_state.mock_report
                )

                st.download_button(
                    "Download Interview Report",
                    data=st.session_state.mock_report,
                    file_name="Shree_AI_Interview_Report.txt",
                    mime="text/plain"
                )

            if st.button("Start New Interview"):

                st.session_state.mock_started = False

                st.session_state.pop(
                    "mock_questions", None
                )

                st.rerun()
