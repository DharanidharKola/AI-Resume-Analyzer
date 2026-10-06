import io
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score_percentage = round(score * 100, 2)

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    missing_skills = list(jd_words - resume_words)[:10]

    return {
        "match_score": score_percentage,
        "missing_keywords": missing_skills
    }