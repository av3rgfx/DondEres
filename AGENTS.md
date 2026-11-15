# Regole del progetto

Valgono per Claude Code e Codex. Leggere questo file a inizio lavoro.

## Progetto
- Cosa fa: gestionale di magazzino. Assegna le scorte agli ordini non ancora evasi o spediti, dal più vecchio al
  più recente, e identifica gli articoli in arrivo da barcode, codice stampato sull'etichetta o immagine.
- Per chi: prima una base valida per qualsiasi magazzino, poi una specializzazione per un magazzino specifico.
- Piattaforma: soprattutto telefono, in locale sulla rete aziendale; anche computer con telecamera integrata.
- Stack: [da definire; non sceglierlo prima di avere i requisiti]
- Decisioni dell'utente: docs/decisioni.md. Analisi: docs/analisi-progetto.md. Ricerche: docs/research/.
- Lingua delle risposte e dei documenti: italiano

## Ordine delle decisioni
1. Istruzioni dell'utente e vincoli effettivi dell'ambiente.
2. Requisiti confermati, sicurezza, integrità dei dati e accessibilità.
3. Evidenze pertinenti e convenzioni della piattaforma di destinazione.
4. Decisioni registrate nei documenti del progetto.
5. Preferenze delle skill: non trasformarle in leggi universali.

## Lavoro
- Prima di cambiare codice, leggere l'implementazione e chi la usa.
- Procedere con scelte reversibili ragionevoli; chiedere solo ciò che cambia materialmente la soluzione.
- Le domande all'utente si fanno in parole semplici: cosa si chiede, perché conta, cosa comporta ogni opzione.
- Le decisioni di gusto spettano all'utente e non si simulano.
- Non inventare utenti, interviste, statistiche o risultati di test. Distinguere fatti, deduzioni e ipotesi.
- Registrare le decisioni dell'utente con data e motivo, in un solo posto.

## Pianificazione
- wayfinder per iniziative grandi con scelte dipendenti, non per ogni modifica. Parte solo con /wayfinder.
- Ticket: Markdown locale in .scratch/<iniziativa>/ (per cambiarlo: /setup-matt-pocock-skills).
- research per le ricerche documentali, un file per tema con data e link alle fonti primarie.
- domain-modeling per glossario e ADR, solo quando servono. prototype per prototipi usa e getta.
- grilling per mettere alla prova un piano quando l'utente lo chiede.

## Semplicità (ponytail)
- Livello lite per esplorazione e prototipi, full per l'implementazione, ultra solo su richiesta.
- Riusare prima codice esistente, funzioni native e dipendenze già presenti; nuove librerie solo per un bisogno concreto.
- Non semplificare via sicurezza, validazione, permessi, gestione degli errori, accessibilità o requisiti espliciti.

## UX e design
- ux-research e ux-strategy per domande e decisioni UX; i loro valori di riferimento vanno verificati nel contesto.
- ux-writing per i testi; accessibility-audit per l'accessibilità (obiettivo WCAG 2.2 AA).
- emil-design-eng per interazioni e rifinitura; apple-design come lettura esterna, non fonte ufficiale Apple.
- mobile-native per il web su telefono; break-ui per i dati limite; review-animations per rivedere le animazioni.
- animate-ui solo se il frontend è React e lo prevede; mai per decorazione.
- Una sola direzione visiva per intervento, registrata con data e motivo.

## Verifica
- Revisione del codice con open-code-review-delegate quando il programma ocr è disponibile; altrimenti dichiararlo e
  fare una revisione diretta.
- Verificare il frontend nel browser (playwright-cli o il browser disponibile).
- ocr e playwright-cli sono installati nel progetto (package.json, versioni esatte), non a livello globale: eseguire
  `npm ci` in un ambiente nuovo, poi usarli come `npx ocr ...` e `npx playwright-cli ...` dove le skill scrivono
  `ocr` e `playwright-cli`. playwright-cli non apre file locali (file://): servire la pagina con un server locale.
  Decisione dell'utente del 15/11/2026: installarli perché le due skill funzionino come previsto.
- write-swift solo per codice Swift.
- Nessuna dichiarazione di conformità o di test superati senza verifica effettiva.

## Confini
- Niente segreti o dati reali di clienti in documenti, fixture, log o commit.
- Niente deploy, pagamenti reali, invio di messaggi o modifiche distruttive senza autorizzazione.
- Non installare programmi o skill globali automaticamente; le skill stanno in .claude/skills e .agents/skills, uguali.
