#!/usr/bin/env bash
# Convierte un .tex de apuntes en un borrador .qmd con pandoc.
# Uso: scripts/tex_a_qmd.sh entrada.tex cursos/<curso>/<tema>.qmd
# El resultado es un punto de partida: hay que revisar entornos de teorema,
# referencias cruzadas, figuras y macros a mano (ver docs/componentes.md).
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Uso: $0 entrada.tex salida.qmd" >&2
  exit 1
fi

pandoc "$1" -f latex -t markdown --wrap=none --markdown-headings=atx -o "$2"
echo "Borrador creado en $2. Revisar a mano antes de publicar."
