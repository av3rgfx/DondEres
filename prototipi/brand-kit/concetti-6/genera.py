"""Giro 11: tre versioni migliorate della R · Arco lungo (decisione 394).
La gamba è un tratto di spessore controllato lungo una curva di Bézier: il contorno si ottiene spostando la linea
di mezzo lungo la normale e si ridisegna con curve morbide (Catmull-Rom convertite in Bézier cubiche).
Uso: python3 genera.py  (scrive gli SVG e dati.json nella stessa cartella)
"""
import json, math, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
import importlib.util


def carica(nome, percorso):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    spec.loader.exec_module(m)
    return m


kit = carica("genera", os.path.join(OUT, "..", "kit", "genera.py"))      # c5 importa «genera»: è il kit
c5 = carica("c5", os.path.join(OUT, "..", "concetti-5", "genera.py"))
f, rect = kit.f, kit.rect

CAP, BASE = kit.CAP, kit.BASE


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    pt = [u**3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t**3 * p3[i] for i in (0, 1)]
    dt = [3 * u * u * (p1[i] - p0[i]) + 6 * u * t * (p2[i] - p1[i]) + 3 * t * t * (p3[i] - p2[i]) for i in (0, 1)]
    return pt, dt


def smooth(pts):
    """Curva morbida che passa per i punti (Catmull-Rom → Bézier cubiche)."""
    d = f"L{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def tratto(segs, w, n=9):
    """segs: lista di Bézier (p0,p1,p2,p3); w(t globale) = mezzo spessore. Contorno chiuso del tratto."""
    left, right = [], []
    N = len(segs)
    for si, sg in enumerate(segs):
        for k in range(n + 1):
            if si > 0 and k == 0:
                continue
            t = k / n
            (x, y), (dx, dy) = bez(*sg, t)
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            hw = w((si + t) / N)
            left.append((x + nx * hw, y + ny * hw))
            right.append((x - nx * hw, y - ny * hw))
    d = f"M{f(left[0][0])} {f(left[0][1])} " + smooth(left)[len(f'L{f(left[0][0])} {f(left[0][1])}'):]
    rr = right[::-1]
    d += f" L{f(rr[0][0])} {f(rr[0][1])}" + smooth(rr)[len(f'L{f(rr[0][0])} {f(rr[0][1])}'):] + " Z"
    return d


def R(x0, s, top, base, variante):
    H = base - top
    bowl, yb, right = c5.occhiello(x0, s, top, H)
    stem = rect(x0, top, s, H)
    y0 = yb - s / 2                        # la gamba parte dalla barra bassa dell'occhiello
    xs = x0 + s * 0.5
    if variante == "pulito":
        # A · uniforme: stesso spessore dell'asta dall'attacco alla base, piede piatto sulla linea di base
        xe = x0 + 0.95 * H
        p0, p3 = (xs, y0), (xe - s / 2, base)
        seg = [(p0, (p0[0] + 0.62 * (p3[0] - p0[0]), p0[1]), (p3[0], p3[1] - 0.45 * (p3[1] - p0[1])), p3)]
        leg = tratto(seg, lambda t: s / 2)
        w = xe
    elif variante == "affusolato":
        # B · affusolato: parte pieno, si assottiglia e si posa sulla linea di base scivolando in avanti
        xe = x0 + 1.06 * H
        he = s / 2 * 0.45
        p0, p3 = (xs, y0), (xe, base - he)
        seg = [(p0, (p0[0] + 0.55 * (p3[0] - p0[0]), p0[1]), (p3[0] - 0.40 * (p3[0] - p0[0]), p3[1]), p3)]
        leg = tratto(seg, lambda t: s / 2 * (1 - 0.55 * t ** 1.3))
        w = xe
    else:
        # C · slitta: l'arco scende, corre basso e la punta risale come il pattino di una slitta
        xe = x0 + 1.06 * H
        ym = base - s * 0.42
        pm = (x0 + 0.70 * H, ym)
        p0 = (xs, y0)
        seg1 = (p0, (p0[0] + 0.45 * (pm[0] - p0[0]), p0[1]), (pm[0] - 0.42 * (pm[0] - p0[0]), ym), pm)
        p4 = (xe - s * 0.3, ym - 0.13 * H)
        a = math.radians(30)                       # la punta risale a 30 gradi: taglio pulito
        seg2 = (pm, (pm[0] + 0.55 * (p4[0] - pm[0]), ym), (p4[0] - 0.09 * H * math.cos(a), p4[1] + 0.09 * H * math.sin(a)), p4)
        leg = tratto([seg1, seg2], lambda t: s / 2 * (1 - 0.12 * t), n=8)
        w = xe
    return [stem, bowl, leg], w - x0


VAR = ["pulito", "affusolato", "slitta"]


def nome(v, x0=20, s=26):
    paths, x = [], x0
    rp, rw = R(x, s, CAP, BASE, v)
    paths += rp
    x += rw + 8
    for fn, gap in ((lambda X: kit.i(X, kit.T, "tondo"), 0), (kit.p, 14), (kit.o, 12)):
        x += gap
        pp, w = fn(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


def simbolo(v):
    H = 196
    paths, w = R(0, 0.22 * H, 0, H, v)
    sc = min(1, 224 / w)
    tx, ty = (256 - w * sc) / 2 - (4 if v == "slitta" else 0), (256 - H * sc) / 2
    return f'<g transform="translate({f(tx)} {f(ty)}) scale({f(sc)})">', paths


if __name__ == "__main__":
    data = {"sym": {}, "nome": {}}
    for v in VAR:
        g, sp = simbolo(v)
        data["sym"][v] = {"g": g, "d": sp}
        body = "".join(f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in sp)
        open(os.path.join(OUT, f"{v}-simbolo.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" '
            f'aria-labelledby="t"><title id="t">Ripo, R arco lungo, {v}</title>{g}{body}</g></svg>\n')
        pp, w = nome(v)
        data["nome"][v] = {"vb": f"0 0 {w} 256", "d": pp}
        open(os.path.join(OUT, f"{v}-nome.svg"), "w").write(kit.svg(pp, w, title=f"Ripo, nome, {v}"))
    # la versione del giro 10, per il confronto
    g, sp = c5.simbolo("lungo")
    data["sym"]["giro10"] = {"g": g, "d": sp}
    pp, w = c5.nome("lungo")
    data["nome"]["giro10"] = {"vb": f"0 0 {w} 256", "d": pp}
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti in", OUT)
