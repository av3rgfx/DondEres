# Lettura automatica delle bolle

Type: research
Label: wayfinder:research
Status: resolved
Blocked by: —

## Question

Si possono leggere in automatico tutti i dati di una bolla di consegna (DDT del fornitore), righe e quantità comprese,
in sede e senza servizi cloud (decisione 193)?

- Da foto del telefono: ritaglio automatico del foglio, raddrizzamento, contrasto «da scansione»; con quali strumenti
  open source e con quale licenza.
- Da PDF digitale caricato (quando l'ufficio ha la versione digitale): testo già presente o da riconoscere.
- Lettura di testata (fornitore, numero, data, ordine citato) e righe (codice, descrizione, quantità, unità): modelli e
  programmi che girano in sede (per esempio PaddleOCR e PP-StructureV3, già nella ricerca del 18/11/2026; modelli che
  leggono immagini e scrivono testo), con e senza scheda grafica.
- Se conviene addestrare o adattare un modello su molte bolle, oppure uno script per fornitore con le regole del suo
  modulo; quante bolle servono.
- Come si misura l'affidabilità: una prova su bolle vere di UFP (con i dati dei clienti coperti), simile alla prova
  visiva.

Non ripetere `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 2). Le quantità lette restano «quantità in
bolla», mai quantità contate (183, 192).

Risultato atteso: `docs/research/<data>-lettura-automatica-bolle.md`, con data e link alle fonti primarie, e la
proposta di una prova su bolle vere da portare all'utente.

## Comments

- 18/11/2026, inizio: il ticket non aveva commenti. Ricerca affidata a un sotto-agente con la skill research; file
  `docs/research/2026-11-18-lettura-automatica-bolle.md`.
- 18/11/2026: l'utente ha mostrato in chat 10 foto di bolle vere di UFP (AGB/Alban Giacomo, ISEO Serrature, SAIT
  Abrasivi, più una lettera di vettura SUSA). Le foto non entrano nel repository; i fatti sono nella sezione «Cosa
  mostrano le bolle vere di UFP» della ricerca, senza riferimenti dei clienti. Prova dell'agente con zxing-cpp 3.1.1
  sulle foto: DataMatrix di AGB con numero e data del DDT (letto su 3 pagine su 4), barcode di riga di ISEO (8 su 9).
- 18/11/2026: domande sulla prova (dove conservare le bolle, cosa coprire, quante, quali sistemi, traguardi) nel primo
  giro della pagina privata https://claude.ai/artifact/KQtNpyrXjbywxnz1iGKnGY, insieme al primo giro di «Resi».
- 18/11/2026, primo giro: accettate tutte le consigliate sulla prova (decisioni 202–206), con due note: valutare
  modelli sul telefono o sul palmare (Zebra in UFP) per non caricare il server; il magazzino Shopify ha solo un PC fisso
  che può fare da server; l'importante è rendere veloce il carico dei DDT in Ad Hoc, senza passaggi ripetuti. Dove gira
  la lettura: domanda nel secondo giro della stessa pagina.

## Answer

Ricerca del 18/11/2026: `docs/research/2026-11-18-lettura-automatica-bolle.md`. In parte sì, a condizioni: testata
(numero, data, ordine citato) leggibile in sede con strumenti a licenza commerciale; righe leggibili da modelli recenti
in sede, ma l'affidabilità sulle bolle italiane è da misurare; finché non è provata vale la 192. Codici stampati
(DataMatrix di AGB, barcode di riga di ISEO) letti dalle foto con zxing-cpp. Esclusi per licenza LayoutLMv3, DocTr,
Qwen2.5-VL-3B e derivati, Marker/Surya, HunyuanOCR; PyMuPDF (AGPL) e Poppler (GPL) da evitare. Proposta di prova
accettata (202–206); sezione «Lettura automatica delle bolle» in `docs/architettura.md`. Nuovo ticket:
[Esecuzione della prova di lettura delle bolle](25-esecuzione-prova-lettura-bolle.md).
