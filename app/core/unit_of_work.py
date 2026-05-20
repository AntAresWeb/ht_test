from contextlib import AbstractAsyncContextManager
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.departments.repository import DepartmentRepository
from app.employees.repository import EmployeeRepository


class UnitOfWork(AbstractAsyncContextManager):
    """
    Паттерн Unit of Work.
    Координирует работу с базой данных в рамках одной бизнес-транзакции.
    Предоставляет доступ к репозиториям, работающим с одной и той же сессией.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        """
        Инициализация UnitOfWork.
        Args:
            session_factory: Фабрика для создания асинхронных сессий SQLAlchemy.
        """
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.departments: DepartmentRepository | None = None
        self.employees: EmployeeRepository | None = None

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        await self.session.begin()

        self.departments = DepartmentRepository(self.session)
        self.employees = EmployeeRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()

        await self.session.close()

    def __call__(self) -> Self:
        return self
