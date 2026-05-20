from sqlalchemy import inspect


def get_indexed_columns(model) -> list[str]:
    """
    Извлекает имена колонок из __table_args__, где заданы индексы (Index).
    Этот метод не использует инспекцию сессии и работает с определением класса.
    """
    indexed_columns = set()

    mapper = inspect(model)
    table = mapper.local_table
    for index in table.indexes:
        for column in index.columns:
            indexed_columns.add(column.name)

    return list(indexed_columns)
