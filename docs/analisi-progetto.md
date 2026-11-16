# Analisi del progetto

Data: 15/11/2026. Stato: prima analisi, completa delle tre ricerche; precede la sessione Wayfinder sull'architettura.

Le decisioni dell'utente sono in `docs/decisioni.md`; qui non si ripetono, si usano.
Le ricerche sono in `docs/research/`. In questo documento:

- **Fatto**: detto dall'utente o documentato in una ricerca, con riferimento.
- **Deduzione**: ragionamento nostro, motivato.
- **Ipotesi**: da verificare.

## 1. Cosa deve fare il sistema

1. **Tenere il catalogo**: fino a 35.000 articoli (decisione 5). Ogni articolo ha uno o più codici, una descrizione e delle foto di riferimento.
2. **Identificare un articolo in arrivo** inquadrandolo con il telefono (decisioni 6 e 9). Prima il barcode; se manca, il codice stampato sull'etichetta; se manca anche quello, l'aspetto.
3. **Registrare l'arrivo**, cioè il movimento di carico, e collegarlo all'ordine fornitore da cui proviene.
4. **Assegnare le scorte agli ordini cliente** non ancora evasi o spediti, dal più vecchio al più recente (decisione 2).
5. **Aggiungere un articolo nuovo fotografandolo**, con codice e descrizione (decisione 8).
6. **Essere installabile in qualsiasi magazzino** e poi specializzabile per uno specifico (decisione 4).

## 2. Concetti del dominio (prima bozza)

Non è ancora il glossario: quello si fa con `domain-modeling` nella sessione Wayfinder.

| Concetto | Cosa rappresenta | Note |
|---|---|---|
| Articolo | Un tipo di prodotto a catalogo (SKU). | Fino a 35.000. |
| Codice articolo | Un codice che identifica l'articolo. | Più codici per articolo: EAN/GTIN, codice del fornitore, codice del produttore, codice interno. Lo stesso codice del fornitore può ripetersi tra fornitori diversi. |
| Numero seriale | Il codice di un singolo pezzo. | Da chiarire, vedi §6 domanda D2. |
| Foto di riferimento | Foto dell'articolo usate per riconoscerlo. | Ogni foto ha la sua impronta numerica (embedding), vedi §4. |
| Fornitore | Chi spedisce la merce. | |
| Ordine fornitore | Merce ordinata e attesa, divisa in righe. | Le righe sono quantità ordinate, ricevute e residue. |
| Ricevimento | L'evento di arrivo di una consegna. | Contiene le identificazioni fatte con il telefono. |
| Giacenza | La quantità disponibile di un articolo, eventualmente per ubicazione. | |
| Movimento | Ogni variazione di giacenza: carico, scarico, rettifica. | Fa da storico e da traccia per i controlli. |
| Ordine cliente | Merce da evadere, divisa in righe; stato: aperto, evaso, spedito. | |
| Assegnazione | Quanta giacenza è riservata a quale riga d'ordine cliente. | Si fa in ordine di data dell'ordine. |

## 3. Il percorso di identificazione

**Fatto**: l'ordine dei tentativi lo ha deciso l'utente (decisione 6): barcode → codice stampato → aspetto.

**Deduzioni** (da confermare nella sessione Wayfinder):

1. **Il barcode chiude quasi sempre la questione.** Se il codice letto è registrato su un solo articolo, l'identificazione è certa. Restano due casi: codice sconosciuto, che porta all'inserimento di un articolo nuovo (§1 punto 5), e codice registrato su più articoli, che porta alla scelta dell'operatore.
2. **Il codice stampato va letto confrontandolo con il catalogo, non preso alla lettera.** L'OCR sbaglia sui caratteri che si somigliano (0/O, 1/I/l, 5/S, 8/B). Conviene quindi cercare nel catalogo i codici più vicini a quello letto, tenendo conto di queste confusioni. Se uno solo è vicino abbastanza, è quello. È il punto che più riduce gli errori, che è l'obiettivo dichiarato dall'utente.
3. **Il contesto restringe i candidati.** Al ricevimento si sa di solito da quale fornitore arriva la merce. Gli articoli plausibili sono allora le righe aperte dei suoi ordini: decine o centinaia, non 35.000. Il riconoscimento visivo deve distinguere tra pochi candidati, il che è molto più affidabile. Vale anche per l'OCR.
4. **L'immagine propone, l'operatore conferma.** Con somiglianza medio-alta tra gli articoli (decisione 7), l'immagine da sola non basta a scalare la giacenza in automatico. Va mostrata una breve lista di candidati, con foto e codice, da confermare con un tocco. Ogni conferma salva la foto come nuovo riferimento, e il sistema migliora con l'uso.
5. **«Non lo so» è una risposta valida.** Sotto una soglia di somiglianza, il sistema lo dice e chiede il codice a mano o l'inserimento di un articolo nuovo, invece di indovinare.

