"""Inserta una firma invisible en los párrafos del sitio compilado.

Al final de cada párrafo largo del contenido principal agrega una secuencia de caracteres de
ancho cero que codifica "MPA26-" más cuatro dígitos hexadecimales derivados de la ruta de la
página. Si alguien copia y pega el texto, la firma viaja con él y `detectar_marca.py` la recupera
e indica de qué página salió.

Uso: python scripts/marca_de_agua.py _site
"""
import hashlib
import re
import sys
from pathlib import Path

CERO, UNO, BORDE = "​", "‌", "⁠"
MIN_CARACTERES = 80


def firma(ruta_relativa: str) -> str:
    huella = hashlib.sha1(ruta_relativa.encode("utf-8")).hexdigest()[:4]
    carga = f"MPA26-{huella}".encode("ascii")
    bits = "".join(f"{byte:08b}" for byte in carga)
    return BORDE + "".join(UNO if b == "1" else CERO for b in bits) + BORDE


def texto_plano(fragmento: str) -> str:
    return re.sub(r"<[^>]+>", "", fragmento)


def marcar(html: str, firma_pagina: str) -> str:
    inicio = html.find("<main")
    fin = html.find("</main>")
    if inicio == -1 or fin == -1:
        return html

    def reemplazo(m: re.Match) -> str:
        abre, cuerpo, cierra = m.group(1), m.group(2), m.group(3)
        if len(texto_plano(cuerpo).strip()) < MIN_CARACTERES or firma_pagina in cuerpo:
            return m.group(0)
        return f"{abre}{cuerpo}{firma_pagina}{cierra}"

    zona = re.sub(r"(<p(?:\s[^>]*)?>)(.*?)(</p>)", reemplazo, html[inicio:fin], flags=re.S)
    return html[:inicio] + zona + html[fin:]


def main(carpeta: str) -> None:
    raiz = Path(carpeta)
    total = 0
    for archivo in sorted(raiz.rglob("*.html")):
        relativa = archivo.relative_to(raiz).as_posix()
        original = archivo.read_text(encoding="utf-8")
        nuevo = marcar(original, firma(relativa))
        if nuevo != original:
            archivo.write_text(nuevo, encoding="utf-8")
            total += 1
    print(f"Páginas marcadas: {total}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_site")
