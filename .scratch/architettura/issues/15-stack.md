# Stack

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sessione del 20/11/2026 con l'utente
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
- 20/11/2026, giro 1: accettate le consigliate su linguaggio, database, foto, barcode, contenitori, aggiornamenti,
  moduli, prove, palmare e nome (422–431); Rust chiesto dall'utente e aggiunto alle opzioni; per schermate e canale
  aperto l'utente ha chiesto un confronto completo (432). Ricerca `docs/research/2026-11-20-librerie-stack.md`.
- 20/11/2026, giro 2: dopo il confronto (ricerca `docs/research/2026-11-20-confronti-stack.md`) accettate le
  consigliate: htmx 4 con piccoli componenti, avvisi dal server senza Redis, posta con il permesso dell'amministratore;
  posta di UFP e del magazzino Shopify non nota (433–436).
- 20/11/2026, riepilogo: confermato con le deduzioni (437).

## Answer

Chiuso il 20/11/2026 in due giri più il riepilogo, con la pagina https://claude.ai/artifact/CEKPn8iQVsJ1B1dsAnUbwr
(copia in `prototipi/stack/index.html`). Decisioni 422–437; specifica nella sezione «Stack» di `docs/architettura.md`.

- Server: Python 3.14 e Django 6.1, con codice stampato e modello in un processo a parte «riconoscimento» e i lavori
  a intervalli in un processo con la coda nel database (422).
- Database: PostgreSQL 18 con pgvector, impronte nella stessa base dati e ricerca esatta; regole «mai sotto zero» e
  «una volta sola» nel database (423). Foto in cartelle per tipo (424).
- Browser: pagine dal server con htmx 4 e piccoli componenti per fotocamera, attese e pezzi ricchi (433); barcode con
  il lettore del browser o zxing-cpp (425); canale con avvisi dal server e campanello di PostgreSQL, niente Redis (434).
- Installazione in contenitori con Docker Compose, aggiornamenti scaricati da internet solo in uscita, moduli nella
  cartella «moduli» (426–428). Posta con il permesso dell'amministratore o indirizzo e password (435, 436).
- Prove: subito la pagina di prova dei dispositivi (nuovo ticket), poi con la prima versione sul computer di casa
  dell'utente (429, 430). Ripo nel codice da ora, repository rinominato a prova visiva finita (431).
- Restano al ticket «Impronte e server in sede, dopo la prova»: programma del modello, dimensione delle impronte,
  macchina e sistema (405).
