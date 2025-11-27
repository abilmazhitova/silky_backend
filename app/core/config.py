from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_1688_URL: str = "https://tstbnd.silkyway.kz/api"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:test1234@localhost/silky"
    BACKEND_URL: str = ""
settings = Settings()
