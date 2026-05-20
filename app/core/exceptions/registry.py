from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

ExceptionHandlerType = Callable[[Request, Exception], Awaitable[Response]]

class ExceptionRegistry:
    """
    Класс для группировки и регистрации обработчиков исключений.
    """
    def __init__(self) -> None:
        self._handlers = []

    def register(self, exception_class: type[Exception]) -> Callable:
        def decorator(func: ExceptionHandlerType) -> ExceptionHandlerType:
            self._handlers.append((exception_class, func))
            return func
        return decorator

    def register_all(self, app: FastAPI) -> None:
        """
        Регистрирует все накопленные обработчики в приложении FastAPI.
        """
        for exception_class, handler_func in self._handlers:
            app.add_exception_handler(exception_class, handler_func)
