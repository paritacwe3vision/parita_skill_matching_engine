from datetime import datetime

from backend.gemini_services.gemini_service_h import (
    get_required_skills
)


def extract_requirements(task_data):
    """
    Extract required skills and duration.
    """
    task_name = task_data.get("task_name")

    if not task_name:
        raise ValueError("Task name is missing.")

    description = task_data["description"]

    technologies = task_data.get("technologies") or []

    tools_and_ide = task_data.get("tools_and_ide") or []
#    add two parameters for technologies and tools_and_ide to the get_required_skills function call, as they are already included in the prompt for Gemini henil 9/7/2026
    # Gemini Skills
    gemini_result = get_required_skills(
    task_name=task_name,
    description=description,
    technologies=technologies,
    tools_ide=tools_and_ide
)

    gemini_skills = gemini_result.get(
    "required_skills",
    []
     )

    # Merge Everything
    required_skills = set()
        # remove two for loop for technologies and tools_and_ide, as they are already included in the prompt for Gemini henil 9/7/2026
    for skill in gemini_skills:
        if isinstance(skill, str):
            skill = skill.strip()

            if skill:
                required_skills.add(skill)

    # Duration
    # Starting Date
    try:
      start_date = datetime.strptime(
        str(task_data["starting_date"]),
        "%Y-%m-%d"
    )
    except ValueError:
      raise ValueError(
        "Invalid starting_date format. Use YYYY-MM-DD."
    )

    # Deadline
    try:
      deadline = datetime.strptime(
        str(task_data["deadline"]),
        "%Y-%m-%d"
    )
    except ValueError:
      raise ValueError(
        "Invalid deadline. Use YYYY-MM-DD."
    )

    # Date Validation
    if deadline < start_date:
      raise ValueError(
        "Deadline cannot be earlier than starting date."
    )

    # Duration
    duration_days = ( deadline - start_date ).days

    return {
        "required_skills": list(
            required_skills
        ),
        "duration_days": duration_days
    }