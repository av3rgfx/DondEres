# Modelli visivi per riconoscere gli articoli in arrivo

Data: 15/11/2026

## Domanda

Quali modelli visivi pronti sono adatti, tra quali famiglie di approccio scegliere, e quale raccomandare per
identificare il **tipo** di articolo (voce di catalogo, SKU) quando un operatore inquadra la scatola con il telefono
(Android e iOS; in secondo luogo un computer con telecamera), tutto **in locale** sulla rete aziendale, con un
catalogo fino a 35.000 articoli molto somiglianti tra loro e con l'aggiunta di articoli nuovi **senza riaddestrare**?

Ordine di identificazione già deciso: barcode → codice stampato sull'etichetta (OCR) → riconoscimento visivo.

## Come leggere questo documento

- **FATTO**: preso da una fonte primaria, con il link accanto. Le pagine sono state aperte il 15/11/2026.
- **DEDUZIONE**: ragionamento mio a partire dai fatti. Può essere sbagliato.
- **IPOTESI**: da verificare con prove sui dati reali.
- **Non verificato**: viene dalla mia memoria e non l'ho ritrovato su una fonte primaria.
- Le licenze sono riassunte da me: non sono un parere legale. Prima di un uso commerciale vanno lette da chi
  decide per l'azienda.

Parole usate spesso:
- **Embedding**: una lista di numeri che riassume l'aspetto di un'immagine. Due foto dello stesso articolo danno
  liste vicine; si confrontano con una ricerca "per somiglianza".
- **Encoder**: il modello che trasforma la foto nell'embedding.
- **Classificatore chiuso**: modello addestrato su un elenco fisso di classi; per aggiungere una classe va
  riaddestrato.
- **Rilevatore (detector)**: modello che trova dove si trova un oggetto nella foto e lo racchiude in un riquadro.
- **VLM**: modello che guarda un'immagine e risponde a domande in testo (vision-language model).
- **Pesi**: il file del modello addestrato. La licenza dei pesi può essere diversa da quella del codice.

## Sintesi

1. Per il terzo stadio (riconoscimento visivo) l'approccio adatto è **embedding + ricerca per somiglianza**: si
   salvano gli embedding delle foto di ogni articolo e si cerca il più vicino. Aggiungere un articolo vuol dire
   aggiungere le sue foto all'indice, senza riaddestrare. Un classificatore chiuso su 35.000 classi che cambiano
   non si presta (DEDUZIONE).
