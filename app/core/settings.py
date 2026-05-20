from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


class PostgresSettings(BaseEnvSettings):
    postgres_db: str = "foobar"
    postgres_user: str = "user"
    postgres_password: SecretStr
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}"
            f":{self.postgres_password.get_secret_value()}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )


class AppSettings(BaseEnvSettings):
    app_title: str = ""
    app_description: str = ""


def get_app_settings() -> AppSettings:
    return AppSettings()


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
