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

    if not matches:
        print("No employee-task matches found.")
        return []

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

    # ----------------------------------------
    # Build Candidate List
    # ----------------------------------------

    candidates = []

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
    # Sort by Highest Similarity
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
        # Verify task is still Pending
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
        # Generate Workload
        # ----------------------------------------

        try:

            workload = generate_employee_workload(

                emp_id=row["emp_id"],

                task_id=row["task_id"],

                similarity_score=row["similarity_score"]

            )

        except Exception as e:

            print(
                f"Workload calculation failed for "
                f"{row['employee_name']} : {e}"
            )

            continue

        # ----------------------------------------
        # Update Scores
        # ----------------------------------------

        row["workload_score"] = round(
            float(workload["workload_score"]), 2
        )

        row["final_score"] = round(
            float(workload["final_workload_score"]), 2
        )

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

        final_assignments.append(row)

        assigned_employees.add(row["emp_id"])
        assigned_tasks.add(row["task_id"])

        print(
            f"✓ Assigned "
            f"{row['employee_name']} "
            f"→ {row['task_name']} "
            f"(Final Score: {row['final_score']})"
        )

    # ----------------------------------------
    # Summary
    # ----------------------------------------

    print("\n" + "=" * 70)
    print("TASK ASSIGNMENT COMPLETED")
    print("=" * 70)
    print(f"Assigned Tasks : {len(final_assignments)}")
    print("=" * 70)

    return final_assignments
