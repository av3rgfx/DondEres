# Inserimento di un articolo nuovo da foto

Type: grilling
Label: wayfinder:grilling
Status: claimed
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
