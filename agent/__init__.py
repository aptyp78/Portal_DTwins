"""
Portal_DTwins Agent Module
Knowledge Gate Agent - центральный агент управления знаниями
"""

from .knowledge_gate import KnowledgeGateAgent
from .operations import AgentOperation, OperationResult
from .session import AgentSession

__all__ = [
    "KnowledgeGateAgent",
    "AgentOperation",
    "OperationResult",
    "AgentSession",
]

__version__ = "1.0.0"
