# Prompt per la prossima sessione (Wayfinder sull'architettura)

Da incollare all'avvio di una nuova sessione sul ramo principale aggiornato. La mappa esiste già: si lavora un ticket
per sessione. Consigliato ora: «Punti di estensione per la specializzazione» (prompt A). Quando nel repository privato ci sono ZIP da
aprire, una sessione a parte lavora la prova visiva (prompt B). Si possono avviare in parallelo.

**Prompt A: punti di estensione** (oppure, se già preso, il primo ticket libero della frontiera)

```text
/wayfinder .scratch/architettura/map.md

Leggi prima AGENTS.md, poi la mappa (solo map.md, non tutti i ticket). Lavora il ticket «Punti di estensione per la
specializzazione»; se è già preso, prendi il primo ticket della frontiera: aperto, non bloccato, non preso.
Registra ogni mia decisione in docs/decisioni.md, con data e motivo; scrivi la tua parte in docs/architettura.md.
Parlami in italiano, con domande semplici: cosa chiedi, perché conta, cosa comporta ogni opzione.
Per le domande usa una pagina interattiva (Artifact) con esempi visivi che cambiano con la risposta, opzione
consigliata, «Accetta tutte le consigliate», note facoltative e risposte salvate che leggi tu quando scrivo «fatto».
Lavora a giri: registra le risposte di ogni giro prima del successivo e chiudi con un riepilogo da confermare.
```

Per un altro ticket preciso, sostituire il titolo nella seconda riga (per esempio «Nome del prodotto»).

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

## Frontiera al 17/11/2026 (fine sessione)

In ordine di numero:

1. «Esecuzione della prova visiva e scelta del modello» (task con l'utente): **in corso**, preso il 17/11/2026 e lavorato
   su più sessioni. Il repository privato `av3rgfx/prova-visiva-foto` esiste; la pagina di scatto è pubblicata su
   https://av3rgfx.github.io/DondEres/ (ramo `gh-pages`, solo la pagina) e funziona sull'iPhone. Ora tocca all'utente:
   scegliere a caso gli articoli (200 a catalogo, 40 fuori, 300 di contorno), scattare con l'iPhone e caricare gli ZIP
   nella cartella `da-caricare` del repository privato (decisioni 149–159). Quando ci sono ZIP da aprire, la sessione
   va avviata con «Lavora il ticket «Esecuzione della prova visiva e scelta del modello»» e con il repository privato
   collegato: apre gli ZIP con `prova-visiva/script/prepara.py`, poi calcola impronte e numeri con gli altri script
   (istruzioni in `prova-visiva/script/LEGGIMI.md`); prompt B. Gli script sono pronti e provati su una prova
   sintetica. Se la pagina di scatto cambia, va copiata anche sul ramo `gh-pages`, che non va cancellato.
2. «Punti di estensione per la specializzazione»: primo ticket libero della frontiera in ordine di numero (prompt A).
   Tra le cose da raccogliere: il collegamento con Ad Hoc dovrà portare gli ordini degli agenti ai piani di spedizione
   e ricevere le vendite assistite (decisione 178).
3. «Nome del prodotto»: poi «Unicità dei nomi scelti» e «Brand kit con la skill logo-design».
4. «Percorso delle schermate»: **chiuso** il 17/11/2026 (decisioni 160–179). «Aspetto grafico» ora aspetta solo il
   brand kit e lo stack; parte dal prototipo `prototipi/percorso-schermate/index.html`.

Si possono lavorare in parallelo in sessioni diverse.

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

17/11/2026, notte: chiuso «Percorso delle schermate» in quattro giri di domande, con il prototipo provato dall'utente
sul telefono. Pagina usata per le domande: https://claude.ai/artifact/BpARZrpffCDENtsKzZgTSZ (privata).
In parallelo resta in corso «Esecuzione della prova visiva e scelta del modello» (prompt B), che aspetta le foto.

## Cose dell'utente, senza sessione

- Scegliere a caso gli articoli della prova (200 a catalogo, 40 fuori, 300 di contorno) e tenere l'elenco nel
  repository privato.
- Primo giro piccolo di foto (10–20 articoli) con la pagina di scatto, poi gli ZIP in `da-caricare`.

