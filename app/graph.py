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

    node_handlers = {
        "detect_intent": detect_intent,
        "pedido": order_response,
        "suporte": support_response,
        "geral": general_response,
    }

    for node_name, node_fn in node_handlers.items():
        graph.add_node(node_name, node_fn)

    graph.set_entry_point("detect_intent")
    graph.add_conditional_edges(
        "detect_intent",
        route_intent,
        {node_name: node_name for node_name in node_handlers if node_name != "detect_intent"}
    )

    for node_name in node_handlers:
        if node_name != "detect_intent":
            graph.add_edge(node_name, END)

    compiled = graph.compile()
    logger.info("Graph compiled successfully")
    return compiled
