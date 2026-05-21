from sqlalchemy import select, update
from sqlalchemy.sql.expression import literal

from app.core.repository import BaseRepository
from app.departments.models import Department


class DepartmentRepository(BaseRepository[Department]):
    """
    Репозиторий для работы с сущностью Department.
    Инкапсулирует логику доступа к данным, связанную с департаментами.
    """
    def __init__(self, session) -> None:
        super().__init__(session=session, model=Department)


    async def exists_by_name_and_parent(self, name: str, parent_id: int | None) -> bool:
        stmt = select(self._model.id).where(
            self._model.name == name,
            self._model.parent_id == parent_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar() is not None


    async def is_descendant_of(self, child_id: int, ancestor_id: int) -> bool:
        node_columns = select(self._model.id, self._model.parent_id)
        ancestors_cte = (
            node_columns
            .where(self._model.id == child_id)
            .cte(name="ancestors", recursive=True)
        )

        ancestors_union = ancestors_cte.union_all(
            node_columns
            .join_from(
                self._model,
                ancestors_cte,
                self._model.id == ancestors_cte.c.parent_id,
            ),
        )

        stmt = (
            select(ancestors_union.c.id)
            .where(ancestors_union.c.id == ancestor_id)
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None


    async def get_tree(self, root_id: int, depth: int) -> list[Department]:
        """
        Возвращает дерево подразделений с учетом глубины (depth).
        """
        descendants_cte = select(
            self._model.id,
            self._model.parent_id,
            literal(0).label("lvl"),
        ).where(self._model.id == root_id).cte(name="descendants", recursive=True)

        recursive_cte = select(
            self._model.id,
            self._model.parent_id,
            (descendants_cte.c.lvl + literal(1)).label("lvl"),
        ).join_from(
            self._model,
            descendants_cte,
            self._model.parent_id == descendants_cte.c.id,
        ).where(descendants_cte.c.lvl < depth)

        full_descendants_cte = descendants_cte.union_all(recursive_cte)

        # Получаем все ID: корень + все потомки до уровня depth
        stmt = (
            select(self._model)
            .where(self._model.id.in_(select(full_descendants_cte.c.id)))
            .order_by(self._model.id)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def bulk_reassign_children_parents(
        self,
        from_department_id: int,
        to_department_id: int,
    ) -> None:
        """
        Пакетно обновляет department_id для всех сотрудников указанного отдела.
        """
        stmt = (
            update(self._model)
            .where(self._model.parent_id == from_department_id)
            .values(parent_id=to_department_id)
            .execution_options(synchronize_session=False)
        )
        await self.session.execute(stmt)
