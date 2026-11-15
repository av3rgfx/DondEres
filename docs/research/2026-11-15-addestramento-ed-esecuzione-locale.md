# Addestramento ed esecuzione locale per il riconoscimento degli articoli

Data: 15/11/2026

## Domanda

Serve addestrare un modello leggero o si può partire senza? Come si adatta con pochi dati, e come si esegue tutto in
locale su telefono, browser e server in sede?

Contesto: gestionale di magazzino; l'operatore inquadra la scatola col telefono (Android/iOS; in secondo luogo un
computer con telecamera); tutto sulla rete aziendale, niente cloud. Ordine di identificazione: barcode, poi codice
stampato (OCR), poi riconoscimento visivo. Fino a 35.000 articoli, somiglianza medio-alta. Un articolo nuovo si aggiunge
fotografandolo, senza riaddestrare.

Legenda: **FATTO** = verificato sulla fonte linkata (aperta il 15/11/2026); **DEDUZIONE** = ragionamento a partire dai
fatti; **IPOTESI** = da verificare con prove sul campo; **non verificato** = dalla memoria, senza fonte aperta.

## Sintesi

1. **Si può partire senza addestrare.** Il riconoscimento di istanza nei lavori originali di DINOv2 e DINOv3 si fa
   proprio così: encoder congelato e similarità coseno contro un archivio di foto. Aggiungere un articolo vuol dire
   aggiungere le sue foto all'archivio. (FATTO sul metodo; DEDUZIONE sull'applicabilità.)
2. **Ma con articoli molto simili l'encoder congelato può non bastare.** L'unico studio recente trovato su prodotti
   simili (Cat2Real, 2026) riporta top-1 del 54% con DINOv3 congelato e dell'81% dopo un adattamento contrastivo.
   Lo scenario non è identico al nostro: va misurato sui nostri articoli. (FATTO + DEDUZIONE)
