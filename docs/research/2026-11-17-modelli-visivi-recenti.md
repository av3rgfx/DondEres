# Modelli visivi recenti per riconoscere l'articolo esatto

Data: 17/11/2026. Pagine e API aperte il 17/11/2026.

## Domanda

Esistono modelli open source più recenti (usciti tra metà 2025 e novembre 2026) migliori di quelli scelti per la
prova (decisioni 140 e 141: SigLIP 2, PE-Core e DINOv2 in taglia media e grande; DINOv3 solo come confronto) nel
riconoscere **l'istanza esatta** di un prodotto con la ricerca per somiglianza? Devono avere una licenza dei pesi che
permetta l'uso commerciale in un prodotto installato presso i clienti e un costo ragionevole su un server senza scheda
grafica (ONNX Runtime o simile).

Da leggere insieme a `2026-11-15-modelli-visivi-riconoscimento-articoli.md` (schede di SigLIP 2, PE-Core, DINOv2,
DINOv3, MobileCLIP, EUPE, MoEViE), `2026-11-15-addestramento-ed-esecuzione-locale.md` (ONNX, CPU) e
`2026-11-15-progetti-simili-riconoscimento-prodotti.md` (banco di prova nyris). Qui non si ripete ciò che è già lì.

## Come leggere questo documento

- **FATTO**: preso da una fonte primaria (articolo, repository, model card o API di Hugging Face), con il link.
- **DEDUZIONE**: ragionamento mio a partire dai fatti. Può essere sbagliato.
- **IPOTESI**: da verificare con la prova sulle foto reali.
- Le licenze sono riassunte da me, non sono un parere legale.
- **GMAC**: miliardi di moltiplicazioni-addizioni per immagine, dalla scheda timm del modello. Indica il costo di
  calcolo: a parità di macchina, il doppio dei GMAC vuol dire all'incirca il doppio del tempo (DEDUZIONE).

## Sintesi

1. Non ho trovato nessun modello uscito da metà 2025 con licenza commerciale che risulti **migliore** di SigLIP 2 e
   PE-Core su un banco di prova di recupero di istanze o di prodotti. Nei confronti indipendenti del 2026 (nyris su
   prodotti e ricambi, Bosch su ricambi industriali, ILIAS) i migliori modelli aperti restano DINOv3, SigLIP 2 e PE-Core.
