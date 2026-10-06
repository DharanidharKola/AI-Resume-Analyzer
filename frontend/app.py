import streamlit as st
import requests

BACKEND_URL = st.secrets["BACKEND_URL"]

st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{BACKEND_URL}/upload",
    files={"file": uploaded_file})
    resume_text = response.json()["resume_text"]

    jd = st.text_area("Paste Job Description")

    if st.button("Analyze"):
        data = {
            "resume_text": resume_text,
            "job_description": jd
        }
        result = requests.post("http://127.0.0.1:8000/analyze", json=data)
        result_json = result.json()

        st.subheader("📊 Match Score")
        st.success(f"{result_json['match_score']} %")

        st.subheader("❌ Missing Keywords")
        for keyword in result_json["missing_keywords"]:
            st.markdown(f"- {keyword}")
