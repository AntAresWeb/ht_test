from app.core.exceptions.exceptions import DepartmentNotFoundError, DepartmentReassignError
from app.core.use_case import BaseUseCase


class DeleteDepartmentUseCase(BaseUseCase):
    """
    Сценарий (Use Case) для удаления департамента.
    Поддерживает два режима: каскадное удаление и перенос сотрудников.
    """

    async def execute(
        self,
        department_id: int,
        mode: str,
        reassign_to_id: int | None = None,
    ) -> None:
        async with self._uow_factory() as uow:
            department = await uow.departments.get_by_id(department_id)
            if not department:
                raise DepartmentNotFoundError(id=department_id)

            match mode:
                case "cascade":
                    # Логика каскадного удаления
                    await uow.session.delete(department)

                case "reassign":
                    if reassign_to_id is None:
                        raise ValueError("Параметр reassign_to_department_id обязателен.")

                    if reassign_to_id == department_id:
                        raise DepartmentReassignError()

                    if await uow.departments.get_by_id(reassign_to_id) is None:
                        raise DepartmentNotFoundError(id=reassign_to_id)

                    await uow.employees.bulk_change_department(
                        from_department_id=department_id,
                        to_department_id=reassign_to_id,
                    )

                    new_parent_id = department.parent_id
                    await uow.departments.bulk_reassign_children_parents(
                        from_department_id=department_id,
                        to_department_id=new_parent_id,
                    )

                    await uow.session.delete(department)

                case _:
                    raise ValueError(f"Неизвестный режим удаления: {mode}")
