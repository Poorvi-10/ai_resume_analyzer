import streamlit as st
import pandas as pd
import plotly.express as px
from pypdf import PdfReader
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer - Smart Skill Matcher")
st.write("Upload your resume and find best job role match!")

@st.cache_data
def load_jobs():
    return pd.read_csv("data/job_roles.csv")

df_jobs = load_jobs()

def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9+, ]', ' ', text.lower())

uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf","docx"])

if uploaded:
    resume_text = extract_text(uploaded)
    st.success("Resume extracted!")
    with st.expander("See Resume Text"):
        st.text(resume_text[:2000])
    results = []
    resume_clean = clean_text(resume_text)
    for idx, row in df_jobs.iterrows():
        role = row['Job Role']
        skills_clean = clean_text(row['Required Skills'])
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_clean, skills_clean])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100
        required_skills = [s.strip().lower() for s in row['Required Skills'].split(',')]
        matched = [s for s in required_skills if s.lower() in resume_clean]
        missing = [s for s in required_skills if s.lower() not in resume_clean]
        results.append({"Job Role": role, "Match %": round(score, 2), "Matched Skills": ", ".join(matched), "Missing Skills": ", ".join(missing)})
    results_df = pd.DataFrame(results).sort_values(by="Match %", ascending=False)
    st.subheader("🎯 Best Match Results")
    st.dataframe(results_df, use_container_width=True)
    fig = px.bar(results_df, x="Job Role", y="Match %", color="Match %", title="Job Role Match Score")
    st.plotly_chart(fig)
    best = results_df.iloc[0]
    st.metric(label=f"Best Role: {best['Job Role']}", value=f"{best['Match %']}% Match")
    if best['Missing Skills']:
        st.warning(f"To become {best['Job Role']}, learn: {best['Missing Skills']}")
    else:
        st.success(f"You have all skills for {best['Job Role']}!")
else:
    st.info("Please upload a resume to start analysis")
    st.dataframe(df_jobs)