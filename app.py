# Use the Groq API

from groq import Groq
from dotenv import load_dotenv
import os
import json


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_user_projects():
    print("\nEnter your project experiences (press Enter twice to finish):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines)


def get_job_description():
    print("\nPaste the job description (press Enter twice to finish):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines)

print("=== AI Resume Tailor ===")

name = input("\nEnter your name: ")

projects_text = get_user_projects()
job = get_job_description()

# Extract keywords from the job description
keyword_prompt = f"""
You are analyzing a job description.

Extract the most important technical skills and keywords required for this role.

Job description:
{job}

Return the result as a simple list of keywords (no explanation).
"""

keyword_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": keyword_prompt}],
    max_tokens=200
)

keywords = keyword_response.choices[0].message.content

print("Extracted Keywords:")
print(keywords)

# Create the prompt for parsing user projects into structured data
parse_prompt = f"""
You are an AI system that structures user experience into JSON.

User input:
{projects_text}

Extract and return structured data in this format:

{{
  "projects": [
    {{
      "name": "...",
      "description": "...",
      "skills": ["..."]
    }}
  ]
}}

Rules:
- Do NOT invent information
- Keep descriptions concise
- Output ONLY valid JSON
- If multiple projects exist, separate them clearly
"""

parse_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": parse_prompt}],
    max_tokens=500
)

raw_data = parse_response.choices[0].message.content

# Clean the response to extract JSON
cleaned = raw_data.replace("```json", "").replace("```", "").strip()

try:
    structured_json = json.loads(cleaned)
except:
    print("Failed to parse JSON, using raw text")
    structured_json = cleaned

print(json.dumps(structured_json, indent=2))

# Create the prompt for resume generation
prompt = f"""
You are an expert resume writer.

Your task is to generate a complete tailored resume for a candidate based on:
1. the candidate's project database
2. the target job description

Understand and structure the candidate's experiences to best match the requirements of the job description.

Job description:
{job}

Key skills required:
{keywords}

Candidate structured data:
{structured_json}

Candidate name: {name}

Requirements:
- Generate a complete resume in Markdown format
- Include these sections:
  1. Name
  2. Summary
  3. Technical Skills
  4. Technical Projects
  5. Experience or Activities (if relevant)
- Select 2-4 projects for the target job ranking based on relevance to the job description
- Rewrite project descriptions into professional resume bullet points
- Strongly align the resume content with the listed key skills
- Keep the writing concise, professional, and ATS-friendly
- Do not invent experiences that are not supported by the input
- Always strictly follow the section structure. Do not omit sections.


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