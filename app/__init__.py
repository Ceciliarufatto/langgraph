"""
Aplicação do Agente Inteligente com LangGraph
"""

import logging

__version__ = "1.0.0"
__author__ = "Cecilia Rufatto"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app.graph import build_graph
from app.state import AgentState
from app.memory import (
    load_memory,
    save_memory,
    save_checkpoint,
    load_checkpoint,
    list_checkpoints,
    clear_memory
)

__all__ = [
    "build_graph",
    "AgentState",
    "load_memory",
    "save_memory",
    "save_checkpoint",
    "load_checkpoint",
    "list_checkpoints",
    "clear_memory"
]
