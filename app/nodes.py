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
    history = load_memory(state.get("session_id", "default"))
    
    response = (
        "🛒 Entendi que você quer informações sobre pedido. "
        "Posso ajudar com:\n"
        "• Rastreamento de pedido\n"
        "• Informações de entrega\n"
        "• Status da compra"
    )
    
    history.append(f"user: {state['message']}")
    history.append(f"assistant: {response}")
    save_memory(state.get("session_id", "default"), history)
    
    state["response"] = response
    state["history"] = history
    return state


def support_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handler para intenção de suporte técnico."""
    history = load_memory(state.get("session_id", "default"))
    
    response = (
        "🆘 Entendo que você precisa de suporte técnico. "
        "Posso ajudar com:\n"
        "• Recuperação de senha\n"
        "• Problemas de acesso\n"
        "• Erros técnicos"
    )
    
    history.append(f"user: {state['message']}")
    history.append(f"assistant: {response}")
    save_memory(state.get("session_id", "default"), history)
    
    state["response"] = response
    state["history"] = history
    return state


def general_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handler para intenções gerais."""
    history = load_memory(state.get("session_id", "default"))
    
    response = (
        "👋 Olá! Bem-vindo ao nosso atendimento inteligente. "
        "Como posso te ajudar hoje?"
    )
    
    history.append(f"user: {state['message']}")
    history.append(f"assistant: {response}")
    save_memory(state.get("session_id", "default"), history)
    
    state["response"] = response
    state["history"] = history
    return state


def route_intent(state: Dict[str, Any]) -> str:
    """Função de roteamento condicional."""
    return state.get("intent", "geral")
