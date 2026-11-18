# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. Consigliato ora: la ricerca «Lettura automatica delle bolle» e poi «Resi» (prompt A).
Quando nel repository privato ci sono ZIP da aprire, una sessione a parte lavora la prova visiva (prompt B). Si possono
avviare in parallelo.

**Prompt A: lettura automatica delle bolle e resi**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora due ticket, in quest'ordine:
1. la ricerca «Lettura automatica delle bolle» (decisione 193): falla approfondita, con un sotto-agente che usa la
   skill research; fonti primarie, data e link; programmi e modelli che girano in sede, con licenza e requisiti;
   proponimi alla fine una prova su bolle vere, chiedendomi prima dove conservarle;
2. poi «Resi» (grilling), che parte dalla ricerca sui gestionali esistenti (§ 1.8) e dalle decisioni 45, 114, 191.
Leggi i commenti dei due ticket. Aggiorna il prototipo prototipi/percorso-schermate/index.html con le schermate dei
resi, senza aspetto grafico.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

Per un altro ticket preciso, sostituire i titoli (per esempio «Inventario periodico», «Punti di estensione per la
specializzazione» o «Nome del prodotto»).

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

## Frontiera al 18/11/2026 (fine sessione)

In ordine di numero:

1. «Esecuzione della prova visiva e scelta del modello» (task con l'utente): **in corso**, su più sessioni. Il
   repository privato `av3rgfx/prova-visiva-foto` esiste; la pagina di scatto è su https://av3rgfx.github.io/DondEres/
   (ramo `gh-pages`, da non cancellare; se la pagina cambia va copiata anche lì). Tocca all'utente: scegliere a caso gli
   articoli (200 a catalogo, 40 fuori, 300 di contorno), scattare con l'iPhone e caricare gli ZIP in `da-caricare`
   (decisioni 149–159). Poi prompt B: gli script in `prova-visiva/script/` sono pronti (istruzioni in `LEGGIMI.md`).
2. «Punti di estensione per la specializzazione»: libero. Da raccogliere anche il collegamento con Ad Hoc che porta ai
   piani di spedizione gli ordini degli agenti e riceve le vendite assistite (178), e il confronto tra merce caricata
   e fattura (192).
3. «Nome del prodotto»: libero; poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Resi» (grilling) e «Inventario periodico» (grilling): liberi, nuovi (decisione 200). «Aspetto grafico» ora aspetta
   anche questi due.
5. «Lettura automatica delle bolle» (ricerca): libera, nuova (decisione 193), consigliata ora (prompt A).

## In sospeso fuori dalla mappa

- Domande per il rivenditore di UFP in `docs/domande-rivenditore-ufp.md` (aggiunte la 17, la 18 e la 20 il
  16/11/2026; la 21 e la 22 il 17/11/2026, su agente, corriere, colli e peso; dalla 23 alla 26 il 18/11/2026, su
  rettifiche di carichi fatturati, DDT di reso, etichette dei corrieri e fatture con i riferimenti ai DDT): le manda
  l'utente (decisione 57). Le risposte si annotano in fondo al file; servono al connettore Ad Hoc della
  specializzazione, non bloccano la mappa.

## Ultimo ticket chiuso

18/11/2026: «Completezza del percorso delle schermate». Decisioni 184–201, sezione «Percorso delle schermate» in
`docs/architettura.md` (con l'analisi del 18/11/2026), prototipo in `prototipi/percorso-schermate/index.html` (anche
https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata). Prima, nella stessa sessione, la ricerca «Gestionali di
magazzino esistenti: funzioni in più e difetti da evitare» (`docs/research/2026-11-18-gestionali-magazzino-esistenti.md`).
Termini nuovi in `GLOSSARY.md`: bolla, quantità in bolla, cose in sospeso, merce danneggiata, scarto, registro.

## Ultima sessione

18/11/2026: ricerca sui gestionali esistenti (Odoo, Business Central, Dynamics SCM, SAP, NetSuite, Oracle, Shopify,
Zoho e altri; G2, Capterra e Reddit non raggiungibili), analisi della base, poi «Completezza del percorso delle
schermate» in tre giri di domande nella pagina https://claude.ai/artifact/13EHJFJ3ZbM8QNXU1dTkag (privata). L'utente
vuole leggere in automatico anche le righe della bolla (193): nuovo ticket di ricerca. In parallelo resta in corso
«Esecuzione della prova visiva e scelta del modello» (prompt B), che aspetta le foto.

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova (200 a catalogo, 40 fuori, 300 di contorno) e tenere l'elenco nel
  repository privato.
- Primo giro piccolo di foto (10–20 articoli) con la pagina di scatto, poi gli ZIP in `da-caricare`.
- Mandare al rivenditore le domande 21–26.
- Tenere da parte 5–10 bolle vere di UFP (con i dati dei clienti coperti) per la futura prova di lettura.
