import json
from pathlib import Path

import pytest

from app.memory import clear_memory, load_memory, save_memory
from app.nodes import (
    detect_intent,
    order_response,
    support_response,
    general_response,
    route_intent,
)
from app.state import build_agent_state
from app.graph import build_graph
import app.memory as memory_module


def test_build_agent_state_includes_required_fields():
    state = build_agent_state("Olá", "sessao123")

    assert state["message"] == "Olá"
    assert state["intent"] == ""
    assert state["confidence"] == 0.0
    assert state["response"] == ""
    assert state["history"] == []
    assert state["metadata"] == {}
    assert state["session_id"] == "sessao123"
    assert state["timestamp"] is not None


def test_detect_intent_pedido():
    state = {"message": "Quero rastrear meu pedido", "intent": "", "confidence": 0.0}
    result = detect_intent(state)

    assert result["intent"] == "pedido"
    assert result["confidence"] >= 0.5


def test_detect_intent_suporte():
    state = {"message": "Estou com problema de senha", "intent": "", "confidence": 0.0}
    result = detect_intent(state)

    assert result["intent"] == "suporte"
    assert result["confidence"] >= 0.5


def test_detect_intent_geral_fallback():
    state = {"message": "Olá, como vai?", "intent": "", "confidence": 0.0}
    result = detect_intent(state)

    assert result["intent"] == "geral"
    assert result["confidence"] == 0.3


def test_route_intent_returns_intent():
    state = {"intent": "suporte"}
    assert route_intent(state) == "suporte"

    state = {}
    assert route_intent(state) == "geral"


def test_order_response_persists_history(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setattr(memory_module, "CHECKPOINT_DIR", str(tmp_path / "checkpoints"))

    state = build_agent_state("Quero rastrear meu pedido", "sessao_1")
    state["intent"] = "pedido"

    result = order_response(state)

    assert "🛒" in result["response"]
    assert result["history"][-1].startswith("assistant:")
    assert load_memory("sessao_1") == result["history"]


def test_support_response_persists_history(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setattr(memory_module, "CHECKPOINT_DIR", str(tmp_path / "checkpoints"))

    state = build_agent_state("Esqueci minha senha", "sessao_2")
    state["intent"] = "suporte"

    result = support_response(state)

    assert "suporte técnico" in result["response"]
    assert result["history"][-1].startswith("assistant:")
    assert load_memory("sessao_2") == result["history"]


def test_general_response_persists_history(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setattr(memory_module, "CHECKPOINT_DIR", str(tmp_path / "checkpoints"))

    state = build_agent_state("Oi", "sessao_3")
    state["intent"] = "geral"

    result = general_response(state)

    assert "Bem-vindo" in result["response"]
    assert result["history"][-1].startswith("assistant:")
    assert load_memory("sessao_3") == result["history"]


def test_clear_memory_removes_saved_history(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setattr(memory_module, "CHECKPOINT_DIR", str(tmp_path / "checkpoints"))

    session_id = "sessao_limpa"
    save_memory(session_id, ["user: oi", "assistant: olá"])
    assert load_memory(session_id) == ["user: oi", "assistant: olá"]

    assert clear_memory(session_id)
    assert load_memory(session_id) == []


def test_graph_inference_routes_to_correct_handler(monkeypatch, tmp_path):
    monkeypatch.setattr(memory_module, "MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setattr(memory_module, "CHECKPOINT_DIR", str(tmp_path / "checkpoints"))

    graph = build_graph()
    state = build_agent_state("Preciso de ajuda com um erro", "sessao_graph")
    result = graph.invoke(state)

    assert result["intent"] == "suporte"
    assert "suporte técnico" in result["response"]


def test_build_graph_compiles():
    graph = build_graph()
    assert graph is not None
