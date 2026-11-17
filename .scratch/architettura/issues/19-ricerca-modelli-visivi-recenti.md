# Modelli visivi open source recenti: ce ne sono di migliori?

Type: research
Label: wayfinder:research
Status: resolved
Blocked by: —

## Question

Prima di eseguire la prova, l'utente vuole una ricerca più approfondita sui modelli open source recenti (17/11/2026, nota
al riepilogo del «Piano della prova di accuratezza visiva»): ce ne sono di migliori di quelli scelti (decisione 140:
SigLIP 2, PE-Core, DINOv2; DINOv3 solo come confronto, 141) per riconoscere l'articolo esatto da una foto, con ricerca
per somiglianza, licenza che permetta l'uso commerciale ed esecuzione su un server in sede forse senza scheda grafica?

Risultato atteso: `docs/research/2026-11-17-modelli-visivi-recenti.md`, con data e link alle fonti primarie, senza
ripetere `docs/research/2026-11-15-modelli-visivi-riconoscimento-articoli.md`; se emerge un candidato migliore, la
proposta di aggiornare la decisione 140 da portare all'utente.

## Answer

Chiuso il 17/11/2026. Ricerca in `docs/research/2026-11-17-modelli-visivi-recenti.md`; i numeri principali (classifica
nyris e ritaglio su ILIAS) sono stati ricontrollati sulle fonti.

- Nessun modello uscito da metà 2025 a novembre 2026, con licenza commerciale, risulta migliore di SigLIP 2 e PE-Core
  sul riconoscimento di prodotti o istanze. Classifica nyris sui prodotti (R@1 medio): SigLIP 2 So400m 45,68%, DINOv3-L
  45,24%, PE-Core L 44,30%, DINOv2-L 36,93%. Niente SigLIP 3, nessun PE-Core successivo, nessun DINOv4.
- Novità con licenza commerciale ma senza risultati diretti sui prodotti: TIPSv2 di Google (Apache-2.0, aprile 2026) e
  C-RADIOv3/v4 di NVIDIA (licenza propria di NVIDIA, modificabile come quella di DINOv3).
- Modelli di embedding basati su modelli linguistici: più pesanti e peggiori sui prodotti, o non commerciali.
- Il guadagno più grande trovato è il ritaglio automatico dell'oggetto (OWLv2): su ILIAS porta DINOv3-L da 26,5 a 42,0 di
  mAP e da 55,0 a 76,0 di R@1, senza addestramento (arXiv 2610.11489). ILIAS ha scene ingombre; sulle nostre foto,
  inquadrate al centro, il guadagno può essere minore (ipotesi).
- Proposte all'utente (giro sulla pagina del «Piano della prova di accuratezza visiva»): elenco dei modelli, ritaglio,
  C-RADIO.
- Risposte dell'utente (17/11/2026): TIPSv2 media al posto di DINOv2 grande (146); si misura anche il ritaglio automatico
  (147); C-RADIO fuori (148).
