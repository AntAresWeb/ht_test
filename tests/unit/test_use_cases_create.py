import pytest

from app.departments.use_cases.create import CreateDepartmentUseCase
from tests.fakes.fake_repositories import FakeDepartmentRepository


# Теперь редактор знает тип фикстуры!
@pytest.fixture
def use_case() -> CreateDepartmentUseCase:
    fake_repo = FakeDepartmentRepository()

    class FakeUnitOfWork:
        def __init__(self):
            self.departments = fake_repo

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

    return CreateDepartmentUseCase(lambda: FakeUnitOfWork())


@pytest.mark.asyncio
async def test_create_department_success(use_case):
    result = await use_case.execute(name="IT", parent_id=None)
    assert result.name == "IT"