2. Nessuna nuova versione delle famiglie scelte: niente SigLIP 3, nessun PE-Core successivo, nessun DINOv4.
3. Due novità con licenza commerciale meritano attenzione, ma senza risultati diretti sul recupero di istanze:
   **TIPSv2** di Google (aprile 2026, Apache-2.0) e **C-RADIOv3/v4** di NVIDIA (2025-2026, licenza propria NVIDIA che
   permette l'uso commerciale).
4. I modelli di embedding multimodali basati su un VLM (Jina v4, Nomic 3B) rendono **molto peggio** di SigLIP 2 e
   PE-Core sui prodotti, e costano molto di più su CPU. Molti sono anche non commerciali. Qwen3-VL-Embedding è
   Apache-2.0, ma pesa 2 miliardi di parametri e non ha risultati sui prodotti.
5. Il miglioramento più grande trovato non viene da un modello nuovo ma dal **ritaglio dell'oggetto**: su ILIAS il
   riordino con ritagli automatici porta DINOv3-L da 26,5 a 42,0 di mAP.
6. Proposta (DEDUZIONE): lasciare invariato l'elenco della decisione 140; al massimo aggiungere TIPSv2-B come candidato
   facoltativo a basso costo. C-RADIO resta fuori dalla prova finché l'utente non legge la licenza NVIDIA.

---

## Tabella comparativa

"Istanze" = risultati di recupero di istanze o di prodotti, con la fonte. Dove non c'è niente lo scrivo. Le taglie sono
i parametri della sola parte visiva, salvo dove indicato.

| Modello | Data | Taglie | Licenza dei pesi | Recupero di istanze (fonte) | CPU e ONNX |
|---|---|---|---|---|---|
| **Riferimento: SigLIP 2** (Google) | feb 2025 | B 86M, L 303M, So400m 400M, g 1B | Apache-2.0 ([HF](https://huggingface.co/google/siglip2-large-patch16-512)) | ILIAS 100M: L@512 20,8, B@512 15,4 ([ILIAS](https://vrg.fel.cvut.cz/ilias/)); nyris, R@1 medio So400m 45,7% ([nyris](https://benchmark.nyris.io/models)) | ONNX di onnx-community per tutte le taglie ([HF](https://huggingface.co/onnx-community/siglip2-large-patch16-512-ONNX)) |
| **Riferimento: PE-Core** (Meta) | apr 2025 | T, S, B 0,09B, L 0,32B, G 1,88B | Apache-2.0 ([HF](https://huggingface.co/facebook/PE-Core-L14-336)) | ILIAS 100M: L 22,0, B 9,7 (20,2 su 5M); nyris L/14 44,3% | ONNX di onnx-community per B e L ([HF](https://huggingface.co/onnx-community/PE-Core-L14-336-ONNX)), non provati |
| **Riferimento: DINOv2** (Meta) | 2023 | S, B 86M, L 304M, g | Apache-2.0 | ILIAS 100M: L 15,3, B 11,5; nyris L 36,9% | ONNX ufficiosi; **B 151,7 / L 507,1 GMAC a 518 px** ([timm L](https://huggingface.co/timm/vit_large_patch14_dinov2.lvd142m)) |
| **Riferimento: DINOv3** (Meta) | ago 2025 | S 21M … L 303M, 7B | DINOv3 License, accesso su richiesta ([HF](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m)) | ILIAS 100M: L 26,5, B 22,0; nyris L 45,2% | ONNX di onnx-community |
| **TIPSv2** (Google DeepMind) | 13/04/2026 | B 86M, L 303M, SO 412M, g 1,1B (più la torre del testo) | Apache-2.0 sul model card ([HF](https://huggingface.co/google/tipsv2-b14)); il repository dice codice Apache-2.0 e "all other materials" CC-BY 4.0 ([GitHub](https://github.com/google-deepmind/tips)) | Nessun risultato su ILIAS né su prodotti. UnED (8 insiemi, tra cui SOP e RP2k): g/14 67,0 contro DINOv2-g 62,7; SigLIP 2 e PE non confrontati su UnED ([arXiv 2604.12012](https://arxiv.org/html/2604.12012)) | **B 107,1 / L 362,5 GMAC a 448 px** ([timm B](https://huggingface.co/timm/vit_base_patch14_reg1_tipsv2.webli), [timm L](https://huggingface.co/timm/vit_large_patch14_reg1_tipsv2.webli)); in timm; ONNX solo di terzi |
| **C-RADIOv3** (NVIDIA) | giu 2025 | B 98M, L 320M, H 652M, g 1,16B (totale dal file) | NVIDIA Open Model License: uso commerciale sì, licenza propria ([HF](https://huggingface.co/nvidia/C-RADIOv3-B), [testo](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf)) | Nessun risultato di recupero di istanze. ImageNet k-NN: B 81,22, L 84,33 ([HF v4](https://huggingface.co/nvidia/C-RADIOv4-SO400M)) | **B 108,0 / L 365,1 GMAC a 512 px** ([timm B](https://huggingface.co/timm/vit_base_patch16_radio_v3.c_radio)); ONNX solo di terzi |
| **C-RADIOv4** (NVIDIA) | 27/01/2026 | SO400M 412-431M, H 631-652M | NVIDIA Open Model License ([HF](https://huggingface.co/nvidia/C-RADIOv4-SO400M)) | Nessun risultato di recupero di istanze. ImageNet k-NN: SO400M 85,75, H 86,68 ([arXiv 2601.17237](https://arxiv.org/html/2601.17237v1)) | SO400M 492,8 GMAC a 512 px ([timm](https://huggingface.co/timm/vit_so400m_patch16_radio_v4.c_radio)); model card con hardware solo NVIDIA |
| Qwen3-VL-Embedding (Alibaba) | 08/01/2026 | 2B (2,13B), 8B | Apache-2.0 ([HF](https://huggingface.co/Qwen/Qwen3-VL-Embedding-2B)) | Nessun risultato su istanze o prodotti; MMEB-V2 "image retrieval" 74,8 (2B), compito diverso | 2 miliardi di parametri: pesante su CPU (DEDUZIONE); ONNX solo di terzi |
| Jina Embeddings v4 | mag 2025 | 3,75B | **Qwen Research License** (il model card corregge un iniziale CC-BY-NC) ([HF](https://huggingface.co/jinaai/jina-embeddings-v4)) | nyris R@1 medio 28,2%, contro 45,7% di SigLIP 2 So400m ([nyris](https://benchmark.nyris.io/models)) | pesante; **escluso** per licenza |
| Jina Embeddings v5 omni | apr 2026 | nano 0,99B, small 1,63B | **CC-BY-NC-4.0** ([HF](https://huggingface.co/jinaai/jina-embeddings-v5-omni-small)) | nessuno | **escluso** (non commerciale) |
| Nomic Embed Multimodal 3B | mar 2025 | 3B | "weights available for research use", derivato da Qwen2.5-VL-3B ([HF](https://huggingface.co/nomic-ai/nomic-embed-multimodal-3b)) | nyris 27,2% | **escluso** |
| NVIDIA Nemotron embed VL | dic 2025 / ott 2026 | 1,55-1,68B (e 8B) | NVIDIA Open Model License ([1B v2](https://huggingface.co/nvidia/llama-nemotron-embed-vl-1b-v2)); OpenMDW-1.1 per Nemotron-3.5 ([HF](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16)), non letta | nessuno; pensati per documenti (etichetta "visual-document-retrieval") | pesanti; fuori tema |
| MetaEncoder (Meta) | 30/09/2026 | 30B | Apache-2.0 + policy del modello base, accesso con consenso ([HF](https://huggingface.co/facebook/meta-encoder)) | nessuno su istanze | 30 miliardi: **impossibile su CPU** |
| Mage-ViT (Microsoft) | lug 2026 | 316M | MIT ([HF](https://huggingface.co/microsoft/Mage-ViT)) | nessun risultato pubblicato; pensato soprattutto per i video | gira su CPU secondo il model card |
| MetaCLIP 2 (Meta) | lug-nov 2025 | S … giant | **CC-BY-NC-4.0** ([HF](https://huggingface.co/facebook/metaclip-2-worldwide-l14)) | — | **escluso** |
| Web-SSL DINO (Meta) | apr 2025 / mar 2026 | 300M-7B | **CC-BY-NC-4.0** ([HF](https://huggingface.co/facebook/webssl-dino300m-light2b-224)) | — | **escluso** |
| Pixio (Meta) | dic 2025 | B … 5B | **FAIR non commercial**, accesso su richiesta ([HF](https://huggingface.co/facebook/pixio-vitl16)) | — | **escluso** |
| Franca (Valeo) | lug 2025 | B, L, g | **Research-only RAIL**: "Commercial use is therefore prohibited" ([LICENSE_MODEL](https://raw.githubusercontent.com/valeoai/Franca/main/LICENSE_MODEL)) | ILIAS 100M L 7,6 | **escluso** |
| RADIOv2.5, E-RADIO (NVIDIA) | 2024 | B … g | **NSCL, non commerciale** ([GitHub](https://github.com/NVlabs/RADIO)) | — | **escluso** |
| AIMv2, DFN-CLIP, MobileCLIP2 (Apple) | 2024-2025 | — | **apple-amlr**, solo ricerca ([HF AIMv2](https://huggingface.co/apple/aimv2-large-patch14-224)) | — | **esclusi** |

---

## Fatti

### Nuovi confronti sul recupero di prodotti e di istanze

- **nyris, "Visual Product Search Benchmark"** (marzo 2026, autori di un'azienda che vende un modello concorrente).
  R@1 medio sui loro otto insiemi (ricambi auto e industriali, mobili, fai da te, Stanford Online Products,
  Products-10K, TOPEX, ILIAS): GEM v6 di
  nyris 65,79%, Gemini Embedding 2 46,89%, **SigLIP 2 So400m 45,68%**, **DINOv3 L/16 45,24%**, Vertex AI 44,73%,
  **PE-Core L/14 44,30%**, Cohere Embed v4 37,38%, **DINOv2 L 36,93%**, Jina Embeddings v4 28,21%, Nomic Embed MM 3B
  27,23% ([classifica](https://benchmark.nyris.io/models), [arXiv 2603.17186](https://arxiv.org/html/2603.17186)).
  Nell'articolo DINOv3 è valutato a 224 px. Il sito non contiene TIPS, C-RADIO né Qwen3-VL-Embedding.
- **Bosch, CVPR 2026 workshop** ("Efficient Fine-grained Image Retrieval with Vision Foundation Models for Industrial
  Objects"): oltre 17.000 ricambi industriali fotografati anche con il telefono, galleria di circa 10.000 immagini. Con
  i modelli usati così come sono, sulla galleria "Challenge" di foto da telefono: R@1 **SigLIP 2 So400m 28,1%**,
  **DINOv3-L 23,6%**; R@10 57,1% contro 44,4%. Con uno strato lineare addestrato sopra: SigLIP 2 42,3%, DINOv3 37,0%,
  DINOv3 + SigLIP 2 insieme 45,6%. Tempo: circa 532 ms per richiesta su una GPU A100 per i due encoder insieme, circa
  2 ms per la ricerca ([PDF](https://openaccess.thecvf.com/content/CVPR2026W/FGVC13/papers/Liu_Efficient_Fine-grained_Image_Retrieval_with_Vision_Foundation_Models_for_Industrial_CVPRW_2026_paper.pdf)).
  Gli autori notano che sull'identificazione a coppie quasi tutti superano il 96% e il compito "may not be sufficiently
  challenging".
- **ILIAS**, classifica aggiornata (mAP@1k su 5M / 100M di immagini di disturbo), modelli congelati: DINOv3-L 31,1 /
  26,5; PE-L@336 27,1 / 22,0; SigLIP2-L@512 25,3 / 20,8; DINOv3-B 26,4 / 22,0; SigLIP2-B@512 18,6 / 15,4; PE-B 20,2 /
  9,7; DINOv2-L 18,5 / 15,3; DINOv2-B 14,3 / 11,5. Modelli più recenti presenti, tutti sotto: UNIC-L 8,9, Franca-L 7,6,
  UDON 5,5-5,9 su 100M. Con l'adattamento lineare: PE-L 33,4, SigLIP2-L 31,3, DINOv3-L 28,3. Nessuna riga per TIPS,
  C-RADIO, Qwen o Jina ([ILIAS](https://vrg.fel.cvut.cz/ilias/)).
- **"Beyond Resolution: Object-to-Image Ratio Mismatch in Instance Retrieval"** (8/10/2026): su ILIAS 100M, DINOv3-L
  passa da mAP 26,5 e R@1 55,0 a **mAP 42,0 e R@1 76,0** riordinando le prime 1.000 risposte con ritagli automatici
  delle immagini della galleria (OWLv2 senza testo, fino a 50 riquadri per immagine, ciascuno ricodificato con
  DINOv3-L), senza addestramento. Costo: circa 31 ritagli per immagine, quindi circa 32 volte il calcolo una tantum
  sulla galleria; dal lato della richiesta resta un solo passaggio. Sul loro banco sintetico, con i modelli usati così
  come sono, SigLIP-2-L (0,662) e DINOv3-L (0,645) sono vicini ([arXiv 2610.11489](https://arxiv.org/html/2610.11489v1)).
- **"Indexing Multimodal Language Models for Large-scale Image Retrieval"** (14/04/2026, autori di ILIAS): usa un VLM
  per confrontare coppie di immagini e riordinare i primi risultati; segnala insuccessi "under severe appearance
  changes" ([arXiv 2604.13268](https://arxiv.org/abs/2604.13268)). Nell'abstract non ci sono tempi né hardware.

### Nuovi modelli con licenza commerciale

- **TIPSv2**: articolo del 13/04/2026, CVPR 2026. Taglie B/L/SO/g, patch 14; l'esempio usa 448 px; caricamento con
  Transformers (`trust_remote_code=True`) e anche in timm. Su UnED (recupero fine su Food2k, CARS196, SOP, InShop,
  iNat, Met, GLDv2, RP2k): TIPSv2 g/14 67,0, TIPS v1 g/14 68,2, DINOv2 g/14 62,7, CLIP L/14 57,4. Non ci sono numeri
  UnED per le taglie B, L e SO, né confronti con SigLIP 2 o PE-Core su UnED. ImageNet k-NN: B 79,8, L 82,5
  ([arXiv 2604.12012](https://arxiv.org/html/2604.12012), [model card](https://huggingface.co/google/tipsv2-b14),
  [GitHub](https://github.com/google-deepmind/tips)).
- **C-RADIOv4**: rapporto tecnico del 24/01/2026; pesi pubblicati il 27/01/2026. È "distillato" da tre modelli
  insegnanti: SigLIP2-g-384, DINOv3-7B e SAM3. Uscite: un vettore riassuntivo dell'immagine (come il CLS) e le
  caratteristiche per zona. Nessun risultato di recupero di immagini nel rapporto
  ([arXiv 2601.17237](https://arxiv.org/html/2601.17237v1)). Il model card elenca solo hardware NVIDIA e TensorRT e
  dice "ready for commercial/non-commercial use" ([HF](https://huggingface.co/nvidia/C-RADIOv4-SO400M)).
- **C-RADIOv3** B/L/H/g (README: rilascio "6.3.2025") con la stessa licenza; i modelli il cui nome inizia per
  `RADIO` ed `E-RADIO` hanno invece la licenza NSCL, non commerciale ([GitHub](https://github.com/NVlabs/RADIO)).
- **NVIDIA Open Model License** (versione di giugno 2024): "Models are commercially useable"; si possono distribuire i
  modelli e quelli derivati, allegando la licenza e un file "Notice" con la frase "Licensed by NVIDIA Corporation under
  the NVIDIA Open Model License"; la licenza decade per chi fa causa sostenendo che il modello viola brevetti o diritti
  d'autore; "NVIDIA may update this Agreement to comply with legal and regulatory requirements at any time", e chi lo
  usa deve adeguarsi o smettere ([PDF](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf)).
- **RADIO1D** (luglio 2026, NVIDIA): misura un recupero "composition-aware" di scene (MS-COCO, nuImages), non di oggetti
  esatti; C-RADIOv4-1D-H ha 1,45B parametri ([arXiv 2607.03624](https://arxiv.org/pdf/2607.03624),
  [HF](https://huggingface.co/nvidia/C-RADIOv4-1D-H)).
- **Qwen3-VL-Embedding**: 2B e 8B, Apache-2.0, vettore fino a 2.048 numeri riducibile (da 64 a 2.048); MMEB-V2
  complessivo 73,2 (2B) e 77,8 (8B); il model card consiglia FlashAttention-2 e non parla di CPU
  ([HF](https://huggingface.co/Qwen/Qwen3-VL-Embedding-2B)).

### Nessuna nuova versione delle famiglie scelte

- **PE**: le ultime novità del repository sono gli 8 checkpoint dell'11/07/2025 (PE-Core T e S, PE-Spatial piccoli) e
  PE-AV per audio e video del 16/12/2025; nessun PE-Core successivo ([GitHub](https://github.com/facebookresearch/perception_models)).
- **SigLIP e DINO**: nell'elenco dei modelli di `google` e `facebook` su Hugging Face creati da giugno 2025 non
  compaiono né SigLIP 3 né DINOv4; ci sono TIPSv2, TIPS v1 (ricaricato ad agosto 2026), MedSigLIP (licenza Health AI
  Developer Foundations), EUPE, MoEViE, Pixio, MetaCLIP 2 e MetaEncoder (API di Hugging Face,
  `https://huggingface.co/api/models?author=<autore>&sort=createdAt`).

### Classifiche cercate e non utili

- **MIEB** (benchmark di embedding di immagini in MTEB) comprende compiti adatti al nostro caso (RP2k, SOP, ROxford,
  RParis), ma nell'articolo non ci sono SigLIP 2, PE né DINOv3 ([arXiv 2504.10471](https://arxiv.org/html/2504.10471)).
  Il repository dei risultati non era accessibile da questa sessione.
- **GPR1200**: nessun risultato recente trovato per SigLIP 2, PE, DINOv3 o modelli nuovi.
- **Revisited Oxford/Paris**: usati nell'articolo del 2026 sul rapporto oggetto/immagine solo per convalida, senza
  modelli nuovi rispetto a quelli già noti.
- **Products-10K e Stanford Online Products**: gli unici numeri recenti per i modelli aperti sono quelli di nyris
  (sopra), solo per le taglie grandi.

### ONNX ed esecuzione su CPU

- Esportazioni ONNX pubblicate da onnx-community: SigLIP 2 (tutte le taglie e risoluzioni), PE-Core B16-224 e
  L14-336, DINOv2, DINOv3. Per TIPSv2 (Armaggheddon), C-RADIO (ZumaInnovations) e Qwen3-VL-Embedding-2B esistono solo
  esportazioni di terzi, con pochissimi download (ricerca nell'API di Hugging Face con il filtro `onnx`).
- Costo dalle schede timm (GMAC per immagine): DINOv2-B a 518 px 151,7, DINOv2-L 507,1; TIPSv2-B a 448 px 107,1,
  TIPSv2-L 362,5; C-RADIOv3-B a 512 px 108,0, C-RADIOv3-L 365,1, C-RADIOv4-SO400M 492,8. Le schede timm di SigLIP 2 e
  PE-Core non riportano i GMAC.

---

## Deduzioni

- **Nessun motivo per sostituire i modelli scelti.** Dove i modelli nuovi sono stati misurati su prodotti (nyris), i
  modelli di embedding multimodali open (Jina v4, Nomic 3B) stanno 16-18 punti sotto SigLIP 2 e PE-Core. Dove non
  sono stati misurati (TIPSv2, C-RADIO, Qwen3-VL-Embedding), non c'è nessuna prova che facciano meglio.
- **SigLIP 2 e PE-Core restano le scelte giuste con licenza Apache.** Sui due confronti più vicini al nostro caso
  (foto da telefono di oggetti quasi uguali: Bosch; prodotti: nyris) SigLIP 2 è pari o superiore a DINOv3 usato così
  com'è. DINOv3 vince solo su ILIAS, dove le immagini sono molto ingombre.
- **TIPSv2 è l'unica novità Apache-2.0 con un indizio sul recupero fine**: su UnED, che contiene anche prodotti al
  dettaglio (RP2k, SOP), la taglia g supera DINOv2-g di 4,3 punti. Ma l'indizio vale per la taglia più grande, non per
  la B, e manca il confronto con SigLIP 2 e PE-Core. La taglia B costa circa come una ViT-B a 448-512 px.
- **C-RADIO è interessante ma non risolve il problema della licenza.** Unisce SigLIP 2 e DINOv3 in un solo modello e
  ha valori k-NN alti, quindi potrebbe offrire risultati simili a DINOv3 senza la sua licenza (IPOTESI). Però la
  licenza NVIDIA è anch'essa propria, con la clausola che permette a NVIDIA di cambiarla, come quella di DINOv3; in più
  non ci sono risultati di recupero di istanze e il model card indica solo hardware NVIDIA. Va trattato come DINOv3:
  confronto facoltativo, dopo che l'utente ha letto la licenza.
- **Su CPU contano taglia e risoluzione più della famiglia.** Una ViT-B a circa 1.000 zone (448-512 px) costa
  circa 110 GMAC, una ViT-L circa 360; DINOv2 a 518 px costa di più (152 e 507) perché divide l'immagine in zone più
  piccole. DINOv2-L è il modello più costoso della prova ed è ultimo in tutti i confronti.
- **La leva più forte non è il modello.** Il ritaglio dell'oggetto vale su ILIAS +15,5 punti di mAP, più del distacco
  tra qualsiasi coppia di modelli. Nel nostro caso le foto di riferimento sono pulite e la foto di arrivo può avere
  sfondo ingombro, cioè il caso opposto di ILIAS: il ritaglio andrebbe fatto sulla foto di arrivo (IPOTESI).
- **VLM per riordinare**: l'approccio degli autori di ILIAS usa un modello linguistico multimodale per ogni coppia da
  riordinare; su CPU, con 5 proposte da confermare, sarebbe lento (IPOTESI, non misurato).

## Cosa resta incerto

- **TIPSv2-B e C-RADIOv3-B sulle nostre foto**: nessun risultato pubblico di recupero di istanze per queste taglie.
- **Licenza dei pesi di TIPS**: Apache-2.0 sul model card e "all other materials" CC-BY 4.0 nel repository. Entrambe
  permettono l'uso commerciale (CC-BY chiede l'attribuzione), ma la discrepanza va notata.
- **Licenze non lette per intero**: Qwen Research License (Jina v4), OpenMDW-1.1 (Nemotron-3.5-Embed), Health AI
  Developer Foundations (MedSigLIP). Li ho esclusi per il compito o per il costo, non solo per la licenza.
- **Esportazioni ONNX di terzi** (TIPSv2, C-RADIO, Qwen3-VL-Embedding): non provate; meglio esportare da timm o
  Transformers in proprio. Anche gli ONNX di PE-Core su onnx-community non hanno download.
- **Confronto a parità di condizioni**: nyris usa DINOv3 a 224 px e solo le taglie grandi; Bosch non include PE-Core;
  ILIAS non include TIPSv2 né C-RADIO. Nessuna fonte confronta tutti i candidati sullo stesso banco.
- **Ricerca non esaustiva**: ho cercato tra i modelli pubblicati su Hugging Face dagli autori principali (Google,
  Meta, NVIDIA, Apple, Microsoft, Alibaba Qwen, Jina, Nomic, BAAI, OpenGVLab, LAION, timm) e su arXiv. Modelli di altri
  gruppi possono essermi sfuggiti.
- **Mage-ViT**: MIT e gira su CPU, ma senza alcun risultato pubblicato; non valutabile.

## Proposta (DEDUZIONE)

**Lasciare invariato l'elenco della decisione 140** (SigLIP 2, PE-Core, DINOv2, ciascuno in taglia media e grande) e
la decisione 141 su DINOv3. Motivo: nessun modello nuovo con licenza commerciale ha risultati migliori sul recupero di
istanze o di prodotti; SigLIP 2 e PE-Core restano i migliori modelli Apache-2.0 misurati.

Una sola aggiunta facoltativa, se il tempo di calcolo della sessione lo permette: **TIPSv2-B/14** (Apache-2.0, circa
107 GMAC a 448 px, in timm). È l'unica novità con licenza libera e un indizio sul recupero fine. Se la prova va
alleggerita, il primo da togliere è **DINOv2 grande**: è il più costoso (507 GMAC a 518 px) ed è ultimo in tutti i
confronti trovati; DINOv2 medio basta come riferimento di base.

**Non aggiungere** C-RADIO per ora: licenza propria NVIDIA da far leggere all'utente, come per DINOv3, e nessun
risultato sul recupero di istanze. Escludere i modelli di embedding multimodali basati su VLM (Qwen3-VL-Embedding,
Jina, Nomic, Nemotron): molte volte più lenti su CPU (DEDUZIONE: da 1,5 a 8 miliardi di parametri contro 0,1-0,3) e, dove misurati,
peggiori.

Infine, i risultati del 2026 indicano che il **ritaglio della scatola nella foto di arrivo** può valere più del cambio di
modello: conviene tenerlo come prima prova di miglioramento dopo la prova di base, prima di cercare altri modelli.

---

## Fonti

Primarie (aperte il 17/11/2026):

- ILIAS, classifica: https://vrg.fel.cvut.cz/ilias/
- nyris, Visual Product Search Benchmark: https://arxiv.org/html/2603.17186 · https://benchmark.nyris.io/models · https://benchmark.nyris.io/models/hf-hub_timm_PE-Core-L-14-336
- Bosch, CVPR 2026 workshop: https://openaccess.thecvf.com/content/CVPR2026W/FGVC13/papers/Liu_Efficient_Fine-grained_Image_Retrieval_with_Vision_Foundation_Models_for_Industrial_CVPRW_2026_paper.pdf
- Rapporto oggetto/immagine e riordino con OWLv2: https://arxiv.org/html/2610.11489v1
- VLM come riordinatori: https://arxiv.org/abs/2604.13268
- TIPSv2: https://arxiv.org/html/2604.12012 · https://huggingface.co/google/tipsv2-b14 · https://github.com/google-deepmind/tips · https://huggingface.co/timm/vit_base_patch14_reg1_tipsv2.webli · https://huggingface.co/timm/vit_large_patch14_reg1_tipsv2.webli
- C-RADIO: https://github.com/NVlabs/RADIO · https://arxiv.org/html/2601.17237v1 · https://huggingface.co/nvidia/C-RADIOv4-SO400M · https://huggingface.co/nvidia/C-RADIOv3-B · https://huggingface.co/timm/vit_base_patch16_radio_v3.c_radio · https://huggingface.co/timm/vit_large_patch16_radio_v3.c_radio · https://huggingface.co/timm/vit_so400m_patch16_radio_v4.c_radio
- NVIDIA Open Model License: https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf
- RADIO1D: https://arxiv.org/pdf/2607.03624 · https://huggingface.co/nvidia/C-RADIOv4-1D-H
- Qwen3-VL-Embedding: https://huggingface.co/Qwen/Qwen3-VL-Embedding-2B
- Jina: https://huggingface.co/jinaai/jina-embeddings-v4 · https://huggingface.co/jinaai/jina-embeddings-v5-omni-small
- Nomic: https://huggingface.co/nomic-ai/nomic-embed-multimodal-3b
- NVIDIA Nemotron embed: https://huggingface.co/nvidia/llama-nemotron-embed-vl-1b-v2 · https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16
- MetaEncoder: https://huggingface.co/facebook/meta-encoder
- Mage-ViT: https://huggingface.co/microsoft/Mage-ViT
- Esclusi per licenza: https://huggingface.co/facebook/metaclip-2-worldwide-l14 · https://huggingface.co/facebook/webssl-dino300m-light2b-224 · https://huggingface.co/facebook/pixio-vitl16 · https://raw.githubusercontent.com/valeoai/Franca/main/LICENSE_MODEL · https://huggingface.co/apple/aimv2-large-patch14-224
- Perception Encoder, novità: https://github.com/facebookresearch/perception_models
- Riferimenti già scelti: https://huggingface.co/google/siglip2-large-patch16-512 · https://huggingface.co/facebook/PE-Core-L14-336 · https://huggingface.co/timm/vit_large_patch14_dinov2.lvd142m · https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m
- MIEB: https://arxiv.org/html/2504.10471
- ONNX: https://huggingface.co/onnx-community
- Licenze, accesso, parametri e date di creazione dei modelli: API pubblica di Hugging Face
  `https://huggingface.co/api/models/<id>` (campi `cardData.license`, `gated`, `safetensors.total`, `createdAt`) e
  `https://huggingface.co/api/models?author=<autore>&sort=createdAt&direction=-1`.

Secondarie (usate solo per orientarsi): risultati di ricerca web su C-RADIOv4, Qwen3-VL-Embedding, PE, SigLIP 3,
DINOv4 e GPR1200, poi verificati sulle fonti primarie dove indicato.

Pagine non raggiungibili: il repository GitHub dei risultati MTEB/MIEB (accesso non abilitato in questa sessione); il
PDF Bosch tramite lo strumento di lettura (scaricato e letto in locale).
