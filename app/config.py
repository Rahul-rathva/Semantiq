from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://semantiq:semantiq@localhost:5432/semantiq"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev-secret-key"
    access_token_expire_minutes: int = 60
    embedding_model: str = "all-MiniLM-L6-v2"
    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
