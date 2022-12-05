"""Module holding configuration."""
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for the client."""

    CW_API_KEY: Optional[str] = None


settings = Settings()
