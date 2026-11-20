"""Scrive nella pagina delle domande (../index.html) i tracciati del giro 3, al posto di /*DATI*/.../*FINE*/.
Aggiunge il nome del giro 2 (scartato) per il confronto. Uso: python3 genera.py && python3 dati_pagina.py
"""
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "concetti"))
import genera as vecchio          # concetti del giro 2

data = json.load(open(os.path.join(here, "dati.json")))
p, w = vecchio.word(vecchio.WORD_ROUND, 24)
data["old"] = {"vb": f"0 0 {w + 24:g} 256", "d": p}
page = os.path.join(here, "..", "index.html")
html = open(page).read()
blob = "/*DATI*/" + json.dumps(data, separators=(",", ":")) + "/*FINE*/"
open(page, "w").write(re.sub(r"/\*DATI\*/.*?/\*FINE\*/", lambda m: blob, html, flags=re.S))
print("dati scritti in", os.path.normpath(page))
