"""Apre gli ZIP della pagina di scatto e sistema le foto nel repository privato (decisione 153).

Uso: python prepara.py --privato /percorso/prova-visiva-foto

- Legge <privato>/da-caricare/*.zip; mette le foto in riferimento/, arrivo/, contorno/ e gli elenchi in elenchi/.
- Toglie gli ZIP aperti senza errori (il commit lo fa chi lancia lo script).
- Aggiorna <privato>/sigle.csv: a ogni codice nuovo dà la sigla anonima successiva (A001, A002…, 129).
- Stampa un riepilogo e gli avvisi: foto senza riga d'elenco, righe senza foto, articoli incompleti.
"""
from __future__ import annotations

import argparse
import csv
import io
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

from comune import TIPI, categorie, leggi_elenchi, leggi_sigle, scrivi_csv


def percorso_sicuro(nome: str) -> PurePosixPath | None:
    """Accetta solo <tipo>/<file>.jpg o elenco_*.csv, senza percorsi assoluti o «..»."""
    p = PurePosixPath(nome)
    if p.is_absolute() or ".." in p.parts:
        return None
    if len(p.parts) == 2 and p.parts[0] in TIPI and p.suffix.lower() == ".jpg":
        return p
    if len(p.parts) == 1 and p.name.startswith("elenco_") and p.suffix.lower() == ".csv":
        return PurePosixPath("elenchi") / p.name
    return None


def apri_zip(zf_path: Path, privato: Path) -> tuple[int, list[str], bool]:
    """Restituisce i file nuovi, gli avvisi e se lo ZIP si può togliere (nessun file rovinato o in conflitto)."""
    avvisi, nuove, pulito = [], 0, True
    with zipfile.ZipFile(zf_path) as zf:
        bad = zf.testzip()
        if bad:
            return 0, [f"{zf_path.name}: file rovinato nello ZIP ({bad}); ZIP lasciato dov'è"], False
        for info in zf.infolist():
            if info.is_dir():
                continue
            dest = percorso_sicuro(info.filename)
            if dest is None:
                avvisi.append(f"{zf_path.name}: ignorato {info.filename!r} (percorso non previsto)")
                continue
            data = zf.read(info)
            if dest.suffix == ".csv":
                intest = next(csv.reader(io.StringIO(data.decode("utf-8"))))
                mancanti = [c for c in ("file", "codice", "tipo", "foto") if c not in intest]
                if mancanti:
                    avvisi.append(f"{zf_path.name}: elenco {dest.name} senza le colonne {mancanti}; ZIP lasciato dov'è")
                    pulito = False
                    continue
            target = privato / dest
            if target.exists():
                if target.read_bytes() != data:
                    avvisi.append(f"{zf_path.name}: {dest} esiste già con un contenuto diverso; lasciato com'era, "
                                  "e ZIP lasciato dov'è")
                    pulito = False
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            nuove += 1
    return nuove, avvisi, pulito


def aggiorna_sigle(privato: Path, righe: list[dict]) -> int:
    sigle = leggi_sigle(privato)
    n = len(sigle)
    for r in righe:  # ordine di prima comparsa negli elenchi
        if r["codice"] not in sigle:
            n += 1
            sigle[r["codice"]] = f"A{n:03d}"
    scrivi_csv(privato / "sigle.csv", [{"codice": c, "sigla": s} for c, s in sigle.items()], ["codice", "sigla"])
    return n


def controlla(privato: Path, righe: list[dict]) -> list[str]:
    avvisi = []
    elencate = {r["file"] for r in righe}
    for tipo in TIPI:
        for f in sorted((privato / tipo).glob("*.jpg")) if (privato / tipo).exists() else []:
            if f"{tipo}/{f.name}" not in elencate:
                avvisi.append(f"foto senza riga d'elenco: {tipo}/{f.name}")
    for r in righe:
        if not Path(r["percorso"]).exists():
            avvisi.append(f"riga d'elenco senza foto: {r['file']}")
    cat = categorie(righe)
    rif = Counter((r["codice"], r["foto"]) for r in righe if r["tipo"] == "riferimento")
    for codice, c in cat.items():
        if c == "catalogo":
            manca = [f for f in ("davanti", "etichetta", "altro-lato") if rif[(codice, f)] == 0]
            if manca:
                avvisi.append(f"articolo a catalogo senza le foto di riferimento {manca}: {codice}")
    tipi_per_codice: dict[str, set] = {}
    for r in righe:
        tipi_per_codice.setdefault(r["codice"], set()).add(r["tipo"])
    for codice, t in tipi_per_codice.items():
        if "contorno" in t and len(t) > 1:
            avvisi.append(f"articolo di contorno con anche foto di {sorted(t - {'contorno'})}: {codice}")
    return avvisi


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--privato", type=Path, required=True, help="cartella del repository privato delle foto")
    ap.add_argument("--tieni-zip", action="store_true", help="non togliere gli ZIP dopo averli aperti")
    a = ap.parse_args()
    privato = a.privato.resolve()

    avvisi, nuove = [], 0
    for zf in sorted((privato / "da-caricare").glob("*.zip")):
        n, avv, pulito = apri_zip(zf, privato)
        nuove += n
        avvisi += avv
        if pulito and not a.tieni_zip:
            zf.unlink()
        print(f"{zf.name}: {n} file nuovi")

    righe = leggi_elenchi(privato)
    n_sigle = aggiorna_sigle(privato, righe) if righe else 0
    avvisi += controlla(privato, righe)

    cat = categorie(righe)
    print(f"\nFile nuovi: {nuove}. Foto in elenco: {len(righe)}. Sigle: {n_sigle}.")
    print("Articoli per categoria:", dict(Counter(cat.values())), "(obiettivo: catalogo 200, fuori 40, contorno 300)")
    print("Foto per tipo:", dict(Counter(r["tipo"] for r in righe)))
    print("Foto di arrivo per dispositivo:", dict(Counter(r["tipo_dispositivo"] for r in righe if r["tipo"] == "arrivo")))
    arr = Counter(r["codice"] for r in righe if r["tipo"] == "arrivo")
    print("Articoli a catalogo o fuori con almeno 3 foto di arrivo:",
          sum(1 for c, k in cat.items() if k != "contorno" and arr[c] >= 3), "di", sum(1 for k in cat.values() if k != "contorno"))
    if avvisi:
        print(f"\nAvvisi ({len(avvisi)}):")
        for x in avvisi:
            print(" -", x)


if __name__ == "__main__":
    main()
