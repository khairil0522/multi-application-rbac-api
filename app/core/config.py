#perjanjian antara code & environment
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #app
    ENABLE_APPLICATION_ADMIN: bool = False

    #database
    DATABASE_URL: str
    DB_DIALECT: str | None = None
    
    #security / JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # === Redis ===
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # <- ini opsional tapi recommended
    )

settings = Settings()
