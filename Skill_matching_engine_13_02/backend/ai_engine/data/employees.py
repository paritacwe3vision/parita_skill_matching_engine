from database.supabase_client import supabase

# ---------------------------------------------------
# Fetch Employee Profiles
# ---------------------------------------------------

profiles = (
    supabase
    .table("employee_profiles")
    .select("*")
    .execute()
).data

# ---------------------------------------------------
# Fetch Employee Skills
# ---------------------------------------------------

skills = (
    supabase
    .table("employee_skills")
    .select("*")
    .execute()
).data

# ---------------------------------------------------
# Create Profile Lookup Dictionary
# Key = emp_id
# ---------------------------------------------------

profile_map = {
    profile["emp_id"]: profile
    for profile in profiles
}

# ---------------------------------------------------
# Build Employee List
# ---------------------------------------------------

employees = []

for skill in skills:

    emp_id = skill["emp_id"]

    profile = profile_map.get(emp_id)

    # Skip if profile doesn't exist
    if profile is None:
        print(f"⚠ Profile not found for emp_id = {emp_id}")
        continue

    # -------------------------------
    # Programming Languages
    # -------------------------------
    programming = {
        language: rating
        for language, rating in zip(
            skill.get("programming_languages", []),
            skill.get("programming_ratings", [])
        )
    }

    # -------------------------------
    # Frameworks
    # -------------------------------
    frameworks = {
        framework: rating
        for framework, rating in zip(
            skill.get("frameworks", []),
            skill.get("framework_ratings", [])
        )
    }

    # -------------------------------
    # Tools & IDE
    # -------------------------------
    tools = {
        tool: rating
        for tool, rating in zip(
            skill.get("tools_and_ide", []),
            skill.get("tools_and_ide_ratings", [])
        )
    }

    # -------------------------------
    # Final Employee Object
    # -------------------------------
    employees.append({

        "emp_id": profile["emp_id"],

        "employee_name": profile["name"],

        "email": profile["email"],

        "role": profile["role"],

        "experience_years": profile["experience_years"],

        "skills": {

            "Programming Languages": programming,

            "Frameworks": frameworks,

            "Tools & IDE": tools

        }

    })

# ---------------------------------------------------
# Debug (Optional)
# ---------------------------------------------------

print(f"\nLoaded {len(employees)} employees from Supabase.\n")