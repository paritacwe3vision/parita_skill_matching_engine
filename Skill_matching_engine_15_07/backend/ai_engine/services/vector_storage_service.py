from database.supabase_client import supabase


# ---------------------------------------------------
# Save Employee Vector
# ---------------------------------------------------
def save_employee_vector(emp_id, embedding):

    supabase.table("employee_vector").upsert(
        {
            "emp_id": emp_id,
            "embedding": embedding.tolist() if hasattr(embedding, "tolist") else embedding
        },
        on_conflict="emp_id"
    ).execute()


# ---------------------------------------------------
# Save Task Vector
# ---------------------------------------------------
def save_task_vector(task_id, task_title, embedding):

    supabase.table("task_vector").upsert(
        {
            "task_id": task_id,
            "task_title": task_title,
            "embedding": embedding.tolist() if hasattr(embedding, "tolist") else embedding
        },
        on_conflict="task_id"
    ).execute()