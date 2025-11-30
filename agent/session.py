"""
Agent Session Management
Управление сессиями агента
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
import json
from pathlib import Path


@dataclass
class QueryRecord:
    """Запись запроса в истории"""
    query: str
    response: Dict
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: Optional[int] = None

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "response_status": self.response.get("status"),
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms
        }


@dataclass
class AgentSession:
    """Сессия агента для отслеживания контекста"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = "AGENT-KNOWLEDGE-GATE"
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None

    # Контекст работы
    materials_accessed: List[str] = field(default_factory=list)
    operations_performed: List[str] = field(default_factory=list)
    current_focus: Optional[str] = None

    # История запросов
    query_history: List[QueryRecord] = field(default_factory=list)

    # Кэш для быстрого доступа
    cache: Dict[str, Any] = field(default_factory=dict)

    # Статус
    is_active: bool = True

    def add_query(self, query: str, response: Dict, duration_ms: Optional[int] = None):
        """Добавление запроса в историю"""
        record = QueryRecord(
            query=query,
            response=response,
            duration_ms=duration_ms
        )
        self.query_history.append(record)

    def access_material(self, material_id: str):
        """Отметка доступа к материалу"""
        if material_id not in self.materials_accessed:
            self.materials_accessed.append(material_id)
        self.current_focus = material_id

    def perform_operation(self, operation: str):
        """Отметка выполненной операции"""
        self.operations_performed.append(operation)

    def set_cache(self, key: str, value: Any, ttl_seconds: int = 300):
        """Установка значения в кэш"""
        self.cache[key] = {
            "value": value,
            "expires_at": datetime.now().timestamp() + ttl_seconds
        }

    def get_cache(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        if key in self.cache:
            entry = self.cache[key]
            if entry["expires_at"] > datetime.now().timestamp():
                return entry["value"]
            else:
                del self.cache[key]
        return None

    def end_session(self):
        """Завершение сессии"""
        self.ended_at = datetime.now()
        self.is_active = False

    def get_duration(self) -> Optional[float]:
        """Длительность сессии в секундах"""
        end = self.ended_at or datetime.now()
        return (end - self.started_at).total_seconds()

    def get_summary(self) -> Dict:
        """Сводка по сессии"""
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_seconds": self.get_duration(),
            "is_active": self.is_active,
            "materials_accessed_count": len(self.materials_accessed),
            "operations_count": len(self.operations_performed),
            "queries_count": len(self.query_history),
            "current_focus": self.current_focus
        }

    def to_dict(self) -> Dict:
        """Полная сериализация сессии"""
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "is_active": self.is_active,
            "materials_accessed": self.materials_accessed,
            "operations_performed": self.operations_performed,
            "current_focus": self.current_focus,
            "query_history": [q.to_dict() for q in self.query_history]
        }

    def save(self, path: Optional[Path] = None):
        """Сохранение сессии в файл"""
        if path is None:
            path = Path(f"sessions/session_{self.session_id}.json")

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Path) -> "AgentSession":
        """Загрузка сессии из файла"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        session = cls(
            session_id=data["session_id"],
            agent_id=data["agent_id"],
            started_at=datetime.fromisoformat(data["started_at"]),
            materials_accessed=data["materials_accessed"],
            operations_performed=data["operations_performed"],
            current_focus=data.get("current_focus"),
            is_active=data["is_active"]
        )

        if data.get("ended_at"):
            session.ended_at = datetime.fromisoformat(data["ended_at"])

        return session


class SessionManager:
    """Менеджер сессий агента"""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("sessions")
        self.active_sessions: Dict[str, AgentSession] = {}

    def create_session(self, agent_id: str = "AGENT-KNOWLEDGE-GATE") -> AgentSession:
        """Создание новой сессии"""
        session = AgentSession(agent_id=agent_id)
        self.active_sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """Получение сессии по ID"""
        return self.active_sessions.get(session_id)

    def end_session(self, session_id: str, save: bool = True) -> Optional[AgentSession]:
        """Завершение сессии"""
        session = self.active_sessions.pop(session_id, None)
        if session:
            session.end_session()
            if save:
                session.save(self.storage_path / f"session_{session_id}.json")
        return session

    def list_active_sessions(self) -> List[Dict]:
        """Список активных сессий"""
        return [s.get_summary() for s in self.active_sessions.values()]

    def cleanup_inactive(self, max_idle_seconds: int = 3600):
        """Очистка неактивных сессий"""
        now = datetime.now()
        to_remove = []

        for session_id, session in self.active_sessions.items():
            if session.query_history:
                last_activity = session.query_history[-1].timestamp
            else:
                last_activity = session.started_at

            if (now - last_activity).total_seconds() > max_idle_seconds:
                to_remove.append(session_id)

        for session_id in to_remove:
            self.end_session(session_id, save=True)

        return len(to_remove)
