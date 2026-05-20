from app.core.exceptions.exceptions import DepartmentNameConflictError, InvalidParentError
from app.core.use_case import BaseUseCase
from app.departments.models import Department


class CreateDepartmentUseCase(BaseUseCase):
    """
    Сценарий (Use Case) для создания нового департамента.
    Управляет транзакцией через UnitOfWork.
    """

    async def execute(self, name: str, parent_id: int | None = None) -> Department:
        """
        Создает новый департамент с проверкой бизнес-правил.
        Args:
            name: Название департамента.
            parent_id: ID родительского департамента.
        Returns:
            Созданный объект Department.
        Raises:
            DepartmentNameConflictError: Если департамент с таким именем уже существует у родителя.
            InvalidParentError: Если родительский департамент не найден.
        """
        async with self._uow_factory() as uow:
            if await uow.departments.exists_by_name_and_parent(name=name, parent_id=parent_id):
                raise DepartmentNameConflictError(name=name)

            if parent_id is not None and await uow.departments.get_by_id(parent_id) is None:
                raise InvalidParentError(id=parent_id)

            new_department = Department(name=name, parent_id=parent_id)
            await uow.departments.add(new_department)
        return new_department
