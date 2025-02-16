from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    DB_TYPE: str
    DB_NAME: str

    JWT_SECRET_KEY: str

    BASE_URL: str
    RESET_TOKEN_EXPIRE_MINUTES: int
    EMAIL_TOKEN_EXPIRE_MINUTES: int

    SENDGRID_SENDER: str
    SENDGRID_API_KEY: str

    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"


app_settings = Settings()
