import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Moodle Alt Text API"
    ALGORITHM: str = "HS256"
    API_KEY: str = os.getenv("API_KEY", "your-default-api-key")
    BLIP_MODEL_PATH: str = os.getenv("BLIP_MODEL_PATH", os.path.expanduser("~/.cache/huggingface/blip-base"))

settings = Settings()