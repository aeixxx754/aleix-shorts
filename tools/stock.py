"""Clips de vídeo reales de fondo (Pexels, gratis y con licencia libre) para los Shorts y los vídeos largos.

La clave de Pexels NO está en el código: es un «secreto de red» del entorno de la tarea (host api.pexels.com,
cabecera Authorization, sin prefijo). Los vídeos se descargan de videos.pexels.com (tiene que estar en los dominios
permitidos del entorno). Si algo falla, `disponible()` dice por qué y el vídeo sale con el fondo de color de siempre.

Uso rápido:  python3 tools/stock.py --check   ·   python3 tools/stock.py "pulpo bajo el agua"
"""
import os, sys, json, hashlib, subprocess, urllib.request, urllib.parse, urllib.error
import numpy as np
from PIL import Image

API = "https://api.pexels.com/videos/search"
CACHE = os.environ.get("ALEIX_STOCK_CACHE", os.path.expanduser("~/.cache/aleix-stock"))
_estado = {}


def _get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "aleix-shorts/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def buscar(query, orientacion="portrait", n=15):
    q = urllib.parse.urlencode({"query": query, "orientation": orientacion, "per_page": n, "size": "medium"})
    return json.loads(_get(f"{API}?{q}")).get("videos", [])


def disponible():
    """None si se pueden usar clips; si no, el motivo."""
    if os.environ.get("ALEIX_STOCK", "1") == "0":
        return "clips desactivados con ALEIX_STOCK=0"
    if "ok" in _estado:
        return _estado["ok"]
    try:
        buscar("nature", n=1); _estado["ok"] = None
    except urllib.error.HTTPError as e:
        _estado["ok"] = {401: "Pexels rechaza la clave (revisa el secreto de api.pexels.com: cabecera Authorization, sin prefijo)",
                         403: "Pexels deniega el acceso"}.get(e.code, f"Pexels respondió {e.code}")
    except Exception as e:
        _estado["ok"] = f"no se llega a api.pexels.com: falta el secreto de red en el entorno ({type(e).__name__})"
    return _estado["ok"]


def _elige_fichero(v, vertical):
    fs = [f for f in v.get("video_files", []) if f.get("link") and f.get("width") and f.get("height")]
    fs = [f for f in fs if (f["height"] > f["width"]) == vertical] or fs
    objetivo = 1920 if vertical else 1080
    fs.sort(key=lambda f: (abs((f["height"] if vertical else f["height"]) - objetivo), -f["width"]))
    return fs[0] if fs else None


def clip(query, minimo=5.0, vertical=True, evitar=()):
    """Descarga (con caché) el mejor clip para `query`. Devuelve (ruta, id_pexels, autor) o None.
    Prefiere clips sin personas (añade palabras de naturaleza/objeto a la búsqueda desde el plan)."""
    if disponible():
        return None
    try:
        vids = buscar(query, "portrait" if vertical else "landscape")
    except Exception:
        return None
    vids = [v for v in vids if v.get("duration", 0) >= minimo and v.get("id") not in evitar]
    for v in vids:
        f = _elige_fichero(v, vertical)
        if not f:
            continue
        os.makedirs(CACHE, exist_ok=True)
        ruta = os.path.join(CACHE, f"{v['id']}_{f.get('width')}x{f.get('height')}.mp4")
        if not os.path.exists(ruta):
            try:
                data = _get(f["link"], timeout=120)
            except Exception:
                continue   # p. ej. videos.pexels.com no está en los dominios permitidos
            open(ruta + ".part", "wb").write(data); os.replace(ruta + ".part", ruta)
        return ruta, v["id"], (v.get("user") or {}).get("name", "")
    return None


def fotogramas(ruta, dur, W, H, fps, tinte=(30, 27, 75), oscuro=0.5, inicio=0.4):
    """Generador de fotogramas RGBA (W×H) del clip, recortado a pantalla completa, más lento si es corto,
    oscurecido y teñido con el color del vídeo para que el texto se lea siempre."""
    n = int(round(dur * fps))
    try:
        info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", ruta],
                                         capture_output=True, text=True).stdout)
        largo = float(info["format"]["duration"])
    except Exception:
        largo = dur + inicio
    lento = max(1.0, (dur + inicio) / max(largo, 0.1))        # si el clip es corto, se ralentiza en vez de cortarse
    vf = (f"setpts={lento:.3f}*PTS,fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"eq=saturation=1.08")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{min(inicio, max(0, largo - 1)):.2f}", "-i", ruta,
                          "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    # capa para legibilidad: tinte de marca + degradado más oscuro arriba y abajo
    y = np.linspace(0, 1, H)[:, None]
    a = (oscuro + 0.22 * (np.abs(y - 0.5) * 2) ** 2)[:, :, None]
    capa = np.zeros((H, W, 3), np.float32) + np.array(tinte, np.float32) * 0.55
    ultimo = None; tam = W * H * 3
    for _ in range(n):
        buf = p.stdout.read(tam)
        if len(buf) == tam:
            ultimo = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        if ultimo is None:
            ultimo = np.zeros((H, W, 3), np.float32) + np.array(tinte, np.float32)
        out = ultimo * (1 - a) + capa * a
        yield Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGB").convert("RGBA")
    p.stdout.close(); p.wait()


if __name__ == "__main__":
    if "--check" in sys.argv:
        falta = disponible()
        print("clips: NO (" + falta + ")" if falta else "clips: OK · Pexels")
    elif len(sys.argv) > 1:
        print(clip(" ".join(sys.argv[1:])))
