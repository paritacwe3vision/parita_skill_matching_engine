from ai_engine.services.vector_fetch_service import (
    get_employee_vectors,
    get_task_vectors,
)

employee_vectors = get_employee_vectors()
task_vectors = get_task_vectors()

print("=" * 60)
print("EMPLOYEE VECTOR")
print("=" * 60)

print(employee_vectors[0])

print()

print("=" * 60)
print("TASK VECTOR")
print("=" * 60)

print(task_vectors[0])