3. **L'adattamento consigliato, se serve, è metric learning su un encoder pre-addestrato**, non un classificatore chiuso:
   l'embedding adattato funziona anche su articoli non visti in addestramento, quindi il catalogo può crescere senza
   riaddestrare ogni volta. (FATTO in Cat2Real: −0,5 punti sui prodotti esclusi dall'addestramento.)
4. **La ricerca esatta basta.** 35.000 articoli × 10 foto = 350.000 vettori: circa 0,5-1 GB in float32, e il calcolo
   della ricerca costa una frazione del calcolo dell'encoder. Un indice approssimato non è necessario all'inizio.
   (DEDUZIONE da dati FAISS e dalle dimensioni dei modelli.)
5. **Barcode e OCR si fanno bene in locale su telefono con app nativa** (ML Kit su Android, Vision/VisionKit su iOS).
   Nel browser il supporto è disomogeneo: `BarcodeDetector` manca su iPhone e su Windows; servono librerie WebAssembly.
   (FATTO)
6. **Una web app sulla rete locale richiede HTTPS anche in LAN**, altrimenti la fotocamera non è accessibile; su iPhone le
   web app installate ripetono la richiesta di permesso. (FATTO)
7. **Architettura più semplice da far partire**: telefono che fa barcode/OCR e invia la foto a un server in sede che
   calcola l'embedding e cerca nell'indice. Il modello sul telefono è possibile ma moltiplica i formati e le versioni da
   gestire. (DEDUZIONE)

## A. Senza addestramento: encoder pre-addestrato + ricerca per somiglianza

### FATTI

- **DINOv2** (Meta, 2023), encoder auto-supervisionato. Su ImageNet-1k: ViT-S/14 (21M parametri) k-NN 79,0% e linear
  probe 81,1%; ViT-B/14 (86M) 82,1% / 84,5%; ViT-L/14 (300M) 83,5% / 86,3%. Codice e pesi **Apache 2.0**.
  [README DINOv2](https://github.com/facebookresearch/dinov2)
- Nel lavoro DINOv2 il **riconoscimento di istanza** (Oxford/Paris, Met, AmsterTime) è fatto senza addestramento: "le
  immagini dell'archivio sono ordinate per similarità coseno con l'immagine di query". DINOv2 ViT-L/14 fa 54,0 mAP su
  Oxford-Hard contro 19,7 di OpenCLIP ViT-G/14, e supera OpenCLIP in tutte le colonne della Tabella 9.
  [DINOv2, arXiv 2304.07193, Tab. 9](https://arxiv.org/html/2304.07193v2)
- Sulla **grana fine** con linear probe (12 dataset, Tab. 8) DINOv2 ViT-g/14 e OpenCLIP ViT-G/14 sono quasi pari in
  media (92,1 vs 91,9); DINOv2 è indietro su Cars (91,4 vs 96,1) e SUN. [DINOv2, Tab. 8](https://arxiv.org/html/2304.07193v2)
- **DINOv3** (Meta, 2025) dichiara feature utilizzabili "senza fine-tuning" e una famiglia distillata: ViT-S/16 21M,
  ViT-S+/16 29M, ViT-B/16 86M, ViT-L/16 300M, ViT-H+/16 840M; ConvNeXt Tiny 29M, Small 50M, Base 89M, Large 198M.
  [arXiv 2508.10104](https://arxiv.org/abs/2508.10104), [repository](https://github.com/facebookresearch/dinov3)
- Nella Tab. 14 di DINOv3 (modelli distillati), sul recupero di istanza Oxford-Hard: ViT-S 39,5 (DINOv2) → 49,5
  (DINOv3); ViT-B 51,0 → 58,5; ViT-L 55,7 → 63,1. Sul modello grande (Tab. 9) Met passa da 44,6 a 55,4.
  [DINOv3, testo completo](https://arxiv.org/html/2508.10104)
- **Licenza DINOv3**: non è Apache. La "DINOv3 License" è gratuita, mondiale, non esclusiva e non esclude l'uso
  commerciale, ma vieta usi militari/ITAR e il reverse engineering, chiede di distribuire una copia dell'accordo con i
  derivati, e Meta può modificarla. I pesi sono "gated" (accesso su richiesta; su Hugging Face: gated "manual", licenza
  "other"). Supporto in Transformers ≥ 4.56.0 e timm ≥ 1.0.20.
  [LICENSE.md](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md),
  [model card HF](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m)
- **SigLIP 2** (Google, 2025): encoder immagine-testo in quattro taglie (ViT-B 86M, L 303M, So400m 400M, g 1B); migliora
  su zero-shot, recupero immagine-testo e caratteristiche dense; varianti a risoluzione multipla con proporzioni native.
  [arXiv 2502.14786](https://arxiv.org/abs/2502.14786). Model card su Hugging Face: Apache 2.0, non gated.
  [google/siglip2-base-patch16-224](https://huggingface.co/google/siglip2-base-patch16-224)
- **CLIP** (OpenAI, 2021): lo zero-shot (classi descritte a parole) eguaglia in media un linear probe con **4 esempi per
  classe** sulle stesse feature; l'equivalente varia moltissimo tra dataset (mediana 5,4, media 20,8, massimo 184 esempi
  per classe) ed è debole su compiti specialistici.
  [CLIP, arXiv 2103.00020, Fig. 6 e sez. 3.1.5](https://arxiv.org/pdf/2103.00020)
- **Il caso più vicino al nostro**: *Cat2Real* (luglio 2026) tratta il riconoscimento di prodotti come **recupero per
  embedding** da foto reale verso immagini di catalogo (valutazione: 5.043 foto, 1.865 prodotti, ambito di ricerca
  2.155 prodotti). Encoder congelati: DINOv2 ViT-L/14 top-1 35,5% / top-5 61,4%; DINOv3 ViT-L/16 a 384 px 53,8% /
  78,1%. Dopo fine-tuning contrastivo: 80,7% / 94,7%. [arXiv 2607.09888](https://arxiv.org/html/2607.09888)
- Già nel 2019, un lavoro sui prodotti da supermercato motivava l'uso di un embedding + K-NN col fatto che gli articoli
  cambiano spesso e un classificatore andrebbe riaddestrato di continuo.
  [arXiv 1902.00760](https://arxiv.org/pdf/1902.00760)
- **Apple Create ML** consiglia, per un classificatore, **almeno 10 immagini per categoria**, bilanciate, da più angoli e
  luci, simili a quelle che il modello vedrà; insieme di prova del 20% se ci sono almeno 25 immagini per categoria.
  [Create ML, Creating an Image Classifier Model](https://developer.apple.com/documentation/createml/creating-an-image-classifier-model)
- Su iOS esiste anche un estrattore di "feature print" di sistema (`VNGenerateImageFeaturePrintRequest`, da iOS 13).
  [Apple Vision](https://developer.apple.com/documentation/vision/vngenerateimagefeatureprintrequest)

### DEDUZIONI

- Le tre varianti "senza addestramento" sono, in ordine di semplicità: (1) **k-NN** su tutte le foto di riferimento;
  (2) **prototipo per articolo** (media degli embedding delle sue foto) — meno memoria, ma perde le viste diverse;
  (3) **linear probe** — è un classificatore chiuso: va rifatto quando cambia il catalogo, quindi va contro il
  requisito "aggiungo con una foto". Per noi la strada naturale è (1), eventualmente con (2) come filtro veloce.
- Il dato Cat2Real dice che con prodotti simili un encoder congelato può sbagliare circa una volta su due in top-1, ma
  che il top-5 è molto più alto (78%). Nel nostro caso la differenza di dominio è minore (foto di riferimento e di query
  fatte con telefoni nello stesso magazzino), quindi è plausibile fare meglio. **Nessun numero pubblicato** riguarda il
  nostro scenario: va misurato.
- Il top-5 alto suggerisce un'interfaccia "propongo 3-5 candidati, l'operatore sceglie": utile finché il top-1 non basta.
- Lo zero-shot da testo (CLIP/SigLIP) serve a poco: gli articoli si distinguono per codici e dettagli, non per nomi.
- **Numero di foto di riferimento**: non ho trovato una regola pubblicata per il k-NN su articoli di magazzino. IPOTESI
  di partenza: 3-5 foto per articolo (fronte, lato, etichetta), che crescono con le conferme (vedi C).
- **Scelta del modello**: DINOv2 (Apache 2.0, nessun vincolo) per partire senza problemi di licenza; DINOv3 è più forte
  sul recupero di istanza ma ha una licenza propria da far valutare; SigLIP 2 (Apache 2.0) è un'alternativa da
  confrontare. La scelta va fatta con una prova sui nostri articoli, non sui benchmark.

## B. Adattamento leggero

### FATTI

- **Metric learning**: *A Metric Learning Reality Check* (Musgrave et al., 2020) rifà gli esperimenti con protocollo
  corretto e trova che i progressi delle loss recenti rispetto a quelle di dieci anni prima sono "marginali nel migliore
  dei casi". [arXiv 2003.08505](https://arxiv.org/abs/2003.08505)
- **pytorch-metric-learning**: licenza MIT, versione 3.0.3 (13/11/2026); la v3 richiede Python ≥ 3.12 e PyTorch ≥ 2.14;
  backend FAISS opzionale. [repository](https://github.com/KevinMusgrave/pytorch-metric-learning),
  [LICENSE](https://raw.githubusercontent.com/KevinMusgrave/pytorch-metric-learning/master/LICENSE),
  [PyPI](https://pypi.org/project/pytorch-metric-learning/)
- **Fine-tuning parziale + contrastivo**: Cat2Real congela i primi 12 blocchi su 24 di DINOv3 ViT-L/16 e addestra gli
  altri con apprendimento contrastivo e ricerca di negativi difficili; su ~197.000 foto reali di ~27.000 prodotti passa
  da 53,8% a 80,7% top-1. Togliendo dall'addestramento tutti i prodotti di valutazione, il top-1 scende solo a 80,2%.
  Addestramento su una sola A100; ore non riportate. [arXiv 2607.09888](https://arxiv.org/html/2607.09888)
- **LoRA** con Hugging Face PEFT su ViT-B/16: si addestra lo 0,77% dei parametri (667.493 su 86,5M), l'adattatore pesa
  ~2,6 MB; nell'esempio ufficiale (5.000 immagini Food-101, classificazione) arriva al 96% in validazione in 5 epoche.
  PEFT è Apache 2.0, versione 0.21.3 (13/11/2026).
  [guida PEFT LoRA](https://huggingface.co/docs/peft/main/en/task_guides/image_classification_lora),
  [PyPI](https://pypi.org/project/peft/)
- **Distillazione**: i modelli piccoli di DINOv2 e DINOv3 sono ottenuti distillando un modello grande.
  [DINOv2](https://arxiv.org/abs/2304.07193), [DINOv3](https://arxiv.org/html/2508.10104)

### DEDUZIONI

- Conviene adattare **solo dopo aver misurato** che l'encoder congelato non basta (vedi I), e conviene adattare
  l'**embedding** (metric learning) invece di addestrare un classificatore: l'embedding adattato resta utilizzabile per
  articoli nuovi, come mostra Cat2Real.
- Visto il "reality check", non vale la pena inseguire la loss più recente: una loss classica (contrastiva, triplet,
  ArcFace o ProxyAnchor da pytorch-metric-learning) con buona scelta dei negativi difficili e buona validazione basta.
- Il valore sta nelle **coppie difficili**: foto di articoli simili ma diversi. Il ciclo di conferma (C) le raccoglie
  gratis: ogni correzione dell'operatore è un negativo difficile.
- LoRA e fine-tuning parziale sono modi per adattare con poca memoria e pochi dati; dopo l'adattamento **tutti gli
  embedding dell'archivio vanno ricalcolati** con il nuovo modello (costo da prevedere, non bloccante: vedi E).
- Distillazione verso un modello più piccolo serve solo se si vuole il modello sul telefono e il modello piccolo
  congelato non basta. Augmentation e dati sintetici: non ho cercato studi specifici per questo caso; IPOTESI che
  l'augmentation di luce/rotazione/sfocatura sia utile, ma non sostituisce foto reali delle condizioni del magazzino.
- Dati necessari, ordine di grandezza (IPOTESI): qualche migliaio di foto etichettate di qualche centinaio di articoli,
  con molte coppie simili. Cat2Real ne ha usate circa 200.000; non ho trovato una curva "quante foto servono".

## C. Catalogo che cambia

### FATTI

- *Open-Set Recognition: a Good Closed-Set Classifier is All You Need* (Vaze et al., 2022): la capacità di dire
  "nessuno dei noti" è fortemente correlata all'accuratezza sui noti; un baseline semplice basato sul punteggio massimo,
  se il modello è accurato, arriva allo stato dell'arte. [arXiv 2110.06207](https://arxiv.org/abs/2110.06207)
- *On Calibration of Modern Neural Networks* (Guo et al., 2017): le reti moderne sono **mal calibrate** (la confidenza
  non corrisponde alla probabilità di avere ragione); il *temperature scaling*, un solo parametro, corregge bene nella
  maggior parte dei casi. [arXiv 1706.04599](https://arxiv.org/abs/1706.04599)
- Il riconoscimento per embedding + K-NN è scelto in letteratura proprio perché gli articoli cambiano spesso.
  [arXiv 1902.00760](https://arxiv.org/pdf/1902.00760), [Cat2Real](https://arxiv.org/html/2607.09888)

### DEDUZIONI

- **Classificatore chiuso**: aggiungere un articolo richiede riaddestramento. **Ricerca per somiglianza**: aggiungere un
  articolo è un inserimento nell'indice. Il requisito utente (decisione 8 in `docs/decisioni.md`) porta alla seconda.
- **Rifiuto degli sconosciuti** con la ricerca per somiglianza: tre segnali semplici e combinabili:
  1. similarità del primo risultato sotto una soglia → "non so";
  2. distacco piccolo tra primo e secondo **articolo** (non foto) → "incerto, scegli tu";
  3. accordo dei primi k vicini sullo stesso articolo.
- Le soglie **non si fissano a priori**: si scelgono su un insieme di prova separato (vedi I), decidendo quanti "non so"
  si accettano per un dato tasso di errore. La similarità coseno non è una probabilità (per analogia con Guo et al.).
- **Ciclo di conferma**: l'app propone; l'operatore conferma o corregge; la foto entra nell'archivio con l'articolo
  confermato. Rischi da gestire: foto sbagliate che "avvelenano" l'archivio (serve tracciare chi ha confermato e poter
  togliere foto), crescita senza limite (tetto di foto per articolo, scelte per varietà), e articoli quasi identici
  (meglio segnalarli come gruppo da distinguere col codice/OCR).
- Il barcode/OCR riuscito è una **etichetta gratuita**: quando l'articolo è identificato dal codice, la foto può entrare
  nell'archivio visivo senza che l'operatore faccia nulla.

## D. Strumenti di annotazione e addestramento

Versioni e licenze verificate sui file LICENSE e su PyPI il 15/11/2026.

| Strumento | Uso | Licenza | Versione | Note |
|---|---|---|---|---|
| Label Studio | annotazione | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/HumanSignal/label-studio/master/LICENSE)) | 1.23.2 ([PyPI](https://pypi.org/project/label-studio/)) | self-hosted |
| CVAT | annotazione | MIT ([LICENSE](https://raw.githubusercontent.com/cvat-ai/cvat/master/LICENSE)) | cvat-sdk 2.83.0 ([PyPI](https://pypi.org/project/cvat-sdk/)) | self-hosted |
| FiftyOne (+ Brain) | esplorare dataset, duplicati, errori, similarità | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/voxel51/fiftyone/main/LICENSE); Brain Apache 2.0 su [PyPI](https://pypi.org/project/fiftyone-brain/)) | 1.22.1 | utile per I |
| timm | modelli PyTorch pre-addestrati | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/huggingface/pytorch-image-models/main/LICENSE)) | 1.0.31 | supporta DINOv3 da 1.0.20 |
| Transformers | modelli + addestramento | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/huggingface/transformers/main/LICENSE)) | 5.23.0 | |
| PEFT | LoRA/adapter | Apache 2.0 | 0.21.3 | |
| pytorch-metric-learning | loss, miner | MIT | 3.0.3 | |
| Ultralytics (YOLO) | rilevamento/classificazione | **AGPL-3.0** ([LICENSE](https://raw.githubusercontent.com/ultralytics/ultralytics/main/LICENSE)) | 8.4.213 | vedi sotto |
| Create ML | classificatore su Mac | proprietario Apple | — | solo macOS/Xcode |
| MediaPipe Model Maker | transfer learning per MediaPipe | Apache 2.0 | 0.2.1.4, **ultimo rilascio 22/04/2024** ([PyPI](https://pypi.org/project/mediapipe-model-maker/)) | vedi sotto |

FATTI importanti:

- **Ultralytics**: per uso commerciale/chiuso o strumenti interni la pagina licenze indica di rilasciare tutto il codice
  sotto AGPL o comprare la licenza Enterprise; "tutti i modelli YOLO addestrati con Ultralytics ricadono sotto AGPL-3.0".
  [ultralytics.com/license](https://www.ultralytics.com/license)
- **Create ML**: richiede Xcode su macOS, produce un modello Core ML; estrattore di default "scene print".
  [Apple](https://developer.apple.com/documentation/createml/creating-an-image-classifier-model)
- **MediaPipe Model Maker**: il pacchetto non riceve rilasci da aprile 2024; la pagina attuale dell'Image Classifier
  MediaPipe parla solo dei modelli pre-addestrati EfficientNet-Lite0/Lite2 (int8/float32, 224×224) e non cita più Model
  Maker. [PyPI](https://pypi.org/project/mediapipe-model-maker/),
  [MediaPipe Image Classifier](https://developers.google.com/edge/mediapipe/solutions/customization/image_classifier)

DEDUZIONI: per la nostra strada (embedding + ricerca) servono soprattutto **FiftyOne** (vedere le confusioni, trovare
duplicati e foto sbagliate) e, se si adatta, **timm/Transformers + PEFT + pytorch-metric-learning**. Label Studio o CVAT
servono solo se si arriva a un rilevatore di scatole o a ritagli manuali. Ultralytics è da evitare salvo licenza
Enterprise; Create ML e Model Maker producono classificatori chiusi, poco adatti al catalogo che cambia (e Model Maker
sembra fermo).

## E. Indici vettoriali locali

### FATTI

| Strumento | Licenza | Forma | Note dalla fonte |
|---|---|---|---|
| NumPy forza bruta | BSD (non verificato) | libreria | prodotto matrice-vettore |
| FAISS | MIT ([LICENSE](https://raw.githubusercontent.com/facebookresearch/faiss/main/LICENSE)) | libreria | v1.16.0 ([PyPI faiss-cpu](https://pypi.org/project/faiss-cpu/)); "l'unico indice che garantisce risultati esatti è IndexFlatL2/IndexFlatIP"; flat non comprime e non aggiunge overhead; tutti gli indici stanno in RAM; HNSW usa (d·4 + M·2·4) byte per vettore ([wiki](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)) |
| hnswlib | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/nmslib/hnswlib/master/LICENSE)) | libreria header-only C++/Python | inserimenti e aggiornamenti ([README](https://github.com/nmslib/hnswlib)); **ultimo rilascio PyPI 0.8.0 del 03/12/2023** ([PyPI](https://pypi.org/project/hnswlib/)) |
| USearch | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/unum-cloud/usearch/main/LICENSE)) | libreria header-only C++20, binding Python/JS/Swift/Java… | ricerca esatta disponibile in tutti i binding; v2.26.6 ([README](https://github.com/unum-cloud/usearch)) |
| sqlite-vec | MIT o Apache 2.0 ([MIT](https://raw.githubusercontent.com/asg017/sqlite-vec/main/LICENSE-MIT), [Apache](https://raw.githubusercontent.com/asg017/sqlite-vec/main/LICENSE-APACHE)) | estensione SQLite, anche WASM | "pre-v1, aspettatevi modifiche incompatibili"; vettori float, int8, binari; v0.1.9 del 31/03/2026 ([README](https://github.com/asg017/sqlite-vec)) |
| pgvector | licenza PostgreSQL ([LICENSE](https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE)) | estensione PostgreSQL (server) | ricerca esatta per default ("perfect recall"); HNSW o IVFFlat opzionali; `vector` fino a 2.000 dimensioni, `halfvec` fino a 4.000 ([README](https://github.com/pgvector/pgvector)) |
| LanceDB | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/lancedb/lancedb/main/LICENSE)) | incorporabile ("gira nel processo dell'applicazione") | v0.41.0 ([README](https://github.com/lancedb/lancedb)) |
| Qdrant | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/qdrant/qdrant/master/LICENSE)) | server (Docker) | client v1.20.0 ([README](https://github.com/qdrant/qdrant)) |

### Dimensionamento (DEDUZIONE, calcoli miei)

Dimensione dell'embedding: 384 per ViT-S, 768 per ViT-B, 1024 per ViT-L (dimensioni standard delle architetture, non
verificate sulle model card).

| Foto per articolo | Vettori (35.000 art.) | ViT-S 384, float32 | ViT-B 768, float32 | ViT-B 768, float16 |
|---|---|---|---|---|
| 5 | 175.000 | 269 MB | 538 MB | 269 MB |
| 10 | 350.000 | 538 MB | 1,08 GB | 538 MB |
| 20 | 700.000 | 1,08 GB | 2,15 GB | 1,08 GB |

- Calcolo di una ricerca esatta con 350.000 vettori a 768 dimensioni: ~0,27 miliardi di moltiplicazioni-somme. Per
  confronto, un DeiT-S (architettura ViT-S) costa 4,5 GMAC per immagine
  ([EfficientFormer, Tab. 1](https://arxiv.org/pdf/2206.01191v5)): la ricerca costa circa il 6% di una sola passata
  dell'encoder piccolo. **La ricerca esatta basta**: il collo di bottiglia è l'encoder, non l'indice.
- HNSW con M=32 su 768 dimensioni: 3.328 byte/vettore (formula FAISS) contro 3.072 del flat → stessa memoria, più
  complessità, risultati approssimati. Non conviene a questa scala.
- Le linee guida FAISS citano indici IVF per "meno di 1M di vettori" quando serve velocità; a 0,35M e con la ricerca che
  pesa poco rispetto all'encoder, il flat esatto è la scelta semplice. Da rivalutare solo oltre ~1M vettori o se le
  misure dicono altro.
- Per un indice **sul telefono**: 35.000 prototipi (uno per articolo) a 384 dimensioni in float16 sono ~27 MB; tutte le
  foto (175.000 × 384 × 2 byte) ~134 MB. Possibile, ma va sincronizzato con il server.
- Scelta semplice: **NumPy o FAISS flat** in memoria sul server, con gli embedding salvati nel database dell'applicazione
  (o pgvector se il database è PostgreSQL, che fa già ricerca esatta). Un server vettoriale separato (Qdrant) non serve
  a questa scala.

## F. Runtime e formati

### FATTI

| Runtime | Licenza | Piattaforme e acceleratori (dalla fonte) | Versione |
|---|---|---|---|
| ONNX Runtime | MIT ([LICENSE](https://raw.githubusercontent.com/microsoft/onnxruntime/main/LICENSE)) | CPU, CUDA, TensorRT, OpenVINO, DirectML, QNN (Qualcomm), XNNPACK, WebGPU, NNAPI; **CoreML in "Preview"**; ROCm deprecato ([execution providers](https://onnxruntime.ai/docs/execution-providers/)) | 1.32.0 ([PyPI](https://pypi.org/project/onnxruntime/)) |
| ONNX Runtime Web | MIT | WASM (tutti gli operatori) e WebGPU/WebGL/WebNN (sottoinsieme di operatori) ([guida](https://onnxruntime.ai/docs/tutorials/web/)) | 1.31.1 ([npm](https://www.npmjs.com/package/onnxruntime-web)) |
| Transformers.js | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/huggingface/transformers.js/main/LICENSE)) | usa ONNX Runtime Web; `device: 'webgpu'`; WebGPU "sperimentale, specie nei browser non Chromium" ([guida WebGPU](https://huggingface.co/docs/transformers.js/guides/webgpu)) | 4.3.2 ([npm](https://www.npmjs.com/package/@huggingface/transformers)) |
| LiteRT (ex TFLite) | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/google-ai-edge/LiteRT/main/LICENSE)) | Android (API 24+), iOS/macOS (runtime iOS ancora **pre-release**), Web (LiteRT.js), desktop; GPU OpenCL/OpenGL/Metal/WebGPU; NPU Qualcomm, MediaTek, Google Tensor, Exynos; conversione da PyTorch con `litert-torch` ([overview](https://developers.google.com/edge/litert/overview)) | ai-edge-litert 2.3.0 |
| MediaPipe Tasks | Apache 2.0 | Web, Android, iOS, Python, Flutter ([Image Classifier](https://developers.google.com/edge/mediapipe/solutions/customization/image_classifier)) | 1.2.3 |
| Core ML / coremltools | BSD-3 ([LICENSE](https://raw.githubusercontent.com/apple/coremltools/main/LICENSE.txt)) | dispositivi Apple (Neural Engine, GPU, CPU) | coremltools 9.0 |
| ExecuTorch | BSD ([LICENSE](https://raw.githubusercontent.com/pytorch/executorch/main/LICENSE)) | XNNPACK (tutte), Core ML, Vulkan (Android maturo), Qualcomm, MediaTek, Exynos, CUDA, WebGPU (sperimentale)… ([backend](https://docs.pytorch.org/executorch/stable/backends-overview.html)) | 1.6.0 |
| OpenVINO | Apache 2.0 ([LICENSE](https://raw.githubusercontent.com/openvinotoolkit/openvino/master/LICENSE)) | CPU/GPU/NPU Intel | 2026.4.1 |
| TensorRT | Apache 2.0 (parti open, [LICENSE](https://raw.githubusercontent.com/NVIDIA/TensorRT/main/LICENSE)) | GPU NVIDIA, Jetson | 11.4 |
| NCNN | BSD-3 ([LICENSE](https://raw.githubusercontent.com/Tencent/ncnn/master/LICENSE.txt)) | mobile (non approfondito) | — |
| llama.cpp | MIT ([LICENSE](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/LICENSE)) | VLM con input immagine via `libmtmd`, `llama-server` con API compatibile OpenAI ([multimodal](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/multimodal.md)) | — |
| Ollama | MIT ([LICENSE](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE)) | server locale per LLM/VLM | — |

Altri FATTI:

- **NNAPI è deprecato da Android 15**; Google indica LiteRT (TFLite in Play Services) e il delegate GPU.
  [Android NNAPI migration guide](https://developer.android.com/ndk/guides/neuralnetworks/migration-guide)
- **WebGPU** (dati MDN): Chrome desktop da 113 (Linux solo GPU Intel Gen12+ da 144), Chrome Android da 121, Safari e
  Safari iOS da 26, Firefox da 141 parziale, Firefox Android no.
  [MDN browser-compat-data, GPU](https://github.com/mdn/browser-compat-data/blob/main/api/GPU.json)
- Esistono export ONNX pubblici di DINOv2-small, DINOv3-ViT-S/16 e SigLIP 2 base (es. `onnx-community/dinov2-small`,
  `onnx-community/dinov3-vits16-pretrain-lvd1689m-ONNX`, `onnx-community/siglip2-base-patch16-224-ONNX`).
  [Hugging Face](https://huggingface.co/onnx-community)
- **Quantizzazione, impatto documentato**:
  - ONNX Runtime: "la quantizzazione non è una trasformazione senza perdita"; dinamica consigliata per i transformer,
    statica per le CNN; QAT solo se la post-training non basta; int8 su GPU solo con Tensor Core int8.
    [ORT quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
  - Core ML: "nella maggior parte dei casi non si perde molta accuratezza con palettizzazione a 6 o 8 bit o
    quantizzazione dei pesi a 8 bit"; W8A8 riduce la latenza su chip recenti (A17 Pro, M4).
    [coremltools optimization](https://apple.github.io/coremltools/docs-guides/source/opt-overview.html)
  - MobileNetV3 (misura pubblicata): Large 1.0 float 75,2% → int8 73,8% top-1 ImageNet; MobileNetV2 1.0 72,0% → 70,9%.
    [MobileNetV3, Tab. 3 e 4](https://arxiv.org/pdf/1905.02244v5)
  - Non ho trovato misure pubblicate dell'effetto di int8/fp16 sul **recupero** con DINOv2/DINOv3: va misurato.

### DEDUZIONI

- **Formato unico consigliato: ONNX**. Lo stesso file gira sul server (ORT CPU/CUDA/OpenVINO), nel browser (ORT Web /
  Transformers.js) e su telefono (ORT mobile; su iOS il provider CoreML è in preview). Core ML o LiteRT nativi servono
  solo se si vuole il massimo sul telefono.
- **Server in sede**: ORT con CPU va bene per cominciare; OpenVINO se la macchina è Intel; CUDA/TensorRT se c'è una GPU
  NVIDIA. fp16 su GPU è il punto di partenza prudente; int8 solo dopo aver misurato l'effetto sul top-1.
- **Regola importante**: embedding dell'archivio e della query **devono** venire dallo stesso modello e dalla stessa
  quantizzazione; se il telefono usa un modello quantizzato e il server un altro, i vettori non sono confrontabili.
- **VLM (llama.cpp/Ollama)**: non adatti a scegliere fra 35.000 articoli (non conoscono il catalogo). Possibile uso
  secondario: leggere un'etichetta difficile o descrivere un articolo nuovo. Peso e tempi elevati: IPOTESI da misurare.

## G. OCR e barcode in locale

### FATTI

- **ML Kit Barcode** (Android/iOS): tutto sul dispositivo, senza rete; formati Codabar, Code 39/93/128, EAN-8/13, ITF,
  UPC-A/E, Aztec, Data Matrix, PDF417, QR; qualsiasi orientamento. Limiti: niente codici 1D di un solo carattere, ITF
  sotto 6 caratteri, FNC2/3/4, QR in modalità ECI; massimo 10 codici per chiamata. Il "Google code scanner" restituisce
  solo il codice più centrale e non richiede permessi fotocamera.
  [ML Kit barcode scanning](https://developers.google.com/ml-kit/vision/barcode-scanning)
- **ML Kit Text Recognition v2**: alfabeti cinese, devanagari, giapponese, coreano e latino. Su Android: modello in Play
  Services ~260 KB o incluso ~4 MB per alfabeto e architettura; carattere di almeno **16×16 pixel** (oltre 24×24 non
  migliora); API minima 23; modelli eseguiti sul dispositivo.
  [ML Kit text v2](https://developers.google.com/ml-kit/vision/text-recognition/v2),
  [Android](https://developers.google.com/ml-kit/vision/text-recognition/v2/android)
- **Apple**: `VNDetectBarcodesRequest` (iOS 11+), `VNRecognizeTextRequest` (iOS 13+), nuova `RecognizeTextRequest`
  (iOS 18+), e `DataScannerViewController` di VisionKit (iOS 16+) che scansiona dal video testo e codici.
  [Vision barcode](https://developer.apple.com/documentation/vision/vndetectbarcodesrequest),
  [Vision text](https://developer.apple.com/documentation/vision/vnrecognizetextrequest),
  [RecognizeTextRequest](https://developer.apple.com/documentation/vision/recognizetextrequest),
  [DataScannerViewController](https://developer.apple.com/documentation/visionkit/datascannerviewcontroller)
- **BarcodeDetector nel browser** (dati MDN): Chrome Android sì (da 83); Chrome desktop **solo ChromeOS e macOS**; Edge
  solo macOS; **Safari/iOS solo dietro flag**; Firefox no. Stato "sperimentale".
  [MDN browser-compat-data, BarcodeDetector](https://github.com/mdn/browser-compat-data/blob/main/api/BarcodeDetector.json)
- **ZXing (Java)**: "progetto in sola manutenzione", nessuno sviluppo attivo. [README](https://github.com/zxing/zxing)
- **zxing-cpp**: Apache 2.0, binding Android, iOS, Python, .NET, **WebAssembly** e altri.
  [README](https://github.com/zxing-cpp/zxing-cpp). Esiste anche `@zxing/library` (porta JS, Apache 2.0, 0.23.0).
  [npm](https://www.npmjs.com/package/@zxing/library)
- **PaddleOCR**: Apache 2.0, versione 3.7.0 (giugno 2026). Il README dichiara PP-OCRv6 in tre taglie (1,5M / 7,7M /
  34,5M parametri) per edge, mobile e server, e un SDK ufficiale per browser (`PaddleOCR.js`, PP-OCRv5). Le affermazioni
  di accuratezza del README sono del produttore. [README](https://github.com/PaddlePaddle/PaddleOCR)
- **Tesseract.js**: Apache 2.0, v7.0.0; porta WebAssembly di Tesseract, "non modifica il modello di riconoscimento per
  migliorarne l'accuratezza". [README](https://github.com/naptha/tesseract.js)

### DEDUZIONI

- **App nativa**: barcode e OCR sono risolti dal sistema (ML Kit, Vision), gratuiti, offline, ottimizzati.
- **Web app**: sul telefono Android `BarcodeDetector` funziona; su iPhone e su PC Windows/Linux no → serve zxing-cpp in
  WASM (o `@zxing/library`) come ripiego. Per l'OCR nel browser: Tesseract.js o PaddleOCR.js, oppure **OCR sul server**
  (PaddleOCR) con la stessa foto inviata per il riconoscimento visivo.
- Per l'OCR del codice articolo conviene **confrontare il testo letto con l'elenco dei codici del catalogo** (corrispondenza
  esatta o con tolleranza di 1-2 caratteri): trasforma un OCR imperfetto in una scelta fra codici esistenti.

## H. Architettura e hardware

### FATTI: vincoli della fotocamera da web app

- `getUserMedia` funziona solo in **contesto sicuro**: in contesto non sicuro `navigator.mediaDevices` è `undefined`.
  [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- Sono contesti sicuri `https`, `localhost`, `127.0.0.0/8`; un IP di rete locale in `http` (es. `http://192.168.x.x`)
  **non** lo è. [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)
- Let's Encrypt con sfida **DNS-01** rilascia certificati per nomi i cui server non sono esposti a internet (serve un
  dominio pubblico e l'API del DNS); non vale per indirizzi IP.
  [Let's Encrypt challenge types](https://letsencrypt.org/docs/challenge-types/)
- iOS, web app installate: il bug WebKit "Persist permissions for getUserMedia" è **aperto** (stato NEW, ultima modifica
  08/07/2026); commenti del 2026 riportano che la PWA chiede di nuovo il permesso fotocamera, anche alla riaccensione
  dello schermo. [WebKit bug 280394](https://bugs.webkit.org/show_bug.cgi?id=280394)

### FATTI: tempi misurati (fonti primarie)

| Modello | Dispositivo | Tempo | Fonte |
|---|---|---|---|
| MobileNetV2 1.0 | iPhone 12, Neural Engine / solo CPU | 1,3 ms / 8,0 ms | [EfficientFormer, Tab. 1](https://arxiv.org/pdf/2206.01191v5) |
| ResNet-50 | iPhone 12, NPU / CPU | 3,0 / 29,4 ms | idem |
| DeiT-S (architettura ViT-S, 22,5M, 4,5 GMAC) | iPhone 12, NPU / CPU | 11,8 / 41,0 ms | idem |
| MobileNetV3-Large 1.0 float | Pixel 1 / 2 / 3, un core grande | 51 / 61 / 44 ms | [MobileNetV3, Tab. 3](https://arxiv.org/pdf/1905.02244v5) |
| MobileNetV2 1.0 float | Pixel 1 / 2 / 3, un core grande | 64 / 76 / 56 ms | idem |
| ResNet (MLPerf) | Jetson AGX Orin | 0,64 ms (single stream) | [NVIDIA Jetson benchmarks](https://developer.nvidia.com/embedded/jetson-benchmarks) |
| ResNet (MLPerf) | Jetson Orin NX 16GB | 2.640 campioni/s (offline) | idem |

Misure **mancanti**: non ho trovato tempi pubblicati da fonti primarie per DINOv2/DINOv3 ViT-S o ViT-B su telefoni
Android recenti, su PC senza GPU o su mini-PC; né per ViT-B su iPhone. La pagina benchmark di OpenVINO non è leggibile
con lo strumento usato (contenuto dinamico). Le misure su iPhone 12 e Pixel 1-3 sono di hardware vecchio (2016-2020).

### DEDUZIONI

| | (a) Modello sul telefono | (b) Foto al server in sede |
|---|---|---|
| Modello e indice | su ogni telefono, da sincronizzare | uno solo, sul server |
| Aggiunta articolo | arriva ai telefoni con la sincronizzazione | immediata per tutti |
| Formati | ONNX + Core ML/LiteRT, test su molti modelli di telefono | ONNX su un solo server |
| Funziona senza rete | sì | no (ma il requisito è comunque la rete aziendale) |
| Tempi | ViT-S ~12 ms su NPU di iPhone 12 (misura sopra); Android variabile | rete locale + encoder sul server: da misurare |
| Telefoni vecchi | rischio di lentezza | indifferenti |

- **Partire con (b)**: un solo modello, un solo indice, aggiornamento istantaneo del catalogo. Barcode e OCR restano sul
  telefono (veloci, di sistema) e la foto va al server solo se il codice non c'è o non si legge.
- (a) ha senso dopo, per lavorare senza rete o per rispondere mentre si inquadra; richiede di mantenere coerenti
  modello e quantizzazione tra telefono e server (vedi F).
- **App nativa vs web app**: la web app evita gli store ma richiede HTTPS con certificato valido in LAN, ripiego WASM
  per i barcode su iPhone/PC e convive con i permessi ripetuti delle PWA iOS. L'app nativa ha ML Kit/Vision e permessi
  stabili. Decisione da prendere con l'utente (costo di distribuzione vs esperienza).
- **Server**: un PC senza GPU probabilmente basta per un ViT-S/ViT-B con poche richieste al minuto (IPOTESI, nessuna
  misura primaria trovata); una GPU NVIDIA o un Jetson Orin danno margine. Da misurare sulla macchina scelta.

## I. Qualità della ripresa e misura dell'accuratezza

### FATTI

- ObjectNet (NeurIPS 2019) varia in modo controllato rotazione, sfondo e punto di vista: i modelli perdono il **40-45%**
  di prestazioni rispetto agli altri benchmark. [objectnet.dev](https://objectnet.dev/)
- Nella Tab. 14 di DINOv3 anche gli encoder recenti calano molto su ObjectNet: ViT-S DINOv3 87,0 su ImageNet-ReaL
  contro 50,9 su ObjectNet. [DINOv3](https://arxiv.org/html/2508.10104)
- Apple consiglia immagini "da angolazioni diverse e con luci diverse" e simili a quelle d'uso, e un insieme di prova
  separato. [Create ML](https://developer.apple.com/documentation/createml/creating-an-image-classifier-model)
- ML Kit: caratteri di almeno 16×16 pixel; la sfocatura riduce l'accuratezza; chiedere di rifare la foto se il
  risultato non è accettabile. [ML Kit text v2 Android](https://developers.google.com/ml-kit/vision/text-recognition/v2/android)
- Le reti sono mal calibrate: la confidenza va tarata su dati separati. [Guo et al.](https://arxiv.org/abs/1706.04599)

### DEDUZIONI: come misurare prima di decidere

- **Insieme di prova separato**: foto di query fatte in giorni diversi, da persone diverse, con telefoni diversi,
  **mai** usate come riferimento. Articoli scelti apposta tra i più simili tra loro, più un gruppo di articoli **non** a
  catalogo per misurare il rifiuto.
- **Metriche**: top-1, top-5, matrice di confusione per gruppi di articoli simili, tasso di "non so" e tasso di errore
  tra le risposte date (curva errore-copertura al variare della soglia), tempo per identificazione.
- **Postazione fissa vs mano libera**: una postazione con sfondo e luce costanti riduce la variabilità (coerente con
  ObjectNet); per le foto di riferimento all'inserimento conviene una procedura guidata (fronte, lato, etichetta).
  A mano libera servono più foto di riferimento e più varietà.
- Ritaglio: la foto contiene scaffale e mani; un ritaglio centrale guidato (riquadro a schermo) è la soluzione più
  semplice; un rilevatore di scatole solo se le misure lo richiedono (IPOTESI).

## Tabella riassuntiva

| Strada | Dati necessari | Sforzo | Quando conviene |
|---|---|---|---|
| Barcode (ML Kit/Vision; zxing-cpp nel web) | nessuno | basso | sempre, primo tentativo |
| OCR codice + confronto con elenco codici | elenco codici del catalogo | basso-medio | etichette stampate leggibili |
| Encoder congelato + k-NN esatto | 3-5 foto per articolo (IPOTESI) | basso | punto di partenza del riconoscimento visivo |
| + prototipi / proposta top-5 all'operatore | stesse foto | basso | quando il top-1 non basta ma il top-5 sì |
| + ciclo di conferma (foto confermate nell'archivio) | si accumulano con l'uso | medio (interfaccia, revisione) | da subito, migliora col tempo |
| Linear probe / classificatore chiuso | ≥10 foto per classe (Apple, per classificatori) | medio | sconsigliato: catalogo che cambia |
| Metric learning / LoRA / fine-tuning parziale | migliaia di foto con coppie simili (IPOTESI) | medio-alto, GPU per addestrare | se le misure mostrano confusioni sistematiche tra simili |
| Modello sul telefono (ONNX/Core ML/LiteRT) | come sopra + sincronizzazione | alto | lavoro senza rete, risposta durante l'inquadratura |
| VLM locale (llama.cpp/Ollama) | nessuno | medio, hardware pesante | solo casi secondari (etichette difficili), non per scegliere tra 35.000 |

## Percorso consigliato (DEDUZIONE)

1. **Barcode** sul telefono (ML Kit/Vision o, nel web, BarcodeDetector + zxing-cpp WASM).
2. **OCR del codice** confrontato con l'elenco dei codici a catalogo.
3. **Prova di fattibilità visiva senza addestramento** sul server in sede: DINOv2 ViT-S e ViT-B (Apache 2.0), SigLIP 2
   base (Apache 2.0) e, se la licenza è accettata, DINOv3 ViT-S/B; ONNX Runtime su CPU; NumPy/FAISS flat. Su 100-300
   articoli scelti tra i più simili, con 3-5 foto di riferimento e un insieme di prova separato. Misurare top-1, top-5,
   tempi.
4. **Interfaccia a candidati** (primi 3-5) con soglia di "non so" tarata sulla prova; **ciclo di conferma** che aggiunge
   le foto confermate e quelle identificate da barcode/OCR.
5. Se le misure lo giustificano: **metric learning** su encoder pre-addestrato (fine-tuning parziale o LoRA) usando le
   correzioni raccolte come negativi difficili; ricalcolare gli embedding dell'archivio.
6. Solo se serve lavorare senza rete o in tempo reale: **modello sul telefono**, con quantizzazione misurata e indice
   sincronizzato.

## Cosa resta incerto

- **Accuratezza reale** sui nostri articoli: nessuno studio pubblicato riproduce lo scenario (foto da telefono, stessi
  ambienti, 35.000 articoli simili). Cat2Real è il riferimento più vicino ma ha una differenza di dominio maggiore.
- **Quante foto di riferimento** servono per articolo con il k-NN: non ho trovato una regola pubblicata.
- **Tempi** di DINOv2/DINOv3 ViT-S/B su telefoni Android attuali, PC senza GPU e mini-PC: nessuna misura primaria
  trovata; le misure disponibili sono su iPhone 12 e Pixel 1-3.
- **Effetto di int8/fp16 sul recupero** con encoder ViT: non documentato; misurato solo per MobileNet in classificazione.
- **Licenza DINOv3**: il testo non esclude l'uso commerciale, ma clausole (modifiche unilaterali, ITAR, redistribuzione
  dei derivati) vanno valutate da chi decide; non è un parere legale.
- **iOS PWA**: persistenza del permesso fotocamera ancora aperta su WebKit; il comportamento può cambiare con le
  versioni di iOS.
- **MediaPipe Model Maker**: sembra fermo (ultimo rilascio 2024), ma non ho trovato un avviso ufficiale di dismissione.
- Le affermazioni di accuratezza di PaddleOCR vengono dal README del produttore, non da una valutazione indipendente.
- Dimensioni degli embedding (384/768/1024) e licenza di NumPy: dalla memoria, non verificate in questa ricerca.

## Fonti

Articoli
- DINOv2 — https://arxiv.org/abs/2304.07193 ; testo: https://arxiv.org/html/2304.07193v2
- DINOv3 — https://arxiv.org/abs/2508.10104 ; testo: https://arxiv.org/html/2508.10104
- SigLIP 2 — https://arxiv.org/abs/2502.14786
- CLIP — https://arxiv.org/pdf/2103.00020
- Cat2Real (2026) — https://arxiv.org/html/2607.09888
- Grocery embedding + K-NN (2019) — https://arxiv.org/pdf/1902.00760
- A Metric Learning Reality Check — https://arxiv.org/abs/2003.08505
- Open-Set Recognition: a Good Closed-Set Classifier is All You Need — https://arxiv.org/abs/2110.06207
- On Calibration of Modern Neural Networks — https://arxiv.org/abs/1706.04599
- EfficientFormer (tempi iPhone 12) — https://arxiv.org/pdf/2206.01191v5
- MobileNetV3 (tempi Pixel, int8) — https://arxiv.org/pdf/1905.02244v5
- ObjectNet — https://objectnet.dev/

Repository, licenze, registri
- DINOv2 — https://github.com/facebookresearch/dinov2
- DINOv3 — https://github.com/facebookresearch/dinov3 ; licenza: https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md
- Model card: https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m ; https://huggingface.co/google/siglip2-base-patch16-224
- File LICENSE (raw.githubusercontent.com) di: label-studio, cvat, fiftyone, pytorch-image-models, transformers,
  ultralytics, mediapipe, LiteRT, pytorch-metric-learning, peft, faiss, hnswlib, usearch, sqlite-vec, pgvector,
  lancedb, qdrant, onnxruntime, executorch, openvino, TensorRT, ncnn, transformers.js, llama.cpp, ollama, zxing,
  zxing-cpp, PaddleOCR, tesseract.js, coremltools (link nelle tabelle sopra)
- Versioni: PyPI (https://pypi.org/project/<nome>/) e npm (https://www.npmjs.com/package/<nome>), consultati il 15/11/2026
- Ultralytics licenze — https://www.ultralytics.com/license
- FAISS, scelta dell'indice — https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index

Documentazione ufficiale
- PEFT LoRA — https://huggingface.co/docs/peft/main/en/task_guides/image_classification_lora
- ONNX Runtime EP — https://onnxruntime.ai/docs/execution-providers/ ; Web — https://onnxruntime.ai/docs/tutorials/web/ ;
  quantizzazione — https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html
- Transformers.js WebGPU — https://huggingface.co/docs/transformers.js/guides/webgpu
- LiteRT — https://developers.google.com/edge/litert/overview
- MediaPipe Image Classifier — https://developers.google.com/edge/mediapipe/solutions/customization/image_classifier
- ExecuTorch backend — https://docs.pytorch.org/executorch/stable/backends-overview.html
- coremltools ottimizzazione — https://apple.github.io/coremltools/docs-guides/source/opt-overview.html
- Android NNAPI deprecato — https://developer.android.com/ndk/guides/neuralnetworks/migration-guide
- ML Kit barcode — https://developers.google.com/ml-kit/vision/barcode-scanning ; testo — https://developers.google.com/ml-kit/vision/text-recognition/v2 ;
  Android — https://developers.google.com/ml-kit/vision/text-recognition/v2/android
- Apple: Create ML — https://developer.apple.com/documentation/createml/creating-an-image-classifier-model ;
  Vision e VisionKit — link nella sezione G
- MDN getUserMedia — https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia ;
  Secure Contexts — https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts
- MDN browser-compat-data (BarcodeDetector, GPU, MediaDevices) — https://github.com/mdn/browser-compat-data
- Let's Encrypt — https://letsencrypt.org/docs/challenge-types/
- WebKit bug 280394 — https://bugs.webkit.org/show_bug.cgi?id=280394
- NVIDIA Jetson benchmarks — https://developer.nvidia.com/embedded/jetson-benchmarks

Non raggiungibili o non leggibili
- Pagina benchmark OpenVINO (https://docs.openvino.ai/2026/about-openvino/performance-benchmarks.html): contenuto
  dinamico, dati non estratti.
- API GitHub bloccata in questa sessione: licenze lette dai file LICENSE grezzi, versioni da PyPI/npm.
- Pagine Apple Developer lette tramite l'endpoint JSON ufficiale della documentazione (la pagina HTML è dinamica).
