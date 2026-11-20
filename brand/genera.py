"""Kit del logo di Ripo (decisioni 396 e 397): la R · Pulito costruito rifinita, la R per i 16 punti, il nome
«Ripo» a peso medio (374), le versioni nera, bianca, blu e blu chiaro, le icone per telefono e browser.

Tutto è fatto di forme piene (niente testo vivo, niente effetti). Uso:

    python3 brand/genera.py            # scrive svg/, icone/ e dati.json accanto a questo file

Per le immagini PNG e il favicon.ico usa gli script della skill logo-design (Chromium già presente).

Correzioni ottiche rispetto a prototipi/brand-kit/concetti-7/genera.py (giro 12):
- le orizzontali dell'occhiello sono più sottili dell'asta (0,9), la parte tonda un po' più spessa (1,05): così
  sembrano uguali all'occhio;
- la gamba è appena più sottile dell'asta (0,95), come le diagonali delle lettere, e resta di spessore costante;
- la gamba passa sotto il vuoto dell'occhiello senza toccarlo (controllo numerico in fondo al file);
- versione bianca un po' più sottile (sul nero il bianco sembra più pesante);
- R apposta per 16 punti, disegnata sulla griglia dei pixel: vuoti più larghi e gamba più corta.
"""
import importlib.util, json, math, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)
SKILL = os.path.join(ROOT, ".claude", "skills", "logo-design", "scripts")

# Colori (decisione 388; variante chiara da confermare nel giro 13)
NERO, BIANCO, BLU = "#000000", "#FFFFFF", "#1F5BFF"
BLU_CHIARO = os.environ.get("RIPO_BLU_CHIARO", "#668FFF")
INCHIOSTRO = "#111111"      # nero dei file di lavoro e delle anteprime
ASTA = float(os.environ.get("RIPO_ASTA", "40"))   # asta del simbolo su 200 di altezza (da confermare nel giro 13)
ICONA = os.environ.get("RIPO_ICONA", "blu")       # fondo dell'icona dell'app: blu, bianco o nero (giro 13)


def f(v):
    return f"{round(v, 2):g}"


def rect(x, y, w, h):
    return f"M{f(x)} {f(y)} L{f(x+w)} {f(y)} L{f(x+w)} {f(y+h)} L{f(x)} {f(y+h)} Z"


def ring(cx, cy, ro, rix, riy):
    """Anello: esterno circolare, interno ellittico (orizzontali più sottili)."""
    return (f"M{f(cx-ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx+ro)} {f(cy)} A{f(ro)} {f(ro)} 0 1 1 {f(cx-ro)} {f(cy)} Z "
            f"M{f(cx-rix)} {f(cy)} A{f(rix)} {f(riy)} 0 1 0 {f(cx+rix)} {f(cy)} "
            f"A{f(rix)} {f(riy)} 0 1 0 {f(cx-rix)} {f(cy)} Z")


def disc(cx, cy, r):
    return f"M{f(cx-r)} {f(cy)} A{f(r)} {f(r)} 0 1 1 {f(cx+r)} {f(cy)} A{f(r)} {f(r)} 0 1 1 {f(cx-r)} {f(cy)} Z"


# --- tratto di spessore costante lungo una Bézier (dal giro 11) -------------------------------------------------

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    pt = [u**3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t**3 * p3[i] for i in (0, 1)]
    dt = [3 * u * u * (p1[i] - p0[i]) + 6 * u * t * (p2[i] - p1[i]) + 3 * t * t * (p3[i] - p2[i]) for i in (0, 1)]
    return pt, dt


def smooth(pts):
    d = ""
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def lati(seg, hw, n=12):
    left, right = [], []
    for k in range(n + 1):
        (x, y), (dx, dy) = bez(*seg, k / n)
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((x + nx * hw, y + ny * hw))
        right.append((x - nx * hw, y - ny * hw))
    return left, right


def tratto(seg, hw, base=None, n=12):
    """Contorno chiuso del tratto. Se base è dato, l'ultimo punto dei due lati si posa esattamente sulla base
    (piede tagliato orizzontale)."""
    left, right = lati(seg, hw, n)
    if base is not None:
        left[-1] = (left[-1][0], base)
        right[-1] = (right[-1][0], base)
    rr = right[::-1]
    return (f"M{f(left[0][0])} {f(left[0][1])}" + smooth(left) +
            f" L{f(rr[0][0])} {f(rr[0][1])}" + smooth(rr) + " Z"), left, right


# --- la R ---------------------------------------------------------------------------------------------------------

