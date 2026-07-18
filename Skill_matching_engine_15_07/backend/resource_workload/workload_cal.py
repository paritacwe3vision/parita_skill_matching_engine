from datetime import datetime
import math
import os
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Ensure that SUPABASE_URL and SUPABASE_KEY are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key not found in environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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


# parita chauhan 7-15-2026 , start 
# -----------------------------
# ACTIVE TASK COUNT
# -----------------------------
def estimate_active_tasks_from_supabase(emp_id):

    try:

        response = (
            supabase
            .table("task_assignment")
            .select("id", count="exact")
            .eq("emp_id", emp_id)
            .execute()
        )

        return response.count or 0

    except Exception as e:

        print(f"Error fetching active tasks: {e}")

        return 0
    
# parita chauhan 7-15-2026 , end

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
# ----------------------------------------------------------
# FINAL WORKLOAD PIPELINE
# ----------------------------------------------------------
def calculate_employee_scores(deadline, skill_matching_score, emp_id):

    # ------------------------------------------------------
    # Validate Deadline
    # ------------------------------------------------------
    today = datetime.today().date()
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

    if deadline_date <= today:
        raise ValueError("Deadline must be a future date.")

    # ------------------------------------------------------
    # Time Calculations
    # ------------------------------------------------------
    total_days = (deadline_date - today).days

    total_weekly_hours = calculate_total_weekly_hours(
        today,
        deadline_date
    )

    # ------------------------------------------------------
    # ACTIVE TASKS
    # ------------------------------------------------------
    # Count currently assigned tasks from the database.
    active_tasks_before_assignment = estimate_active_tasks_from_supabase(
        emp_id
    )

    # ------------------------------------------------------
    # AFTER NEW ASSIGNMENT
    # ------------------------------------------------------
    # We are evaluating the employee after assigning
    # the current task.
    active_tasks_after_assignment = (
        active_tasks_before_assignment + 1
    )

    # ------------------------------------------------------
    # Availability
    # ------------------------------------------------------
    availability = calculate_availability(
        total_weekly_hours
    )

    # ------------------------------------------------------
    # Workload
    # ------------------------------------------------------
    workload = calculate_workload(
        total_days=total_days,
        total_weekly_hours=total_weekly_hours,
        active_tasks=active_tasks_after_assignment
    )
    # ------------------------------------------------------
    # Resource Balancing
    # ------------------------------------------------------
    resource_score = calculate_resource_balance(
        availability_score=availability["availability_score"],
        workload_score=workload["workload_score"]
    )

    # ------------------------------------------------------
    # Skill Score Normalization
    # ------------------------------------------------------
    if skill_matching_score <= 1:
        skill_matching_score *= 100

    # ------------------------------------------------------
    # Final Score
    # ------------------------------------------------------
    final_workload_score = (
        skill_matching_score * 0.70 +
        resource_score * 0.30
    )

    # ------------------------------------------------------
    # Return Results
    # ------------------------------------------------------
    return {

        "deadline": deadline,
        "total_days": total_days,

        "total_task_hours": total_days * WORKING_HOURS_PER_DAY,
        "total_weekly_available_hours": total_weekly_hours,
        "free_hour_before_deadline": availability["free_hours"],

     # --------------------------------------------------
        # Task Information
        # --------------------------------------------------
        "active_tasks_before_assignment":
            active_tasks_before_assignment,

        "new_task_assigned":
            True,

        "active_tasks_after_assignment":
            active_tasks_after_assignment,

        # Availability
        "availability_score": availability["availability_score"],

        # Workload
        "task_load": workload["task_load_score"],
        "hours_utilization": workload["hours_utilization"],
        "workload_score": workload["workload_score"],

        # Resource Balancing
        "resource_balancing_score": resource_score,
        # Skill Matching
        "skill_matching_score": round(skill_matching_score, 2),

        # Final Score
        "final_workload_score": round(final_workload_score, 2)
    }