#!/usr/bin/env bash
# Busca claves, rutas personales y el usuario local en los archivos que se van a commitear.
# Uso: bash scripts/chequeo_publico.sh   (sale con 1 si encuentra algo)
set -u
cd "$(dirname "$0")/.."
patron="sk-ant-|ANTHROPIC_API_KEY=.+|${HOME}|/home/[a-z]|/Users/[a-zA-Z]|/mnt/[a-z]"
[ -n "${USER:-}" ] && patron="${patron}|\\b${USER}\\b"
archivos=$( (git ls-files; git ls-files --others --exclude-standard) | sort -u | grep -v '^scripts/chequeo_publico.sh$')
if [ -n "$archivos" ] && echo "$archivos" | xargs -d '\n' grep -nIiE "$patron" 2>/dev/null; then
  echo "ATENCIÓN: revisar las coincidencias de arriba antes de commitear." >&2
  exit 1
fi
echo "Chequeo público OK (claves, rutas y usuario local). Revisá a mano nombres de empresas reales."
