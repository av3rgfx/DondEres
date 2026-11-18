# Punti di estensione per la specializzazione

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 01, 02, 04

## Question

Come si specializza la base per un magazzino senza toccarne il cuore (decisione 4)? Cosa si fa con la sola
configurazione (ubicazioni sì o no, regola all'arrivo, testi) e cosa con moduli di codice (connettori ai gestionali e a
Shopify, formati di etichette dei fornitori, regole di assegnazione diverse, campi aggiuntivi, seriali e lotti)?
Come si aggiorna la base senza rompere le specializzazioni?

Risultato atteso: l'elenco dei punti di estensione e il loro contratto in `docs/architettura.md`.

## Comments

- 15/11/2026, dal ticket «Fonti degli ordini»: collegamenti previsti e loro posto (51, 67): scambio a file nella base,
  Shopify modulo con la base, Ad Hoc nella specializzazione. Il connettore traduce documenti e stati (61) e lavora con
  la coda d'uscita (54). Configurazioni nuove: modo, connettore Shopify, intervallo di scambio, solo ordini pagati.
- 16/11/2026, dal ticket «Modello dei dati»: nuove scelte per magazzino (prezzi accesi o spenti, 83; uscita automatica
  dal telefono, 80); spazio previsto per una «partita» facoltativa per seriali, lotti e scadenze (17); i campi
  aggiuntivi restano da decidere qui.
- 16/11/2026, dal ticket «Percorso di identificazione»: le parole che indicano la quantità sulle etichette (93) si
  possono ampliare con i termini dei fornitori di un magazzino; i formati di etichetta dei fornitori con regole proprie
  sono un candidato a punto di estensione.
- 18/11/2026, dal ticket «Resi» (226): proporre all'utente di far partire anche gli ordini fornitore dal programma,
  come le richieste di reso (223), dalla mail aziendale del responsabile; oggi li manda una persona (64). Anche come
  Ad Hoc riceve il documento di reso e il «reso da cliente» (domande 24 e 27).
