"""Kit di Ripo (giro 8): la R · Rampa (380) e il nome «Ripo» (386) disegnati come forme piene.
Peso medio delle minuscole (374): asta 22 sull'altezza della x di 96. Linea di base y=200, x a 104, maiuscola a 56,
discendente della p fino a 244. Varianti per le domande: R del nome a rampa o normale, puntino della i tondo o quadrato.
Uso: python3 genera.py  (scrive dati.json e gli SVG nella stessa cartella)
"""
import json, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
BASE, XH, CAP, DESC = 200, 104, 56, 244
T = 22                      # asta delle minuscole (peso medio)


def f(v):
    return f"{round(v, 2):g}"


def poly(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def ring(cx, cy, ro, ri):
    return (f"M{f(cx-ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx+ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx-ro)} {f(cy)} Z "
            f"M{f(cx-ri)} {f(cy)} A{f(ri)} {f(ri)} 0 1 0 {f(cx+ri)} {f(cy)} A{f(ri)} {f(ri)} 0 1 0 {f(cx-ri)} {f(cy)} Z")


def R(x0, s, top, base, gamba="rampa"):
    """R con le proporzioni del simbolo 380: occhiello alto due terzi, tratto dritto 1,33 raggi.
    gamba «rampa»: cuneo a 45 gradi; «normale»: un'asta obliqua a 45 gradi dello stesso spessore."""
    H = base - top
    ro = 0.33 * H
    ri = ro - s
    yb = top + 2 * ro                  # fondo dell'occhiello
    cx = x0 + 1.33 * ro                # centro dell'arco
    stem = rect(x0, top, s, H)
    bowl = (f"M{f(x0)} {f(top)} L{f(cx)} {f(top)} A{f(ro)} {f(ro)} 0 0 1 {f(cx)} {f(yb)} L{f(x0)} {f(yb)} Z "
            f"M{f(x0+s)} {f(top+s)} L{f(cx)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(cx)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    yt = yb - 0.15 * ro                # la gamba entra un po' nell'occhiello
    xl, xr = x0 + 1.15 * ro, x0 + 1.58 * ro
    if gamba == "rampa":
        leg = poly([(xl, yt), (xr, yt), (xr + (base - yt), base), (xl, base)])
        right = xr + (base - yt)
    else:
        w = s * math.sqrt(2)
        leg = poly([(xr - w, yt), (xr, yt), (xr + (base - yt), base), (xr - w + (base - yt), base)])
        right = xr + (base - yt)
    return [stem, bowl, leg], right - x0


def i(x, t=T, dot="tondo"):
    d = t * 1.25
    cx, cy = x + t / 2, XH - 14 - d / 2
    if dot == "tondo":
        dd = f"M{f(cx-d/2)} {f(cy)} A{f(d/2)} {f(d/2)} 0 1 1 {f(cx+d/2)} {f(cy)} A{f(d/2)} {f(d/2)} 0 1 1 {f(cx-d/2)} {f(cy)} Z"
    else:
        dd = rect(cx - d / 2, cy - d / 2, d, d)
    return [rect(x, XH, t, BASE - XH), dd], t


def p(x, t=T):
    ro = 49
    return [rect(x, XH, t, DESC - XH), ring(x + ro, 152, ro, ro - t)], 2 * ro


def o(x, t=T):
    return [ring(x + 49, 152, 49, 49 - t)], 98


def nome(gamba="rampa", dot="tondo", x0=20):
    """«Ripo»: la R alla stessa altezza delle maiuscole, un po' più spessa delle minuscole (come la K di Kiln)."""
    paths, x = [], x0
    rp, rw = R(x, T * 1.18, CAP, BASE, gamba)
    paths += rp
    x += rw + 10
    for fn, gap in ((lambda X: i(X, T, dot), 0), (lambda X: p(X), 14), (lambda X: o(X), 12)):
        x += gap
        pp, w = fn(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


def simbolo():
    """Il simbolo 380 rifatto con la stessa funzione della R del nome (asta 44 su 256)."""
    paths, w = R(0, 44, 28, 228, "rampa")
    dx = (256 - w) / 2
    out = []
    for d in paths:
        out.append(shift(d, dx))
    return out


def shift(d, dx):
    """Sposta in orizzontale un tracciato fatto di M, L, A, Z (le A hanno 7 numeri, si sposta il sesto)."""
    toks, out, cmd, buf = d.replace(",", " ").split(), [], None, []
    for tk in toks:
        if tk[0].isalpha():
            cmd = tk[0]; out.append(cmd); rest = tk[1:]
            if rest:
                buf.append(rest)
        else:
            buf.append(tk)
        if cmd in "ML" and len(buf) == 2:
            out += [f(float(buf[0]) + dx), buf[1]]; buf = []
        elif cmd == "A" and len(buf) == 7:
            buf[5] = f(float(buf[5]) + dx); out += buf; buf = []
        elif cmd == "Z":
            buf = []
    return " ".join(out).replace("M ", "M").replace("L ", "L").replace("A ", "A")


def svg(paths, w, h=256, title="Ripo", fill="#111111"):
    body = "\n".join(f'  <path fill="{fill}" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t">\n  <title id="t">{title}</title>\n{body}\n</svg>\n')


if __name__ == "__main__":
    data = {"sym": simbolo(), "nome": {}}
    for g in ("rampa", "normale"):
        for d in ("tondo", "quadrato"):
            pp, w = nome(g, d)
            data["nome"][f"{g}-{d}"] = {"vb": f"0 0 {w} 256", "d": pp}
            open(os.path.join(OUT, f"nome-{g}-{d}.svg"), "w").write(svg(pp, w, title=f"Ripo, R {g}, puntino {d}"))
    open(os.path.join(OUT, "simbolo.svg"), "w").write(svg(data["sym"], 256, title="Ripo, simbolo R · Rampa"))
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti in", OUT)
