# Percorso di identificazione e lettura della quantità

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: —

## Question

Come procede passo per passo l'identificazione barcode → codice stampato → immagine (decisioni 6 e 24), e come si
legge la quantità scritta sulla scatola (decisione 25)?

- Confronto del codice stampato con il catalogo, tenendo conto dei caratteri che si confondono (analisi §3 punto 2):
  quando una corrispondenza è unica?
- Restringere i candidati con il contesto (fornitore, ordini fornitore aperti): sempre, o solo quando c'è?
- Barcode registrato su più articoli, o sconosciuto: cosa vede l'operatore?
- Quantità sulla scatola: quali scritte si cercano, come si distinguono da altri numeri, come si propone il valore?
- Ogni conferma salva la foto come nuovo riferimento: sempre, o con qualche filtro?

Le soglie numeriche (quando dire «non lo so») si fissano dopo la prova: qui si decide il percorso.
Risultato atteso: il percorso di identificazione in `docs/architettura.md`.

## Answer

Risolto il 16/11/2026 in due giri, con la pagina https://claude.ai/artifact/TfFoX5VKMN38WPPUQjdRvS (privata). Tutte le
risposte sono le proposte consigliate; riepilogo e deduzioni confermati.

- Decisioni 87–104 in `docs/decisioni.md`: un'inquadratura sola (87); prima gli articoli attesi, poi il catalogo con
  avviso (88); confronto del codice stampato con i segni che si confondono, e un carattere diverso solo con un unico
  candidato tra gli attesi (89); scheda unica «È questo» (90); barcode su più articoli (91) e sconosciuto, collegato da
  confermare (92); quali scritte sono la quantità (93), chili e metri (101), barcode unico registrato con la quantità
  letta (99); più colli (94); valore di partenza (95) e contenuto del collo ricordato (100); foto di riferimento con
  filtri e tetto (96); stesso percorso in ogni momento, controllo al prelievo (97, 103); più codici nell'inquadratura
  (102); uscite del «non lo so» (98); riepilogo e deduzioni (104).
- Specifica: sezione «Percorso di identificazione e lettura della quantità» in `docs/architettura.md`; nel «Modello dei
  dati» aggiornate foto di riferimento e scansione, aggiunto il contenuto del collo.
- Glossario: identificazione, articoli attesi, «non lo so», collo, contenuto del collo.
- Da fissare con la prova visiva: soglie di «convincente» e «non lo so», tetto di foto per articolo, qualità di lettura
  di codice stampato e quantità (commento nel ticket «Piano della prova di accuratezza visiva»).
