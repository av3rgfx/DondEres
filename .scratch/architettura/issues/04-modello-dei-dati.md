# Modello dei dati

Type: grilling
Label: wayfinder:grilling
Status: open
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
