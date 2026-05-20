from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.container import CreateEmployeeForDepartmentUseCase, create_employee_ucr
from app.employees.schemas import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/departments", tags=["employees"])


@router.post("/{id}/employees/", response_model=EmployeeResponse)
async def create(
    id: int,
    payload: EmployeeCreate,
    use_case: Annotated[CreateEmployeeForDepartmentUseCase, Depends(create_employee_ucr)],
) -> EmployeeResponse:
    employee = await use_case.execute(
        department_id=id,
        full_name=payload.full_name,
        position=payload.position,
        hired_at=payload.hired_at,
    )
    return EmployeeResponse.model_validate(employee)
