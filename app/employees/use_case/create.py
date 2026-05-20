from app.core.exceptions.exceptions import (
    DepartmentNotFoundError,
    EmployeeAlreadyExistsError,
)
from app.core.use_case import BaseUseCase
from app.employees.models import Employee


class CreateEmployeeForDepartmentUseCase(BaseUseCase):
    async def execute(
            self,
            department_id: int,
            full_name: str,
            position: str,
            hired_at=None,
    ) -> Employee:
        async with self._uow_factory() as uow:
            if await uow.departments.get_by_id(department_id) is None:
                raise DepartmentNotFoundError(id=department_id)

            if await uow.employees.get_by_departmentid_and_name(
                department_id=department_id,
                employee_name=full_name,
            ) is not None:
                raise EmployeeAlreadyExistsError(name=full_name)

            new_employee = Employee(
                full_name=full_name,
                position=position,
                hired_at=hired_at,
                department_id=department_id,
            )

            await uow.employees.add(new_employee)

        return new_employee
