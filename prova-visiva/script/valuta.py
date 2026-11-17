"""Calcola i numeri della prova sull'aspetto e scrive i risultati con le sole sigle anonime (decisioni 135-147).

Uso: python valuta.py --privato /percorso/prova-visiva-foto --cache /percorso/cache --uscita prova-visiva/risultati/AAAA-MM-GG

Cosa misura, per ogni modello e ritaglio (riquadro o OWLv2), con 1 foto di riferimento (davanti) e con 3:
- articolo giusto al primo posto e tra le prime 5 proposte, con 20, 100, 200 e 500 articoli attesi (138, 139):
  per ogni foto di arrivo si pesca a caso tra gli altri articoli (di contorno compresi), più volte (--ripetizioni);
- lo stesso con 100 attesi, diviso per dispositivo (137);
- le soglie (145): le foto di arrivo si dividono a caso in due metà per articolo; sulla prima si scelgono la soglia
  dell'articolo «convincente» tra gli attesi (88) e quella del «non lo so» (24), le più severe che rispettano ancora
  il traguardo (144); sulla seconda si controllano, e valgono quei numeri.

Come si usa una soglia (deduzione, coerente con 88 e 24): se il migliore tra gli attesi supera la soglia
«convincente», le 5 proposte vengono dagli attesi; altrimenti si cerca in tutto il catalogo della prova. Se il
punteggio migliore che resta è sotto la soglia «non lo so», il programma dice «non lo so». Il punteggio di un articolo
è la somiglianza più alta tra la foto di arrivo e le sue foto di riferimento.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from comune import categorie, leggi_elenchi, leggi_sigle, scrivi_csv

TRAGUARDO = 0.95  # 144: con 100 attesi, giusto tra le 5 proposte in almeno 95 arrivi su 100


def wilson(p: float, n: int) -> tuple[float, float]:
    """Intervallo al 95% per una proporzione su n foto (le ripetizioni non aggiungono informazione)."""
    if n == 0:
        return (float("nan"), float("nan"))
    z = 1.96
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, c - m), min(1.0, c + m))


def carica(cache: Path, nome: str) -> dict[str, np.ndarray]:
    d = np.load(cache / f"{nome}.npz", allow_pickle=False)
    return {f: v.astype(np.float32) for f, v in zip(d["foto"], d["vettori"])}


def punteggi(vett: dict, arrivi: list[dict], galleria: list[str], rif: dict[str, list[str]]) -> np.ndarray:
    """S[i, j] = somiglianza più alta tra la foto di arrivo i e le foto di riferimento dell'articolo j."""
    Q = np.stack([vett[r["file"]] for r in arrivi])
    files, gruppo = [], []
    for j, c in enumerate(galleria):
        for f in rif[c]:
            files.append(f)
            gruppo.append(j)
    R = np.stack([vett[f] for f in files])
    D = Q @ R.T
    S = np.full((len(arrivi), len(galleria)), -np.inf, dtype=np.float32)
    for k, j in enumerate(gruppo):
        S[:, j] = np.maximum(S[:, j], D[:, k])
    return S


def simula(S: np.ndarray, vero: np.ndarray, N: int, ripetizioni: int, rng: np.random.Generator) -> dict:
    """Per ogni arrivo e ripetizione: rango del vero tra N attesi (il vero più N-1 pescati) e statistiche per le soglie.
    vero[i] = indice dell'articolo giusto, oppure -1 per gli articoli fuori catalogo."""
    n, G = S.shape
    N = min(N, G)
    out = {k: np.zeros((n, ripetizioni), dtype=np.float32) for k in ("rango", "bestE", "bestNE")}
    for i in range(n):
        t = vero[i]
        for r in range(ripetizioni):
            pesca = rng.random(G)
            if t >= 0:
                pesca[t] = np.inf
                altri = np.argpartition(pesca, N - 1)[: N - 1]
                st = S[i, t]
                out["rango"][i, r] = np.sum(S[i, altri] > st)
                out["bestE"][i, r] = max(st, S[i, altri].max()) if N > 1 else st
                out["bestNE"][i, r] = S[i, altri].max() if N > 1 else -np.inf  # attesi senza il vero
            else:
                scelti = np.argpartition(pesca, N - 1)[:N]
                out["bestE"][i, r] = S[i, scelti].max()
    best_g = S.max(axis=1)
    rango_g = np.array([np.sum(S[i] > S[i, t]) if t >= 0 else -1 for i, t in enumerate(vero)])
    out["bestG"] = np.repeat(best_g[:, None], ripetizioni, axis=1)
    out["top5G"] = np.repeat((rango_g < 5)[:, None] & (vero >= 0)[:, None], ripetizioni, axis=1)
    out["N"] = N
    return out


