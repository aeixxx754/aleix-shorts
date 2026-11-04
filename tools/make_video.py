"""Vídeo largo horizontal (1920x1080) del canal: un «top 10» de datos curiosos con voz de ElevenLabs.

Uso:  python3 tools/make_video.py content/<archivo>.json <carpeta_trabajo> <salida.mp4>
Crea también <salida>.jpg (miniatura 1280x720) y <salida>.capitulos.txt (capítulos para la descripción).

Formato del JSON: ver tools/ejemplo_largo.json. Los puntos se cuentan hacia atrás (#10 … #1) para que la gente
se quede hasta el final. Cada tramo dura lo que dura su locución (+ un pequeño margen); sin voz, duraciones fijas.
"""
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import make_short as MS          # reutiliza fuentes, emojis, textos y la música

W, H, FPS = 1920, 1080, 25
PALETAS = [((30, 27, 75), (88, 60, 200)), ((14, 80, 120), (20, 160, 170)), ((120, 40, 90), (220, 80, 120)),
           ((20, 90, 60), (60, 170, 100)), ((140, 70, 20), (230, 150, 50)), ((60, 30, 120), (160, 60, 200))]
MARGEN = 1.4                     # segundos de aire tras cada locución
SIN_VOZ = {"intro": 7.0, "item": 16.0, "outro": 9.0}


def gradiente(c1, c2):
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    t = np.clip(0.55 * x + 0.45 * y, 0, 1)[..., None]
    a = np.array(c1) * (1 - t) + np.array(c2) * t
    return Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")


def texto(t, size, color=(255, 255, 255), maxw=1000, box=None, minw=0):
    return MS.text_layer(t, size, color=color, maxw=maxw, box=box, minw=minw)


