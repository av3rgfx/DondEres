# Shopify: resi, rimborsi e cosa si può collegare

Type: research
Label: wayfinder:research
Status: resolved
Assignee: sessione del 19/11/2026
Blocked by: —

## Question

Nel magazzino Shopify i resi dei clienti sono tutti a mano (decisione 321). Con fonti primarie (documentazione di
Shopify, app ufficiali, documentazione dei servizi), cosa si può fare in automatico?

- **Resi**: come nasce un reso su Shopify (richiesta del cliente dal sito, reso creato dal negozio), stati, etichette di
  reso, motivo; cosa legge e scrive un'app del negozio (`read_returns`, `write_returns`, 212) e cosa resta solo
  nell'amministrazione di Shopify.
- **Rimborsi**: rimborso sul metodo di pagamento originale e credito del negozio (store credit, carte regalo); se un'app
  può proporli o eseguirli, con quali permessi, chi deve confermare; limiti per metodo di pagamento e per paese (Italia).
- **Comunicazione con il cliente**: oggi WhatsApp o email (321). Notifiche di Shopify sui resi, email dal programma,
  WhatsApp Business (API ufficiale, costi, regole sui messaggi); cosa si può mandare in automatico e cosa no.
- **Tutto ciò a cui ci si può collegare** da Shopify con il modello di traffico della base, solo in uscita dal server
  in sede, interrogando a intervalli (54): ordini, evasioni, giacenze, prodotti, clienti, resi, rimborsi, corrieri ed
  etichette di spedizione, fatture, pagamenti. Per ognuno: si legge, si scrive, con quale permesso, con quale piano di
  Shopify.
- **App già esistenti** per i resi su Shopify: cosa fanno, se conviene affiancarne una o farlo nel programma.

Risultato atteso: `docs/research/<data>-shopify-resi-rimborsi-collegamenti.md`, un file con data e link alle fonti
primarie, fatti distinti da deduzioni e ipotesi; le conseguenze per il ticket «Resi del cliente nel magazzino Shopify».

## Comments

- 19/11/2026: nasce dalla richiesta dell'utente (321). Ricerca già fatta: `docs/research/2026-11-15-shopify-ordini-
  evasione-giacenze.md` (non ripeterla, aggiornarla dove serve). Specifica attuale: «Resi» → «Reso del cliente» in
  `docs/architettura.md` (210–212: esiti sul reso del sito, rimborso e credito restano sul sito).
- 19/11/2026, risoluzione: `docs/research/2026-11-19-shopify-resi-rimborsi-collegamenti.md`. In automatico dal server
  in sede: leggere i resi aperti (dagli ordini con `return_status`), creare, approvare o rifiutare un reso, caricare
  un'etichetta propria, scrivere l'esito per pezzo, eseguire il rimborso sul metodo originale o in credito del negozio
  (`returnProcess`), con le notifiche di Shopify al cliente. No: etichette di reso Shopify Shipping in Italia (solo
  USA e Canada), stato del pacco di reso, ricerca per tracking (serve un indice nostro), scelta del rimborso da parte
  del cliente con i soli resi di Shopify (serve un'estensione dell'account cliente), email libere al cliente tramite
  Shopify, messaggi WhatsApp in arrivo senza indirizzo pubblico, rimborso di contrassegno e bonifico. Per legge
  (Codice del consumo 52–57, 54-bis): rimborso entro 14 giorni dalla richiesta di recesso, stesso mezzo salvo accordo
  espresso del cliente; recesso valido anche per email. Durante la ricerca l'utente ha proposto due idee (scelta del
  rimborso sul sito; casella dei resi letta da un'automazione con un LLM e conferma di una persona), confrontate nella
  sezione 6 e nelle conseguenze.
