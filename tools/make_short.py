import sys, os, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

import json
# Contenido: se carga desde un JSON (ver content/2026-10-30_animales.json)
TEXT = None
HOOK_EMOJI = "🤯"
PALETTE_POOL = [((255, 94, 98), (255, 153, 102)), ((72, 52, 212), (0, 168, 255)),
    ((0, 150, 136), (120, 220, 140)), ((140, 80, 40), (240, 170, 70)), ((230, 50, 120), (130, 60, 230)),
    ((20, 120, 200), (90, 220, 230)), ((240, 120, 30), (250, 200, 60)), ((90, 40, 160), (220, 80, 160)),
    ((30, 140, 80), (180, 220, 60)), ((200, 40, 60), (250, 120, 90))]
PALETTES = PALETTE_POOL[:5]
DUR = [2.0, 5.5, 5.5, 5.5, 2.5]  # ~21 s: corto para mejor retención
HIGHLIGHTS = [(255, 255, 140), (140, 255, 220), (255, 200, 120), (200, 230, 255)]
HL = HIGHLIGHTS[0]
BUBBLE_MODE = "bubbles"

def font(sz): return ImageFont.truetype(FONT, sz)

def gradient(c1, c2):
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    t = np.clip(0.75 * y + 0.25 * x, 0, 1)[..., None]
    a = np.array(c1) * (1 - t) + np.array(c2) * t
    return Image.fromarray(a.astype(np.uint8), "RGB")

def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    k = size / max(im.width, im.height)  # cabe en un cuadrado size x size
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def clean(text):
    # Poppins no tiene emojis: se quitan del texto en pantalla
    f = font(40)
    return " ".join("".join(ch for ch in text if ch == " " or f.getmask(ch).getbbox() is not None and ord(ch) < 0x2000 or ch in "¿¡…–—’“”€").split())

def text_layer(text, size, color=(255, 255, 255), maxw=940, stroke=0, box=None):
    text = clean(text)
    f = font(size)
    while True:
        lines = wrap(text, f, maxw)
        if all(f.getlength(l) <= maxw for l in lines): break
        size -= 6; f = font(size)
    lh = int(size * 1.18)
    pad = 40 if box else 10
    w = int(max(f.getlength(l) for l in lines)) + pad * 2
    h = lh * len(lines) + pad * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if box: d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=box)
    for i, l in enumerate(lines):
        lw = f.getlength(l)
        d.text(((w - lw) / 2, pad + i * lh - size * 0.08), l, font=f, fill=color,
               stroke_width=stroke, stroke_fill=(0, 0, 0, 90))
    # soft drop shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").point(lambda a: a * 0.35))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    out.alpha_composite(sh, (12, 16)); out.alpha_composite(im, (4, 4))
    return out

def ease_out_back(t):
    t = min(max(t, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3

def place(frame, layer, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.02: return
    if abs(scale - 1) > 0.01:
        layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.BILINEAR)
    if alpha < 0.99:
        layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda a: int(a * alpha)))
    frame.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def bubbles(frame, t, seed):
    rng = np.random.default_rng(seed)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(14):
        x = rng.uniform(0, W); sp = rng.uniform(40, 120); r = rng.uniform(20, 90)
        y = (rng.uniform(0, H) - sp * t) % (H + 200) - 100
        x += 30 * math.sin(t * rng.uniform(0.5, 1.5) + rng.uniform(0, 6))
        a = int(rng.uniform(18, 40))
        if BUBBLE_MODE == "bubbles": d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))
        elif BUBBLE_MODE == "squares": d.rounded_rectangle((x - r * .7, y - r * .7, x + r * .7, y + r * .7), radius=int(r * .25), fill=(255, 255, 255, a))
        else:
            pts = [(x + r * math.cos(k * math.pi / 5 - math.pi / 2) * (1 if k % 2 == 0 else .45), y + r * math.sin(k * math.pi / 5 - math.pi / 2) * (1 if k % 2 == 0 else .45)) for k in range(10)]
            d.polygon(pts, fill=(255, 255, 255, a))
    frame.alpha_composite(ov)

def progress(frame, gt, total):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle((60, 90, W - 60, 104), radius=7, fill=(255, 255, 255, 70))
    d.rounded_rectangle((60, 90, 60 + max(14, (W - 120) * min(gt / total, 1)), 104), radius=7, fill=(255, 255, 255, 255))
    frame.alpha_composite(ov)

