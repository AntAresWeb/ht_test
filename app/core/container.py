from typing import Annotated

from dependency_injector import containers, providers
from fastapi import Depends

from app.core.pg_connector import get_pg_connector
from app.core.unit_of_work import UnitOfWork
from app.departments.use_cases.create import CreateDepartmentUseCase
from app.departments.use_cases.delete import DeleteDepartmentUseCase
from app.departments.use_cases.get_with_tree import GetDepartmentDetailsUseCase
from app.departments.use_cases.move import MoveDepartmentUseCase
from app.employees.use_case.create import CreateEmployeeForDepartmentUseCase


class DependencyContainer(containers.DeclarativeContainer):
    """
    Контейнер, который собирает весь стек зависимостей,
    скрывая детали работы с БД от верхних слоев.
    """

    pg_connector = providers.Singleton(get_pg_connector)

    unit_of_work_factory = providers.Factory(
        UnitOfWork,
        session_factory=pg_connector.provided.db_session,
    )

    create_department_uc = providers.Factory(
        CreateDepartmentUseCase,
        uow_factory=unit_of_work_factory.provider,
    )

    move_department_uc = providers.Factory(
        MoveDepartmentUseCase,
        uow_factory=unit_of_work_factory,
    )

    get_department_uc = providers.Factory(
        GetDepartmentDetailsUseCase,
        uow_factory=unit_of_work_factory,
    )

    delete_department_uc = providers.Factory(
        DeleteDepartmentUseCase,
        uow_factory=unit_of_work_factory,
    )

    create_employee_uc = providers.Factory(
        CreateEmployeeForDepartmentUseCase,
        uow_factory=unit_of_work_factory,
    )


def get_dependency_container() -> DependencyContainer:
    return DependencyContainer()


# резолверы юзкейсов
def get_department_ucr(
    container: Annotated[DependencyContainer, Depends(get_dependency_container)],
) -> GetDepartmentDetailsUseCase:
    return container.get_department_uc()


def create_department_ucr(
    container: Annotated[DependencyContainer, Depends(get_dependency_container)],
) -> CreateDepartmentUseCase:
    return container.create_department_uc()


def delete_department_ucr(
    container: Annotated[DependencyContainer, Depends(get_dependency_container)],
) -> DeleteDepartmentUseCase:
    return container.delete_department_uc()


def move_department_ucr(
    container: Annotated[DependencyContainer, Depends(get_dependency_container)],
) -> MoveDepartmentUseCase:
    return container.move_department_uc()


def create_employee_ucr(
    container: Annotated[DependencyContainer, Depends(get_dependency_container)],
) -> CreateEmployeeForDepartmentUseCase:
    return container.create_employee_uc()
