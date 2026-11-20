"""Concetti del giro 10: R con il vuoto tondo e la gamba lunga e curva (decisione 393).
Ogni R è una funzione di altezza H e asta s: la stessa forma fa il simbolo 256 x 256 e la R del nome «Ripo».
Uso: python3 genera.py  (scrive gli SVG e dati.json nella stessa cartella)
"""
import json, math, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "..", "kit"))
import genera as kit
from genera import f, rect

CAP, BASE, XH = kit.CAP, kit.BASE, kit.XH


def occhiello(x0, s, top, H, k=0.62):
    """Occhiello tondo: tratto dritto corto, poi un semicerchio; il vuoto è quasi un semicerchio (393)."""
    ro = k * H / 2
    ri = ro - s
    yb = top + 2 * ro
    cx = x0 + s + 0.25 * ro
    d = (f"M{f(x0)} {f(top)} L{f(cx)} {f(top)} A{f(ro)} {f(ro)} 0 0 1 {f(cx)} {f(yb)} L{f(x0)} {f(yb)} Z "
         f"M{f(x0+s)} {f(top+s)} L{f(cx)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(cx)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    return d, yb, cx + ro


def arco(x0, s, top, base, lungo=False):
    """A · Arco: la gamba esce dall'occhiello e scende con un arco fino alla linea di base.
    B · Arco lungo: lo stesso arco, steso in avanti: la R che parte di corsa."""
    H = base - top
    bowl, yb, right = occhiello(x0, s, top, H)
    xa = x0 + s * 0.6                     # la gamba parte dentro l'asta
    ry = base - yb + s * 0.5               # parte un po' dentro l'occhiello
    rx = (0.92 if lungo else 0.62) * H
    ytop = base - ry
    leg = (f"M{f(xa)} {f(ytop)} A{f(rx)} {f(ry)} 0 0 1 {f(xa+rx)} {f(base)} L{f(xa+rx-s*1.1)} {f(base)} "
           f"A{f(rx-s*1.1)} {f(ry-s)} 0 0 0 {f(xa)} {f(ytop+s)} Z")
    return [rect(x0, top, s, H), bowl, leg], xa + rx - x0


def scivolo(x0, s, top, base):
    """B · Scivolo: la gamba scende con una curva concava e si assottiglia, come uno scivolo che porta giù i colli."""
    H = base - top
    bowl, yb, right = occhiello(x0, s, top, H)
    xl = x0 + 0.34 * H
    yt = yb - 0.04 * H
    xe = x0 + 1.02 * H
    te = 0.075 * H                         # spessore in fondo: regge le stampe termiche
    rx_o, ry_o = xe - xl, base - yt
    rx_i, ry_i = xe - (xl + s), base - te - yt
    leg = (f"M{f(xl)} {f(yt)} L{f(xl+s)} {f(yt)} A{f(rx_i)} {f(ry_i)} 0 0 0 {f(xe)} {f(base-te)} "
           f"L{f(xe)} {f(base)} A{f(rx_o)} {f(ry_o)} 0 0 1 {f(xl)} {f(yt)} Z")
    return [rect(x0, top, s, H), bowl, leg], xe - x0


def nastro(x0, s, top, base):
    """C · Nastro: la gamba scende, gira e corre lungo la linea di base, come un nastro trasportatore."""
    H = base - top
    bowl, yb, right = occhiello(x0, s, top, H)
    xl = x0 + 0.34 * H
    rb = 0.22 * H                          # raggio esterno della curva
    t = 0.75 * s                           # il nastro un po' più sottile dell'asta
    xe = x0 + 1.02 * H
    yt = yb - 0.04 * H
    leg = (f"M{f(xl)} {f(yt)} L{f(xl+s)} {f(yt)} L{f(xl+s)} {f(base-rb)} "
           f"A{f(rb-s)} {f(rb-t)} 0 0 0 {f(xl+rb)} {f(base-t)} L{f(xe)} {f(base-t)} L{f(xe)} {f(base)} "
           f"L{f(xl+rb)} {f(base)} A{f(rb)} {f(rb)} 0 0 1 {f(xl)} {f(base-rb)} Z")
    return [rect(x0, top, s, H), bowl, leg], xe - x0


def arco_lungo(x0, s, top, base):
    return arco(x0, s, top, base, lungo=True)


FN = {"arco": arco, "lungo": arco_lungo, "scivolo": scivolo}


def nome(kind, x0=20, s=26):
    paths, x = [], x0
    rp, rw = FN[kind](x, s, CAP, BASE)
    paths += rp
    x += rw + (10 if kind == "arco" else 6)
    for fn, gap in ((lambda X: kit.i(X, kit.T, "tondo"), 0), (kit.p, 14), (kit.o, 12)):
        x += gap
        pp, w = fn(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


def simbolo(kind):
    H = 196
    paths, w = FN[kind](0, 0.22 * H, 0, H)
    sc = min(1, 224 / w)
    tx, ty = (256 - w * sc) / 2, (256 - H * sc) / 2
    return f'<g transform="translate({f(tx)} {f(ty)}) scale({f(sc)})">', paths


if __name__ == "__main__":
    data = {"sym": {}, "nome": {}}
    for k in FN:
        g, sp = simbolo(k)
        data["sym"][k] = {"g": g, "d": sp}
        body = "".join(f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in sp)
        open(os.path.join(OUT, f"{k}-simbolo.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" '
            f'aria-labelledby="t"><title id="t">Ripo, concetto {k}</title>{g}{body}</g></svg>\n')
        pp, w = nome(k)
        data["nome"][k] = {"vb": f"0 0 {w} 256", "d": pp}
        open(os.path.join(OUT, f"{k}-nome.svg"), "w").write(kit.svg(pp, w, title=f"Ripo, nome, concetto {k}"))
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti in", OUT)
