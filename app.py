import streamlit as st
import PyPDF2

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description Here"
)

if uploaded_file and job_description:

    try:

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text

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

        st.subheader("ATS Analysis")

        st.metric(
            "ATS Match Score",
            f"{score}%"
        )

        st.progress(score)

        if score >= 80:
            st.success("Excellent Match")
        elif score >= 60:
            st.warning("Moderate Match")
        else:
            st.error("Low Match")

        st.subheader("Matching Keywords")

        if matched:
            st.write(
                ", ".join(list(matched)[:25])
            )
        else:
            st.write(
                "No matching keywords found."
            )

        missing = jd_words - resume_words

        st.subheader("Missing Keywords")

        if missing:
            st.write(
                ", ".join(list(missing)[:25])
            )
        else:
            st.success(
                "No major keywords missing."
            )

        st.subheader("Suggestions")

        if score < 60:
            st.warning(
                """
                • Add more job-specific skills
                • Include relevant keywords
                • Improve project descriptions
                • Add measurable achievements
                """
            )

        elif score < 80:
            st.info(
                """
                • Resume is reasonably aligned
                • Add missing keywords where relevant
                • Improve project impact statements
                """
            )

        else:
            st.success(
                """
                Resume is strongly aligned with the job description.
                """
            )

    except Exception as e:
        st.error(
            f"Error processing file: {e}"
        )
