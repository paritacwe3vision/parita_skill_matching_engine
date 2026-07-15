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
        # print("No completed tasks found.")
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
            # print(f"Task '{task['task_name']}' already archived.")
            continue

        # ----------------------------------------
        # Fetch Assignment Details
        # ----------------------------------------

        assignment = (
            supabase
            .table("task_assignment")
            .select("*")
            .eq("task_id", task["id"])
            .execute()
        ).data

        assignment_data = assignment[0] if assignment else {}

        # ----------------------------------------
        # Insert into task_completed
        # ----------------------------------------

        response = (
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
                "status": task["status"],

                # Assignment Details
                "emp_id": assignment_data.get("emp_id"),
                "employee_name": assignment_data.get("employee_name"),
                "similarity_score": assignment_data.get("similarity_score"),
                "workload_score": assignment_data.get("workload_score"),
                "final_score": assignment_data.get("final_score")

            })
            .execute()
        )

        # ----------------------------------------
        # If insert failed, don't delete anything
        # ----------------------------------------

        if not response.data:
            # print(f"Failed to archive task '{task['task_name']}'.")
            continue

        # ----------------------------------------
        # Delete Active Assignment
        # ----------------------------------------

        (
            supabase
            .table("task_assignment")
            .delete()
            .eq("task_id", task["id"])
            .execute()
        )

        # ----------------------------------------
        # Delete Employee Workload
        # ----------------------------------------

        (
            supabase
            .table("employee_workload")
            .delete()
            .eq("task_id", task["id"])
            .execute()
        )

        # ----------------------------------------
        # Delete Task
        # ----------------------------------------

        (
            supabase
            .table("tasks")
            .delete()
            .eq("id", task["id"])
            .execute()
        )

        # print(f"✓ {task['task_name']} moved to task_completed.")

    # print("\nCompleted task migration finished.")