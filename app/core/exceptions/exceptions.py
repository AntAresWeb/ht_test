class AppExceptionError(Exception):
    message_template: str = "Произошла ошибка приложения."

    def __init__(self, message: str | None = None, **context) -> None:
        if message:
            super().__init__(message)
        else:
            self.context = context
            self.message = self.message_template.format(**self.context)
            super().__init__(self.message)


# Исключения для Department

class DepartmentNotFoundError(AppExceptionError):
    message_template = "Подразделение с id={id} не найдено."

    def __init__(self, id: int) -> None:
        context = {"id": id}
        super().__init__(**context)


class DepartmentNameConflictError(AppExceptionError):
    message_template = "Подразделение с таким именем name={name} уже существует у родителя."

    def __init__(self, name: str) -> None:
        context = {"name": name}
        super().__init__(**context)


class DepartmentCycleError(AppExceptionError):
    message_template = "Попытка переместить подразделение внутрь собственного поддерева (создание цикла)."


class InvalidParentError(AppExceptionError):
    message_template = "Попытка сделать родителем несуществующее подразделение с id={id}."

    def __init__(self, id: int) -> None:
        context = {"id": id}
        super().__init__(**context)


class DepartmentSelfParentError(AppExceptionError):
    message_template = "Попытка сделать родителем самого себя."


class DepartmentHasEmployeesError(AppExceptionError):
    message_template="Нельзя удалить подразделение, так как в нем есть сотрудники (без режима reassign)."

# Исключения для Employee

class EmployeeNotFoundError(AppExceptionError):
    message_template = "Сотрудник с id={id} не найден."

    def __init__(self, id: int) -> None:
        context = {"id": id}
        super().__init__(**context)


class EmployeeAlreadyExistsError(AppExceptionError):
    message_template="Сотрудник с именем '{name}' в подразделении уже есть."

    def __init__(self, name: str) -> None:
        context = {"name": name}
        super().__init__(**context)
