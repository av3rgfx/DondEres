# Resi del cliente nel magazzino Shopify

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sessione del 19/11/2026 con l'utente
Blocked by: 27

## Question

Come diventa digitale, e dove si può automatico, il reso del cliente nel magazzino Shopify (decisione 321), partendo da
come si lavora oggi e dai risultati della ricerca «Shopify: resi, rimborsi e cosa si può collegare»?

- **Oggi** (fatto riferito, 321): arrivano le scatole del reso; si controllano le etichette; si decide come rimborsare;
  una persona si accorda con il cliente per WhatsApp o email tra credito del negozio e rimborso sul metodo di pagamento
  originale. Niente è registrato in digitale.
- **Da decidere**: come si riconosce la scatola all'arrivo (etichetta di reso, numero d'ordine, inquadratura); chi
  decide il rimborso e dove (programma o amministrazione di Shopify); se il programma propone o esegue rimborso e
  credito; come e da dove si scrive al cliente, con quali testi; cosa resta in «Documenti»; cosa cambia nelle 210–212.
- Le schermate si provano sul prototipo `prototipi/percorso-schermate/index.html`.

Risultato atteso: la parte «Reso del cliente» della sezione «Resi» di `docs/architettura.md` aggiornata per il magazzino
Shopify, ed eventuali scelte nuove in Configurazione.

## Comments

- 19/11/2026: nasce dalla richiesta dell'utente (321), da lavorare nella sessione successiva, dopo la ricerca.
- 19/11/2026, risoluzione (tre giri, pagina privata https://claude.ai/artifact/AR5aJVmctJ7FbEzbwyjCQd; decisioni
  322–343, riepilogo confermato nella 343): resi di Shopify letti e scritti dal programma, senza app; richiesta dal
  sito con un modulo nostro che fa scegliere credito o rimborso e salva la scelta, con l'indirizzo del ritiro GLS;
  mail lette dal programma da un indirizzo dedicato, con bozza del modello solo dopo una prova (ancora da definire) e
  conferma di una persona; il responsabile approva le richieste, prenota il ritiro GLS dal riepilogo o carica
  l'etichetta FedEx; rimborso eseguito dal programma dopo la conferma, importo scritto dal responsabile; «giorno N di
  14»; niente cambi; scheda in «Documenti». Tre punti per la parte legale (342). Specifica in `docs/architettura.md`,
  «Resi» → «Reso del cliente nel magazzino Shopify».
