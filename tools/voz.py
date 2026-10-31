"""Voz en off para los Shorts.

Dos motores, por orden de preferencia:
1. Piper (voz neuronal). Necesita acceso a pypi.org y huggingface.co para instalarse.
2. espeak-ng + MBROLA (voces de difonos grabadas). Viene ya compilado en la rama `voz`
   de este repositorio, así que solo necesita GitHub.
`bash tools/instalar_voz.sh` instala el que pueda. Si no hay ninguno, `disponible()`
explica qué falta y el Short sale solo con música, como antes.
"""
import os, wave, tempfile, subprocess
import numpy as np

VOICES_DIR = os.environ.get("ALEIX_VOICES", os.path.expanduser("~/.cache/aleix-voices"))
VOICES = {"es": "es_ES-davefx-medium", "en": "en_US-lessac-medium"}
# Paquete espeak-ng + MBROLA (rama `voz`): carpeta con bin/ y espeak-ng-data/
MBROLA_DIR = os.environ.get("ALEIX_MBROLA", os.path.join(VOICES_DIR, "mbrola"))
MBROLA_VOZ = {"es": os.environ.get("ALEIX_VOZ_ES", "mb-es2"), "en": os.environ.get("ALEIX_VOZ_EN", "mb-us1")}
MBROLA_PPM = {"es": 150, "en": 155}  # palabras por minuto a velocidad normal
ENTRADA = 0.15   # la voz empieza 0,15 s después del inicio de cada tramo
MARGEN = 0.10    # y termina al menos 0,10 s antes del cambio de escena
MIN_ESCALA = 0.78  # como mucho, un 22 % más rápida que su velocidad normal


def model_path(lang):
    return os.path.join(VOICES_DIR, VOICES[lang] + ".onnx")


def _piper_ok(lang):
    try:
        import piper  # noqa: F401
    except Exception:
        return False
    m = model_path(lang)
    return os.path.exists(m) and os.path.exists(m + ".json")


def _mbrola_ok(lang):
    voz = MBROLA_VOZ[lang].replace("mb-", "")
    return all(os.path.exists(os.path.join(MBROLA_DIR, p)) for p in
               ("bin/espeak-ng", "bin/mbrola", f"espeak-ng-data/mbrola/{voz}"))


def motor(lang):
    """'piper', 'mbrola' o None."""
    if os.environ.get("ALEIX_VOZ", "1") == "0" or lang not in VOICES:
        return None
    if os.environ.get("ALEIX_MOTOR") != "mbrola" and _piper_ok(lang):
        return "piper"
    if _mbrola_ok(lang):
        return "mbrola"
    return None


def disponible(lang):
    """None si se puede generar voz en `lang`; si no, el motivo."""
    if os.environ.get("ALEIX_VOZ", "1") == "0":
        return "voz desactivada con ALEIX_VOZ=0"
    if lang not in VOICES:
        return f"no hay voz para el idioma {lang}"
    if motor(lang):
        return None
    return f"no hay motor de voz instalado en {VOICES_DIR} (ejecuta tools/instalar_voz.sh)"


def descripcion(lang):
    m = motor(lang)
    return {"piper": f"Piper {VOICES.get(lang)}", "mbrola": f"MBROLA {MBROLA_VOZ.get(lang)}"}.get(m, "sin voz")


_voces = {}


def _voice(lang):
    from piper import PiperVoice
    if lang not in _voces:
        _voces[lang] = PiperVoice.load(model_path(lang))
    return _voces[lang]