def R(x0, s, top, base, k_or=0.9, k_tondo=1.05, k_gamba=0.95, reach=0.92, sottile=0.0):
    """R · Pulito costruito (396). x0, top, base: gabbia; s: asta.
    k_or / k_tondo / k_gamba: spessori relativi di orizzontali, parte tonda e gamba.
    sottile: quanto togliere a ogni bordo (versione bianca su fondo scuro)."""
    H = base - top
    r = 0.32 * H
    sh, sr, sg = k_or * s, k_tondo * s, k_gamba * s
    xb = x0 + s + 0.2 * r
    yb = top + 2 * r
    e = sottile
    # asta + occhiello in un solo contorno; il vuoto è un semi-ellisse (quasi un semicerchio, 393)
    out = (f"M{f(x0+e)} {f(top+e)} L{f(xb)} {f(top+e)} A{f(r-e)} {f(r-e)} 0 0 1 {f(xb)} {f(yb-e)} "
           f"L{f(x0+s-e)} {f(yb-e)} L{f(x0+s-e)} {f(base-e)} L{f(x0+e)} {f(base-e)} Z")
    rx, ry = r - sr + e, r - sh + e
    vuoto = (f"M{f(x0+s-e)} {f(top+sh-e)} L{f(xb)} {f(top+sh-e)} A{f(rx)} {f(ry)} 0 0 1 {f(xb)} {f(yb-sh+e)} "
             f"L{f(x0+s-e)} {f(yb-sh+e)} Z")
    # gamba: nasce sotto l'occhiello, dentro l'asta, e si posa diritta sulla base
    hw = sg / 2 - e
    xe = x0 + reach * H
    p0 = (x0 + s * 0.55, yb - sg / 2)
    p3 = (xe - sg / 2, base)
    seg = (p0, (p0[0] + 0.62 * (p3[0] - p0[0]), p0[1] + 0.04 * H), (p3[0], p3[1] - 0.45 * (p3[1] - p0[1])), p3)
    gamba, left, right = tratto(seg, hw, base=base - e)
    info = {"vuoto": (x0 + s, top + sh, xb + rx, yb - sh), "bordo_alto_gamba": right, "larghezza": xe - x0}
    return [out + " " + vuoto, gamba], info


def controlla_vuoto(info):
    """La gamba non deve entrare nel vuoto dell'occhiello: il bordo alto della gamba resta sotto il fondo del vuoto
    finché è sotto il vuoto."""
    x1, _, x2, ybot = info["vuoto"]
    peggio = min((y - ybot for x, y in info["bordo_alto_gamba"] if x1 <= x <= x2), default=99)
    assert peggio >= 0.5, f"la gamba è a {peggio:.2f} dal vuoto (minimo 0,5)"
    return peggio


# --- R per 16 punti, sulla griglia dei pixel ------------------------------------------------------------------------

def R16():
    """Disegnata in un quadrato di 16: asta di 3 pixel da x=2 a 5, da y=1 a 15; orizzontali di 2 pixel, così il
    vuoto è alto 4 e largo 3,5; gamba di 3 pixel più corta (finisce a x=14), piede da 11 a 14 sulla base."""
    x0, top, base, s = 2, 1, 15, 3
    r, xb, yb = 4, 7, 9
    out = (f"M{x0} {top} L{xb} {top} A{r} {r} 0 0 1 {xb} {yb} L{x0+s} {yb} L{x0+s} {base} L{x0} {base} Z")
    vuoto = f"M{x0+s} 3 L{xb} 3 A1.5 2 0 0 1 {xb} 7 L{x0+s} 7 Z"
    p0, p3 = (x0 + 1.6, yb - 0.3), (12.5, base)
    seg = (p0, (p0[0] + 0.6 * (p3[0] - p0[0]), p0[1] + 0.6), (p3[0], p3[1] - 0.45 * (p3[1] - p0[1])), p3)
    gamba, left, right = tratto(seg, 1.5, base=base, n=8)
    return [out + " " + vuoto, gamba], {"vuoto": (x0 + s, 3, xb + 1.5, 7), "bordo_alto_gamba": right}


# --- le minuscole di «Ripo», peso medio (374) ------------------------------------------------------------------------

BASE, XH, CAP, DESC = 200, 104, 56, 244
T = 22                      # asta delle minuscole
KO = 0.9                    # orizzontali delle tonde


def i_(x, t=T):
    d = t * 1.25
    return [rect(x, XH, t, BASE - XH), disc(x + t / 2, XH - 14 - d / 2, d / 2)], t


def p_(x, t=T):
    ro = 49.5
    return [rect(x, XH, t, DESC - XH), ring(x + ro, 152, ro, ro - t, ro - KO * t)], 2 * ro


