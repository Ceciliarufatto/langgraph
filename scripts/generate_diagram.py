"""
Gera diagrama do StateGraph do agente.

Tenta primeiro draw_mermaid_png() (requer rede para o renderer da Mermaid.ink).
Se falhar, salva o source Mermaid em .mmd e o ASCII do grafo em .txt,
que podem ser renderizados manualmente (mermaid.live / mermaid-cli).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.graph import build_graph

OUT_DIR = ROOT / "metrics"
OUT_DIR.mkdir(exist_ok=True)


def main():
    graph = build_graph()
    g = graph.get_graph()

    mmd_path = OUT_DIR / "graph.mmd"
    mmd_path.write_text(g.draw_mermaid(), encoding="utf-8")
    print(f"Mermaid source -> {mmd_path}")

    ascii_path = OUT_DIR / "graph_ascii.txt"
    try:
        ascii_path.write_text(g.draw_ascii(), encoding="utf-8")
        print(f"ASCII diagram  -> {ascii_path}")
    except Exception as e:
        print(f"(ASCII indisponível: {e})")

    png_path = OUT_DIR / "graph.png"
    try:
        png_bytes = g.draw_mermaid_png()
        png_path.write_bytes(png_bytes)
        print(f"PNG diagram    -> {png_path}")
    except Exception as e:
        print(f"PNG não gerado (rede/render indisponível): {e}")
        print(f"Renderize {mmd_path} em https://mermaid.live para obter o PNG.")


if __name__ == "__main__":
    main()
