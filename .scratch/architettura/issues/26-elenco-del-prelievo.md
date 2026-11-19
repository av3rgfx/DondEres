# Elenco del prelievo e correzione della quantità

Type: prototype
Label: wayfinder:prototype
Status: open
Blocked by: —

## Question

Come si presenta un ordine da preparare con molti articoli (10–20 righe), e come si corregge la quantità al prelievo,
in modo pulito e professionale (decisioni 262, 266, 269, 270)?

- **Elenco all'apertura dell'ordine** (270): la lista degli articoli da prelevare. Toccando un articolo si aprono dei
  tasti rapidi per le azioni su quell'articolo, tra cui «Preleva» per prelevarlo da solo. In cima alla lista
  «Sospendi» (246) e «Prelievo guidato», che accompagna un articolo dopo l'altro senza toccarli uno per uno (oggi è
  l'unico modo, 164). Quali altri tasti rapidi servono (giacenze e ubicazione, 258; concludi senza, 246; correggi
  quantità).
- **Un solo tasto per correggere** (269): al posto di «Ne trovo di più» e «Ne trovo meno» (251, 252, 256), un tasto
  come «Correggi quantità»; il nome si sceglie qui. Le regole restano quelle della 256 (un passo solo, si torna alla
  riga e si preleva).
- **«Aspetto»** con l'ubicazione in conta da un collega (233): oggi vuol dire «aspetto che finisca la conta»; poco
  chiaro e forse inutile ora che la riga mostra le altre ubicazioni (258). Da togliere o rinominare.
- **Prova con un ordine lungo**: un ordine d'esempio di 10–20 righe nel prototipo, per vedere se la schermata resta
  chiara e pulita, al telefono.
- Se lo stesso elenco serve anche nella vendita assistita.

Risultato atteso: prototipo `prototipi/percorso-schermate/index.html` aggiornato, provato su telefono, e la sezione
«Percorso delle schermate» → «Preparazione e spedizione» di `docs/architettura.md` corretta.

## Comments

- 19/11/2026: nasce dalle richieste dell'utente dopo la prova del prototipo da computer (ordine 1053, ubicazione in
  conta): «non mi piacciono i tasti "Ne trovo di più" e "Ne trovo meno", da poca professionalità […] forse avrebbe
  senso un solo tasto con "Correggi quantità"»; elenco degli articoli con tasti rapidi, «Sospendi» e «Prelievo
  guidato» in cima; prova con 10–20 articoli. L'utente vuole farlo nella prossima sessione.
