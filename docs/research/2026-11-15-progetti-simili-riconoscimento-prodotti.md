# Progetti simili: riconoscimento di articoli e gestionali di magazzino

Data: 15/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina aperta il 15/11/2026). **DEDUZIONE** = conclusione
nostra a partire dai fatti. **IPOTESI** = da verificare. "L'azienda dichiara" = affermazione del produttore, non
verificata da terzi. "Non verificato" = viene dalla memoria, senza fonte aperta.

## Domanda

Esistono progetti simili al nostro (open source, commerciali, accademici)? Come sono fatti, quali soluzioni usano,
che lezioni ne ricaviamo? Il nostro caso: gestionale di magazzino con nucleo generico; assegnazione delle scorte agli
ordini cliente dal più vecchio; al ricevimento l'operatore inquadra la scatola col telefono, tutto in rete locale;
identificazione con barcode, poi codice stampato (OCR), poi riconoscimento visivo; fino a 35.000 articoli molto
simili tra loro; articolo nuovo aggiunto con una foto, senza riaddestrare.

## Sintesi

- Non abbiamo trovato nessun progetto, aperto o commerciale, che unisca tutto: gestionale + allocazione + barcode/OCR +
  riconoscimento visivo da telefono, in locale. I pezzi esistono, separati.
- Per il riconoscimento con catalogo che cresce senza riaddestrare, lo schema ricorrente è sempre lo stesso:
  ritaglio dell'oggetto, "impronta" numerica (embedding) dell'immagine, ricerca della più vicina in un indice di foto
  di riferimento (PaddleClas PP-ShiTu, NVIDIA, Seeed Studio, i baseline di Amazon ARMBench).
- Con articoli quasi identici i modelli generici rendono poco: su minuteria industriale (fermagli e connettori) il
  primo risultato è giusto nel 10-26% dei casi con DINOv2/DINOv3/SigLIP2; anche il modello specializzato di nyris si
  ferma al 63%. Fra i primi 5 risultati invece la risposta giusta c'è molto più spesso.
- Amazon (ARMBench) restringe il confronto ai soli oggetti attesi nel contenitore e misura la confidenza col distacco
  fra primo e secondo candidato; dichiara che per alta precisione servono altre informazioni (testo, dimensioni).
- I gestionali open source (InvenTree, Odoo, ERPNext) gestiscono bene ricevimento, prenotazione e allocazione, e hanno
  un sistema di plugin/moduli; nessuno offre riconoscimento visivo degli articoli. Il criterio "ordine più vecchio
  prima" non è il comportamento predefinito di InvenTree; in Odoo è vicino a quello del pianificatore.
- Molti dataset del settore vietano l'uso commerciale (RPC, SKU-110K, MVTec D2S, Products-10K): vanno bene per
  provare, non per addestrare un prodotto.

## 1. Open source: riconoscimento di prodotti e articoli

Ricerca fatta con l'API di ricerca di GitHub (argomenti `product-recognition`, parole chiave "product recognition",
"sku recognition", "few-shot product recognition", "fastener recognition", "inventory computer vision"). Risultato:
pochissimi progetti seri; la maggior parte sono esercizi o tesi con 0-5 stelle. Su "fastener recognition" e
"inventory computer vision" nulla di serio (solo repository personali con 0-1 stelle, classificatori YOLO chiusi).

### PaddleClas PP-ShiTu (Baidu) — il più completo e maturo
- FATTO: tre moduli: rilevamento del soggetto principale (PicoDet-LCNet_x2_5), estrazione del vettore di
  caratteristiche (PPLCNetV2_base), ricerca vettoriale con la libreria Faiss. Modelli totali 49 MB; Recall@1 73,8%
  (V2) contro 66,8% (V1) sul loro insieme di prova, misurato su CPU Intel.
  [PPShiTuV2_introduction](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.6/docs/en/PPShiTu/PPShiTuV2_introduction.md)
- FATTO: aggiungere una categoria "non richiede di riaddestrare il modello": si mettono le foto nella cartella
  "galleria", si aggiorna un file di testo (percorso, TAB, etichetta) e si ricostruisce l'indice. Se si cambia il
  modello di estrazione, l'indice va ricostruito. Nella demo Android si aggiunge un oggetto con una foto e un nome e
  si salva l'indice. I risultati portano un punteggio di somiglianza (`rec_scores`), ma la guida non indica una soglia.
  [quick start recognition](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.6/docs/en/quick_start/quick_start_recognition_en.md)
