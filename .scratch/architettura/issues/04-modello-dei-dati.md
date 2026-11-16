# Modello dei dati

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: 01, 02

## Question

Quali entità, relazioni e stati servono alla base per catalogo, codici, foto di riferimento, fornitori, ordini,
ricevimenti, giacenze (anche VEND, se resta), assegnazioni, movimenti, ubicazioni facoltative (decisione 26), utenti
e ruoli (decisione 27)?

Da chiarire anche:

- Come si annulla un movimento senza perdere lo storico, e cosa succede alle assegnazioni?
- Come si tiene traccia della provenienza dei dati importati (decisione 19)?
- Dove si lascia spazio alle estensioni previste: seriali, lotti e scadenze (decisione 17), campi aggiuntivi?

Risultato atteso: il modello dei dati in `docs/architettura.md` e `GLOSSARY.md` allineato.

## Comments

- 15/11/2026, dal ticket «Fonti degli ordini» (`docs/architettura.md`, «Fonti dei dati e collegamenti»): ogni dato
  importato porta il suo sistema d'origine e il codice che ha lì (49, 66); articolo provvisorio (59); ordine cliente
  «banco» (56, 65) e stato «in attesa di pagamento» (63); compito «rimetti a posto» (62); proposta d'ordine e documento
  dell'ordine fornitore (46, 64). In UFP lo stesso articolo può stare in più ubicazioni e il prelievo scansiona
  l'ubicazione (fatto riferito dall'utente).
- 16/11/2026, dal documento dell'utente sul funzionamento attuale di ARS Logistica in UFP (non copiato nel repository:
  contiene nomi, un indirizzo email e l'indirizzo del server interno). Fatti utili al modello: il ricevimento oggi passa
  da controllo a penna sulla bolla, DDT al PC dalle righe d'ordine e lista «Libera» al palmare dal CHECK alle buche
  (due registrazioni della stessa merce); un DDT può venire da più ordini (OF e OT) e lo stesso codice può stare su più
  righe; codici e unità del fornitore diversi da quelli interni (TO e KG, «Coppia» e NR, PZ e NR); numero DDT del
  fornitore con suffissi, distinto dal protocollo interno; casi di scansioni perse dopo «Sospendi» e di un DDT corretto
  cancellandolo e rifacendolo. Il primo giro di domande è stato rifatto su questa base (13 domande).

## Answer

Risolto il 16/11/2026 in due giri, con la pagina https://claude.ai/artifact/4HA7JqQbi8QtgcpfPmo9xd (privata). Il primo
giro è stato rifatto dopo il documento dell'utente sul funzionamento di ARS in UFP.

- Decisioni 68–86 in `docs/decisioni.md`: ricevimento in un passaggio dal telefono con DDT aperto fino alla chiusura
  (68); area di ricevimento assegnabile subito (69); scelta della riga d'ordine fornitore (70); collegamento dei codici
  del fornitore da confermare (71); unità di magazzino e conversioni approvate (72); quantità in bolla (73); correzioni
  senza cancellare (74, 81); ubicazione abituale (75); assegnazione per quantità (76); mai sotto zero, conteggio
  dell'operatore (77); prezzi accesi per magazzino e presi dal gestionale (78, 83–85); clienti solo codice e nome (79);
  accesso con nome e PIN (80); chiusura del DDT con una riga ferma a scelta dell'operatore (82); riepilogo e deduzioni
  (86).
- Specifica: sezione «Modello dei dati» in `docs/architettura.md` (entità, ricevimento in un passaggio, correzioni,
  requisiti di affidabilità, prezzi, spazio per le estensioni).
- Glossario: area di ricevimento, messa a posto, ubicazione abituale, unità di magazzino, conversione, collegamento da
  confermare, quantità in bolla, correzione, rettifica, prezzo di vendita, costo d'acquisto, compito, da controllare.
- Domande 17 e 18 aggiunte per il rivenditore di UFP (prezzi, codici dei fornitori e conversioni in Ad Hoc).