def render(lang, outdir):
    T = TEXT[lang]; total = sum(DUR)
    bgs = [gradient(*p).convert("RGBA") for p in PALETTES]
    files = []; gstart = 0.0
    for si, dur in enumerate(DUR):
        n = int(round(dur * FPS))
        tmp = os.path.join(outdir, f"{lang}_s{si}.tmp.mp4"); fin = tmp.replace(".tmp", "")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        if si == 0:
            L1 = text_layer(T["hook"][0], 120, maxw=900); L2 = text_layer(T["hook"][1], 76, color=(255, 240, 200))
            E = emoji_img(HOOK_EMOJI, 360)
        elif si <= 3:
            em, a, b, c = T["facts"][si - 1]
            E = emoji_img(em, 440)
            badge = text_layer(f"{si}/3", 64, color=(40, 40, 40), box=(255, 255, 255, 235))
            La = text_layer(a, 78); Lb = text_layer(b, 128, color=HL, maxw=960); Lc = text_layer(c, 62, color=(255, 255, 255))
            ya = 1010 + La.height / 2; yb = ya + La.height / 2 + Lb.height / 2 - 10; yc = yb + Lb.height / 2 + Lc.height / 2 + 10
        else:
            L1 = text_layer(T["outro"][0], 88); L2 = text_layer(T["outro"][1], 66, color=(40, 40, 40), box=(255, 255, 255, 240))
            E = emoji_img("🔔", 300)
        for i in range(n):
            t = i / FPS; gt = gstart + t
            fr = bgs[si].copy(); bubbles(fr, gt, si)
            if si == 0:
                place(fr, E, W / 2, 620 + 15 * math.sin(t * 6), ease_out_back(t / 0.3))
                place(fr, L1, W / 2, 1060, ease_out_back((t - 0.05) / 0.4), ease((t - 0.05) / 0.2))
                place(fr, L2, W / 2, 1060 + L1.height / 2 + L2.height / 2 + 20 + 60 * (1 - ease((t - 0.5) / 0.3)), 1, ease((t - 0.5) / 0.3))
            elif si <= 3:
                place(fr, badge, W / 2, 300, ease_out_back(t / 0.4))
                place(fr, E, W / 2, 680 + 20 * math.sin(t * 3), ease_out_back((t - 0.1) / 0.6) * (1 + 0.03 * math.sin(t * 5)))
                place(fr, La, W / 2, ya + 50 * (1 - ease((t - 0.35) / 0.3)), 1, ease((t - 0.35) / 0.3))
                place(fr, Lb, W / 2, yb, ease_out_back((t - 0.8) / 0.4), ease((t - 0.8) / 0.2))
                place(fr, Lc, W / 2, yc + 50 * (1 - ease((t - 1.9) / 0.3)), 1, ease((t - 1.9) / 0.3))
            else:
                place(fr, E, W / 2, 640, ease_out_back(t / 0.5) * (1 + 0.08 * math.sin(t * 9) * (t > 0.6)))
                place(fr, L1, W / 2, 1040, ease_out_back((t - 0.15) / 0.4), ease((t - 0.15) / 0.25))
                place(fr, L2, W / 2, 1040 + L1.height / 2 + L2.height / 2 + 30, ease_out_back((t - 0.6) / 0.4) * (1 + 0.04 * math.sin(t * 6)), ease((t - 0.6) / 0.25))
            # fade in/out between scenes
            fade = min(1, (t / 0.15) if si > 0 else 1, (dur - t) / 0.15 if si < 4 else 1)
            if si == 4 and dur - t < 0.35:  # bucle: el final se funde con el fondo del inicio
                fr = Image.blend(fr.convert("RGB"), bgs[0].convert("RGB"), 1 - (dur - t) / 0.35).convert("RGBA")
            img = fr.convert("RGB")
            if fade < 1: img = Image.blend(Image.new("RGB", (W, H), (255, 255, 255)), img, max(fade, 0) * 0.7 + 0.3)
            progress_img = img.convert("RGBA"); progress(progress_img, gt, total)
            p.stdin.write(progress_img.convert("RGB").tobytes())
        p.stdin.close(); assert p.wait() == 0
        os.replace(tmp, fin); files.append(fin); gstart += dur
    return files

