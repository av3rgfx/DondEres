# Inventario periodico

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sessione del 18/11/2026 con l'utente
Blocked by: —

## Question

Come si fa nella base la conta periodica di tutto il magazzino o di una parte (decisione 200)? Rettifica per conteggio,
correzioni ed effetto sulle assegnazioni sono già definiti nel «Modello dei dati» (74, 77).

- Conta di tutto o di una parte (per ubicazione, per articolo, a rotazione); chi la chiede, chi conta, divisione tra
  più persone.
- Conta «cieca» (senza mostrare la quantità attesa, come Odoo di serie) o con l'atteso; seconda conta sulle differenze.
- Lavoro del magazzino durante la conta: si ferma, continua, o si conta per zone.
- Documento al gestionale; in UFP come si fa oggi l'inventario con ARS (fatto da chiedere all'utente).
- Schermate: cose in sospeso (187), «Annulla» e «Conferma» (190), «Documenti» (189), tempi (195).

Si parte dalla ricerca `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 1.7).

Risultato atteso: una sezione «Inventario periodico» in `docs/architettura.md` e le schermate aggiunte al prototipo.

## Comments

- 18/11/2026, inizio: il ticket non aveva commenti. Fatti già noti: in UFP ARS fa le rilevazioni d'inventario anche
  in una versione senza rete e le scrive in Ad Hoc (ricerca `docs/research/2026-11-15-adhoc-revolution-ars-logistica.md`);
  se UFP la usi davvero va chiesto all'utente.
- 18/11/2026, primo giro (pagina https://claude.ai/artifact/QGQvc1pHzoQTsJBATiM1g5): accettate tutte le consigliate
  (229–235), con due fatti (227: in UFP inventario annuale su carta o foglio di calcolo ricopiato in Ad Hoc, ARS non si
  usa, correzioni sul momento; 228: nel magazzino Shopify lo stesso) e due note: conta cieca e seconda conta si
  cambiano nelle impostazioni del responsabile (230, 231). Domanda 28 per il rivenditore.
- 18/11/2026: prototipo aggiornato con le schermate dell'inventario e provato nel browser (conta cieca, seconda conta,
  articoli attesi non contati, «in conta da…» al prelievo, approvazione con gli ordini che perdono merce, nuovo
  inventario, configurazione). Secondo giro di 8 domande nella stessa pagina.
- 18/11/2026, secondo giro: accettate le consigliate (236–238, 240–243) tranne la 4: «tutto il magazzino» sono solo le
  ubicazioni normali (239, scelta dell'utente, motivo non indicato). Nessuna nota. Prototipo confermato (243).
- 18/11/2026: prototipo aggiornato con il secondo giro. Rileggendo la 238 è emersa un'incongruenza: la conta fuori
  dall'inventario si apre dalla scheda dell'articolo, che mostra le giacenze, quindi non è davvero cieca. Terzo giro:
  una domanda su questo e il riepilogo con le deduzioni da confermare.
- 18/11/2026, terzo giro: accettate le consigliate. «Conta un'ubicazione» in «Cerca e conta», con la schermata
  dell'inventario (244); riepilogo con le deduzioni confermato senza note (245). Prototipo aggiornato e provato nel
  browser.

## Answer

Chiuso il 18/11/2026 in tre giri, con la pagina https://claude.ai/artifact/QGQvc1pHzoQTsJBATiM1g5 (privata). Decisioni
227–245; specifica nella sezione «Inventario periodico» di `docs/architettura.md`; prototipo
`prototipi/percorso-schermate/index.html` (https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata), provato nel
browser; termini nuovi in `GLOSSARY.md`: inventario, conta cieca, seconda conta, differenza d'inventario, in conta.

- Oggi: in UFP e nel magazzino Shopify inventario di tutto una volta l'anno, su carta o foglio di calcolo, più
  correzioni sul momento (227, 228).
- Un solo lavoro «Inventario» creato dal responsabile: tutto (solo le ubicazioni normali), ubicazioni, articoli,
  fornitore; filtri «non contate da…» e «con differenze recenti»; nessuna proposta automatica (229, 239, 241).
- Conta cieca e seconda conta dalla stessa persona, di serie in Configurazione e cambiabili per un inventario; seconda
  conta accesa o spenta; domanda sugli attesi non contati (230, 231, 236, 237).
- Una persona per ubicazione, «in conta da…», lavoro che continua; confronto con la giacenza alla chiusura
  dell'ubicazione (233, 234).
- Differenze valide all'approvazione del responsabile, con gli ordini che perdono merce; rettifiche al gestionale o
  variazioni a Shopify a ogni approvazione; esportazione con sole quantità; non contate lasciate come sono e messe in un
  nuovo inventario (232, 235, 240, 242).
- «Conta un'ubicazione» fuori dall'inventario: stesse regole, vale subito, da «Cerca e conta» (77, 238, 244).
- Domanda 28 per il rivenditore.

