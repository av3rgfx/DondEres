"""Crea una prova sintetica nel formato della pagina di scatto, per controllare gli script senza le foto vere.

Uso: python prova_sintetica.py --immagini CARTELLA --uscita CARTELLA [--etichette etichette.csv]

I numeri che ne escono NON valgono come risultati della prova: le «foto» sono ritagli ruotati, spostati e
schiariti delle stesse poche immagini. Servono solo a far girare tutta la catena: ZIP, prepara.py, impronte.py,
valuta.py, etichette.py.

- Ogni immagine dà 3 articoli (immagine intera e due ritagli); gli articoli dell'ultima immagine restano fuori
  catalogo (solo foto di arrivo); altri 6 ritagli fanno da contorno.
- --etichette: CSV facoltativo con nome_file,codice_stampato,quantita per le immagini intere (la verità della 142).
- --uscita diventa un finto repository privato: lo ZIP finisce in <uscita>/da-caricare/. Va tenuta fuori dai
  repository: può contenere immagini e codici veri.
"""
from __future__ import annotations

import argparse
import csv
import io
import random
import zipfile
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from comune import COLONNE

REGIONI = [(0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 0.65, 0.65), (0.35, 0.35, 0.65, 0.65)]


def scatto(src: Image.Image, rng: random.Random) -> tuple[bytes, int, int]:
    W, H = 1440, 1920  # come un iPhone in verticale
    fondo = tuple(rng.randint(60, 190) for _ in range(3))
    tela = Image.new("RGB", (W, H), fondo).filter(ImageFilter.GaussianBlur(2))
    k = rng.uniform(0.5, 0.68) * W / src.width
    img = src.resize((max(8, int(src.width * k)), max(8, int(src.height * k))))
    img = img.rotate(rng.uniform(-7, 7), expand=True, fillcolor=fondo)
    img = ImageEnhance.Brightness(img).enhance(rng.uniform(0.75, 1.25))
    img = ImageEnhance.Contrast(img).enhance(rng.uniform(0.85, 1.15))
    if rng.random() < 0.3:
        img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.5, 1.5)))
    x = (W - img.width) // 2 + rng.randint(-W // 12, W // 12)
    y = (H - img.height) // 2 + rng.randint(-H // 12, H // 12)
    tela.paste(img, (x, y))
    buf = io.BytesIO()
    tela.save(buf, "JPEG", quality=90)
    return buf.getvalue(), W, H


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--immagini", type=Path, required=True)
    ap.add_argument("--uscita", type=Path, required=True)
    ap.add_argument("--etichette", type=Path)
    ap.add_argument("--seme", type=int, default=7)
    a = ap.parse_args()
    rng = random.Random(a.seme)
    verita = {}
    if a.etichette:
        with a.etichette.open(newline="", encoding="utf-8") as fh:
            verita = {r["nome_file"]: r for r in csv.DictReader(fh)}

    sorgenti = sorted(p for p in a.immagini.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    if len(sorgenti) < 2:
        raise SystemExit("Servono almeno 2 immagini")
    righe, files = [], {}
    ora = [100000]

    def aggiungi(codice, tipo, foto, img, giorno, disp, stampato="", qta=""):
        data, w, h = scatto(img, rng)
        ora[0] += 7
        tag = {"riferimento": "rif-" + foto, "contorno": "contorno-" + foto, "arrivo": "arrivo"}[tipo]
        nome = f"{tipo}/{codice}__{tag}__{giorno}__{disp}__P1__{ora[0]:06d}000.jpg"
        files[nome] = data
        righe.append({"file": nome, "codice": codice, "origine_codice": "scritto" if tipo != "arrivo" else "elenco",
                      "tipo": tipo, "foto": foto, "giorno": giorno, "ora": "10:00:00", "dispositivo": disp,
                      "tipo_dispositivo": "iphone", "persona": "P1", "larghezza": w, "altezza": h,
                      "riquadro_x": 0.15, "riquadro_y": 0.15, "riquadro_l": 0.7, "riquadro_a": 0.7,
                      "codice_stampato": stampato, "quantita": qta, "pagina": "sintetica", "browser": "sintetico"})

    for i, p in enumerate(sorgenti):
        base = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        fuori = i == len(sorgenti) - 1
        v = verita.get(p.name, {})
        for j, (x, y, w, h) in enumerate(REGIONI):
            reg = base.crop((int(x * base.width), int(y * base.height), int((x + w) * base.width), int((y + h) * base.height)))
            codice = f"SINT-{i + 1:02d}-{j + 1}"
            if not fuori:
                aggiungi(codice, "riferimento", "davanti", reg, "2026-11-18", "iphone-a")
                aggiungi(codice, "riferimento", "etichetta", reg, "2026-11-18", "iphone-a",
                         v.get("codice_stampato", "") if j == 0 else "", v.get("quantita", "") if j == 0 else "")
                aggiungi(codice, "riferimento", "altro-lato", ImageOps.mirror(reg), "2026-11-18", "iphone-a")
            for k in range(3):
                aggiungi(codice, "arrivo", "arrivo", reg, f"2026-11-{19 + k}", "iphone-a" if k < 2 else "iphone-b")
    for c in range(6):
        p = rng.choice(sorgenti)
        base = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        x, y = rng.uniform(0, 0.5), rng.uniform(0, 0.5)
        reg = base.crop((int(x * base.width), int(y * base.height), int((x + 0.5) * base.width), int((y + 0.5) * base.height)))
        reg = ImageOps.flip(reg) if c % 2 else ImageEnhance.Color(reg).enhance(0.3)
        aggiungi(f"SINT-C{c + 1:02d}", "contorno", "davanti", reg, "2026-11-18", "iphone-a")

    out = a.uscita / "da-caricare"
    out.mkdir(parents=True, exist_ok=True)
    elenco = io.StringIO()
    wcsv = csv.DictWriter(elenco, fieldnames=COLONNE, lineterminator="\r\n")
    wcsv.writeheader()
    wcsv.writerows(righe)
    with zipfile.ZipFile(out / "giro_sintetico_parte-1-di-1.zip", "w", zipfile.ZIP_STORED) as zf:
        for nome, data in files.items():
            zf.writestr(nome, data)
        zf.writestr("elenco_sintetico_parte-1-di-1.csv", elenco.getvalue())
    print(f"{len(files)} foto sintetiche in {out}")


if __name__ == "__main__":
    main()
