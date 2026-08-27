from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "TennisQServer"
    debug: bool = False
    db_name: str = "test.db"
    db_user: str = ""
    db_pass: str = ""

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///{self.db_name}"


config = Config()
