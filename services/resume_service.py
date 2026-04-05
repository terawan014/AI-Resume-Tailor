import json

from services.llm_client import get_client


MODEL_NAME = "llama-3.3-70b-versatile"


def extract_keywords(job_description):
    client = get_client()
    prompt = f"""
    You are analyzing a job description.

    Extract the most important technical skills and keywords required for this role.

    Job description:
    {job_description}

    Return the result as a simple list of keywords (no explanation).
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content


def parse_projects(projects_text):
    client = get_client()
    prompt = f"""
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

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    cleaned = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()

    try:
        return json.dumps(json.loads(cleaned), indent=2)
    except json.JSONDecodeError:
        fix_prompt = f"""
The following text should be valid JSON but has formatting errors.
Fix it and return ONLY valid JSON, nothing else:
 
{cleaned}
"""
        fix_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": fix_prompt}],
            max_tokens=500,
        )
        fixed = fix_response.choices[0].message.content.replace("```json", "").replace("```", "").strip()

        try:
            return json.dumps(json.loads(fixed), indent=2)
        except json.JSONDecodeError:
            return projects_text


def generate_resume(name, projects_text, job_description):
    client = get_client()
    keywords = extract_keywords(job_description)
    structured_projects = parse_projects(projects_text)

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
- Developed a full-stack e-commerce application using React and Node.js, reducing page load time by 30%
- Integrated Stripe payment API to handle secure transactions for 500+ monthly users
- Deployed on AWS EC2 with Docker containerization, achieving 99.9% uptime
 
**Project: Data Pipeline Tool**
- Built an automated ETL pipeline in Python to process 10,000+ records daily from REST APIs
- Designed PostgreSQL schema and optimized queries, improving data retrieval speed by 40%
- Implemented error handling and logging to ensure pipeline reliability
 
## Activities
- Teaching Assistant, Introduction to Programming - supported 30 students with weekly lab sessions
---
 
Now generate a resume for the following candidate:
 
Job description:
{job_description}
 
Key skills required:
{keywords}
 
Candidate projects (structured):
{structured_projects}
 
Candidate name: {name}
 
Requirements:
- Follow the exact format shown in the example above
- Include these sections: Name, Summary, Technical Skills, Technical Projects, Activities (if relevant)
- Select 2-4 most relevant projects and rank them by relevance to the job
- Each project must have 2-3 bullet points starting with a strong action verb
- Summary must be 2-3 sentences, tailored to the job description
- Technical Skills must include keywords from the job description where applicable
- Projects must ONLY come from the candidate's structured data. Never use the job description as a project source
- Do not invent experiences not supported by the input
- Output only the final resume, no explanation
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    return response.choices[0].message.content.replace("鈥?", "\n- ").replace("閳?", "\n- ").strip()
