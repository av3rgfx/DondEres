# Shopify: resi, rimborsi e cosa si può collegare

Type: research
Label: wayfinder:research
Status: open
Assignee: sessione del 19/11/2026 (ricerca in corso)
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
