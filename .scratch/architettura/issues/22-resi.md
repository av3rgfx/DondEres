# Resi

Type: grilling
Label: wayfinder:grilling
Status: claimed
Blocked by: —

## Question

Come si registrano nella base i resi dai clienti e i resi al fornitore (decisione 200)?

- **Resi al fornitore**: nascono dalla merce non prevista che il responsabile decide di rendere (45), dagli annullamenti
  (37, 41), dagli articoli nuovi rifiutati (114), dalla merce danneggiata (191), dalle eccedenze (32). Chi li prepara,
  cosa si scansiona, dove aspetta la merce, quale documento va al gestionale; in UFP chi emette il DDT di reso (domanda
  per il rivenditore o per UFP).
- **Resi dai clienti**: soprattutto nel magazzino Shopify (resi del sito); in UFP come arrivano. Se la merce torna
  libera, danneggiata o da controllare; effetto sulle assegnazioni (16) e su Shopify.
- Schermate: dove stanno nel percorso, con cose in sospeso (187), «Annulla» e «Conferma» (190), «Documenti» (189).

Si parte dalla ricerca `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 1.8) e da
`docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md`.

Risultato atteso: una sezione «Resi» in `docs/architettura.md` e le schermate aggiunte al prototipo
`prototipi/percorso-schermate/index.html`.

## Comments

- 18/11/2026, inizio: il ticket non aveva commenti. Fatti su Shopify letti nella documentazione ufficiale (API
  2026-10): resi solo di merce spedita; stati richiesto, aperto, rifiutato, chiuso, annullato; esito per pezzo con
  `reverseFulfillmentOrderDispose` (RESTOCKED, NOT_RESTOCKED, MISSING, PROCESSING_REQUIRED), dato una volta sola;
  `returnProcess` dalla 2025-07; permessi `read_returns` e `write_returns`.
  Fonti: https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps,
  https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-fulfillment-orders,
  https://shopify.dev/docs/api/admin-graphql/latest/enums/ReverseFulfillmentOrderDispositionType,
  https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnProcess (consultate il 18/11/2026).
- 18/11/2026: dalle bolle vere di UFP, due spunti per il secondo giro: pallet «a rendere» sulle bolle AGB (un reso di
  imballi al fornitore) e il timbro «accettato con riserva» sulla lettera del corriere (primo passo di un reso per
  danni). Primo giro di 7 domande nella pagina https://claude.ai/artifact/KQtNpyrXjbywxnz1iGKnGY.
