# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. Consigliato ora: «Inventario periodico» (prompt A), che con «Nome del prodotto» e lo
stack sblocca «Aspetto grafico». Quando nei repository privati ci sono foto o bolle da aprire, sessioni a parte lavorano
la prova visiva (prompt B) e la prova di lettura delle bolle (prompt C). Si possono avviare in parallelo.

**Prompt A: inventario periodico**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Inventario periodico»
(grilling), che parte dalla ricerca sui gestionali esistenti (§ 1.7) e dalle decisioni 77, 190, 191, 207 e 222.
Leggi i commenti del ticket. Aggiorna il prototipo prototipi/percorso-schermate/index.html con le schermate
dell'inventario, senza aspetto grafico.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

Per un altro ticket preciso, sostituire il titolo (per esempio «Punti di estensione per la specializzazione» o «Nome
del prodotto»).

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

## Frontiera al 18/11/2026 (fine sessione)

In ordine di numero:

1. «Esecuzione della prova visiva e scelta del modello» (task con l'utente): **in corso**, su più sessioni. Il
   repository privato `av3rgfx/prova-visiva-foto` esiste; la pagina di scatto è su https://av3rgfx.github.io/DondEres/
   (ramo `gh-pages`, da non cancellare; se la pagina cambia va copiata anche lì). Tocca all'utente scegliere gli
   articoli, scattare e caricare gli ZIP in `da-caricare` (decisioni 149–159). Poi prompt B.
2. «Punti di estensione per la specializzazione»: libero. Da raccogliere anche: collegamento con Ad Hoc per gli ordini
   degli agenti e le vendite assistite (178), confronto tra merce caricata e fattura (192), invio degli ordini fornitore
   dal programma come le richieste di reso (226), documento di reso e «reso da cliente» verso Ad Hoc (24, 27).
3. «Nome del prodotto»: libero; poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Inventario periodico» (grilling): libero, consigliato ora (prompt A). «Aspetto grafico» aspetta ancora questo.
5. «Esecuzione della prova di lettura delle bolle» (task con l'utente, nuovo): parte quando le bolle sono nella cartella
   `bolle/` del repository privato (prompt C).

## In sospeso fuori dalla mappa

- Domande per il rivenditore di UFP in `docs/domande-rivenditore-ufp.md` (dalla 17 alla 27; la 24 annotata e la 27
  aggiunta il 18/11/2026, sui resi): le manda l'utente (decisione 57). Le risposte si annotano in fondo al file;
  servono al connettore Ad Hoc della specializzazione, non bloccano la mappa.
- Punto tecnico aperto: mandare le mail dalla casella aziendale di ogni responsabile (223) chiede un permesso al server
  di posta dell'azienda; si sceglie con lo stack e all'installazione.

## Ultimo ticket chiuso

18/11/2026: «Resi», in tre giri, con la pagina https://claude.ai/artifact/KQtNpyrXjbywxnz1iGKnGY (privata). Decisioni
207–226, sezione «Resi» in `docs/architettura.md`, prototipo con le schermate dei resi
(`prototipi/percorso-schermate/index.html`, anche https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata). Prima,
nella stessa sessione, la ricerca «Lettura automatica delle bolle» (`docs/research/2026-11-18-lettura-automatica-bolle.md`,
decisioni 202–206 sulla prova). Termini nuovi in `GLOSSARY.md`: reso al fornitore, reso del cliente, da rendere, area
resi, richiesta di reso, riserva.

## Ultima sessione

18/11/2026: ricerca sulla lettura delle bolle con un sotto-agente; l'utente ha mostrato in chat 10 foto di bolle di UFP
(AGB, ISEO, SAIT, più una lettera di vettura) e alcune mail di reso e di segnalazione: nel repository solo i fatti,
senza nomi e senza le immagini. Prova con zxing-cpp sulle foto: DataMatrix di AGB con numero e data, barcode di riga di
ISEO. Poi «Resi» in tre giri. L'utente chiede un carico semplice e veloce quando mancano codici o quantità (222, 224).

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova visiva, scattare il primo giro (10–20 articoli) e caricare gli ZIP.
- Raccogliere il primo giro di 20 bolle per la prova di lettura, coprire i dati dei clienti e caricarle in `bolle/` nel
  repository privato (202–204); dire quali fornitori sono ricorrenti e quanti mandano il PDF.
- Mandare al rivenditore le domande 21–27.
- Se le etichette sotto il monitor dell'ufficio contengono password vere, cambiarle e toglierle (si vedevano nelle foto
  delle mail).
