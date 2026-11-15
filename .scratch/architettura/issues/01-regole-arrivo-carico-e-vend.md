# Regole all'arrivo: carico normale e merce venduta (VEND)

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: —

## Question

Come funzionano, nella base, le due regole all'arrivo della decisione 15?

- **Carico normale**: la merce entra in giacenza, scala il residuo dell'ordine fornitore e poi si assegna agli
  ordini cliente dal più vecchio (decisione 16).
- **Merce venduta, con la giacenza «VEND»**: la merce che arriva va subito a un ordine cliente.

Da chiarire con esempi numerici:

- Nella merce venduta, come si sa a quale ordine cliente va il pezzo arrivato? Esiste un legame tra la riga
  d'ordine cliente e l'ordine fornitore? Cosa vuol dire «l'ultimo ordine effettuato su quel fornitore»?
- «VEND» è una giacenza separata o un'assegnazione con un nome proprio? Quando la merce esce da VEND?
- Le due regole convivono nello stesso magazzino? Chi decide quale si applica: l'articolo, l'ordine, il fornitore o
  una scelta di configurazione?
- Cosa succede se arriva più merce di quella venduta, o meno? E se arriva merce senza ordine fornitore?
- Le due regole stanno entrambe nella base, come configurazione, oppure la merce venduta è un'estensione?
- Quale dei due magazzini reali usa quale regola (informazione, non decisione)?

Risultato atteso: le regole di ricevimento e di assegnazione in `docs/architettura.md` e i termini nuovi (VEND,
carico, residuo) in `GLOSSARY.md`.

## Comments

- 15/11/2026, primo giro (pagina interattiva «Merce in arrivo»): confermate tutte le proposte. Decisioni 29–33 in
  `docs/decisioni.md`; termini Carico, Residuo, Eccedenza, Merce senza ordine e VEND in `GLOSSARY.md`.
- 15/11/2026, secondo giro: decisioni 34–38. Le note dell'utente cambiano il modello di VEND: il collegamento tra
  ordine cliente e ordine fornitore non lo fa il programma quando manca giacenza, ma nasce dal **riferimento del
  cliente scritto sull'ordine fornitore**; al ricevimento si carica il DDT, che rimanda all'ordine, e si scansiona la
  merce per controllarla. Le risposte a «quale ordine fornitore» e «nessun ordine aperto» (collegamento automatico)
  restano sospese, e la decisione 29 va rivista: si chiarisce nel terzo giro.
- 15/11/2026, terzo giro: decisioni 39–43. UFP è il magazzino con Ad Hoc + ARS e usa VEND (corregge la 15). Fatto:
  il DDT arriva di carta dal corriere, viene scansionato e caricato; gli uffici spesso hanno la versione digitale, non
  usata in magazzino. La domanda «da dove nasce VEND» non era chiara all'utente: si ripete nel quarto giro, insieme al
  rapporto tra «sempre dal DDT» (40) e merce senza ordine (31) e all'uso di VEND nel magazzino Shopify.
- 15/11/2026, quarto giro: decisioni 44 (corregge la 29) e 45 (precisa la 31). Fatti: in UFP gli ordini dei clienti
  arrivano per telefono o email, e VEND oggi è un tavolo con gli articoli venduti pronti per la spedizione. Nel
  magazzino Shopify VEND non c'è formalmente: la merce venduta si carica senza ubicarla e si mette su un tavolo con un
  biglietto che dice di chi è. Proposte dell'utente, da confermare nel riepilogo finale: nel magazzino Shopify il
  riferimento va preso in automatico dall'ordine del sito; VEND diventa un'ubicazione con posti numerati (VEND1,
  VEND2…) e il palmare dice in quale posto si trova ogni articolo venduto, anche in UFP.
- 15/11/2026, riepilogo finale confermato dall'utente: decisioni 46–48.

## Answer

Regole scritte in [`docs/architettura.md`](../../../docs/architettura.md), sezione «Ricevimento e assegnazione»;
decisioni 30–48 in `docs/decisioni.md` (la 44 sostituisce la 29, la 42 corregge la 15). In sintesi:

- Il ricevimento parte sempre dal DDT; ogni riga prende una di tre strade: **VEND** se l'ordine fornitore porta il
  riferimento del cliente, **carico normale** se è un ordine di magazzino, **merce non prevista** se nessun ordine la
  prevede (resta ferma finché decide il responsabile).
- VEND nasce solo dal riferimento cliente, mai da un collegamento automatico; vince sulla regola «dal più vecchio»;
  esce con il prelievo; può avere posti numerati, un posto per ordine cliente.
- Più merce: si accetta e si segnala; meno merce: la riga resta aperta.
- VEND sta nella base, spento di serie, acceso per magazzino. UFP (Ad Hoc + ARS) lo usa con riferimento scritto da chi
  ordina; il magazzino Shopify lo userà con riferimento compilato dal programma sulla proposta d'ordine.
- Termini nuovi in `GLOSSARY.md`: Carico, Residuo, Eccedenza, Merce senza ordine, VEND, DDT, Riferimento cliente.
- Strumento usato per le domande: pagina interattiva «Merce in arrivo» (https://claude.ai/artifact/8bpuk2jouU2yTzEU9ewKnh).
