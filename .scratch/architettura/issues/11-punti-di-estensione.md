# Punti di estensione per la specializzazione

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sessione del 19/11/2026 con l'utente
Blocked by: 01, 02, 04

## Question

Come si specializza la base per un magazzino senza toccarne il cuore (decisione 4)? Cosa si fa con la sola
configurazione (ubicazioni sì o no, regola all'arrivo, testi) e cosa con moduli di codice (connettori ai gestionali e a
Shopify, formati di etichette dei fornitori, regole di assegnazione diverse, campi aggiuntivi, seriali e lotti)?
Come si aggiorna la base senza rompere le specializzazioni?

Risultato atteso: l'elenco dei punti di estensione e il loro contratto in `docs/architettura.md`.

## Comments

- 15/11/2026, dal ticket «Fonti degli ordini»: collegamenti previsti e loro posto (51, 67): scambio a file nella base,
  Shopify modulo con la base, Ad Hoc nella specializzazione. Il connettore traduce documenti e stati (61) e lavora con
  la coda d'uscita (54). Configurazioni nuove: modo, connettore Shopify, intervallo di scambio, solo ordini pagati.
- 16/11/2026, dal ticket «Modello dei dati»: nuove scelte per magazzino (prezzi accesi o spenti, 83; uscita automatica
  dal telefono, 80); spazio previsto per una «partita» facoltativa per seriali, lotti e scadenze (17); i campi
  aggiuntivi restano da decidere qui.
- 16/11/2026, dal ticket «Percorso di identificazione»: le parole che indicano la quantità sulle etichette (93) si
  possono ampliare con i termini dei fornitori di un magazzino; i formati di etichetta dei fornitori con regole proprie
  sono un candidato a punto di estensione.
- 18/11/2026, dal ticket «Resi» (226): proporre all'utente di far partire anche gli ordini fornitore dal programma,
  come le richieste di reso (223), dalla mail aziendale del responsabile; oggi li manda una persona (64). Anche come
  Ad Hoc riceve il documento di reso e il «reso da cliente» (domande 24 e 27).
- 19/11/2026, primo giro (pagina privata https://claude.ai/artifact/H5oSLLHmbpw3qMAXpNFEkz): accettate le consigliate,
  senza note (301–307): base unica con Configurazione e moduli; moduli solo nostri; «Da registrare nel gestionale»;
  parole in Configurazione e lettori di etichette; precedenza sostituibile; campi aggiuntivi dell'admin; aggiornamento
  fermo se un modulo non va.
- 19/11/2026, secondo giro: accettate le consigliate (308–316). Note: uscita della vendita assistita scelta dall'admin
  (308); confronto con la fattura facoltativo (310); testo della mail oltre al PDF (311); domanda su chi stampa i
  documenti in UFP (313), con risposta nel riepilogo. «Collegamento» al posto di «connettore» (316).
- 19/11/2026, riepilogo: accettate le consigliate (317–320). Nota alla 317: la scelta legata al gestionale c'è solo se il
  collegamento legge la chiusura; in UFP la merce prelevata non è più disponibile anche sul pancale dell'agente; il
  passaggio da OP a bolla al ritiro è il candidato per l'uscita, da verificare con il rivenditore (domanda 29).

## Answer

Chiuso il 19/11/2026 in due giri più il riepilogo, con la pagina https://claude.ai/artifact/H5oSLLHmbpw3qMAXpNFEkz
(privata). Decisioni 301–320; specifica nella sezione «Punti di estensione» di `docs/architettura.md`; termini nuovi in
`GLOSSARY.md` (base, specializzazione, configurazione, modulo, collegamento, punto d'aggancio, partita, lettore di
etichette, campo aggiuntivo, «Da registrare nel gestionale»); domanda 29 per il rivenditore.

- Base unica: la specializzazione è fatta di «Configurazione» e moduli, mai di una copia modificata (301); moduli solo
  nostri, accesi dall'admin in «Collegamenti» (302, 316).
- Quattro punti d'aggancio: collegamento (che dichiara cosa legge e manda; il resto va in «Da registrare nel
  gestionale»), lettore di etichette, precedenza dell'assegnazione, partita (303–305, 314). Parole di quantità, campi
  aggiuntivi, intestazione dei documenti e nomi in Configurazione; gli altri testi uguali per tutti (304, 306, 313, 315).
- Aggiornamenti: regole valide almeno un anno, prova delle specializzazioni, aggiornamento fermo se un modulo non va
  (307).
- Punti lasciati alla specializzazione: vendita assistita prelevata alla conferma ed esce quando sceglie l'admin
  (308, 317); agenti in «Ordini da assegnare» con filtro (309); confronto con la fattura facoltativo (310); «Invia al
  fornitore» con testo di serie (311, 318); inventario in una delle due forme (312); documenti con un solo autore (319);
  resi verso Ad Hoc in «Da registrare nel gestionale» finché il rivenditore non risponde (303).
