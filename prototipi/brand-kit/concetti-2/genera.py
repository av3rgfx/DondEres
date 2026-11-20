"""Concetti del giro 3 per Varko: lettere nuove a spessore variabile e tre simboli
(cartello di corsia, corsia, porta di carico). Decisioni 369-373.

Lettere costruite a mano come forme piene: altezza 256, linea di base y=200, altezza della x 96 (y 104),
maiuscola 144 (y 56). Lo spessore t dell'asta cambia il peso di tutto il nome.
Uso: python3 genera.py  (scrive i file nella stessa cartella)
"""
import math, os, json

OUT = os.path.dirname(os.path.abspath(__file__))
BASE, XH, CAP = 200, 104, 56
R2 = math.sqrt(2)
PESI = {"medio": 22, "leggero": 16}     # spessore dell'asta delle minuscole


def f(v):
    return f"{round(v, 2):g}"


def poly(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def ring(cx, cy, ro, ri):
    return (f"M{f(cx-ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx+ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx-ro)} {f(cy)} Z "
            f"M{f(cx-ri)} {f(cy)} A{f(ri)} {f(ri)} 0 1 0 {f(cx+ri)} {f(cy)} A{f(ri)} {f(ri)} 0 1 0 {f(cx-ri)} {f(cy)} Z")


# ---------------- lettere ----------------
def V_pts(t):
    """Contorno della V: metà sinistra e destra come una figura sola."""
    s = math.tan(math.radians(15))    # bracci a 75 gradi
    h = t / math.cos(math.radians(15))  # spessore orizzontale del braccio
    fl = 1.5 * h                      # larghezza del fondo piatto
    W = 2 * (BASE - CAP) * s + fl
    c = W / 2
    yi = CAP + (c - h) / s            # vertice interno
    return [(0, CAP), (h, CAP), (c, yi), (W - h, CAP), (W, CAP), (c + fl / 2, BASE), (c - fl / 2, BASE)], W, s, h, yi


def V(x, t, ripiani=0, gap=0):
    pts, W, s, h, yi = V_pts(t)
    if not ripiani:
        return [poly([(px + x, py) for px, py in pts])], W
    # V a ripiani: i due bracci tagliati da fessure orizzontali (concetto «Corsia»)
    c = W / 2
    out_l = lambda y: (y - CAP) * s
    in_l = lambda y: min(c, h + (y - CAP) * s)
    H = BASE - CAP
    seg = (H - ripiani * gap) / (ripiani + 1)
    paths = []
    for i in range(ripiani + 1):
        a = CAP + i * (seg + gap)
        b = a + seg
        if b <= yi or a >= yi:
            if a >= yi:   # sotto il vertice: un pezzo unico al centro
                paths.append(poly([(x + out_l(a), a), (x + W - out_l(a), a), (x + W - out_l(b), b), (x + out_l(b), b)]))
                continue
            for side in (0, 1):
                pts2 = [(out_l(a), a), (in_l(a), a), (in_l(b), b), (out_l(b), b)]
                if side:
                    pts2 = [(W - px, py) for px, py in pts2]
                paths.append(poly([(px + x, py) for px, py in pts2]))
        else:             # il pezzo contiene il vertice: forma unica a V
            paths.append(poly([(x + out_l(a), a), (x + in_l(a), a), (x + c, yi), (x + W - in_l(a), a),
                               (x + W - out_l(a), a), (x + W - out_l(b), b), (x + out_l(b), b)]))
    return paths, W


def a(x, t):
    ro = 49
    return [ring(x + ro, 152, ro, ro - t), rect(x + 2 * ro - t, XH, t + 1, BASE - XH)], 2 * ro


def r(x, t):
    ri = t * 0.7
    w = 40 + t
    d = (f"M{f(x)} {BASE} L{f(x)} {XH} L{f(x+w)} {XH} L{f(x+w)} {f(XH+t)} L{f(x+t+ri)} {f(XH+t)} "
         f"A{f(ri)} {f(ri)} 0 0 0 {f(x+t)} {f(XH+t+ri)} L{f(x+t)} {BASE} Z")
    return [d], w


def k(x, t):
    """k geometrica: asta e una «<» a 45 gradi che la tocca a metà della x."""
    d2 = t * R2 / 2
    X0 = x + t + 48                         # asse del braccio in alto
    yin = XH + 48 - d2                      # dove il bordo interno tocca l'asta
    chev = [(X0 - d2, XH), (X0 + d2, XH), (x + t + d2, 152), (X0 + d2, BASE), (X0 - d2, BASE),
            (x + t, 304 - yin), (x + t - 3, 304 - yin), (x + t - 3, yin), (x + t, yin)]
    return [rect(x, CAP, t, BASE - CAP), poly(chev)], X0 + d2 - x


def o(x, t):
    return [ring(x + 49, 152, 49, 49 - t)], 98


def word(t, x0=24, vfn=None):
    vfn = vfn or (lambda x: V(x, t))
    paths, x = [], x0
    gaps = {"medio": (-8, 12, 12, 9), "leggero": (-6, 13, 13, 10)}
    g = gaps["medio"] if t >= 20 else gaps["leggero"]
    for fn, gp in ((vfn, 0), (lambda X: a(X, t), g[0]), (lambda X: r(X, t), g[1]), (lambda X: k(X, t), g[2]),
                   (lambda X: o(X, t), g[3])):
        x += gp
        p, w = fn(x)
        paths += p
        x += w
    return paths, math.ceil(x + x0)


# ---------------- simboli 256 x 256 ----------------
def tr(paths_pts, sc, tx, ty):
    return [poly([(px * sc + tx, py * sc + ty) for px, py in pts]) for pts in paths_pts]


def sym_cartello(t):
    """Targa quadrata arrotondata con la V del nome ritagliata e i due fori per appenderla,
    come i cartelli sopra le corsie."""
    o0, o1, rr = 20, 236, 46
    plate = (f"M{o0+rr} {o0} L{o1-rr} {o0} A{rr} {rr} 0 0 1 {o1} {o0+rr} L{o1} {o1-rr} A{rr} {rr} 0 0 1 {o1-rr} {o1} "
             f"L{o0+rr} {o1} A{rr} {rr} 0 0 1 {o0} {o1-rr} L{o0} {o0+rr} A{rr} {rr} 0 0 1 {o0+rr} {o0} Z")
    pts, W, *_ = V_pts(t * 1.7)
    sc = 0.88
    tx = 128 - W * sc / 2
    ty = 140 - (CAP + BASE) / 2 * sc
    hole = poly([(px * sc + tx, py * sc + ty) for px, py in pts])
    foro = " ".join(f"M{cx-8} 50 A8 8 0 1 0 {cx+8} 50 A8 8 0 1 0 {cx-8} 50 Z" for cx in (64, 192))
    return [plate + " " + hole + " " + foro]


def sym_corsia(t):
    """La V del nome a ripiani, ingrandita: due scaffali che si incontrano in fondo alla corsia."""
    paths, W = V(0, t * 1.45, ripiani=3, gap=9)
    sc = 1.45
    tx = 128 - W * sc / 2
    ty = 128 - (CAP + BASE) / 2 * sc - 3
    out = []
    for d in paths:
        pts = [tuple(map(float, p.split())) for p in d.replace("M", "").replace(" Z", "").split(" L")]
        out.append(poly([(px * sc + tx, py * sc + ty) for px, py in pts]))
    return out


def sym_porta():
    """Porta di carico: architrave, due montanti e la serranda alzata a metà; sotto, il passaggio."""
    return [rect(32, 36, 192, 34), rect(32, 70, 34, 150), rect(190, 70, 34, 150),
            rect(80, 84, 96, 20), rect(80, 114, 96, 20), rect(80, 144, 96, 20)]


def svg(paths, vb, title):
    w = vb.split()[2]
    body = "\n".join(f'  <path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="256" role="img" '
            f'aria-labelledby="t">\n  <title id="t">{title}</title>\n{body}\n</svg>\n')


def lockup(sym, wp, ww, title):
    ss, ws, pad, gap = 0.75, 0.8, 16, 36
    tx = pad + 256 * ss + gap
    total = math.ceil(tx + ww * ws + pad)
    g = lambda paths, s, x, y: f'<g transform="translate({f(x)} {f(y)}) scale({s})">' + "".join(
        f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in paths) + "</g>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total} 256" width="{total}" height="256" role="img" '
            f'aria-labelledby="t">\n  <title id="t">{title}</title>\n  {g(sym, ss, pad, 32)}\n  {g(wp, ws, tx, 128 - 128 * ws)}\n</svg>\n')


