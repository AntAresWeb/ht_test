from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.employees.schemas import EmployeeResponse


class DepartmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DepartmentModel(DepartmentBase):
    name: str = Field(..., min_length=1, max_length=200)
    parent_id: int | None = Field(None, ge=1)

    @field_validator("name")
    @classmethod
    def trim_name(cls, value: str | None) -> str | None:
        return value.strip() if value is not None else None


# Модель для создания
class DepartmentCreate(DepartmentModel): ...


# Модель для обновления
class DepartmentUpdate(DepartmentModel):
    name: str | None = Field(None, min_length=1, max_length=200)


# Модели для ответов
class DepartmentResponseBase(DepartmentBase):
    id: int
    name: str
    parent_id: int | None


class DepartmentResponse(DepartmentBase):
    department: DepartmentResponseBase
    employees: list[EmployeeResponse] | None
    children: list[DepartmentResponseBase] | None


# Модели для параметров запросов
class DepartmentDeleteQuery(BaseModel):
    mode: Literal["cascade", "reassign"] = "cascade"
    reassign_to_department_id: int | None = None


class DepartmentRequestQuery(BaseModel):
    depth: int = Field(ge=1, le=5, default=1)
    include_employees: bool = True