def esito(sim: dict, dentro: np.ndarray, tc: float, tn: float) -> dict:
    """Risultato con le soglie per gli arrivi a catalogo (dentro=True) e fuori catalogo (dentro=False)."""
    top5E = sim["rango"] < 5
    conv = sim["bestE"] >= tc
    finale = np.where(conv, sim["bestE"], sim["bestG"])
    nls = finale < tn
    giusto = np.where(conv, top5E, sim["top5G"]) & ~nls
    d, f = dentro, ~dentro
    return {
        "giusto_tra_5": float(giusto[d].mean()) if d.any() else float("nan"),
        "non_lo_so_a_catalogo": float(nls[d].mean()) if d.any() else float("nan"),
        "ricerca_in_tutto": float((~conv[d]).mean()) if d.any() else float("nan"),
        "non_lo_so_fuori": float(nls[f].mean()) if f.any() else float("nan"),
        "convinto_sbagliato_non_atteso": float((sim["bestNE"][d] >= tc).mean()) if d.any() else float("nan"),
    }


def scegli_soglie(sim: dict, dentro: np.ndarray) -> tuple[float, float, bool]:
    """Le soglie più severe che rispettano il traguardo sulla prima metà; prima «convincente», poi «non lo so»."""
    if not dentro.any():
        return (-np.inf, -np.inf, False)
    valori = np.unique(np.quantile(np.concatenate([sim["bestE"][dentro].ravel(), sim["bestG"][dentro].ravel()]),
                                   np.linspace(0, 1, 401)))
    if esito(sim, dentro, -np.inf, -np.inf)["giusto_tra_5"] < TRAGUARDO:
        return (-np.inf, -np.inf, False)
    tc = max([v for v in valori if esito(sim, dentro, v, -np.inf)["giusto_tra_5"] >= TRAGUARDO], default=-np.inf)
    tn = max([v for v in valori if esito(sim, dentro, tc, v)["giusto_tra_5"] >= TRAGUARDO], default=-np.inf)
    return (float(tc), float(tn), True)


