from os.path import isfile
from pathlib import Path
from pydantic_settings import BaseSettings

base_dir = Path(__file__).parent.absolute()


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    path_to_folders: str
    file_process_interval: int = 3 * 60

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}"

    class Config:
        config_file_name = f"{base_dir}/.env"
        if isfile(config_file_name):
            env_file = config_file_name
