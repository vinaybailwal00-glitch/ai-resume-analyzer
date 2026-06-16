import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if uploaded_file and job_description:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    resume_words = set(
        resume_text.lower().split()
    )

    jd_words = set(
        job_description.lower().split()
    )

    matched = resume_words.intersection(jd_words)

    score = int(
        (len(matched) / max(len(jd_words), 1)) * 100
    )

    st.subheader("ATS Score")

    st.progress(score)

    st.success(f"{score}% Match")

    missing = jd_words - resume_words

    st.subheader("Missing Keywords")

    st.write(
        ", ".join(list(missing)[:20])
    )

    if score < 60:
        st.warning(
            "Add more job-specific keywords."
        )
    else:
        st.success(
            "Good resume-job match."
        )
