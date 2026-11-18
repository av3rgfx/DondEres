# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione, più le ricerche. Consigliato ora: la ricerca sui gestionali esistenti e poi «Completezza del percorso delle
schermate» (prompt A). Quando nel repository privato ci sono ZIP da aprire, una sessione a parte lavora la prova visiva
(prompt B). Si possono avviare in parallelo.

**Prompt A: gestionali esistenti e completezza delle schermate**

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora due ticket, in quest'ordine:
1. la ricerca «Gestionali di magazzino esistenti: funzioni in più e difetti da evitare»: falla molto approfondita, con
   un sotto-agente che usa la skill research; fonti primarie, data e link; i difetti segnalati dagli utenti come
   esperienze riferite, non come fatti;
2. poi «Completezza del percorso delle schermate» (prototype), che parte dai risultati della ricerca.
Leggi i commenti dei due ticket e le decisioni 160–183. Voglio un'analisi della situazione: cosa manca alla base rispetto
ai gestionali esistenti e a come si lavora davvero in UFP, cosa evitare dei loro difetti, e soluzioni migliori per
il DDT (decisione 183). Poi aggiorna il prototipo prototipi/percorso-schermate/index.html perché sia completo: tasti
Annulla e Conferma, elenchi delle cose in sospeso per ogni sezione, sezione Documenti con storico e log, DDT con le righe
create dalle letture e il ripiego a mano per articolo o per ordine. Resta senza aspetto grafico (ticket «Aspetto grafico»).
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

Per un altro ticket preciso, sostituire i titoli (per esempio «Punti di estensione per la specializzazione» o «Nome del
prodotto»).

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
   piani di spedizione gli ordini degli agenti e riceve le vendite assistite (178).
3. «Nome del prodotto»: libero; poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Gestionali di magazzino esistenti: funzioni in più e difetti da evitare» (ricerca): libero, consigliato ora
   (prompt A), richiesto dall'utente il 18/11/2026 (decisione 180).
5. «Completezza del percorso delle schermate»: si sblocca con la ricerca del punto 4; stessa sessione (prompt A).
   «Aspetto grafico» ora aspetta anche questo ticket.

«Percorso delle schermate» è chiuso (decisioni 160–179), ma l'utente l'ha trovato non completo (180–183): si riprende
nel ticket del punto 5.

## In sospeso fuori dalla mappa

- Domande per il rivenditore di UFP in `docs/domande-rivenditore-ufp.md` (aggiunte la 17, la 18 e la 20 il
  16/11/2026; la 20 riguarda gli articoli non a catalogo sugli ordini fornitore; la 21 e la 22 il 17/11/2026, su
  agente, corriere, colli e peso): le manda l'utente (decisione 57). Le
  risposte si annotano in fondo al file; servono al connettore Ad Hoc della specializzazione, non bloccano la mappa.

## Ultimo ticket chiuso

17/11/2026: «Percorso delle schermate». Decisioni 160–179, sezione «Percorso delle schermate» in
`docs/architettura.md`, prototipo in `prototipi/percorso-schermate/index.html` (anche
https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata). Termini nuovi in `GLOSSARY.md`: vendita assistita, agente,
piano di spedizione, coda di prelievo, corriere, mansione, permesso.

## Ultima sessione

17/11/2026, notte, e 18/11/2026: chiuso «Percorso delle schermate» in quattro giri di domande, con il prototipo provato
dall'utente sul telefono. Dopo la prova l'utente l'ha trovato giusto ma grezzo e ha chiesto una ricerca sui gestionali
esistenti, gli elenchi delle cose in sospeso, la sezione «Documenti» e il DDT automatico (decisioni 180–183): nuovi
ticket «Gestionali di magazzino esistenti: funzioni in più e difetti da evitare» e «Completezza del percorso delle
schermate». Pagina usata per le domande: https://claude.ai/artifact/BpARZrpffCDENtsKzZgTSZ (privata).
In parallelo resta in corso «Esecuzione della prova visiva e scelta del modello» (prompt B), che aspetta le foto.

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova (200 a catalogo, 40 fuori, 300 di contorno) e tenere l'elenco nel
  repository privato.
- Primo giro piccolo di foto (10–20 articoli) con la pagina di scatto, poi gli ZIP in `da-caricare`.

