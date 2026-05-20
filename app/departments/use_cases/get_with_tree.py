from app.core.exceptions.exceptions import DepartmentNotFoundError
from app.core.use_case import BaseUseCase


class GetDepartmentDetailsUseCase(BaseUseCase):
    """
    Сценарий для управляемого получения департамента.
    Использует репозиторий с умной загрузкой данных.
    """
    async def execute(
        self,
        department_id: int,
        depth: int = 1,
        include_employees: bool = True,
    ) -> dict:
        async with self._uow_factory() as uow:
            if await uow.departments.get_by_id(department_id) is None:
                raise DepartmentNotFoundError(department_id)

            departments = (
                await uow.departments
                .get_tree(
                root_id=department_id,
                depth=depth,
                )
            )

            employees = (
                await uow.employees
                .list_by_department_id(department_id) if include_employees else []
            )

        root_dept = next((dept for dept in departments if dept.id == department_id), None)
        return {
            "department": root_dept,
            "employees": employees,
            "children": [dept for dept in departments if dept.id != department_id],
        }
