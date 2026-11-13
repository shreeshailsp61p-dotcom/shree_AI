# Shree AI – AI-Powered Career Preparation Platform

Shree AI is an AI-powered career preparation platform built using Python and Streamlit. It helps students and job seekers prepare for their careers through intelligent tools for resume analysis, ATS checking, interview practice, and AI assistance.

## 🚀 Features

### 1. AI Chat
An AI-powered conversational assistant that helps users with questions, learning, and career-related guidance.

### 2. Resume Analyzer
Analyzes uploaded resumes and provides feedback to help users improve their resumes.

### 3. ATS Score Checker
Evaluates how well a resume matches a given job description and helps identify missing skills and keywords.

### 4. Smart Resume Builder
Helps users create professional resumes using customizable templates.

### 5. AI Mock Interview
Provides interview practice through AI-generated questions and responses to help users improve their interview preparation.

## 🛠️ Technologies Used

- Python
- Streamlit
- Ollama
- Qwen 2.5 (3B)
- Supabase
- Pandas
- NumPy
- PyMuPDF
- python-docx
- ReportLab
- Pillow

## 📁 Project Structure

```text
shree_AI/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── components/
├── modules/
│   ├── ai_chat.py
│   ├── ats_checker.py
│   ├── mock_interview.py
│   ├── resume_analyzer.py
│   └── resume_builder.py
│
├── services/
│   ├── chat_history.py
│   └── supabase_client.py
│
├── storage/
├── utils/
└── assets/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shreeshailsp61p-dotcom/shree_AI.git
```

### 2. Navigate to the project directory

```bash
cd shree_AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment (Windows)

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Set up Ollama

Install Ollama and download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before launching the application.

### 7. Configure environment variables

Create a `.env` file in the project root and configure the Supabase credentials required by your application.

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your_supabase_publishable_key
```

Never upload private credentials or secret keys to GitHub.

### 8. Run the application

```bash
streamlit run app.py
```

## 🎯 Project Objective

The objective of Shree AI is to make career preparation more accessible by combining AI-powered assistance, resume improvement, ATS evaluation, resume creation, and mock interview practice into one platform.

## 👨‍💻 Developer

**Shreeshail**

GitHub: [shreeshailsp61p-dotcom](https://github.com/shreeshailsp61p-dotcom)

---

*Shree AI – Your intelligent companion for career preparation.*