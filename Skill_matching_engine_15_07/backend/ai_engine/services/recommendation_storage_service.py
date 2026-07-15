from database.supabase_client import supabase


def save_recommendations(recommendations):

    for recommendation in recommendations:

        # ---------------------------------------------
        # Fetch Employee Name
        # ---------------------------------------------
        employee = (
            supabase
            .table("employee_profiles")
            .select("name")
            .eq("emp_id", recommendation["emp_id"])
            .single()
            .execute()
        )

        employee_name = employee.data["name"]

        # ---------------------------------------------
        # Save Recommendation
        # ---------------------------------------------
        (
       supabase.table("employee_task_match").upsert(
    {
        "emp_id": recommendation["emp_id"],
        "name": employee_name,
        "task_id": recommendation["task_id"],
        "task_name": recommendation["task_name"],
        "similarity_score": recommendation["similarity_score"],
        "status": recommendation["status"]
    },
    on_conflict="emp_id,task_id"
).execute()
        )

    print("\n✓ Recommendations saved successfully.")