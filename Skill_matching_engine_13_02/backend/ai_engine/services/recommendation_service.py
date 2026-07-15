from backend.ai_engine.services.similarity_service import (
    calculate_similarity,
)


# ==========================================================
# GENERATE EMPLOYEE-TASK RECOMMENDATIONS
# ----------------------------------------------------------
# Compares every employee embedding with every task
# embedding using cosine similarity.
#
# The generated similarity score is converted into a
# percentage and classified into a matching category.
#
# Returns:
#     List[dict] : Employee ↔ Task recommendation matrix.
# ==========================================================

def generate_recommendations(employee_vectors, task_vectors):

    recommendations = []

    # ------------------------------------------------------
    # DEBUG
    # Uncomment to display similarity generation.
    # ------------------------------------------------------

    # print("\nGenerating Employee-Task Similarity Matrix...\n")

    # ------------------------------------------------------
    # Compare every employee against every task.
    #
    # This creates a complete similarity matrix where
    # each employee receives a similarity score for
    # every available task.
    # ------------------------------------------------------

    for employee in employee_vectors:

        for task in task_vectors:

            # --------------------------------------------------
            # Calculate cosine similarity between employee
            # embedding and task embedding.
            # --------------------------------------------------

            score = calculate_similarity(
                employee["embedding"],
                task["embedding"]
            )

            # --------------------------------------------------
            # Convert similarity score into percentage.
            # --------------------------------------------------

            percentage = round(score * 100, 2)

            # --------------------------------------------------
            # Classify similarity score into matching level.
            # --------------------------------------------------

            if percentage >= 90:
                status = "Excellent Match"

            elif percentage >= 75:
                status = "Good Match"

            elif percentage >= 60:
                status = "Average Match"

            else:
                status = "Poor Match"

            # --------------------------------------------------
            # Store recommendation record.
            # This data is later saved into the
            # employee_task_match table.
            # --------------------------------------------------

            recommendations.append({

                "emp_id": employee["emp_id"],

                "task_id": task["task_id"],

                "task_name": task["task_title"],

                "similarity_score": percentage,

                "status": status

            })

            # --------------------------------------------------
            # DEBUG
            # Uncomment to display similarity score for every
            # Employee ↔ Task pair.
            # --------------------------------------------------

            # print(
            #     f"✓ Employee {employee['emp_id']} "
            #     f"↔ {task['task_title']} "
            #     f"({percentage}%)"
            # )

    # ------------------------------------------------------
    # DEBUG
    # Uncomment to display total recommendations generated.
    # ------------------------------------------------------

    # print(f"\nTotal Recommendation Records : {len(recommendations)}")

    # ------------------------------------------------------
    # Return complete Employee ↔ Task similarity matrix.
    # ------------------------------------------------------

    return recommendations