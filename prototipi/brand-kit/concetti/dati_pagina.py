"""Scrive nella pagina delle domande (../index.html) i tracciati dei concetti, al posto del segnaposto /*DATI*/...
Uso: python3 dati_pagina.py
"""
import json, os, re
import genera as g

here = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(here, "..", "index.html")


def word(letters):
    p, w = g.word(letters, 24)
    return {"vb": f"0 0 {w + 24:g} 256", "d": p}


mp, _ = g.o_mirino(0)
data = {
    "sym": {"A": {"vb": "0 0 256 256", "d": g.sym_a()},
            "B": {"vb": "-16 88 128 128", "d": mp},
            "C": {"vb": "0 0 256 256", "d": g.sym_c()}},
    "word": {"A-tonda": word(g.WORD_VARCO),
             "A-mirino": word([(g.V_varco, 0)] + g.WORD_MIRINO[1:]),
             "B-tonda": word(g.WORD_ROUND), "B-mirino": word(g.WORD_MIRINO),
             "C-tonda": word(g.WORD_ROUND), "C-mirino": word(g.WORD_MIRINO)},
}
html = open(page).read()
blob = "/*DATI*/" + json.dumps(data, separators=(",", ":")) + "/*FINE*/"
html = re.sub(r"/\*DATI\*/.*?/\*FINE\*/", lambda m: blob, html, flags=re.S)
open(page, "w").write(html)
print("dati scritti in", os.path.normpath(page))
