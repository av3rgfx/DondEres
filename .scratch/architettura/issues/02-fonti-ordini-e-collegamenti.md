# Fonti degli ordini e collegamento ai gestionali esistenti

Type: grilling
Label: wayfinder:grilling
Status: claimed
Blocked by: 03, 18

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
- Chi crea l'app Shopify: la stessa organizzazione del negozio o un'altra (vedi la risposta del ticket di
  ricerca su Shopify)?
- Nel primo magazzino ARS Logistica fa già ricevimento, prelievo e inventario da telefono: cosa fa il nostro
  prodotto e cosa resta ad ARS, così da non registrare due volte la stessa merce? Il rivenditore va interpellato
  (domande nella ricerca del ticket 18, §7)?
- Ogni quanto si scambiano i dati e cosa succede se lo scambio fallisce?
- I due gestionali esistenti sono Ad Hoc Revolution e ARS Logistica: vedi la ricerca del ticket
  [Ad Hoc Revolution e ARS Logistica: come si scambiano i dati](18-ricerca-adhoc-revolution-ars-logistica.md).

Risultato atteso: la parte su fonti e scambi in `docs/architettura.md`, più l'elenco dei connettori previsti.

## Comments

- 15/11/2026, dall'utente: i due gestionali del primo magazzino si chiamano «ad hoc Revolution» e «ARS Logistica».
- 15/11/2026, dal ticket «Regole all'arrivo» (vedi `docs/architettura.md`, «Ricevimento e assegnazione»): nel
  magazzino Shopify la base prepara le proposte d'ordine al fornitore con il riferimento del cliente preso dall'ordine
  del sito (decisione 46), quindi gli ordini fornitore nascono anche nella base. Il riferimento cliente sta sull'ordine
  fornitore intero o su ogni riga (39) e va scambiato con i gestionali. UFP vende anche al banco: è una fonte di ordini
  cliente da considerare. Il ricevimento parte sempre dal DDT (40): da capire se il DDT arriva dai gestionali.
