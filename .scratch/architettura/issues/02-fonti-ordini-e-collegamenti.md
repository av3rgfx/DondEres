# Fonti degli ordini e collegamento ai gestionali esistenti

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 03

## Question

La decisione 19 chiede una base che possa fare da gestionale principale e anche affiancare uno o più gestionali
esistenti. Come?

- Quali dati entrano e quali escono (articoli, ordini fornitore, ordini cliente, movimenti, giacenze) e chi comanda su
  ciascuno quando i due sistemi non sono d'accordo?
- Con due gestionali affiancati allo stesso magazzino, come si dividono i dati tra loro?
- Cosa sta nella base: inserimento a mano, importazione ed esportazione da file? Cosa sta nei connettori: i due
  gestionali, Shopify?
- Shopify, quando il prodotto è il gestionale principale: gli ordini arrivano da lì, ma le giacenze tornano a Shopify?
  E l'evasione? (Vedi la ricerca del ticket
  [Shopify: ordini, evasione e giacenze viste da un gestionale esterno](03-ricerca-shopify.md).)
- Ogni quanto si scambiano i dati e cosa succede se lo scambio fallisce?
- Come si chiamano i due gestionali esistenti (informazione, serve per una ricerca futura)?

Risultato atteso: la parte su fonti e scambi in `docs/architettura.md`, più l'elenco dei connettori previsti.
