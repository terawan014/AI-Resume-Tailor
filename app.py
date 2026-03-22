# Use the Groq API

from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load the projects from the JSON file
with open("projects.json", "r") as f:
    projects = json.load(f)

# Load the job description from the text file
with open("job.txt", "r") as f:
    job = f.read()


prompt = f"""
You are an expert resume writer.

Your task is to generate a complete tailored resume for a candidate based on:
1. the candidate's project database
2. the target job description

Job description:
{job}

Candidate project database:
{projects}


Requirements:
- Generate a complete resume in Markdown format
- Include these sections:
  1. Name
  2. Summary
  3. Technical Skills
  4. Technical Projects
  5. Experience or Activities (if relevant)
- Select 2-4 relevant projects for the target job
- Rewrite project descriptions into professional resume bullet points
- Prioritize keywords from the job description
- Keep the writing concise, professional, and ATS-friendly
- Do not invent experiences that are not supported by the input

Project format:

Project: <project name>
• Bullet point 1
• Bullet point 2

Project: <project name>
• Bullet point 1
• Bullet point 2

Rules:
- Use bullet points starting with "•"
- Each bullet should start with an action verb
- Focus on impact and technical skills
- Output only the final resume
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=1200
)


resume_text = response.choices[0].message.content

# Save the generated resume to a Markdown file
with open("generated_resume.md", "w", encoding="utf-8") as f:
    f.write(resume_text)

print("Resume generated and saved to generated_resume.md")