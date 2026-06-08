"""
Gera QR code apontando para o repositório do grupo.
Salva em metrics/qrcode_repo.png — usado no rodapé do painel A1.
"""

import sys
from pathlib import Path

import qrcode

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "metrics" / "qrcode_repo.png"
OUT.parent.mkdir(exist_ok=True)

DEFAULT_URL = "https://github.com/Ceciliarufatto/langgraph"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(OUT)
    print(f"QR code -> {OUT}")
    print(f"URL: {url}")


if __name__ == "__main__":
    main()
