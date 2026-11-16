# Percorso delle schermate

Type: prototype
Label: wayfinder:prototype
Status: open
Blocked by: 04, 05, 06, 07

## Question

Quali schermate servono e in che ordine, per operatore e responsabile (decisione 27): ricevimento e identificazione,
conferma dei candidati, quantità, articolo nuovo, prelievo e spedizione, assegnazioni, rettifiche, configurazione
iniziale? Si prova con un prototipo da guardare sul telefono, poco curato nell'aspetto.

Risultato atteso: il percorso in `docs/architettura.md`, con il link al prototipo.

## Comments

- 15/11/2026, dal ticket «Fonti degli ordini»: servono la schermata «banco» (cliente, articoli, ubicazione, conferma;
  avviso quando si toglie merce assegnata) (58, 65), il compito «rimetti a posto» (62), gli avvisi di scambio bloccato
  e di differenze col sistema d'origine (49, 54), «aggiorna ora» (54), il documento dell'ordine fornitore (64). Oggi in
  UFP la vendita al banco si fa da telefono con ARS: cliente, poi articoli e ubicazione, poi conferma.
- 16/11/2026, dal ticket «Modello dei dati»: schermate da prevedere per il ricevimento in un passaggio dal telefono
  (68), la chiusura del DDT con una riga ferma e la scelta dell'operatore (82), l'elenco «da mettere a posto» (69), le
  cose da controllare del responsabile (86), la correzione dell'operatore a DDT aperto (81), il conteggio quando la
  merce non risulta (77), il prezzo al banco e il costo visibile solo al responsabile (84, 85), l'accesso con nome e
  PIN (80).
- 16/11/2026, dal ticket «Percorso di identificazione»: schermate e stati da prevedere: inquadratura unica (87); registrato
  con «Annulla» e quantità modificabile (99); scheda «È questo» / «No, è un altro» (90); schede di un barcode su più
  articoli (91); «Collego questo barcode?» (92); avviso «codice simile, controlla» (89); scelta tra più codici
  nell'inquadratura (102); due quantità lette (93); «× colli» (94); «come l'ultima volta» (100); avviso «non è tra gli
  attesi» (88); stop al prelievo con un altro articolo (97, 103); uscite del «non lo so» (98).
- 16/11/2026, dal ticket «Inserimento di un articolo nuovo da foto»: schermate da disegnare: righe attese senza
  articolo in cima (109), tre foto guidate con riquadro e avvisi (106), scheda con campi compilati dal programma (107),
  parole dell'etichetta da toccare (108), «È uno di questi?» (110), segno «da confermare» (115), uscite del responsabile
  «Conferma / Unisci / Rifiuta» (114), «Aggiungi foto» nella scheda dell'articolo (117). Al prelievo l'uscita
  «Articolo nuovo» non compare (118).
