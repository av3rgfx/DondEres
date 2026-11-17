"""Misura la lettura del codice stampato e della quantità con PaddleOCR (decisioni 89, 93, 142, 145, 157).

Uso: python etichette.py --privato /percorso/prova-visiva-foto --cache /percorso/cache --uscita prova-visiva/risultati/AAAA-MM-GG

Variabili d'ambiente utili: PADDLE_PDX_MODEL_SOURCE=huggingface (i modelli si scaricano da Hugging Face).

- La verità è quanto ha scritto chi scatta alla foto dell'etichetta (142).
- L'OCR legge la foto intera (il programma riceve tutta l'inquadratura); i testi letti restano in cache.
- Codice: un testo letto corrisponde se è uguale al codice dopo il confronto della 89 (segni che si confondono,
  separatori, maiuscole). Si provano le righe intere, le righe senza parole come «Art.» o «Articolo» e le parole.
- Quantità: numero accanto a una parola di quantità (93), compresa «Quantità» vista sulle etichette d'esempio.
- Foto di arrivo: si cerca il codice tra quelli di tutti gli articoli a catalogo della prova, come farà il programma;
  si conta se porta all'articolo giusto, a uno sbagliato o a nessuno.
- Nel risultato solo numeri, senza codici (129).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from comune import categorie, leggi_elenchi, norma_codice, scrivi_csv

PREFISSI = re.compile(r"^(?:ART(?:ICOLO)?|COD(?:ICE)?|REF|RIF|ITEM)\b\.?\s*:?\s*", re.I)
_NUM = r"(\d+(?:[.,]\d+)?)"
_PAROLE = r"\b(?:Q\.?\s?T[AÀ]|Q\.?\s?TY|QUANTIT[AÀ]|PZ|PCS|PEZZI|NR|N°|CONF)"
QUANTITA = [re.compile(_PAROLE + r"\.?\s*:?\s*" + _NUM),                       # «Pz.7», «Quantità 4»
            re.compile(r"(?<![\d.,])" + _NUM + r"\s*(?:PZ|PCS|PEZZI)\b(?!\s*\.?\s*\d)"),  # «50 pz», non «01.04 Pz.7»
            re.compile(r"(?:^|\s)[X×]\s*" + _NUM + r"\b")]                        # «× 12», non «125X125»


def candidati_codice(testi: list[str]) -> set[str]:
    out = set()
    for t in testi:
        for v in (t, PREFISSI.sub("", t.strip())):
            out.add(norma_codice(v))
        out.update(norma_codice(p) for p in t.split())
    out.discard("")
    return out


def numero(s: str) -> float | None:
    m = re.search(_NUM, s or "")
    return float(m.group(1).replace(",", ".")) if m else None


def quantita_lette(testi: list[str]) -> set[float]:
    unito = " ".join(testi).upper()
    vals = set()
    for rx in QUANTITA:
        for m in rx.finditer(unito):
            vals.add(float(m.group(1).replace(",", ".")))
    return vals


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--privato", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--uscita", type=Path, required=True)
    ap.add_argument("--soglia", type=float, default=0.5, help="punteggio minimo di un testo letto dall'OCR")
    a = ap.parse_args()
    a.cache.mkdir(parents=True, exist_ok=True)
    righe = leggi_elenchi(a.privato.resolve())
    cat = categorie(righe)

    # Verità: codice stampato e quantità scritti alla foto dell'etichetta (142).
    vero_codice = {r["codice"]: r["codice_stampato"].strip() for r in righe
                   if r["tipo"] == "riferimento" and r["foto"] == "etichetta" and r["codice_stampato"].strip()}
    norma_art = defaultdict(set)  # codice normalizzato -> articoli a catalogo
    for art, cod in vero_codice.items():
        norma_art[norma_codice(cod)].add(art)

    da_leggere = [r for r in righe if (r["tipo"] == "riferimento" and r["foto"] == "etichetta") or r["tipo"] == "arrivo"]
    cache_f = a.cache / "ocr.json"
    letti = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    nuovi = [r for r in da_leggere if r["file"] not in letti]
    tempi = []
    if nuovi:
        os.environ.setdefault("PADDLE_PDX_MODEL_SOURCE", "huggingface")
        from paddleocr import PaddleOCR
        # enable_mkldnn=False: con Paddle 3.3 l'accelerazione oneDNN dà NotImplementedError su questi modelli.
        # Il testo si cerca sulla foto ridotta a 1280 px di lato lungo (a piena risoluzione la memoria non basta);
        # le righe trovate si leggono poi sulla foto originale.
        ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=True,
                        enable_mkldnn=False, text_det_limit_side_len=1280, text_det_limit_type="max",
                        text_detection_model_name="PP-OCRv5_server_det",
                        text_recognition_model_name="PP-OCRv5_server_rec")
        for k, r in enumerate(nuovi, 1):
            t0 = time.perf_counter()
            res = ocr.predict(r["percorso"])[0]
            tempi.append(time.perf_counter() - t0)
            letti[r["file"]] = [[t, float(s)] for t, s in zip(res["rec_texts"], res["rec_scores"])]
            if k % 20 == 0:
                cache_f.write_text(json.dumps(letti))
                print(f"OCR: {k} di {len(nuovi)}")
        cache_f.write_text(json.dumps(letti))

    def testi(f: str) -> list[str]:
        return [t for t, s in letti.get(f, []) if s >= a.soglia]

    # Foto di riferimento dell'etichetta: codice e quantità.
    cod_esito, qta_esito = Counter(), Counter()
    for r in righe:
        if not (r["tipo"] == "riferimento" and r["foto"] == "etichetta"):
            continue
        tt = testi(r["file"])
        if r["codice_stampato"].strip():
            cod_esito["letto" if norma_codice(r["codice_stampato"]) in candidati_codice(tt) else "non letto"] += 1
        else:
            cod_esito["nessun codice sulla scatola"] += 1
        q = numero(r["quantita"])
        if q is not None:
            lette = quantita_lette(tt)
            qta_esito["giusta" if lette == {q} else "due o più numeri, c'è la giusta" if q in lette
                      else "sbagliata" if lette else "non letta"] += 1
        else:
            qta_esito["nessuna quantità sulla scatola"] += 1

    # Foto di arrivo: identificazione dal codice stampato tra gli articoli a catalogo della prova.
    arr_esito, per_disp = Counter(), defaultdict(Counter)
    for r in righe:
        if r["tipo"] != "arrivo":
            continue
        trovati = set()
        for c in candidati_codice(testi(r["file"])):
            trovati |= norma_art.get(c, set())
        if cat[r["codice"]] == "fuori":
            e = "fuori catalogo: nessun codice (giusto)" if not trovati else "fuori catalogo: portato a un articolo (sbagliato)"
        elif r["codice"] not in vero_codice:
            e = "a catalogo senza codice stampato"
        elif trovati == {r["codice"]}:
            e = "giusto"
        elif r["codice"] in trovati:
            e = "giusto tra più articoli"
        elif trovati:
            e = "sbagliato"
        else:
            e = "codice non trovato"
        arr_esito[e] += 1
        per_disp[f"{r['tipo_dispositivo']} {r['dispositivo']}"][e] += 1

    def tabella(titolo: str, c: Counter) -> list[str]:
        tot = sum(c.values())
        out = [f"\n## {titolo}\n", "| Esito | Foto | % |", "|---|---|---|"]
        out += [f"| {k} | {v} | {100 * v / tot:.1f} |" for k, v in c.most_common()]
        return out

    md = ["# Lettura di codice stampato e quantità\n",
          "PaddleOCR PP-OCRv5 server, foto intera, testi con punteggio almeno "
          f"{a.soglia}. Confronto del codice come nella decisione 89; quantità con le parole della 93."]
    if tempi:
        md.append(f"\nTempo dell'OCR su CPU di questa sessione: {sum(tempi) / len(tempi):.1f} s per foto "
                  f"({len(tempi)} foto nuove).")
    md += tabella("Codice sulla foto dell'etichetta", cod_esito)
    md += tabella("Quantità sulla foto dell'etichetta", qta_esito)
    md += tabella("Foto di arrivo: articolo trovato dal codice stampato", arr_esito)
    md.append("\n## Foto di arrivo per dispositivo\n")
    md.append("| Dispositivo | Giusto | Foto con codice stampato | % |")
    md.append("|---|---|---|---|")
    for d, c in sorted(per_disp.items()):
        con = sum(v for k, v in c.items() if not k.startswith("fuori") and k != "a catalogo senza codice stampato")
        md.append(f"| {d} | {c['giusto']} | {con} | {100 * c['giusto'] / con:.1f} |" if con else f"| {d} | 0 | 0 | — |")
    a.uscita.mkdir(parents=True, exist_ok=True)
    (a.uscita / "etichette.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    scrivi_csv(a.uscita / "etichette.csv",
               [{"misura": m, "esito": k, "foto": v} for m, c in (("codice_etichetta", cod_esito), ("quantita_etichetta", qta_esito),
                                                                   ("arrivo_dal_codice", arr_esito)) for k, v in c.items()],
               ["misura", "esito", "foto"])
    print(f"Scritto {a.uscita / 'etichette.md'}")


if __name__ == "__main__":
    main()
