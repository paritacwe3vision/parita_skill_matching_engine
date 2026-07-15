from database.supabase_client import supabase
import ast


# --------------------------------------------------------
# Fetch Employee Vectors
# --------------------------------------------------------

def get_employee_vectors():

    response = (
        supabase
        .table("employee_vector")
        .select("*")
        .execute()
    )

    employee_vectors = response.data

    for employee in employee_vectors:

        embedding = employee["embedding"]

        # Convert string -> Python list
        if isinstance(embedding, str):
            employee["embedding"] = ast.literal_eval(embedding)

    return employee_vectors


# --------------------------------------------------------
# Fetch Task Vectors
# --------------------------------------------------------

def get_task_vectors():

    response = (
        supabase
        .table("task_vector")
        .select("*")
        .execute()
    )

    task_vectors = response.data

    for task in task_vectors:

        embedding = task["embedding"]

        # Convert string -> Python list
        if isinstance(embedding, str):
            task["embedding"] = ast.literal_eval(embedding)

    return task_vectors