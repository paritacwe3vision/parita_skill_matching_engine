from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List
from backend.gemini_services.requirement_extractor import extract_requirements # import this file henil 29/06
from database.supabase_client import supabase

router = APIRouter()


class TaskModel(BaseModel):
    task_name: str
    description: str

    technologies: List[str]
    tools_and_ide: List[str]
  # remove the requried_experience , estimated hour ,duration day ,req_skill from here - henil 29/06/26
    starting_date: date
    deadline: date
    complexity: str
    priority: str
class UpdateTaskStatus(BaseModel):
    task_id: str
    status: str
    deadline: date

@router.post("/task")
def create_task(task: TaskModel):
    
    # task data into dict henil 29/06/2026 start
    # Convert request data to dictionary
    task_data = task.model_dump()

    # Extract skills and duration
    extracted_data = extract_requirements(task_data)
    #  henil 29/06/2026 end

    data = {
        "task_name": task.task_name,
        "description": task.description,
        "technologies": task.technologies,
        "tools_and_ide": task.tools_and_ide,
        "required_skills": extracted_data["required_skills"],
       # remove the requried_experience , estimated hour from here - henil 29/06/26
        "duration_days": extracted_data["duration_days"],
        "starting_date": str(task.starting_date),
        "deadline": str(task.deadline),
        "complexity": task.complexity,
        "priority": task.priority
    }

    result = supabase.table("tasks").insert(data).execute()

    return {
        "message": "Task Created Successfully",
        "data": result.data
    }

# Drashti 29/06/2026 - add the below code for get assigned task for logged-in employee 

# ======================================
# GET ASSIGNED TASK FOR LOGGED-IN EMPLOYEE
# ======================================

@router.get("/employee-assignment/{emp_id}")
def get_employee_assignment(emp_id: int):

    result = (
        supabase
        .table("task_assignment")
        .select("*")
        .eq("emp_id", emp_id)
        .single()
        .execute()
    )

    return result.data

@router.get("/task-assigned/{emp_id}")
def get_task_assignment(emp_id: int):

    result = (
        supabase
        .table("task_assignment")
        .select("*")
        .eq("emp_id", emp_id)
        .execute()
    )

    if len(result.data) == 0:
        return {
            "assigned": False,
            "message": "No task assigned"
        }

    return {
        "assigned": True,
        **result.data[0]
    }

# =====================================
# ADMIN - GET ALL TASK ASSIGNMENTS
# =====================================

@router.get("/admin-task-assignments")
def get_admin_task_assignments():

    assignments = (
        supabase
        .table("task_assignment")
        .select("""
            employee_name,
            task_name,
            final_score,
            tasks(deadline)
        """)
        .execute()
    )

    data = []

    for item in assignments.data:

        deadline = ""

        if item.get("tasks"):
            deadline = item["tasks"]["deadline"]

        data.append({
            "employee": item["employee_name"],
            "task": item["task_name"],
            "deadline": deadline,
            "score": item["final_score"]
        })

    return data
# =====================================
# UPDATE TASK STATUS & DEADLINE
# =====================================

@router.put("/update-task-status")
def update_task_status(data: UpdateTaskStatus):

    # --------------------------------------------
    # Update task status
    # --------------------------------------------

    (
        supabase
        .table("tasks")
        .update({
            "status": data.status,
            "deadline": str(data.deadline)
        })
        .eq("id", data.task_id)
        .execute()
    )

    # --------------------------------------------
    # If task is not completed, stop here
    # --------------------------------------------

    if data.status.lower() != "completed":

        return {
            "message": "Task Updated Successfully"
        }

    # --------------------------------------------
    # Fetch Task
    # --------------------------------------------

    task = (

        supabase
        .table("tasks")
        .select("*")
        .eq("id", data.task_id)
        .single()
        .execute()

    ).data

    # --------------------------------------------
    # Fetch Assignment
    # --------------------------------------------

    assignment = (

        supabase
        .table("task_assignment")
        .select("employee_name")
        .eq("task_id", data.task_id)
        .single()
        .execute()

    ).data

    employee_name = None

    if assignment:
        employee_name = assignment["employee_name"]

    # --------------------------------------------
    # Insert into task_completed
    # --------------------------------------------

    (
        supabase
        .table("task_completed")
        .insert({

            "task_id": task["id"],

            "task_name": task["task_name"],

            "description": task["description"],

            "technologies": task["technologies"],

            "tools_and_ide": task["tools_and_ide"],

            "required_skills": task["required_skills"],

            "duration_days": task["duration_days"],

            "starting_date": task["starting_date"],

            "priority": task["priority"],

            "created_at": task["created_at"],

            "complexity": task["complexity"],

            "deadline": task["deadline"],

            "status": "Completed",

            "employee_name": employee_name

        })
        .execute()
    )

    # --------------------------------------------
    # Delete Assignment
    # --------------------------------------------

    (
        supabase
        .table("task_assignment")
        .delete()
        .eq("task_id", data.task_id)
        .execute()
    )

    # --------------------------------------------
    # Delete Task
    # --------------------------------------------

    (
        supabase
        .table("tasks")
        .delete()
        .eq("id", data.task_id)
        .execute()
    )

    return {

        "message": "Task Completed Successfully"

    }