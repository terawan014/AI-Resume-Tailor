import streamlit as st

from database import (
    delete_resume,
    get_recent_resumes,
    init_db,
    save_resume,
    update_resume_markdown,
)
from services.auth_service import restore_user, sign_in, sign_out, sign_up
from services.resume_service import generate_resume
from services.supabase_client import is_supabase_enabled
from utils.resume_editor import build_resume_markdown, parse_resume_markdown


def reset_history_editor_state(item):
    base_key = f'history-editor-{item["id"]}'
    parsed = parse_resume_markdown(item["resume_markdown"])
    st.session_state[f"{base_key}-name"] = parsed["name"] or item["name"]
    st.session_state[f"{base_key}-summary"] = parsed["summary"]
    st.session_state[f"{base_key}-skills"] = parsed["skills"]
    st.session_state[f"{base_key}-activities"] = parsed["activities"]
    st.session_state[f"{base_key}-project-count"] = max(len(parsed["projects"]), 1)

    for index, project in enumerate(parsed["projects"], start=1):
        st.session_state[f"{base_key}-project-title-{index}"] = project["title"]
        st.session_state[f"{base_key}-project-bullets-{index}"] = "\n".join(project["bullets"])

    st.session_state[f"{base_key}-initialized"] = True
    st.session_state[f"{base_key}-source-markdown"] = item["resume_markdown"]


def initialize_history_editor(item):
    base_key = f'history-editor-{item["id"]}'
    if not st.session_state.get(f"{base_key}-initialized"):
        reset_history_editor_state(item)
        return

    if st.session_state.get(f"{base_key}-source-markdown") != item["resume_markdown"]:
        reset_history_editor_state(item)


def build_history_resume_from_state(item):
    base_key = f'history-editor-{item["id"]}'
    project_count = st.session_state[f"{base_key}-project-count"]
    projects = []

    for index in range(1, project_count + 1):
        projects.append(
            {
                "title": st.session_state.get(f"{base_key}-project-title-{index}", ""),
                "bullets": st.session_state.get(
                    f"{base_key}-project-bullets-{index}", ""
                ).splitlines(),
            }
        )

    return build_resume_markdown(
        st.session_state.get(f"{base_key}-name", item["name"]),
        st.session_state.get(f"{base_key}-summary", ""),
        st.session_state.get(f"{base_key}-skills", ""),
        projects,
        st.session_state.get(f"{base_key}-activities", ""),
    )


def clear_all_history_editor_state():
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith("history-editor-")]
    for key in keys_to_remove:
        del st.session_state[key]


st.set_page_config(
    page_title="AI Resume Tailor",
    layout="wide",
)

init_db()

if "name_input" not in st.session_state:
    st.session_state.name_input = ""
if "projects_input" not in st.session_state:
    st.session_state.projects_input = ""
if "job_input" not in st.session_state:
    st.session_state.job_input = ""
if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = ""
if "auth" not in st.session_state:
    st.session_state.auth = {
        "access_token": None,
        "refresh_token": None,
        "user": None,
    }

st.title("AI Resume Tailor")
st.caption("Paste your experience and a target job description to generate a tailored resume.")