def o_(x, t=T):
    ro = 49.5
    return [ring(x + ro, 152, ro, ro - t, ro - KO * t)], 2 * ro


def nome(x0=20, sottile=0.0, spazi=(12, 13, 11)):
    """«Ripo»: la R alla stessa altezza delle maiuscole, un po' più spessa delle minuscole (come la K di Kiln)."""
    paths, x = [], x0
    rp, info = R(x, T * 1.18, CAP, BASE, sottile=sottile)
    controlla_vuoto(info)
    paths += rp
    x += info["larghezza"]
    for fn, gap in ((i_, spazi[0]), (p_, spazi[1]), (o_, spazi[2])):
        x += gap
        pp, w = fn(x)
        paths += pp
        x += w
    return paths, math.ceil(x + x0)


# --- file ---------------------------------------------------------------------------------------------------------

def svg(paths, vb, title, fill, w=None, h=None, bg=None, extra=""):
    x, y, W, H = vb
    size = f' width="{w}" height="{h}"' if w else ""
    back = f'<rect x="{f(x)}" y="{f(y)}" width="{f(W)}" height="{f(H)}" fill="{bg}"/>' if bg else ""
    body = "".join(f'<path fill="{fill}" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x)} {f(y)} {f(W)} {f(H)}"{size} role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{back}{extra}{body}</svg>\n')


def simbolo(sottile=0.0):
    """Il simbolo su 256: R alta 200, asta 40, centrata e alzata di 2 unità (centro ottico)."""
    H, s = 200, ASTA
    paths, info = R(0, s, 0, H, sottile=sottile)
    controlla_vuoto(info)
    w = info["larghezza"]
    tx, ty = (256 - w) / 2, (256 - H) / 2 - 2
    return paths, (tx, ty)


def gruppo(paths, tx, ty, sc=1.0):
    return paths, f'<g transform="translate({f(tx)} {f(ty)}) scale({f(sc)})">'


def scrivi(rel, txt):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt)
    return p


def sym_svg(fill, sottile=0.0, title="Ripo, simbolo", bg=None, scala=1.0, raggio=0, size=256):
    paths, (tx, ty) = simbolo(sottile)
    c = 128
    tr = f"translate({f(c)} {f(c)}) scale({f(scala)}) translate({f(-c)} {f(-c)}) translate({f(tx)} {f(ty)})"
    body = "".join(f'<path fill="{fill}" fill-rule="evenodd" d="{p}"/>' for p in paths)
    back = f'<rect width="256" height="256" rx="{f(raggio)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="{size}" height="{size}" role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{back}<g transform="{tr}">{body}</g></svg>\n')


def sym16_svg(fill, title="Ripo, simbolo per 16 punti", bg=None):
    paths, info = R16()
    controlla_vuoto(info)
    back = f'<rect width="16" height="16" fill="{bg}"/>' if bg else ""
    body = "".join(f'<path fill="{fill}" fill-rule="evenodd" d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{back}{body}</svg>\n')


def carica(nome_mod, percorso):
    spec = importlib.util.spec_from_file_location(nome_mod, percorso)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome_mod] = m
    spec.loader.exec_module(m)
    return m


