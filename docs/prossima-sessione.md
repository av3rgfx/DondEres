# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato.

```text
/wayfinder Architettura del gestionale di magazzino DondEres.

Leggi prima, in quest'ordine:
- AGENTS.md
- docs/decisioni.md: decisioni già prese, non rimetterle in discussione
- docs/analisi-progetto.md: analisi, proposta tecnica, domande aperte D1–D8, rischi
- le tre ricerche in docs/research/, da consultare quando servono e senza ripeterle

Destinazione proposta, da confermare con me: una specifica di architettura della base generica, pronta per
pianificare l'implementazione. Deve coprire:
- modello dei dati e glossario
- regole di ricevimento e di assegnazione delle scorte agli ordini
- percorso di identificazione: barcode → codice stampato → immagine
- inserimento di un articolo nuovo da foto
- divisione tra telefono, computer e server in sede
- scelta tra app nativa e web app
- punti di estensione per la specializzazione di un singolo magazzino
- piano della prova di accuratezza visiva con foto reali

La specializzazione per un magazzino specifico è fuori da questa mappa (decisione 4 in docs/decisioni.md).

Ticket in Markdown locale in .scratch/architettura/ (map.md e issues/NN-*.md), come da AGENTS.md.
Parti dalle domande aperte D1–D8 dell'analisi: D1 (regola all'arrivo), D2 (numero seriale) e D4 (fonte degli
ordini: gestionale principale o affiancato a un ERP esistente) bloccano gran parte del resto.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
```
