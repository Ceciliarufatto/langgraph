"""
Definição do estado compartilhado no grafo de LangGraph.
"""

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
