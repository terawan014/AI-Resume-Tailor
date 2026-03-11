# Use the Groq API

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    # The messages is for testing the API for now, it will be replaced by the actual resume bullet points in the future.
    messages=[
        {
            "role": "user",
            "content": "Rewrite this resume bullet point to sound more professional: Built a browser extension to compute video duration."
        }
    ]
)

print(response.choices[0].message.content)