def music(path, total, pops, voz=None, presencia=None):
    """Música de fondo; si hay `voz`, la mezcla encima y baja la música mientras se habla."""
    sr = 44100; n = int(sr * total); t = np.arange(n) / sr
    bpm = 116; beat = 60 / bpm
    out = np.zeros(n)
    prog = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    bar = beat * 4
    for k in range(int(total / beat) + 1):
        st = k * beat; idx = int(st * sr)
        if idx >= n: break
        chord = prog[int(st / bar) % 4]
        L = int(beat * sr); seg = np.arange(min(L, n - idx)) / sr
        env = np.exp(-seg * 3.0)
        for f in chord:
            out[idx:idx + len(seg)] += 0.06 * env * (np.sin(2 * np.pi * f * seg) + 0.3 * np.sin(4 * np.pi * f * seg))
        # bass
        out[idx:idx + len(seg)] += 0.12 * np.exp(-seg * 4) * np.sin(2 * np.pi * chord[0] / 2 * seg)
        # kick
        kl = min(int(0.15 * sr), n - idx); ks = np.arange(kl) / sr
        out[idx:idx + kl] += 0.35 * np.exp(-ks * 25) * np.sin(2 * np.pi * (110 * np.exp(-ks * 20) + 45) * ks)
        # hat on offbeat
        hi = int((st + beat / 2) * sr); hl = min(int(0.04 * sr), n - hi)
        if hl > 0: out[hi:hi + hl] += 0.05 * np.random.default_rng(k).standard_normal(hl) * np.exp(-np.arange(hl) / sr * 90)
    for pt in pops:
        i = int(pt * sr); l = min(int(0.12 * sr), n - i)
        if l > 0:
            s = np.arange(l) / sr
            out[i:i + l] += 0.25 * np.exp(-s * 30) * np.sin(2 * np.pi * (500 + 900 * s * 8) * s)
    fade = np.minimum(1, np.minimum(t / 0.3, (total - t) / 0.8))
    out = np.tanh(out * fade * 1.4) * 0.8
    if voz is not None:
        m = min(n, len(voz))
        out[:m] *= 1 - 0.7 * presencia[:m]          # la música baja al 30 % bajo la voz
        out[:m] += 0.95 * voz[:m]
        out = np.tanh(out * 1.1) / np.tanh(1.1)      # limitador suave
        out *= 0.92 / max(1e-6, float(np.max(np.abs(out))))
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

if __name__ == "__main__":
    # uso: python3 make_short.py contenido.json idioma(es|en) carpeta_salida salida.mp4
    cfile, lang, outdir, final = sys.argv[1:5]; os.makedirs(outdir, exist_ok=True)
    C = json.load(open(cfile, encoding="utf-8"))
    HOOK_EMOJI = C.get("hook_emoji", "🤯")
    L = C[lang]
    TEXT = {lang: {"hook": tuple(L["hook"]), "facts": [tuple(f) for f in L["facts"]], "outro": tuple(L["outro"])}}
    seed = sum(ord(ch) for ch in os.path.basename(cfile))
    rng = np.random.default_rng(seed); idx = rng.permutation(len(PALETTE_POOL))[:5]
    PALETTES = C.get("palettes") or [PALETTE_POOL[i] for i in idx]
    PALETTES[4] = PALETTES[0]  # el final tiene el color del inicio (bucle)
    HL = HIGHLIGHTS[seed % len(HIGHLIGHTS)]
    BUBBLE_MODE = ["bubbles", "squares", "stars"][(seed // 7) % 3]
    files = render(lang, outdir)
    lst = os.path.join(outdir, f"{lang}_list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    starts = np.cumsum([0] + DUR[:-1])
    pops = [0.0, 0.1] + [s + o for s in starts[1:4] for o in (0.1, 0.8)] + [starts[4] + 0.15, starts[4] + 0.6]
    # Voz en off (Piper). El JSON puede traer "voz": [gancho, dato1, dato2, dato3, final] por idioma;
    # si no, se lee el texto de pantalla. Sin Piper instalado, el Short sale solo con música.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import voz as V
    voz = presencia = None
    falta = V.disponible(lang)
    if falta:
        print(f"voz: NO ({falta})")
    else:
        textos = L.get("voz") or V.textos_desde_pantalla(TEXT[lang])
        voz, presencia, avisos = V.pista(textos, list(starts), DUR, lang, sum(DUR))
        print(f"voz: sí, {V.descripcion(lang)}" + ("" if L.get("voz") else " (leída del texto en pantalla)"))
        for a in avisos: print("voz: AVISO", a)
    wav = os.path.join(outdir, f"{lang}_music.wav"); music(wav, sum(DUR), pops, voz, presencia)
    silent = os.path.join(outdir, f"{lang}_silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    tmpf = final[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", tmpf], check=True)
    os.replace(tmpf, final)
    print(final)
