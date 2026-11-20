"""Genera gli SVG dei tre concetti del brand kit di Varko (giro 2).

Lettere costruite a mano come forme piene (niente <text>): altezza 256, linea di base y=200,
altezza della x 96 (y 104), maiuscola 144 (y 56), asta delle minuscole 30.
Uso: python3 genera.py  (scrive i file nella stessa cartella)
"""
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))
BASE, XH, CAP, ST = 200, 104, 56, 30


def poly(pts, dx=0):
    return "M" + " L".join(f"{x+dx:g} {y:g}" for x, y in pts) + " Z"


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def ring(cx, cy, ro, ri):
    return (f"M{cx-ro:g} {cy:g} A{ro:g} {ro:g} 0 1 1 {cx+ro:g} {cy:g} A{ro:g} {ro:g} 0 1 1 {cx-ro:g} {cy:g} Z "
            f"M{cx-ri:g} {cy:g} A{ri:g} {ri:g} 0 1 0 {cx+ri:g} {cy:g} A{ri:g} {ri:g} 0 1 0 {cx-ri:g} {cy:g} Z")


# ---- lettere: ogni funzione restituisce (lista di path, larghezza) ----
def V(x):
    return [poly([(0, CAP), (38, CAP), (68, 146), (98, CAP), (136, CAP), (88, BASE), (48, BASE)], x)], 136


def V_varco(x):
    """La V del nome divisa in basso da un varco verticale largo 12 (concetto A)."""
    h = 6
    yi = CAP + (68 - h - 38) * 3                      # il bordo interno (pendenza 1/3) incontra il varco
    left = [(0, CAP), (38, CAP), (68 - h, yi), (68 - h, BASE), (48, BASE)]
    right = [(136 - px, py) for px, py in left]
    return [poly(left, x), poly(right, x)], 136


def a(x):
    cx, cy, ro, ri = x + 49, 152, 49, 19
    # l'asta sporge di 1 oltre il cerchio: niente filo chiaro dove i bordi coincidono
    return [ring(cx, cy, ro, ri), rect(x + 68, XH, 31, BASE - XH)], 98


def r(x):
    """Asta e spalla in un solo tracciato: testa piatta, curva solo all'interno."""
    ri = 19
    d = (f"M{x:g} {BASE:g} L{x:g} {XH:g} L{x+64:g} {XH:g} L{x+64:g} {XH+30:g} L{x+30+ri:g} {XH+30:g} "
         f"A{ri} {ri} 0 0 0 {x+30:g} {XH+30+ri:g} L{x+30:g} {BASE:g} Z")
    return [d], 64


def k(x):
    return [rect(x, CAP, 30, BASE - CAP),
            poly([(20, 138), (54, XH), (96, XH), (20, 180)], x),        # braccio, entra nell'asta
            poly([(50.07, 148), (80.04, 118.03), (102, BASE), (64, BASE)], x)], 102  # gamba a 75 gradi, entra nel braccio


def o(x):
    return [ring(x + 49, 152, 49, 19)], 98


def o_mirino(x):
    """o quadrata e arrotondata, aperta al centro di ogni lato: il mirino della telecamera."""
    S_, t, R, ri, g = 96, 28, 40, 10, 8     # lato, spessore, raggio esterno, raggio interno, varco
    y0 = 152 - S_ / 2
    h = S_ / 2 - g / 2                       # fine del pezzo d'angolo
    # angolo in alto a sinistra, in coordinate locali; gli altri tre sono specchiati
    tl = [("M", 0, h), ("L", 0, R), ("A", R, R, R, 0), ("L", h, 0), ("L", h, t), ("L", t + ri, t),
          ("A", ri, ri, t, t + ri, 0), ("L", t, h), ("Z",)]
    paths = []
    for fx, fy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        X = lambda v: x + ((S_ - v) if fx else v)
        Y = lambda v: y0 + ((S_ - v) if fy else v)
        sweep_flip = (fx + fy) % 2
        d = ""
        for c in tl:
            if c[0] in "ML":
                d += f"{c[0]}{X(c[1]):g} {Y(c[2]):g} "
            elif c[0] == "A" and len(c) == 5:   # arco esterno
                sw = 1 ^ sweep_flip
                d += f"A{c[1]} {c[1]} 0 0 {sw} {X(c[3]):g} {Y(c[4]):g} "
            elif c[0] == "A":                   # arco interno
                sw = 0 ^ sweep_flip
                d += f"A{c[1]} {c[1]} 0 0 {sw} {X(c[3]):g} {Y(c[4]):g} "
            else:
                d += "Z"
        paths.append(d.strip())
    return paths, S_


