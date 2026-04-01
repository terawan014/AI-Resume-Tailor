# Development Log

## Milestone 1 – LLM Environment Setup & API Integration

### ✅ Completed

* Set up Python development environment (Python 3.14)
* Configured virtual environment (`.venv`) for dependency isolation
* Set up environment variable management using `.env`
* Successfully integrated Groq API
* Built a simple prototype that rewrites resume bullet points using LLM

---
### Current Project State

The project is currently able to:

* Send prompts to an LLM
* Receive and display generated responses
* Perform basic resume bullet point rewriting

---

## Milestone 2 – Structured Data & Prompt Pipeline

### ✅ Completed

* Designed and created a structured project database (`projects.json`)

  * Converted resume projects into structured format (name, description, skills, tags)
* Added job description input file (`job.txt`)
* Implemented data loading pipeline in Python:

  * Read project data from JSON
  * Read job description from text file
* Designed first multi-input LLM prompt combining:

  * Candidate projects
  * Job description
* Upgraded LLM usage from single-sentence rewriting → structured task:

  * Selecting relevant projects
  * Rewriting them into resume bullet points

---

### Current Project State

The system can now:

* Take **multiple projects + job description**
* Analyze relevance using LLM
* Generate tailored resume-style bullet points

Pipeline:

projects.json + job.txt → LLM → tailored output

---

## Milestone 3 – Full Resume Generation & Job-Aware Optimization

### ✅ Completed

* Expanded candidate data structure in `projects.json`

  * Added personal info, education, skills, and activities
  * Improved project descriptions with structured fields
* Redesigned LLM prompt from simple rewriting → full resume generation
* Added output file generation (`generated_resume.md`)
* Introduced **job-aware keyword extraction step**

  * Extracted key skills from job description using LLM
  * Injected extracted keywords into resume generation prompt
* Improved alignment between resume content and job requirements
* Reduced generic outputs and increased relevance to target role

---

### Current Project State

The system now supports:

* Job description understanding via keyword extraction
* Targeted resume tailoring based on role requirements
* File-based output for generated resumes

Pipeline:

job.txt
↓
LLM → extract keywords
↓
projects.json + keywords
↓
LLM → generate tailored resume
↓
generated_resume.md

---

## Milestone 4 – User Input Pipeline & Product-Oriented CLI

### ✅ Completed

* Replaced file-based inputs (`projects.json`, `job.txt`) with **fully user-driven input**

  * Implemented interactive CLI for:

    * User name input
    * Project experience input (free text)
    * Job description input
* Removed hardcoded data sources and improved flexibility of the system
* Added multi-stage LLM pipeline:

  1. Keyword extraction from job description
  2. Parsing unstructured user input into structured JSON
  3. Resume generation using structured data and extracted keywords
* Enabled system to process raw, unstructured user input and convert it into professional resume content
* Improved prompt design for:

  * Better alignment with job requirements
  * Cleaner and more consistent output formatting

### Current Project State

The system is now a **fully interactive CLI-based AI application**.

Capabilities:

* Accepts user-provided project experience (no predefined dataset)
* Understands and structures raw user input using LLM
* Extracts job-relevant keywords automatically
* Generates a complete, job-tailored resume
* Outputs a ready-to-use Markdown resume file

---

## Milestone 5 – Web UI Integration & Stability Issues

### ✅ Completed

* Built the first web-based interface using Streamlit
* Integrated the existing multi-stage LLM pipeline into the UI
* Refactored core logic into a reusable function (`generate_resume`)

  * Enabled reuse across both CLI and UI environments
  * Improved code modularity and separation of concerns
* Enabled real-time display of generated resume in Markdown format

---

### ⚠️ Current Issues

* Output quality is **inconsistent across runs**

  * Weak or repetitive bullet points
  * Poor alignment with job description
  * Poor stucture markdown format

* UI lacks validation and error handling

  * No safeguards for empty or low-quality inputs

---









