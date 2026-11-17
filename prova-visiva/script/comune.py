"""Funzioni comuni agli script della prova di accuratezza visiva.

Decisioni di riferimento in docs/decisioni.md: 128-159. Gli script leggono le foto dal repository privato
(prova-visiva-foto) e scrivono nel repository pubblico solo numeri con le sigle anonime (129).
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

TIPI = ("riferimento", "arrivo", "contorno")

# Colonne dell'elenco CSV scritto dalla pagina di scatto (prova-visiva/pagina-scatto/index.html).
COLONNE = ["file", "codice", "origine_codice", "tipo", "foto", "giorno", "ora", "dispositivo", "tipo_dispositivo",
           "persona", "larghezza", "altezza", "riquadro_x", "riquadro_y", "riquadro_l", "riquadro_a",
           "codice_stampato", "quantita", "pagina", "browser"]

# Decisione 89: segni che si confondono. Si confronta tutto in maiuscolo, quindi «l» minuscola diventa «L»:
# per non perderla, anche «L» vale 1 (più permissivo della 89 alla lettera; il confronto avviene solo tra codici a
# catalogo, dove una L scambiata per 1 è rara).
_CONFUSI = str.maketrans({"O": "0", "I": "1", "L": "1", "S": "5", "B": "8", "Z": "2"})
_SEPARATORI = re.compile(r"[\s\-_./\\:,;]+")


def norma_codice(testo: str) -> str:
    """Codice normalizzato per il confronto della decisione 89: maiuscole, separatori ignorati, segni confusi uguali."""
    t = unicodedata.normalize("NFKC", testo or "").upper()
    return _SEPARATORI.sub("", t).translate(_CONFUSI)


def leggi_elenchi(privato: Path) -> list[dict]:
    """Tutte le righe degli elenchi CSV in <privato>/elenchi, una per foto, con il percorso assoluto della foto."""
    righe, visti = [], set()
    for f in sorted((privato / "elenchi").glob("*.csv")):
        with f.open(newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["file"] in visti:
                    continue
                visti.add(r["file"])
                r["percorso"] = str(privato / r["file"])
                righe.append(r)
    return righe


def leggi_sigle(privato: Path) -> dict[str, str]:
    """Tabella codice vero -> sigla anonima (A001…), che sta solo nel repository privato (129)."""
    f = privato / "sigle.csv"
    if not f.exists():
        return {}
    with f.open(newline="", encoding="utf-8") as fh:
        return {r["codice"]: r["sigla"] for r in csv.DictReader(fh)}


def categorie(righe: list[dict]) -> dict[str, str]:
    """Categoria di ogni codice: «catalogo» se ha foto di riferimento, «contorno» se ha solo la foto di contorno,
    «fuori» se ha solo foto di arrivo (i 40 articoli lasciati fuori dal catalogo, 133)."""
    tipi: dict[str, set] = {}
    for r in righe:
        tipi.setdefault(r["codice"], set()).add(r["tipo"])
    out = {}
    for codice, t in tipi.items():
        out[codice] = "catalogo" if "riferimento" in t else "contorno" if "contorno" in t else "fuori"
    return out


def riquadro(r: dict) -> tuple[float, float, float, float]:
    """Riquadro al centro della pagina di scatto, in frazioni della foto: x, y, larghezza, altezza (145)."""
    try:
        return tuple(float(r[k]) for k in ("riquadro_x", "riquadro_y", "riquadro_l", "riquadro_a"))
    except (KeyError, TypeError, ValueError):
        return (0.15, 0.15, 0.7, 0.7)


def scrivi_csv(percorso: Path, righe: list[dict], colonne: list[str]) -> None:
    percorso.parent.mkdir(parents=True, exist_ok=True)
    with percorso.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=colonne, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)
