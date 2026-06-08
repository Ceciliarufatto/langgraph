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


def _read_json(file_path: str, default):
    """Lê um JSON de disco com tratamento de erro."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.debug(f"Arquivo não encontrado: {file_path}")
        return default
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Falha ao carregar JSON {file_path}: {e}")
        return default


def _write_json(file_path: str, data: Any) -> bool:
    """Grava dados em JSON com tratamento de erro."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Saved data to {file_path}")
        return True
    except IOError as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        return False


def _get_memory_file(session_id: str = "default") -> str:
    """Retorna o caminho do arquivo de memória para uma sessão."""
    return os.path.join(MEMORY_DIR, f"{session_id}_memory.json")


def load_memory(session_id: str = "default") -> List[str]:
    """Carrega o histórico de conversas da memória persistente."""
    _ensure_directories()

    memory_file = _get_memory_file(session_id)
    return _read_json(memory_file, [])


def save_memory(session_id: str = "default", history: List[str] = None) -> bool:
    """Salva o histórico de conversas na memória persistente."""
    if history is None:
        history = []

    _ensure_directories()
    memory_file = _get_memory_file(session_id)
    return _write_json(memory_file, history)


def save_checkpoint(session_id: str, state: Dict[str, Any], checkpoint_name: Optional[str] = None) -> Optional[str]:
    """Salva um checkpoint do estado atual do agente."""
    _ensure_directories()

    if checkpoint_name is None:
        checkpoint_name = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{session_id}_{checkpoint_name}.json"
    checkpoint_path = os.path.join(CHECKPOINT_DIR, filename)

    return checkpoint_path if _write_json(checkpoint_path, state) else None


def load_checkpoint(session_id: str, checkpoint_name: str) -> Optional[Dict[str, Any]]:
    """Carrega um checkpoint previamente salvo."""
    filename = f"{session_id}_{checkpoint_name}.json"
    checkpoint_path = os.path.join(CHECKPOINT_DIR, filename)

    if not os.path.exists(checkpoint_path):
        logger.warning(f"Checkpoint not found: {checkpoint_path}")
        return None

    return _read_json(checkpoint_path, None)


def list_checkpoints(session_id: str = None) -> List[str]:
    """Lista todos os checkpoints disponíveis."""
    _ensure_directories()

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
