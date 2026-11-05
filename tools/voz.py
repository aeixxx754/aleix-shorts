"""Voz en off de los Shorts con ElevenLabs.

La clave de la API NO está en el código ni en variables: se guarda como «network secret» en el
entorno en la nube de la tarea (host api.elevenlabs.io, cabecera xi-api-key) y el proxy del
entorno la añade a cada petición. Por eso aquí las peticiones salen sin clave.

Si ElevenLabs no responde (sin secreto, sin créditos, sin red), `disponible()` dice por qué y el
Short sale solo con música, como antes: la publicación nunca se para por la voz.

Uso rápido para comprobar la conexión:  python3 tools/voz.py --check
"""
import os, sys, json, wave, hashlib, tempfile, subprocess, urllib.request, urllib.error
import numpy as np

API = "https://api.elevenlabs.io/v1"
MODELO = os.environ.get("ALEIX_VOZ_MODELO", "eleven_multilingual_v2")  # el mismo narrador en ES y EN
CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz_config.json")
CACHE = os.environ.get("ALEIX_VOZ_CACHE", os.path.expanduser("~/.cache/aleix-voz"))
# Si voz_config.json no fija una voz, se elige la primera de estas que exista en la cuenta
PREFERIDAS = ["George", "Brian", "Daniel", "Charlie", "Sarah", "Laura"]
MAX_RAPIDEZ = 1.2    # como mucho, un 20 % más rápido (límite de ElevenLabs) para que una frase quepa en su tramo

_estado = {}


def _peticion(ruta, datos=None, timeout=60):
    req = urllib.request.Request(API + ruta, method="POST" if datos is not None else "GET")
    req.add_header("Accept", "audio/mpeg" if datos is not None else "application/json")
    if datos is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(datos).encode()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _config():
    try:
        return json.load(open(CONFIG, encoding="utf-8"))
    except Exception:
        return {}


def voz_id():
    """ID de la voz del canal: la de voz_config.json o una de las preferidas de la cuenta."""
    if "voz" in _estado:
        return _estado["voz"]
    cfg = _config()
    if cfg.get("voice_id"):
        _estado["voz"] = (cfg["voice_id"], cfg.get("nombre", "?"))
        return _estado["voz"]
    voces = json.loads(_peticion("/voices")).get("voices", [])
    por_nombre = {v.get("name", "").split(" ")[0].split("-")[0].strip(): v for v in voces}
    for n in PREFERIDAS:
        if n in por_nombre:
            _estado["voz"] = (por_nombre[n]["voice_id"], por_nombre[n]["name"]); return _estado["voz"]
    if voces:
        _estado["voz"] = (voces[0]["voice_id"], voces[0]["name"]); return _estado["voz"]
    raise RuntimeError("la cuenta de ElevenLabs no tiene ninguna voz")


def disponible(lang=None):
    """None si se puede generar voz; si no, el motivo (en castellano)."""
    if os.environ.get("ALEIX_VOZ", "1") == "0":
        return "voz desactivada con ALEIX_VOZ=0"
    if "ok" in _estado:
        return _estado["ok"]
    try:
        voz_id(); _estado["ok"] = None
    except urllib.error.HTTPError as e:
        _estado["ok"] = {401: "ElevenLabs rechaza la clave (revisa el secreto xi-api-key del entorno)",
                         403: "ElevenLabs deniega el acceso con esta clave"}.get(e.code, f"ElevenLabs respondió {e.code}")
    except Exception as e:
        _estado["ok"] = ("no se llega a api.elevenlabs.io: falta el secreto de red en el entorno de la tarea"
                         f" ({type(e).__name__})")
    return _estado["ok"]


def descripcion():
    v = _estado.get("voz")
    return f"ElevenLabs · {v[1]} · {MODELO}" if v else "ElevenLabs"


def sintetizar(texto, rapidez=1.0):
    """Texto -> (muestras float32 mono, frecuencia). Guarda en caché para no gastar créditos dos veces."""
    vid = voz_id()[0]
    cfg = _config()
    ajustes = {"stability": cfg.get("stability", 0.45), "similarity_boost": cfg.get("similarity_boost", 0.8),
               "style": cfg.get("style", 0.3), "use_speaker_boost": True, "speed": round(rapidez, 2)}
    clave = hashlib.sha1(json.dumps([vid, MODELO, texto, ajustes], ensure_ascii=False).encode()).hexdigest()
    os.makedirs(CACHE, exist_ok=True)
    mp3 = os.path.join(CACHE, clave + ".mp3")
    if not os.path.exists(mp3):
        audio = _peticion(f"/text-to-speech/{vid}?output_format=mp3_44100_128",
                          {"text": texto, "model_id": MODELO, "voice_settings": ajustes}, timeout=120)
        open(mp3 + ".part", "wb").write(audio); os.replace(mp3 + ".part", mp3)
    fd, wav = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "44100", wav], check=True)
        with wave.open(wav, "rb") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return a, 44100
    finally:
        os.remove(wav)


def _recortar(a, sr, umbral=0.015):
    idx = np.flatnonzero(np.abs(a) > umbral)
    if not len(idx):
        return a[:0]
    return a[max(0, idx[0] - int(0.02 * sr)): min(len(a), idx[-1] + int(0.08 * sr))]


