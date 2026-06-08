"""
Suite de avaliação do agente LangGraph (G1 - EN-045).

Roda o dataset rotulado pelo grafo e calcula:
- Accuracy global
- Precision / Recall / F1 por classe
- Matriz de confusão (PNG)
- Latência média por mensagem (ms)
- Distribuição de confidence

Artefatos gerados em metrics/:
- metrics.json
- confusion_matrix.png
- report.md
"""

import json
import time
import logging
import uuid
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)

from app.graph import build_graph
from app.state import build_agent_state

logging.basicConfig(level=logging.WARNING)

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "eval_dataset.json"
METRICS_DIR = ROOT / "metrics"
METRICS_DIR.mkdir(exist_ok=True)

LABELS = ["pedido", "suporte", "geral"]


def load_dataset():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def run_evaluation():
    dataset = load_dataset()
    samples = dataset["samples"]
    graph = build_graph()

    y_true, y_pred = [], []
    latencies_ms = []
    confidences = []

    session_id = f"eval-{uuid.uuid4().hex[:8]}"

    for sample in samples:
        msg, label = sample["message"], sample["label"]

        start = time.perf_counter()
        result = graph.invoke(
            build_agent_state(msg, session_id, history=[], metadata={"eval": True})
        )
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        y_true.append(label)
        y_pred.append(result.get("intent", "geral"))
        latencies_ms.append(elapsed_ms)
        confidences.append(float(result.get("confidence", 0.0)))

    return y_true, y_pred, latencies_ms, confidences


def compute_metrics(y_true, y_pred, latencies_ms, confidences):
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, zero_division=0
    )
    cm = confusion_matrix(y_true, y_pred, labels=LABELS)

    per_class = {
        label: {
            "precision": round(float(precision[i]), 4),
            "recall": round(float(recall[i]), 4),
            "f1": round(float(f1[i]), 4),
            "support": int(support[i]),
        }
        for i, label in enumerate(LABELS)
    }

    metrics = {
        "generated_at": datetime.now().isoformat(),
        "dataset_size": len(y_true),
        "labels": LABELS,
        "accuracy": round(float(accuracy), 4),
        "macro_f1": round(float(np.mean(f1)), 4),
        "per_class": per_class,
        "confusion_matrix": cm.tolist(),
        "latency_ms": {
            "mean": round(float(np.mean(latencies_ms)), 3),
            "p50": round(float(np.percentile(latencies_ms, 50)), 3),
            "p95": round(float(np.percentile(latencies_ms, 95)), 3),
            "max": round(float(np.max(latencies_ms)), 3),
        },
        "confidence": {
            "mean": round(float(np.mean(confidences)), 4),
            "min": round(float(np.min(confidences)), 4),
            "max": round(float(np.max(confidences)), 4),
        },
    }
    return metrics, cm


def plot_confusion_matrix(cm, out_path):
    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(LABELS)))
    ax.set_yticks(range(len(LABELS)))
    ax.set_xticklabels(LABELS)
    ax.set_yticklabels(LABELS)
    ax.set_xlabel("Predito", fontsize=12)
    ax.set_ylabel("Verdadeiro", fontsize=12)
    ax.set_title("Matriz de Confusão — Classificador de Intenção", fontsize=13)

    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color=color, fontsize=14, fontweight="bold")

    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def write_report(metrics, out_path):
    pc = metrics["per_class"]
    lat = metrics["latency_ms"]
    conf = metrics["confidence"]

    lines = [
        "# Relatório de Avaliação — Agente LangGraph (G1)",
        "",
        f"Gerado em: {metrics['generated_at']}",
        f"Tamanho do dataset: **{metrics['dataset_size']}** mensagens rotuladas",
        "",
        "## Métricas globais",
        "",
        f"- **Accuracy:** {metrics['accuracy']:.2%}",
        f"- **Macro F1:** {metrics['macro_f1']:.4f}",
        "",
        "## Por classe",
        "",
        "| Classe | Precision | Recall | F1 | Suporte |",
        "|--------|-----------|--------|----|---------|",
    ]
    for label in LABELS:
        c = pc[label]
        lines.append(
            f"| {label} | {c['precision']:.4f} | {c['recall']:.4f} | {c['f1']:.4f} | {c['support']} |"
        )

    lines += [
        "",
        "## Latência (ms)",
        "",
        f"- Média: {lat['mean']:.2f}",
        f"- P50: {lat['p50']:.2f}",
        f"- P95: {lat['p95']:.2f}",
        f"- Máx: {lat['max']:.2f}",
        "",
        "## Confidence",
        "",
        f"- Média: {conf['mean']:.4f}",
        f"- Mín: {conf['min']:.4f}",
        f"- Máx: {conf['max']:.4f}",
        "",
        "## Matriz de confusão",
        "",
        "Veja `confusion_matrix.png`.",
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Executando avaliação...")
    y_true, y_pred, latencies, confidences = run_evaluation()

    metrics, cm = compute_metrics(y_true, y_pred, latencies, confidences)

    metrics_path = METRICS_DIR / "metrics.json"
    cm_path = METRICS_DIR / "confusion_matrix.png"
    report_path = METRICS_DIR / "report.md"

    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    plot_confusion_matrix(cm, cm_path)
    write_report(metrics, report_path)

    print("\n=== Resultados ===")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
    print(f"Latência média: {metrics['latency_ms']['mean']:.2f} ms")
    print("\nClassification report:")
    print(classification_report(y_true, y_pred, labels=LABELS, zero_division=0))

    print(f"\nArtefatos salvos em: {METRICS_DIR}")


if __name__ == "__main__":
    main()
