# Addestramento ed esecuzione locale per il riconoscimento degli articoli

Data: 15/11/2026

Stato: BOZZA in lavorazione.

## Domanda

Serve addestrare un modello leggero o si può partire senza? Come si adatta con pochi dati, e come si esegue tutto in
locale su telefono, browser e server in sede?

Legenda: **FATTO** = verificato sulla fonte linkata; **DEDUZIONE** = ragionamento mio a partire dai fatti;
**IPOTESI** = da verificare con prove sul campo; **non verificato** = dalla memoria, senza fonte aperta.

## Sintesi

(da completare)

## A. Senza addestramento: encoder pre-addestrato + ricerca per somiglianza

**FATTI**

- DINOv2 (Meta, 2023) è un encoder visivo auto-supervisionato. Il README ufficiale dà, su ImageNet-1k, k-NN 79,0% e
  linear probe 81,1% per ViT-S/14 (21M parametri), 82,1% / 84,5% per ViT-B/14 (86M), 83,5% / 86,3% per ViT-L/14
  (300M). Codice e pesi sono sotto **Apache 2.0**.
  [README DINOv2](https://github.com/facebookresearch/dinov2)
- Nel lavoro originale, il riconoscimento di istanza (Oxford/Paris, Met, AmsterTime) è fatto **senza addestramento**:
  le immagini dell'archivio sono ordinate per similarità coseno con la foto di query. DINOv2 ViT-L/14 ottiene per esempio
  54,0 mAP su Oxford-Hard contro 19,7 di OpenCLIP ViT-G/14, e supera OpenCLIP su tutte le colonne della Tabella 9.
  [DINOv2, arXiv 2304.07193, Tab. 9](https://arxiv.org/html/2304.07193v2)
- Sulla classificazione a grana fine con linear probe (12 dataset, Tab. 8) DINOv2 ViT-g/14 e OpenCLIP ViT-G/14 sono
  quasi pari in media (92,1 vs 91,9); DINOv2 resta indietro su Cars (91,4 vs 96,1) e SUN.
  [DINOv2, Tab. 8](https://arxiv.org/html/2304.07193v2)
- DINOv3 (Meta, 2025) dichiara feature "congelate" utilizzabili senza fine-tuning e una famiglia distillata: ViT-S/16
  21M, ViT-S+/16 29M, ViT-B/16 86M, ViT-L/16 300M, ViT-H+/16 840M, più ConvNeXt Tiny 29M / Small 50M / Base 89M /
  Large 198M. Nella Tab. 14 del lavoro, sul recupero di istanza Oxford-Hard il ViT-S passa da 39,5 (DINOv2) a 49,5
  (DINOv3) e il ViT-B da 51,0 a 58,5.
  [DINOv3, arXiv 2508.10104](https://arxiv.org/abs/2508.10104), [testo completo, Tab. 9 e 14](https://arxiv.org/html/2508.10104),
  [repository](https://github.com/facebookresearch/dinov3)
- **Licenza DINOv3**: non è Apache. È la "DINOv3 License": licenza gratuita, mondiale, non esclusiva, che non esclude
  l'uso commerciale ma vieta usi militari/ITAR, vieta il reverse engineering, impone di distribuire una copia
  dell'accordo con i derivati e consente a Meta di modificarla. I pesi si scaricano dopo richiesta (accesso "gated").
  Supporto in Transformers dalla 4.56.0 e in timm dalla 1.0.20.
  [LICENSE.md](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md), [README](https://github.com/facebookresearch/dinov3)
- SigLIP 2 (Google, 2025): encoder immagine-testo in quattro taglie (ViT-B 86M, L 303M, So400m 400M, g 1B); migliora
  rispetto a SigLIP su classificazione zero-shot, recupero immagine-testo e caratteristiche dense; varianti a
  risoluzione multipla con proporzioni native. Checkpoint nel repository big_vision.
  [SigLIP 2, arXiv 2502.14786](https://arxiv.org/abs/2502.14786)
- CLIP (OpenAI, 2021): il classificatore zero-shot (dal testo) eguaglia in media un linear probe a **4 esempi per
  classe** sullo stesso spazio di feature; il numero di esempi equivalente varia molto tra dataset (mediana 5,4, media
  20,8, fino a 184 per classe), ed è debole su compiti specialistici.
  [CLIP, arXiv 2103.00020, Fig. 6 e sez. 3.1.5](https://arxiv.org/pdf/2103.00020)
- Il caso più vicino al nostro trovato in letteratura: *Cat2Real* (luglio 2026), riconoscimento di prodotti come
  **recupero per embedding** (non classificazione chiusa) da foto reale verso immagini di catalogo, su 1.865 prodotti
  in valutazione. Encoder congelati: DINOv2 ViT-L/14 top-1 35,5% / top-5 61,4%; DINOv3 ViT-L/16 a 384 px 53,8% /
  78,1%. Dopo fine-tuning contrastivo (12 blocchi su 24 sbloccati, ~197.000 foto reali di ~27.000 prodotti): 80,7% /
  94,7%. Togliendo dall'addestramento i prodotti di valutazione, il top-1 scende solo di 0,5 punti.
  [Cat2Real, arXiv 2607.09888](https://arxiv.org/html/2607.09888)
- Lavori su prodotti da supermercato motivano lo stesso approccio: gli articoli cambiano spesso, quindi si impara un
  embedding e si usa il K-NN invece di riaddestrare un classificatore.
  [arXiv 1902.00760](https://arxiv.org/pdf/1902.00760)
- Apple: Create ML consiglia **almeno 10 immagini per categoria**, bilanciate, da più angolazioni e luci, e un insieme
  di prova di circa il 20% se si hanno almeno 25 immagini per categoria.
  [Create ML, Creating an Image Classifier Model](https://developer.apple.com/documentation/createml/creating-an-image-classifier-model)

**DEDUZIONI**

- Partire **senza addestramento** è sensato: è lo stesso protocollo (similarità coseno su feature congelate) con cui
  DINOv2/DINOv3 sono valutati sul riconoscimento di istanza, ed è quello che permette di aggiungere un articolo con una
  foto senza riaddestrare.
- Ma il dato Cat2Real dice che, con prodotti molto simili e con differenza di dominio, un encoder congelato può
  sbagliare circa una volta su due in top-1, mentre lo stesso encoder adattato sale oltre l'80%. Nel nostro caso la
  differenza di dominio è minore (foto di riferimento e foto di query fatte con telefoni simili nello stesso magazzino),
  quindi è plausibile fare meglio di quel 50%, ma **non c'è un numero pubblicato per il nostro scenario**: va misurato.
- Il testo libero (zero-shot alla CLIP/SigLIP) serve poco: i nostri articoli si distinguono per codici e dettagli, non
  per nomi descrivibili. Lo zero-shot non sostituisce le foto di riferimento.
- Un buon punto di partenza per le foto di riferimento: 3-10 per articolo (fronte, lato, etichetta), poi crescono con
  l'uso (vedi C). Il "10" di Apple riguarda un classificatore addestrato, non il k-NN: per il k-NN non ho trovato una
  regola pubblicata; va stabilito con una prova.

## B. Adattamento leggero

(in lavorazione)

**FATTI**

- *A Metric Learning Reality Check* (Musgrave et al., 2020): rifacendo gli esperimenti con protocollo corretto, i
  miglioramenti delle loss di metric learning più recenti rispetto a quelle di dieci anni prima sono "marginali nel
  migliore dei casi". [arXiv 2003.08505](https://arxiv.org/abs/2003.08505)
- pytorch-metric-learning (dello stesso autore) è sotto licenza **MIT**, versione 3.0.3 del 13/11/2026 su PyPI; ha
  backend FAISS opzionale. [repository](https://github.com/KevinMusgrave/pytorch-metric-learning),
  [LICENSE](https://raw.githubusercontent.com/KevinMusgrave/pytorch-metric-learning/master/LICENSE),
  [PyPI](https://pypi.org/project/pytorch-metric-learning/)
- LoRA con Hugging Face PEFT su un ViT-B/16: si addestra lo 0,77% dei parametri (667.493 su 86,5M), l'adattatore pesa
  circa 2,6 MB; nell'esempio ufficiale (5.000 immagini Food-101) arriva al 96% in validazione in 5 epoche.
  [PEFT, guida image classification LoRA](https://huggingface.co/docs/peft/main/en/task_guides/image_classification_lora)
- Cat2Real (vedi A) è un esempio pubblicato di fine-tuning parziale (metà dei blocchi congelati) con apprendimento
  contrastivo e ricerca di negativi difficili, su una sola GPU A100; non riporta ore di addestramento.
  [arXiv 2607.09888](https://arxiv.org/html/2607.09888)

## C. Catalogo che cambia

(in lavorazione)

- *Open-Set Recognition: a Good Closed-Set Classifier is All You Need* (Vaze et al., 2022): la capacità di dire
  "nessuno dei noti" è fortemente correlata all'accuratezza sui noti; migliorare l'accuratezza chiusa di un baseline
  basato sul punteggio massimo dà risultati allo stato dell'arte sul rifiuto degli sconosciuti.
  [arXiv 2110.06207](https://arxiv.org/abs/2110.06207)

## D. Strumenti di annotazione e addestramento
## E. Indici vettoriali locali
## F. Runtime e formati
## G. OCR e barcode in locale
## H. Architettura e hardware
## I. Qualità della ripresa e misura dell'accuratezza
## Tabella riassuntiva
## Percorso consigliato (DEDUZIONE)
## Cosa resta incerto
## Fonti
