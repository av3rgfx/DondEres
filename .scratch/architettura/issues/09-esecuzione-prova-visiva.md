# Esecuzione della prova visiva e scelta del modello

Type: task
Label: wayfinder:task
Status: open
Assignee: sessione del 17/11/2026 (Claude, con l'utente)
Blocked by: 08, 19

## Question

Eseguire la prova secondo il piano: l'utente fornisce le foto reali, l'agente prepara gli script, calcola le
impronte con i modelli scelti, misura e riporta i risultati senza abbellirli. L'utente sceglie il modello in base ai
numeri.

Tipo: task con l'utente (le foto le scatta l'utente). Risultato atteso: i numeri e il modello scelto in
`docs/architettura.md`, la scelta in `docs/decisioni.md`, la posizione delle foto e degli script annotata qui.

## Comments

- 17/11/2026, dal ticket «Piano della prova di accuratezza visiva»: il piano e la lista delle foto sono nella sezione
  «Prova di accuratezza visiva» di `docs/architettura.md` (decisioni 128–145). L'utente crea il repository privato delle
  foto e lo aggiunge alla sessione (128, 145); l'agente prepara la pagina di scatto (dal browser, su un indirizzo sicuro,
  per esempio GitHub Pages) e la fa provare prima su un telefono (136); se l'utente vuole DINOv3, serve la sua chiave di
  Hugging Face, da chiedere con il modulo sicuro, mai in chat (141). I tempi si misurano solo nella sessione (143).
  Prima di iniziare va chiuso il ticket di ricerca «Modelli visivi open source recenti: ce ne sono di migliori?», che
  può cambiare l'elenco dei modelli (140).
- 17/11/2026, dal ticket di ricerca «Modelli visivi open source recenti: ce ne sono di migliori?»: modelli della prova
  SigLIP 2 e PE-Core media e grande, DINOv2 media, TIPSv2 media, DINOv3 solo confronto (141, 146); ogni modello anche con
  il ritaglio automatico della scatola, OWLv2 (147); C-RADIO fuori (148). Il ticket è sbloccato: per partire serve il
  repository privato delle foto creato dall'utente.
