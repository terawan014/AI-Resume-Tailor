# AI Resume Tailor – Setup Log

This document records the current project setup and explains how to run the project locally.

---

## 1. Current Progress

So far we have completed:

* Python development environment setup
* Virtual environment configuration
* Groq API integration
* First LLM test script (`app.py`) that rewrites resume bullet points

Next steps will include:

* Creating a structured project database (`projects.json`)
* Parsing job descriptions
* Generating tailored resumes using LLM prompts

---

## 2. Environment Setup

### Step 1 – Install Python

Install Python 3.11+ from:

https://www.python.org/downloads/

Verify installation:

python --version

---

### Step 2 – Create virtual environment

Inside the project folder terminal run:

python -m venv .venv

Activate environment:

Windows:
..venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

There should be a folder called `.venv` in the project folder then.
#### Do NOT commit `.venv` to GitHub.

---

### Step 3 – Install dependencies

pip install groq python-dotenv

---

### Step 4 – Add API key

Create a `.env` file in the project root:

GROQ_API_KEY=api_key_here

#### Do NOT commit `.env` to GitHub.

---

## 4. Run the test script

Run:

python app.py

Expected output:
The LLM should rewrite the resume bullet point into a more professional version.

---

## 5. Notes

We are currently using a free Groq LLM API for inference and there is a limit. Do not overuse it too much!

Model used:
llama-3.3-70b-versatile


