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

### Next Steps

We will begin transitioning from a prototype to a user-facing product:

1. Replace file-based input with interactive input

   * CLI-based input (short term)
   * Web interface (long term)
2. Improve output reliability:

   * More consistent formatting
   * Controlled section structure
3. Enhance decision logic:

   * Explicit project ranking / scoring
   * Better keyword-to-project matching
4. Prepare for user experience layer:

   * Input → generate → view result workflow






