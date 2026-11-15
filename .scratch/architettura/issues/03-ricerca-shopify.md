# Shopify: ordini, evasione e giacenze viste da un gestionale esterno

Type: research
Label: wayfinder:research
Status: resolved
Blocked by: —

## Question

Cosa espongono le API ufficiali attuali di Shopify a un gestionale di magazzino esterno che deve importare gli ordini,
segnarne l'evasione e la spedizione, leggere e scrivere le giacenze e ricevere notifiche, da un server in sede
spesso senza indirizzo pubblico? Con quale autenticazione, quali limiti e quale calendario di versioni? Dove i
concetti di Shopify coincidono con quelli del nostro glossario e dove no?

Risultato atteso: un file in `docs/research/`, con link alle fonti primarie.

## Answer

Ricerca completa in
[`docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md`](../../../docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md)
(fonti: shopify.dev e Help Center di Shopify). In sintesi, per i ticket che ne dipendono:

- **Dove sta.** Nella base va solo un punto di estensione neutro «canale di vendita»; il connettore Shopify è un
  modulo separato (deduzione della ricerca, da decidere in
  [Fonti degli ordini e collegamento ai gestionali esistenti](02-fonti-ordini-e-collegamenti.md) e
  [Punti di estensione per la specializzazione](11-punti-di-estensione.md)).
- **API.** GraphQL Admin API, versione stabile 2026-10; una versione nuova ogni tre mesi, ciascuna valida circa un
  anno: il connettore va aggiornato almeno una volta l'anno. REST è «legacy».
- **Ordini.** Shopify divide l'ordine per luogo (`FulfillmentOrder`). Il suo numero d'ordine non è garantito
  sequenziale: per lo spareggio a parità di data (decisione 16) il connettore deve fornire un'altra chiave.
- **Evaso e spedito.** «Spedito» corrisponde al `Fulfillment` di Shopify; «evaso» non ha un equivalente. Falso amico:
  "fulfilled" non vuol dire «evaso».
- **Giacenze.** Shopify calcola l'impegnato da sé, senza ordine di anzianità, e non lo lascia scrivere: la nostra
  assegnazione dal più vecchio resta nella base. Da provare come non scalare due volte la stessa uscita.
- **Notifiche.** I webhook richiedono un server raggiungibile da Internet; per un server in sede la via è
  l'interrogazione periodica in uscita, più un riallineamento periodico.
- **Da chiedere all'utente** nel ticket sulle fonti: chi crea l'app Shopify (la stessa organizzazione del negozio
  permette il token più semplice).
- **Incerto:** permessi dei `FulfillmentOrder` per un'app della propria organizzazione, dati protetti dei clienti,
  varianti che condividono la stessa giacenza.
