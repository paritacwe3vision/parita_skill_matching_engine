from backend.ai_engine.models.employee_embeddings import (
    generate_employee_embeddings,
)

from backend.ai_engine.models.task_embeddings import (
    generate_task_embeddings,
)

from backend.ai_engine.services.vector_fetch_service import (
    get_employee_vectors,
    get_task_vectors,
)

from backend.ai_engine.services.recommendation_service import (
    generate_recommendations,
)

from backend.ai_engine.services.recommendation_storage_service import (
    save_recommendations,
)

from backend.ai_engine.services.task_assignment_service import (
    assign_tasks,
)

from backend.ai_engine.services.assignment_storage_service import (
    save_assignments,
)

from backend.ai_engine.services.task_completed_service import (
    move_completed_tasks,
)


# =====================================================
# STEP 0 : CHECK FOR COMPLETED TASKS
# -----------------------------------------------------
# Moves completed tasks from the active assignment table
# and updates their status before starting a new
# recommendation cycle.
# =====================================================

# print("\n" + "=" * 70)
# print("CHECKING COMPLETED TASKS")
# print("=" * 70)

move_completed_tasks()


# =====================================================
# STEP 1 : GENERATE EMPLOYEE EMBEDDINGS
# -----------------------------------------------------
# Converts every employee profile into a vector
# representation using the embedding model and stores
# the vectors inside Supabase.
# =====================================================

print("\n" + "=" * 70)
print("GENERATING EMPLOYEE EMBEDDINGS")
print("=" * 70)

generate_employee_embeddings()


# =====================================================
# STEP 2 : GENERATE TASK EMBEDDINGS
# -----------------------------------------------------
# Converts every pending task into an embedding vector
# and stores the vectors inside Supabase.
# Only tasks with status = "Pending" are processed.
# =====================================================

print("\n" + "=" * 70)
print("GENERATING TASK EMBEDDINGS")
print("=" * 70)

generate_task_embeddings()


# =====================================================
# STEP 3 : FETCH STORED VECTORS
# -----------------------------------------------------
# Retrieves employee and task embeddings from the
# vector database for similarity calculation.
#
# DEBUG
# Uncomment the print statements below if vector
# statistics are required.
# =====================================================

employee_vectors = get_employee_vectors()
task_vectors = get_task_vectors()

# print("\n" + "=" * 70)
# print("FETCHING STORED VECTORS")
# print("=" * 70)
# print(f"Employee Vectors : {len(employee_vectors)}")
# print(f"Task Vectors     : {len(task_vectors)}")


# =====================================================
# STEP 4 : GENERATE RECOMMENDATIONS
# -----------------------------------------------------
# Calculates cosine similarity between every employee
# embedding and every task embedding to generate the
# Employee ↔ Task similarity matrix.
#
# DEBUG
# Uncomment the print statements below to display
# recommendation statistics.
# =====================================================

recommendations = generate_recommendations(
    employee_vectors,
    task_vectors,
)

# print("\n" + "=" * 70)
# print("GENERATING RECOMMENDATIONS")
# print("=" * 70)
# print(f"Recommendations Generated : {len(recommendations)}")


# =====================================================
# STEP 5 : STORE RECOMMENDATIONS
# -----------------------------------------------------
# Saves the generated similarity matrix into the
# employee_task_match table.
#
# DEBUG
# Uncomment the print statements below to confirm
# recommendation storage.
# =====================================================

save_recommendations(recommendations)

# print("\n" + "=" * 70)
# print("RECOMMENDATIONS STORED SUCCESSFULLY")
# print("=" * 70)


# =====================================================
# STEP 6 : ASSIGN TASKS
# -----------------------------------------------------
# Uses the similarity matrix together with workload
# calculations to determine the best employee for each
# pending task.
# =====================================================

print("\n" + "=" * 70)
print("ASSIGNING TASKS")
print("=" * 70)

assignments = assign_tasks()

print(f"Assignments Generated : {len(assignments)}")


# =====================================================
# STEP 7 : STORE FINAL ASSIGNMENTS
# -----------------------------------------------------
# Stores the final task assignments into the
# task_assignment table for frontend consumption.
# =====================================================

save_assignments(assignments)


# =====================================================
# PIPELINE COMPLETED
# -----------------------------------------------------
# Indicates that the complete AI assignment pipeline
# executed successfully.
# =====================================================

print("\n" + "=" * 70)
print("AI PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)