from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Cancer Care API"
    DEBUG: bool = True

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 24

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    FRONTEND_URL: str

    CORS_ORIGINS: str = "http://localhost:4200"

    class Config:
        env_file = ".env"

settings = Settings()
