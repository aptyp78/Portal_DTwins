"""
Agent Operations
Определение операций и результатов агента
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class OperationStatus(Enum):
    """Статус выполнения операции"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    ROUTED = "routed"
    PENDING = "pending"


class OperationType(Enum):
    """Типы операций агента"""
    # Material Management
    GET_MATERIAL = "get_material"
    LIST_MATERIALS = "list_materials"
    UPDATE_MATERIAL = "update_material"
    ARCHIVE_MATERIAL = "archive_material"

    # Search
    SEARCH = "search"
    SEMANTIC_SEARCH = "semantic_search"
    KEYWORD_SEARCH = "keyword_search"

    # Traceability
    GET_SOURCE_CHAIN = "get_source_chain"
    GET_NODE_SOURCES = "get_node_sources"
    GET_NODE_EDGES = "get_node_edges"

    # Statistics
    GET_OVERVIEW = "get_overview"
    GET_STATISTICS = "get_statistics"

    # Routing
    ROUTE_TO_AGENT = "route_to_agent"

    # Validation
    VALIDATE_INTEGRITY = "validate_integrity"
    CHECK_TRACEABILITY = "check_traceability"


@dataclass
class AgentOperation:
    """Модель операции агента"""
    operation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: OperationType = OperationType.GET_MATERIAL
    params: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: OperationStatus = OperationStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None

    def complete(self, status: OperationStatus, result: Optional[Dict] = None, error: Optional[str] = None):
        """Завершение операции"""
        self.completed_at = datetime.now()
        self.status = status
        self.result = result
        self.error = error
        self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)

    def to_dict(self) -> Dict:
        """Сериализация в словарь"""
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "params": self.params,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms
        }


@dataclass
class OperationResult:
    """Результат операции агента"""
    status: OperationStatus
    operation: str
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def success(cls, operation: str, data: Any, **metadata) -> "OperationResult":
        """Создание успешного результата"""
        return cls(
            status=OperationStatus.SUCCESS,
            operation=operation,
            data=data,
            metadata=metadata
        )

    @classmethod
    def error(cls, operation: str, error: str, **metadata) -> "OperationResult":
        """Создание результата с ошибкой"""
        return cls(
            status=OperationStatus.ERROR,
            operation=operation,
            error=error,
            metadata=metadata
        )

    @classmethod
    def routed(cls, operation: str, target_agent: str, **metadata) -> "OperationResult":
        """Создание результата маршрутизации"""
        return cls(
            status=OperationStatus.ROUTED,
            operation=operation,
            data={"target_agent": target_agent},
            metadata=metadata
        )

    def to_dict(self) -> Dict:
        """Сериализация в словарь"""
        return {
            "status": self.status.value,
            "operation": self.operation,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


# Карта операций для быстрого доступа
OPERATION_MAP = {
    # Material operations
    "get": OperationType.GET_MATERIAL,
    "list": OperationType.LIST_MATERIALS,
    "update": OperationType.UPDATE_MATERIAL,
    "archive": OperationType.ARCHIVE_MATERIAL,

    # Search operations
    "search": OperationType.SEARCH,
    "find": OperationType.SEARCH,
    "semantic": OperationType.SEMANTIC_SEARCH,
    "keyword": OperationType.KEYWORD_SEARCH,

    # Traceability
    "trace": OperationType.GET_SOURCE_CHAIN,
    "sources": OperationType.GET_NODE_SOURCES,
    "edges": OperationType.GET_NODE_EDGES,

    # Stats
    "overview": OperationType.GET_OVERVIEW,
    "stats": OperationType.GET_STATISTICS,

    # Validation
    "validate": OperationType.VALIDATE_INTEGRITY,
    "check": OperationType.CHECK_TRACEABILITY,
}


def parse_operation(query: str) -> Optional[OperationType]:
    """
    Парсинг типа операции из запроса

    Args:
        query: Текстовый запрос

    Returns:
        Тип операции или None
    """
    query_lower = query.lower()
    for keyword, op_type in OPERATION_MAP.items():
        if keyword in query_lower:
            return op_type
    return None
