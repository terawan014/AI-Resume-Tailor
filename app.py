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

Job description:
{job}

Candidate projects:
{projects}

Tasks:
1. Select the TOP 2 most relevant projects for this job.
2. Rewrite each project into strong resume bullet points.

Output format:

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

"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=300
)


print(response.choices[0].message.content)