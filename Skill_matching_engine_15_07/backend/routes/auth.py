from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.supabase_client import supabase

router = APIRouter()


# ==========================
# Signup Model
# ==========================

class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    role: str = "employee"


# ==========================
# Login Model
# ==========================

class LoginModel(BaseModel):
    email: str
    password: str


# ==========================
# Signup API
# ==========================

@router.post("/signup")
def signup(user: SignupModel):

    try:

        # -------------------------
        # Admin Signup
        # -------------------------

        if user.role == "admin":

            # Check if email already exists
            existing = (
                supabase.table("admin_signup")
                .select("id")
                .eq("email", user.email)
                .execute()
            )

            if existing.data:
                raise HTTPException(
                    status_code=400,
                    detail="Admin email already exists"
                )

            response = (
                supabase.table("admin_signup")
                .insert({
                    "username": user.username,
                    "email": user.email,
                    "password": user.password
                })
                .execute()
            )

        # -------------------------
        # Employee Signup
        # -------------------------

        else:

            # Check if email already exists
            existing = (
                supabase.table("signup")
                .select("id")
                .eq("email", user.email)
                .execute()
            )

            if existing.data:
                raise HTTPException(
                    status_code=400,
                    detail="Employee email already exists"
                )

            response = (
                supabase.table("signup")
                .insert({
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "role": "employee"
                })
                .execute()
            )

        return {
            "message": "Signup successful",
            "data": response.data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# Login API
# ==========================

@router.post("/login")
def login(user: LoginModel):

    try:

        # -------------------------
        # Check Admin Table
        # -------------------------

        admin = (
            supabase.table("admin_signup")
            .select("*")
            .eq("email", user.email)
            .execute()
        )

        if admin.data:

            db_admin = admin.data[0]

            if db_admin["password"] != user.password:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )

            return {
                "message": "Login successful",
                "user": {
                    "id": db_admin["id"],
                    "username": db_admin["username"],
                    "email": db_admin["email"],
                    "role": "admin"
                }
            }

        # -------------------------
        # Check Employee Table
        # -------------------------

        employee = (
            supabase.table("signup")
            .select("*")
            .eq("email", user.email)
            .execute()
        )

        if not employee.data:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        db_user = employee.data[0]

        if db_user["password"] != user.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "user": {
                "id": db_user["id"],
                "emp_id": db_user["emp_id"],
                "username": db_user["username"],
                "email": db_user["email"],
                "role": db_user["role"],
                "skills_completed": db_user["skills_completed"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================
# GET LOGGED-IN USER DETAILS
# =====================================

@router.get("/user/{user_id}")
def get_user(user_id: str):

    try:

        # -------------------------
        # Check Admin
        # -------------------------

        admin = (
            supabase
            .table("admin_signup")
            .select("username")
            .eq("id", user_id)
            .execute()
        )

        if admin.data:

            return {
                "username": admin.data[0]["username"],
                "role": "admin"
            }

        # -------------------------
        # Check Employee
        # -------------------------

        employee = (
            supabase
            .table("signup")
            .select("username, role")
            .eq("id", user_id)
            .single()
            .execute()
        )

        return employee.data

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )