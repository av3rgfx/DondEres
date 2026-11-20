# Aspetto grafico

Type: prototype
Label: wayfinder:prototype
Status: open
Blocked by: 14, 15, 16, 21, 22, 23, 26 (16 chiuso il 17/11/2026; 21, 22 e 23 chiusi il 18/11/2026; 26 chiuso il 19/11/2026; 14 e 15 chiusi il 20/11/2026)

## Question

Quale aspetto deve avere l'interfaccia: colori, caratteri, disposizione, stile (decisione 14)? Si parte dal brand
kit e dal percorso delle schermate; si mostrano poche varianti da guardare; sceglie l'utente. Una sola direzione
visiva, registrata in `docs/decisioni.md`. Obiettivo di accessibilità WCAG 2.2 AA.

Risultato atteso: la direzione visiva in `docs/architettura.md` e in `docs/decisioni.md`.

## Comments
- 19/11/2026, dal ticket «Elenco del prelievo e correzione della quantità»: i responsabili e l'admin lavorano quasi
  sempre dal computer (292): aspetto e schermate vanno progettati anche per il computer, non solo per il telefono. Al
  computer le quantità si scrivono con la tastiera, con l'icona a calcolatrice che apre il tastierino (290). Le icone
  vere (📷 dell'elenco, calcolatrice) arrivano qui (267).
- 20/11/2026, dal ticket «Divisione tra telefono, computer e server in sede»: da disegnare la fascia «Senza rete» con i
  due messaggi e l'ora dei dati, «Inviata», l'esito «non riuscita» con il motivo e «1 operazione di Mario in attesa»
  (413, 414, 416–418).
- 20/11/2026, dal ticket «Stack» (433): pagine dal server con htmx 4 e piccoli componenti JavaScript per i pezzi ricchi;
  l'aspetto si fa con il CSS, e le transizioni fra schermate con le View Transitions (Chrome 111, Safari 18, Firefox
  144), spente di serie in htmx 4. Animate UI resta fuori: è per React. L'utente tiene a una versione da computer ricca,
  ben studiata, veloce e intuitiva (432).
