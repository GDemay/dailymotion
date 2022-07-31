""" This is the config class for the application. """
import secrets
import os
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv


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

    # This is not secure at all but I set it here for the sake of simplicity
    # In order to avoid you to have to set it in your environment variable
    # I would normaly recommand to use a more secure method like
    # like

    load_dotenv(find_dotenv())
    MAILJET_API_KEY: str = os.environ.get("MAILJET_API_KEY")
    MAILJET_API_SECRET: str = os.environ.get("MAILJET_API_SECRET")
    MAILJET_FROM_EMAIL: str = "guillaumedemay@hotmail.fr"


# Load the environment variables from the .env file

settings = Settings()
