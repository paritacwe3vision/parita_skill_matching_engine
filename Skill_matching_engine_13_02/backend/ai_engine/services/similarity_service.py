from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_similarity(employee_vector, task_vector):

    employee_vector = np.array(employee_vector).reshape(1, -1)

    task_vector = np.array(task_vector).reshape(1, -1)

    score = cosine_similarity(
        employee_vector,
        task_vector
    )[0][0]

    return float(score)