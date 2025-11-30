"""
Portal_DTwins Database Module
PostgreSQL + pgvector for knowledge management
"""

from .config import DatabaseConfig, EmbeddingConfig, db_config, embedding_config
from .operations import (
    DatabaseManager,
    Material,
    MaterialCategory,
    MaterialStatus,
    db_manager,
)

__all__ = [
    "DatabaseConfig",
    "EmbeddingConfig",
    "db_config",
    "embedding_config",
    "DatabaseManager",
    "Material",
    "MaterialCategory",
    "MaterialStatus",
    "db_manager",
]

__version__ = "1.0.0"
