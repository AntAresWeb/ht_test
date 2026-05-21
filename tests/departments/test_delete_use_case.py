import pytest
from unittest.mock import AsyncMock, MagicMock

# Импортируем UseCase и исключение
from app.departments.use_cases.delete import DeleteDepartmentUseCase
from app.core.exceptions.exceptions import DepartmentNotFoundError

@pytest.mark.asyncio
async def test_delete_nonexistent_department_raises_error():
    """
    Проверяет, что UseCase корректно обрабатывает удаление несуществующего отдела.
    """
    # --- 1. Настройка Mock-объектов (Фабрика и UoW) ---

    # Создаем Mock для самого UnitOfWork (того, что войдет в 'async with')
    # Используем AsyncMock, чтобы у него были __aenter__ и __aexit__
    mock_uow_instance = AsyncMock()
    
    # Создаем Mock для фабрики, которая возвращает UoW
    mock_uow_factory = AsyncMock()

    # --- 2. Ключевая настройка (ИСПРАВЛЕНО) ---
    # Мы настраиваем результат ВЫЗОВА фабрики.
    # Когда код дойдет до await self._uow_factory(), он должен получить mock_uow_instance.
    mock_uow_factory.return_value = mock_uow_instance 

    # --- 3. Настройка репозитория внутри UoW ---
    # Настраиваем метод get_by_id так, чтобы он возвращал None (отдел не найден)
    # .configure_mock - удобный способ задать атрибуты вложенных мок-объектов
    mock_uow_instance.configure_mock(
        **{
            'departments.get_by_id.return_value': None,
            'session.delete': AsyncMock() # Мокаем метод delete, чтобы проверить его вызов
        }
    )

    # --- 4. Создание UseCase и выполнение ---
    use_case = DeleteDepartmentUseCase(uow_factory=mock_uow_factory)

    # Используем pytest для проверки, что исключение было вызвано
    with pytest.raises(DepartmentNotFoundError) as exc_info:
        await use_case.execute(
            department_id=999,
            mode="cascade"
        )
    
    # Проверяем текст исключения
    assert "999" in str(exc_info.value)

    # --- 5. Проверка того, что методы были вызваны ---

    # Проверяем, что фабрика была вызвана один раз
    mock_uow_factory.assert_awaited_once()

    # Проверяем, что метод get_by_id был вызван с нужным ID
    mock_uow_instance.departments.get_by_id.assert_awaited_once_with(999)

    # Проверяем, что метод delete НЕ был вызван (так как отдела нет)
    mock_uow_instance.session.delete.assert_not_called()