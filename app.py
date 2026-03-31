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
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
              break
            else:
                empty_count = 0
                lines.append(line)

    return "\n".join(lines)


def get_job_description():
    print("\nPaste the job description (press Enter twice to finish):")

    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)

    return "\n".join(lines)

def generate_resume(name, projects_text, job):
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
        structured_data = json.loads(cleaned)
        structured_json = json.dumps(structured_data, indent=2)
        print("\nParsed Projects:")
        print(structured_json)
    except json.JSONDecodeError:
        print("\nWarning: JSON parsing failed, attempting recovery...")
        fix_prompt = f"""
The following text should be valid JSON but has formatting errors.
Fix it and return ONLY valid JSON, nothing else:
 
{cleaned}
"""
        fix_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": fix_prompt}],
            max_tokens=500
        )
        fixed = fix_response.choices[0].message.content
        fixed_cleaned = fixed.replace("```json", "").replace("```", "").strip()
 
        try:
            structured_data = json.loads(fixed_cleaned)
            structured_json = json.dumps(structured_data, indent=2)
            print("Recovery successful.")
            print(structured_json)
        except json.JSONDecodeError:
            # Final fallback: pass raw text but warn
            print("Warning: Could not parse JSON after recovery. Using raw text.")
            structured_json = projects_text

    
    # Create the prompt for resume generation
    prompt = f"""
You are an expert resume writer. Generate a complete, professional, ATS-friendly resume in Markdown format.
 
Below is an example of the exact output format you must follow:
 
---
# Jane Smith
 
## Summary
Results-driven software engineer with 2 years of experience building full-stack web applications. Proficient in Python, React, and cloud deployment. Passionate about clean code and scalable systems.
 
## Technical Skills
Python, React, Node.js, PostgreSQL, Docker, AWS, Git
 
## Technical Projects
 
**Project: E-Commerce Platform**
• Developed a full-stack e-commerce application using React and Node.js, reducing page load time by 30%
• Integrated Stripe payment API to handle secure transactions for 500+ monthly users
• Deployed on AWS EC2 with Docker containerization, achieving 99.9% uptime
 
**Project: Data Pipeline Tool**
• Built an automated ETL pipeline in Python to process 10,000+ records daily from REST APIs
• Designed PostgreSQL schema and optimized queries, improving data retrieval speed by 40%
• Implemented error handling and logging to ensure pipeline reliability
 
## Activities
• Teaching Assistant, Introduction to Programming – supported 30 students with weekly lab sessions
---
 
Now generate a resume for the following candidate:
 
Job description:
{job}
 
Key skills required:
{keywords}
 
Candidate projects (structured):
{structured_json}
 
Candidate name: {name}
 
Requirements:
- Follow the exact format shown in the example above
- Include these sections: Name, Summary, Technical Skills, Technical Projects, Activities (if relevant)
- Select 2-4 most relevant projects and rank them by relevance to the job
- Each project must have 2-3 bullet points starting with a strong action verb
- Each bullet point MUST start on a new line with "• " (bullet + space)
- Summary must be 2-3 sentences, tailored to the job description
- Technical Skills must include keywords from the job description where applicable
- Do not invent experiences not supported by the input
- If the candidate has no activities or experience, write "• No additional activities to report" under Activities
- Output only the final resume, no explanation
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
 
    resume_text = response.choices[0].message.content
    resume_text = resume_text.replace("• ", "\n• ").strip()
    return resume_text
 
 
if __name__ == "__main__":
    print("=== AI Resume Tailor ===")
    name = input("\nEnter your name: ").strip()
 
    if not name:
        print("Error: Name cannot be empty.")
        exit(1)
 
    projects_text = get_user_projects()
    if not projects_text.strip():
        print("Error: Project experience cannot be empty.")
        exit(1)
 
    job = get_job_description()
    if not job.strip():
        print("Error: Job description cannot be empty.")
        exit(1)
 
    resume_text = generate_resume(name, projects_text, job)
 
    with open("generated_resume.md", "w", encoding="utf-8") as f:
        f.write(resume_text)
 
    print("\nResume generated and saved to generated_resume.md")

