import pytest

from app.core.exception.exceptions import DepartmentNameConflict
from app.departments.use_cases.create import CreateDepartmentUseCase


class FakeDepartmentRepository:
    def __init__(self) -> None:
        self.departments = []
        self.exists_data = {}

    async def exists_by_name_and_parent(self, name, parent_id):
        return self.exists_data.get((name, parent_id), False)

    async def add(self, department):
        self.departments.append(department)

    async def save(self):
        pass

    async def get_by_id(self, id_department: int):
        # Простая реализация для теста родителя
        for dep in self.departments:
            if dep.id == id_department:
                return dep
        raise ValueError("Не найден")


async def test_create_department_success() -> None:
    fake_repo = FakeDepartmentRepository()
    use_case = CreateDepartmentUseCase(fake_repo)

    new_dept = await use_case.execute(name="IT", parent_id=None)

    assert new_dept.name == "IT"
    assert len(fake_repo.departments) == 1
    assert fake_repo.departments[0].name == "IT"


async def test_create_department_name_conflict() -> None:
    fake_repo = FakeDepartmentRepository()
    fake_repo.exists_data[("IT", None)] = True

    use_case = CreateDepartmentUseCase(fake_repo)

    with pytest.raises(DepartmentNameConflict):
        await use_case.execute(name="IT", parent_id=None)
