from datetime import datetime
import math

WORKING_HOURS_PER_WEEK = 48
WORKING_HOURS_PER_DAY = 8
WORKING_DAYS_PER_WEEK = 6
MAXIMUM_ACTIVE_TASKS = 10


# -----------------------------
# TOTAL WEEKLY HOURS
# -----------------------------
def calculate_total_weekly_hours(today, deadline_date):
    total_days = (deadline_date - today).days

    weeks = math.ceil(total_days / WORKING_DAYS_PER_WEEK)

    return weeks * WORKING_HOURS_PER_WEEK


# -----------------------------
# ACTIVE TASK ESTIMATION
# -----------------------------
def estimate_active_tasks(deadline_date, today):
    days = (deadline_date - today).days

    if days > 60:
        return 2
    elif days > 30:
        return 4
    elif days > 14:
        return 6
    elif days > 7:
        return 8
    else:
        return 9


# -----------------------------
# AVAILABILITY (FIXED)
# -----------------------------
def calculate_availability(total_weekly_hours):
    # Since we removed assigned_hours, we assume full capacity baseline
    free_hours = total_weekly_hours
    availability_score = 100

    return {
        "availability_score": round(availability_score, 2),
        "free_hours": free_hours,
        "weekly_hours": total_weekly_hours
    }


# -----------------------------
# WORKLOAD SCORE
# -----------------------------
def calculate_workload(total_days, total_weekly_hours, active_tasks):

    total_task_hours = total_days * WORKING_HOURS_PER_DAY

    task_load_score = (active_tasks / MAXIMUM_ACTIVE_TASKS) * 100

    hours_utilization = min(
        (total_task_hours / total_weekly_hours) * 100,
        100
    )

    workload_score = (task_load_score * 0.30) + (hours_utilization * 0.70)

    return {
        "workload_score": round(workload_score, 2),
        "hours_utilization": round(hours_utilization, 2),
        "task_load_score": round(task_load_score, 2)
    }


# -----------------------------
# RESOURCE BALANCE
# -----------------------------
def calculate_resource_balance(availability_score, workload_score):

    remaining_capacity = 100 - workload_score

    resource_balancing_score = (
        availability_score * 0.50 +
        remaining_capacity * 0.50
    )

    return round(resource_balancing_score, 2)


# -----------------------------
# FINAL PIPELINE (FIXED)
# -----------------------------
def calculate_employee_scores(deadline, skill_matching_score):
    
    today = datetime.today().date()
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

    if deadline_date <= today:
        raise ValueError("Deadline must be future date.")

    total_days = (deadline_date - today).days

    total_weekly_hours = calculate_total_weekly_hours(today, deadline_date)

    active_tasks = estimate_active_tasks(deadline_date, today)

    availability = calculate_availability(total_weekly_hours)

    workload = calculate_workload(
        total_days,
        total_weekly_hours,
        active_tasks
    )

    resource_score = calculate_resource_balance(
        availability["availability_score"],
        workload["workload_score"]
    )

    # -----------------------------
    # SKILL SCORE NORMALIZATION
    # -----------------------------
    if skill_matching_score <= 1:
        skill_matching_score *= 100

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    final_workload_score = (
        skill_matching_score * 0.70 +
        resource_score * 0.30
    )

    return {
        "deadline": deadline,
        "total_days": total_days,
        "total_task_hours": total_days * WORKING_HOURS_PER_DAY,
        "total_weekly_available_hours": total_weekly_hours,
        "free_hour_before_deadline": availability["free_hours"],

        "availability_score": availability["availability_score"],
        "active_tasks": active_tasks,
        "task_load": workload["task_load_score"],
        "hours_utilization": workload["hours_utilization"],
        "workload_score": workload["workload_score"],

        "resource_balancing_score": resource_score,
        "skill_matching_score": round(skill_matching_score, 2),

        "final_workload_score": round(final_workload_score, 2)
    }
    