def icone():
    """Icone per il browser e per il telefono. Il favicon a 16 usa la R per i 16 punti; 32 e 48 e le icone grandi
    usano il simbolo. Fondo e colore della R da ICONA."""
    rp = carica("render_png", os.path.join(SKILL, "render_png.py"))
    sys.path.insert(0, SKILL)
    d = os.path.join(OUT, "icone")
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, ".tmp")
    os.makedirs(tmp, exist_ok=True)
    bg, fg = {"blu": (BLU, BIANCO), "bianco": (BIANCO, BLU), "nero": (NERO, BIANCO)}[ICONA]
    so = 1.0 if fg == BIANCO else 0.0       # R bianca su fondo pieno: un punto più sottile
    f16 = scrivi("icone/favicon-16.svg", sym16_svg(BLU, "Ripo"))
    fav = scrivi("icone/favicon.svg", sym_svg(BLU, title="Ripo", scala=1.12))
    tile = scrivi("icone/.tmp/tile.svg", sym_svg(fg, so, "Ripo", bg=bg, scala=0.72))
    mask = scrivi("icone/.tmp/mask.svg", sym_svg(fg, so, "Ripo", bg=bg, scala=0.56))
    app = scrivi("icone/icona-app.svg", sym_svg(fg, so, "Ripo", bg=bg, scala=0.72, raggio=57.6))
    jobs = [(f16, "favicon-16.png", 16), (fav, "favicon-32.png", 32), (fav, "favicon-48.png", 48),
            (tile, "apple-touch-icon.png", 180), (tile, "icon-192.png", 192), (tile, "icon-512.png", 512),
            (mask, "maskable-512.png", 512)]
    for src, name, px in jobs:
        assert rp.render(src, os.path.join(d, name), px, px), name
    rp.write_ico([os.path.join(d, f"favicon-{s}.png") for s in (16, 32, 48)], os.path.join(d, "favicon.ico"))
    for x in os.listdir(tmp):
        os.remove(os.path.join(tmp, x))
    os.rmdir(tmp)
    manifest = {"name": "Ripo", "short_name": "Ripo", "lang": "it", "display": "standalone", "start_url": "/",
                "theme_color": BLU, "background_color": BIANCO, "icons": [
                    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                    {"src": "/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    scrivi("icone/site.webmanifest", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    scrivi("icone/head-snippet.html",
           '<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">\n'
           '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
           '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
           '<link rel="manifest" href="/site.webmanifest">\n'
           f'<meta name="theme-color" content="{BLU}">\n')


def prova_stampa():
    """Foglio di prova per la stampante termica (etichetta 100 x 70 mm, nero): simbolo alto 4–10 mm, nome largo
    12–30 mm. Si stampa al 100 %, senza adattare alla pagina. Le scritte sono testo: è un foglio di prova, non un logo."""
    sp, info = R(0, ASTA, 0, 200)
    np_, w = nome()
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="70mm" viewBox="0 0 100 70" role="img" '
           'aria-labelledby="t"><title id="t">Ripo, prova di stampa</title><rect width="100" height="70" fill="#fff"/>',
           '<g font-family="sans-serif" font-size="2.4" fill="#000">',
           '<text x="4" y="6">Ripo · prova di stampa · stampare al 100 % · simbolo: altezza; nome: larghezza</text>']
    x = 4
    for mm in (4, 5, 6, 8, 10):
        sc = mm / 200
        out.append(f'<g transform="translate({f(x)} {f(24 - mm)}) scale({f(sc)})">' +
                   "".join(f'<path fill="#000" fill-rule="evenodd" d="{d}"/>' for d in sp) + "</g>")
        out.append(f'<text x="{f(x)}" y="28">{mm} mm</text>')
        x += info["larghezza"] * sc + 8
    y = 33
    for row in ((12, 15, 20), (25, 30)):
        x = 4
        for mm in row:
            sc = mm / (w - 40)
            out.append(f'<g transform="translate({f(x - 20 * sc)} {f(y - 56 * sc)}) scale({f(sc)})">' +
                       "".join(f'<path fill="#000" fill-rule="evenodd" d="{d}"/>' for d in np_) + "</g>")
            out.append(f'<text x="{f(x)}" y="{f(y + 190 * sc + 3)}">{mm} mm</text>')
            x += mm + 8
        y += 16
    out.append("</g></svg>\n")
    return "".join(out)


def main():
    colori = {"nero": NERO, "blu": BLU, "bianco": BIANCO, "blu-chiaro": BLU_CHIARO}
    dati = {"colori": colori, "simbolo": {}, "nome": {}}
    for k, c in colori.items():
        sottile = 1.0 if k in ("bianco", "blu-chiaro") else 0.0     # su fondo scuro: un punto più sottile
        scrivi(f"svg/ripo-simbolo-{k}.svg", sym_svg(c, sottile, f"Ripo, simbolo {k}"))
        pp, w = nome(sottile=sottile * 0.65)
        scrivi(f"svg/ripo-nome-{k}.svg", svg(pp, (0, 0, w, 256), f"Ripo, nome {k}", c, w, 256))
    scrivi("svg/ripo-simbolo-16.svg", sym16_svg(NERO))
    scrivi("prova-stampa.svg", prova_stampa())
    sp, (tx, ty) = simbolo()
    sp16, _ = R16()
    np_, w = nome()
    dati["simbolo"] = {"g": f"translate({f(tx)} {f(ty)})", "d": sp}
    dati["simbolo_scuro"] = {"g": f"translate({f(tx)} {f(ty)})", "d": simbolo(1.0)[0]}
    dati["simbolo16"] = {"d": sp16}
    dati["nome"] = {"vb": f"0 0 {w} 256", "d": np_}
    scrivi("dati.json", json.dumps(dati, separators=(",", ":")))
    if "--senza-icone" not in sys.argv:
        icone()
    print("scritti in", OUT)


if __name__ == "__main__":
    main()