def build():
    data = {"sym": {}, "word": {}, "lock": {}}
    for peso, t in PESI.items():
        wp, ww = word(t)
        wc, wcw = word(t, vfn=lambda x: V(x, t, ripiani=2, gap=6))
        data["word"][peso] = {"vb": f"0 0 {f(ww)} 256", "d": wp}
        data["word"][peso + "-corsia"] = {"vb": f"0 0 {f(wcw)} 256", "d": wc}
        data["sym"]["cartello-" + peso] = {"vb": "0 0 256 256", "d": sym_cartello(t)}
        data["sym"]["corsia-" + peso] = {"vb": "0 0 256 256", "d": sym_corsia(t)}
    data["sym"]["porta"] = {"vb": "0 0 256 256", "d": sym_porta()}
    return data


if __name__ == "__main__":
    t = PESI["medio"]
    wp, ww = word(t)
    wc, wcw = word(t, vfn=lambda x: V(x, t, ripiani=2, gap=6))
    files = {
        "nome-medio.svg": svg(wp, f"0 0 {f(ww)} 256", "Varko, nome, peso medio"),
        "nome-leggero.svg": svg(word(16)[0], f"0 0 {f(word(16)[1])} 256", "Varko, nome, peso leggero"),
        "a-simbolo.svg": svg(sym_cartello(t), "0 0 256 256", "Varko, concetto A: cartello di corsia"),
        "a-lockup.svg": lockup(sym_cartello(t), wp, ww, "Varko, concetto A, simbolo e nome"),
        "b-simbolo.svg": svg(sym_corsia(t), "0 0 256 256", "Varko, concetto B: corsia"),
        "b-lockup.svg": svg(wc, f"0 0 {f(wcw)} 256", "Varko, concetto B: nome con la V a ripiani"),
        "c-simbolo.svg": svg(sym_porta(), "0 0 256 256", "Varko, concetto C: porta di carico"),
        "c-lockup.svg": lockup(sym_porta(), wp, ww, "Varko, concetto C, simbolo e nome"),
    }
    for n, s in files.items():
        open(os.path.join(OUT, n), "w").write(s)
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(build(), separators=(",", ":")))
    print("scritti", len(files), "file e dati.json in", OUT)
