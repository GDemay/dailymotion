""" This is the config class for the application. """
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    """_summary_ : This is the settings class for the application.

    Args:
        BaseSettings (_type_): _description_ - The base settings class.
    """

    SECRET_KEY: str = secrets.token_urlsafe(
        32
    )  # This is the secret key for decoding the JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # Bearer token expires in 7 days
    ACCESS_TOKEN_EXPIRE_MINUTE_CODE_VALIDATION: int = (
        1  # Code for email validation expires in 1 minute
    )
    ALGORITHM = "HS256"  # This is the algorithm for the JWT
    API_VERSION: str = "/api/v1"  # This is the version of the API


settings = Settings()
