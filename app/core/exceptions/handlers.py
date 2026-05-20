from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions.exceptions import (
    AppExceptionError,
    DepartmentCycleError,
    DepartmentHasEmployeesError,
    DepartmentNameConflictError,
    DepartmentNotFoundError,
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    InvalidParentError,
)
from app.core.exceptions.registry import ExceptionRegistry

registry = ExceptionRegistry()


@registry.register(AppExceptionError)
async def handle_app_exception(_: Request, exc: AppExceptionError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {"message": exc.message}},
    )

@registry.register(DepartmentNotFoundError)
async def department_not_found_handler(
    _: Request,
    exc: DepartmentNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.message}},
    )


@registry.register(DepartmentNameConflictError)
async def department_name_conflict_handler(
    _: Request,
    exc: DepartmentNameConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": {"message": exc.message}},
    )


@registry.register(DepartmentCycleError)
async def circular_move_error_handler(
    _: Request,
    exc: DepartmentCycleError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": {"message": exc.message}},
    )


@registry.register(InvalidParentError)
async def invalid_parent_handler(
    _: Request,
    exc: InvalidParentError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.message}},
    )


@registry.register(DepartmentHasEmployeesError)
async def department_has_employees_handler(
    _: Request,
    exc: DepartmentHasEmployeesError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.message}},
    )


@registry.register(EmployeeNotFoundError)
async def employee_not_found_handler(
    _: Request,
    exc: EmployeeNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.message}},
    )

@registry.register(EmployeeAlreadyExistsError)
async def employee_already_exists_handler(
    _: Request,
    exc: EmployeeNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": {"message": exc.message}},
    )
