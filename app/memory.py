"""
Persistência de memória e checkpoints do agente.
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

MEMORY_DIR = "data/memory"
CHECKPOINT_DIR = "data/checkpoints"


def _ensure_directories():
    """Garante que os diretórios necessários existem."""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)


def _get_memory_file(session_id: str = "default") -> str:
    """Retorna o caminho do arquivo de memória para uma sessão."""
    return os.path.join(MEMORY_DIR, f"{session_id}_memory.json")


def load_memory(session_id: str = "default") -> List[str]:
    """Carrega o histórico de conversas da memória persistente."""
    _ensure_directories()
    
    memory_file = _get_memory_file(session_id)
    
    if not os.path.exists(memory_file):
        logger.debug(f"Memory file not found for session {session_id}")
        return []

    try:
        with open(memory_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Loaded {len(data)} messages from memory")
            return data
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Failed to load memory: {e}")
        return []


def save_memory(session_id: str = "default", history: List[str] = None) -> bool:
    """Salva o histórico de conversas na memória persistente."""
    if history is None:
        history = []
    
    _ensure_directories()
    
    memory_file = _get_memory_file(session_id)
    
    try:
        with open(memory_file, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(history)} messages to memory")
        return True
    except IOError as e:
        logger.error(f"Failed to save memory: {e}")
        return False


def save_checkpoint(session_id: str, state: Dict[str, Any], checkpoint_name: Optional[str] = None) -> Optional[str]:
    """Salva um checkpoint do estado atual do agente."""
    _ensure_directories()
    
    if checkpoint_name is None:
        checkpoint_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"{session_id}_{checkpoint_name}.json"
    checkpoint_path = os.path.join(CHECKPOINT_DIR, filename)
    
    try:
        with open(checkpoint_path, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=4, ensure_ascii=False, default=str)
        logger.info(f"Checkpoint saved: {checkpoint_path}")
        return checkpoint_path
    except IOError as e:
        logger.error(f"Failed to save checkpoint: {e}")
        return None


def load_checkpoint(session_id: str, checkpoint_name: str) -> Optional[Dict[str, Any]]:
    """Carrega um checkpoint previamente salvo."""
    filename = f"{session_id}_{checkpoint_name}.json"
    checkpoint_path = os.path.join(CHECKPOINT_DIR, filename)
    
    if not os.path.exists(checkpoint_path):
        logger.warning(f"Checkpoint not found: {checkpoint_path}")
        return None
    
    try:
        with open(checkpoint_path, "r", encoding="utf-8") as file:
            state = json.load(file)
            logger.info(f"Checkpoint loaded: {checkpoint_path}")
            return state
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load checkpoint: {e}")
        return None


def list_checkpoints(session_id: str = None) -> List[str]:
    """Lista todos os checkpoints disponíveis."""
    _ensure_directories()
    
    if not os.path.exists(CHECKPOINT_DIR):
        return []
    
    checkpoints = []
    for filename in os.listdir(CHECKPOINT_DIR):
        if filename.endswith(".json"):
            name = filename[:-5]
            if session_id is None or name.startswith(f"{session_id}_"):
                checkpoints.append(name)
    
    return sorted(checkpoints)


def clear_memory(session_id: str = "default") -> bool:
    """Limpa o histórico de uma sessão."""
    memory_file = _get_memory_file(session_id)
    
    try:
        if os.path.exists(memory_file):
            os.remove(memory_file)
            logger.info(f"Memory cleared for session {session_id}")
        return True
    except OSError as e:
        logger.error(f"Failed to clear memory: {e}")
        return False