2. Su un banco di prova pubblico di riconoscimento di oggetti specifici (ILIAS), tra gli encoder "congelati" i
   migliori sono **DINOv3-L**, **Perception Encoder L** e **SigLIP 2-L**; DINOv2 e CLIP stanno sotto
   ([ILIAS](https://vrg.fel.cvut.cz/ilias/)).
3. Le licenze cambiano la scelta: **SigLIP 2, Perception Encoder (PE-Core), DINOv2** sono Apache-2.0;
   **DINOv3** ha una licenza propria con accesso su richiesta; **MobileCLIP/MobileCLIP2 e FastVLM** (Apple) sono
   solo per ricerca non commerciale; **DEIMv2** è non commerciale; **Ultralytics YOLO** è AGPL-3.0 o a pagamento.
4. Barcode e OCR sul telefono si fanno con gli strumenti di sistema già pronti e locali: **ML Kit** (Android, anche
   iOS) e **Apple Vision** (iOS). Sul server o sul computer: **zxing-cpp** e **PaddleOCR (PP-OCRv6)**, Apache-2.0.
5. I VLM piccoli (Gemma 4 E2B/E4B, Qwen3.5 2B/4B, Apache-2.0) servono per **proporre** codice e descrizione quando
   si inserisce un articolo nuovo, con conferma umana; non per decidere l'identità (DEDUZIONE).
6. Raccomandazione (DEDUZIONE): barcode e OCR sul telefono; riconoscimento visivo su un server in sede con
   **SigLIP 2 o PE-Core** come primi candidati (DINOv3 se la licenza viene accettata), indice vettoriale semplice,
   e sempre una **rosa di 3-5 proposte** che l'operatore conferma. Prima della scelta finale serve una prova sulle
   foto reali del magazzino.

---

## 1. Encoder "foundation" per embedding e ricerca per somiglianza

### Perché questa famiglia

- FATTO: nel banco di prova ILIAS (1.000 oggetti specifici, 100 milioni di immagini di disturbo) i modelli
  affinati su un solo dominio (per esempio solo prodotti) vanno bene in quel dominio ma male in generale; un
  semplice strato lineare addestrato sopra l'encoder migliora i risultati; il riordino con descrittori locali
  resta importante con sfondi molto ingombri ([arXiv 2502.11748](https://arxiv.org/abs/2502.11748)).
- DEDUZIONE: per un catalogo che cresce, un encoder generico usato così com'è, eventualmente con un piccolo
  adattamento sui propri dati, è il punto di partenza giusto. Aggiungere un articolo = calcolare l'embedding delle
  sue foto e salvarlo.

### Risultati comparativi (ILIAS, encoder congelati)

FATTO, dalla classifica pubblicata dagli autori ([ILIAS](https://vrg.fel.cvut.cz/ilias/)), metrica mAP@1k
immagine-contro-immagine (più alto è meglio), su 100M di immagini di disturbo:

| Modello | Risoluzione (addestr./prova) | ILIAS 100M |
|---|---|---|
| DINOv3-L | 768 / 768 | 26,5 |
| DINOv3-B | 768 / 768 | 22,0 |
| PE-L@336 | 336 / 512 | 22,0 |
| SigLIP2-L@512 | 512 / 724 | 20,8 |
| SigLIP2-B@512 | 512 / 724 | 15,4 |
| DINOv2-L | 518 / 724 | 15,3 |
| DINOv2-B | 518 / 724 | 11,5 |
| OpenCLIP-ViT-L | 224 / 384 | 9,4 |
| OAI-CLIP-B | 224 / 384 | 4,2 |

- FATTO: con un adattamento lineare i valori salgono (DINOv3-L 28,3; SigLIP2-L@512 31,3; PE-L@336 33,4) e con il
  riordino si arriva a 38,9 (AMES + SigLIP adattato) ([ILIAS](https://vrg.fel.cvut.cz/ilias/)).
- FATTO: il valore di PE-B è 20,2 su 5M ma 9,7 su 100M; lo scarto è insolito e va verificato
  ([ILIAS](https://vrg.fel.cvut.cz/ilias/)).
- DEDUZIONE: ILIAS non è un catalogo di magazzino. Lì la galleria è enorme e gli oggetti molto vari; da noi la
  galleria è piccola (35.000 articoli) ma gli articoli si somigliano molto. La classifica indica quali famiglie
  provare per prime, non quale vincerà sulle nostre scatole.

### Schede dei modelli

**DINOv3 (Meta)**
- FATTO: varianti ViT-S/16 distillato 21M parametri, S+/16 29M, B/16 86M, L/16 300M, H+/16 840M, 7B/16 6.716M;
  anche ConvNeXt Tiny 29M, Small 50M, Base 89M, Large 198M
  ([repo](https://github.com/facebookresearch/dinov3)).
- FATTO: "DINOv3 code and model weights are released under the DINOv3 License"; i pesi si ottengono dopo una
  richiesta via modulo ([repo](https://github.com/facebookresearch/dinov3)); anche su Hugging Face sono ad accesso
  manuale (campo `gated: manual` nell'API di Hugging Face per `facebook/dinov3-vits16-pretrain-lvd1689m`).
- FATTO: la licenza concede un diritto "non-exclusive, worldwide, non-transferable and royalty-free limited" di
  usare, distribuire e modificare; vieta usi militari, nucleari, di spionaggio e soggetti a ITAR; chi ridistribuisce
  deve allegare la licenza; Meta può aggiornare l'accordo
  ([LICENSE.md](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md)).
- DEDUZIONE: il testo non limita l'uso alla ricerca, quindi sembra ammettere l'uso commerciale, ma non è Apache e
  richiede accettazione e revisione.
- FATTO: si carica con PyTorch Hub, Transformers (da 4.56.0) e timm (da 1.0.20); la pagina non cita ONNX
  ([repo](https://github.com/facebookresearch/dinov3)).
- Dove gira (DEDUZIONE): S/16 e B/16 sono di taglia compatibile con un telefono dopo conversione; L/16 a 768 px è da
  server.

**DINOv2 (Meta)**
- FATTO: "DINOv2 code and model weights are released under the Apache License 2.0"; ViT-S/14 21M, B/14 86M,
  L/14 300M, g/14 1.100M; ImageNet k-NN 79,0% (S) fino a 83,5% (g)
  ([repo](https://github.com/facebookresearch/dinov2)).
- FATTO: le varianti Cell-DINO e XRay-DINO hanno licenze non commerciali (non servono qui)
  ([repo](https://github.com/facebookresearch/dinov2)).
- DEDUZIONE: è la scelta con la licenza più tranquilla e molto materiale d'uso, ma su ILIAS rende meno di SigLIP 2,
  PE e DINOv3 a pari taglia.

**SigLIP 2 (Google)**
- FATTO: quattro taglie: ViT-B 86M, L 303M, So400m 400M, g 1B; varianti che accettano più risoluzioni e mantengono
  le proporzioni dell'immagine (NaFlex) ([arXiv 2502.14786](https://arxiv.org/abs/2502.14786)).
- FATTO: licenza Apache-2.0 sul model card
  ([HF siglip2-base-patch16-naflex](https://huggingface.co/google/siglip2-base-patch16-naflex)); pesi non ad accesso
  riservato (API di Hugging Face).
- FATTO: supportato in OpenCLIP ([repo](https://github.com/mlfoundations/open_clip)).
- Nota: è un modello immagine+testo, quindi permette anche la ricerca "da testo a immagine" (utile per cercare un
  articolo scrivendone la descrizione) (DEDUZIONE).

**Perception Encoder, PE-Core (Meta)**
- FATTO: configurazioni T/16 384 px, S/16 384 px, B/16 224 px, L/14 336 px, G/14 448 px; zero-shot ImageNet 62,1 (T),
  72,7 (S), 78,4 (B), 83,5 (L), 85,4 (G) ([repo](https://github.com/facebookresearch/perception_models)).
- FATTO: codice Apache-2.0, pesi PE con licenza Apache 2.0; i pesi del modello PLM (un VLM) hanno invece una "FAIR
  Research License" ([repo](https://github.com/facebookresearch/perception_models)); il model card di PE-Core-S16-384
  indica Apache-2.0 e nessun accesso riservato ([HF](https://huggingface.co/facebook/PE-Core-S16-384)).
- FATTO: torri visive B/16 0,09B, L/14 0,32B, G/14 1,88B parametri ([HF](https://huggingface.co/facebook/PE-Core-S16-384)).
- FATTO: integrato in timm e OpenCLIP ([repo](https://github.com/facebookresearch/perception_models),
  [open_clip](https://github.com/mlfoundations/open_clip)).

**CLIP / OpenCLIP**
- FATTO: codice OpenCLIP con licenza MIT ([LICENSE](https://github.com/mlfoundations/open_clip/blob/main/LICENSE));
  la licenza dei pesi dipende dal singolo modello e va letta sul suo model card
  ([repo](https://github.com/mlfoundations/open_clip)).
- FATTO: su ILIAS i CLIP stanno sotto SigLIP, PE e DINOv3 ([ILIAS](https://vrg.fel.cvut.cz/ilias/)).
- FATTO: gli errori visivi tipici dei VLM sono legati al fatto che l'encoder CLIP considera simili immagini con
  differenze visive chiare ("CLIP-blind pairs") ([arXiv 2401.06209](https://arxiv.org/abs/2401.06209)).
- DEDUZIONE: OpenCLIP è utile come libreria per caricare SigLIP 2 e PE, meno come scelta di pesi.

**MobileCLIP / MobileCLIP2 (Apple)**
- FATTO: MobileCLIP2-S0 11,4M (immagine) + 63,4M (testo) con 1,5 ms per l'immagine; MobileCLIP2-S2 35,7M, 3,6 ms,
  77,2% zero-shot ImageNet; MobileCLIP2-B 86,3M, 10,4 ms, 79,4%; la misura di S4 è dichiarata su iPhone 12 Pro Max
  ([repo](https://github.com/apple/ml-mobileclip)).
- FATTO: codice MIT, ma i modelli sono sotto "Apple ML Research Model TOU": licenza concessa "exclusively for Research
  Purposes", definite come "non-commercial scientific research", con esclusione esplicita di "any commercial
  exploitation, product development or use in any commercial product or service"
  ([LICENSE_MODELS](https://github.com/apple/ml-mobileclip/blob/main/LICENSE_MODELS)); su Hugging Face la licenza è
  `apple-amlr`.
- DEDUZIONE: tecnicamente ideali per il telefono, ma **non usabili** in un gestionale commerciale.

**Altre famiglie recenti trovate (verificate solo la licenza e la taglia)**
- TIPS v1 (Google): S/14 con torre visiva 22M a 448 px, fino a g/14 1,1B; licenza Apache-2.0
  ([HF tipsv1-s14](https://huggingface.co/google/tipsv1-s14)). Non compare nella classifica ILIAS consultata.
- EUPE ViT-T/S (Meta, marzo 2026) e MoEViE (Meta, agosto 2026): licenze rispettivamente
  `fair-noncommercial-research-license` e `cc-by-nc-4.0` (campo licenza dell'API di Hugging Face per
  [EUPE-ViT-S](https://huggingface.co/facebook/EUPE-ViT-S) e
  [MoEViE-B16-224](https://huggingface.co/facebook/MoEViE-B16-224)): **non commerciali**.
- Mage-ViT (Microsoft, luglio 2026): 316M parametri, licenza MIT ([HF](https://huggingface.co/microsoft/Mage-ViT));
  non ho letto il model card né risultati.

### Dove salvare gli embedding

- FATTO: FAISS ha licenza MIT ([LICENSE](https://github.com/facebookresearch/faiss/blob/main/LICENSE)), USearch
  Apache-2.0 ([LICENSE](https://github.com/unum-cloud/usearch/blob/main/LICENSE)), pgvector la licenza PostgreSQL
  ([LICENSE](https://github.com/pgvector/pgvector/blob/master/LICENSE)).
- DEDUZIONE (conto): 35.000 articoli × 5 foto × 768 numeri × 2 byte ≈ 270 MB. Un confronto esaustivo su questa
  quantità è fattibile su un server normale; non serve un indice approssimato complesso.

---

## 2. Classificatori leggeri da affinare

- FATTO: MobileNetV4 è pensato per CPU, GPU, DSP e acceleratori mobili, compresi Apple Neural Engine e Pixel EdgeTPU;
  la variante Hybrid-Large dichiara 87% su ImageNet-1K con 3,8 ms su Pixel 8 EdgeTPU
  ([arXiv 2404.10518](https://arxiv.org/abs/2404.10518)).
- FATTO: `mobilenetv4_conv_medium` in timm: 9,7M parametri, 1,1 GMAC, 256 px in addestramento e 320 px in prova,
  80,9% top-1 a 320 px, licenza Apache-2.0; con `num_classes=0` restituisce un embedding invece della classe
  ([HF timm](https://huggingface.co/timm/mobilenetv4_conv_medium.e500_r256_in1k)).
- FATTO: timm ha licenza Apache-2.0 ([LICENSE](https://github.com/huggingface/pytorch-image-models/blob/main/LICENSE)).
- FATTO: ConvNeXt V2: codice MIT, ma i modelli pre-addestrati e affinati su ImageNet sono CC-BY-NC
  ([README](https://github.com/facebookresearch/ConvNeXt-V2)) → **non commerciali**.
- FATTO: FastViT (Apple) usa la licenza di esempio Apple, che concede uso, modifica e ridistribuzione
  ([LICENSE](https://github.com/apple/ml-fastvit/blob/main/LICENSE)). Non ho verificato la licenza dei pesi
  pubblicati in timm per FastViT.
- EfficientNet: non verificato in questa ricerca.

**Perché un classificatore chiuso è poco adatto qui** (DEDUZIONE):
- con 35.000 classi l'ultimo strato diventa grande e ogni articolo nuovo richiede un nuovo addestramento, mentre il
  requisito è aggiungerlo con una foto e basta;
- per molti articoli ci saranno poche foto (anche una sola all'inserimento): troppo poche per addestrare bene una
  classe;
- un classificatore sceglie sempre una delle classi note: per un articolo non ancora a catalogo dà comunque una
  risposta sicura e sbagliata, mentre con la ricerca per somiglianza si può fissare una soglia di distanza e dire
  "nessun articolo noto".
- Uso sensato dei classificatori: come encoder leggero (togliendo l'ultimo strato) o per compiti piccoli e fissi,
  per esempio "c'è una scatola / un'etichetta nell'inquadratura?".

---

## 3. Rilevatori per isolare la scatola o l'etichetta

**Ultralytics YOLO**
- FATTO: YOLO26 uscito a gennaio 2026; YOLO26n 2,4M parametri, 40,9 mAP COCO, 38,9 ms su CPU con ONNX; YOLO26s 9,5M,
  48,6 mAP; esportazione verso TensorRT, ONNX, CoreML, LiteRT, OpenVINO
  ([docs YOLO26](https://docs.ultralytics.com/models/yolo26/)).
- FATTO: YOLO27 è annunciato ma non disponibile ("Join the waitlist. Coming soon")
  ([licenza Ultralytics](https://www.ultralytics.com/license)).
- FATTO: codice AGPL-3.0 ([LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)); secondo
  Ultralytics "All Ultralytics YOLO trained models fall under the AGPL-3.0 License by default", anche quelli affinati;
  per prodotti commerciali chiusi, strumenti interni non pubblicati e servizi in rete serve la Enterprise License a
  pagamento ([licenza Ultralytics](https://www.ultralytics.com/license)).
- DEDUZIONE: tecnicamente comodo, ma impone di pubblicare tutto il codice del gestionale o di pagare una licenza.

**Alternative con licenza permissiva**
- RF-DETR (Roboflow): codice Apache-2.0; pesi di rilevamento Nano (30,5M, 384 px, 48,4 mAP, 2,3 ms su T4), Small,
  Medium, Large Apache-2.0; le taglie Atto, Femto, Pico, XL, 2XL sono sotto "PML 1.0", che per l'installazione
  commerciale in proprio richiede un componente Enterprise; tutti i modelli di segmentazione sono Apache-2.0
  ([repo](https://github.com/roboflow/rf-detr)).
- D-FINE e DEIM (prima versione): Apache-2.0 ([D-FINE LICENSE](https://github.com/Peterande/D-FINE/blob/master/LICENSE),
  [DEIM LICENSE](https://github.com/ShihuaHuang95/DEIM/blob/main/LICENSE)).
- RT-DETR (repo dell'autore): Apache-2.0 ([LICENSE](https://github.com/lyuwenyu/RT-DETR/blob/main/LICENSE)).
- YOLOX: Apache-2.0 ([LICENSE](https://github.com/Megvii-BaseDetection/YOLOX/blob/main/LICENSE)).
- RTMDet (in MMDetection): Apache-2.0 ([LICENSE MMDetection](https://github.com/open-mmlab/mmdetection/blob/main/LICENSE)).
- **Attenzione** DEIMv2: modelli da 0,5M a 50,3M parametri, esportazione ONNX/TensorRT, ma la "DEIMv2 License"
  concede diritti "solely for Non-Commercial Purposes" e "No rights are granted for Commercial Use"
  ([repo](https://github.com/Intellindust-AI-Lab/DEIMv2), [LICENSE.md](https://github.com/Intellindust-AI-Lab/DEIMv2/blob/main/LICENSE.md)).

DEDUZIONE: un rilevatore va affinato su poche classi fisse ("scatola", "etichetta", "barcode"). Serve a ritagliare
la zona utile prima dell'embedding o dell'OCR, riducendo l'effetto dello sfondo (che ILIAS indica come problema). È
un miglioramento, non un requisito del primo prototipo.

---

## 4. Rilevamento e segmentazione a vocabolario aperto

Questi modelli trovano oggetti descritti a parole ("cardboard box", "label") senza addestramento specifico.

- Grounding DINO (originale): Apache-2.0 ([LICENSE](https://github.com/IDEA-Research/GroundingDINO/blob/main/LICENSE)).
  Le versioni 1.5 e 1.6 sono offerte tramite API su cloud con token
  ([Grounding-DINO-1.5-API](https://github.com/IDEA-Research/Grounding-DINO-1.5-API)): **non usabili in locale**.
- OWLv2 (Google): base 0,2B parametri, Apache-2.0, descritto come "research output"
  ([HF](https://huggingface.co/google/owlv2-base-patch16-ensemble)). Non verificato: la ricerca guidata da
  un'immagine di esempio è disponibile nell'implementazione Transformers.
- YOLO-World: GPL-3.0 ([LICENSE](https://github.com/AILab-CVC/YOLO-World/blob/master/LICENSE)).
- YOLOE: testo, esempio visivo o nessun suggerimento; YOLOE-v8-L 35,9 AP su LVIS con testo; esportazione ONNX e
  CoreML; costruito sul codice Ultralytics; licenza AGPL-3.0 ([repo](https://github.com/THU-MIG/yoloe)).
- SAM 3 (Meta): segmenta tutte le istanze di un concetto da una frase o da esempi; 848M parametri; richiede GPU CUDA
  12.6+; pesi ad accesso riservato; SAM 3.1 uscito il 27/03/2026 ([repo](https://github.com/facebookresearch/sam3)).
  Licenza "SAM License" (aggiornata al 19/11/2025): diritto non esclusivo, gratuito, di usare, distribuire e
  modificare, con divieti per usi militari e soggetti a ITAR
  ([LICENSE](https://github.com/facebookresearch/sam3/blob/main/LICENSE)).
- SAM 2: Apache-2.0 ([LICENSE](https://github.com/facebookresearch/sam2/blob/main/LICENSE)).
- MobileSAM: Apache-2.0 ([LICENSE](https://github.com/ChaoningZhang/MobileSAM/blob/master/LICENSE)).

DEDUZIONE: in produzione la scatola è quasi sempre l'oggetto principale dell'inquadratura, quindi un rilevatore
chiuso e piccolo basta. Questi modelli sono più utili **in fase di preparazione**: per ritagliare automaticamente
le foto quando si costruisce il catalogo o per pre-etichettare i dati con cui affinare il rilevatore. SAM 3 è da
server con GPU.

---

## 5. VLM piccoli in locale

| Modello | Parametri | Licenza | Note dalla fonte |
|---|---|---|---|
| Gemma 4 E2B / E4B | 2,3B / 4,5B "effettivi" (5,1B / 8B con embedding) | Apache 2.0 | pensati per telefoni e portatili; budget di token visivi 70-1120, quelli alti per OCR e testo piccolo ([HF](https://huggingface.co/google/gemma-4-E2B-it)) |
| Qwen3.5-2B (anche 0,8B, 4B, 9B) | 2,27B | Apache-2.0 | OCRBench 85,4 (2B); il 2B in modalità "thinking" può entrare in cicli; suggerito per prototipi e affinamento ([HF](https://huggingface.co/Qwen/Qwen3.5-2B)) |
| Qwen3-VL-2B / 4B | 2,13B / 4,44B | Apache-2.0 | (API di Hugging Face per [2B](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) e [4B](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)) |
| SmolVLM2 256M / 500M / 2.2B | fino a ~2B | Apache 2.0 | 2.2B: OCRBench 72,9; circa 5,2 GB di memoria GPU per video; avverte che può produrre contenuti "that appear factual but may not be accurate" ([HF](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct)) |
| Florence-2 base / large | 0,23B / 0,77B | MIT | compiti OCR, OCR con regioni, didascalie, rilevamento ([HF](https://huggingface.co/microsoft/Florence-2-base)) |
| PaliGemma 2 3B | 3,03B | Gemma Terms, accesso su richiesta | (API di Hugging Face per [paligemma2-3b-pt-224](https://huggingface.co/google/paligemma2-3b-pt-224)) |
| Gemma 3n E2B | 5,4B totali | Gemma Terms, accesso su richiesta | (API di Hugging Face per [gemma-3n-E2B-it](https://huggingface.co/google/gemma-3n-E2B-it)) |
| Moondream 3 (preview) | 9B totali, 2B attivi | BSL 1.1 con concessione aggiuntiva: uso interno anche in produzione sì, prodotti in concorrenza con M87 Labs no | richiede GPU CUDA negli esempi ([HF](https://huggingface.co/moondream/moondream3-preview)); Moondream 3.1 (giugno 2026) ha la "moondream-model-license-1.0", non letta |
| Moondream 2 | 1,93B | Apache-2.0 | (API di Hugging Face per [moondream2](https://huggingface.co/vikhyatk/moondream2)) |
| FastVLM 0.5B / 1.5B / 7B | 0,5-7B | modelli solo ricerca non commerciale | app dimostrativa per iPhone/iPad/Mac ([repo](https://github.com/apple/ml-fastvlm), [LICENSE_MODEL](https://github.com/apple/ml-fastvlm/blob/main/LICENSE_MODEL)) |
| PaddleOCR-VL-1.6 | 0,9B | Apache 2.0 (PaddleOCR) | specializzato nella lettura di documenti, 96,3% su OmniDocBench v1.6 ([repo](https://github.com/PaddlePaddle/PaddleOCR)) |

Limiti (FATTI): i VLM fanno errori visivi sistematici su coppie di immagini diverse che l'encoder vede come simili,
e danno spiegazioni inventate ([arXiv 2401.06209](https://arxiv.org/abs/2401.06209)); i model card di SmolVLM2 e
Qwen3.5 avvertono di risposte non accurate e di cicli di generazione (link in tabella).

DEDUZIONI:
- Un VLM **non** è adatto a scegliere tra 35.000 articoli simili: non conosce il catalogo, è lento (genera testo
  parola per parola) e può inventare un codice plausibile.
- È utile **all'inserimento di un articolo nuovo**: legge l'etichetta, propone codice, descrizione, marca, misure;
  l'operatore corregge e conferma. Può anche fare da OCR di riserva quando quello classico fallisce, purché il
  codice letto venga poi **verificato contro il catalogo**.
- Gemma 4 E2B e Qwen3.5-2B sono di taglia da telefono di fascia alta, ma la via più semplice è eseguirli sul server
  in sede (IPOTESI da provare: tempi di risposta accettabili su una GPU singola).

---

## 6. OCR e barcode in locale

### Barcode

- **ML Kit Barcode Scanning** (Google, Android e iOS): "performed completely on the device, and doesn't require a
  network connection"; formati Codabar, Code 39, Code 93, Code 128, EAN-8, EAN-13, ITF, UPC-A, UPC-E, Aztec, Data
  Matrix, PDF417, QR; ITF sotto 6 caratteri è instabile; massimo 10 codici per chiamata
  ([ML Kit](https://developers.google.com/ml-kit/vision/barcode-scanning)).
  Requisiti: l'unità più piccola del codice ≥ 2 pixel; un EAN-13 ≥ 190 pixel di larghezza; risoluzione consigliata
  1280×720 o 1920×1080; modello incluso nell'app circa 2,4 MB, oppure circa 200 KB scaricato da Google Play Services
  ([guida Android](https://developers.google.com/ml-kit/vision/barcode-scanning/android)).
- **Apple Vision** (iOS/macOS): simbologie supportate tra cui Aztec, Codabar, Code 39/93/128, Data Matrix, EAN-8,
  EAN-13, GS1 DataBar (anche Expanded e Limited), ITF-14, I2of5, MicroPDF417, MicroQR, MSI Plessey, PDF417, QR,
  UPC-E ([VNBarcodeSymbology](https://developer.apple.com/documentation/vision/vnbarcodesymbology)). VisionKit
  `DataScannerViewController` (da iOS 16) legge testo e codici dal video live della fotocamera
  ([DataScannerViewController](https://developer.apple.com/documentation/visionkit/datascannerviewcontroller)).
- **zxing-cpp**: Apache-2.0, involucri per Android, iOS, Python, WebAssembly, .NET e altri; supporta anche DataBar
  ([repo](https://github.com/zxing-cpp/zxing-cpp), [LICENSE](https://github.com/zxing-cpp/zxing-cpp/blob/master/LICENSE)).
  DEDUZIONE: è la scelta per il computer con telecamera (nel browser via WebAssembly) e per il server.
- **ZXing (Java)**: "Project in Maintenance Mode Only", nessuno sviluppo attivo ([README](https://github.com/zxing/zxing)).
- **ZBar**: LGPL 2.1 o successiva ([COPYING](https://github.com/mchehab/zbar/blob/master/COPYING)).

### OCR per codici alfanumerici brevi

- **ML Kit Text Recognition v2** (Android e iOS): script latino, cinese, devanagari, giapponese, coreano;
  restituisce blocchi, righe, parole e singoli caratteri con riquadro e punteggio di confidenza
  ([ML Kit](https://developers.google.com/ml-kit/vision/text-recognition/v2)); ogni carattere idealmente ≥ 16×16
  pixel, oltre 24×24 nessun vantaggio; modello incluso circa 4 MB per script e architettura
  ([guida Android](https://developers.google.com/ml-kit/vision/text-recognition/v2/android)).
- **Apple Vision** `RecognizeTextRequest` (iOS 18, macOS 15) ([doc](https://developer.apple.com/documentation/vision/recognizetextrequest));
  `customWords` aggiunge parole che hanno la precedenza sul lessico standard
  ([doc](https://developer.apple.com/documentation/vision/vnrecognizetextrequest/customwords));
  `usesLanguageCorrection` disattivato restituisce il riconoscimento grezzo
  ([doc](https://developer.apple.com/documentation/vision/vnrecognizetextrequest/useslanguagecorrection)).
  DEDUZIONE: per codici come "A10-0O1I" la correzione linguistica va disattivata, perché tende a trasformare i
  codici in parole.
- **PaddleOCR / PP-OCRv6**: PaddleOCR 3.7.0 (11/06/2026) introduce PP-OCRv6 in tre taglie, tiny 1,5M, small 7,7M,
  medium 34,5M parametri; 50 lingue; conversione ONNX ed esecuzione con ONNX Runtime, OpenVINO, TensorRT; esiste
  PaddleOCR.js per il browser (con PP-OCRv5); licenza Apache 2.0 ([repo](https://github.com/PaddlePaddle/PaddleOCR)).
  Il model card del riconoscitore small indica circa 5,2M parametri e precisione media 81,3 contro 78,1 di
  PP-OCRv5_server; cita scenari industriali come caratteri a matrice di punti
  ([HF PP-OCRv6_small_rec](https://huggingface.co/PaddlePaddle/PP-OCRv6_small_rec)). La differenza 5,2M / 7,7M
  probabilmente dipende dal contare rilevatore + riconoscitore (IPOTESI). Il README non cita Android o iOS.
- **Tesseract**: Apache-2.0 ([LICENSE](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE)); funziona meglio
  da 300 dpi in su; `--psm 7` per una riga singola; `tessedit_char_whitelist` limita i caratteri ammessi;
  `load_system_dawg` e `load_freq_dawg` a false disattivano i dizionari
  ([ImproveQuality](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)). DEDUZIONE: pensato per pagine
  scansionate più che per foto da telefono; da tenere come ripiego.
- **docTR** (Mindee): Apache-2.0 ([LICENSE](https://github.com/mindee/doctr/blob/main/LICENSE)); non approfondito.

### Confusioni tipiche 0/O, 1/I/l, 5/S, 8/B, 2/Z

- DEDUZIONE: nessun OCR le elimina del tutto, perché in molti caratteri tipografici i segni sono quasi uguali. La
  difesa efficace non è un OCR migliore ma il **confronto con il catalogo**: il codice letto si cerca tra i codici
  noti trattando come equivalenti le coppie confondibili (e accettando una o due differenze), e si mostra
  all'operatore l'articolo trovato. Se il formato dei codici è noto (per esempio "3 lettere + 6 cifre") si può
  correggere per posizione. Con Tesseract si può limitare l'alfabeto; con Apple Vision si possono passare i codici
  come `customWords` (IPOTESI: con 35.000 codici non so se regge, da provare).

---

## Tabella comparativa

Legenda "Dove": T = realistico sul telefono, S = server in sede. "T/S" = possibile su entrambi. La colonna "Dove" è
una DEDUZIONE dalla taglia e dai requisiti dichiarati, salvo dove indicato nelle sezioni sopra.

| Modello | Ruolo | Parametri | Licenza pesi | Uso commerciale | Dove | Nota decisiva |
|---|---|---|---|---|---|---|
| SigLIP 2 B/16, L/16 | embedding | 86M / 303M | Apache-2.0 | sì | S (B anche T) | 2° famiglia su ILIAS; anche ricerca da testo |
| PE-Core S/B/L | embedding | B 0,09B, L 0,32B | Apache-2.0 | sì | S (S/T anche T) | PE-L a pari merito con DINOv3-B su ILIAS |
| DINOv3 S/B/L | embedding | 21M / 86M / 300M | DINOv3 License, accesso su richiesta | sembra sì, da far verificare | S (S anche T) | migliore su ILIAS |
| DINOv2 S/B/L | embedding | 21M / 86M / 300M | Apache-2.0 | sì | T/S | licenza più semplice, risultati inferiori |
| TIPS v1 S/B | embedding | 22M / 86M (visivo) | Apache-2.0 | sì | T/S | nessun risultato di recupero verificato |
| MobileCLIP2 | embedding | 11-322M | Apple AMLR, solo ricerca | **no** | T | escluso per licenza |
| EUPE, MoEViE | embedding | – | non commerciali | **no** | – | esclusi |
| MobileNetV4 (timm) | classificatore / encoder leggero | 9,7M (medium) | Apache-2.0 | sì | T | per compiti piccoli e fissi |
| ConvNeXt V2 (pesi ImageNet) | classificatore | – | CC-BY-NC | **no** | – | escluso |
| YOLO26 | rilevatore | 2,4-55,7M | AGPL-3.0 o Enterprise | solo pubblicando il codice o pagando | T/S | esportazione molto comoda |
| RF-DETR N/S/M/L | rilevatore | 30,5-33,9M | Apache-2.0 | sì | S (T da verificare) | XL/2XL e Atto-Pico no |
| D-FINE, DEIM v1, RT-DETR, YOLOX, RTMDet | rilevatore | – | Apache-2.0 | sì | T/S | alternative permissive |
| DEIMv2 | rilevatore | 0,5-50,3M | non commerciale | **no** | – | escluso |
| Grounding DINO (orig.) | vocabolario aperto | – | Apache-2.0 | sì | S | per preparare i dati |
| OWLv2 | vocabolario aperto | 0,2B | Apache-2.0 | sì | S | per preparare i dati |
| YOLO-World / YOLOE | vocabolario aperto | – | GPL-3.0 / AGPL-3.0 | con obblighi copyleft | T/S | sconsigliati per licenza |
| SAM 3 / 3.1 | segmentazione da testo | 848M | SAM License, accesso su richiesta | sembra sì | S (GPU CUDA) | pesante |
| SAM 2, MobileSAM | segmentazione | – | Apache-2.0 | sì | S / T | ritaglio preciso |
| Gemma 4 E2B/E4B | VLM | 2,3B / 4,5B effettivi | Apache 2.0 | sì | S (T forse) | proposta descrizione/codice |
| Qwen3.5 2B/4B, Qwen3-VL 2B/4B | VLM | 2,1-4,7B | Apache-2.0 | sì | S | buon OCR dichiarato |
| Florence-2 | VLM/OCR | 0,23 / 0,77B | MIT | sì | S (T forse) | piccolo, compiti fissi |
| SmolVLM2 | VLM | 0,26-2,2B | Apache 2.0 | sì | T/S | più debole |
| Moondream 3 | VLM | 9B (2B attivi) | BSL 1.1 + concessione | uso interno sì, con limiti | S | leggere la licenza |
| FastVLM | VLM | 0,5-7B | Apple, solo ricerca | **no** | T | escluso |
| ML Kit Barcode / Text v2 | barcode / OCR | – | SDK chiuso di Google (termini non letti) | – | T | sul dispositivo, pronto |
| Apple Vision / VisionKit | barcode / OCR | – | parte di iOS | – | T (iOS) | sul dispositivo, pronto |
| zxing-cpp | barcode | – | Apache-2.0 | sì | T/S/browser | per PC e server |
| PP-OCRv6 tiny/small/medium | OCR | 1,5 / 7,7 / 34,5M | Apache 2.0 | sì | S (tiny forse T) | OCR di riserva lato server |
| Tesseract | OCR | – | Apache-2.0 | sì | S | ripiego |

---

## Raccomandazione (DEDUZIONE)

Tutto ciò che segue è una mia deduzione dai fatti sopra, da confermare con una prova sulle foto reali.

**Architettura in tre stadi**

1. **Sul telefono, barcode**: ML Kit su Android, Apple Vision o VisionKit su iOS. Sono locali, gratuiti, già
   ottimizzati e non richiedono di distribuire modelli. Sul computer con telecamera: zxing-cpp in WebAssembly.
2. **Sul telefono, OCR del codice**: ML Kit Text Recognition v2 e Apple Vision con correzione linguistica
   disattivata. Il testo letto **non** si accetta così com'è: si confronta con l'elenco dei codici del catalogo
   tollerando le coppie confondibili (0/O, 1/I, 5/S, 8/B), e si mostra l'articolo trovato da confermare. Se la
   lettura sul telefono fallisce, il server può riprovare con PP-OCRv6 (small o medium).
3. **Sul server in sede, riconoscimento visivo per somiglianza**:
   - Primi candidati da confrontare: **SigLIP 2** (B/16 e L/16 a 384-512 px) e **PE-Core** (B/16, L/14 336 px).
     Licenza Apache-2.0, buoni risultati su ILIAS, nessun accesso riservato.
   - **DINOv3** (B/16, L/16) da includere nella prova **solo se** l'azienda accetta la DINOv3 License: è il
     migliore su ILIAS, ma la licenza non è standard.
   - **DINOv2** come riferimento di base, per la licenza semplice.
   - Indice: ricerca esatta (FAISS o pgvector) sugli embedding di più foto per articolo; a questa scala basta.
   - Risposta all'operatore: **le 3-5 proposte più vicine** con foto e codice, mai una scelta automatica silenziosa
     sotto una soglia di somiglianza; "nessun articolo noto" se la distanza è troppo grande.
   - Il server è preferibile al telefono perché l'indice dei 35.000 articoli resta in un solo posto, si aggiorna
     subito quando si aggiunge un articolo e si può cambiare modello senza aggiornare le app.

**Miglioramenti successivi, solo se la prova li giustifica**
- Rilevatore per ritagliare scatola ed etichetta: **RF-DETR Nano/Small** o **D-FINE** (Apache-2.0), affinati su
  poche classi. Da evitare Ultralytics (AGPL) se non si compra la licenza e DEIMv2 (non commerciale).
- Adattamento leggero dell'encoder sulle proprie foto (uno strato lineare o affinamento metrico), che su ILIAS
  migliora molto i risultati. Non serve ripeterlo per ogni articolo nuovo.
- Riordino delle prime proposte con un confronto più fine (descrittori locali o un secondo modello).

**Inserimento di un articolo nuovo**
- Foto (più angolazioni) → embedding salvati nell'indice → codice letto da barcode/OCR → **Gemma 4 E4B o
  Qwen3.5-4B sul server** propone descrizione e codice dall'etichetta → l'operatore corregge e conferma.
- Grounding DINO o OWLv2 possono ritagliare automaticamente la scatola nelle foto di catalogo.

**Da escludere per licenza**: MobileCLIP/MobileCLIP2, FastVLM, EUPE, MoEViE, pesi ImageNet di ConvNeXt V2, DEIMv2,
RF-DETR XL/2XL/Atto/Femto/Pico (senza accordo Roboflow), Grounding DINO 1.5/1.6 (solo cloud). Da usare solo con
consapevolezza degli obblighi: Ultralytics YOLO/YOLOE (AGPL), YOLO-World (GPL), Moondream 3.

**Prova consigliata prima di decidere** (IPOTESI di metodo): 200-500 articoli reali, 3-5 foto di catalogo ciascuno
e 2-3 foto "di arrivo" scattate da operatori con telefoni diversi; misurare quante volte l'articolo giusto è il
primo e quante volte è tra i primi 5, e il tempo di risposta dal telefono al server.

---

## Cosa resta incerto

- **Precisione reale sulle nostre scatole**: nessun dato pubblico misura questi modelli su scatole di magazzino
  quasi identiche. ILIAS è il riferimento più vicino trovato, ma è un compito diverso.
- **Quanto spesso il riconoscimento visivo da solo basterà**: con articoli che differiscono solo per una scritta
  (taglia, variante), è probabile che l'immagine non basti e serva l'OCR (IPOTESI).
- **Licenza DINOv3 e SAM**: il testo non limita l'uso alla ricerca, ma va letto da chi decide; Meta può aggiornarlo.
- **Termini d'uso di ML Kit**: non li ho letti; ML Kit è un SDK chiuso di Google. Va verificato che non invii dati
  e che l'uso commerciale sia ammesso (non verificato).
- **Prestazioni sul telefono**: non ho verificato tempi né conversioni (Core ML, LiteRT, ONNX Runtime Mobile) per
  SigLIP 2, PE o DINOv3. Le latenze di MobileCLIP sono su iPhone ma quel modello è escluso per licenza.
- **Esportazione di RF-DETR verso formati mobili**: il README non elenca ONNX, CoreML o TFLite.
- **Uscite di Ultralytics**: la pagina licenze non dice se le predizioni prodotte siano coperte da AGPL.
- **PP-OCRv6**: discrepanza 5,2M (model card) contro 7,7M (README) per la taglia small; nessun dato di latenza su
  telefono; README non cita Android/iOS.
- **Gemma 4**: il model card cita un rapporto tecnico "Published Jul 2"; fonti secondarie indicano un'uscita ad
  aprile 2026 (non verificato sulla fonte primaria).
- **PE-B su ILIAS**: scarto anomalo tra 5M e 100M segnalato dalla stessa classifica.
- **EfficientNet, FastViT (pesi timm), docTR**: non approfonditi.
- **Interpretazione del catalogo**: si assume che "35.000" siano articoli diversi e che il "numero seriale" sia il
  codice del tipo di articolo (vedi `docs/decisioni.md`, note di lettura).

---

## Fonti

Primarie (aperte il 15/11/2026):

- DINOv3: https://github.com/facebookresearch/dinov3 · https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md
- DINOv2: https://github.com/facebookresearch/dinov2
- SigLIP 2: https://arxiv.org/abs/2502.14786 · https://huggingface.co/google/siglip2-base-patch16-naflex
- Perception Encoder: https://github.com/facebookresearch/perception_models · https://huggingface.co/facebook/PE-Core-S16-384
- OpenCLIP: https://github.com/mlfoundations/open_clip · https://github.com/mlfoundations/open_clip/blob/main/LICENSE
- MobileCLIP: https://github.com/apple/ml-mobileclip · https://github.com/apple/ml-mobileclip/blob/main/LICENSE_MODELS
- TIPS: https://huggingface.co/google/tipsv1-s14
- EUPE / MoEViE / Mage-ViT: https://huggingface.co/facebook/EUPE-ViT-S · https://huggingface.co/facebook/MoEViE-B16-224 · https://huggingface.co/microsoft/Mage-ViT
- ILIAS: https://arxiv.org/abs/2502.11748 · https://vrg.fel.cvut.cz/ilias/
- MobileNetV4: https://arxiv.org/abs/2404.10518 · https://huggingface.co/timm/mobilenetv4_conv_medium.e500_r256_in1k
- timm: https://github.com/huggingface/pytorch-image-models/blob/main/LICENSE
- ConvNeXt V2: https://github.com/facebookresearch/ConvNeXt-V2
- FastViT: https://github.com/apple/ml-fastvit/blob/main/LICENSE
- Ultralytics: https://www.ultralytics.com/license · https://docs.ultralytics.com/models/yolo26/ · https://github.com/ultralytics/ultralytics/blob/main/LICENSE
- RF-DETR: https://github.com/roboflow/rf-detr
- D-FINE: https://github.com/Peterande/D-FINE/blob/master/LICENSE
- DEIM: https://github.com/ShihuaHuang95/DEIM/blob/main/LICENSE
- DEIMv2: https://github.com/Intellindust-AI-Lab/DEIMv2 · https://github.com/Intellindust-AI-Lab/DEIMv2/blob/main/LICENSE.md
- RT-DETR: https://github.com/lyuwenyu/RT-DETR/blob/main/LICENSE
- YOLOX: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/LICENSE
- MMDetection (RTMDet): https://github.com/open-mmlab/mmdetection/blob/main/LICENSE
- Grounding DINO: https://github.com/IDEA-Research/GroundingDINO/blob/main/LICENSE · https://github.com/IDEA-Research/Grounding-DINO-1.5-API
- OWLv2: https://huggingface.co/google/owlv2-base-patch16-ensemble
- YOLO-World: https://github.com/AILab-CVC/YOLO-World/blob/master/LICENSE
- YOLOE: https://github.com/THU-MIG/yoloe
- SAM 3: https://github.com/facebookresearch/sam3 · https://github.com/facebookresearch/sam3/blob/main/LICENSE
- SAM 2: https://github.com/facebookresearch/sam2/blob/main/LICENSE
- MobileSAM: https://github.com/ChaoningZhang/MobileSAM/blob/master/LICENSE
- Gemma 4: https://huggingface.co/google/gemma-4-E2B-it
- Qwen3.5: https://huggingface.co/Qwen/Qwen3.5-2B
- Qwen3-VL: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct · https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct
- SmolVLM2: https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct
- Florence-2: https://huggingface.co/microsoft/Florence-2-base
- PaliGemma 2 / Gemma 3n: https://huggingface.co/google/paligemma2-3b-pt-224 · https://huggingface.co/google/gemma-3n-E2B-it
- Moondream: https://huggingface.co/moondream/moondream3-preview · https://huggingface.co/vikhyatk/moondream2 · https://huggingface.co/moondream/moondream3.1-9B-A2B
- FastVLM: https://github.com/apple/ml-fastvlm · https://github.com/apple/ml-fastvlm/blob/main/LICENSE_MODEL
- Limiti dei VLM (MMVP): https://arxiv.org/abs/2401.06209
- ML Kit: https://developers.google.com/ml-kit/vision/barcode-scanning · https://developers.google.com/ml-kit/vision/barcode-scanning/android · https://developers.google.com/ml-kit/vision/text-recognition/v2 · https://developers.google.com/ml-kit/vision/text-recognition/v2/android
- Apple Vision / VisionKit: https://developer.apple.com/documentation/vision/recognizetextrequest · https://developer.apple.com/documentation/vision/vnrecognizetextrequest/customwords · https://developer.apple.com/documentation/vision/vnrecognizetextrequest/useslanguagecorrection · https://developer.apple.com/documentation/vision/vnbarcodesymbology · https://developer.apple.com/documentation/visionkit/datascannerviewcontroller
- zxing-cpp / ZXing / ZBar: https://github.com/zxing-cpp/zxing-cpp · https://github.com/zxing/zxing · https://github.com/mchehab/zbar/blob/master/COPYING
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR · https://huggingface.co/PaddlePaddle/PP-OCRv6_small_rec
- Tesseract: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html · https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE
- docTR: https://github.com/mindee/doctr/blob/main/LICENSE
- Indici vettoriali: https://github.com/facebookresearch/faiss/blob/main/LICENSE · https://github.com/unum-cloud/usearch/blob/main/LICENSE · https://github.com/pgvector/pgvector/blob/master/LICENSE
- Licenze, gating e numero di parametri di vari modelli Hugging Face: API pubblica `https://huggingface.co/api/models/<id>` (campi `cardData.license`, `gated`, `safetensors.total`).

Secondarie (usate solo per orientarsi, non citate come prova): risultati di ricerca web su Gemma 4 e Qwen3-VL
(articoli di stampa e aggregatori), poi verificati sui model card ufficiali.

Pagine non raggiungibili o incomplete: nessun blocco. Le pagine di documentazione Apple sono state lette tramite il
loro endpoint JSON ufficiale (developer.apple.com/tutorials/data/...), perché la pagina HTML richiede JavaScript.
