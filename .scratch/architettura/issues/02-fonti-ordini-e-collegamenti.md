# Fonti degli ordini e collegamento ai gestionali esistenti

Type: grilling
Label: wayfinder:grilling
Status: resolved
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
- 15/11/2026, primo giro di domande (pagina https://claude.ai/artifact/G5XtbLq6KFxqngFxXMXsVd): l'utente ha accettato
  tutte le proposte consigliate, senza note. Registrate come decisioni 49–57.
- 15/11/2026, secondo giro (stessa pagina): accettate le proposte consigliate; decisioni 58–64. La domanda «dove nasce
  la vendita al banco in UFP» resta aperta: l'utente aveva scelto «in Ad Hoc, letta subito dal programma», ma la sua
  nota descrive un'altra pratica (sotto). Si richiede nel terzo giro.
- 15/11/2026, fatti riferiti dall'utente su UFP: oggi la vendita assistita al banco si fa con ARS Logistica da
  telefono. Si sceglie prima il cliente: un cliente preciso (per esempio i clienti chiamati «OP»), il codice cliente
  generico delle vendite al banco ai privati, oppure nessuno. Poi si scansionano uno o più articoli e l'ubicazione da
  cui si prendono, perché lo stesso articolo può stare in più ubicazioni (per le scorte). Alla conferma l'ordine compare
  da solo nelle vendite di Ad Hoc, dove si fanno i documenti di vendita. Serve anche ai ticket «Modello dei dati»
  (un articolo in più ubicazioni) e «Percorso delle schermate».
- 15/11/2026, terzo giro: confermati la vendita al banco sul telefono e il riepilogo, deduzioni comprese (decisioni
  65–67). L'utente precisa che «OP» è il nome del documento di vendita in Ad Hoc, per qualsiasi cliente, non un tipo
  di cliente.

## Answer

Risolto il 15/11/2026 in tre giri di domande (pagina https://claude.ai/artifact/G5XtbLq6KFxqngFxXMXsVd, privata).
Decisioni 49–67 in `docs/decisioni.md`; specifica nella sezione «Fonti dei dati e collegamenti» di
`docs/architettura.md`; domande per il rivenditore in `docs/domande-rivenditore-ufp.md`.

- **Chi comanda**: il sistema d'origine di ogni dato; il programma aggiunge i propri dati e segnala le differenze (49).
- **UFP**: il programma fa tutto il lavoro fisico al posto di ARS Logistica e scrive in Ad Hoc un documento per ogni
  fatto di magazzino (50, 61). Nessun collegamento con ARS (67).
- **Connettori previsti**: scambio a file nella base; Shopify modulo con la base, spento di serie; Ad Hoc nella
  specializzazione per UFP, dopo le risposte del rivenditore (51, 57, 67).
- **Shopify**: catalogo importato (una variante = un articolo); verso il sito arrivi, rettifiche e spedizioni; app
  creata dal negozio; solo gli ordini pagati ricevono merce, scelta per magazzino (52, 53, 60, 63).
- **Senza gestionale**: a mano e da file per articoli, fornitori e ordini; movimenti esportati su file; ordine al
  fornitore come documento che una persona manda (55, 64).
- **Banco**: ordine cliente «banco» creato sul telefono, prelevato e spedito subito; prima la merce libera, poi chi
  vende decide vedendo a chi la toglie; VEND mai (56, 58, 65).
- **Scambio**: ogni 5 minuti più «aggiorna ora»; se si blocca si lavora e la coda riparte una volta sola; avviso dopo
  15 minuti (54). Regole sugli ordini importati: data d'origine, codice d'origine, articoli sconosciuti, più magazzini
  Shopify (66). Ordine annullato dopo il prelievo: compito «rimetti a posto» (62). Articolo nuovo con gestionale:
  provvisorio, poi collegato (59).

