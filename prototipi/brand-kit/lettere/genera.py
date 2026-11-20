"""Schizzi del giro 4: otto lettere candidate, ciascuna con una modifica d'esempio (decisione 375).
Non sono loghi finiti: servono a scegliere le lettere su cui disegnare i concetti.
Tela 100 x 100. Uso: python3 genera.py  (scrive dati.json e un SVG per lettera)
"""
import json, math, os

OUT = os.path.dirname(os.path.abspath(__file__))


def f(v):
    return f"{round(v, 2):g}"


def poly(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def k_scatto():
    """K: asta e una «<» staccata a 60 gradi; tra le due resta una fessura."""
    xa, hw, d = 56.7, 12.7, 23.09
    cut = 48                                   # taglio verticale: fessura larga 12 dall'asta
    dy = (cut - (xa - hw)) * 40 / d
    chev = [(xa + d - hw, 10), (xa + d + hw, 10), (xa + hw, 50), (xa + d + hw, 90), (xa + d - hw, 90),
            (cut, 50 + dy), (cut, 50 - dy)]
    return [rect(14, 10, 22, 80), poly(chev)]


def r_piede():
    """R: occhiello tondo e una gamba che scende diritta come un piede d'appoggio."""
    bowl = "M14 10 L56 10 A25 25 0 0 1 56 60 L14 60 Z M32 28 L56 28 A7 7 0 0 1 56 42 L32 42 Z"
    return [rect(14, 10, 18, 80), bowl, rect(62, 60, 20, 30)]


def s_squadrata():
    """S: due curve a gomito, tagliate a squadra, con due angoli tondi opposti."""
    top = "M38 10 L84 10 L84 28 L38 28 L38 41 L20 41 L20 28 A18 18 0 0 1 38 10 Z"
    mid = rect(20, 41, 64, 18)
    bot = "M66 59 L84 59 L84 72 A18 18 0 0 1 66 90 L16 90 L16 72 L66 72 Z"
    return [top, mid, bot]


def m_scaffale():
    """M: tre montanti appesi a una trave, come una scaffalatura vista di fronte."""
    return [rect(10, 10, 80, 18), rect(10, 28, 18, 62), rect(41, 28, 18, 34), rect(72, 28, 18, 62)]


def a_tenda():
    """A: un triangolo pieno con una porta al centro al posto della barra."""
    return ["M50 8 L94 90 L60 90 L60 62 L40 62 L40 90 L6 90 Z"]


def q_blocco():
    """Q: un anello e una coda a blocco quadrato che esce in basso a destra."""
    ring = "M10 48 A38 38 0 1 1 86 48 A38 38 0 1 1 10 48 Z M28 48 A20 20 0 1 0 68 48 A20 20 0 1 0 28 48 Z"
    return [ring, rect(64, 64, 28, 28)]


def g_taglio():
    """G: anello aperto in alto a destra e una barra che rientra verso il centro."""
    ring = "M90 50 A40 40 0 1 1 70 15.36 L61 30.95 A22 22 0 1 0 72 50 Z"
    return [ring, rect(52, 50, 38, 16)]


def x_smistamento():
    """X: quattro triangoli che puntano al centro; la X è il vuoto tra loro, come un incrocio di smistamento."""
    return [poly([(14, 8), (86, 8), (50, 42)]), poly([(14, 92), (86, 92), (50, 58)]),
            poly([(8, 14), (8, 86), (42, 50)]), poly([(92, 14), (92, 86), (58, 50)])]


LETTERE = {"K": k_scatto, "R": r_piede, "S": s_squadrata, "M": m_scaffale, "A": a_tenda, "Q": q_blocco,
           "G": g_taglio, "X": x_smistamento}

if __name__ == "__main__":
    data = {}
    for n, fn in LETTERE.items():
        d = fn()
        data[n] = d
        body = "".join(f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in d)
        open(os.path.join(OUT, f"{n.lower()}.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="256" height="256" role="img" '
            f'aria-labelledby="t"><title id="t">Lettera {n}, schizzo</title>{body}</svg>\n')
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritte", len(data), "lettere in", OUT)
