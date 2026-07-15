def rating_to_level(rating):
    """
    Convert numerical rating (1-5) into a skill level.
    """

    levels = {
        1: "Beginner",
        2: "Basic",
        3: "Intermediate",
        4: "Advanced",
        5: "Expert"
    }

    return levels.get(rating, "Unknown")


# ==========================================================
# Build Employee Text
# ==========================================================

def build_employee_text(employee):

    text = f"Employee Name: {employee['employee_name']}\n\n"

    text += (
        "This employee has experience in the following "
        "programming skills and development tools.\n\n"
    )

    for category, skills in employee["skills"].items():

        text += f"{category}:\n"

        for skill, rating in skills.items():

            level = rating_to_level(rating)

            text += (
                f"- {skill}: {level} proficiency "
                f"({rating}/5)\n"
            )

        text += "\n"

    return text


# ==========================================================
# Build Task Text
# ==========================================================

def build_task_text(task):

    text = f"Task Name: {task['title']}\n\n"

    text += (
        f"Project Description:\n"
        f"{task['description']}\n\n"
    )

    text += (
        "This project requires knowledge of the following "
        "technologies:\n"
    )

    for technology in task["technologies"]:

        text += f"- {technology}\n"

    text += "\n"

    text += (
        "Recommended development tools for this project:\n"
    )

    for tool in task["tools"]:

        text += f"- {tool}\n"

    return text