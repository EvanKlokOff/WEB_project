from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

path_to_template = Path().cwd().parent / "templates"/"emails"
path_to_env_file = Path().cwd().parent.parent / "venv_files" / "email.env"
path_to_template.mkdir(parents=True, exist_ok=True)

class Config(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(env_file=path_to_env_file)

conf = Config()

if __name__ == "__main__":
    pass