from typing import Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    ALLOWED_ORIGINS: Optional[str]
    ALLOWED_REST_METHODS: Optional[str]
    API_VERSION_PREFIX: str = "/v1"
    BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    @property
    def ALLOWED_ORIGINS_LIST(self) -> Optional[list]:
        if self.ALLOWED_ORIGINS:
            return self.ALLOWED_ORIGINS.split(",")

    @property
    def ALLOWED_REST_METHODS_LIST(self) -> Optional[list]:
        if self.ALLOWED_REST_METHODS:
            return self.ALLOWED_REST_METHODS.split(",")
        return ["*"]


settings = Settings()
