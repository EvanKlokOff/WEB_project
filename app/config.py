from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class Config(BaseSettings):
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_USER_NAME: str
    DB_DRIVER_NAME: str

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER_NAME,
            username=self.DB_USER_NAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            database=self.DB_NAME,
            port=self.DB_PORT
        )

    @property
    def db_url_alembic(self) -> str:
        return f"{self.DB_DRIVER_NAME}://{self.DB_USER_NAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="./env.env")


Config = Config()
