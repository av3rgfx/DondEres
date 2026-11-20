# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. I due ticket sui resi del cliente nel magazzino Shopify sono chiusi
(19/11/2026, decisioni 322–343; il prompt A resta come esempio di forma). Anche «Nome del prodotto» è chiuso
(20/11/2026, decisioni 344–357; il prompt D resta come esempio): preferiti in ordine Kurso, Varko, Velko. Consigliato
ora: «Unicità dei nomi scelti» (prompt E), una ricerca che porta alla scelta del nome e al brand kit. Lo stack aspetta
ancora la divisione tra le macchine, che aspetta la prova visiva; «Aspetto grafico» aspetta brand kit e stack (deve
contare anche la vista da computer per responsabili e admin, decisione 292). Quando nei repository privati ci sono
foto o bolle da aprire, sessioni a parte lavorano la prova visiva (prompt B) e la prova di lettura delle bolle
(prompt C).

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

19/11/2026: «Punti di estensione per la specializzazione». Una base sola, adattata con «Configurazione» e moduli che
scriviamo noi; quattro punti d'aggancio (collegamento, lettore di etichette, precedenza dell'assegnazione, partita); un
documento che il collegamento non sa mandare va in «Da registrare nel gestionale»; l'aggiornamento non parte se un
modulo non va. Dai punti lasciati ad Ad Hoc: la merce di una vendita assistita è prelevata alla conferma ed esce quando
sceglie l'admin (in UFP candidato il passaggio da OP a bolla, domanda 29); ordini degli agenti con un filtro; confronto
con la fattura facoltativo; ordini fornitore con «Invia al fornitore» e un testo di serie; ogni documento ha un solo
autore (in UFP Ad Hoc fa bolle e fatture). «Collegamento» al posto di «connettore» (316). L'utente ha chiesto che le
scelte che dipendono dal modo di lavorare del magazzino stiano in Configurazione (308, 310).

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova visiva, scattare il primo giro (10–20 articoli) e caricare gli ZIP.
- Raccogliere il primo giro di 20 bolle per la prova di lettura, coprire i dati dei clienti e caricarle in `bolle/` nel
  repository privato (202–204); dire quali fornitori sono ricorrenti e quanti mandano il PDF.
- Rispondere alla proposta A/B sulle domande al rivenditore (sopra); non mandare l'email da privato per ora.
