from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str

    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    echo: bool

    secret_key: str
    salt: str

    backend_host: str
    frontend_host: str

    model_config = SettingsConfigDict(env_file=".docker-env")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"



settings = Settings()