with st.sidebar:
    if is_supabase_enabled():
        st.header("Account")
        auth_state = st.session_state.auth

        if auth_state["access_token"] and auth_state["refresh_token"] and auth_state["user"] is None:
            try:
                auth_state["user"] = restore_user(
                    auth_state["access_token"],
                    auth_state["refresh_token"],
                )
            except Exception:
                st.session_state.auth = {"access_token": None, "refresh_token": None, "user": None}

        if st.session_state.auth["user"]:
            user_email = getattr(st.session_state.auth["user"], "email", "Signed in user")
            st.success(f"Signed in as {user_email}")
            if st.button("Sign Out", use_container_width=True):
                sign_out(
                    st.session_state.auth["access_token"],
                    st.session_state.auth["refresh_token"],
                )
                st.session_state.auth = {"access_token": None, "refresh_token": None, "user": None}
                clear_all_history_editor_state()
                st.rerun()
        else:
            auth_mode = st.radio("Auth mode", ["Sign In", "Sign Up"], horizontal=True)
            with st.form("auth_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button(auth_mode, use_container_width=True)

            if submitted:
                try:
                    if auth_mode == "Sign In":
                        auth_result = sign_in(email, password)
                        session = auth_result["session"]
                        user = auth_result["user"]
                        st.session_state.auth = {
                            "access_token": session.access_token,
                            "refresh_token": session.refresh_token,
                            "user": user,
                        }
                        clear_all_history_editor_state()
                        st.rerun()
                    else:
                        auth_result = sign_up(email, password)
                        session = auth_result["session"]
                        user = auth_result["user"]
                        if session and user:
                            st.session_state.auth = {
                                "access_token": session.access_token,
                                "refresh_token": session.refresh_token,
                                "user": user,
                            }
                            clear_all_history_editor_state()
                            st.rerun()
                        else:
                            st.success("Account created. Check your email to confirm your sign-up before signing in.")
                except Exception as error:
                    st.error(f"Authentication failed: {error}")

    st.header("How to use")
    st.write("1. Enter your name.")
    st.write("2. Paste your project experience.")
    st.write("3. Paste the job description.")
    st.write("4. Click Generate Resume.")

name = st.text_input("Your name", key="name_input", placeholder="Jane Smith")
projects = st.text_area(
    "Project experience",
    key="projects_input",
    height=280,
    placeholder=(
        "Example:\n"
        "Built a full-stack task manager using React, Node.js, and MongoDB.\n"
        "Added JWT authentication and deployed with Docker.\n\n"
        "Created a data dashboard in Python using Pandas and Streamlit."
    ),
)
job = st.text_area(
    "Job description",
    key="job_input",
    height=280,
    placeholder="Paste the full job description here...",
)

generate_clicked = st.button("Generate Resume", type="primary", use_container_width=True)

st.subheader("Generated Resume")
output_box = st.empty()

if st.session_state.generated_resume:
    output_box.markdown(st.session_state.generated_resume)
else:
    output_box.info("Your tailored resume will appear here.")

if generate_clicked:
    if not name.strip():
        st.error("Please enter your name.")
    elif not projects.strip():
        st.error("Please enter your project experience.")
    elif not job.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Generating your resume... this may take a few seconds."):
                result = generate_resume(name, projects, job)
                current_user = st.session_state.auth["user"]
                if is_supabase_enabled():
                    if current_user:
                        save_resume(name, projects, job, result, user_id=current_user.id)
                    else:
                        st.info("Resume generated. Sign in to save it to your online history.")
                else:
                    save_resume(name, projects, job, result)

            st.session_state.generated_resume = result
            output_box.markdown(result)
            st.success("Resume generated successfully.")
            st.download_button(
                label="Download Resume (.md)",
                data=result,
                file_name="generated_resume.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as error:
            st.error(f"Something went wrong: {error}")
            st.info("Make sure GROQ_API_KEY is configured in .env or in your deployment secrets.")

st.divider()
st.subheader("Resume History")

if is_supabase_enabled() and not st.session_state.auth["user"]:
    st.info("Sign in to view and manage your personal resume history.")
    history = []
    current_user_id = None
else:
    current_user_id = st.session_state.auth["user"].id if is_supabase_enabled() else None
    history = get_recent_resumes(user_id=current_user_id)

if not history:
    if not (is_supabase_enabled() and not st.session_state.auth["user"]):
        st.info("No saved resumes yet. Generate one to start building history.")
else:
    for display_index, item in enumerate(history, start=1):
        job_preview = item["job_description"].strip().replace("\n", " ")
        if len(job_preview) > 90:
            job_preview = job_preview[:87] + "..."

        with st.expander(
            f'Resume #{display_index} | {item["name"]} | {item["created_at"]} | {job_preview}'
        ):
            initialize_history_editor(item)
            base_key = f'history-editor-{item["id"]}'
            edit_col, preview_col = st.columns([1.1, 0.9])

            with edit_col:
                st.text_input(
                    "Name",
                    key=f"{base_key}-name",
                    placeholder="Candidate name",
                )
                st.text_area(
                    "Summary",
                    key=f"{base_key}-summary",
                    height=100,
                    help="Write in normal English. No markdown needed.",
                )
                st.text_area(
                    "Technical skills",
                    key=f"{base_key}-skills",
                    height=80,
                    help="Use commas to separate skills, for example: Python, SQL, LLM, Streamlit",
                )

                project_count = st.session_state[f"{base_key}-project-count"]
                st.markdown("Projects")
                for project_index in range(1, project_count + 1):
                    st.text_input(
                        f"Project {project_index} title",
                        key=f"{base_key}-project-title-{project_index}",
                        placeholder="Project title",
                    )
                    st.text_area(
                        f"Project {project_index} bullet points",
                        key=f"{base_key}-project-bullets-{project_index}",
                        height=120,
                        help="Write one bullet point per line in plain English.",
                    )

                add_col, remove_col = st.columns(2)
                with add_col:
                    if st.button(
                        f"Add Project #{display_index}",
                        key=f"{base_key}-add-project",
                        use_container_width=True,
                    ):
                        st.session_state[f"{base_key}-project-count"] += 1
                        st.rerun()
                with remove_col:
                    if st.button(
                        f"Remove Last Project #{display_index}",
                        key=f"{base_key}-remove-project",
                        use_container_width=True,
                        disabled=project_count <= 1,
                    ):
                        current_count = st.session_state[f"{base_key}-project-count"]
                        st.session_state.pop(f"{base_key}-project-title-{current_count}", None)
                        st.session_state.pop(f"{base_key}-project-bullets-{current_count}", None)
                        st.session_state[f"{base_key}-project-count"] = max(current_count - 1, 1)
                        st.rerun()

                st.text_area(
                    "Activities",
                    key=f"{base_key}-activities",
                    height=100,
                    help="Write one activity per line. Leave blank if not needed.",
                )

            edited_resume_markdown = build_history_resume_from_state(item)

            with preview_col:
                st.markdown("Preview")
                st.markdown(edited_resume_markdown)

            save_col, download_col, delete_col = st.columns(3)

            with save_col:
                if st.button(
                    f"Save Changes #{display_index}",
                    key=f'save-history-{item["id"]}',
                    use_container_width=True,
                ):
                    update_resume_markdown(
                        item["id"],
                        edited_resume_markdown,
                        user_id=current_user_id,
                    )
                    st.session_state[f"{base_key}-source-markdown"] = edited_resume_markdown
                    if st.session_state.generated_resume == item["resume_markdown"]:
                        st.session_state.generated_resume = edited_resume_markdown
                    st.success(f"Resume #{display_index} updated.")
                    st.rerun()

            with download_col:
                st.download_button(
                    label=f"Download Resume #{display_index}",
                    data=edited_resume_markdown,
                    file_name=f"resume_{display_index}.md",
                    mime="text/markdown",
                    key=f'download-history-{item["id"]}',
                    use_container_width=True,
                )

            with delete_col:
                if st.button(
                    f"Delete Resume #{display_index}",
                    key=f'delete-history-{item["id"]}',
                    use_container_width=True,
                ):
                    clear_all_history_editor_state()
                    delete_resume(item["id"], user_id=current_user_id)
                    st.success(f"Resume #{display_index} deleted.")
                    st.rerun()
