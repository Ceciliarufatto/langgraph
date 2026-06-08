"""
Definição do estado compartilhado no grafo de LangGraph.
"""

from datetime import datetime
from typing import TypedDict, List, Optional, Dict, Any


class AgentState(TypedDict):
    """Estado imutável do agente conversacional."""
    message: str
    intent: str
    confidence: float
    response: str
    history: List[str]
    metadata: Dict[str, Any]
    timestamp: Optional[str]
    session_id: str


def build_agent_state(
    message: str,
    session_id: str,
    history: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> "AgentState":
    """Construção padrão do estado inicial para invocação do grafo."""
    if history is None:
        history = []
    if metadata is None:
        metadata = {}

    return {
        "message": message,
        "intent": "",
        "confidence": 0.0,
        "response": "",
        "history": history,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
    }
