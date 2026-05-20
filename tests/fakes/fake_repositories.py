from app.departments.models import Department


class FakeDepartmentRepository:
    def __init__(self):
        self.departments = []
        self.next_id = 1
        self._storage = {}

    async def add(self, department: Department) -> None:
        department.id = self.next_id
        self.departments.append(department)
        self._storage[department.id] = department
        self.next_id += 1

    async def save(self) -> None:
        pass

    async def exists_by_name_and_parent(self, name, parent_id):
        return any(dep.name == name and dep.parent_id == parent_id for dep in self.departments)

    async def get_by_id(self, department_id: int) -> Department:
        if department_id not in self._storage:
            # Имитация поведения реального репозитория
            raise Exception("Not Found")
        return self._storage[department_id]
