# AI Resume Tailor

AI Resume Tailor is a web app that helps users turn raw project experience and a target job description into a polished, job-tailored resume in Markdown.

It is designed for students, new grads, and developers who want a faster way to customize resumes for different roles without rewriting everything manually.

## What This Project Does

This app takes three inputs:

- Your name
- Your project experience in free text
- A target job description

It then uses an LLM pipeline to generate a resume that is more aligned with the target role.
The final output is shown directly in the web app and can be downloaded as a Markdown file.

## Tech Stack

- Python
- Streamlit
- Groq API
- `llama-3.3-70b-versatile`
- `python-dotenv`

## Project Structure

- `app_ui.py`: Streamlit frontend
- `app.py`: CLI entry point
- `services/`: backend service layer for LLM and resume generation
- `database.py`: persistence layer for resume history
- `utils/`: shared helpers for resume parsing and formatting


## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/terawan014/AI-Resume-Tailor.git
cd AI-Resume-Tailor
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

## Run the App Locally

### Option 1: Start from terminal

```bash
streamlit run app_ui.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

### Option 2: Double-click on Windows

You can also run:

- [Open_AI_Resume_Tailor.bat](/c:/Users/huashuo/Desktop/AI-Resume-Tailor/Open_AI_Resume_Tailor.bat)

This starts the Streamlit app locally in your browser.

## Deploy as a Public Website

The easiest deployment path for this project is Streamlit Community Cloud.

### Deploy with Streamlit Community Cloud

1. Push your latest code to GitHub
2. Go to `https://share.streamlit.io/`
3. Click `New app`
4. Select this repository
5. Set the main file path to `app_ui.py`
6. Add your app secret:

```toml
GROQ_API_KEY = "your_api_key_here"
```

7. Click `Deploy`

After deployment, Streamlit will generate a public URL that anyone can open in the browser.

## Deployment Notes

- The app is already structured for Streamlit Cloud deployment
- `app_ui.py` is the web entry point
- `requirements.txt` contains the deployment dependencies
- `services/llm_client.py` supports both local `.env` and Streamlit secrets
- Local files like `.env`, `resume_history.db`, `DEV_LOG.md`, `SETUP_LOG.md`, `job.txt`, and `projects.json` are already ignored by Git


## Input Tips

You will get better results if your project input includes:

- The project name
- What you built
- Tools or technologies used
- Measurable outcomes when possible
- Your individual contributions

Example project input:

```text
Built a full-stack task management web app using React, Node.js, and MongoDB.
Implemented JWT authentication and role-based access control.
Deployed the app with Docker and reduced API response time by optimizing queries.

Created a sales dashboard in Python using Pandas and Streamlit.
Cleaned and analyzed weekly sales data from CSV files.
Built charts for business trends and automated report generation.
```

## Privacy

Your project experience and job description are sent to the configured LLM provider through the Groq API in order to generate the resume. Do not paste sensitive information you would not want processed by a third-party API.

## Development Status

Current development roadmap:

- [x] Add persistent resume history with SQLite
- [x] Show saved resume history inside the app
- [ ] Deploy the app as a public website
- [x] Refactor the project into a clearer frontend/backend structure
- [ ] Add user authentication so each user can manage their own resumes
- [ ] Support exporting resumes to PDF and DOCX
- [x] Add editable resume sections after AI generation

## Troubleshooting

### Missing API key error

Make sure `GROQ_API_KEY` is set in either:

- `.env` for local runs
- Streamlit secrets for deployed runs

### `streamlit` command not found

Make sure your virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### The app opens but generation fails

Check:

- Your API key is valid
- Your internet connection is working
- The Groq API is available
- Your input is not empty
