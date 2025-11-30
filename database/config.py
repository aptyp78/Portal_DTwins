"""
Конфигурация базы данных Portal_DTwins
PostgreSQL + pgvector
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Конфигурация подключения к PostgreSQL"""
    host: str = "localhost"
    port: int = 5432
    database: str = "portal_dtwins"
    user: str = "postgres"
    password: str = ""

    # pgvector settings
    vector_dimensions: int = 1536  # OpenAI ada-002

    # Connection pool
    min_connections: int = 1
    max_connections: int = 10

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Загрузка конфигурации из переменных окружения"""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "portal_dtwins"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            vector_dimensions=int(os.getenv("VECTOR_DIMENSIONS", "1536")),
        )

    @property
    def connection_string(self) -> str:
        """PostgreSQL connection string"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def async_connection_string(self) -> str:
        """Async PostgreSQL connection string (asyncpg)"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class EmbeddingConfig:
    """Конфигурация для генерации embeddings"""
    provider: str = "openai"  # openai, local, sentence-transformers
    model: str = "text-embedding-ada-002"
    dimensions: int = 1536
    batch_size: int = 100

    # API settings
    api_key: Optional[str] = None
    api_base: Optional[str] = None

    @classmethod
    def from_env(cls) -> "EmbeddingConfig":
        """Загрузка из переменных окружения"""
        return cls(
            provider=os.getenv("EMBEDDING_PROVIDER", "openai"),
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
            dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "1536")),
            api_key=os.getenv("OPENAI_API_KEY"),
        )


# Глобальные экземпляры конфигурации
db_config = DatabaseConfig.from_env()
embedding_config = EmbeddingConfig.from_env()
