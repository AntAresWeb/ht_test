from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.container import (
    CreateDepartmentUseCase,
    DeleteDepartmentUseCase,
    GetDepartmentDetailsUseCase,
    MoveDepartmentUseCase,
    create_department_ucr,
    delete_department_ucr,
    get_department_ucr,
    move_department_ucr,
)
from app.departments.schemas import (
    DepartmentCreate,
    DepartmentDeleteQuery,
    DepartmentRequestQuery,
    DepartmentResponse,
    DepartmentResponseBase,
    DepartmentUpdate,
)

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/", response_model=DepartmentResponseBase)
async def create_department(
    payload: DepartmentCreate,
    use_case: Annotated[CreateDepartmentUseCase, Depends(create_department_ucr)],
) -> DepartmentResponseBase:
    department = await use_case.execute(
        name=payload.name,
        parent_id=payload.parent_id,
    )
    return DepartmentResponseBase.model_validate(department)


@router.get("/{id}", response_model=DepartmentResponse)
async def get(
    id: int,
    query_parameters: Annotated[DepartmentRequestQuery, Query()],
    use_case: Annotated[
        GetDepartmentDetailsUseCase,
        Depends(get_department_ucr),
    ],
) -> DepartmentResponse:
    return await use_case.execute(
        id,
        query_parameters.depth,
        query_parameters.include_employees,
    )


@router.patch("/{id}")
async def patch(
    id: int,
    payload: DepartmentUpdate,
    use_case: Annotated[MoveDepartmentUseCase, Depends(move_department_ucr)],
) -> DepartmentResponseBase:
    return await use_case.execute(
        department_id=id,
        new_parent_id=payload.parent_id,
        new_name=payload.name,
    )


@router.delete("/{id}")
async def delete(
    id: int,
    query_parameters: Annotated[DepartmentDeleteQuery, Query()],
    use_cases: Annotated[DeleteDepartmentUseCase, Depends(delete_department_ucr)],
) -> None:
    use_cases.execute(
        department_id=id,
        mode=query_parameters.mode,
        reassign_to_department_id=query_parameters.reassign_to_department_id,
    )