def barra(fr, frac, n, k):
    ov = Image.new("RGBA", (W - 140, 20), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle((10, 4, W - 150, 16), radius=6, fill=(255, 255, 255, 60))
    d.rounded_rectangle((10, 4, 10 + max(12, (W - 160) * min(frac, 1)), 16), radius=6, fill=(255, 255, 255, 230))
    fr.alpha_composite(ov, (70, H - 64))


def tramos(C):
    """Lista de tramos: (tipo, datos, texto_voz)."""
    E = C["es"]
    out = [("intro", E["intro"], E["intro"].get("voz", ""))]
    n = len(E["items"])
    for i, it in enumerate(E["items"]):
        out.append(("item", dict(it, numero=n - i), it.get("voz", "")))
    out.append(("outro", E["outro"], E["outro"].get("voz", "")))
    return out


def render_tramo(tipo, D, dur, pal, idx, total_prev, total, outdir, n_items):
    n = int(round(dur * FPS)); bg = gradiente(*pal)
    tmp = os.path.join(outdir, f"largo_{idx:02d}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    if tipo == "intro":
        E = MS.emoji_img(D.get("emoji", "🤯"), 340)
        L1 = texto(D["texto"][0], 104, maxw=1500); L2 = texto(D["texto"][1], 60, color=(255, 240, 200), maxw=1400)
        PILL = texto(f"TOP {n_items}", 54, color=(30, 27, 75), box=(255, 214, 0, 250))
    elif tipo == "item":
        E = MS.emoji_img(D["emoji"], 520)
        NUM = texto(f"#{D['numero']}", 120, color=(30, 27, 75), box=(255, 214, 0, 250), minw=230)
        T = texto(D["titulo"], 100, maxw=1000); X = texto(D["texto"], 62, color=(255, 245, 225), maxw=980)
    else:
        E = MS.emoji_img("🔔", 300)
        L1 = texto(D["texto"][0], 92, maxw=1500); L2 = texto(D["texto"][1], 56, color=(40, 40, 40), box=(255, 255, 255, 240))
        SUB = texto("SUSCRÍBETE para más datos curiosos", 56, color=(255, 255, 255), box=(214, 40, 40, 245))
    estatico = None
    for i in range(n):
        t = i / FPS
        if estatico is not None:
            fr = estatico.copy()
        else:
            fr = bg.copy()
            if tipo == "intro":
                MS.place(fr, PILL, W / 2, 90, MS.ease_out_back(t / 0.3))
                MS.place(fr, L1, W / 2, 640, 1 + 0.02 * math.sin(t * 5))
                MS.place(fr, L2, W / 2, 640 + L1.height / 2 + L2.height / 2 + 20, 1, MS.ease((t - 0.3) / 0.3))
            elif tipo == "item":
                MS.place(fr, NUM, 1240, 260, MS.ease_out_back(t / 0.35))
                yt = 380 + T.height / 2
                MS.place(fr, T, 1240, yt + 40 * (1 - MS.ease((t - 0.2) / 0.3)), 1, MS.ease((t - 0.2) / 0.3))
                MS.place(fr, X, 1240, yt + T.height / 2 + X.height / 2 + 30 + 40 * (1 - MS.ease((t - 0.7) / 0.3)), 1, MS.ease((t - 0.7) / 0.3))
            else:
                MS.place(fr, L1, W / 2, 460, MS.ease_out_back(t / 0.3))
                MS.place(fr, L2, W / 2, 460 + L1.height / 2 + L2.height / 2 + 24, MS.ease_out_back((t - 0.3) / 0.3))
                MS.place(fr, SUB, W / 2, 460 + L1.height / 2 + L2.height + 90 + SUB.height / 2, MS.ease_out_back((t - 0.6) / 0.3))
            if t > 1.6:   # a partir de aquí el texto ya no se mueve: se reutiliza
                estatico = fr.copy()
        barra(fr, (total_prev + t) / total, n_items, idx)
        # el emoji siempre se mueve un poco
        if tipo == "intro":
            MS.place(fr, E, W / 2, 340 + 12 * math.sin(t * 2.2), 0.7 + 0.3 * MS.ease_out_back(t / 0.3))
        elif tipo == "item":
            MS.place(fr, E, 480, 520 + 18 * math.sin(t * 1.8), MS.ease_out_back((t - 0.05) / 0.4) * (1 + 0.02 * math.sin(t * 3)))
        else:
            MS.place(fr, E, W / 2, 230 + 10 * math.sin(t * 6) * (t > 0.5), MS.ease_out_back(t / 0.4))
        img = fr.convert("RGB")
        f = min(1, t / 0.25, (dur - t) / 0.25) if tipo != "intro" else min(1, (dur - t) / 0.25)
        if f < 1:
            img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, max(f, 0))
        p.stdin.write(img.tobytes())
    p.stdin.close(); assert p.wait() == 0
    return tmp


def miniatura(C, path):
    E = C["es"]; T = (E.get("miniatura") or E["intro"]["texto"][0]).upper()
    w, h = 1280, 720
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(0, 1, w)[None, :]
    t = np.clip(0.6 * x + 0.4 * y, 0, 1)[..., None]
    c1, c2 = (255, 94, 98), (130, 60, 230)
    im = Image.fromarray((np.array(c1) * (1 - t) + np.array(c2) * t).astype(np.uint8)).convert("RGBA")
    em = MS.emoji_img(C.get("hook_emoji", "🤯"), 460)
    im.alpha_composite(em, (w - em.width - 40, (h - em.height) // 2 + 20))
    f = MS.font(96); lines = MS.wrap(T, f, 720)
    while len(lines) > 3 or any(f.getlength(l) > 720 for l in lines):
        f = MS.font(f.size - 8); lines = MS.wrap(T, f, 720)
    d = ImageDraw.Draw(im); yy = (h - len(lines) * f.size * 1.12) / 2
    for l in lines:
        d.text((60, yy), l, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(20, 20, 40)); yy += f.size * 1.12
    pill = MS.text_layer(f"TOP {len(E['items'])}", 54, color=(30, 27, 75), box=(255, 214, 0, 255))
    im.alpha_composite(pill, (50, 30))
    im.convert("RGB").save(path, quality=92)


def mmss(s):
    s = int(s); return f"{s // 60}:{s % 60:02d}"


if __name__ == "__main__":
    cfile, outdir, final = sys.argv[1:4]; os.makedirs(outdir, exist_ok=True)
    C = json.load(open(cfile, encoding="utf-8"))
    TR = tramos(C); n_items = len(C["es"]["items"])
    V = None
    if os.environ.get("ALEIX_VOZ", "1") != "0":
        import voz as V
        falta = V.disponible("es")
        if falta: print(f"voz: NO ({falta})"); V = None
    # 1) duración de cada tramo según su locución
    durs = []
    for tipo, D, vz in TR:
        d = SIN_VOZ[tipo]
        if V and vz.strip():
            a, sr = V.sintetizar(" ".join(vz.split()), 1.0); a = V._recortar(a, sr)
            d = max(d * 0.4, len(a) / sr + MARGEN)
        durs.append(round(d * FPS) / FPS)
    total = sum(durs); starts = list(np.cumsum([0] + durs[:-1]))
    print(f"duración: {mmss(total)} ({len(TR)} tramos)" + (f" · voz: sí · {V.descripcion()}" if V else " · sin voz"))
    # 2) vídeo
    files = []
    for k, ((tipo, D, vz), d) in enumerate(zip(TR, durs)):
        files.append(render_tramo(tipo, D, d, PALETAS[k % len(PALETAS)], k, starts[k], total, outdir, n_items))
    lst = os.path.join(outdir, "largo_list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    silent = os.path.join(outdir, "largo_silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    # 3) audio: música suave + voz
    voz = pres = None
    if V:
        seg = [(vz, st + 0.35, d - 0.5) for (tipo, D, vz), st, d in zip(TR, starts, durs) if vz.strip()]
        voz, pres, avisos = V.pista(seg, total)
        for a in avisos: print("voz: AVISO", a)
    wav = os.path.join(outdir, "largo_music.wav")
    MS.music(wav, total, [s for s in starts], voz, pres)
    tmpf = final[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmpf], check=True)
    os.replace(tmpf, final)
    # 4) miniatura y capítulos
    miniatura(C, final[:-4] + ".jpg")
    caps = [f"{mmss(starts[0])} Intro"] + [f"{mmss(st)} #{D['numero']} {D['titulo']}" for (tipo, D, vz), st in zip(TR, starts) if tipo == "item"] \
        + [f"{mmss(starts[-1])} Final"]
    open(final[:-4] + ".capitulos.txt", "w", encoding="utf-8").write("\n".join(caps) + "\n")
    print(final)