## 4. Riconoscimento visivo: impostazione

Fonti di questa sezione, tutte del 15/11/2026:

- [Modelli visivi](research/2026-11-15-modelli-visivi-riconoscimento-articoli.md) (in breve: «Modelli»)
- [Progetti simili](research/2026-11-15-progetti-simili-riconoscimento-prodotti.md) (in breve: «Progetti»)
- [Addestramento ed esecuzione locale](research/2026-11-15-addestramento-ed-esecuzione-locale.md) (in breve: «Addestramento»)

Due dati sono stati ricontrollati a campione sulla fonte originale: la classifica ILIAS e la tabella 1 di Cat2Real.

**Deduzione**, valida a prescindere dal modello scelto. Con 35.000 articoli e un catalogo che cresce fotografando, un classificatore a classi fisse è inadatto: andrebbe riaddestrato a ogni articolo nuovo. Lo schema adatto è la **ricerca per somiglianza**:

1. Un modello già addestrato trasforma ogni foto in un'impronta numerica (embedding).
2. Le impronte delle foto di riferimento stanno in un indice.
3. Per riconoscere una foto si cerca l'impronta più vicina, eventualmente solo tra i candidati del contesto (§3 punto 3).
4. Aggiungere un articolo vuol dire aggiungere impronte, non riaddestrare.

Un adattamento leggero del modello sulle foto del magazzino resta possibile più avanti, se i dati reali lo giustificano.

### 4.1 Cosa dicono le ricerche (fatti)

- **I progetti esistenti seguono questo schema.** Chi aggiunge articoli senza riaddestrare ritaglia l'oggetto, ne calcola l'impronta e cerca la più vicina: PaddleClas PP-ShiTu (Apache-2.0), i progetti di NVIDIA e Seeed, i riferimenti di ARMBench («Progetti» §1, §3). Nessun progetto unisce gestionale, assegnazione e riconoscimento da telefono in locale («Progetti», sintesi).
- **Si può partire senza addestrare, ma su articoli simili non basta.**
  - Nello studio più vicino al nostro caso (Cat2Real, 2026: 1.865 prodotti, foto reali contro immagini di catalogo), DINOv3 non adattato indica come primo candidato l'articolo giusto nel 54% dei casi; lo mette tra i primi 5 nel 78%.
  - Dopo un adattamento per confronto tra foto (metric learning) si sale all'81% e al 95%. Sui prodotti esclusi dall'addestramento si perde solo mezzo punto («Addestramento» §A–B).
  - Seeed, con DINOv2-small, passa dal 51% di risposte giuste con 1 foto per articolo al 79% con 8 foto («Progetti» §1).
- **Amazon (ARMBench) confronta l'oggetto solo con quelli attesi, non con tutto il catalogo.** Gli autori scrivono che per una precisione alta servono anche testo e dimensioni («Progetti» §3–4). È la stessa idea di §3 punti 2–3.
- **Classifica ILIAS** (riconoscimento di oggetti specifici, modelli non adattati): DINOv3-L 26,5; DINOv3-B e PE-L 22,0; SigLIP2-L 20,8; DINOv2-L 15,3; i CLIP sotto 10 («Modelli» §1). È un compito diverso dal nostro: indica quali famiglie provare per prime, non quale vincerà.
- **Le licenze decidono quanto i risultati.**
  - Uso commerciale libero (Apache-2.0): SigLIP 2, PE-Core, DINOv2.
  - Licenza propria, da far leggere a chi decide per l'azienda: DINOv3.
  - Esclusi perché non commerciali: MobileCLIP/MobileCLIP2, FastVLM, i pesi ImageNet di ConvNeXt V2, DEIMv2.
  - Obbligo di pubblicare il codice: Ultralytics YOLO (AGPL-3.0, oppure licenza a pagamento) e YOLO-World (GPL-3.0).

  Fonti: «Modelli» §1–3, «Addestramento» §D.
