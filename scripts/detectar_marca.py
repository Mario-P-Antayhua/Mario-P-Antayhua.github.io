"""Busca la firma invisible en un texto copiado.

Uso: python scripts/detectar_marca.py archivo.txt
     (o pega el texto por la entrada estándar)
"""
import hashlib
import re
import sys
from pathlib import Path

CERO, UNO, BORDE = "​", "‌", "⁠"


def decodificar(texto: str) -> list[str]:
    hallazgos = []
    for m in re.finditer(f"{BORDE}([{CERO}{UNO}]+){BORDE}", texto):
        bits = "".join("1" if c == UNO else "0" for c in m.group(1))
        octetos = [bits[i:i + 8] for i in range(0, len(bits) - len(bits) % 8, 8)]
        hallazgos.append(bytes(int(o, 2) for o in octetos).decode("ascii", errors="replace"))
    return hallazgos


def pagina_de(huella: str, carpeta_sitio: str = "_site") -> str:
    for archivo in Path(carpeta_sitio).rglob("*.html"):
        relativa = archivo.relative_to(carpeta_sitio).as_posix()
        if hashlib.sha1(relativa.encode("utf-8")).hexdigest()[:4] == huella:
            return relativa
    return "página no encontrada en _site"


if __name__ == "__main__":
    texto = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    firmas = decodificar(texto)
    if not firmas:
        print("No se encontró ninguna firma.")
    for f in sorted(set(firmas)):
        print(f"Firma: {f}  ->  {pagina_de(f.split('-')[-1])}")
