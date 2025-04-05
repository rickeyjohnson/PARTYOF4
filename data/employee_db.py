# Simulated database of employee profiles
EMPLOYEE_DB = {}

def create_employee(employee_id, name, role, department, skills, years_experience, pfp_url=""):
    EMPLOYEE_DB[employee_id] = {
        "employee_id": employee_id,
        "name": name,
        "role": role,
        "pfp": pfp_url,
        "department": department,
        "skills": skills,
        "years_experience": years_experience,
        "feedback": {
            "manager": {"raw": "", "summary": ""},
            "peer": {"raw": "", "summary": ""},
            "self": {"raw": "", "summary": ""}
        }
    }

def get_employee(employee_id):
    return EMPLOYEE_DB.get(employee_id, {})

def get_all_employees():
    return list(EMPLOYEE_DB.keys())

def add_feedback(employee_id, source, raw_feedback):
    if employee_id in EMPLOYEE_DB and source in EMPLOYEE_DB[employee_id]["feedback"]:
        EMPLOYEE_DB[employee_id]["feedback"][source]["raw"] = raw_feedback
        EMPLOYEE_DB[employee_id]["feedback"][source]["summary"] = summarize_feedback(raw_feedback)

def summarize_feedback(raw):
    # Fake AI summary (replace with real model/API later)
    if not raw.strip():
        return "No feedback provided."
    if len(raw) < 80:
        return f"Summary: {raw}"
    return f"Summary: {raw[:75]}..."  # Truncate for now

def get_profile_summary(employee_id):
    profile = get_employee(employee_id)
    if not profile:
        return "Employee not found."

    summary_lines = [
        f"Name: {profile['name']}",
        f"Role: {profile['role']} in {profile['department']}",
        f"Skills: {', '.join(profile['skills'])}",
        f"Years of Experience: {profile['years_experience']}",
        "--- Feedback Summaries ---"
    ]

    for source, feedback in profile["feedback"].items():
        summary_lines.append(f"{source.capitalize()} Summary: {feedback['summary']}")

    return "\n".join(summary_lines)
