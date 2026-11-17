# Piano della prova di accuratezza visiva

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: —

## Question

Come si fa la prova con foto reali che decide il modello visivo (decisione 12)?

- **Prima di tutto**: dove si conservano le foto reali e se possono stare nel repository (Notes della mappa).
- Quanti articoli (l'analisi propone 200–500, scegliendo i gruppi più simili), quante foto di catalogo e quante
  «di arrivo», da quali telefoni e con quale luce?
- Quali modelli si confrontano (analisi §4.2 punto 3: SigLIP 2, PE-Core, DINOv2 come riferimento; DINOv3 solo se
  l'azienda ne accetta la licenza: chi la legge e decide?).
- Cosa si misura: giusto al primo posto, tra i primi 5, con e senza restringere ai candidati del contesto, tempi su
  quale macchina. Si prova anche la lettura del codice stampato e della quantità?
- Che risultato basta per scegliere un modello senza adattarlo?

Risultato atteso: il piano della prova in `docs/architettura.md`, con la lista delle foto da scattare per
l'utente.

## Comments

- 16/11/2026, dal ticket «Percorso di identificazione»: la prova deve dare i numeri per fissare quando un candidato è
  «convincente» tra gli attesi (88), la soglia del «non lo so» (24) e il tetto di foto per articolo (96). Da misurare
  con e senza restringere agli articoli attesi (88, 97). Va deciso se misurare anche la lettura del codice stampato con
  il confronto dei segni che si confondono (89) e la lettura della quantità (93, 101).
- 16/11/2026, dal ticket «Inserimento di un articolo nuovo da foto»: all'inserimento si scattano fino a tre foto
  guidate (davanti, etichetta, altro lato), con la sola prima obbligatoria (106); poi le foto crescono con le conferme
  (96) e con «Aggiungi foto» (117). Il piano può misurare quanto riconosce l'aspetto con 1 e con 3 foto per articolo, e
  quanto bene si leggono le parole dell'etichetta proposte per la descrizione (108).
- 16/11/2026, dal ticket «App nativa o web app»: il programma è una web app (121), quindi le foto «di arrivo» della
  prova vanno scattate come le scatterà il programma, dal browser dei telefoni (Safari su iPhone, Chrome su Android e
  sul palmare, 119, 124), non con l'app Fotocamera. Il codice stampato si legge sul server (121). Accanto alla prova
  visiva servono le prove sui dispositivi veri elencate in `docs/architettura.md` (127).

## Answer

Chiuso il 17/11/2026 in tre giri, un riepilogo e una spiegazione con un esempio, chiesta dall'utente (pagina delle
domande: https://claude.ai/artifact/9fL5bbNUMMkYAzxWjECaHs, privata). Decisioni 128–145 in `docs/decisioni.md`; sezione
«Prova di accuratezza visiva» in `docs/architettura.md`, con la lista delle foto; ricerca
`docs/research/2026-11-17-locateanything-nvidia.md`.

- Foto in un repository GitHub privato e separato; nel repository pubblico solo piano, script e numeri con sigle
  anonime; solo scatole ed etichette; foto conservate dopo la prova (128–131).
- UFP ora, magazzino Shopify facoltativo dopo; 200 articoli a caso tra quelli che arrivano, 40 fuori catalogo, 300 di
  contorno (132–134, 139). La 138 (500 attesi con 200 articoli) è corretta dalla 139.
- 3 foto di riferimento e 3 di arrivo per articolo, con una pagina di scatto dal browser; iPhone, Android e palmare, due
  persone, due giorni, luce normale (135–137).
- Modelli: SigLIP 2, PE-Core, DINOv2 in taglia media e grande; DINOv3 solo come confronto (140, 141). LocateAnything
  escluso: localizza ma non riconosce l'articolo, e la licenza è non commerciale.
- Si misurano anche codice stampato e quantità; tempi solo nella sessione di Claude, perché computer e server aziendali
  non si toccano finché non c'è una versione da provare (142, 143).
- Traguardo: con 100 attesi, il giusto tra le 5 proposte in 95 arrivi su 100; si sceglie il più veloce (144).
- Deduzioni confermate: due metà per soglie e controllo, soglie, tetto di 10 foto, PaddleOCR, nessun ritaglio, colli
  diversi, chi crea repository e pagina (145).
- Nuovo ticket di ricerca «Modelli visivi open source recenti: ce ne sono di migliori?», chiesto dall'utente prima di
  iniziare; blocca l'esecuzione.

