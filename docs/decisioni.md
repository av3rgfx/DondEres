# Decisioni dell'utente

Unico registro delle decisioni prese dall'utente, con data e motivo.
Se il motivo non è stato detto, è scritto «non indicato»: non si deduce.
Le decisioni tecniche ancora aperte non stanno qui: stanno in `docs/analisi-progetto.md`.

| N. | Data | Decisione | Motivo |
|---|---|---|---|
| 1 | 15/11/2026 | `ocr` e `playwright-cli` si installano nel progetto, non a livello globale. | Perché le due skill funzionino come previsto. (Riportata da `AGENTS.md`.) |
| 2 | 15/11/2026 | Il prodotto è un gestionale di magazzino che assegna le scorte agli ordini non ancora evasi o non ancora spediti, dal più vecchio al più recente. | Non indicato. |
| 3 | 15/11/2026 | Il riconoscimento degli articoli avviene con un modello visivo che gira in locale. | Leggere automaticamente anche gli articoli senza barcode. |
| 4 | 15/11/2026 | Prima si costruisce una struttura di base valida per qualsiasi magazzino; poi, a struttura completata, una specializzazione per un magazzino specifico. | Poterlo installare in qualsiasi magazzino. |
| 5 | 15/11/2026 | La base va dimensionata per un catalogo grande: fino a 35.000 articoli. | Non indicato. |
| 6 | 15/11/2026 | Il sistema identifica l'articolo anche leggendo il codice sulla scatola: il barcode se c'è, altrimenti il codice stampato sull'etichetta (l'utente lo chiama «numero seriale»). | Semplificare il lavoro e ridurre gli errori. |
| 7 | 15/11/2026 | Si assume una somiglianza medio-alta tra gli articoli. | È la condizione reale attesa. |
| 8 | 15/11/2026 | Un articolo nuovo si aggiunge al catalogo fotografandolo, con codice e descrizione, e finisce da solo nel database. | Non indicato. |
| 9 | 15/11/2026 | L'applicazione si usa soprattutto da telefono, in locale e collegata alla rete aziendale; deve funzionare anche su computer con telecamera integrata. | «Deve funzionare in locale» (non è stato detto perché). |
| 10 | 15/11/2026 | L'architettura si approfondisce in una nuova sessione con Wayfinder, dopo l'analisi. | Non indicato. |
| 11 | 15/11/2026 | Destinazione della mappa di architettura: un unico documento `docs/architettura.md` con la specifica della base generica, più `GLOSSARY.md` alla radice per il glossario. Mappa e ticket stanno in `.scratch/architettura/`. | Non indicato (proposta accettata). |
| 12 | 15/11/2026 | La prova di accuratezza visiva con foto reali si progetta e si esegue dentro la mappa, non dopo. Il modello visivo si sceglie in base ai suoi risultati. | Non indicato. |
| 13 | 15/11/2026 | La specifica comprende anche lo stack (linguaggi, database, programmi per il modello visivo). | Non indicato. |
| 14 | 15/11/2026 | La specifica comprende anche la grafica: sia il percorso delle schermate, sia l'aspetto (colori, caratteri, disposizione, stile). | Non indicato. |

## Note di lettura

- Decisione 5: «fino a 35.000 unità» è stato inteso come 35.000 articoli diversi a catalogo, non 35.000 pezzi in giacenza. Da confermare.
- Decisione 6: di solito «numero seriale» indica il singolo pezzo, mentre «codice articolo» indica il tipo. Qui è stato inteso come codice che identifica il tipo di articolo. Da confermare.
