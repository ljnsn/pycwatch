from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    CW_API_KEY: Optional[str] = None


settings = Settings()
