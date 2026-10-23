# AI Resume Analyzer and Job Recommendation System

## Project Objective
Build an NLP-based application that helps students understand how well their resume matches selected job roles. Provides match score, missing skills, and learning roadmap.

## Tools Used
- Python, pypdf, python-docx
- Pandas, Scikit-learn (TF-IDF + Cosine Similarity)
- Streamlit (UI), Plotly (Charts)

## How to Run
pip install -r requirements.txt
streamlit run app.py
Then open http://localhost:8501

## Features
- Upload PDF/DOCX resume
- Extract text and clean
- Identify 30+ skills
- Compare with 5 roles: Data Analyst, ML Engineer, AI Engineer, NLP Engineer, CV Engineer
- Match score %, Bar chart, Top 3 roles, Missing skills, Roadmap

## Folder Structure
ai_resume_analyzer/
|-- app.py
|-- requirements.txt
|-- README.md
|-- data/job_roles.csv
|-- sample_resumes/

## Responsible AI
Only evaluates job skills. Does NOT score gender, age, religion, photo. Scores are estimates.

Major Project - Student Learning Purpose