from app.core.exceptions.exceptions import (
    DepartmentCycleError,
    DepartmentNameConflictError,
    DepartmentNotFoundError,
    DepartmentSelfParentError,
    InvalidParentError,
)
from app.core.use_case import BaseUseCase
from app.departments.models import Department


class MoveDepartmentUseCase(BaseUseCase):
    """
    Use Case для перемещения департамента.
    """
    async def execute(
        self,
        department_id: int,
        new_parent_id: int | None = None,
        new_name: int | None = None,
    ) -> Department:
        async with self._uow_factory() as uow:
            if department_id == new_parent_id:
                raise DepartmentSelfParentError()

            department = await uow.departments.get_by_id(department_id)
            if department is None:
                raise DepartmentNotFoundError(id=department_id)

            new_values = {}
            if new_name is not None:
                if await uow.departments.exists_by_name_and_parent(parent_id=new_parent_id, name=new_name):
                    raise DepartmentNameConflictError(name=new_name)
                new_values["name"] = new_name

            if new_parent_id is not None:
                parent = await uow.departments.get_by_id(new_parent_id)
                if parent is None:
                    raise InvalidParentError(id=new_parent_id)

                is_descendant = await uow.departments.is_descendant_of(
                    child_id=new_parent_id,
                    ancestor_id=department.id,
                )
                if is_descendant:
                    raise DepartmentCycleError()

                new_values["parent_id"] = new_parent_id

            for k, v in new_values.items():
                setattr(department, k, v)
        return department
