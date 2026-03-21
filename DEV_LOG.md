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

###  Next Steps

Next we will improve the intelligence and structure of the system:

1. Improve prompt quality:

   * More controlled output format
   * Clear bullet point structure
2. Introduce project ranking logic:

   * Make LLM explicitly select top N projects
3. Improve output consistency:

   * Standardize resume bullet formatting
4. Add CLI input instead of only file-based input