def pista(segmentos, total, sr=44100, sintetizador=None):
    """segmentos: lista de (texto, inicio_s, hueco_s). Devuelve (voz, presencia, avisos), arrays de `total` s.
    `presencia` vale 1 donde se oye la voz y sirve para bajar la música debajo."""
    sint = sintetizador or sintetizar
    n = int(round(sr * total))
    voz = np.zeros(n, np.float32); presencia = np.zeros(n, np.float32); avisos = []
    for k, (txt, st, hueco) in enumerate(segmentos):
        txt = " ".join((txt or "").split())
        if not txt:
            continue
        a, vsr = sint(txt, 1.0); a = _recortar(a, vsr)
        largo = len(a) / vsr
        if largo > hueco:  # habla un poco más rápido para que quepa (una sola vez, para no gastar de más)
            a, vsr = sint(txt, min(MAX_RAPIDEZ, largo / hueco * 1.03)); a = _recortar(a, vsr)
        if vsr != sr and len(a):
            a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * sr / vsr)), np.arange(len(a)), a).astype(np.float32)
        maxn = int(hueco * sr)
        if len(a) > maxn:
            avisos.append(f"frase {k + 1} («{txt[:40]}…»): dura {len(a) / sr:.1f} s y caben {hueco:.1f} s; acórtala")
            a = a[:maxn].copy(); f = min(len(a), int(0.08 * sr)); a[-f:] *= np.linspace(1, 0, f)
        pico = float(np.max(np.abs(a))) if len(a) else 0
        if pico > 0:
            a = a * (0.9 / pico)
        i = int(st * sr); a = a[: max(0, n - i)]
        voz[i:i + len(a)] += a; presencia[i:i + len(a)] = 1
    k = int(0.12 * sr)
    if presencia.any():
        presencia = np.clip(np.convolve(presencia, np.ones(k, np.float32) / k, mode="same") * 1.5, 0, 1)
    return voz, presencia, avisos


def _frase(t):
    """«¿QUÉ TIENES…?» -> «¿Qué tienes…?»"""
    t = " ".join(str(t).split()).lower()
    for i, ch in enumerate(t):
        if ch.isalpha():
            return t[:i] + ch.upper() + t[i + 1:]
    return t


def segmentos(formato, T, voz_json, starts, dur, lang, VOF_REVEAL=2.3):
    """Cuándo suena cada frase. `voz_json` es el campo "voz" del JSON (o None: se lee la pantalla).
    - datos: [gancho, dato1, dato2, dato3, final]
    - vof:   [gancho, [afirmación1, revelación1], [afirmación2, revelación2], [afirmación3, revelación3], final]"""
    if formato == "vof":
        si, no = ("¡Verdadero!", "¡Falso!") if lang == "es" else ("True!", "False!")
        if not voz_json:
            def es_v(x): return x is True or str(x).strip().lower() in ("true", "verdadero", "v", "1", "si", "sí")
            # sin locución escrita: la afirmación tal cual y, en la revelación, solo el veredicto
            voz_json = [_frase(T["hook"][0])] + [[a, si if es_v(ok) else no] for _, a, ok, e in T["facts"]] + [T["outro"][0]]
        seg = [(voz_json[0], starts[0] + 0.05, dur[0] - 0.15)]
        for i in range(3):
            af, rev = voz_json[1 + i]
            seg += [(af, starts[1 + i] + 0.1, VOF_REVEAL - 0.2), (rev, starts[1 + i] + VOF_REVEAL + 0.05, dur[1 + i] - VOF_REVEAL - 0.15)]
        seg.append((voz_json[4], starts[4] + 0.05, dur[4] - 0.3))
        return seg
    if not voz_json:
        voz_json = [_frase(T["hook"][0])] + [f"{a} {b.lower()}, {c}" for _, a, b, c in T["facts"]] + [T["outro"][0]]
    return [(t, starts[i] + (0.05 if i in (0, 4) else 0.1), dur[i] - (0.3 if i == 4 else 0.15)) for i, t in enumerate(voz_json[:5])]


def creditos():
    """(usados, límite, fecha de renovación 'AAAA-MM-DD') de la suscripción de ElevenLabs, o None si no se puede saber."""
    try:
        d = json.loads(_peticion("/user/subscription"))
        import datetime as _dt
        ren = d.get("next_character_count_reset_unix")
        ren = _dt.datetime.utcfromtimestamp(ren).strftime("%Y-%m-%d") if ren else "?"
        return int(d.get("character_count", 0)), int(d.get("character_limit", 0)), ren
    except Exception:
        return None


if __name__ == "__main__" and "--creditos" in sys.argv:
    c = creditos()
    if not c:
        print("creditos: ? (no se ha podido consultar)")
    else:
        usados, limite, ren = c; quedan = max(0, limite - usados)
        pct = 100 * quedan / limite if limite else 0
        print(f"creditos: quedan {quedan} de {limite} caracteres ({pct:.0f} %) · se renuevan el {ren}"
              + (" · AVISO: quedan menos del 20 %" if pct < 20 else ""))

if __name__ == "__main__" and "--check" in sys.argv:
    falta = disponible()
    print("voz: NO (" + falta + ")" if falta else "voz: OK · " + descripcion())
