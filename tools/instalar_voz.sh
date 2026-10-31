#!/usr/bin/env bash
# Instala un motor de voz para los Shorts. Prueba, por este orden:
#  1. Piper (voz neuronal): necesita acceso a pypi.org, files.pythonhosted.org y huggingface.co.
#  2. espeak-ng + MBROLA, ya compilados en la rama `voz` de este repositorio: solo necesita GitHub.
# Si ninguno se puede instalar, los Shorts se siguen generando, solo que sin voz.
set -uo pipefail
DIR="${ALEIX_VOICES:-$HOME/.cache/aleix-voices}"
REPO="${ALEIX_REPO:-https://github.com/aeixxx754/aleix-shorts}"
mkdir -p "$DIR"

piper() {
  python3 -c "import piper" 2>/dev/null || \
    timeout 180 pip install --quiet --retries 0 --timeout 15 --break-system-packages piper-tts 2>/dev/null || \
    timeout 180 pip install --quiet --retries 0 --timeout 15 piper-tts 2>/dev/null || return 1
  local BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main"
  for v in es/es_ES/davefx/medium/es_ES-davefx-medium en/en_US/lessac/medium/en_US-lessac-medium; do
    local n; n="$(basename "$v")"
    for ext in onnx onnx.json; do
      if [ ! -s "$DIR/$n.$ext" ]; then
        curl -fsSL --max-time 300 -o "$DIR/$n.$ext.part" "$BASE/$v.$ext" || { rm -f "$DIR/$n.$ext.part"; return 1; }
        mv "$DIR/$n.$ext.part" "$DIR/$n.$ext"
      fi
    done
  done
  python3 -c "import piper" 2>/dev/null
}

mbrola() {
  if [ ! -x "$DIR/mbrola/bin/espeak-ng" ]; then
    rm -rf "$DIR/mbrola.tmp"
    timeout 600 git clone -q --depth 1 -b voz "$REPO" "$DIR/mbrola.tmp" || return 1
    rm -rf "$DIR/mbrola" && mv "$DIR/mbrola.tmp" "$DIR/mbrola"
  fi
  chmod +x "$DIR/mbrola/bin/"* 2>/dev/null
  PATH="$DIR/mbrola/bin:$PATH" "$DIR/mbrola/bin/espeak-ng" --path="$DIR/mbrola" -v mb-es2 -w /dev/null "hola" >/dev/null 2>&1
}

if [ "${ALEIX_MOTOR:-}" != "mbrola" ] && piper; then
  echo "Voz lista: Piper (neuronal) en $DIR"
elif mbrola; then
  echo "Voz lista: espeak-ng + MBROLA en $DIR/mbrola"
else
  echo "AVISO: no se ha podido instalar ningún motor de voz; los Shorts saldrán solo con música" >&2
  exit 1
fi
