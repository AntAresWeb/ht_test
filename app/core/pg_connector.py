from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import get_postgres_settings


class PGConnector:
    """
    Управляет подключением к PostgreSQL.
    Создает движок (engine) и фабрику сессий (sessionmaker) один раз при запуске.
    """

    def __init__(self) -> None:
        postgres_settings = get_postgres_settings()
        self._engine = create_async_engine(postgres_settings.database_url)
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory


def get_pg_connector() -> PGConnector:
    return PGConnector()