- **L'indice è piccolo.** 35.000 articoli × 5–10 foto fanno da 175.000 a 350.000 impronte, circa 0,3–1 GB. La ricerca esatta basta, senza indice approssimato (FAISS MIT, pgvector) («Addestramento» §E).
- **Barcode e OCR sul telefono sono maturi e locali.** Su Android si usa ML Kit, su iOS Apple Vision/VisionKit.
  - Nel browser, `BarcodeDetector` funziona su Chrome per Android ma non su iPhone; il ripiego è zxing-cpp in WebAssembly.
  - Sul server: PaddleOCR (PP-OCRv6, Apache-2.0) («Modelli» §6, «Addestramento» §G).
- **Fotocamera da web app.** Serve HTTPS anche sulla rete interna. Nelle web app installate su iPhone c'è un difetto noto, ancora aperto, sul permesso della fotocamera («Addestramento» §H).
- **Formato dei modelli.** ONNX Runtime (MIT) copre server, browser e telefono. NNAPI è deprecato da Android 15 («Addestramento» §F).
- **Mancano dati per il nostro caso.** Non esistono dati pubblici su scatole di magazzino quasi identiche fotografate da telefono, né sul conteggio dei pezzi da telefono («Progetti» e «Modelli», «Cosa resta incerto»).

### 4.2 Proposta (deduzione, da confermare nella sessione Wayfinder)

1. **Sul telefono: barcode e OCR del codice**, con le librerie native. Il codice letto si confronta con il catalogo come in §3 punto 2.
2. **Su un server in sede: riconoscimento visivo e indice.**
   - L'indice dei 35.000 articoli sta in un solo posto e si aggiorna appena si aggiunge un articolo.
   - Il modello si cambia senza aggiornare le app.
   - Un modello sul telefono serve solo se si deve lavorare senza rete (domanda D6).
3. **Modelli da mettere a confronto**: SigLIP 2 e PE-Core (Apache-2.0); DINOv3 solo se l'azienda ne accetta la licenza; DINOv2 come termine di paragone.
4. **Risposta all'operatore**: da 3 a 5 proposte con foto e codice, la soglia del «non so», e le conferme che arricchiscono l'archivio delle foto.
5. **Inserimento di un articolo nuovo**:
   - si scattano più foto da angolazioni e luci diverse;
   - il codice si legge con barcode o OCR;
   - un modello che legge immagini e scrive testo (VLM), eseguito sul server, può proporre la descrizione dall'etichetta;
   - l'operatore conferma.

   Si conservano sempre le foto originali: se cambia il modello, tutte le impronte vanno ricalcolate.
6. **Prima di scegliere il modello, una prova con foto reali**, come proposto nelle ricerche:
   - da 200 a 500 articoli, scegliendo di proposito i gruppi più simili;
   - poche foto di catalogo per articolo, più foto «di arrivo» scattate da telefoni diversi;
   - si misura quante volte l'articolo giusto è il primo, quante volte è tra i primi 5, e i tempi.

   L'adattamento del modello (metric learning) si fa solo se i numeri lo giustificano.

## 5. Base generica e specializzazione

**Deduzione**: perché la base sia installabile ovunque (decisione 4), deve contenere la logica comune a ogni magazzino e lasciare fuori ciò che cambia da un magazzino all'altro.

- **Nella base**: catalogo, codici, identificazione, ricevimento, giacenza, movimenti, ordini, assegnazione, utenti e permessi, storico.
- **Nella specializzazione**: collegamento al gestionale o ERP già in uso (importare ordini, esportare movimenti), formati di codici ed etichette dei fornitori, regole di assegnazione diverse, ubicazioni, campi aggiuntivi, testi.
- **Come**: configurazione per le differenze semplici, punti di estensione (moduli o plugin) per quelle che richiedono codice. Si sceglie nella sessione Wayfinder.