def sintetizar(text, lang, escala=1.0):
    """Texto -> (muestras float32 mono entre -1 y 1, frecuencia de muestreo).
    `escala` < 1 habla más rápido (0,8 = un 20 % más corto)."""
    fd, tmp = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        if motor(lang) == "mbrola":
            env = dict(os.environ, PATH=os.path.join(MBROLA_DIR, "bin") + os.pathsep + os.environ.get("PATH", ""))
            ppm = int(min(230, MBROLA_PPM[lang] / max(escala, 0.5)))
            subprocess.run([os.path.join(MBROLA_DIR, "bin", "espeak-ng"), "--path=" + MBROLA_DIR,
                            "-v", MBROLA_VOZ[lang], "-s", str(ppm), "-w", tmp, text],
                           env=env, check=True, capture_output=True, timeout=60)
        else:
            v = _voice(lang)
            with wave.open(tmp, "wb") as wf:
                try:  # piper-tts >= 1.3
                    from piper import SynthesisConfig
                    v.synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=escala))
                except ImportError:  # piper-tts 1.2
                    v.synthesize(text, wf, length_scale=escala)
        with wave.open(tmp, "rb") as wf:
            sr, ch = wf.getframerate(), wf.getnchannels()
            a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        if ch > 1:
            a = a.reshape(-1, ch).mean(1)
        return a, sr
    finally:
        os.remove(tmp)


def _recortar(a, sr, umbral=0.02):
    """Quita el silencio del principio y del final."""
    idx = np.flatnonzero(np.abs(a) > umbral)
    if not len(idx):
        return a[:0]
    i0 = max(0, idx[0] - int(0.02 * sr)); i1 = min(len(a), idx[-1] + int(0.06 * sr))
    return a[i0:i1]


def _remuestrear(a, sr, sr2):
    if sr == sr2 or not len(a):
        return a
    n2 = int(round(len(a) * sr2 / sr))
    return np.interp(np.linspace(0, len(a) - 1, n2), np.arange(len(a)), a).astype(np.float32)


def pista(textos, inicios, duraciones, lang, total, sr=44100, sintetizador=None):
    """Pista de voz alineada con los tramos del vídeo.

    Devuelve (voz, presencia): dos arrays de `total` segundos a `sr` Hz. `presencia`
    vale 1 donde se oye la voz y sirve para bajar la música debajo.
    `sintetizador(texto, lang, escala)` permite sustituir Piper (pruebas).
    """
    sint = sintetizador or sintetizar
    n = int(round(sr * total))
    voz = np.zeros(n, np.float32); presencia = np.zeros(n, np.float32)
    avisos = []
    for k, (txt, st, du) in enumerate(zip(textos, inicios, duraciones)):
        txt = " ".join((txt or "").split())
        if not txt:
            continue
        hueco = du - ENTRADA - MARGEN
        a, vsr = sint(txt, lang, 1.0); a = _recortar(a, vsr)
        largo = len(a) / vsr
        if largo > hueco:  # habla un poco más rápido para que quepa
            escala = max(MIN_ESCALA, hueco / largo * 0.97)
            a, vsr = sint(txt, lang, escala); a = _recortar(a, vsr)
        a = _remuestrear(a, vsr, sr)
        maxn = int(hueco * sr)
        if len(a) > maxn:  # sigue sin caber: se corta con un fundido y se avisa
            avisos.append(f"tramo {k + 1}: la voz dura {len(a) / sr:.1f} s y caben {hueco:.1f} s; acorta el texto")
            a = a[:maxn].copy(); f = int(0.08 * sr); a[-f:] *= np.linspace(1, 0, f)
        pico = float(np.max(np.abs(a))) if len(a) else 0
        if pico > 0:
            a = a * (0.9 / pico)
        i = int((st + ENTRADA) * sr)
        a = a[: max(0, n - i)]
        voz[i:i + len(a)] += a
        presencia[i:i + len(a)] = 1
    # suaviza la presencia para que la música baje y suba sin saltos (~120 ms)
    k = int(0.12 * sr)
    if k > 1 and presencia.any():
        presencia = np.convolve(presencia, np.ones(k, np.float32) / k, mode="same")
        presencia = np.clip(presencia * 1.5, 0, 1)
    return voz, presencia, avisos


def textos_desde_pantalla(T):
    """Locución por defecto cuando el JSON no trae `voz`: se lee lo que sale en pantalla."""
    def frase(s):
        s = " ".join(s.split()).lower()
        for i, ch in enumerate(s):
            if ch.isalpha():
                return s[:i] + ch.upper() + s[i + 1:]
        return s
    hook = frase(T["hook"][0])
    facts = [f"{frase(a)} {b.lower()}. {c}" for _, a, b, c in T["facts"]]
    outro = f"{T['outro'][0]} {T['outro'][1]}"
    return [hook] + facts + [outro]
