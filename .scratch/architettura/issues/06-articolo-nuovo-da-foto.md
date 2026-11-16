# Inserimento di un articolo nuovo da foto

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: 02, 05

## Question

Come si aggiunge un articolo nuovo fotografandolo (decisione 8)?

- Chi può farlo: solo il responsabile, o anche l'operatore con approvazione successiva (decisione 27)?
- Quante foto, da quali angolazioni, con quale guida a schermo?
- Codice letto da barcode o codice stampato; descrizione scritta a mano o proposta da un modello (vedi Not yet
  specified)?
- Quando il prodotto affianca un gestionale esistente, l'articolo nuovo va anche lì, oppure nasce solo lì
  (decisione 19)?
- Cosa succede se l'articolo esiste già con un altro codice?

Risultato atteso: il flusso dell'articolo nuovo in `docs/architettura.md`.

## Comments

- 15/11/2026, dal ticket «Fonti degli ordini»: con un gestionale accanto l'articolo nuovo nasce provvisorio e si
  collega quando il gestionale lo conosce con lo stesso codice (59). Nel magazzino Shopify gli articoli venduti sul sito
  arrivano da Shopify; da foto si creano quelli fuori dal sito (60).
- 16/11/2026, dal ticket «Percorso di identificazione»: l'articolo nuovo si raggiunge dall'uscita «Articolo nuovo» del
  «non lo so» (98); un barcode sconosciuto prima prova codice stampato e aspetto (92), quindi «articolo nuovo» arriva
  solo quando nessuno dei due trova l'articolo. Le foto dell'inserimento sono foto di riferimento come quelle delle
  conferme (96).

## Answer

Chiuso il 16/11/2026 in due giri con l'utente (pagina delle domande: https://claude.ai/artifact/Ya1PcYYrLdq2hj3qPdSJCt,
privata). Decisioni 105–118 in `docs/decisioni.md`; flusso nella sezione «Articolo nuovo da foto» di
`docs/architettura.md`; nuovi termini «Articolo da confermare» e «Unione di articoli» in `GLOSSARY.md`.

- Chi: anche l'operatore, dall'uscita «Articolo nuovo» del «non lo so»; l'articolo nasce da confermare e si usa
  subito (105, 115). Al prelievo l'uscita non compare (118).
- Foto e dati: fino a tre foto guidate, la prima obbligatoria; obbligatori foto, descrizione e unità; codici letti dalle
  foto; descrizione dell'operatore aiutata dalle parole dell'etichetta (106–108). «Aggiungi foto» su qualsiasi
  articolo (117).
- Merce: in cima le righe attese con un articolo sconosciuto o solo descritto, così la merce segue la sua strada, VEND
  compreso (109).
- Doppioni: «È uno di questi?» prima di salvare; unione con l'esistente dopo (110, 111).
- Responsabile: conferma, unisce o rifiuta (114).
- Gestionale: riga ferma per l'articolo provvisorio, collegamento per codice o a mano, banco in coda (112, 113, 115).
  Shopify: collegamento proposto al responsabile (116).
- Resta nella nebbia: descrizione proposta da un modello (dopo la prova visiva) e merce rifiutata da rendere (resi).
