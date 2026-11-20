# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. 20/11/2026: chiuso il ticket «Divisione tra telefono, computer e server in sede»
(decisioni 406–421, sezione omonima di `docs/architettura.md`): dati, assegnazione, impronte e foto sul server; codice
letto più foto a ogni inquadratura; fascia «Senza rete» con l'operazione in attesa. Prossimo passo: prompt J (stack).
Poi, con i numeri della prova visiva, il ticket «Impronte e server in sede, dopo la prova», e infine l'aspetto grafico.
Quando nei repository privati ci sono foto o bolle da aprire, sessioni a parte lavorano la prova visiva (prompt B) e la
prova delle bolle (prompt C). Restano fuori dai ticket la prova di stampa del marchio (403) e la ricerca europea dei
marchi dal consulente (387). I prompt A, D, E, F, G, H e I restano come esempi di forma.

**Prompt J: stack**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Stack»: leggi i suoi
commenti. Si scelgono linguaggi, database e librerie della base (decisione 13), partendo da web app servita dal server
in sede (119–127), punti di estensione e moduli (301–320) e divisione tra le macchine (406–421, sezione «Divisione tra
telefono, computer e server in sede» di docs/architettura.md): lettura del barcode nel browser, canale aperto con ogni
dispositivo, operazioni in attesa nella memoria del browser, database e archivio delle foto, confronto esatto tra le
impronte, certificato e aggiornamenti con copia di sicurezza, moduli a versione. Il programma che fa girare il modello
visivo e la macchina in sede restano al ticket «Impronte e server in sede, dopo la prova» (405): scegli uno stack che
non li blocchi. La 127 chiede prove su dispositivi veri (iPhone, Android, palmare di UFP) prima di scegliere: dimmi cosa
si può scegliere prima e proponimi come farle (per esempio una pagina di prova pubblicata come la pagina di scatto,
149), ricordando che computer e server aziendali non si toccano finché non c'è una versione da provare (143). Decidi
con me anche quando sostituire il nome provvisorio DondEres con Ripo nel repository (nebbia della mappa).
Consulta le decisioni già prese senza rimetterle in discussione e le ricerche in docs/research/ quando servono (per le
librerie soprattutto docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md, §E–H); se serve un fatto nuovo
(versioni, licenze, manutenzione), fai una ricerca con la skill research e salvala in docs/research/. Usa le skill
grilling, domain-modeling e ponytail (full); termini chiariti in GLOSSARY.md, la tua parte in docs/architettura.md.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo. Parlami in italiano, con domande semplici: cosa
chiedi, perché conta, cosa comporta ogni opzione.
Per le domande crea una pagina privata nuova, come quella della divisione (copia in prototipi/stack/index.html), con
esempi visivi che cambiano con la risposta (per esempio lo schema dei pezzi del programma), opzione consigliata,
«Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto». Lavora a giri:
registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare. Poi chiudi il ticket,
aggiorna la mappa e prepara il prompt della sessione successiva.
```

**Prompt I: divisione tra telefono, computer e server in sede**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Divisione tra telefono,
computer e server in sede»: leggi i suoi commenti e la decisione 405, che lo ha diviso in due. Qui si decide solo ciò
che non dipende dai numeri della prova visiva: database, archivio delle foto, assegnazione, ricerca tra le impronte,
lettura di barcode, codice stampato e quantità, cosa viaggia in rete per ogni inquadratura, cosa resta sul telefono
quando cade la rete (23, 127). Dove si calcolano le impronte e che macchina serve in sede restano al ticket «Impronte e
server in sede, dopo la prova». Consulta le decisioni già prese senza rimetterle in discussione (soprattutto 87–104,
119–127, 143, 301–320) e le ricerche in docs/research/ quando servono.
Usa le skill grilling e domain-modeling; termini chiariti in GLOSSARY.md, la tua parte in docs/architettura.md.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo. Parlami in italiano, con domande semplici: cosa
chiedi, perché conta, cosa comporta ogni opzione.
Per le domande crea una pagina privata nuova, come quella del brand kit (copia in prototipi/divisione/index.html),
con esempi visivi che cambiano con la risposta (per esempio uno schema di cosa gira dove), opzione consigliata,
«Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto». Lavora a giri:
registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare. Poi chiudi il ticket,
aggiorna la mappa e prepara il prompt per lo stack.
```

