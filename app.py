from services.resume_service import generate_resume


def get_multiline_input(prompt):
    print(f"\n{prompt} (press Enter twice to finish):")

    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    print("=== AI Resume Tailor ===")
    name = input("\nEnter your name: ").strip()

    if not name:
        print("Error: Name cannot be empty.")
        raise SystemExit(1)

    projects_text = get_multiline_input("Enter your project experiences")
    if not projects_text.strip():
        print("Error: Project experience cannot be empty.")
        raise SystemExit(1)

    job_description = get_multiline_input("Paste the job description")
    if not job_description.strip():
        print("Error: Job description cannot be empty.")
        raise SystemExit(1)

    resume_text = generate_resume(name, projects_text, job_description)

    with open("generated_resume.md", "w", encoding="utf-8") as file:
        file.write(resume_text)

    print("\nResume generated and saved to generated_resume.md")
