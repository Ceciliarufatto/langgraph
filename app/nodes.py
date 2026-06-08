"""
Nós do grafo: processam diferentes tipos de intenção do usuário.
"""

import logging
from typing import Dict, Any
from app.memory import load_memory, save_memory

logger = logging.getLogger(__name__)

INTENT_KEYWORDS = {
    "pedido": ["pedido", "compra", "rastrear", "entrega", "produto", "ordem"],
    "suporte": ["senha", "suporte", "problema", "erro", "bug", "ajuda", "técnico"],
}

RESPONSE_TEMPLATES = {
    "pedido": (
        "🛒 Entendi que você quer informações sobre pedido. "
        "Posso ajudar com:\n"
        "• Rastreamento de pedido\n"
        "• Informações de entrega\n"
        "• Status da compra"
    ),
    "suporte": (
        "🆘 Entendo que você precisa de suporte técnico. "
        "Posso ajudar com:\n"
        "• Recuperação de senha\n"
        "• Problemas de acesso\n"
        "• Erros técnicos"
    ),
    "geral": (
        "👋 Olá! Bem-vindo ao nosso atendimento inteligente. "
        "Como posso te ajudar hoje?"
    ),
}


def _append_history(state: Dict[str, Any], response: str) -> Dict[str, Any]:
    """Atualiza o histórico e persiste a sessão atual."""
    session_id = state.get("session_id", "default")
    history = load_memory(session_id)

    history.append(f"user: {state['message']}")
    history.append(f"assistant: {response}")
    save_memory(session_id, history)

    state["response"] = response
    state["history"] = history
    return state


def detect_intent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detecta a intenção do usuário analisando palavras-chave."""
    message = state["message"].lower()
    detected_intent = "geral"
    confidence = 0.3

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message:
                detected_intent = intent
                confidence = min(0.9, 0.5 + len(keywords) * 0.1)
                logger.info(f"Intent detected: {intent} (confidence: {confidence:.2f})")
                break
        if detected_intent != "geral":
            break

    state["intent"] = detected_intent
    state["confidence"] = confidence
    return state


def order_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handler para intenção de pedido."""
    return _append_history(state, RESPONSE_TEMPLATES["pedido"])


def support_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handler para intenção de suporte técnico."""
    return _append_history(state, RESPONSE_TEMPLATES["suporte"])


def general_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handler para intenções gerais."""
    return _append_history(state, RESPONSE_TEMPLATES["geral"])


def route_intent(state: Dict[str, Any]) -> str:
    """Função de roteamento condicional."""
    return state.get("intent", "geral")
