print("EMPLOYEE FILE LOADED")  # Drashti 27/06/2026

from backend.services.feature_pipeline import process_employee

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from database.supabase_client import supabase

router = APIRouter()


# =====================================================
# Employee Models
# =====================================================

class EmployeeModel(BaseModel):

    user_id: str
    emp_id: int

    name: str
    email: str
    role: str
    experience_years: int

    programming_languages: List[str]
    programming_ratings: List[int]

    frameworks: List[str]
    framework_ratings: List[int]

    tools_and_ide: List[str]
    tools_and_ide_ratings: List[int]


class EmployeeProfileUpdate(BaseModel):

    programming_languages: List[str]
    programming_ratings: List[int]

    frameworks: List[str]
    framework_ratings: List[int]

    tools_and_ide: List[str]
    tools_and_ide_ratings: List[int]


# =====================================================
# ADD EMPLOYEE
# =====================================================

@router.post("/employee")
def add_employee(employee: EmployeeModel):

    print("EMPLOYEE ROUTE HIT")

    try:

        # =====================================
        # GET USER DETAILS FROM SIGNUP TABLE
        # =====================================

        signup_user = (

            supabase

            .table("signup")

            .select("emp_id, username, email")

            .eq("id", employee.user_id)

            .single()

            .execute()

        )

        if not signup_user.data:

            raise HTTPException(

                status_code=404,

                detail="Employee not found."

            )

        db_user = signup_user.data

        # =====================================
        # VALIDATE EMPLOYEE DETAILS
        # =====================================

        if employee.emp_id != db_user["emp_id"]:

            raise HTTPException(

                status_code=400,

                detail="Employee ID does not match the signup record."

            )

        if employee.name.strip() != db_user["username"].strip():

            raise HTTPException(

                status_code=400,

                detail="Employee name does not match the signup record."

            )

        if employee.email.strip().lower() != db_user["email"].strip().lower():

            raise HTTPException(

                status_code=400,

                detail="Employee email does not match the signup record."

            )

        # =====================================
        # FEATURE ENGINEERING
        # =====================================

        result = process_employee({

            "emp_id": db_user["emp_id"],

            "name": db_user["username"],

            "email": db_user["email"],

            "role": employee.role,

            "experience": employee.experience_years,

            "languages": employee.programming_languages,

            "frameworks": employee.frameworks,

            "tools": employee.tools_and_ide,

            "programming_ratings": employee.programming_ratings,

            "framework_ratings": employee.framework_ratings,

            "tools_and_ide_ratings": employee.tools_and_ide_ratings

        })

        # =====================================
        # UPDATE signup TABLE
        # =====================================

        supabase.table("signup").update(

            {

                "skills_completed": True

            }

        ).eq(

            "id",

            employee.user_id

        ).execute()

        return {

            "message": "Employee processed successfully",

            "result": result

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================================
# GET ALL EMPLOYEES
# =====================================================

@router.get("/employees")
def get_all_employees():

    result = (

        supabase

        .table("employee_profiles")

        .select("emp_id,name,email,role,experience_years")

        .order("emp_id")

        .execute()

    )

    return result.data


# =====================================================
# GET EMPLOYEE PROFILE
# =====================================================

@router.get("/employee/profile/{emp_id}")
def get_employee_profile(emp_id: int):

    try:

        result = (

            supabase

            .table("employee_skills")

            .select("""

                emp_id,

                name,
                    
                  programming_languages,
                    programming_ratings,
                    frameworks,
                    framework_ratings,
                    tools_and_ide,
                    tools_and_ide_ratings

            """)

            .eq("emp_id", emp_id)

            .single()

            .execute()

        )

        if not result.data:

            raise HTTPException(

                status_code=404,

                detail="Employee profile not found."

            )

        return result.data

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================================
# UPDATE EMPLOYEE PROFILE
# =====================================================

@router.put("/employee/profile/{emp_id}")
def update_employee_profile(

    emp_id: int,

    profile: EmployeeProfileUpdate
    

):
    
    try:

        result = (

            supabase

            .table("employee_skills")

            .update({

            "programming_languages": profile.programming_languages,
            "programming_ratings": profile.programming_ratings,

            "frameworks": profile.frameworks,
            "framework_ratings": profile.framework_ratings,

            "tools_and_ide": profile.tools_and_ide,
            "tools_and_ide_ratings": profile.tools_and_ide_ratings

            })

            .eq("emp_id", emp_id)

            .execute()

        )

        return {

            "message": "Employee Profile Updated Successfully",

            "data": result.data

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )