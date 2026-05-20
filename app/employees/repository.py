from sqlalchemy import select, update

from app.core.repository import BaseRepository
from app.core.utils.introspection import get_indexed_columns
from app.employees.models import Employee


class EmployeeRepository(BaseRepository[Employee]):
    """
    Репозиторий для работы с сущностью Employee.
    Инкапсулирует логику доступа к данным, связанную с сотрудниками.
    """
    def __init__(self, session) -> None:
        super().__init__(session=session, model=Employee)


    async def list_by_department_id(
        self,
        department_id: int,
        sort_by: str = "full_name",
    ) -> list[Employee]:
        """
        Возвращает список сотрудников для заданного подразделения.
        """
        column_name = sort_by if sort_by in get_indexed_columns(self._model) else "full_name"
        order_column = getattr(self._model, column_name)

        stmt = (
            select(self._model)
            .where(self._model.department_id == department_id)
            .order_by(order_column)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_by_department_id_and_name(
        self,
        department_id: int,
        employee_name: str,
    ) -> Employee | None:
        """
        Находит сотрудника по его полному имени и идентификатору подразделения.
        Ищет запись в базе данных, где совпадают department_id и full_name.
        """
        stmt = (
            select(self._model)
            .where(
                self._model.department_id == department_id,
                self._model.full_name == employee_name,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def bulk_change_department(
        self,
        from_department_id: int,
        to_department_id: int,
    ) -> None:
        """
        Пакетно обновляет department_id для всех сотрудников указанного отдела.
        """
        stmt = (
            update(self._model)
            .where(self._model.department_id == from_department_id)
            .values(department_id=to_department_id)
            .execution_options(synchronize_session=False)
        )
        await self.session.execute(stmt)
