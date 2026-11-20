"""Concetti del giro 5: lettere R e Q (decisioni 375-379). Simboli 256 x 256, forme piene, asta 44.
Il nome non c'è ancora: nasce dalla lettera scelta (375, 379).
Uso: python3 genera.py  (scrive gli SVG e dati.json nella stessa cartella)
"""
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))


def f(v):
    return f"{round(v, 2):g}"


def poly(pts, dx=0, dy=0):
    return "M" + " L".join(f"{f(x+dx)} {f(y+dy)}" for x, y in pts) + " Z"


def ring(cx, cy, ro, ri):
    return (f"M{f(cx-ro)} {f(cy)} A{ro} {ro} 0 1 1 {f(cx+ro)} {f(cy)} A{ro} {ro} 0 1 1 {f(cx-ro)} {f(cy)} Z "
            f"M{f(cx-ri)} {f(cy)} A{ri} {ri} 0 1 0 {f(cx+ri)} {f(cy)} A{ri} {ri} 0 1 0 {f(cx-ri)} {f(cy)} Z")


def r_rampa():
    """R · Rampa: asta, occhiello tondo e una gamba a cuneo a 45 gradi, come la rampa di carico."""
    dx = -15                                     # centra l'insieme sulla tela
    stem = poly([(52, 28), (96, 28), (96, 228), (52, 228)], dx)
    bowl = (f"M{52+dx} 28 L{140+dx} 28 A66 66 0 0 1 {140+dx} 160 L{52+dx} 160 Z "
            f"M{96+dx} 72 L{140+dx} 72 A22 22 0 0 1 {140+dx} 116 L{96+dx} 116 Z")
    ramp = poly([(128, 150), (156, 150), (234, 228), (128, 228)], dx)
    return [stem, bowl, ramp]


def q_collo():
    """Q · Collo: un anello e, come coda, un collo quadrato appoggiato in basso a destra."""
    c = 122
    sq = poly([(c + 40, c + 40), (c + 104, c + 40), (c + 104, c + 104), (c + 40, c + 104)])
    return [ring(c, c, 92, 48), sq]


def q_nastro():
    """Q · Nastro: il rotolo di nastro da imballo; la coda è il nastro che si srotola."""
    cx, cy = 106, 128
    t, x1 = 22, cx + 128                         # nastro sottile; in fondo il taglio a dentini del dispenser
    y0 = cy + 92 - t
    strip = poly([(cx, y0), (x1, y0), (x1 + 8, y0 + t / 4), (x1, y0 + t / 2), (x1 + 8, y0 + 3 * t / 4),
                  (x1, cy + 92), (cx, cy + 92)])
    return [ring(cx, cy, 92, 48), strip]


SIMBOLI = {"r-rampa": r_rampa, "q-collo": q_collo, "q-nastro": q_nastro}

if __name__ == "__main__":
    data = {}
    for n, fn in SIMBOLI.items():
        d = fn()
        data[n] = d
        body = "\n".join(f'  <path fill="#111111" fill-rule="evenodd" d="{p}"/>' for p in d)
        open(os.path.join(OUT, n + ".svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" '
            f'aria-labelledby="t">\n  <title id="t">Concetto {n}</title>\n{body}\n</svg>\n')
    open(os.path.join(OUT, "dati.json"), "w").write(json.dumps(data, separators=(",", ":")))
    print("scritti", len(data), "simboli in", OUT)