- FATTO: licenza Apache-2.0, circa 5.860 stelle, ultimo push 12/11/2026 (API di ricerca GitHub, campo `pushed_at`).
  Scenari citati: prodotti, loghi, veicoli. Dipende dal framework PaddlePaddle.
- Foto per articolo: non indicate.

### NVIDIA Few-Shot Product Recognition (Metropolis, versione alfa)
- FATTO: app di riferimento per casse self-service. Un rilevatore trova gli oggetti senza classificarli; un secondo
  modello produce un vettore di 2048 numeri per oggetto; un servizio confronta il vettore con un database di articoli
  etichettati; il risultato è il barcode dell'articolo più vicino. Se il barcode letto dallo scanner non coincide,
  parte un avviso; l'oggetto non riconosciuto diventa "unknown" e un utente può aggiungere immagine e barcode al
  database. Un valutatore classifica le predizioni in corrette, sbagliate (sotto soglia) o "unseen".
  [NVIDIA docs](https://docs.nvidia.com/mms/text/Smart_self_checkout_Overview.html)
- FATTO: stato alfa, "da reimplementare", fornita così com'è e senza supporto. Modelli distribuiti su NGC, non come
  codice aperto. Foto per articolo e valore della soglia: non indicati.

### Seeed Studio, Edge Product Recognition — il più vicino al nostro flusso, ma codice non pubblicato
- FATTO (l'azienda dichiara): rilevatore YOLOX-Tiny a classe unica + DINOv2 small/base riaddestrato con ArcFace su
  immagini e-commerce; vettore da 512; ricerca FAISS per somiglianza coseno su una galleria con versioni immutabili.
  "L'identità dello SKU vive solo nella ricerca, non nei pesi del modello."
  [Seeed wiki](https://wiki.seeedstudio.com/solutions/edge-product-recognition/)
- FATTO: nuovo SKU con 3-8 foto (fronte, retro, lato, due condizioni di luce); meno di 3 vengono rifiutate. Su
  Grocery Store Dataset, DINOv2-small: 51,11% al primo colpo con 1 foto per SKU, 79,11% con 8.
- FATTO: ogni rilevamento restituisce `similarity`, `top2_margin` (distacco dal secondo), un blocco `ocr` e un flag
  `fallback`; la pagina dice che il riordino con OCR e il ripiego su un modello visivo-linguistico (VLM) "non sono
  implementati". Chiede di salvare con ogni risultato versione e hash della galleria e dei modelli, perché vettori di
  modelli diversi non sono confrontabili. Conteggio dei pezzi "non ancora misurato".
- FATTO: codice del progetto Apache-2.0 ma repository non pubblicato; i pesi hanno restrizioni non commerciali o
  solo accademiche. Pagina aggiornata il 07/09/2026.

### Altri, minori
- `kouroshkarimi/visual_product_recognition_using_DINOv2`: DINOv2 + FAISS + verifica geometrica dei primi candidati
  con un matcher di punti (GIM). Aggiornamento incrementale dell'indice indicato come lavoro futuro. MIT, 3 stelle.
  [repo](https://github.com/kouroshkarimi/visual_product_recognition_using_DINOv2)
- `thomas-yanxin/ColugoMum`: piattaforma di cassa basata su PaddleClas, LGPL-2.1, ferma al 21/12/2022 (API GitHub).
- RetailKLIP (articolo, 2023): riaddestra l'encoder visivo di OpenCLIP con metric learning su una sola GPU, così che
  il "vicino più prossimo" funzioni per prodotti nuovi senza addestramento incrementale.
  [arXiv 2312.10282](https://arxiv.org/abs/2312.10282). Il link al codice non compare nella pagina arXiv.

DEDUZIONE: fra gli open source, PP-ShiTu è l'unico pronto, mantenuto e con licenza commerciale libera; Seeed è
istruttivo come progetto (soglie, galleria versionata, numero di foto) ma non usabile come codice.

## 2. Gestionali e ERP open source

| Sistema | Barcode / visione oggi | Ricevimento e ordini fornitore | Allocazione agli ordini cliente | Nucleo e personalizzazioni |
|---|---|---|---|---|
| InvenTree | Barcode interni, esterni e personalizzati collegati a parti, giacenze, ubicazioni, ordini; scansione da webcam nel web e da fotocamera nell'app mobile. Nessun riconoscimento visivo. [barcode](https://docs.inventree.org/en/latest/barcodes/) | Ogni riga ricevuta diventa una giacenza; ubicazione di riga prevale su quella dell'ordine; numeri di serie opzionali. [purchase order](https://docs.inventree.org/en/latest/purchasing/purchase_order/) | Manuale o automatica (task in background), raggruppata in spedizioni; "Stock Priority" predefinita FIFO sulle giacenze (quale lotto consumare), non sull'età dell'ordine. [sales order](https://docs.inventree.org/en/latest/sales/sales_order/) | Plugin "disaccoppiati dal codice di InvenTree", installabili da PyPI; il comportamento dei barcode si estende con plugin. [plugin](https://docs.inventree.org/en/latest/plugins/) |
| Odoo 19 | App Barcode (non verificato in dettaglio). | Ricevimenti come trasferimenti di magazzino (non verificato). | Metodi di prenotazione: alla conferma, manuale, prima della data prevista. [doc](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/shipping_receiving/reservation_methods.html). Il pianificatore assegna i movimenti in ordine `reservation_date, priority desc, date asc, id asc`. [stock_rule.py](https://github.com/odoo/odoo/blob/19.0/addons/stock/models/stock_rule.py) | Moduli che ereditano modelli e viste (il tutorial ufficiale ha i capitoli "Model Inheritance" e "View Inheritance"). [tutorial](https://www.odoo.com/documentation/19.0/developer/tutorials/server_framework_101/12_inheritance.html) |
| ERPNext v15+ | Non approfondito. | Ricevuta d'acquisto (Purchase Receipt). | "Stock Reservation Entry" contro righe dell'ordine cliente o pick list; opzione di prenotazione automatica alla ricevuta d'acquisto. Nessuna regola di priorità documentata. [doc](https://docs.frappe.io/erpnext/user/manual/en/stock-reservation) | App Frappe (non verificato). |
| Grocy | Scansione da fotocamera nel browser con ZXing, solo su HTTPS; plugin di ricerca barcode esterna (Open Food Facts predefinito). MIT. [repo](https://github.com/grocy/grocy) | Non approfondito. | Non pertinente (dispensa domestica). | Plugin per la ricerca barcode. |
| Part-DB | Ubicazioni di magazzino documentate; scanner barcode e "information provider" esistono come pagine ma non li ho aperti. [doc](https://docs.part-db.de/usage/getting_started.html) | Non documentato nella pagina aperta. | Non documentato. | — |
| Snipe-IT, OpenBoxes | Non aperti per limiti di tempo. Snipe-IT è gestione di beni aziendali, non di scorte (non verificato). | — | — | — |

DEDUZIONI:
- Nessun gestionale open source maturo offre riconoscimento visivo degli articoli: va costruito come modulo a parte.
- L'aggancio naturale è il punto "scansione" che già esiste (InvenTree: plugin barcode; Grocy: plugin di ricerca):
  il riconoscimento visivo può presentarsi al gestionale come un altro modo di produrre "un codice articolo candidato".
- La regola "ordine più vecchio prima" va scritta esplicitamente: in InvenTree la priorità FIFO riguarda le giacenze,
  non gli ordini; in Odoo l'ordinamento del pianificatore considera prima data di prenotazione e priorità, poi la data.
- Tutti separano prenotazione/allocazione (impegno della merce) da prelievo e spedizione: utile anche per noi.

## 3. Prodotti commerciali (dichiarazioni delle aziende)

### Casse e bilance con riconoscimento visivo
- Mashgin. L'azienda dichiara: più telecamere 3D che costruiscono un modello 3D di ogni oggetto in tempo reale;
  accuratezza "oltre il 99,99%"; "bastano pochi secondi per insegnare a Mashgin nuovi articoli"; nessun barcode;
  addestrato su oltre 1,5 miliardi di transazioni. [mashgin.com](https://www.mashgin.com/)
- Tiliter. L'azienda dichiara: riconoscimento prodotti in "1.000+" sedi e "50M+" immagini l'anno; uso dei telefoni o
  delle telecamere già presenti; risposte "con un punteggio di confidenza". Nessun dettaglio tecnico sulla pagina.
  [tiliter.com](https://www.tiliter.com/)
- Diebold Nixdorf Vynamic Smart Vision. La pagina ufficiale che ho provato risponde 404. Da stampa di settore (fonte
  secondaria): telecamera accanto alla bilancia per frutta e verdura; addestrato su centinaia di prodotti; il
  personale aggiunge nuovi articoli; tecnologia SeeWare di SeeChange.
  [biometricupdate.com](https://www.biometricupdate.com/202506/diebold-nixdorf-integrates-yoti-age-checks-with-produce-recognition-for-self-checkouts)
- DEDUZIONE: questi sistemi lavorano con hardware fisso, luce e sfondo controllati e cataloghi relativamente piccoli
  (frutta e verdura, menu di mensa). Le loro percentuali non si trasferiscono a un telefono tenuto in mano.

### Lettura di barcode ed etichette su telefono
- Scandit Smart Label Capture. L'azienda dichiara: con una pressione legge più barcode e testo stampato (numeri di
  serie, pesi, scadenze, lotti, IMEI, VIN), su Android, iOS e web, tramite un "AI Engine". Non dice se l'elaborazione
  è sul dispositivo. [scandit.com](https://www.scandit.com/products/smart-label-capture/)
- Google ML Kit Text Recognition v2. FATTO: Android e iOS; latino, cinese, devanagari, giapponese, coreano; restituisce
  blocchi, righe, parole, simboli con riquadri e punteggi di confidenza.
  [doc](https://developers.google.com/ml-kit/vision/text-recognition/v2). FATTO: modello sul dispositivo, incluso
  nell'app (~4 MB per script e architettura) o scaricato da Google Play services (~260 KB); ogni carattere deve
  essere almeno 16x16 pixel, oltre 24x24 non migliora. [Android](https://developers.google.com/ml-kit/vision/text-recognition/v2/android)
- Zebra DataWedge / OCR Wedge. FATTO: sui terminali Zebra Android, configurazioni OCR a licenza (targhe, documenti,
  VIN, TIN, contatori), OCR "free-form" che restituisce parole raggruppate per riga e blocco, e "Picklist + OCR" per
  barcode o testo nello stesso flusso. [techdocs](https://techdocs.zebra.com/datawedge/14-0/guide/programmers-guides/workflow-input)
- Anyline. FATTO: SDK per pneumatici (DOT), VIN, contatori, targhe, barcode, documenti; nessun prodotto dedicato ai
  numeri di serie nella pagina; nessuna dichiarazione sull'uso offline. [anyline.com](https://anyline.com/products/)
- PaddleOCR (open source, citato qui per confronto). FATTO: Apache-2.0; versione 3.7.0 dell'11/06/2026 con PP-OCRv6
  in tre taglie (1,5M / 7,7M / 34,5M parametri) per edge, mobile, server; esportazione ONNX/OpenVINO/TensorRT e SDK
  per browser. [repo](https://github.com/PaddlePaddle/PaddleOCR)

### Ricerca visiva di ricambi su grandi cataloghi
- nyris. L'azienda dichiara: si fotografa un ricambio e lo si trova in secondi; pipeline di immagini sintetiche da CAD
  "99% più veloce e 90% più economica" della fotografia. [nyris.io](https://www.nyris.io/)
- nyris ha pubblicato un banco di prova (autore dipendente nyris, quindi parte in causa). FATTO, dall'articolo:
  [arXiv 2603.17186](https://arxiv.org/html/2603.17186), marzo 2026. Ricerca immagine-immagine; galleria indicizzata
  foto per foto, prodotto scalare esatto su vettori normalizzati. Recall@1 (%) scelti:

  | Modello | Fermagli e connettori (12.531 prodotti, gallerie da render CAD) | Automotive | Products-10K | Stanford Online Products |
  |---|---|---|---|---|
  | DINOv2-L | 13,7 | 19,3 | 50,2 | 56,3 |
  | DINOv3 ViT-L/16 | 26,4 | 26,3 | 59,2 | 66,6 |
  | SigLIP2 SO400M | 10,6 | 22,0 | 66,0 | 80,3 |
  | PE-Core L/14 | 12,1 | 18,8 | 65,7 | 80,1 |
  | Gemini Embedding 2 | 10,3 | 21,9 | 62,0 | 75,6 |
  | nyris GEM v5.1 | 63,4 | 28,2 | 77,1 | 86,9 |

  L'articolo descrive i fermagli come pezzi "molti dei quali differiscono solo per minime proprietà geometriche o
  dimensionali" e avverte che i test su dataset "intra" (SOP, Products-10K) possono sovrastimare le prestazioni reali.
  Ci sono incongruenze interne (es. SigLIP2 su DIY: 0,0 nel testo, 23,9 in tabella).
- Partium. L'azienda dichiara: trova il ricambio da foto, etichetta, codice, parole o distinta base; estrae da una foto
  dati di targhetta, incisioni e codici; mostra "ogni risposta con fonte e confidenza". Nessun numero di accuratezza;
  nulla su installazione locale. [partium.io](https://www.partium.io/)

### Amazon: ARMBench (centri logistici)
- FATTO: dataset raccolto in un magazzino Amazon con un braccio robotico: 235.000+ prelievi, 190.000+ oggetti diversi;
  compiti: segmentazione, identificazione dell'oggetto, rilevamento difetti. [arXiv 2303.16382](https://arxiv.org/abs/2303.16382)
- FATTO: l'identificazione è impostata come ricerca per immagini in insieme aperto. La galleria non è l'intero
  catalogo ma le foto di riferimento degli oggetti presenti nel contenitore ("container manifest"); fino a 6 foto di
  riferimento per oggetto, prese in operazioni precedenti; per alcuni oggetti mancano, come per un articolo nuovo.
  La verità di riferimento viene da scanner barcode nella cella, o da un operatore che scansiona a mano.
- FATTO: baseline con vettori pre-addestrati e somiglianza coseno: DINO ViT-S Recall@1 77,2% (solo foto del
  prelievo) / 79,5% (con le viste durante il trasferimento); ResNet50-RMAC 71,7/72,2. La difficoltà cresce con il
  numero di oggetti nel contenitore. Confidenza = 1 − c2/c1 (rapporto fra secondo e primo candidato). Richiamo al 99%
  di precisione: 33,8% (test) e 7,8% (test con 20% di oggetti senza foto di riferimento).
- FATTO: gli autori scrivono che, per un richiamo alto con vincoli di precisione, servono stima dell'incertezza e
  altre modalità "come testo e dimensioni". Casi difficili mostrati: confezione cambiata, oggetto senza foto in
  galleria scambiato con uno simile, varianti che differiscono solo per il gusto stampato al centro.
- Il sito ufficiale (armbench.com, ospitato su S3) ha risposto 403: non consultato.

## 4. Dataset e lavori accademici

| Dataset | Contenuto | Dimensione | Licenza | Fonte |
|---|---|---|---|---|
| RPC (Retail Product Checkout) | Foto di singoli prodotti per addestrare + foto di cassa con più prodotti | 53.739 foto singole; 6.000 + 24.000 foto di cassa | CC BY-NC-SA 4.0 (no uso commerciale) | [sito](https://rpc-dataset.github.io/), [arXiv 1901.07249](https://arxiv.org/abs/1901.07249) |
| SKU-110K | Rilevamento di prodotti fitti sugli scaffali | Numeri non leggibili dalla pagina (tabella in immagine) | Solo uso accademico e non commerciale | [repo](https://github.com/eg4000/SKU110K_CVPR19) |
| Products-10K (JD.com) | 10.000 SKU, foto di negozio e di clienti, etichette a gerarchia | ~150.000 immagini, distribuzione sbilanciata | Ricerca non commerciale | [sito](https://products-10k.github.io/), [articolo](https://ar5iv.labs.arxiv.org/html/2008.10545) |
| ABO (Amazon Berkeley Objects) | Prodotti Amazon con metadati, foto 360°, modelli 3D | 147.702 prodotti; 398.212 foto; 7.900+ modelli 3D | CC BY 4.0 (uso commerciale ammesso con attribuzione) | [sito](https://amazon-berkeley-objects.s3.amazonaws.com/index.html) |
| Stanford Online Products | Prodotti online per metric learning | 120.000 immagini, 23.000 classi | Non verificata (pagina del progetto: errore 503) | [arXiv 1511.06452](https://arxiv.org/abs/1511.06452) |
| AliProducts | Immagini web rumorose, non annotate a mano | 50.000 classi, 2,5 milioni di immagini | Non verificata | [ECCV 2020 / arXiv 2008.11586](https://arxiv.org/abs/2008.11586) (letto via risultato di ricerca) |
| RP2K | Prodotti fotografati sugli scaffali di 500+ negozi | v1: 2.000 SKU, 500.000+ immagini; versione successiva: 2.388 SKU, ~400.000 | Non verificata | [arXiv 2006.12634](https://arxiv.org/abs/2006.12634) (numeri dai risultati di ricerca) |
| MVTec D2S | Generi alimentari, scenario cassa/magazzino, maschere al pixel | 21.000 immagini, 60 categorie | CC BY-NC-SA 4.0 | [MVTec](https://www.mvtec.com/company/research/datasets/mvtec-d2s) |
| ARMBench | Vedi sezione 3 | 190.000+ oggetti | Non verificata (sito 403) | [arXiv 2303.16382](https://arxiv.org/abs/2303.16382) |
| ILIAS | Recupero di istanze: 1.000 oggetti contro 100 milioni di immagini di disturbo | — | — | [arXiv 2502.11748](https://arxiv.org/abs/2502.11748) |

### Lavori chiave sugli encoder "di base" usati con poco o nessun addestramento
- DINOv2. FATTO: codice e pesi Apache-2.0; taglie 21M, 86M, 300M, 1,1 miliardi di parametri; caratteristiche usabili
  "senza alcun bisogno di fine-tuning" con classificatori semplici. [repo](https://github.com/facebookresearch/dinov2)
- DINOv3 (agosto 2025). FATTO: supera lo stato dell'arte "senza fine-tuning" in molti compiti; taglie distillate da
  21M a 840M, più 7 miliardi e varianti ConvNeXt. [arXiv 2508.10104](https://arxiv.org/abs/2508.10104),
  [repo](https://github.com/facebookresearch/dinov3). FATTO: licenza propria "DINOv3 License" (gratuita, mondiale, con
  obblighi di redistribuzione e restrizioni su controlli all'esportazione e usi militari).
  [LICENSE.md](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md). DEDUZIONE: non è una licenza open
  source standard; l'uso commerciale sembra permesso, ma va letto da chi decide.
- ILIAS (CVPR 2025). FATTO: i modelli specializzati per un dominio (es. prodotti) vanno bene lì e male altrove; un
  semplice strato lineare di adattamento migliora; i descrittori locali restano importanti per il riordino, specie con
  sfondo disordinato. [arXiv 2502.11748](https://arxiv.org/abs/2502.11748)
- Grocery retrieval con VLM open source (ICPR 2026). FATTO: valutati senza addestramento 190 modelli OpenCLIP; la
  qualità dei dati di pre-addestramento conta più della dimensione; MobileCLIP-B (150M) batte modelli da 351M; i
  migliori arrivano al 94,5% Recall@5 ma perdono 17,5 punti al Recall@1. Codice: github.com/upeee/openmpr.
  [arXiv 2605.18029](https://arxiv.org/abs/2605.18029)
- PRISM (2025). FATTO: SigLIP recupera 35 candidati, YOLO-E ritaglia, LightGlue confronta punti chiave: top-1 da
  38,6% a 42,8%; ~725 ms per richiesta su A100 contro 21,7 ms del solo SigLIP. [arXiv 2509.14985](https://arxiv.org/html/2509.14985v1)
- RetailKLIP (2023): vedi sezione 1.
- Non ho trovato un lavoro accademico pubblico che valuti il riconoscimento con poche foto su decine di migliaia di
  articoli quasi identici fotografati da telefono. I test più grandi trovati: nyris (gallerie da 10.000 a 50.000
  prodotti, ma dati industriali privati) e ARMBench (190.000 oggetti, ma galleria ristretta al contenitore).

## 5. Schemi architetturali ricorrenti

| Schema | Esempi | Pro documentati | Contro documentati |
|---|---|---|---|
| Classificatore chiuso (una classe per articolo) | Progetti YOLO su RPC, repository minori | Semplice, veloce | Ogni articolo nuovo richiede di riaddestrare (DEDUZIONE: è proprio ciò che PP-ShiTu, NVIDIA e Seeed evitano) |
| Rilevatore + embedding + ricerca nel catalogo | PP-ShiTu, NVIDIA, Seeed, baseline ARMBench | Articolo nuovo = nuove foto nell'indice, senza riaddestrare ([PP-ShiTu](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.6/docs/en/quick_start/quick_start_recognition_en.md)) | Precisione al primo colpo bassa su articoli quasi identici ([nyris](https://arxiv.org/html/2603.17186)); cambiare modello obbliga a ricostruire l'indice |
| Come sopra + riordino dei primi candidati (punti chiave, verifica geometrica) | PRISM, repo DINOv2+GIM, ILIAS | Migliora il primo risultato ([PRISM](https://arxiv.org/html/2509.14985v1)) | Molto più lento; da applicare solo ai primi candidati |
| VLM (modello visivo-linguistico) come ripiego o riordino | Seeed (previsto, non implementato), Pailitao-VL (Alibaba, solo sintesi letta) | Può leggere testo e ragionare sui dettagli (IPOTESI) | Latenza e costo; il riordino generativo è citato come collo di bottiglia (Pailitao-VL, da sintesi di ricerca, non verificato sul testo) |
| Fusione con barcode / OCR / peso / ordine atteso | NVIDIA (barcode come controllo), ARMBench (galleria = contenuto atteso), Scandit/Zebra (barcode + testo), Mashgin (3D) | Restringe i candidati e riduce gli errori; ARMBench indica testo e dimensioni come necessari per alta precisione | Richiede dati puliti (codici, pesi, ordini) |

Come gestiscono i punti critici:
- **Catalogo che cambia**: galleria/indice separato dal modello, con versioni (Seeed) o ricostruzione (PP-ShiTu).
- **Articoli quasi identici**: più viste per articolo e in più luci (Seeed); viste multiple al momento della domanda
  migliorano il risultato (ARMBench: da 77,2% a 79,5%); riordino con punti locali (PRISM, ILIAS); restrizione dei
  candidati (ARMBench).
- **Bassa confidenza**: distacco fra primo e secondo (ARMBench `1 − c2/c1`, Seeed `top2_margin`); soglia di somiglianza
  con stato "unknown/unseen" (NVIDIA); conferma o etichettatura da parte di un operatore (NVIDIA; ARMBench usa un
  operatore con scanner quando il barcode non viene letto).
- **Articolo nuovo**: foto + etichetta/barcode inseriti nella galleria dall'utente (PP-ShiTu Android, NVIDIA,
  Seeed 3-8 foto).
- **Conteggio dei pezzi**: poco documentato. SKU-110K tratta il rilevamento di oggetti fitti; Seeed dichiara il
  conteggio "non ancora misurato". Non ho trovato una soluzione documentata per contare pezzi dentro una scatola da
  telefono.

## Lezioni per il nostro progetto (DEDUZIONI)

1. **Lo schema giusto per il catalogo che cresce è "embedding + indice", non un classificatore.** Tutti i sistemi che
   aggiungono articoli senza riaddestrare fanno così. Coincide con la decisione 8.
2. **Restringere i candidati è la leva più forte.** ARMBench confronta solo con gli oggetti attesi nel contenitore e la
   difficoltà cresce con il loro numero. Per noi, al ricevimento, i candidati naturali sono le righe degli ordini
   fornitore aperti (o della bolla del fornitore): decine o centinaia di articoli invece di 35.000. Questo richiede che
   il gestionale conosca gli ordini fornitore attesi.
3. **Con articoli molto simili la sola visione non basta per accettare in automatico.** I numeri su minuteria
   (10-26% al primo colpo con modelli generici) e il basso richiamo ad alta precisione di ARMBench indicano: barcode
   e codice stampato restano la via principale; la visione propone una breve lista (es. primi 5, dove la risposta
   giusta compare molto più spesso) e l'operatore conferma.
4. **Misurare la confidenza col distacco fra primo e secondo candidato** e definire uno stato "non so" che porta a
   conferma manuale o a "articolo nuovo". Le soglie vanno tarate sui nostri dati: nessuna fonte ne dà di riusabili.
5. **Più foto per articolo, in più viste e luci.** Seeed: da 1 a 8 foto il primo colpo passa da 51% a 79%. Il flusso
   "aggiungi articolo" dovrebbe chiedere alcune foto guidate, non una.
6. **Versionare indice e modello insieme.** Cambiare encoder obbliga a ricalcolare tutti i vettori (PP-ShiTu, Seeed):
   conservare sempre le foto originali, non solo i vettori.
7. **OCR sul dispositivo è maturo e gratuito** (ML Kit; PaddleOCR Apache-2.0). Il rischio vero è confrontare il testo
   letto con i codici del catalogo (formati, caratteri simili come 0/O): IPOTESI da verificare con etichette reali.
8. **Il riordino fine (punti chiave, VLM) è un secondo stadio opzionale**, da usare solo sui primi candidati e solo se
   le misure lo giustificano: costa centinaia di millisecondi o più.
9. **Attenzione alle licenze.** Molti dataset sono non commerciali (RPC, SKU-110K, D2S, Products-10K); ABO è CC BY 4.0;
   DINOv2 Apache-2.0; DINOv3 ha una licenza propria; i pesi di Seeed sono non commerciali. Le foto del nostro magazzino
   saranno probabilmente il dato più prezioso.
10. **Gestionale: modellare a parte prenotazione/allocazione e spedizione**, come InvenTree, Odoo, ERPNext. La regola
    "ordine più vecchio prima" va resa esplicita e configurabile (InvenTree non la ha come predefinita).
11. **Nucleo + estensioni come plugin/moduli** (InvenTree, Odoo): utile per la decisione 4 (nucleo generico, poi
    specializzazione). Il riconoscimento visivo può essere un modulo che restituisce "articolo candidato + confidenza"
    al flusso di scansione già esistente.
12. **Le percentuali commerciali (es. Mashgin 99,99%) vengono da hardware fisso e ambienti controllati**: non sono un
    riferimento per un telefono in mano su scatole di magazzino.

## Cosa resta incerto

- Quanto rende la visione sul **nostro** catalogo: nessun dato pubblico copre scatole di magazzino quasi identiche da
  telefono. Serve un piccolo test con foto reali prima di scegliere.
- Se i codici stampati sulle etichette sono abbastanza leggibili e univoci da rendere la visione un caso raro.
- Se l'elaborazione va fatta sul telefono o su un server nella rete locale: entrambe possibili (ML Kit sul
  dispositivo; PP-ShiTu e FAISS su server), non ho trovato confronti diretti per il nostro caso.
- Se un VLM locale aiuti davvero come ripiego: le fonti lette lo citano come previsto o costoso, senza misure utili.
- Conteggio dei pezzi: nessuna soluzione documentata trovata.
- Licenza DINOv3: letta la clausola di concessione, ma la valutazione legale spetta a chi decide.
- Dati non verificati: licenze di SOP, AliProducts, RP2K e ARMBench; numeri di SKU-110K; Odoo Barcode, ERPNext e
  Part-DB non approfonditi; Snipe-IT e OpenBoxes non aperti.
- L'articolo nyris è scritto da nyris e ha incongruenze interne fra testo e tabelle.

## Fonti

Pagine non raggiungibili: armbench.com (S3, 403); pagina Stanford Online Products (503); pagina Diebold Nixdorf Smart
Vision (404, sostituita con stampa di settore dichiarata); benchmark.nyris.io/report (404, sostituito con l'articolo
arXiv); docs.inventree.org/.../sales/allocation (404, usata la pagina sales order); contenuti del repository
PaddleClas via API GitHub (403, letti dalle pagine web).

Open source e documentazione
- https://github.com/PaddlePaddle/PaddleClas/blob/release/2.6/docs/en/PPShiTu/PPShiTuV2_introduction.md
- https://github.com/PaddlePaddle/PaddleClas/blob/release/2.6/docs/en/quick_start/quick_start_recognition_en.md
- https://docs.nvidia.com/mms/text/Smart_self_checkout_Overview.html
- https://wiki.seeedstudio.com/solutions/edge-product-recognition/
- https://github.com/kouroshkarimi/visual_product_recognition_using_DINOv2
- https://github.com/PaddlePaddle/PaddleOCR
- https://github.com/facebookresearch/dinov2
- https://github.com/facebookresearch/dinov3 e https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md

Gestionali
- https://docs.inventree.org/en/latest/sales/sales_order/
- https://docs.inventree.org/en/latest/barcodes/
- https://docs.inventree.org/en/latest/purchasing/purchase_order/
- https://docs.inventree.org/en/latest/plugins/
- https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/shipping_receiving/reservation_methods.html
- https://github.com/odoo/odoo/blob/19.0/addons/stock/models/stock_rule.py
- https://www.odoo.com/documentation/19.0/developer/tutorials/server_framework_101/12_inheritance.html
- https://docs.frappe.io/erpnext/user/manual/en/stock-reservation
- https://github.com/grocy/grocy
- https://docs.part-db.de/usage/getting_started.html

Commerciali
- https://www.mashgin.com/
- https://www.tiliter.com/
- https://www.biometricupdate.com/202506/diebold-nixdorf-integrates-yoti-age-checks-with-produce-recognition-for-self-checkouts (secondaria)
- https://www.scandit.com/products/smart-label-capture/
- https://developers.google.com/ml-kit/vision/text-recognition/v2 e .../v2/android
- https://techdocs.zebra.com/datawedge/14-0/guide/programmers-guides/workflow-input
- https://anyline.com/products/
- https://www.nyris.io/
- https://www.partium.io/

Articoli e dataset
- https://arxiv.org/abs/2303.16382 (ARMBench)
- https://arxiv.org/html/2603.17186 (Visual Product Search Benchmark, nyris)
- https://arxiv.org/abs/2605.18029 (Grocery product retrieval con VLM open source)
- https://arxiv.org/html/2509.14985v1 (PRISM)
- https://arxiv.org/abs/2502.11748 (ILIAS)
- https://arxiv.org/abs/2508.10104 (DINOv3)
- https://arxiv.org/abs/2312.10282 (RetailKLIP)
- https://rpc-dataset.github.io/ e https://arxiv.org/abs/1901.07249
- https://github.com/eg4000/SKU110K_CVPR19
- https://products-10k.github.io/ e https://ar5iv.labs.arxiv.org/html/2008.10545
- https://amazon-berkeley-objects.s3.amazonaws.com/index.html
- https://arxiv.org/abs/1511.06452 (Stanford Online Products)
- https://arxiv.org/abs/2008.11586 (AliProducts)
- https://arxiv.org/abs/2006.12634 (RP2K)
- https://www.mvtec.com/company/research/datasets/mvtec-d2s
