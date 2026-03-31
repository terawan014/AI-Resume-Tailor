import streamlit as st
from app import generate_resume

st.title("AI Resume Tailor")

name = st.text_input("Enter your name")
projects = st.text_area("Enter your project experience", height=200)
job = st.text_area("Paste job description", height=200)

if st.button("Generate Resume"):

    # Input validation
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

            st.success("Resume generated!")
            st.markdown(result)

            # Download button
            st.download_button(
                label="Download Resume (.md)",
                data=result,
                file_name="generated_resume.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.info("Please check your API key or try again.")