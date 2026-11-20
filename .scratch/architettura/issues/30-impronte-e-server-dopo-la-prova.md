# Impronte e server in sede, dopo la prova

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 09, 10, 15 (10 chiuso il 20/11/2026)

## Question

Con i numeri della prova visiva: le impronte delle foto si calcolano nel browser del telefono o sul server in sede?
Con quale programma gira il modello scelto? Che macchina serve in sede (scheda grafica sì o no, memoria, sistema
operativo), alla luce dei tempi misurati nella prova (143) e delle prove su dispositivi veri (127)?

Nato dalla divisione del ticket «Divisione tra telefono, computer e server in sede» (405). Assorbe la voce «Server in
sede: requisiti minimi» della nebbia della mappa.

Risultato atteso: la scelta e i requisiti minimi del server in `docs/architettura.md` e in `docs/decisioni.md`.

## Comments
- 20/11/2026, dal ticket «Divisione tra telefono, computer e server in sede»: il confronto tra le impronte si fa sul
  server, con un elenco solo (407); la foto viaggia comunque a ogni inquadratura (408), quindi calcolare l'impronta nel
  browser toglierebbe lavoro al server ma non traffico; se si calcolerà nel browser, passerà in più l'impronta (421).
