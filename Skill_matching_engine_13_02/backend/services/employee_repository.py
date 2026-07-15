# Employee Repository
# Handles all employee-related database operations

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from database.supabase_client import supabase


# =====================================
# CREATE EMPLOYEE PROFILE
# =====================================

def create_employee_profile(data):

    result = (
        supabase
        .table("employee_profiles")
        .upsert(
            {
                "emp_id": data["emp_id"],
                "name": data["name"],
                "email": data["email"],
                "role": data["role"],
                "experience_years": data["experience"]
            },
            on_conflict="emp_id"
        )
        .execute()
    )

    if not result.data:
        raise Exception("Profile insert failed")

    return result.data[0]["id"]


# =====================================
# CREATE EMPLOYEE SKILLS
# =====================================

# =====================================
# CREATE EMPLOYEE SKILLS
# =====================================

def create_employee_skills(data):

    result = (
        supabase
        .table("employee_skills")
        .upsert(
            {
                "emp_id": data["emp_id"],
                "name": data["name"],

                "programming_languages": data.get("programming_languages", []),
                "programming_ratings": data.get("programming_ratings", []),

                "frameworks": data.get("frameworks", []),
                "framework_ratings": data.get("framework_ratings", []),

                "tools_and_ide": data.get("tools_and_ide", []),
                "tools_and_ide_ratings": data.get("tools_and_ide_ratings", [])
            },
            on_conflict="emp_id"
        )
        .execute()
    )

    return result.data


# =====================================
# CREATE EMPLOYEE FEATURES
# =====================================

def create_employee_features(
    emp_id,
    technical_score,
    learning_score,
    adaptability_score,
    execution_score
):

    result = (
        supabase
        .table("employee_features")
        .upsert(
            {
                "emp_id": emp_id,
                "technical_score": technical_score,
                "learning_score": learning_score,
                "adaptability_score": adaptability_score,
                "execution_score": execution_score
            },
            on_conflict="emp_id"
        )
        .execute()
    )

    return result.data


# =====================================
# CREATE DEFAULT WORKLOAD
# =====================================

def create_employee_workload(emp_id):

    result = (
        supabase
        .table("employee_workload")
        .insert(
            {
                "emp_id": emp_id
            }
        )
        .execute()
    )

    return result.data


# =====================================
# GET EMPLOYEE PROFILE
# =====================================

def get_employee_profile(emp_id):

    result = (
        supabase
        .table("employee_profiles")
        .select("*")
        .eq("emp_id", emp_id)
        .execute()
    )

    return result.data


# =====================================
# GET EMPLOYEE SKILLS
# =====================================

def get_employee_skills(emp_id):

    result = (
        supabase
        .table("employee_skills")
        .select("*")
        .eq("emp_id", emp_id)
        .execute()
    )

    return result.data


# =====================================
# GET EMPLOYEE UUID
# =====================================

def get_employee_id(emp_id):

    result = (
        supabase
        .table("employee_profiles")
        .select("id")
        .eq("emp_id", emp_id)
        .execute()
    )

    return result.data[0]["id"]

def get_employee_id(emp_id):

    result = (
        supabase
        .table("employee_profiles")
        .select("id")
        .eq("emp_id", emp_id)
        .execute()
    )

    if not result.data:
        raise Exception(f"Employee profile not found for emp_id={emp_id}")

    return result.data[0]["id"]
