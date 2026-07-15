from database.supabase_client import supabase


def save_assignments(assignments):

    if not assignments:
        print("\nNo task assignments generated.")
        return

    records = []

    # ----------------------------------------
    # Build Records
    # ----------------------------------------

    for assignment in assignments:

        records.append({

            "task_id": assignment["task_id"],

            "task_name": assignment["task_name"],

            "emp_id": assignment["emp_id"],

            "employee_name": assignment["employee_name"],

            "similarity_score": assignment["similarity_score"],

            "workload_score": assignment["workload_score"],

            "final_score": assignment["final_score"]

        })

    # ----------------------------------------
    # Save Assignments
    # ----------------------------------------

    for record in records:

        # Check whether assignment already exists
        existing = (
            supabase
            .table("task_assignment")
            .select("task_id")
            .eq("task_id", record["task_id"])
            .execute()
        ).data

        if existing:

            # Update existing assignment
            (
                supabase
                .table("task_assignment")
                .update({

                    "task_name": record["task_name"],
                    "emp_id": record["emp_id"],
                    "employee_name": record["employee_name"],
                    "similarity_score": record["similarity_score"],
                    "workload_score": record["workload_score"],
                    "final_score": record["final_score"]

                })
                .eq("task_id", record["task_id"])
                .execute()
            )

        else:

            # Insert new assignment
            (
                supabase
                .table("task_assignment")
                .insert(record)
                .execute()
            )

    # ----------------------------------------
    # Console Output
    # ----------------------------------------

    print("\n" + "=" * 70)
    print("FINAL TASK ASSIGNMENTS")
    print("=" * 70)

    for assignment in records:

        print(
            f"✓ {assignment['employee_name']} "
            f"→ {assignment['task_name']} "
            f"(Final Score : {assignment['final_score']})"
        )

    print("\n" + "=" * 70)
    print(f"Assigned Tasks : {len(records)}")
    print("=" * 70)