**Prompt H: kit finale di Ripo**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Brand kit con la skill
logo-design», già in corso con me: leggi i suoi commenti, le decisioni 362–397 e la sezione «Brand kit» di
docs/architettura.md (in fondo, «Stato a fine sessione»). Usa la skill logo-design (fase 7, il kit) sulla R scelta,
prototipi/brand-kit/concetti-7/pulito-simbolo.svg (generata da concetti-7/genera.py), con il nome «Ripo» a peso medio,
il blu elettrico #1F5BFF e le indicazioni delle ricerche docs/research/2026-11-20-analisi-libreria-lettera-r.md e
docs/research/2026-11-20-loghi-lettera-singola-fonti.md. Il kit: rifinitura ottica, R per i 16 punti, blu chiaro per
il tema scuro, versioni nera, bianca e blu, icone (favicon, icone dell'app, manifest), tavola d'uso, guida di una
pagina, confronto affiancato con Revolut e con le R della raccolta. Le scelte di gusto sono mie: mostrami il kit e
fammelo confermare; poi chiudi il ticket e aggiorna la mappa.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa la pagina https://claude.ai/artifact/JQ2vwNwRMfT2qi4BDWNnX5 (copia in prototipi/brand-kit/index.html),
con esempi visivi che cambiano con la risposta, opzione consigliata, «Accetta tutte le consigliate», note facoltative
e risposte salvate che leggi tu quando scrivo «fatto». Lavora a giri: registra le risposte di ogni giro prima del
successivo e chiudi con un riepilogo da confermare.
```

**Prompt G: nome in R e kit (dopo la verifica nei registri)**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Brand kit con la skill
logo-design», già in corso con me (leggi i suoi commenti e le decisioni 362–385, e la sezione «Brand kit» di
docs/architettura.md). Prima chiudi il ticket «Verifica dei nomi in R nei registri dei marchi»: ti incollo i risultati
di TMview che ho cercato a mano (o il parere del consulente); scrivili in docs/research/2026-11-20-unicita-nomi-in-r.md
e fammi scegliere il nome. Poi prepara il kit sulla R · Rampa (prototipi/brand-kit/concetti-3/) con la skill
logo-design: lettere del nome, colore lontano da rosso, verde e giallo (367), versioni, icone, guida.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa la pagina https://claude.ai/artifact/JQ2vwNwRMfT2qi4BDWNnX5 (o una nuova), con esempi visivi che
cambiano con la risposta, opzione consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che
leggi tu quando scrivo «fatto». Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un
riepilogo da confermare.
```

**Prompt F: brand kit**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Brand kit con la skill
logo-design» (leggi l'etichetta del ticket per il tipo). Leggi i commenti del ticket e le decisioni 20, 351, 358 e
359. Prima di installare la skill logo-design nel progetto (.claude/skills e .agents/skills, uguali) leggine il
contenuto e dimmi cosa fa; niente installazioni globali. Le scelte di gusto sono mie.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

**Prompt E: unicità dei nomi scelti**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Risolvi la ricerca «Unicità dei nomi scelti»
con la skill research: fonti primarie (registri EUIPO, UIBM, WIPO; domini; prodotti simili nel settore), un file in
docs/research/ con data e link. Leggi i commenti del ticket e le decisioni 349, 354 e 356. È una ricerca, non un
parere legale. Poi mostrami i risultati senza abbellirli e fammi scegliere il nome, con le stesse regole delle
domande: registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in
docs/architettura.md. Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni
opzione. Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
```

**Prompt A: resi del cliente nel magazzino Shopify**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Prima risolvi la ricerca «Shopify: resi,
rimborsi e cosa si può collegare» con la skill research: fonti primarie, un file in docs/research/ con data e link.
Poi lavora con me il ticket «Resi del cliente nel magazzino Shopify» (grilling), partendo da come si lavora oggi
(decisione 321) e dai risultati della ricerca: mostrami prima, senza abbellirlo, cosa si può fare in automatico con
Shopify e cosa no, e tutto quello a cui ci si può collegare. Leggi i commenti dei due ticket e la parte «Reso del
cliente» della sezione «Resi» di docs/architettura.md (decisioni 210–212).
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

**Prompt D: nome del prodotto**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Nome del prodotto»
(leggi l'etichetta del ticket per il tipo). Leggi i commenti del ticket e la decisione 20.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

Per un altro ticket preciso, sostituire il titolo.

**Prompt B: prova visiva, quando ci sono ZIP in `da-caricare`** (collegare alla sessione il repository privato
`av3rgfx/prova-visiva-foto`)

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Esecuzione della prova
visiva e scelta del modello», già in corso con me. Controlla che il repository privato prova-visiva-foto sia
collegato alla sessione; se non c'è, chiedimelo prima di tutto il resto. Poi apri gli ZIP con
prova-visiva/script/prepara.py, fai il commit nel repository privato e calcola i numeri seguendo
prova-visiva/script/LEGGIMI.md. Mostrami i risultati senza abbellirli e proponimi le due scelte sulle soglie
annotate nella sezione «Script del calcolo» di docs/architettura.md.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

**Prompt C: prova di lettura delle bolle, quando ci sono bolle in `bolle/`** (collegare alla sessione il repository
privato `av3rgfx/prova-visiva-foto`)

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Esecuzione della prova di
lettura delle bolle» (task con me), con il piano della sezione «Lettura automatica delle bolle» di
docs/architettura.md (decisioni 202–206 e 221) e la ricerca docs/research/2026-11-18-lettura-automatica-bolle.md.
Controlla che il repository privato prova-visiva-foto sia collegato alla sessione; se non c'è, chiedimelo prima di
tutto il resto. Primo giro di 20 bolle: scrivi gli script (senza bolle) nel repository del progetto, prepara con me la
verità di ogni bolla, fai girare i sistemi e mostrami i numeri senza abbellirli.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

## Frontiera al 19/11/2026, sera tardi

In ordine di numero:

1. «Esecuzione della prova visiva e scelta del modello» (task con l'utente): **in corso**, su più sessioni. Il
   repository privato `av3rgfx/prova-visiva-foto` esiste; la pagina di scatto è su https://av3rgfx.github.io/DondEres/
   (ramo `gh-pages`, da non cancellare; se la pagina cambia va copiata anche lì). Tocca all'utente scegliere gli
   articoli, scattare e caricare gli ZIP in `da-caricare` (decisioni 149–159). Poi prompt B.
2. Ricerca «Shopify: resi, rimborsi e cosa si può collegare» e poi «Resi del cliente nel magazzino Shopify»: liberi,
   consigliati (prompt A, decisione 321).
3. «Nome del prodotto»: libero (prompt D); poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Esecuzione della prova di lettura delle bolle» (task con l'utente): parte quando le bolle sono nella cartella
   `bolle/` del repository privato (prompt C).
5. «Stack»: aspetta solo la divisione tra telefono, computer e server, che aspetta la prova visiva. «Punti di
   estensione» è chiuso (decisioni 301–320).

## In sospeso fuori dalla mappa

- Domande per il rivenditore di UFP in `docs/domande-rivenditore-ufp.md` (dalla 17 alla 29; la 24 annotata, la 27 sui resi
  e la 28 sull'inventario aggiunte il 18/11/2026, la 29 sull'uscita della vendita assistita il 19/11/2026): le manda
  l'utente (decisione 57). Le risposte si annotano in fondo al file; servono al collegamento Ad Hoc della
  specializzazione, non bloccano la mappa.
- Domande al rivenditore, 19/11/2026: l'utente teme che un'email da privato, senza UFP alle spalle, resti senza risposta,
  e non può scrivere a nome di UFP. Proposta in attesa di risposta: (A) dividere il file in una lista «da osservare in
  UFP» (la maggior parte delle domande: versione, moduli, documenti, OP e bolla, agente e corriere, resi, giacenza dopo
  una vendita) e una breve email con le 5–6 domande che solo il rivenditore può chiarire (permesso sul database,
  ambiente di prova, come scrive ARS, frequenza delle letture, costi), da far mandare a UFP quando adotterà il
  programma; (B) una ricerca online sulle poche domande generali (importazione da file, servizi web, «NEX Logistica»,
  fatture elettroniche). Non bloccano la mappa: il collegamento Ad Hoc sta nella specializzazione.
- Punto tecnico aperto: mandare le mail dalla casella aziendale di ogni responsabile (223, 311) chiede un permesso al
  server di posta dell'azienda; si sceglie con lo stack e all'installazione.

## Ultimo ticket chiuso

19/11/2026: «Punti di estensione per la specializzazione», in due giri più il riepilogo, con la pagina
https://claude.ai/artifact/H5oSLLHmbpw3qMAXpNFEkz (privata). Decisioni 301–320, sezione «Punti di estensione» di
`docs/architettura.md`, termini nuovi in `GLOSSARY.md` (base, specializzazione, configurazione, modulo, collegamento,
punto d'aggancio, partita, lettore di etichette, campo aggiuntivo, «Da registrare nel gestionale»), domanda 29 per il
rivenditore. Prima, lo stesso giorno: «Elenco del prelievo e correzione della quantità» (270–300).

## Ultima sessione

20/11/2026: «Brand kit con la skill logo-design», dodici giri (decisioni 362–397), pagina privata
https://claude.ai/artifact/JQ2vwNwRMfT2qi4BDWNnX5. Skill installata nel progetto senza la raccolta di loghi altrui
(362). Concetti sulla V scartati (369, 374); ordine invertito, prima la lettera e poi il nome (375). Varko in riserva
(376); nome per ora **Ripo** dopo una verifica UIBM riportata dall'utente (386, 387). Blu elettrico (388). Dopo due
ricerche sui loghi a lettera singola, R scelta: **Pulito costruito** (396). Il kit finale è il prossimo passo (397).

## Cose dell'utente, senza sessione

- Quando si parla con il consulente in marchi: ricerca europea per somiglianza su Ripo (il RIPPO di AISLUX in classe
  35 da guardare) e sulla R come marchio figurativo (387, 359).

- Scegliere a caso gli articoli della prova visiva, scattare il primo giro (10–20 articoli) e caricare gli ZIP.
- Raccogliere il primo giro di 20 bolle per la prova di lettura, coprire i dati dei clienti e caricarle in `bolle/` nel
  repository privato (202–204); dire quali fornitori sono ricorrenti e quanti mandano il PDF.
- Rispondere alla proposta A/B sulle domande al rivenditore (sopra); non mandare l'email da privato per ora.
