import secrets

from pydantic import (AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn,
                      validator)


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    ACCESS_TOKEN_EXPIRE_MINUTE_CODE_VALIDATION: int = 1  # 1 minute
    ALGORITHM = "HS256"
    API_VERSION: str = "/api/v1"


settings = Settings()
