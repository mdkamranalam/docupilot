from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "DocuPilot"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = "docupilot"
    POSTGRES_PASSWORD: str = "docupilot_password"
    POSTGRES_DB: str = "docupilot_db"

    LLM_PROVIDER: str = "groq"  # "groq" or "openai"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "openai/gpt-oss-120b"
    
    EMBEDDING_PROVIDER: str = "fastembed"  # "fastembed" (free local) or "openai"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
