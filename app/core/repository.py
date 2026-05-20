from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=object)


class BaseRepository(ABC, Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self.session: AsyncSession = session
        self._model: type[ModelType] = model


    async def add(self, entity: ModelType) -> None:
        self.session.add(entity)


    async def get_by_id(self, entity_id: int) -> ModelType | None:
        stmt = select(self._model).where(self._model.id == entity_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def delete(self, entity: ModelType) -> None:
        self.session.delete(entity)
