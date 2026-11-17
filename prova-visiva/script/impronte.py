"""Calcola le impronte (embedding) delle foto con i modelli della prova e misura i tempi (decisioni 143, 146, 147).

Uso: python impronte.py --privato /percorso/prova-visiva-foto --cache /percorso/cache [--modelli siglip2-b,...]
     [--ritagli riquadro,owlv2] [--fili 4]

- Ritaglio «riquadro»: il riquadro al centro della pagina di scatto (145).
- Ritaglio «owlv2»: OWLv2 senza testo trova gli oggetti nella foto; si tiene l'oggetto più probabile con il centro
  dentro il riquadro e almeno il 5% della foto, con un margine del 5%; se non c'è, si usa il riquadro (147).
- Le impronte (normalizzate, float16) e i riquadri di OWLv2 vanno nella cartella --cache, fuori dai repository:
  si ricalcolano quando servono. Uno .npz per modello e ritaglio; le foto già fatte si saltano.
- I tempi sono misurati su questa macchina (CPU), una foto per volta: servono solo a confrontare i modelli (143).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps

from comune import leggi_elenchi, riquadro

# Decisione 146: SigLIP 2 e PE-Core media (B) e grande (L), DINOv2 media, TIPSv2 media. Tutti Apache-2.0, da timm.
MODELLI = {
    "siglip2-b": "vit_base_patch16_siglip_512.v2_webli",
    "siglip2-l": "vit_large_patch16_siglip_512.v2_webli",
    "pecore-b": "vit_pe_core_base_patch16_224.fb",
    "pecore-l": "vit_pe_core_large_patch14_336.fb",
    "dinov2-b": "vit_base_patch14_dinov2.lvd142m",
    "tipsv2-b": "vit_base_patch14_reg1_tipsv2.webli",
}
OWLV2 = "google/owlv2-base-patch16-ensemble"


def apri(percorso: str) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(percorso)).convert("RGB")


def taglia(img: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    """box in frazioni: x, y, larghezza, altezza."""
    w, h = img.size
    x, y, bw, bh = box
    l, t = max(0, round(x * w)), max(0, round(y * h))
    r, b = min(w, round((x + bw) * w)), min(h, round((y + bh) * h))
    return img.crop((l, t, r, b)) if r - l > 8 and b - t > 8 else img


class RitaglioOwl:
    """OWLv2 usato solo per l'«objectness»: nessun testo, nessun addestramento."""

    def __init__(self, cache: Path):
        from transformers import Owlv2ForObjectDetection, Owlv2Processor
        self.proc = Owlv2Processor.from_pretrained(OWLV2)
        self.model = Owlv2ForObjectDetection.from_pretrained(OWLV2).eval()
        self.file = cache / "owlv2-riquadri.json"
        self.box = json.loads(self.file.read_text()) if self.file.exists() else {}
        self.tempi: list[float] = []

    @torch.inference_mode()
    def trova(self, chiave: str, img: Image.Image, riq: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        if chiave in self.box:
            return tuple(self.box[chiave])
        t0 = time.perf_counter()
        w, h = img.size
        s = max(w, h)
        quad = Image.new("RGB", (s, s), (128, 128, 128))  # OWLv2 lavora su un quadrato riempito in basso e a destra
        quad.paste(img, (0, 0))
        # Il testo è obbligatorio per la chiamata ma non conta: si usa solo il punteggio «è un oggetto».
        inp = self.proc(text=[["an object"]], images=quad, return_tensors="pt")
        out = self.model(**inp)
        obj = out.objectness_logits[0].sigmoid()                             # probabilità che sia un oggetto
        cx, cy, bw, bh = out.pred_boxes[0].unbind(-1)                        # frazioni del quadrato
        cx, cy, bw, bh = cx * s / w, cy * s / h, bw * s / w, bh * s / h     # frazioni della foto
        rx, ry, rw, rh = riq
        ok = (cx > rx) & (cx < rx + rw) & (cy > ry) & (cy < ry + rh) & (bw * bh > 0.05)
        best = None
        if ok.any():
            i = int(torch.where(ok, obj, torch.full_like(obj, -1)).argmax())
            m = 0.05
            x0 = max(0.0, float(cx[i] - bw[i] / 2) - m * float(bw[i]))
            y0 = max(0.0, float(cy[i] - bh[i] / 2) - m * float(bh[i]))
            x1 = min(1.0, float(cx[i] + bw[i] / 2) + m * float(bw[i]))
            y1 = min(1.0, float(cy[i] + bh[i] / 2) + m * float(bh[i]))
            best = (x0, y0, x1 - x0, y1 - y0)
        self.tempi.append(time.perf_counter() - t0)
        self.box[chiave] = list(best or riq)
        return self.box[chiave]

    def salva(self) -> None:
        self.file.write_text(json.dumps(self.box))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--privato", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--modelli", default=",".join(MODELLI))
    ap.add_argument("--ritagli", default="riquadro,owlv2")
    ap.add_argument("--fili", type=int, default=4, help="thread della CPU")
    a = ap.parse_args()
    torch.set_num_threads(a.fili)
    a.cache.mkdir(parents=True, exist_ok=True)
    import timm

    righe = leggi_elenchi(a.privato.resolve())
    if not righe:
        raise SystemExit("Nessuna foto negli elenchi: lancia prima prepara.py")
    ritagli = a.ritagli.split(",")
    owl = RitaglioOwl(a.cache) if "owlv2" in ritagli else None
    box: dict[str, dict[str, tuple]] = {k: {} for k in ritagli}
    for r in righe:
        riq = riquadro(r)
        if "riquadro" in box:
            box["riquadro"][r["file"]] = riq
        if owl:
            box["owlv2"][r["file"]] = owl.trova(r["file"], apri(r["percorso"]), riq)
    if owl:
        owl.salva()
        print(f"OWLv2: {len(owl.tempi)} foto nuove, {1000 * np.mean(owl.tempi) if owl.tempi else 0:.0f} ms per foto")

    tempi_file = a.cache / "tempi.json"
    tempi = json.loads(tempi_file.read_text()) if tempi_file.exists() else {}
    if owl and owl.tempi:
        tempi["owlv2"] = {"ms_per_foto": 1000 * float(np.mean(owl.tempi)), "foto": len(owl.tempi), "fili": a.fili}
        tempi_file.write_text(json.dumps(tempi, indent=1))  # subito: se un modello dopo si ferma, il tempo resta

    for nome in a.modelli.split(","):
        model = timm.create_model(MODELLI[nome], pretrained=True, num_classes=0).eval()
        cfg = timm.data.resolve_model_data_config(model)
        tf = timm.data.create_transform(**cfg, is_training=False)
        for rit in ritagli:
            out = a.cache / f"{nome}__{rit}.npz"
            fatti = dict(np.load(out, allow_pickle=False)) if out.exists() else {}
            files = list(fatti.get("foto", np.array([], dtype=str)))
            vec = list(fatti.get("vettori", np.zeros((0, 0), dtype=np.float16)))
            nuovi = [r for r in righe if r["file"] not in set(files)]
            ms = []
            with torch.inference_mode():
                for r in nuovi:
                    img = taglia(apri(r["percorso"]), box[rit][r["file"]])
                    t0 = time.perf_counter()
                    v = model(tf(img).unsqueeze(0))[0]
                    ms.append(1000 * (time.perf_counter() - t0))
                    v = torch.nn.functional.normalize(v.float(), dim=0)
                    files.append(r["file"])
                    vec.append(v.numpy().astype(np.float16))
            if nuovi:
                np.savez(out, foto=np.array(files), vettori=np.stack(vec))
                # la prima foto paga il riscaldamento del modello: non conta nei tempi
                ms_utili = ms[1:] if len(ms) > 1 else ms
                tempi[f"{nome}__{rit}"] = {"ms_per_foto": float(np.median(ms_utili)), "foto": len(ms_utili),
                                            "fili": a.fili, "risoluzione": list(cfg["input_size"][1:]),
                                            "modello_timm": MODELLI[nome]}
            print(f"{nome} {rit}: {len(nuovi)} foto nuove, {len(files)} in tutto"
                  + (f", {np.median(ms[1:] if len(ms) > 1 else ms):.0f} ms per foto" if ms else ""))
        del model
    tempi_file.write_text(json.dumps(tempi, indent=1))


if __name__ == "__main__":
    main()
