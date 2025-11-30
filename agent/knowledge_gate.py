"""
Knowledge Gate Agent
Центральный агент управления базой знаний Portal_DTwins

Функции:
- Управление материалами (CRUD)
- Поиск и навигация по знаниям
- Трассировка source → node
- Маршрутизация к downstream агентам
- Логирование операций
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid

from database.operations import DatabaseManager, MaterialCategory, MaterialStatus

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Состояния агента"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class AgentContext:
    """Контекст текущей сессии агента"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = field(default_factory=datetime.now)
    materials_accessed: List[str] = field(default_factory=list)
    operations_performed: List[str] = field(default_factory=list)
    current_focus: Optional[str] = None
    query_history: List[Dict] = field(default_factory=list)


class KnowledgeGateAgent:
    """
    Knowledge Gate Agent — первый на входе в систему знаний.

    Capabilities:
    - material_management: индексация, получение, обновление материалов
    - search: полнотекстовый и семантический поиск
    - traceability: отслеживание связей source → node
    - routing: маршрутизация к специализированным агентам
    - validation: проверка целостности данных
    """

    AGENT_ID = "AGENT-KNOWLEDGE-GATE"
    AGENT_NAME = "Knowledge Gate Agent"
    AGENT_VERSION = "1.0.0"

    # Паттерны маршрутизации
    ROUTING_PATTERNS = {
        "analyze_": "analytical_agent",
        "graph_": "graph_agent",
        "edge_": "graph_agent",
        "source_": "source_agent",
        "raw_": "source_agent",
        "visualize_": "visualization_agent",
        "render_": "visualization_agent",
        "diagram_": "visualization_agent",
    }

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Инициализация агента

        Args:
            db_manager: Менеджер базы данных (если не передан, создаётся новый)
        """
        self.db = db_manager or DatabaseManager()
        self.state = AgentState.IDLE
        self.context = AgentContext()
        self._load_knowledge_index()

        logger.info(f"[{self.AGENT_ID}] Агент инициализирован, сессия: {self.context.session_id}")

    def _load_knowledge_index(self):
        """Загрузка индекса знаний из Gold JSON"""
        try:
            gold_index_path = Path(__file__).parent.parent / "data" / "gold" / "gold_index.json"
            if gold_index_path.exists():
                with open(gold_index_path, 'r', encoding='utf-8') as f:
                    self._gold_index = json.load(f)
                logger.info(f"[{self.AGENT_ID}] Gold Index загружен: {self._gold_index.get('quick_stats', {})}")
            else:
                self._gold_index = {}
                logger.warning(f"[{self.AGENT_ID}] Gold Index не найден")
        except Exception as e:
            self._gold_index = {}
            logger.error(f"[{self.AGENT_ID}] Ошибка загрузки Gold Index: {e}")

    # ==========================================
    # ОСНОВНЫЕ ОПЕРАЦИИ
    # ==========================================

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Обработка запроса пользователя

        Args:
            query: Текстовый запрос

        Returns:
            Результат обработки с данными или маршрутизацией
        """
        self.state = AgentState.PROCESSING
        self.context.query_history.append({
            "query": query,
            "timestamp": datetime.now().isoformat()
        })

        try:
            # Определяем тип запроса
            query_lower = query.lower()

            # Проверяем маршрутизацию к другим агентам
            for pattern, agent in self.ROUTING_PATTERNS.items():
                if pattern in query_lower:
                    return self._route_to_agent(agent, query)

            # Обрабатываем локально
            if any(kw in query_lower for kw in ["найди", "поиск", "search", "find"]):
                return self._handle_search(query)
            elif any(kw in query_lower for kw in ["покажи", "получи", "get", "show"]):
                return self._handle_get(query)
            elif any(kw in query_lower for kw in ["список", "list", "все"]):
                return self._handle_list(query)
            elif any(kw in query_lower for kw in ["статистика", "stats", "overview"]):
                return self._handle_stats()
            elif any(kw in query_lower for kw in ["связи", "трассировка", "trace", "source"]):
                return self._handle_traceability(query)
            else:
                # Умный поиск по умолчанию
                return self._smart_search(query)

        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"[{self.AGENT_ID}] Ошибка обработки: {e}")
            return self._error_response(str(e))
        finally:
            self.state = AgentState.IDLE

    def _route_to_agent(self, target_agent: str, query: str) -> Dict:
        """Маршрутизация к downstream агенту"""
        logger.info(f"[{self.AGENT_ID}] Маршрутизация к {target_agent}")
        return {
            "status": "routed",
            "target_agent": target_agent,
            "original_query": query,
            "message": f"Запрос перенаправлен к {target_agent}",
            "agent_capabilities": self._get_agent_capabilities(target_agent)
        }

    def _get_agent_capabilities(self, agent_id: str) -> Dict:
        """Получение возможностей downstream агента"""
        capabilities = {
            "analytical_agent": {
                "purpose": "Глубокий анализ содержимого узлов",
                "operations": ["analyze_node", "compare_nodes", "extract_insights"]
            },
            "graph_agent": {
                "purpose": "Работа с графом связей",
                "operations": ["get_edges", "find_path", "centrality_analysis"]
            },
            "source_agent": {
                "purpose": "Работа с первоисточниками",
                "operations": ["extract_text", "parse_document", "get_metadata"]
            },
            "visualization_agent": {
                "purpose": "Визуализация данных",
                "operations": ["render_graph", "create_diagram", "export_chart"]
            }
        }
        return capabilities.get(agent_id, {})

    # ==========================================
    # ОПЕРАЦИИ МАТЕРИАЛОВ
    # ==========================================

    def get_material(self, material_id: str) -> Dict:
        """
        Получение материала по ID

        Args:
            material_id: ID материала (NODE-*, SRC-*, etc.)
        """
        self.context.materials_accessed.append(material_id)
        self.context.current_focus = material_id

        material = self.db.get_material(material_id)
        if material:
            self._log_operation("get_material", {"material_id": material_id}, "success")
            return {
                "status": "success",
                "operation": "get_material",
                "data": material
            }
        else:
            return {
                "status": "error",
                "operation": "get_material",
                "error": f"Материал {material_id} не найден"
            }

    def list_materials(
        self,
        category: Optional[str] = None,
        layer: Optional[str] = None,
        limit: int = 50
    ) -> Dict:
        """
        Список материалов с фильтрацией

        Args:
            category: Категория (RAW_SOURCES, ANALYTICAL_NODES, etc.)
            layer: Слой (L1-Strategic, L2-Operational, L3-Technical)
            limit: Максимум записей
        """
        cat_enum = MaterialCategory[category] if category else None
        materials = self.db.list_materials(category=cat_enum, layer=layer, limit=limit)

        self._log_operation("list_materials", {
            "category": category,
            "layer": layer,
            "limit": limit
        }, "success")

        return {
            "status": "success",
            "operation": "list_materials",
            "data": {
                "count": len(materials),
                "materials": materials,
                "filters": {"category": category, "layer": layer}
            }
        }

    def search(self, query: str, category: Optional[str] = None) -> Dict:
        """
        Поиск материалов

        Args:
            query: Поисковый запрос
            category: Ограничение по категории
        """
        cat_enum = MaterialCategory[category] if category else None
        results = self.db.search_materials(query, category=cat_enum)

        self._log_operation("search", {"query": query, "category": category}, "success")

        return {
            "status": "success",
            "operation": "search",
            "data": {
                "query": query,
                "count": len(results),
                "results": results
            }
        }

    # ==========================================
    # ТРАССИРОВКА
    # ==========================================

    def get_source_chain(self, source_id: str) -> Dict:
        """
        Получение цепочки трассировки: Source → Nodes

        Args:
            source_id: ID первоисточника (SRC-*)
        """
        chain = self.db.get_source_chain(source_id)
        self._log_operation("get_source_chain", {"source_id": source_id}, "success")

        return {
            "status": "success",
            "operation": "get_source_chain",
            "data": chain
        }

    def get_node_sources(self, node_id: str) -> Dict:
        """
        Получение источников узла

        Args:
            node_id: ID узла (NODE-*)
        """
        sources = self.db.get_node_sources(node_id)
        self._log_operation("get_node_sources", {"node_id": node_id}, "success")

        return {
            "status": "success",
            "operation": "get_node_sources",
            "data": {
                "node_id": node_id,
                "sources": sources
            }
        }

    def get_node_edges(self, node_id: str, direction: str = "both") -> Dict:
        """
        Получение связей узла

        Args:
            node_id: ID узла
            direction: 'incoming', 'outgoing', 'both'
        """
        edges = self.db.get_node_edges(node_id, direction)
        self._log_operation("get_node_edges", {"node_id": node_id, "direction": direction}, "success")

        return {
            "status": "success",
            "operation": "get_node_edges",
            "data": {
                "node_id": node_id,
                "direction": direction,
                "edges": edges
            }
        }

    # ==========================================
    # СТАТИСТИКА И ОБЗОР
    # ==========================================

    def get_overview(self) -> Dict:
        """Полный обзор базы знаний"""
        stats = self.db.get_statistics()
        graph_overview = self.db.get_graph_overview()

        # Добавляем данные из Gold Index
        gold_stats = self._gold_index.get("quick_stats", {})

        return {
            "status": "success",
            "operation": "get_overview",
            "data": {
                "database": stats,
                "graph": graph_overview,
                "gold_index": gold_stats,
                "critical_path": self._gold_index.get("critical_path", {}),
                "backlinks_ranking": self._gold_index.get("backlinks_ranking", [])[:5]
            }
        }

    def get_statistics(self) -> Dict:
        """Статистика базы данных"""
        stats = self.db.get_statistics()
        return {
            "status": "success",
            "operation": "get_statistics",
            "data": stats
        }

    # ==========================================
    # БЫСТРЫЙ ДОСТУП (Gold Index)
    # ==========================================

    def quick_lookup(self, material_id: str) -> Dict:
        """
        Быстрый поиск пути к материалу через Gold Index

        Args:
            material_id: ID материала
        """
        path = self._gold_index.get("id_to_path", {}).get(material_id)
        if path:
            return {
                "status": "success",
                "operation": "quick_lookup",
                "data": {
                    "material_id": material_id,
                    "path": path
                }
            }
        return {
            "status": "error",
            "operation": "quick_lookup",
            "error": f"Материал {material_id} не найден в индексе"
        }

    def search_by_keyword(self, keyword: str) -> Dict:
        """
        Поиск по ключевым словам из Gold Index

        Args:
            keyword: Ключевое слово
        """
        keywords_map = self._gold_index.get("search_keywords", {})

        # Поиск точного совпадения
        if keyword in keywords_map:
            nodes = keywords_map[keyword]
            return {
                "status": "success",
                "operation": "search_by_keyword",
                "data": {
                    "keyword": keyword,
                    "nodes": nodes,
                    "count": len(nodes)
                }
            }

        # Поиск частичного совпадения
        matching = {}
        keyword_lower = keyword.lower()
        for kw, nodes in keywords_map.items():
            if keyword_lower in kw.lower():
                matching[kw] = nodes

        if matching:
            return {
                "status": "success",
                "operation": "search_by_keyword",
                "data": {
                    "keyword": keyword,
                    "matches": matching
                }
            }

        return {
            "status": "not_found",
            "operation": "search_by_keyword",
            "message": f"Ключевое слово '{keyword}' не найдено"
        }

    def get_layer_nodes(self, layer: str) -> Dict:
        """
        Получение узлов по слою

        Args:
            layer: L1-Strategic, L2-Operational, L3-Technical
        """
        layer_members = self._gold_index.get("layer_members", {})
        nodes = layer_members.get(layer, [])

        return {
            "status": "success",
            "operation": "get_layer_nodes",
            "data": {
                "layer": layer,
                "nodes": nodes,
                "count": len(nodes)
            }
        }

    # ==========================================
    # ВНУТРЕННИЕ МЕТОДЫ
    # ==========================================

    def _handle_search(self, query: str) -> Dict:
        """Обработка поискового запроса"""
        # Извлекаем ключевые слова из запроса
        words = query.lower().replace("найди", "").replace("поиск", "").strip().split()
        search_term = " ".join(words)
        return self.search(search_term)

    def _handle_get(self, query: str) -> Dict:
        """Обработка запроса на получение"""
        # Ищем ID материала в запросе
        import re
        pattern = r'(NODE|SRC|GRAPH|SCHEMA|GOLD)-[A-Z0-9-]+'
        match = re.search(pattern, query.upper())
        if match:
            return self.get_material(match.group())
        return self._smart_search(query)

    def _handle_list(self, query: str) -> Dict:
        """Обработка запроса на список"""
        query_lower = query.lower()

        if "node" in query_lower or "узл" in query_lower:
            return self.list_materials(category="ANALYTICAL_NODES")
        elif "source" in query_lower or "источник" in query_lower:
            return self.list_materials(category="RAW_SOURCES")
        elif "strategic" in query_lower or "l1" in query_lower:
            return self.list_materials(layer="L1-Strategic")
        elif "operational" in query_lower or "l2" in query_lower:
            return self.list_materials(layer="L2-Operational")
        elif "technical" in query_lower or "l3" in query_lower:
            return self.list_materials(layer="L3-Technical")
        else:
            return self.list_materials()

    def _handle_stats(self) -> Dict:
        """Обработка запроса статистики"""
        return self.get_overview()

    def _handle_traceability(self, query: str) -> Dict:
        """Обработка запроса трассировки"""
        import re
        pattern = r'(NODE|SRC)-[A-Z0-9-]+'
        match = re.search(pattern, query.upper())

        if match:
            material_id = match.group()
            if material_id.startswith("SRC"):
                return self.get_source_chain(material_id)
            else:
                return self.get_node_sources(material_id)

        return {
            "status": "error",
            "message": "Укажите ID материала (SRC-* или NODE-*)"
        }

    def _smart_search(self, query: str) -> Dict:
        """Умный поиск по контексту"""
        # Сначала ищем по ключевым словам Gold Index
        result = self.search_by_keyword(query)
        if result.get("status") == "success":
            return result

        # Затем полнотекстовый поиск
        return self.search(query)

    def _log_operation(self, operation: str, params: Dict, status: str):
        """Логирование операции"""
        self.context.operations_performed.append(operation)
        logger.info(f"[{self.AGENT_ID}] {operation}: {status}")

    def _error_response(self, error: str) -> Dict:
        """Формирование ответа об ошибке"""
        return {
            "status": "error",
            "error": error,
            "agent_id": self.AGENT_ID,
            "session_id": self.context.session_id
        }

    # ==========================================
    # ИНФОРМАЦИЯ ОБ АГЕНТЕ
    # ==========================================

    def get_agent_info(self) -> Dict:
        """Информация об агенте"""
        return {
            "agent_id": self.AGENT_ID,
            "name": self.AGENT_NAME,
            "version": self.AGENT_VERSION,
            "state": self.state.value,
            "session_id": self.context.session_id,
            "capabilities": [
                "material_management",
                "search",
                "traceability",
                "routing",
                "validation"
            ],
            "downstream_agents": list(set(self.ROUTING_PATTERNS.values())),
            "gold_index_loaded": bool(self._gold_index)
        }

    def get_session_context(self) -> Dict:
        """Текущий контекст сессии"""
        return {
            "session_id": self.context.session_id,
            "started_at": self.context.started_at.isoformat(),
            "materials_accessed": self.context.materials_accessed,
            "operations_count": len(self.context.operations_performed),
            "current_focus": self.context.current_focus,
            "queries_count": len(self.context.query_history)
        }
