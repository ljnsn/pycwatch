"""Module holding configuration."""

import os
from typing import Optional

import attrs


@attrs.define()
class Settings:
    """Settings for the client."""

    CW_API_KEY: Optional[str] = None

    def __attrs_post_init__(self) -> None:
        """Post init hook."""
        if self.CW_API_KEY is None:
            self.CW_API_KEY = os.getenv("CW_API_KEY")


settings = Settings()
