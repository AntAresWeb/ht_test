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
        reassign_to_department_id: int | None = None,
    ) -> None:
        async with self._uow_factory() as uow:
            department = await uow.departments.get_by_id(department_id)

            if mode == "reassign":
                if reassign_to_department_id is None:
                    raise ValueError("В режиме 'reassign' обязателен параметр reassign_to_department_id.")
                await uow.departments.get_by_id(reassign_to_department_id)

            if mode == "cascade":
                await uow.departments.delete(department)
            elif mode == "reassign":
                await uow.employees.bulk_change_department(
                    from_department_id=department_id,
                    to_department_id=reassign_to_department_id,
                )
                await uow.departments.delete(department)
            else:
                raise ValueError(f"Неизвестный режим удаления: {mode}. Используйте 'cascade' или 'reassign'.")
