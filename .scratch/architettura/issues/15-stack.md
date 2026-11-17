# Stack

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 07, 09, 10, 11

## Question

Con quali linguaggi, database e programmi per il modello visivo si costruisce la base (decisione 13)? Va scelto a
partire da app nativa o web, divisione tra le macchine, modello scelto nella prova e punti di estensione. Si
riusano prima le funzioni native e le librerie mature; si guardano le licenze (analisi §4.1).

Risultato atteso: lo stack e il motivo di ogni scelta in `docs/architettura.md` e in `docs/decisioni.md`.

## Comments

- 16/11/2026, dal ticket «App nativa o web app»: niente app nativa; web app nel browser servita dal server in sede
  (121, 122). Da coprire: lettura del barcode nel browser (`BarcodeDetector` dove c'è, zxing-cpp in WebAssembly
  altrove), fotocamera solo in contesto sicuro, memoria del browser per l'operazione in corso (127), certificato del
  dominio con la sfida DNS di Let's Encrypt oppure certificato interno (123), aggiornamento del server con copia di
  sicurezza e aggiornamenti obbligatori notturni (125), lettore a grilletto del palmare come tastiera (ipotesi, 119).
  Prima di scegliere, le prove su dispositivi veri (127).
- 17/11/2026, dal ticket «Piano della prova di accuratezza visiva»: per la prova, lettura del codice stampato sul
  server con PaddleOCR (Apache-2.0), modelli visivi SigLIP 2, PE-Core e DINOv2 (Apache-2.0), DINOv3 solo come confronto
  (140–142, 145). Lo stack del riconoscimento dipende dal modello scelto nell'esecuzione della prova.
