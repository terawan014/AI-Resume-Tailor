import streamlit as st

from app import generate_resume
from database import delete_resume, get_recent_resumes, init_db, save_resume


st.set_page_config(
    page_title="AI Resume Tailor",
    layout="wide",
)

init_db()

st.title("AI Resume Tailor")
st.caption("Paste your experience and a target job description to generate a tailored resume.")

with st.sidebar:
    st.header("How to use")
    st.write("1. Enter your name.")
    st.write("2. Paste your project experience.")
    st.write("3. Paste the job description.")
    st.write("4. Click Generate Resume.")

name = st.text_input("Your name", placeholder="Jane Smith")
projects = st.text_area(
    "Project experience",
    height=280,
    placeholder=(
        "Example:\n"
        "Built a full-stack task manager using React, Node.js, and MongoDB.\n"
        "Added JWT authentication and deployed with Docker.\n\n"
        "Created a data dashboard in Python using Pandas and Streamlit."
    ),
)
job = st.text_area(
    "Job description",
    height=280,
    placeholder="Paste the full job description here...",
)

generate_clicked = st.button("Generate Resume", type="primary", use_container_width=True)

st.subheader("Generated Resume")
output_box = st.empty()
output_box.info("Your tailored resume will appear here.")

if generate_clicked:
    if not name.strip():
        st.error("Please enter your name.")
    elif not projects.strip():
        st.error("Please enter your project experience.")
    elif not job.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Generating your resume... this may take a few seconds."):
                result = generate_resume(name, projects, job)
                save_resume(name, projects, job, result)

            output_box.markdown(result)
            st.success("Resume generated successfully.")
            st.download_button(
                label="Download Resume (.md)",
                data=result,
                file_name="generated_resume.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Make sure GROQ_API_KEY is configured in .env or in your deployment secrets.")

st.divider()
st.subheader("Resume History")

history = get_recent_resumes()

if not history:
    st.info("No saved resumes yet. Generate one to start building history.")
else:
    for item in history:
        job_preview = item["job_description"].strip().replace("\n", " ")
        if len(job_preview) > 90:
            job_preview = job_preview[:87] + "..."

        with st.expander(f'{item["name"]} | {item["created_at"]} | {job_preview}'):
            st.markdown(item["resume_markdown"])
            download_col, delete_col = st.columns(2)

            with download_col:
                st.download_button(
                    label=f'Download Resume #{item["id"]}',
                    data=item["resume_markdown"],
                    file_name=f'resume_{item["id"]}.md',
                    mime="text/markdown",
                    key=f'download-history-{item["id"]}',
                    use_container_width=True,
                )

            with delete_col:
                if st.button(
                    f'Delete Resume #{item["id"]}',
                    key=f'delete-history-{item["id"]}',
                    use_container_width=True,
                ):
                    delete_resume(item["id"])
                    st.success(f'Resume #{item["id"]} deleted.')
                    st.rerun()
