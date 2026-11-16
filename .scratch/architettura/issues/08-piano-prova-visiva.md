# Piano della prova di accuratezza visiva

Type: grilling
Label: wayfinder:grilling
Status: open
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
