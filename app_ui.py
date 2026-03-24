import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from app import generate_resume
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("AI Resume Tailor")

name = st.text_input("Enter your name")

projects = st.text_area("Enter your project experience")

job = st.text_area("Paste job description")

if st.button("Generate Resume"):
    result = generate_resume(name, projects, job)
    st.markdown(result)