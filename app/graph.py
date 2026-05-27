"""
Construção do grafo de orquestração em LangGraph.
"""

import logging
from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.nodes import (
    detect_intent,
    order_response,
    support_response,
    general_response,
    route_intent
)

logger = logging.getLogger(__name__)


def build_graph():
    """Constrói e compila o grafo de estados para o agente."""
    graph = StateGraph(AgentState)
    
    logger.info("Building LangGraph agent graph...")
    
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("pedido", order_response)
    graph.add_node("suporte", support_response)
    graph.add_node("geral", general_response)
    
    graph.set_entry_point("detect_intent")
    
    graph.add_conditional_edges(
        "detect_intent",
        route_intent,
        {
            "pedido": "pedido",
            "suporte": "suporte",
            "geral": "geral"
        }
    )
    
    graph.add_edge("pedido", END)
    graph.add_edge("suporte", END)
    graph.add_edge("geral", END)
    
    compiled = graph.compile()
    logger.info("Graph compiled successfully")
    
    return compiled
