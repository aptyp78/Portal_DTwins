"""
Database operations for Portal_DTwins
Knowledge Gate Agent database interface
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from pgvector.psycopg2 import register_vector

from .config import db_config, DatabaseConfig

logger = logging.getLogger(__name__)


class MaterialCategory(Enum):
    """Категории материалов"""
    RAW_SOURCES = "RAW_SOURCES"
    ANALYTICAL_NODES = "ANALYTICAL_NODES"
    KNOWLEDGE_GRAPH = "KNOWLEDGE_GRAPH"
    SCHEMAS = "SCHEMAS"
    INDEXES = "INDEXES"
    DOCUMENTATION = "DOCUMENTATION"
    ARCHIVE = "ARCHIVE"
    GOLD = "GOLD"


class MaterialStatus(Enum):
    """Статусы материалов"""
    PRODUCTION = "production"
    IMMUTABLE = "immutable"
    DRAFT = "draft"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


@dataclass
class Material:
    """Модель материала"""
    material_id: str
    filename: str
    title: str
    category: MaterialCategory
    status: MaterialStatus
    file_path: str
    file_size_bytes: Optional[int] = None
    layer: Optional[str] = None
    metadata: Optional[Dict] = None
    tags: Optional[List[str]] = None
    version: str = "1.0.0"
    embedding: Optional[List[float]] = None


class DatabaseManager:
    """Менеджер базы данных Portal_DTwins"""

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or db_config
        self._connection = None

    def connect(self) -> psycopg2.extensions.connection:
        """Установка соединения с базой данных"""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
            )
            # Регистрируем pgvector типы
            register_vector(self._connection)
        return self._connection

    def close(self):
        """Закрытие соединения"""
        if self._connection and not self._connection.closed:
            self._connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ==========================================
    # MATERIAL OPERATIONS
    # ==========================================

    def get_material(self, material_id: str) -> Optional[Dict]:
        """Получение материала по ID"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT m.*, an.backlinks_count, an.outgoing_edges_count, an.source_ids
                FROM materials m
                LEFT JOIN analytical_nodes an ON m.id = an.id
                WHERE m.material_id = %s
            """, (material_id,))
            result = cur.fetchone()
            return dict(result) if result else None

    def list_materials(
        self,
        category: Optional[MaterialCategory] = None,
        status: Optional[MaterialStatus] = None,
        layer: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """Список материалов с фильтрацией"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            conditions = []
            params = []

            if category:
                conditions.append("category = %s")
                params.append(category.value)
            if status:
                conditions.append("status = %s")
                params.append(status.value)
            if layer:
                conditions.append("layer = %s")
                params.append(layer)

            where_clause = " AND ".join(conditions) if conditions else "1=1"

            cur.execute(f"""
                SELECT material_id, filename, title, category, status, layer,
                       file_size_bytes, version, created_at, updated_at
                FROM materials
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, params + [limit, offset])

            return [dict(row) for row in cur.fetchall()]

    def search_materials(
        self,
        query: str,
        category: Optional[MaterialCategory] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Полнотекстовый поиск материалов"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            params = [query, query]
            category_filter = ""
            if category:
                category_filter = "AND m.category = %s"
                params.append(category.value)

            cur.execute(f"""
                SELECT m.material_id, m.title, m.category, m.layer,
                       ts_rank(si.content_tsvector, plainto_tsquery('russian', %s)) as rank
                FROM materials m
                JOIN search_index si ON m.id = si.material_id
                WHERE si.content_tsvector @@ plainto_tsquery('russian', %s)
                {category_filter}
                ORDER BY rank DESC
                LIMIT %s
            """, params + [limit])

            return [dict(row) for row in cur.fetchall()]

    def semantic_search(
        self,
        embedding: List[float],
        category: Optional[MaterialCategory] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Семантический поиск по embedding"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            params = [embedding]
            category_filter = ""
            if category:
                category_filter = "AND category = %s"
                params.append(category.value)

            cur.execute(f"""
                SELECT material_id, title, category, layer,
                       1 - (embedding <=> %s::vector) as similarity
                FROM materials
                WHERE embedding IS NOT NULL
                {category_filter}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, params + [embedding, limit])

            return [dict(row) for row in cur.fetchall()]

    # ==========================================
    # TRACEABILITY OPERATIONS
    # ==========================================

    def get_source_chain(self, source_id: str) -> Dict:
        """Получение цепочки: Source -> Nodes -> Edges"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Информация об источнике
            cur.execute("""
                SELECT material_id, filename, title, file_size_bytes
                FROM materials WHERE material_id = %s
            """, (source_id,))
            source = cur.fetchone()

            if not source:
                return {"error": f"Source {source_id} not found"}

            # Связанные узлы
            cur.execute("""
                SELECT m.material_id, m.title, m.layer,
                       an.backlinks_count, an.outgoing_edges_count
                FROM source_node_mapping snm
                JOIN materials s ON snm.source_id = s.id
                JOIN materials m ON snm.node_id = m.id
                LEFT JOIN analytical_nodes an ON m.id = an.id
                WHERE s.material_id = %s
            """, (source_id,))
            nodes = [dict(row) for row in cur.fetchall()]

            return {
                "source": dict(source),
                "derived_nodes": nodes,
                "nodes_count": len(nodes),
                "total_backlinks": sum(n.get("backlinks_count", 0) for n in nodes)
            }

    def get_node_sources(self, node_id: str) -> List[Dict]:
        """Получение источников для узла"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT s.material_id, s.filename, s.title, snm.mapping_type, snm.confidence
                FROM source_node_mapping snm
                JOIN materials n ON snm.node_id = n.id
                JOIN materials s ON snm.source_id = s.id
                WHERE n.material_id = %s
            """, (node_id,))
            return [dict(row) for row in cur.fetchall()]

    # ==========================================
    # GRAPH OPERATIONS
    # ==========================================

    def get_node_edges(self, node_id: str, direction: str = "both") -> Dict:
        """Получение связей узла"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            result = {"incoming": [], "outgoing": []}

            if direction in ("both", "outgoing"):
                cur.execute("""
                    SELECT t.material_id as target_id, t.title as target_title,
                           me.edge_type, me.weight
                    FROM material_edges me
                    JOIN materials s ON me.source_material_id = s.id
                    JOIN materials t ON me.target_material_id = t.id
                    WHERE s.material_id = %s
                """, (node_id,))
                result["outgoing"] = [dict(row) for row in cur.fetchall()]

            if direction in ("both", "incoming"):
                cur.execute("""
                    SELECT s.material_id as source_id, s.title as source_title,
                           me.edge_type, me.weight
                    FROM material_edges me
                    JOIN materials s ON me.source_material_id = s.id
                    JOIN materials t ON me.target_material_id = t.id
                    WHERE t.material_id = %s
                """, (node_id,))
                result["incoming"] = [dict(row) for row in cur.fetchall()]

            return result

    def get_graph_overview(self) -> Dict:
        """Обзор Knowledge Graph"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Общая статистика
            cur.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE category = 'ANALYTICAL_NODES') as nodes_count,
                    (SELECT COUNT(*) FROM material_edges) as edges_count,
                    SUM(COALESCE((metadata->>'backlinks_count')::int, 0))
                        FILTER (WHERE category = 'ANALYTICAL_NODES') as total_backlinks
                FROM materials
            """)
            stats = dict(cur.fetchone())

            # По слоям
            cur.execute("""
                SELECT layer, COUNT(*) as count
                FROM materials
                WHERE category = 'ANALYTICAL_NODES' AND layer IS NOT NULL
                GROUP BY layer
            """)
            by_layer = {row["layer"]: row["count"] for row in cur.fetchall()}

            return {
                "nodes_count": stats["nodes_count"],
                "edges_count": stats["edges_count"],
                "total_backlinks": stats["total_backlinks"],
                "by_layer": by_layer
            }

    # ==========================================
    # STATISTICS
    # ==========================================

    def get_statistics(self) -> Dict:
        """Общая статистика базы"""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM v_category_stats
            """)
            by_category = {row["category"]: dict(row) for row in cur.fetchall()}

            cur.execute("""
                SELECT COUNT(*) as total FROM materials
            """)
            total = cur.fetchone()["total"]

            return {
                "total_materials": total,
                "by_category": by_category,
                "timestamp": datetime.now().isoformat()
            }

    # ==========================================
    # AGENT OPERATIONS LOG
    # ==========================================

    def log_operation(
        self,
        agent_id: str,
        operation: str,
        params: Dict,
        status: str,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        affected_materials: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ):
        """Логирование операции агента"""
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO agent_operations
                (agent_id, operation, params, status, result, error_message,
                 affected_materials, session_id, completed_at, duration_ms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(),
                        EXTRACT(EPOCH FROM (NOW() - started_at)) * 1000)
                RETURNING id
            """, (
                agent_id,
                operation,
                json.dumps(params),
                status,
                json.dumps(result) if result else None,
                error,
                affected_materials,
                session_id
            ))
            conn.commit()
            return cur.fetchone()[0]


# Глобальный экземпляр менеджера
db_manager = DatabaseManager()