## 6. Domande aperte per l'utente

Sono le domande che cambiano materialmente la soluzione. Risposte del 15/11/2026: decisioni 15–28 in `docs/decisioni.md`. D5 è stata chiusa nella mappa `.scratch/architettura/map.md` il 16/11/2026: web app servita dal server in sede (decisioni 119–127).

- **D1. Regola all'arrivo.** La frase ricevuta è: «Se il magazzino ha disponibilità, la quantità viene scalata; altrimenti l'articolo arrivato viene associato all'ultimo ordine effettuato su quel fornitore e scalato direttamente dall'ordine». Non è chiaro cosa si scali quando la merce *arriva*, perché l'arrivo di solito aumenta la giacenza. Ci sono anche due possibili contraddizioni:
  - gli ordini cliente si servono dal più vecchio, ma l'ordine fornitore scelto è «l'ultimo»;
  - non è chiaro se «ordine» indichi l'ordine al fornitore o quello del cliente.

  Serve un esempio concreto con numeri.
- **D2. «Numero seriale».** È un codice che identifica il *tipo* di articolo (codice articolo del produttore o del fornitore)? Oppure identifica il *singolo pezzo*, e allora va anche registrato pezzo per pezzo (tracciabilità per seriale)?
- **D3. 35.000.** Sono 35.000 articoli diversi a catalogo, oppure 35.000 pezzi in giacenza?
- **D4. Fonte degli ordini.** Il sistema è il gestionale principale, cioè gli ordini nascono qui? Oppure si affianca a un gestionale o ERP esistente da cui importa ordini e a cui restituisce i movimenti? È la domanda che più incide sulla base generica.
- **D5. App sul telefono.** App installata (nativa o multipiattaforma) o applicazione web aperta dal browser? Il web è più semplice da distribuire. Però dal browser la fotocamera richiede una connessione HTTPS anche sulla rete interna, e su iOS ci sono limiti. Dipende anche da quali telefoni ha il magazzino: aziendali o personali, Android o iPhone.
- **D6. Rete assente.** Se il telefono perde la rete aziendale, il lavoro si ferma o deve continuare e sincronizzarsi dopo?
- **D7. Conferma dell'operatore.** Si accetta di confermare con un tocco quando il riconoscimento è solo visivo (§3 punto 4), o l'obiettivo è lo scarico senza nessun tocco?
- **D8. Quantità.** Si inquadra un pezzo alla volta, o anche un collo con più pezzi da contare? Contare pezzi dall'immagine è un problema diverso e più difficile.

## 7. Rischi principali

| Rischio | Perché | Mitigazione proposta |
|---|---|---|
| Articoli quasi identici scambiati | Somiglianza medio-alta (decisione 7). | Codice prima dell'immagine; candidati ristretti dal contesto; conferma dell'operatore. |
| Movimento sbagliato registrato in automatico | L'errore si propaga a giacenze e assegnazioni. | Ogni movimento annullabile e tracciato; conferma sotto soglia. |
| Foto di riferimento scarse o di cattiva qualità | Il riconoscimento dipende da come sono state scattate. | Guida alla ripresa nell'app; più foto per articolo; nuove foto dalle conferme. |
| Licenze dei modelli | Alcuni modelli non permettono l'uso commerciale o impongono AGPL. | Elenco in §4.1. Le licenze di DINOv3 e SAM e i termini di ML Kit vanno letti da chi decide per l'azienda: le ricerche ne riassumono il testo, non sono un parere legale. |
| Accuratezza visiva insufficiente | Nessun dato pubblico sul nostro caso; i modelli non adattati sbagliano spesso il primo candidato su articoli simili. | Codice prima dell'immagine; candidati ristretti; prova reale prima di scegliere (§4.2 punto 6). |
| Base troppo legata al primo magazzino | Il primo cliente detta i dettagli. | Separazione esplicita in §5; la specializzazione si fa dopo la base (decisione 4). |
