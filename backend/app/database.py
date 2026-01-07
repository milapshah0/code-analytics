from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PGHOST: str = os.getenv("PGHOST", "localhost")
    PGUSER: str = os.getenv("PGUSER", "postgres")
    PGPORT: str = os.getenv("PGPORT", "5432")
    PGPASSWORD: str = os.getenv("PGPASSWORD", "postgres")
    PGDATABASE: str = os.getenv("PGDATABASE", "analytics")

    @property
    def default_database_url(self) -> str:
        # Construct asyncpg URL
        return f"postgresql+asyncpg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    GITLAB_GROUP_ID: int = int(os.getenv("GITLAB_GROUP_ID", "59715498"))

    def get_db_url(self) -> str:
        return self.DATABASE_URL or self.default_database_url

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_async_engine(settings.get_db_url(), echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
