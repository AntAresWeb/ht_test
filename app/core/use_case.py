from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from app.core.unit_of_work import UnitOfWork


class BaseUseCase(ABC):
    def __init__(self, uow_factory: Callable[..., UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:  # noqa: ANN401
        ...
