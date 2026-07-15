from database.supabase_client import supabase


def move_completed_tasks():

    # ----------------------------------------
    # Fetch all completed tasks
    # ----------------------------------------

    tasks = (
        supabase
        .table("tasks")
        .select("*")
        .eq("status", "Completed")
        .execute()
    ).data

    if not tasks:
        print("No completed tasks found.")
        return

    for task in tasks:

        # ----------------------------------------
        # Check if task already exists
        # ----------------------------------------

        exists = (
            supabase
            .table("task_completed")
            .select("task_id")
            .eq("task_id", task["id"])
            .execute()
        ).data

        if exists:
            continue

        # ----------------------------------------
        # Insert into task_completed
        # ----------------------------------------

        (
            supabase
            .table("task_completed")
            .insert({

                "task_id": task["id"],
                "task_name": task["task_name"],
                "description": task["description"],
                "technologies": task["technologies"],
                "tools_and_ide": task["tools_and_ide"],
                "required_skills": task["required_skills"],
                "duration_days": task["duration_days"],
                "starting_date": task["starting_date"],
                "deadline": task["deadline"],
                "priority": task["priority"],
                "complexity": task["complexity"],
                "status": task["status"]

            })
            .execute()
        )

        # ----------------------------------------
        # Delete from tasks table
        # ----------------------------------------

        (
            supabase
            .table("tasks")
            .delete()
            .eq("id", task["id"])
            .execute()
        )

        print(f"✓ {task['task_name']} moved to task_completed.")

    print("Completed task migration finished.")