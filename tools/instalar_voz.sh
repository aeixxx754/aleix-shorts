#!/usr/bin/env bash
# Instala Piper (voz local y gratuita) y descarga las voces en español e inglés.
# Necesita acceso de red a pypi.org, files.pythonhosted.org y huggingface.co.
# Si falla, los Shorts se siguen generando, solo que sin voz.
set -euo pipefail
DIR="${ALEIX_VOICES:-$HOME/.cache/aleix-voices}"
mkdir -p "$DIR"

python3 -c "import piper" 2>/dev/null || \
  pip install --quiet --break-system-packages piper-tts 2>/dev/null || \
  pip install --quiet piper-tts

BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main"
for v in es/es_ES/davefx/medium/es_ES-davefx-medium en/en_US/lessac/medium/en_US-lessac-medium; do
  n="$(basename "$v")"
  for ext in onnx onnx.json; do
    if [ ! -s "$DIR/$n.$ext" ]; then
      curl -fsSL --retry 2 -o "$DIR/$n.$ext.part" "$BASE/$v.$ext"
      mv "$DIR/$n.$ext.part" "$DIR/$n.$ext"
    fi
  done
done

python3 -c "import piper" && echo "Voz lista: Piper + voces en $DIR"
