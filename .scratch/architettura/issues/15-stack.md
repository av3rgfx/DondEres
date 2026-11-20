# Stack

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 07, 10, 11 (tutti chiusi; 10 il 20/11/2026). Non aspetta più la prova visiva (decisione 405).

## Question

Con quali linguaggi, database e programmi si costruisce la base (decisione 13)? Va scelto a
partire da app nativa o web, divisione tra le macchine e punti di estensione. Il programma che fa girare il modello
visivo si sceglie nel ticket «Impronte e server in sede, dopo la prova» (405). Si
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
- 19/11/2026, dal ticket «Punti di estensione»: lo stack deve permettere moduli che si agganciano alla base senza
  modificarla (301), accesi e spenti dall'admin (302), con regole dei punti d'aggancio a versione e il controllo prima
  di ogni aggiornamento (307); quattro punti d'aggancio (collegamento, lettore di etichette, precedenza, partita) e campi
  aggiuntivi da configurazione (306). Da scegliere qui: come si scrivono i moduli e la forma delle regole.
- 20/11/2026: non aspetta più la prova visiva; la parte del modello passa al ticket «Impronte e server in sede, dopo la prova» (405).
- 20/11/2026, dal ticket «Divisione tra telefono, computer e server in sede» (406–421): dati solo sul server; per ogni
  inquadratura codice letto più foto ferma (0,3–0,6 MB, stima); confronto dell'aspetto tra 175.000–350.000 impronte sul
  server (ricerca esatta, ricerca del 15/11 §E); canale aperto con ogni dispositivo per aggiornare gli schermi condivisi
  entro pochi secondi (411); operazioni in attesa nella memoria del browser, con la loro identità, fascia dopo 3 secondi
  e due messaggi (413, 416–418); archivio delle foto con cancellazione dopo 30 giorni e copie di sicurezza senza quelle
  foto (412, 419); stampa dei PDF dal browser (415). Da scegliere qui le librerie per tutto questo.
