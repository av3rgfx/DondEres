# Gestionali di magazzino esistenti: funzioni in più e difetti da evitare

Type: research
Label: wayfinder:research
Status: resolved
Assignee: agente (sessione del 18/11/2026)
Blocked by: —

## Question

Come funzionano i gestionali di magazzino esistenti, e cosa possiamo imparare per la base (decisione 180)?

- **Quali guardare**: gestionali di magazzino (WMS) e moduli di magazzino dei gestionali, sia per piccole e medie aziende
  sia più grandi, italiani e internazionali; ARS Logistica compresa (ricerca già fatta in
  `docs/research/2026-11-15-adhoc-revolution-ars-logistica.md`, da non ripetere). La scelta dei prodotti va motivata.
- **Funzioni**: ricevimento (come si crea il DDT, come si abbinano le righe agli ordini), messa a posto, prelievo e
  piani o giri di prelievo, spedizione, vendita al banco, inventario, resi, elenchi delle cose in sospeso, storico e
  registro delle operazioni, permessi, annullamenti e conferme, uso da telefono e palmare. Cosa hanno più della base, e
  cosa servirebbe davvero ai due magazzini di prova (UFP e Shopify).
- **Difetti**: problemi segnalati da chi li usa (recensioni, forum, documentazione di supporto, note di rilascio): dati
  persi, passaggi ripetuti, lentezza, errori di abbinamento, schermate confuse, blocchi senza rete. Per ognuno, come la
  base lo evita o perché non la riguarda.
- **Fonti**: primarie quando ci sono (documentazione ufficiale, manuali, video dei produttori); le recensioni come
  esperienze riferite, non come fatti. Data di ogni fonte.

Risultato atteso: `docs/research/<data>-gestionali-magazzino-esistenti.md`, un file con data e link alle fonti, con una
tabella finale «funzione o difetto → cosa proponiamo per la base», da usare nel ticket «Completezza del percorso delle
schermate». Niente decisioni: le prende l'utente.

## Answer

Chiuso il 18/11/2026. Ricerca in `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (Odoo 19, Business
Central, Dynamics SCM, SAP B1 ed EWM, NetSuite WMS, Oracle WMS Cloud, Shopify, Zoho, inFlow, Katana, ShipStation; due
fonti chiave ricontrollate: «Find PO by Item» di NetSuite e la pagina AgID sul DDT Peppol). G2, Capterra, TrustRadius e
Reddit non erano raggiungibili: le esperienze riferite vengono solo da forum e community ufficiali.

- Tutti ricevono «contro ordine»; i più completi mettono più ordini in un documento di entrata; NetSuite cerca l'ordine
  per articolo: la decisione 183 coincide con le soluzioni PMI più complete.
- Nessun prodotto crea le righe da un DDT cartaceo in modo affidabile; i servizi di lettura dei documenti leggono solo
  la testata e stanno in cloud. Proposte: foto della bolla con il DDT, numero e data letti in sede e confermati, righe
  della bolla solo come «quantità in bolla», avvisi elettronici dei fornitori come punto d'estensione.
- Il DDT elettronico tra imprese non risulta obbligatorio (DPR 472/1996 fissa il contenuto, non la forma; Peppol DDT
  approvato da AgID nel 2020 senza effetti sull'NSO).
- Difetti riferiti da evitare: validare senza scansionare e «riempi con l'atteso», residuo chiuso per sbaglio, quantità
  attesa riscritta dopo una ricarica, lentezza con cataloghi grandi, giacenze Shopify sovrascritte da altre app, ordini
  «presi» e mai finiti.
- Mancano alla base: elenchi in sospeso per sezione, «Documenti» con storico e registro, una regola per «Annulla» e
  «Conferma», merce danneggiata e scarto, resi, inventario periodico, etichette e distinte del corriere, un requisito
  di velocità.

Le proposte si decidono nel ticket «Completezza del percorso delle schermate».
