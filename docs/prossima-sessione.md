# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. Consigliato ora: «Punti di estensione per la specializzazione» (prompt A), che sblocca lo
stack con la divisione tra le macchine; in alternativa «Nome del prodotto», che porta al brand kit. «Aspetto grafico»
aspetta ancora brand kit e stack. Quando nei repository privati ci sono foto o bolle da aprire, sessioni a parte lavorano
la prova visiva (prompt B) e la prova di lettura delle bolle (prompt C). Si possono avviare in parallelo.

**Prompt A: punti di estensione per la specializzazione**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Punti di estensione per la
specializzazione» (grilling). Raccogli anche i punti lasciati alla specializzazione nelle sezioni di
docs/architettura.md (collegamento con Ad Hoc per ordini degli agenti e vendite assistite, 178; confronto tra merce
caricata e fattura, 192; invio degli ordini fornitore dal programma, 226; documento di reso e «reso da cliente», domande
24 e 27; inventario verso Ad Hoc, domanda 28). Leggi i commenti del ticket.
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

## Frontiera al 18/11/2026 (fine sessione dell'inventario)

In ordine di numero:

1. «Esecuzione della prova visiva e scelta del modello» (task con l'utente): **in corso**, su più sessioni. Il
   repository privato `av3rgfx/prova-visiva-foto` esiste; la pagina di scatto è su https://av3rgfx.github.io/DondEres/
   (ramo `gh-pages`, da non cancellare; se la pagina cambia va copiata anche lì). Tocca all'utente scegliere gli
   articoli, scattare e caricare gli ZIP in `da-caricare` (decisioni 149–159). Poi prompt B.
2. «Punti di estensione per la specializzazione»: libero. Da raccogliere anche: collegamento con Ad Hoc per gli ordini
   degli agenti e le vendite assistite (178), confronto tra merce caricata e fattura (192), invio degli ordini fornitore
   dal programma come le richieste di reso (226), documento di reso e «reso da cliente» verso Ad Hoc (24, 27),
   inventario verso Ad Hoc (domanda 28). Consigliato ora (prompt A).
3. «Nome del prodotto»: libero; poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Esecuzione della prova di lettura delle bolle» (task con l'utente, nuovo): parte quando le bolle sono nella cartella
   `bolle/` del repository privato (prompt C).

## In sospeso fuori dalla mappa

- Domande per il rivenditore di UFP in `docs/domande-rivenditore-ufp.md` (dalla 17 alla 28; la 24 annotata, la 27 sui resi
  e la 28 sull'inventario aggiunte il 18/11/2026): le manda l'utente (decisione 57). Le risposte si annotano in fondo al file;
  servono al connettore Ad Hoc della specializzazione, non bloccano la mappa.
- Punto tecnico aperto: mandare le mail dalla casella aziendale di ogni responsabile (223) chiede un permesso al server
  di posta dell'azienda; si sceglie con lo stack e all'installazione.

## Ultimo ticket chiuso

18/11/2026: «Inventario periodico», in tre giri, con la pagina https://claude.ai/artifact/QGQvc1pHzoQTsJBATiM1g5
(privata). Decisioni 227–245, sezione «Inventario periodico» in `docs/architettura.md`, prototipo con le schermate
dell'inventario (`prototipi/percorso-schermate/index.html`, anche https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur,
privata). Termini nuovi in `GLOSSARY.md`: inventario, conta cieca, seconda conta, differenza d'inventario, in conta.
Prima, sempre il 18/11/2026: «Resi» (207–226) e la ricerca «Lettura automatica delle bolle» (202–206).

## Ultima sessione

18/11/2026: «Inventario periodico» in tre giri. Fatti dall'utente: in UFP e nel magazzino Shopify l'inventario di tutto
si fa una volta l'anno (in UFP su carta o foglio di calcolo, ricopiato in Ad Hoc; ARS non si usa) e durante l'anno si
corregge sul momento. Scelta dell'utente diversa dalla proposta: «tutto il magazzino» sono solo gli scaffali (239).
Poi, guardando il prototipo da telefono, l'utente ha corretto la preparazione (decisioni 246–257, pagina privata
https://claude.ai/artifact/Qft5i5wPiwfyYEQpdUz5Kq): sospendere o concludere senza l'articolo mancante, resto che parte
dopo, avvisi che non bloccano nel piano e nell'anteprima, «Ne trovo di più/meno» in un passo solo, righe che non
risultano in fondo al prelievo, «Altri lavori» solo con lavori dati in più e permessi, lavoro dei colleghi per
magazzino. Specifica in «Percorso delle schermate» → «Preparazione e spedizione». Deduzione ancora da confermare: un
ordine senza nessun pezzo preso non diventa pronto.
Il 19/11/2026: giacenze per ubicazione e scelta dell'ubicazione al prelievo e nella vendita assistita, aggiunta da
«Cerca» nella vendita (258–260); «Disponibilità» al posto di «liberi» (261); interfaccia pulita con un «ⓘ» nel titolo
(262, 266, 267); tre gruppi di permessi, Admin, Responsabile di magazzino e Responsabile dei piani, con gli avvisi
della preparazione al responsabile dei piani (263–265; corregge la 27). Pagina privata delle domande:
https://claude.ai/artifact/ScDtAoDaYsTP1K3b61x6MP.

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova visiva, scattare il primo giro (10–20 articoli) e caricare gli ZIP.
- Raccogliere il primo giro di 20 bolle per la prova di lettura, coprire i dati dei clienti e caricarle in `bolle/` nel
  repository privato (202–204); dire quali fornitori sono ricorrenti e quanti mandano il PDF.
- Mandare al rivenditore le domande 21–28.
