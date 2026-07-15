from database.supabase_client import supabase

from backend.resource_workload.workload_service import (
    generate_employee_workload
)


def assign_tasks():

    # ----------------------------------------
    # Fetch Similarity Matrix
    # ----------------------------------------

    matches = (
        supabase
        .table("employee_task_match")
        .select("*")
        .execute()
    ).data

    # ----------------------------------------
    # Fetch Pending Tasks
    # ----------------------------------------

    pending_tasks = (
        supabase
        .table("tasks")
        .select("id, status")
        .eq("status", "Pending")
        .execute()
    ).data

    pending_task_ids = {
        task["id"]
        for task in pending_tasks
    }

    candidates = []

    # ----------------------------------------
    # Build Candidate List
    # ----------------------------------------

    for row in matches:

        if row["task_id"] not in pending_task_ids:
            continue

        candidates.append({

            "emp_id": row["emp_id"],

            "employee_name": row["name"],

            "task_id": row["task_id"],

            "task_name": row["task_name"],

            "similarity_score": round(
                float(row["similarity_score"]), 2
            ),

            "workload_score": 0,

            "final_score": round(
                float(row["similarity_score"]), 2
            )

        })

    # ----------------------------------------
    # Highest Final Score First
    # ----------------------------------------

    candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    assigned_employees = set()
    assigned_tasks = set()

    final_assignments = []

    # ----------------------------------------
    # Assign Tasks
    # ----------------------------------------

    for row in candidates:

        if row["emp_id"] in assigned_employees:
            continue

        if row["task_id"] in assigned_tasks:
            continue

        # ----------------------------------------
        # Verify task still Pending
        # ----------------------------------------

        task = (
            supabase
            .table("tasks")
            .select("status")
            .eq("id", row["task_id"])
            .single()
            .execute()
        ).data

        if not task:
            continue

        if task["status"] != "Pending":
            continue

        # ----------------------------------------
        # Calculate Workload
        # ----------------------------------------

        workload_data = generate_employee_workload(

            emp_id=row["emp_id"],

            task_id=row["task_id"],

            similarity_score=row["similarity_score"]

        )

        row["workload_score"] = round(
            float(workload_data["workload_score"]), 2
        )

        row["final_score"] = round(
            float(workload_data["final_workload_score"]), 2
        )

        final_assignments.append(row)

        # ----------------------------------------
        # Update Task Status
        # ----------------------------------------

        (
            supabase
            .table("tasks")
            .update({
                "status": "Assigned"
            })
            .eq("id", row["task_id"])
            .execute()
        )

        assigned_employees.add(row["emp_id"])
        assigned_tasks.add(row["task_id"])

    return final_assignments