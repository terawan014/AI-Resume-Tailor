def normalize_bullet_text(line):
    stripped = line.strip()
    for prefix in ("- ", "* ", "鈥?", "閳?"):
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return stripped


def parse_resume_markdown(resume_markdown):
    normalized = resume_markdown.replace("\r\n", "\n").replace("閳?", "- ")
    lines = normalized.split("\n")

    parsed = {
        "name": "",
        "summary": "",
        "skills": "",
        "activities": "",
        "projects": [],
    }

    current_section = None
    section_lines = {"summary": [], "skills": [], "activities": []}
    current_project = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            parsed["name"] = line[2:].strip()
            continue
        if line == "## Summary":
            current_section = "summary"
            current_project = None
            continue
        if line == "## Technical Skills":
            current_section = "skills"
            current_project = None
            continue
        if line == "## Technical Projects":
            current_section = "projects"
            current_project = None
            continue
        if line == "## Activities":
            current_section = "activities"
            current_project = None
            continue

        if current_section == "projects":
            if line.startswith("**Project:") and line.endswith("**"):
                title = line.replace("**Project:", "").replace("**", "").strip()
                current_project = {"title": title, "bullets": []}
                parsed["projects"].append(current_project)
            elif current_project is not None:
                current_project["bullets"].append(normalize_bullet_text(line))
        elif current_section in section_lines:
            section_lines[current_section].append(normalize_bullet_text(line))

    parsed["summary"] = " ".join(section_lines["summary"]).strip()
    parsed["skills"] = ", ".join(
        [part.strip() for line in section_lines["skills"] for part in line.split(",") if part.strip()]
    )
    parsed["activities"] = "\n".join(section_lines["activities"]).strip()

    if not parsed["projects"]:
        parsed["projects"].append({"title": "", "bullets": []})

    return parsed


def build_resume_markdown(name, summary, skills, projects, activities):
    lines = [f"# {name.strip()}", "", "## Summary", summary.strip(), "", "## Technical Skills"]
    lines.append(", ".join([part.strip() for part in skills.split(",") if part.strip()]))
    lines.extend(["", "## Technical Projects", ""])

    for project in projects:
        title = project["title"].strip()
        bullets = [bullet.strip() for bullet in project["bullets"] if bullet.strip()]
        if not title and not bullets:
            continue

        lines.append(f"**Project: {title or 'Untitled Project'}**")
        for bullet in bullets:
            lines.append(f"- {bullet}")
        lines.append("")

    activity_lines = [line.strip() for line in activities.splitlines() if line.strip()]
    if activity_lines:
        lines.extend(["## Activities"])
        for activity in activity_lines:
            lines.append(f"- {activity}")

    return "\n".join(lines).strip()