def pct(x: float) -> str:
    return "—" if x != x else f"{100 * x:.1f}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--privato", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--uscita", type=Path, required=True)
    ap.add_argument("--attesi", default="20,100,200,500")
    ap.add_argument("--ripetizioni", type=int, default=20)
    ap.add_argument("--seme", type=int, default=2026)
    a = ap.parse_args()
    privato = a.privato.resolve()

    righe = leggi_elenchi(privato)
    sigle = leggi_sigle(privato)
    cat = categorie(righe)
    galleria = sorted(c for c, k in cat.items() if k in ("catalogo", "contorno"))
    gi = {c: j for j, c in enumerate(galleria)}
    rif1, rif3 = defaultdict(list), defaultdict(list)
    for r in righe:
        if r["tipo"] == "riferimento":
            rif3[r["codice"]].append(r["file"])
            if r["foto"] == "davanti":
                rif1[r["codice"]].append(r["file"])
        elif r["tipo"] == "contorno":
            rif1[r["codice"]].append(r["file"])
            rif3[r["codice"]].append(r["file"])
    galleria = [c for c in galleria if rif1[c]]  # senza foto davanti l'articolo non entra
    gi = {c: j for j, c in enumerate(galleria)}
    arrivi = [r for r in righe if r["tipo"] == "arrivo" and (cat[r["codice"]] == "fuori" or r["codice"] in gi)]
    vero = np.array([gi.get(r["codice"], -1) if cat[r["codice"]] == "catalogo" else -1 for r in arrivi])
    dentro = vero >= 0

    rng = np.random.default_rng(a.seme)
    codici_arrivo = sorted({r["codice"] for r in arrivi})
    prima = set(rng.permutation(codici_arrivo)[: len(codici_arrivo) // 2].tolist())
    meta_a = np.array([r["codice"] in prima for r in arrivi])

    richiesti = [int(x) for x in a.attesi.split(",")]
    lista_attesi = sorted({min(n, len(galleria)) for n in richiesti})  # con un catalogo piccolo i casi si fondono
    centrale = min(100, len(galleria))  # il caso del traguardo (144)
    tempi = json.loads((a.cache / "tempi.json").read_text()) if (a.cache / "tempi.json").exists() else {}
    combinazioni = sorted(p.stem for p in a.cache.glob("*__*.npz"))

    righe_csv, md = [], []
    oggi = dt.date.today().isoformat()
    n_cat_arr = int(dentro.sum())
    md.append(f"# Risultati della prova visiva · {oggi}\n")
    md.append(f"Articoli: {sum(1 for k in cat.values() if k == 'catalogo')} a catalogo, "
              f"{sum(1 for k in cat.values() if k == 'fuori')} fuori catalogo, "
              f"{sum(1 for k in cat.values() if k == 'contorno')} di contorno. "
              f"Foto di arrivo: {n_cat_arr} di articoli a catalogo, {int((~dentro).sum())} fuori catalogo. "
              f"Ripetizioni per foto: {a.ripetizioni}; seme {a.seme}. Traguardo: {int(TRAGUARDO * 100)} su 100 (144).\n")
    if len(galleria) < max(richiesti):
        md.append(f"Attenzione: il catalogo della prova ha solo {len(galleria)} articoli; i casi con più attesi "
                  f"sono limitati a {len(galleria)}.\n")

    sintesi, per_disp, peggiori = [], [], defaultdict(list)
    for comb in combinazioni:
        modello, ritaglio = comb.split("__")
        vett = carica(a.cache, comb)
        mancanti = [r["file"] for r in righe if r["file"] not in vett]
        if mancanti:
            md.append(f"{comb}: {len(mancanti)} foto senza impronta, combinazione saltata (rilancia impronte.py).\n")
            continue
        for nrif, rif in (("1", rif1), ("3", rif3)):
            S = punteggi(vett, arrivi, galleria, rif)
            for N in lista_attesi:
                sim = simula(S, vero, N, a.ripetizioni, np.random.default_rng(a.seme + N))
                top1 = float((sim["rango"][dentro] < 1).mean()) if dentro.any() else float("nan")
                top5 = float((sim["rango"][dentro] < 5).mean()) if dentro.any() else float("nan")
                lo, hi = wilson(top5, n_cat_arr)  # intervallo sul numero di foto, non sulle ripetizioni
                righe_csv.append({"modello": modello, "ritaglio": ritaglio, "foto_riferimento": nrif, "attesi": sim["N"],
                                  "dispositivo": "tutti", "primo_posto": round(top1, 4), "tra_5": round(top5, 4),
                                  "tra_5_min95": round(lo, 4), "tra_5_max95": round(hi, 4), "foto_arrivo": n_cat_arr})
                if N != centrale:
                    continue
                for disp in sorted({r["tipo_dispositivo"] + " " + r["dispositivo"] for r in arrivi}):
                    m = dentro & np.array([r["tipo_dispositivo"] + " " + r["dispositivo"] == disp for r in arrivi])
                    if m.any():
                        t5 = float((sim["rango"][m] < 5).mean())
                        per_disp.append((modello, ritaglio, nrif, disp, int(m.sum()), t5))
                        righe_csv.append({"modello": modello, "ritaglio": ritaglio, "foto_riferimento": nrif,
                                          "attesi": sim["N"], "dispositivo": disp,
                                          "primo_posto": round(float((sim["rango"][m] < 1).mean()), 4),
                                          "tra_5": round(t5, 4), "foto_arrivo": int(m.sum())})
                tc, tn, ok = scegli_soglie(sim, dentro & meta_a)
                sel_b = ~meta_a
                sim_b = {k: (v[sel_b] if isinstance(v, np.ndarray) else v) for k, v in sim.items()}
                e = esito(sim_b, dentro[sel_b], tc, tn)
                n_b = int((dentro & sel_b).sum())
                tm = tempi.get(comb, {})
                sintesi.append({"modello": modello, "ritaglio": ritaglio, "foto_riferimento": nrif,
                                "tra_5_100": top5, "primo_100": top1, "soglie_ok": ok, "tc": tc, "tn": tn,
                                "foto_b": n_b, "ms": tm.get("ms_per_foto"), **e})
                for i in np.where(dentro)[0]:
                    peggiori[(modello, ritaglio, nrif)].append((sigle.get(arrivi[i]["codice"], "?"),
                                                                 float((sim["rango"][i] < 5).mean())))

    md.append(f"\n## Sintesi con {centrale} articoli attesi\n")
    md.append("«Tra 5» e «primo» su tutte le foto di arrivo, senza soglie. Le colonne con le soglie valgono sulla "
              "seconda metà delle foto (145). Tempi su CPU di questa sessione, una foto per volta (143): solo per "
              "confrontare i modelli.\n")
    md.append("| Modello | Ritaglio | Foto rif. | Tra 5 % | Primo % | Traguardo con le soglie | Giusto tra 5 con soglie % "
              "| «Non lo so» fuori catalogo % | «Non lo so» a catalogo % | Ricerca in tutto % | Convinto e sbagliato % | ms per foto |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s in sorted(sintesi, key=lambda s: -s["tra_5_100"]):
        trag = ("non raggiunto" if not s["soglie_ok"] else
                "sì" if s["giusto_tra_5"] >= TRAGUARDO else "no sulla seconda metà")
        md.append(f"| {s['modello']} | {s['ritaglio']} | {s['foto_riferimento']} | {pct(s['tra_5_100'])} | "
                  f"{pct(s['primo_100'])} | {trag} | {pct(s['giusto_tra_5'])} | {pct(s['non_lo_so_fuori'])} | "
                  f"{pct(s['non_lo_so_a_catalogo'])} | {pct(s['ricerca_in_tutto'])} | "
                  f"{pct(s['convinto_sbagliato_non_atteso'])} | {'—' if s['ms'] is None else round(s['ms'])} |")
    if "owlv2" in tempi:
        md.append(f"\nRitaglio OWLv2: {round(tempi['owlv2']['ms_per_foto'])} ms per foto in più, una volta per foto.\n")

    md.append("\n## Articoli attesi\n")
    md.append(f"Articolo giusto tra le prime 5 proposte (%), con l'intervallo al 95% per {centrale} attesi.\n")
    attesi_eff = sorted({r["attesi"] for r in righe_csv})
    md.append("| Modello | Ritaglio | Foto rif. | " + " | ".join(f"{n} attesi" for n in attesi_eff) + " |")
    md.append("|---|---|---|" + "---|" * len(attesi_eff))
    chiavi = sorted({(r["modello"], r["ritaglio"], r["foto_riferimento"]) for r in righe_csv})
    for k in chiavi:
        celle = []
        for n in attesi_eff:
            r = next((r for r in righe_csv if (r["modello"], r["ritaglio"], r["foto_riferimento"]) == k
                      and r["attesi"] == n and r["dispositivo"] == "tutti"), None)
            celle.append("—" if r is None else pct(r["tra_5"]) + (f" ({pct(r['tra_5_min95'])}–{pct(r['tra_5_max95'])})" if n == centrale else ""))
        md.append(f"| {k[0]} | {k[1]} | {k[2]} | " + " | ".join(celle) + " |")

    md.append(f"\n## Per dispositivo, {centrale} attesi\n")
    md.append("| Modello | Ritaglio | Foto rif. | Dispositivo | Foto di arrivo | Tra 5 % |")
    md.append("|---|---|---|---|---|---|")
    for m_, r_, n_, d_, k_, t_ in per_disp:
        md.append(f"| {m_} | {r_} | {n_} | {d_} | {k_} | {pct(t_)} |")

    if sintesi:
        migliore = max(sintesi, key=lambda s: s["tra_5_100"])
        k = (migliore["modello"], migliore["ritaglio"], migliore["foto_riferimento"])
        per_art = defaultdict(list)
        for sig, v in peggiori[k]:
            per_art[sig].append(v)
        dieci = sorted(per_art.items(), key=lambda kv: np.mean(kv[1]))[:10]
        md.append(f"\n## Articoli più difficili per {k[0]} {k[1]} con {k[2]} foto (sigle anonime)\n")
        md.append("Da guardare nel repository privato con la tabella delle sigle.\n")
        md.append("| Sigla | Foto di arrivo | Tra 5 % |")
        md.append("|---|---|---|")
        for sig, v in dieci:
            md.append(f"| {sig} | {len(v)} | {pct(float(np.mean(v)))} |")

    a.uscita.mkdir(parents=True, exist_ok=True)
    (a.uscita / "risultati.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    scrivi_csv(a.uscita / "risultati.csv", righe_csv, ["modello", "ritaglio", "foto_riferimento", "attesi", "dispositivo",
                                                       "primo_posto", "tra_5", "tra_5_min95", "tra_5_max95", "foto_arrivo"])
    scrivi_csv(a.uscita / "soglie.csv", [{k: v for k, v in s.items()} for s in sintesi],
               ["modello", "ritaglio", "foto_riferimento", "tra_5_100", "primo_100", "soglie_ok", "tc", "tn", "foto_b", "ms",
                "giusto_tra_5", "non_lo_so_fuori", "non_lo_so_a_catalogo", "ricerca_in_tutto", "convinto_sbagliato_non_atteso"])
    print(f"Scritto {a.uscita / 'risultati.md'}")


if __name__ == "__main__":
    main()
