from database.supabase_client import supabase


# ==========================================================
# FETCH PENDING TASKS
# ----------------------------------------------------------
# Retrieves all tasks whose status is "Pending" from
# Supabase and converts each database record into the
# format required by the AI Engine.
#
# Returns:
#     List[dict] : List of pending task dictionaries.
# ==========================================================

def get_pending_tasks():

    # ------------------------------------------------------
    # Fetch only pending tasks from Supabase
    # ------------------------------------------------------

    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("status", "Pending")
        .execute()
    )

    tasks = []

    # ------------------------------------------------------
    # Convert database records into AI-friendly format
    # ------------------------------------------------------

    for row in response.data:

        task = {

            "id": row["id"],

            "title": row["task_name"],

            "description": row.get("description") or "",

            "technologies": row.get("technologies") or [],

            "tools": row.get("tools_and_ide") or [],

            "required_skills": row.get("required_skills") or [],

            "status": row.get("status")

        }

        tasks.append(task)

    # ------------------------------------------------------
    # DEBUG
    # Uncomment to verify fetched pending tasks.
    # ------------------------------------------------------

    # print(f"Pending Tasks Found : {len(tasks)}")
    # print(tasks)

    return tasks