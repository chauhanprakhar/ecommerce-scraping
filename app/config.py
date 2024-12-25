from pydantic import BaseSettings, HttpUrl

class Settings(BaseSettings):
    AUTH_TOKEN: str = "your-secret-token"
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5
    REDIS_URL: str = "redis://localhost:6379"
    DEFAULT_TARGET_URL: HttpUrl = "https://dentalstall.com/shop/"  # Default URL
    
    class Config:
        env_file = ".env"

settings = Settings()