def word(letters, x0=0):
    """letters: lista di (funzione, spazio prima)."""
    paths, x = [], x0
    for fn, gap in letters:
        x += gap
        p, w = fn(x)
        paths += p
        x += w
    return paths, x


WORD_ROUND = [(V, 0), (a, -10), (r, 14), (k, 14), (o, 10)]
WORD_VARCO = [(V_varco, 0), (a, -10), (r, 14), (k, 14), (o, 10)]
WORD_MIRINO = [(V, 0), (a, -10), (r, 14), (k, 14), (o_mirino, 12)]


# ---- simboli 256 x 256 ----
def sym_a():
    """A · Varco: la V del nome, ingrandita 1,4 volte e centrata (un po' sopra il centro)."""
    sc = 1.4
    tx = (256 - 136 * sc) / 2
    ty = (256 - (BASE - CAP) * sc) / 2 - CAP * sc - 3
    paths, _ = V_varco(0)
    return [scale_path(p, sc, tx, ty) for p in paths]


def scale_path(d, sc, tx, ty):
    """Scala un tracciato fatto solo di M, L e Z."""
    parts, res = d.replace("Z", "").replace("M", "").split(" L"), []
    for pt in parts:
        x, y = map(float, pt.split())
        res.append((round(x * sc + tx, 2), round(y * sc + ty, 2)))
    return poly(res)


def sym_c():
    """C · Colli: due colli in alto lasciano un varco largo un collo; il terzo ci passa sotto."""
    s, gy = 72, 16
    y0 = (256 - (2 * s + gy)) / 2
    x0 = (256 - 3 * s) / 2
    return [rect(x0, y0, s, s), rect(x0 + 2 * s, y0, s, s), rect(x0 + s, y0 + s + gy, s, s)]


def svg(paths, w, h=256, title="Varko"):
    body = "\n".join(f'  <path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-labelledby="t">\n  <title id="t">{title}</title>\n{body}\n</svg>\n')


def transform(paths, sx, tx, ty):
    return f'<g transform="translate({tx:g} {ty:g}) scale({sx:g})">' + "".join(
        f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in paths) + "</g>"


def lockup(sym, letters, title):
    """Simbolo a 0,75 accanto al nome a 0,8, centrati sulla stessa linea."""
    wp, ww = word(letters)
    ss, ws = 0.75, 0.8
    pad, gap = 16, 40
    sym_w = 256 * ss
    tx_word = pad + sym_w + gap
    total = math.ceil(tx_word + ww * ws + pad)
    g1 = transform(sym, ss, pad, (256 - 256 * ss) / 2)
    g2 = transform(wp, ws, tx_word, 128 - 128 * ws)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total:g} 256" width="{total:g}" height="256" '
            f'role="img" aria-labelledby="t">\n  <title id="t">{title}</title>\n  {g1}\n  {g2}\n</svg>\n')


def wordmark(letters, title):
    wp, ww = word(letters, 24)
    return svg(wp, ww + 24, 256, title)


def write(name, text):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(text)


if __name__ == "__main__":
    write("a-simbolo.svg", svg(sym_a(), 256, title="Varko, concetto A: Varco"))
    write("a-lockup.svg", wordmark(WORD_VARCO, "Varko, concetto A: nome con la V a varco"))
    # B: il nome scritto; come simbolo la o a mirino, da sola
    mp, mw = o_mirino(0)
    write("b-simbolo.svg", svg([p for p in mp], mw, title="Varko, concetto B: o a mirino").replace(
        f'viewBox="0 0 {mw:g} 256"', 'viewBox="-16 88 128 128"').replace(f'width="{mw:g}" height="256"', 'width="256" height="256"'))
    write("b-lockup.svg", wordmark(WORD_MIRINO, "Varko, concetto B: nome con la o a mirino"))
    write("c-simbolo.svg", svg(sym_c(), 256, title="Varko, concetto C: Colli"))
    write("c-lockup.svg", lockup(sym_c(), WORD_ROUND, "Varko, concetto C, simbolo e nome"))
    print("scritti in", OUT)
