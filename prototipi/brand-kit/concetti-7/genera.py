"""Giro 12: la R di Ripo costruita da forme elementari, dopo le ricerche del 20/11/2026 (decisione 395):
- un dettaglio solo, la gamba, che nasce dalla geometria dell'occhiello (stesso spessore dell'asta, archi di cerchio);
- sagoma più piena, che regga a 16 punti e in un colore solo, senza bisogno del riquadro.
Tre strade: A · Pulito costruito, C · Slitta costruita (da A e C del giro 11), N · Collo ritagliato (radicale).
Uso: python3 genera.py  (scrive gli SVG e dati.json nella stessa cartella)
"""
import importlib.util, json, math, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))


def carica(nome, percorso):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    spec.loader.exec_module(m)
    return m


kit = carica("genera", os.path.join(OUT, "..", "kit", "genera.py"))
f, rect = kit.f, kit.rect
CAP, BASE = kit.CAP, kit.BASE


def occhiello(x0, s, top, r, k=0.2):
    """Occhiello: tratto dritto corto e un semicerchio di raggio r; il vuoto è quasi un semicerchio."""
    xb = x0 + s + k * r
    yb = top + 2 * r
    ri = r - s
    d = (f"M{f(x0)} {f(top)} L{f(xb)} {f(top)} A{f(r)} {f(r)} 0 0 1 {f(xb)} {f(yb)} L{f(x0)} {f(yb)} Z "
         f"M{f(x0+s)} {f(top+s)} L{f(xb)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(xb)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    return d, xb, yb


def quarto(xc, yc, ro, s):
    """Quarto di anello: dall'alto (xc, yc-ro) scende a destra fino a (xc+ro, yc). Spessore s, piede diritto."""
    ri = ro - s
    return (f"M{f(xc)} {f(yc-ro)} A{f(ro)} {f(ro)} 0 0 1 {f(xc+ro)} {f(yc)} L{f(xc+ri)} {f(yc)} "
            f"A{f(ri)} {f(ri)} 0 0 0 {f(xc)} {f(yc-ri)} Z")


def contorno_pulito(x0, s, top, base, r=None):
    """Asta, occhiello e gamba in un solo contorno (niente fili chiari dove i pezzi si toccano) e il vuoto a parte.
    La gamba è un quarto d'anello con il centro sulla linea di base, nel punto in cui finisce l'asta: nasce dalla
    geometria della lettera e ha lo stesso spessore."""
    H = base - top
    r = r or 0.32 * H                    # occhiello un po' più grande: il vuoto non si chiude in piccolo
    xb = x0 + s + 0.2 * r
    yb = top + 2 * r
    ri = r - s
    ro = base - yb                       # raggio esterno della gamba
    xc = x0 + s                          # centro della gamba
    d = (f"M{f(x0)} {f(top)} L{f(xb)} {f(top)} A{f(r)} {f(r)} 0 0 1 {f(xb)} {f(yb)} L{f(xc)} {f(yb)} "
         f"A{f(ro)} {f(ro)} 0 0 1 {f(xc+ro)} {f(base)} L{f(xc+ro-s)} {f(base)} "
         f"A{f(ro-s)} {f(ro-s)} 0 0 0 {f(xc)} {f(base-ro+s)} L{f(xc)} {f(base)} L{f(x0)} {f(base)} Z")
    vuoto = (f"M{f(x0+s)} {f(top+s)} L{f(xb)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(xb)} {f(yb-s)} "
             f"L{f(x0+s)} {f(yb-s)} Z")
    return d, vuoto, xc + ro - x0


c6 = carica("c6", os.path.join(OUT, "..", "concetti-6", "genera.py"))


def pulito(x0, s, top, base):
    """A · Pulito costruito: asta e occhiello semplici; la gamba è un arco lungo di spessore uguale all'asta, che
    nasce dove finisce l'asta e si posa diritto sulla linea di base (la «Pulito» del giro 11, con più vuoto)."""
    H = base - top
    r = 0.32 * H
    xb = x0 + s + 0.2 * r
    yb = top + 2 * r
    ri = r - s
    stem_bowl = (f"M{f(x0)} {f(top)} L{f(xb)} {f(top)} A{f(r)} {f(r)} 0 0 1 {f(xb)} {f(yb)} L{f(x0)} {f(yb)} Z "
                 f"M{f(x0+s)} {f(top+s)} L{f(xb)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(xb)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    xe = x0 + 0.92 * H
    p0, p3 = (x0 + s * 0.55, yb - s / 2), (xe - s / 2, base)
    seg = [(p0, (p0[0] + 0.62 * (p3[0] - p0[0]), p0[1]), (p3[0], p3[1] - 0.45 * (p3[1] - p0[1])), p3)]
    leg = c6.tratto(seg, lambda t: s / 2)
    return [rect(x0, top, s, H), stem_bowl, leg], xe - x0




def slitta(x0, s, top, base):
    """C · Slitta costruita: la gamba della Slitta del giro 11, ma con lo spessore dell'asta dall'inizio alla
    fine e l'attacco nel punto in cui finisce l'asta."""
    H = base - top
    r = 0.32 * H
    xb = x0 + s + 0.2 * r
    yb = top + 2 * r
    ri = r - s
    stem_bowl = (f"M{f(x0)} {f(top)} L{f(xb)} {f(top)} A{f(r)} {f(r)} 0 0 1 {f(xb)} {f(yb)} L{f(x0)} {f(yb)} Z "
                 f"M{f(x0+s)} {f(top+s)} L{f(xb)} {f(top+s)} A{f(ri)} {f(ri)} 0 0 1 {f(xb)} {f(yb-s)} L{f(x0+s)} {f(yb-s)} Z")
    xe = x0 + 1.04 * H
    ym = base - s / 2
    pm = (x0 + 0.68 * H, ym)
    p0 = (x0 + s * 0.55, yb - s / 2)
    seg1 = (p0, (p0[0] + 0.45 * (pm[0] - p0[0]), p0[1]), (pm[0] - 0.42 * (pm[0] - p0[0]), ym), pm)
    a = math.radians(30)
    p4 = (xe - s * 0.3, ym - 0.12 * H)
    seg2 = (pm, (pm[0] + 0.55 * (p4[0] - pm[0]), ym), (p4[0] - 0.09 * H * math.cos(a), p4[1] + 0.09 * H * math.sin(a)), p4)
    leg = c6.tratto([seg1, seg2], lambda t: s / 2, n=8)
    return [rect(x0, top, s, H), stem_bowl, leg], xe - x0


def collo(x0, s, top, base):
    """N · Collo ritagliato: la R di A ritagliata da un collo pieno, cioè da una scatola vista di fronte.
    Il simbolo è la scatola; la R è lo spazio vuoto. Funziona da icona senza bisogno di un riquadro."""
    H = base - top
    m = 0.16 * H                         # margine tra la R e il bordo della scatola
    rr = 0.14 * H                        # raggio degli angoli della scatola
    Rh = H - 2 * m
    d, vuoto, w = contorno_pulito(0, s * 0.9, 0, Rh)
    W = w + 2 * m
    ox, oy = x0 + m, top + m
    shift = lambda path: kit_shift(path, ox, oy)
    box = (f"M{f(x0+rr)} {f(top)} L{f(x0+W-rr)} {f(top)} A{f(rr)} {f(rr)} 0 0 1 {f(x0+W)} {f(top+rr)} "
           f"L{f(x0+W)} {f(base-rr)} A{f(rr)} {f(rr)} 0 0 1 {f(x0+W-rr)} {f(base)} L{f(x0+rr)} {f(base)} "
           f"A{f(rr)} {f(rr)} 0 0 1 {f(x0)} {f(base-rr)} L{f(x0)} {f(top+rr)} A{f(rr)} {f(rr)} 0 0 1 {f(x0+rr)} {f(top)} Z")
    return [box + " " + shift(d) + " " + shift(vuoto)], W


def kit_shift(d, dx, dy):
    """Sposta un tracciato fatto di M, L, A, Z."""
    toks = d.replace("M", " M ").replace("L", " L ").replace("A", " A ").replace("Z", " Z ").split()
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t in "ML":
            out.append(f"{t}{f(float(toks[i+1])+dx)} {f(float(toks[i+2])+dy)}"); i += 3
        elif t == "A":
            a = toks[i+1:i+8]
            out.append(f"A{a[0]} {a[1]} {a[2]} {a[3]} {a[4]} {f(float(a[5])+dx)} {f(float(a[6])+dy)}"); i += 8
        else:
            out.append("Z"); i += 1
    return " ".join(out)


FN = {"pulito": pulito, "slitta": slitta, "collo": collo}


def nome(k, x0=20, s=26):
    paths, x = [], x0
    rp, rw = FN[k](x, s, CAP, BASE)
    paths += rp
    x += rw + 8
    for fn, gap in ((lambda X: kit.i(X, kit.T, "tondo"), 0), (kit.p, 14), (kit.o, 12)):
        x += gap
        pp, w = fn(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


def simbolo(k):
    H = 200
    s = (0.22 if k == "slitta" else 0.20) * H
    paths, w = FN[k](0, s, 0, H)
    sc = min(1.0, 228 / w, 228 / H)
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
            f'aria-labelledby="t"><title id="t">Ripo, R {k}</title>{g}{body}</g></svg>\n')
        pp, w = nome(k)
        data["nome"][k] = {"vb": f"0 0 {w} 256", "d": pp}
        open(os.path.join(OUT, f"{k}-nome.svg"), "w").write(kit.svg(pp, w, title=f"Ripo, nome, R {k}"))
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti in", OUT)
