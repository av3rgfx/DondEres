# Elenco del prelievo e correzione della quantità

Type: prototype
Label: wayfinder:prototype
Status: resolved
Assignee: sessione del 19/11/2026 con l'utente
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
- 19/11/2026, primo giro (pagina privata https://claude.ai/artifact/SdXpDTDFxGAs76mx17cNb5): accettate le consigliate
  (271–278). Note: «Concludi senza» solo sull'ultimo articolo del prelievo guidato, prima «Prosegui» (272); «Elimina» al
  posto di «Togli» nella vendita (277); attenzione ai nomi di tasti e titoli (278).
- 19/11/2026, secondo giro, dopo la prova dal telefono: accettate le consigliate (279–282). Richieste nuove: conferma
  prima di registrare una quantità diversa da quella proposta (283); tastierino del programma (284); chi segue la merce
  mancante con i piani (al terzo giro).
- 19/11/2026, terzo giro: accettate le consigliate (285–291). Fatti di UFP: dopo una spedizione parziale il preparatore
  non vede più l'ordine, il resto lo segue il responsabile che crea il piano; la merce appena caricata sta in «check».
  Responsabili e admin soprattutto dal computer (292).
- 19/11/2026, dopo una seconda prova: la giacenza si sceglie dentro l'articolo, non nella riga (293). Riepilogo: si entra
  subito nell'articolo (294); «Elimina» e «Rimetti a posto» sugli articoli presi (295); resti con la coda (296); area di
  ricevimento senza scansione dell'ubicazione (297); «Ordini da assegnare», scelta dell'utente diversa dalla proposta
  (298); riepilogo confermato (299).

## Answer

Chiuso il 19/11/2026 in tre giri più il riepilogo, con la pagina https://claude.ai/artifact/SdXpDTDFxGAs76mx17cNb5
(privata). Decisioni 271–299; specifica in «Percorso delle schermate» → «Preparazione e spedizione» di
`docs/architettura.md` («Elenco del prelievo» e «Ciò che resta da spedire»); prototipo
`prototipi/percorso-schermate/index.html` (https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata) con l'ordine
d'esempio 1060 di 15 articoli, provato nel browser a larghezza di telefono; termini nuovi in `GLOSSARY.md`: elenco del
prelievo, prelievo guidato, resto.

- L'ordine si apre sull'elenco in ordine di ubicazione, con «Prelievo guidato» e «Sospendi» in cima; gruppi «Da
  prendere», «Restano aperti», «Presi» (270, 274, 281, 282).
- Toccando un articolo da prendere si entra nell'articolo, dove si scelgono giacenza e quantità; toccando un articolo
  preso, «Elimina» e «Rimetti a posto»; 📷 entra nell'articolo inquadrato (276, 293–295).
- Un solo tasto «Correggi giacenza» al posto di «Ne trovo di più/meno» (273). «Più tardi» al posto di «Aspetto» (275).
- «Concludi senza» dove si decide davvero; nel prelievo guidato «Prosegui» fino all'ultimo; con 0 si lascia aperto tutto
  l'articolo; conferma prima di registrare una quantità diversa (272, 279, 283, 289). Il tasto resta «Preso» (280).
- Tastierino del programma al telefono e al palmare in tutte le quantità; al computer tastiera e icona (284, 290, 291).
- Il resto resta nello stesso ordine: con i piani lo segue il responsabile dei piani in «Da completare», con l'avviso
  all'arrivo e «Crea piano» con il preparatore della prima parte; con la coda torna in coda da solo, con una scelta in
  Configurazione (285–288, 296). Area di ricevimento senza scansione dell'ubicazione (297).
- Vendita assistita con lo stesso elenco, «Quantità» ed «Elimina» (277). «Ordini da assegnare» nel nuovo piano (298).
- Per «Aspetto grafico»: responsabili e admin soprattutto dal computer (292).
