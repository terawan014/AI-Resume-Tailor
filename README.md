# AI-Resume-Tailor

This project includes a Streamlit web UI and can be run locally or deployed as a public link.

## Fastest way to open it

On Windows, double-click:

`Open_AI_Resume_Tailor.bat`

This will start the local web app and open it in your browser.

## Manual run

1. Create and activate `.venv`
2. Install dependencies from `requirements.txt`
3. Add `GROQ_API_KEY=...` to `.env`
4. Run:

`streamlit run app_ui.py`

## Public link deployment

The easiest way is Streamlit Community Cloud:

1. Push this project to GitHub
2. Go to Streamlit Community Cloud
3. Create a new app from this repository
4. Set the main file path to `app_ui.py`
5. In app secrets, add:

`GROQ_API_KEY="your_key_here"`

6. Deploy, and Streamlit will give you a public URL

This repo is already set up for that flow:

- `requirements.txt` contains the Python dependencies
- `app.py` supports both local `.env` and deployed secrets
- `app_ui.py` is the web entry point

## Notes

- `app.py` contains the resume generation logic
- `app_ui.py` contains the web page
- `DEV_LOG.md` records development progress
