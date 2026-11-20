"""Concetti del giro 9: la R più curva dallo schizzo dell'utente (389) e altre idee (392).
Ogni R è una funzione con altezza H e asta s, così la stessa forma fa il simbolo (256 x 256) e la R del nome «Ripo».
Uso: python3 genera.py  (scrive gli SVG e dati.json nella stessa cartella)
"""
import json, math, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "..", "kit"))
import genera as kit                        # i, p, o del nome a peso medio (374) e le funzioni di base
from genera import f, poly, rect, ring

CAP, BASE, XH = kit.CAP, kit.BASE, kit.XH


def occhiello(x0, s, top, H, attacco=True, g=0):
    """Occhiello a D con il vuoto rettangolare, come nello schizzo. Senza attacco: staccato dall'asta (stencil)."""
    ro = 0.33 * H
    yb = top + 2 * ro
    cx = x0 + 0.47 * H
    xin = cx + 0.03 * H
    xa = x0 if attacco else x0 + s + g
    d = (f"M{f(xa)} {f(top)} L{f(cx)} {f(top)} A{f(ro)} {f(ro)} 0 0 1 {f(cx)} {f(yb)} L{f(xa)} {f(yb)} ")
    if attacco:
        d += (f"Z M{f(x0+s)} {f(top+s)} L{f(xin)} {f(top+s)} L{f(xin)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    else:
        d += (f"L{f(xa)} {f(yb-s)} L{f(xin)} {f(yb-s)} L{f(xin)} {f(top+s)} L{f(xa)} {f(top+s)} Z")
    return d, yb


def U(xl, s, ru, yt_l, yt_r, base):
    """Gamba a U: braccio sinistro da yt_l, fondo tondo sulla linea di base, braccio destro fino a yt_r."""
    cy = base - ru
    ri = ru - s
    xr = xl + 2 * ru
    return (f"M{f(xl)} {f(yt_l)} L{f(xl)} {f(cy)} A{f(ru)} {f(ru)} 0 0 0 {f(xr)} {f(cy)} L{f(xr)} {f(yt_r)} "
            f"L{f(xr-s)} {f(yt_r)} L{f(xr-s)} {f(cy)} A{f(ri)} {f(ri)} 0 0 1 {f(xl+s)} {f(cy)} L{f(xl+s)} {f(yt_l)} Z")


def gancio(x0, s, top, base):
    """A · Il tuo schizzo: la gamba scende, gira e risale a U, staccata dall'asta: un gancio che prende la merce."""
    H = base - top
    bowl, yb = occhiello(x0, s, top, H)
    xl, ru = x0 + 0.30 * H, 0.31 * H
    # il braccio sinistro entra nell'occhiello; il destro si ferma più in basso, staccato, come nello schizzo
    return [rect(x0, top, s, H), bowl, U(xl, s, ru, yb - 0.05 * H, yb + 0.07 * H, base)], 0.92 * H


def legatura(x0, s, top, base, xh, dot=True):
    """B · Ri: la gamba a U risale e diventa la i del nome, con il suo puntino."""
    H = base - top
    bowl, yb = occhiello(x0, s, top, H)
    xs = x0 + 0.88 * H                       # asta della i, a destra dell'occhiello
    xl = x0 + 0.30 * H
    ru = (xs + s - xl) / 2
    parts = [rect(x0, top, s, H), bowl, U(xl, s, ru, yb - 0.05 * H, xh, base)]
    if dot:
        dd = s * 1.25
        cx, cy = xs + s / 2, xh - 0.1 * H - dd / 2
        parts.append(f"M{f(cx-dd/2)} {f(cy)} A{f(dd/2)} {f(dd/2)} 0 1 1 {f(cx+dd/2)} {f(cy)} "
                     f"A{f(dd/2)} {f(dd/2)} 0 1 1 {f(cx-dd/2)} {f(cy)} Z")
    return parts, xs + s - x0


def stencil(x0, s, top, base):
    """C · Stencil: la stessa R in tre pezzi con i ponti, come le lettere spruzzate sulle casse."""
    H = base - top
    g = 0.06 * H
    bowl, yb = occhiello(x0, s, top, H, attacco=False, g=g)
    xl, ru = x0 + 0.30 * H, 0.31 * H
    return [rect(x0, top, s, H), bowl, U(xl, s, ru, yb + g, yb + g, base)], 0.92 * H


def scivolo(x0, s, top, base):
    """D · Scivolo: la rampa della R, ma curva come lo scivolo a rulli che porta i colli giù dal soppalco."""
    H = base - top
    bowl, yb = occhiello(x0, s, top, H)
    xl = x0 + 0.30 * H
    yt = yb - 0.05 * H
    r = base - yt
    xe = xl + s + r
    leg = (f"M{f(xl)} {f(yt)} L{f(xl+s)} {f(yt)} A{f(r)} {f(r)} 0 0 0 {f(xe)} {f(base)} L{f(xl)} {f(base)} Z")
    return [rect(x0, top, s, H), bowl, leg], xe - x0


def nome(kind, x0=20, s=26):
    """«Ripo» con la R del concetto alla stessa altezza delle maiuscole."""
    paths, x = [], x0
    if kind == "legatura":
        rp, rw = legatura(x, s, CAP, BASE, XH)
        paths += rp
        x += rw + 14
    else:
        fn = {"gancio": gancio, "stencil": stencil, "scivolo": scivolo}[kind]
        rp, rw = fn(x, s, CAP, BASE)
        paths += rp
        x += rw + 12
        pp, w = kit.i(x, kit.T, "tondo")
        paths += pp
        x += w + 14
    for fnl, gap in ((kit.p, 0), (kit.o, 12)):
        x += gap
        pp, w = fnl(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


def simbolo(kind):
    """Il simbolo: la R del concetto su 256 x 256, con le stesse proporzioni (asta 0,22 dell'altezza)."""
    H = 196
    s = 0.22 * H
    if kind == "legatura":
        paths, w = legatura(0, s, 0, H, 0.33 * H)
        top_extra = 0                       # il puntino sta sotto la linea delle maiuscole
    else:
        paths, w = {"gancio": gancio, "stencil": stencil, "scivolo": scivolo}[kind](0, s, 0, H)
    sc = min(1, 220 / w)
    tx, ty = (256 - w * sc) / 2, (256 - H * sc) / 2
    return [f'<g transform="translate({f(tx)} {f(ty)}) scale({f(sc)})">'] + paths + ["</g>"]


def svg_sym(parts, title):
    g0, paths, g1 = parts[0], parts[1:-1], parts[-1]
    body = "".join(f'<path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{g0}{body}{g1}</svg>\n')


if __name__ == "__main__":
    data = {"sym": {}, "nome": {}}
    for k in ("gancio", "legatura", "stencil", "scivolo"):
        sp = simbolo(k)
        data["sym"][k] = {"g": sp[0], "d": sp[1:-1]}
        open(os.path.join(OUT, f"{k}-simbolo.svg"), "w").write(svg_sym(sp, f"Ripo, concetto {k}"))
        pp, w = nome(k)
        data["nome"][k] = {"vb": f"0 0 {w} 256", "d": pp}
        open(os.path.join(OUT, f"{k}-nome.svg"), "w").write(kit.svg(pp, w, title=f"Ripo, nome, concetto {k}"))
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti in", OUT)
