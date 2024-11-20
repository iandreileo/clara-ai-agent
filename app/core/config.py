import os
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    API_VERSION_STR: str = os.getenv("API_VERSION_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Resume builder agent")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    DEBUG: bool = os.getenv("DEBUG", False)
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "A resume builder agent")
    PROJECT_AUTHOR: str = os.getenv("PROJECT_AUTHOR", "Ilie Andrei-Leonard")
    PROJECT_EMAIL: str = os.getenv("PROJECT_EMAIL", "andreileonard1801@yahoo.ro")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    PORT: int = os.getenv("PORT", 8000)
    HOST: str = os.getenv("HOST", "0.0.0.0")
    RESUME_API_BASE_URL: str = os.getenv("RESUME_API_BASE_URL", "")
    DB_URI: str = os.getenv("DB_URI", "")
    RESUME_SECTIONS: List[str] = os.getenv("RESUME_SECTIONS", ["personal_info", "work_experience", "education"])

    class Config:
        env_file = ".env"

settings = Settings()