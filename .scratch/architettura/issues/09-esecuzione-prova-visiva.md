# Esecuzione della prova visiva e scelta del modello

Type: task
Label: wayfinder:task
Status: open
Assignee: in corso con l'utente, su più sessioni (iniziato il 17/11/2026)
Blocked by: 08, 19

## Question

Eseguire la prova secondo il piano: l'utente fornisce le foto reali, l'agente prepara gli script, calcola le
impronte con i modelli scelti, misura e riporta i risultati senza abbellirli. L'utente sceglie il modello in base ai
numeri.

Tipo: task con l'utente (le foto le scatta l'utente). Risultato atteso: i numeri e il modello scelto in
`docs/architettura.md`, la scelta in `docs/decisioni.md`, la posizione delle foto e degli script annotata qui.

## Comments

- 17/11/2026, dal ticket «Piano della prova di accuratezza visiva»: il piano e la lista delle foto sono nella sezione
  «Prova di accuratezza visiva» di `docs/architettura.md` (decisioni 128–145). L'utente crea il repository privato delle
  foto e lo aggiunge alla sessione (128, 145); l'agente prepara la pagina di scatto (dal browser, su un indirizzo sicuro,
  per esempio GitHub Pages) e la fa provare prima su un telefono (136); se l'utente vuole DINOv3, serve la sua chiave di
  Hugging Face, da chiedere con il modulo sicuro, mai in chat (141). I tempi si misurano solo nella sessione (143).
  Prima di iniziare va chiuso il ticket di ricerca «Modelli visivi open source recenti: ce ne sono di migliori?», che
  può cambiare l'elenco dei modelli (140).
- 17/11/2026, dal ticket di ricerca «Modelli visivi open source recenti: ce ne sono di migliori?»: modelli della prova
  SigLIP 2 e PE-Core media e grande, DINOv2 media, TIPSv2 media, DINOv3 solo confronto (141, 146); ogni modello anche con
  il ritaglio automatico della scatola, OWLv2 (147); C-RADIO fuori (148). Il ticket è sbloccato: per partire serve il
  repository privato delle foto creato dall'utente.
- 17/11/2026, prima sessione di esecuzione: repository privato `av3rgfx/prova-visiva-foto` creato dall'utente e
  collegato; contiene README, la cartella `da-caricare` per gli ZIP e la cartella `esempi` con quattro foto d'esempio
  di etichette (fuori dalla prova). Pagina di scatto in `prova-visiva/pagina-scatto/index.html`, pubblicata dal ramo
  `gh-pages` su https://av3rgfx.github.io/DondEres/ (versione 3), provata dall'utente sull'iPhone. Decisioni
  149–158: per ora solo iPhone con 3 foto di arrivo per articolo, palmare e Android dopo (155); all'arrivo l'articolo
  si sceglie dall'elenco (156). Prossimo passo: l'utente sceglie a caso gli articoli (200 a catalogo, 40 fuori, 300 di
  contorno), scatta e carica gli ZIP; poi una sessione li apre, assegna le sigle anonime e prepara gli script.
  Domande pagine: https://claude.ai/artifact/52C1DcnRuhw8SBov9wvJnd (privata).
- 17/11/2026, seconda sessione di esecuzione: script del calcolo in `prova-visiva/script/` (prepara, impronte,
  valuta, etichette, più `prova_sintetica.py`), con versioni esatte in `requirements.txt` e istruzioni in
  `LEGGIMI.md`. Provati da capo a fondo su una prova sintetica ricavata dalle quattro foto d'esempio, fuori dai
  repository: tutti e sei i modelli e OWLv2 si scaricano da Hugging Face e girano su CPU; PaddleOCR gira con
  oneDNN spento e il testo cercato a 1.280 pixel. Due punti sulle soglie (145) da decidere con i primi numeri veri:
  sezione «Script del calcolo» di `docs/architettura.md`.

