from fastapi import APIRouter

from backend.resource_workload.workload_service import (
    generate_employee_workload
)

from pydantic import BaseModel


router = APIRouter(
    prefix="/workload",
    tags=["Workload"]
)


class WorkloadRequest(BaseModel):

    emp_id: int


@router.post("/calculate")

def calculate_workload(request: WorkloadRequest):

    result = generate_employee_workload(
        request.emp_id
    )

    return {

        "message": "Workload calculated.",

        "data": result

    }