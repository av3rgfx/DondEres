# Lettura automatica delle bolle (DDT del fornitore) in sede

Data: 18/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina, model card, file LICENSE o articolo aperti il
18/11/2026). **DEDUZIONE** = conclusione nostra a partire dai fatti. **IPOTESI** = da verificare con una prova.
"Il produttore dichiara" = risultato pubblicato da chi ha fatto il modello, non verificato da altri. "Classifica" =
tabella pubblicata da chi mantiene un benchmark. Le date tra parentesi sono quelle della pagina o del rilascio, quando
la fonte le mostra; per le model card di Hugging Face è la data dell'ultima modifica del repository letta dalla sua API
(`lastModified`). Quando una pagina non era raggiungibile è scritto.

Questa ricerca non prende decisioni: dove serve una scelta scrive **proposta** o **da decidere**. I numeri tra
parentesi senza altra indicazione sono decisioni di `docs/decisioni.md`. Le quantità lette dalla bolla sono sempre
**«quantità in bolla»**, mai quantità contate (183, 192, 193).

Non si ripete la § 2 di `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (norma sul DDT, come entra il
documento del fornitore nei prodotti, servizi in cloud Azure, Google e Mindee, ASN e DESADV): qui si rimanda a essa.

## Domanda

Ticket «Lettura automatica delle bolle» (decisione 193). Si possono leggere in automatico tutti i dati di una bolla di
consegna (DDT italiano del fornitore), testata e righe con le quantità, **in sede, senza servizi cloud**?

- Da foto del telefono: rilevamento del foglio, ritaglio, raddrizzamento, contrasto «da scansione».
- Da PDF digitale: testo già presente o da riconoscere.
- Lettura di testata (fornitore, numero, data, ordine citato) e righe (codice, descrizione, quantità, unità).
- Addestrare o adattare un modello, oppure uno script per fornitore; quante bolle servono.
- Come si misura l'affidabilità: una prova su bolle vere di UFP con i dati dei clienti coperti.

Vincoli del progetto usati qui: web app aperta dal browser del telefono, servita da un server in sede (121, 126); il
DDT si crea scegliendo il fornitore (183) e il programma conosce gli ordini fornitore aperti (70, 183); numero e data
letti dalla foto si confermano (184); la quantità in bolla entra alla chiusura del DDT, con la foto della bolla davanti
(192); nessun tasto riempie la quantità attesa (186); i tempi si misurano per ora solo nella sessione di Claude (143).

## Sintesi

1. **Risposta: in parte sì, a condizioni.** La testata (numero, data, numero d'ordine citato) è leggibile in sede con
   strumenti open source a licenza commerciale. Le righe con codice e quantità sono leggibili da modelli recenti che
   girano in sede, ma nessuna fonte misura bolle italiane: l'affidabilità sulle bolle di UFP è **da misurare**. Oggi
   la lettura può **proporre** la quantità in bolla, non sostituire il controllo dell'operatore (192). (DEDUZIONE)
2. **Le classifiche pubbliche non bastano.** OmniDocBench, il benchmark più usato, contiene solo pagine cinesi e
   inglesi e nessun documento di trasporto ([OmniDocBench](https://github.com/opendatalab/OmniDocBench)); i benchmark
   delle righe (DocILE) sono fatture inglesi ([arXiv 2302.05658](https://arxiv.org/pdf/2302.05658)). Servono bolle vere.
   (FATTO + DEDUZIONE)
3. **Le foto storte sono il punto debole delle catene «classiche».** Su Real5-OmniDocBench (le stesse pagine
   rifotografate storte, piegate, con luce diversa) PP-StructureV3 scende da 84,68 (scansione) a 37,98 (foglio storto),
   mentre i modelli che leggono l'immagine intera restano sopra 90 (PaddleOCR-VL-1.6: 92,66; MiniCPM-OCR 1.0: 93,28)
   ([classifica Real5](https://huggingface.co/datasets/PaddlePaddle/Real5-OmniDocBench)). La classifica è dello stesso
   gruppo che fa PaddleOCR. (FATTO)
4. **Ritaglio e raddrizzamento si fanno con strumenti liberi**: OpenCV (Apache-2.0) e OpenCV.js nel browser,
   jscanify (MIT) che ritaglia il foglio dal video, UVDoc (MIT; anche dentro PaddleOCR) per i fogli piegati. Lo
   scanner di documenti di Android (ML Kit) e quello di iPhone (VisionKit) sono **solo per app native**: non si usano
   da una web app (121). (FATTO)
5. **PDF con testo: non serve leggere l'immagine.** pdfplumber e pdfminer.six (MIT) danno testo e posizione di ogni
   carattere; Camelot e Tabula (MIT) estraggono tabelle dai PDF con testo; Docling (MIT) fa entrambe le cose con
   TableFormer. **PyMuPDF è AGPL** (o licenza commerciale di Artifex) e **Poppler è GPL**: da evitare dentro il
   programma, o da valutare. (FATTO)
6. **Licenze: molti modelli famosi non vanno bene per un uso commerciale.** Pesi non commerciali o con soglie:
   LayoutLMv3 (CC BY-NC-SA 4.0), Qwen2.5-VL-3B e i suoi derivati (Nanonets-OCR, OCRFlux: licenza di ricerca),
   jina-ocr-v1 (CC BY-NC 4.0), DocTr (non commerciale), Marker/Surya/Chandra (gratis solo sotto una soglia di
   ricavi); HunyuanOCR **esclude l'Unione europea**. Licenze libere per i pesi: PaddleOCR e PaddleOCR-VL, Qwen3-VL e
   Qwen3.5, Gemma 4, GLM-OCR, MiniCPM-OCR, InternVL3.5, granite-docling, Mistral Small 3.2. (FATTO, tabella finale)
7. **Senza scheda grafica si può, ma i tempi sono da misurare.** PaddleOCR-VL dichiara il supporto su CPU x86 e ha un
   GGUF per llama.cpp; Qwen3-VL ha GGUF ufficiali (8B in 4 bit: file da 5,03 GB più 0,75 GB per la parte visiva).
   Nessun autore pubblica tempi su CPU per una pagina intera con questi modelli. Nella prova visiva PaddleOCR ha
   impiegato circa 18 secondi per foto sulla CPU della sessione (`docs/architettura.md`). (FATTO + DEDUZIONE)
8. **Il tempo conta meno del previsto.** Numero e data servono subito (184), ma le righe servono alla chiusura del DDT
   (192): la lettura completa può girare sul server mentre l'operatore conta la merce. (DEDUZIONE)
9. **Uscita in JSON valido**: llama.cpp e vLLM vincolano l'uscita a uno schema JSON; il JSON valido non vuol dire
   valori giusti. (FATTO + DEDUZIONE)
10. **Il controllo più forte è l'ordine aperto.** Il fornitore è già scelto (183): le righe lette si confrontano con i
    codici del fornitore negli ordini aperti, con le quantità residue e con il numero d'ordine stampato (70). Un codice
    letto che non esiste negli ordini aperti del fornitore è un segnale d'errore o di merce non prevista. (DEDUZIONE)
11. **Addestrare non è il primo passo.** Con 5.180 documenti di addestramento i modelli del 2023 arrivavano a F1 0,72
    sulle righe di DocILE; i modelli recenti leggono senza addestramento. Proposta: modello generale + controlli +
    «memoria» per fornitore delle correzioni; adattamento (LoRA) solo se la prova mostra errori sistematici. Quante
    bolle servono per un adattamento: nessuna fonte lo dice per i DDT, da misurare. (FATTO + DEDUZIONE)
12. **Proposta di prova**: circa 100–120 bolle vere, di 8–12 fornitori ricorrenti più 20–30 occasionali, ognuna
    fotografata due volte (bene e «come capita»), più i PDF quando ci sono; verità scritta a mano; 3 sistemi a
    confronto più la via del PDF con testo; traguardi **da decidere** con l'utente; esecuzione nella sessione di Claude.
13. **Le bolle vere di UFP viste il 18/11/2026** (3 fornitori, 10 foto) hanno impaginazioni molto diverse, più pagine,
    righe che non sono merce, due tipi di riferimento d'ordine, timbri e segni a penna. Su due fornitori su tre una
    parte dei dati è stampata anche in **codici a barre** (EAN per riga, DataMatrix con numero e data): si leggono con
    zxing-cpp senza OCR. Proposta: i codici stampati come primo passo della lettura. (FATTO + DEDUZIONE, sezione
    dedicata)
14. **Da decidere prima della prova**: dove conservare le bolle (la 130 oggi esclude i documenti dalle foto della prova
    visiva), quante e di quali fornitori, cosa si copre, quali traguardi.

## Cosa mostrano le bolle vere di UFP (18/11/2026)

Fonte: 10 foto da telefono di DDT di 3 fornitori (AGB/Alban Giacomo, ISEO Serrature, SAIT Abrasivi) e una lettera di
vettura del corriere SUSA, mostrate dall'utente in chat all'agente principale il 18/11/2026 e descritte da lui. Le
bolle non sono riprodotte qui; i riferimenti dei clienti sono omessi. È scritto FATTO solo ciò che l'agente principale
ha riferito di aver visto o provato.

### Impaginazioni

- FATTO: tre impaginazioni molto diverse.
  - **AGB**: tabella con colonne N.ORDINE / N.RIGA / ARTICOLO / DESCRIZIONE / U.M. / QUANTITÀ, su 4 pagine con la
    testata ripetuta, «Pag. 1/4» e «SEGUE».
  - **ISEO**: tabella a celle con un barcode Code 128 stampato sotto ogni riga (l'EAN-13 dell'articolo), quantità
    scritta «10,00», unità «pcs», numero e riga della conferma d'ordine del fornitore; testi in italiano e inglese;
    carta grigia.
  - **SAIT**: niente tabella; blocchi per posizione (Pos 000010; Materiale 1000000005; descrizione; «Codice EAN
    8028641000052»; quantità «200,00 PZ»), 3 pagine, data in formato ISO.
- FATTO: numeri DDT nei formati «23964/VI», «26-000046414», «1026039742»; date nei formati 13/11/26, 17/11/2026,
  2026-11-12.
- DEDUZIONE: un modulo per fornitore con regole fisse (§ 4.2) andrebbe scritto tre volte già per tre fornitori; i
  formati dei numeri e delle date confermano che serve una normalizzazione per fornitore (§ 3.4, controllo 2). Le
  quantità con la virgola decimale («10,00», «200,00») vanno lette all'italiana.

### Riferimenti d'ordine

- FATTO: due tipi di riferimento.
  - Il numero di **conferma d'ordine del fornitore** (AGB 2635577, ISEO 10098494).
  - Il numero dell'**ordine di UFP**: in AGB è una riga di sola descrizione «ord n …» sotto ogni gruppo; in ISEO è
    «Rif.Cliente/Ref.Customer: …»; in SAIT è «Ordine di riferimento …».
- FATTO: in AGB ogni gruppo ha un'intestazione «***Saldo Vs. Ord. del 08/10/26 2635577» oppure «***Acconto …», cioè
  ordine completato oppure consegna parziale.
- DEDUZIONE: l'ordine «indicato sul DDT» della decisione 70 è il numero d'ordine di UFP, che ogni fornitore scrive in
  un posto diverso; il numero di conferma del fornitore serve solo se il programma lo conosce (per esempio se l'ufficio
  lo registra sull'ordine). Una bolla può riferirsi a più ordini, uno per gruppo di righe (AGB). «Saldo» e «Acconto»
  sono un indizio utile per il residuo dell'ordine, non una quantità.

### Righe che non sono merce

- FATTO: compaiono intestazioni Saldo/Acconto, righe «ord n …», riferimenti del cliente scritti nella descrizione,
  pallet «A RENDERE» con codice Z99999PL00, testi legali, e in SAIT «Materiale ceduto a titolo di sconto merce» con lo
  stesso articolo su due posizioni.
- DEDUZIONE: la lettura deve dire per ogni riga **che tipo di riga è** (merce, sconto merce, imballo a rendere,
  intestazione, riferimento, testo); due righe dello stesso articolo (una a pagamento, una in sconto) sono due righe
  di quantità in bolla, da sommare per il confronto con la merce contata ma da tenere distinte per l'ufficio.

### Segni a mano, timbri, foto

- FATTO: sulle bolle d'archivio ci sono spunte a penna su ogni riga, quantità corrette a mano («240» accanto a 200),
  numeri d'ordine scritti a mano, evidenziatore, il timbro «REGISTRATO ARS LOGISTIC» sopra la testata e il timbro
  «ACCETTATO CON RISERVA…» con la data a mano.
- FATTO: nel nuovo flusso la foto si scatta all'apertura del DDT (184), quindi prima dei segni a penna.
- FATTO: nelle foto ci sono fogli curvi, ombre, altri fogli sovrapposti, pagine un po' ruotate, puntini di toner.
- DEDUZIONE: le bolle d'archivio sono più difficili di quelle che il programma vedrà davvero; nella prova vanno
  separate («con segni» / «senza segni») o rifotografate pulite quando è possibile. Una quantità corretta a mano è
  proprio il caso in cui la lettura **non** deve proporre la quantità stampata come buona: va segnalata.

### Codici stampati: prova dell'agente principale

- FATTO: con zxing-cpp 3.1.1 (Apache-2.0; licenza già verificata in
  `docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md`, § G) sulle foto intere sono stati letti 8 barcode
  di riga su 9 nella bolla ISEO (Code 128 con l'EAN dell'articolo).
- FATTO: nella bolla AGB il DataMatrix in alto a destra contiene «IG01092026111323964VI», cioè la data 2026-11-13 e il
  numero 23964VI; è stato letto sulle pagine 1, 2 e 3 (ritagliando l'angolo), non sulla 4.
- DEDUZIONE: per alcuni fornitori testata e articoli si leggono **senza OCR**, dai codici stampati, in modo esatto o
  per nulla (un barcode letto non ha cifre «quasi giuste»); il DataMatrix ripetuto tiene insieme le pagine dello stesso
  DDT. L'EAN letto si cerca negli articoli (barcode già collegati, 92) e la quantità resta da leggere dal testo accanto.
  Il contenuto del DataMatrix di AGB è un formato del fornitore, da interpretare con una regola per quel fornitore.

### Lettera di vettura

- FATTO: la lettera di vettura SUSA porta colli, peso e «Rif. Mittente 0023964 del 13/11/2026», che rimanda al DDT.
- DEDUZIONE: il programma deve riconoscere che non è un DDT (niente righe di merce) e non crearne uno; il riferimento
  del mittente e i colli possono servire per collegarla al DDT e per un controllo sul numero di colli arrivati.

## 1. Da foto del telefono

### 1.1 Strumenti per ritagliare, raddrizzare e pulire

- FATTO: OpenCV è sotto Apache-2.0 ([LICENSE](https://github.com/opencv/opencv/blob/master/LICENSE)). La trasformazione
  prospettica richiede «4 points on the input image and corresponding points on the output image. Among these 4 points,
  3 of them should not be collinear», poi `cv.getPerspectiveTransform` e `cv.warpPerspective`
  ([tutorial, sorgente su GitHub](https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.markdown)).
  La soglia adattiva calcola una soglia diversa per ogni zona e dà «better results for images with varying
  illumination» ([tutorial soglie](https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.markdown)).
  Le pagine su docs.opencv.org hanno risposto «403 Forbidden» a questa sessione: si sono letti i sorgenti della
  documentazione sul repository.
- FATTO: OpenCV.js è «a JavaScript binding for selected subset of OpenCV functions for the web platform», compilato
  con Emscripten in WebAssembly ([introduzione](https://github.com/opencv/opencv/blob/4.x/doc/js_tutorials/js_setup/js_intro/js_intro.markdown)).
  Il pacchetto npm `@techstark/opencv-js` 5.0.0 è Apache-2.0 e pesa circa 14,7 MB non compresso
  ([registro npm](https://registry.npmjs.org/@techstark/opencv-js/latest)).
- FATTO: jscanify (MIT, [LICENSE](https://github.com/puffinsoft/jscanify/blob/master/LICENSE)), versione 1.4.3
  (20/07/2026, [npm](https://registry.npmjs.org/jscanify)), «Powered with opencv.js», fa «paper detection &
  highlighting» e «paper scanning with distortion correction», anche dal video della fotocamera con `getUserMedia`;
  dalla 1.3.0 dichiara «glare suppression» ([README](https://github.com/puffinsoft/jscanify)). Il raddrizzamento è
  prospettico (quattro angoli), non corregge un foglio piegato. (DEDUZIONE dal nome delle funzioni `extractPaper` con
  larghezza e altezza)
- FATTO: UVDoc (raddrizzamento di fogli piegati con una rete neurale) ha codice sotto MIT
  ([LICENSE](https://github.com/tanguymagne/UVDoc/blob/main/LICENSE)). PaddleOCR lo include come modulo «Text Image
  Rectification»: CER 0,179 sul benchmark DocUNet, 19 ms su GPU T4, 870 ms su CPU Xeon Gold 6271C (8 thread, modalità
  ad alte prestazioni), 30,3 MB ([documentazione PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/module_usage/text_image_unwarping.en.md)).
  Il produttore dichiara; il tempo è del solo modello.
- FATTO: DocRes (CVPR 2024) fa in un modello raddrizzamento, rimozione ombre, miglioramento dell'aspetto, rimozione
  sfocatura e binarizzazione; codice MIT ([LICENSE](https://github.com/ZZZHANG-jx/DocRes/blob/master/LICENSE),
  [README](https://github.com/ZZZHANG-jx/DocRes)). I pesi si scaricano da un link OneDrive senza una licenza propria
  scritta nel README: licenza dei pesi **non chiara**.
- FATTO: DocTr (raddrizzamento, Hao Feng) ha una licenza propria: «Any Commercial Use of the Algorithm is strictly
  prohibited without explicit prior written permission» ([LICENSE.md](https://github.com/fh2019ustc/DocTr/blob/main/LICENSE.md)).
  **Escluso.** (Da non confondere con docTR di Mindee, un OCR, § 3.1.)

### 1.2 Scanner di sistema di Android e iPhone

- FATTO: ML Kit Document Scanner è descritto solo per Android; «The entire document scanner flow operates on-device»;
  fa rilevamento dei bordi, ritaglio, rotazione, filtri, rimozione di ombre e macchie, più pagine
  ([panoramica](https://developers.google.com/ml-kit/vision/doc-scanner)). Si aggiunge all'app con la dipendenza Gradle
  `play-services-mlkit-document-scanner:16.0.0`, API 21 o superiore, almeno 1,7 GB di RAM, uscita JPEG e PDF
  ([Android](https://developers.google.com/ml-kit/vision/doc-scanner/android)). Le pagine non citano il web.
- FATTO: `VNDocumentCameraViewController` (VisionKit) è «An object that presents UI for a camera pass-through that helps
  people scan physical documents», per iOS e iPadOS 13.0 e successivi, Mac Catalyst e visionOS
  ([documentazione Apple, versione JSON](https://developer.apple.com/tutorials/data/documentation/visionkit/vndocumentcameraviewcontroller.json);
  la pagina HTML si carica con JavaScript e non era leggibile come testo).
- DEDUZIONE: entrambi sono API per app native (Kotlin/Java, Swift/UIKit). Una web app aperta da Safari o Chrome non le
  può chiamare. Con la decisione 121 (niente app installata) restano fuori.
- IPOTESI da provare sui telefoni: dal tasto «scegli file» della pagina l'utente può forse passare da un'app del
  telefono che scansiona (per esempio l'app File su iPhone o Google Drive su Android) e caricare il PDF risultante. È
  un giro in più per l'operatore; non verificato.

### 1.3 Cosa si fa nel browser e cosa sul server

- FATTO: l'attributo `capture` di `<input type="file">` (apre la fotocamera del telefono) è supportato da Chrome per
  Android dalla 25 e da Safari per iOS dalla 10 ([MDN browser-compat-data, input](https://github.com/mdn/browser-compat-data/blob/main/html/elements/input.json)).
  `ImageCapture.takePhoto()` (foto a piena risoluzione da `getUserMedia`) c'è in Chrome dalla 60 e in Safari dalla
  18.4 ([MDN browser-compat-data, ImageCapture](https://github.com/mdn/browser-compat-data/blob/main/api/ImageCapture.json)).
- FATTO (progetto): la pagina di scatto della prova visiva salva foto dal video con il lato lungo al massimo di 1.920
  pixel (`docs/architettura.md`, sezione «Prova di accuratezza visiva»).
- DEDUZIONE (calcolo nostro): su un A4 fotografato intero, 1.920 pixel sul lato lungo sono circa 6,5 pixel per
  millimetro; una cifra alta 2,5 mm (carattere da circa 10 punti) occupa circa 16 pixel, al limite dei «16×16 pixel»
  minimi che ML Kit indica per i caratteri (già citato in `docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md`,
  § G). Per le bolle conviene la foto a piena risoluzione (`capture` o `takePhoto`), non il fotogramma del video.
  Da verificare nella prova.
- DEDUZIONE: divisione proposta.
  - **Nel browser**: anteprima con il contorno del foglio (jscanify/OpenCV.js) per aiutare a inquadrare; scatto a
    piena risoluzione; eventuale ritaglio prospettico per mostrare all'operatore cosa è stato preso; più pagine una
    dopo l'altra. Costo: circa 15 MB di OpenCV.js da scaricare la prima volta (FATTO sulla dimensione, sopra).
  - **Sul server**: la foto originale (sempre conservata, 184), il raddrizzamento dei fogli piegati (UVDoc), la
    lettura. I modelli recenti (§ 3.3) leggono anche foto storte senza ritaglio (Real5, sotto): il ritaglio nel
    browser serve soprattutto a guidare lo scatto e a mostrare la bolla «da scansione».
  - Il contrasto «da scansione» (soglia adattiva) è utile da **mostrare** e da archiviare in piccolo; per la lettura
    con i modelli neurali la binarizzazione può togliere informazione (IPOTESI: da misurare con e senza).

### 1.4 Quanto pesano foto storte, pieghe, luce

- FATTO (classifica Real5-OmniDocBench, ECCV 2026, 1.355 pagine di OmniDocBench v1.5 rifatte in 5 condizioni: 6.775
  immagini): punteggio complessivo per condizione ([dataset e classifica](https://huggingface.co/datasets/PaddlePaddle/Real5-OmniDocBench),
  [articolo](https://arxiv.org/abs/2603.04205)).

  | Sistema | Scansione | Piegato | Foto di schermo | Luce | Storto |
  |---|---|---|---|---|---|
  | MiniCPM-OCR 1.0 (1,3B) | 94,45 | 93,54 | 93,74 | 93,74 | 93,28 |
  | PaddleOCR-VL-1.6 (0,9B) | 94,74 | 92,48 | 92,78 | 93,28 | 92,66 |
  | GLM-OCR (0,9B) | 92,67 | 90,68 | 91,75 | 91,12 | 85,39 |
  | Qwen3-VL-235B | 89,43 | 89,99 | 89,27 | 89,27 | 86,56 |
  | dots.ocr (3B) | 86,87 | 86,01 | 87,18 | 87,57 | 84,27 |
  | DeepSeek-OCR 2 (3B) | 89,59 | 66,53 | 71,65 | 76,02 | 61,28 |
  | PP-StructureV3 (catena classica) | 84,68 | 59,34 | 66,89 | 73,38 | 37,98 |
  | Marker 1.8.2 (catena classica) | 70,27 | 58,98 | 63,65 | 66,31 | 41,27 |

- DEDUZIONE: la catena «rileva le righe di testo → riconosci → ricomponi» soffre molto se il foglio è storto o
  piegato; i modelli che leggono l'immagine intera molto meno. Il benchmark è stato costruito da PaddlePaddle, autore
  di due dei sistemi in classifica: va letto con questa cautela.
- Limiti non misurati da nessuna fonte trovata su documenti di trasporto: carta stropicciata o bagnata, carta
  chimica/copia carbone sbiadita, timbri sopra le righe, correzioni e quantità scritte a mano dal trasportatore,
  bolle di più pagine con righe spezzate tra le pagine. PaddleOCR-VL-1.6 dichiara miglioramenti su timbri («seal/stamp
  recognition», [model card](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6), 06/11/2026); Nemotron Parse 2.0
  riporta un forte miglioramento sulle note scritte a mano di OmniDocBench (distanza di modifica da 0,9739 a 0,3395,
  [model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0)). Su bolle vere: **da misurare**.

## 2. Da PDF digitale

### 2.1 PDF con il testo dentro

| Strumento | Licenza (file letto) | Cosa fa | Nota |
|---|---|---|---|
| pdfplumber 0.11.10 | MIT ([LICENSE.txt](https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt)) | Testo con posizione di ogni carattere, linee, rettangoli, tabelle | «Works best on machine-generated, rather than scanned, PDFs», basato su pdfminer.six ([README](https://github.com/jsvine/pdfplumber)) |
| pdfminer.six 20260107 | MIT ([LICENSE](https://github.com/pdfminer/pdfminer.six/blob/master/LICENSE)) | Estrazione del testo con le coordinate | Base di pdfplumber |
| PyMuPDF 2.1 | **AGPL-3.0** o licenza commerciale Artifex ([COPYING](https://github.com/pymupdf/PyMuPDF/blob/main/COPYING), [PyPI](https://pypi.org/project/pymupdf/)) | Veloce, testo e immagini delle pagine | L'AGPL obbliga a dare il codice a chi usa il programma in rete: da evitare nel prodotto (DEDUZIONE, non parere legale) |
| Poppler (`pdftotext`) | **GPL-2.0** ([COPYING](https://gitlab.freedesktop.org/poppler/poppler/-/blob/master/COPYING)) | Testo e immagini delle pagine | «programs which call Poppler must be licensed under the GPL as well» ([README](https://gitlab.freedesktop.org/poppler/poppler/-/blob/master/README.md)) |
| pypdfium2 5.15.2 | BSD-3-Clause e Apache-2.0 ([PyPI](https://pypi.org/project/pypdfium2/)) | Trasforma le pagine in immagini (PDFium) | Alternativa con licenza libera per passare il PDF a un modello visivo |
| pdf.js (`pdfjs-dist` 6.5.438) | Apache-2.0 ([npm](https://registry.npmjs.org/pdfjs-dist/latest)) | Mostra il PDF nel browser | Per la vista della bolla accanto alle righe (192) |

### 2.2 Tabelle nei PDF con testo

- FATTO: Camelot 2.0.0 (MIT, [LICENSE](https://github.com/camelot-dev/camelot/blob/master/LICENSE)) ha i modi
  `lattice` (tabelle con le linee), `stream` e `network` (tabelle senza linee), `ml` (Table Transformer) e da poco
  anche OCR per i PDF senza testo; i modi classici «need a text-based PDF»
  ([README](https://github.com/camelot-dev/camelot)).
- FATTO: tabula-py (MIT) richiede Java 8+ perché usa tabula-java (MIT)
  ([README](https://github.com/chezou/tabula-py), [LICENSE tabula-java](https://github.com/tabulapdf/tabula-java/blob/master/LICENSE)).
- FATTO (vecchio confronto riportato da IBM): sulla struttura delle tabelle (TEDS), Tabula 67,9, Camelot 73,0,
  Acrobat Pro 65,3, TableFormer 93,6 ([docling-models](https://huggingface.co/docling-project/docling-models)). Misura
  dell'autore di TableFormer, su tabelle di articoli scientifici.

### 2.3 Docling e i suoi modelli

- FATTO: Docling 2.150.1 (14/11/2026) è MIT ([LICENSE](https://github.com/docling-project/docling/blob/main/LICENSE),
  [PyPI](https://pypi.org/project/docling/)); dichiara «Local execution capabilities for sensitive data and air-gapped
  environments», «Extensive OCR support for scanned PDFs and images» e il supporto a modelli visivi come
  granite-docling ([README](https://github.com/docling-project/docling)). Come OCR può usare RapidOCR, EasyOCR,
  Tesseract e altri ([pipeline_options.py](https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py)).
- FATTO: i modelli di layout e TableFormer sono pubblicati con licenze CDLA-Permissive-2.0 e Apache-2.0
  ([docling-models](https://huggingface.co/docling-project/docling-models), 03/12/2025); il codice dei modelli
  (`docling-ibm-models`) è MIT ([LICENSE](https://github.com/docling-project/docling-ibm-models/blob/main/LICENSE)).
- FATTO: granite-docling-258M è Apache-2.0, lingua «English», giapponese, arabo e cinese «experimental»
  ([model card](https://huggingface.co/ibm-granite/granite-docling-258M), 23/09/2025). SmolDocling-256M-preview è
  CDLA-Permissive-2.0 e dichiara «Avg of 0.35 secs per page on A100 GPU»
  ([model card](https://huggingface.co/ds4sd/SmolDocling-256M-preview)).
- DEDUZIONE: Docling è un buon contenitore per i PDF (testo, tabelle, OCR quando serve), con licenza libera. Il suo
  modello visivo piccolo è dichiarato per l'inglese: sulle bolle italiane fotografate non è il primo candidato.

### 2.4 Marker, Surya, MinerU, olmOCR

- FATTO: Marker e Surya hanno oggi il **codice** sotto Apache-2.0 ([LICENSE Marker](https://github.com/datalab-to/marker/blob/master/LICENSE),
  [LICENSE Surya](https://github.com/datalab-to/surya/blob/master/LICENSE)), ma i **pesi** «use a modified AI Pubs
  Open Rail-M license (free for research, personal use, and startups under $5M funding/revenue)»
  ([README Marker](https://github.com/datalab-to/marker), [README Surya](https://github.com/datalab-to/surya)).
  Per Chandra OCR 2 la soglia scritta è «$2M» e i pesi «Cannot be used competitively with our API»
  ([model card](https://huggingface.co/datalab-to/chandra-ocr-2)).
- FATTO: il codice di MinerU ha la «MinerU Open Source License»: Apache-2.0 più termini aggiuntivi (licenza commerciale
  separata oltre 100 milioni di utenti al mese o 20 milioni di dollari di ricavi al mese; obbligo di citare MinerU nei
  servizi online) ([LICENSE.md](https://github.com/opendatalab/MinerU/blob/master/LICENSE.md)). Il modello
  MinerU2.5-2509-1.2B su Hugging Face è invece etichettato **AGPL-3.0**
  ([API Hugging Face](https://huggingface.co/api/models/opendatalab/MinerU2.5-2509-1.2B)). Licenza dei pesi da chiarire.
- FATTO: olmOCR (Ai2) ha codice e pesi Apache-2.0; olmOCR-2-7B deriva da Qwen2.5-VL-7B
  ([model card](https://huggingface.co/allenai/olmOCR-2-7B-1025), [LICENSE](https://github.com/allenai/olmocr/blob/main/LICENSE)).
  Il README dice «it requires a GPU», NVIDIA con almeno 12 GB ([README](https://github.com/allenai/olmocr)); lingua
  della model card: inglese.

### 2.5 PDF scansionati

- DEDUZIONE: un PDF senza testo (scansione dell'ufficio o del fornitore) è una serie di immagini: si trasforma in
  pagine (pypdfium2) e segue la strada della foto (§ 3), senza i problemi di prospettiva. Il programma deve capire da
  solo se il testo c'è: per esempio se pdfplumber trova testo sulla pagina.

## 3. Lettura di testata e righe

### 3.1 OCR classici (leggono il testo, non capiscono la bolla)

| Strumento | Licenza | Italiano | CPU | Nota |
|---|---|---|---|---|
| PaddleOCR 3.7.0 (11/06/2026), PP-OCRv5 e PP-OCRv6 | Apache-2.0 ([LICENSE](https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE), [PyPI](https://pypi.org/project/paddleocr/)) | Sì: il modello latino di PP-OCRv5 elenca l'italiano ([documentazione](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.en.md)); PP-OCRv6 dichiara 50 lingue «including Chinese, English, Japanese, and 46 Latin-script languages» senza l'elenco nella pagina letta ([OCR.en.md](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md)) | Sì. Rilevamento PP-OCRv5 server 383 ms su Xeon Gold 6271C, solo il modello (stessa pagina); PP-OCRv6 dichiara «5.2× CPU speedup (OpenVINO)» ([README](https://github.com/PaddlePaddle/PaddleOCR)) | Già scelto per il codice stampato (145). Nella sessione di Claude: circa 18 s per foto e 7,7 GB di picco (`docs/architettura.md`) |
| PP-StructureV3 (in PaddleOCR) | Apache-2.0 | Come sopra | Sì | Pagina → Markdown/JSON con coordinate di celle e testo ([README](https://github.com/PaddlePaddle/PaddleOCR)); debole sulle foto storte (§ 1.4) |
| Tesseract | Apache-2.0 ([LICENSE](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE)) | Sì: `ita.traineddata` in [tessdata_best](https://github.com/tesseract-ocr/tessdata_best) (Apache-2.0) | Sì | In OmniDocBench v1.5 e precedenti; non nella classifica v1.6 letta |
| docTR (Mindee) 1.1.0 | Apache-2.0 ([LICENSE](https://github.com/mindee/doctr/blob/main/LICENSE)) | Vocabolario `italian` presente ([vocabs.py](https://github.com/mindee/doctr/blob/main/doctr/datasets/vocabs.py)); i modelli pre-addestrati predefiniti non sono stati verificati per l'italiano | Sì | Ha un «KIE predictor» con rilevatore a più classi da addestrare ([README](https://github.com/mindee/doctr)) |
| EasyOCR 1.7.2 (24/09/2024) | Apache-2.0 ([LICENSE](https://github.com/JaidedAI/EasyOCR/blob/master/LICENSE)) | «80+ supported languages» ([README](https://github.com/JaidedAI/EasyOCR)) | Sì | Ultima versione del 2024 ([PyPI](https://pypi.org/project/easyocr/)) |
| RapidOCR 3.10.0 | Apache-2.0 ([LICENSE](https://github.com/RapidAI/RapidOCR/blob/main/LICENSE)) | Modelli di PaddleOCR convertiti; predefiniti cinese e inglese ([README](https://github.com/RapidAI/RapidOCR)) | Sì, ONNX Runtime, OpenVINO | Usato da Docling |

DEDUZIONE: un OCR classico dà righe di testo con la posizione. Per ricavare «codice, descrizione, quantità, unità»
servono regole (colonne, parole come «Q.tà», «UM», «Cod. art.») o un modello che capisce la pagina. Le regole
funzionano bene su un modulo fisso e stampato pulito; si rompono a ogni modulo nuovo e con le foto storte (§ 1.4).

### 3.2 Modelli di comprensione dei documenti «di prima generazione»

- FATTO: Donut (NAVER) ha codice e pesi MIT ([LICENSE](https://github.com/clovaai/donut/blob/master/LICENSE),
  [donut-base](https://huggingface.co/naver-clova-ix/donut-base)); su CORD (scontrini indonesiani) il modello addestrato
  fa 91,3 di accuratezza a distanza d'albero (TED) in 0,7 s per immagine, con un esempio di valutazione che dà F1 0,84
  sui campi ([README](https://github.com/clovaai/donut)). Il pre-addestramento sintetico è in inglese, cinese,
  giapponese e coreano (stesso README). CORD ha 800 immagini di addestramento, 100 di sviluppo e 100 di prova
  ([CORD](https://github.com/clovaai/cord)).
- FATTO: LayoutLMv3 ha i pesi sotto **CC BY-NC-SA 4.0** ([model card](https://huggingface.co/microsoft/layoutlmv3-base),
  [README](https://github.com/microsoft/unilm/tree/master/layoutlmv3)); F1 su FUNSD 0,9059 (base) e 0,9215 (large)
  (stesso README). FUNSD ha 199 moduli annotati ([FUNSD](https://guillaumejaume.github.io/FUNSD/)). **Escluso per la
  licenza.**
- FATTO: LiLT ha codice e pesi MIT ([LICENSE](https://github.com/jpWang/LiLT/blob/main/LICENSE),
  [lilt-roberta-en-base](https://huggingface.co/SCUT-DLVCLab/lilt-roberta-en-base)). UDOP: pesi MIT
  ([udop-large](https://huggingface.co/microsoft/udop-large)).
- DEDUZIONE: questi modelli vanno **addestrati** sui propri documenti (centinaia di esempi nei dataset citati) e non
  sono pensati per l'italiano. Sono superati, per chi non vuole addestrare, dai modelli del § 3.3.

### 3.3 Modelli che leggono l'immagine e scrivono testo, eseguibili in sede

Due famiglie:

- **Lettori di documenti specializzati** (0,3–5 miliardi di parametri): trasformano la pagina in Markdown o JSON con
  le tabelle; alcuni estraggono campi da uno schema JSON.
- **Modelli generali** (2–30 miliardi): rispondono a una richiesta, per esempio «restituisci testata e righe in
  questo schema JSON».

**Classifica OmniDocBench v1.6** (pagine cinesi e inglesi; punteggio complessivo = media di testo, formule e
tabelle; [README OmniDocBench](https://github.com/opendatalab/OmniDocBench), aggiornato al 12/11/2026). Alcuni valori:
OXR-1.0 97,03; MiniCPM-OCR 1.0 96,44; PaddleOCR-VL-1.6 96,34; MinerU2.5-Pro 95,75; GLM-OCR 95,22; Unlimited-OCR 94,00;
Qianfan-OCR 93,90; dots.ocr 90,77; DeepSeek-OCR 2 90,25; Qwen3-VL-235B 89,78; olmOCR 85,74; Nanonets-OCR-s 83,61;
Marker 78,44. FATTO; DEDUZIONE: le formule, che pesano un terzo, nelle bolle non ci sono; il testo e le tabelle sì.

Risultati dei modelli generali piccoli dichiarati dagli autori:

- FATTO: Qwen3-VL (Apache-2.0 tutte le taglie lette: 2B, 4B, 8B, 30B-A3B; [API Hugging Face](https://huggingface.co/api/models/Qwen/Qwen3-VL-8B-Instruct)).
  Rapporto tecnico, tabella 4, versioni «instruct»: DocVQA 93,3 (2B), 95,3 (4B), 96,1 (8B); OCRBench 858, 881, 896;
  CC-OCR 72,8, 76,2, 79,9; OmniDocBench inglese (distanza, più bassa è meglio) 0,292, 0,244, 0,170
  ([arXiv 2511.21631](https://arxiv.org/pdf/2511.21631)). OCR in 39 lingue, sopra il 70% in 32; l'elenco è in una
  figura non leggibile come testo, quindi **italiano non verificato** (stesso articolo). GGUF ufficiali: 8B in Q4_K_M
  5,03 GB più parte visiva 0,75 GB (Q8_0); 4B in Q4_K_M 2,50 GB più 0,45 GB
  ([Qwen3-VL-8B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct-GGUF),
  [Qwen3-VL-4B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct-GGUF)).
- FATTO: Qwen3.5 (febbraio 2026, Apache-2.0, multimodale) dichiara 201 lingue; 9B: OmniDocBench 1.5 87,7, CC-OCR 79,3,
  OCRBench 89,2; 4B: 86,2, 76,7, 85,0 ([model card 9B](https://huggingface.co/Qwen/Qwen3.5-9B)). GGUF di terzi
  (Unsloth): 9B Q4_K_M 5,68 GB più 0,92 GB ([file](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF)). Esiste anche
  Qwen3.6-35B-A3B, Apache-2.0 ([API](https://huggingface.co/api/models/Qwen/Qwen3.6-35B-A3B)).
- FATTO: Qwen2.5-VL ha licenze diverse per taglia: 3B «Qwen RESEARCH LICENSE» («"Non-Commercial" shall mean for
  research or evaluation purposes only»), 7B e 32B Apache-2.0, 72B licenza Qwen con soglia di 100 milioni di utenti
  ([LICENSE 3B](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/blob/main/LICENSE),
  [LICENSE 72B](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct/blob/main/LICENSE)). DEDUZIONE: i modelli derivati
  dal 3B (Nanonets-OCR-s, Nanonets-OCR2-3B, OCRFlux-3B) ereditano il problema; la model card di Nanonets-OCR2-3B non
  indica una licenza e non ha un file LICENSE (risposta 404).
- FATTO: Gemma 4 (2026) ha pesi Apache-2.0: il link della licenza porta a `gemma.ai/resources/apache-2/`
  ([model card E4B](https://huggingface.co/google/gemma-4-E4B-it), 03/11/2026). OmniDocBench 1.5 (distanza):
  0,181 (E4B), 0,290 (E2B), 0,164 (12B), 0,131 (31B); «Out-of-the-box support for 35+ languages, pre-trained on 140+
  languages»; per OCR consiglia il budget di token visivi più alto (1120) (stessa model card). GGUF E4B Q4_K_M 4,98 GB
  più 0,99 GB ([file](https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF)).
- FATTO: Gemma 3 e Gemma 3n hanno le «Gemma Terms of Use» con una politica d'uso vietato incorporata, accesso su
  richiesta ([termini](https://ai.google.dev/gemma/terms), modificati il 01/04/2026;
  [gemma-3-4b-it](https://huggingface.co/api/models/google/gemma-3-4b-it)).
- FATTO: InternVL3.5 (2B, 4B, 8B) Apache-2.0, con Qwen3 come componente Apache-2.0
  ([model card 8B](https://huggingface.co/OpenGVLab/InternVL3_5-8B)). MiniCPM-V 4.5 (8B) ora «open-sourced under the
  Apache-2.0 license» con un questionario di registrazione facoltativo, supporto llama.cpp e Ollama «for efficient CPU
  inference» ([model card](https://huggingface.co/openbmb/MiniCPM-V-4_5), 09/11/2026).
- FATTO: Mistral Small 3.2 24B e Pixtral 12B Apache-2.0, italiano tra le lingue dichiarate; Mistral Small 3.2 «requires
  ~55 GB of GPU RAM in bf16 or fp16» ([model card](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506),
  [Pixtral](https://huggingface.co/mistralai/Pixtral-12B-2409)). Ministral 3 8B (Apache-2.0, visione, italiano) «fitting
  in 12GB of VRAM in FP8» ([model card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512)).
- FATTO: Florence-2 (MIT, 0,77B) ha un compito `<OCR>` ma la model card avverte che la versione continuata «might not
  be trained well» ([model card](https://huggingface.co/microsoft/Florence-2-large)). SmolVLM e SmolVLM2: Apache-2.0,
  lingua inglese ([SmolVLM2-2.2B](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct)).

Lettori di documenti specializzati recenti (licenza dei pesi dalla model card o dall'API di Hugging Face):

- FATTO: **PaddleOCR-VL-1.6** (0,9B, Apache-2.0, 28/05/2026): «96.33%» su OmniDocBench v1.6 (il produttore dichiara,
  confermato dalla classifica sopra), timbri, tabelle, «text spotting» ([model card](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6)).
  La versione 1.0 dichiarava 109 lingue ([README](https://github.com/PaddlePaddle/PaddleOCR)). Supporto CPU x86 con
  PaddlePaddle e con Transformers; GGUF ufficiale per llama.cpp (0,94 GB più 0,88 GB); la guida consiglia comunque
  GPU per la parte di layout del client ([documentazione PaddleOCR-VL](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/PaddleOCR-VL.en.md),
  [GGUF](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6-GGUF)).
- FATTO: **MiniCPM-OCR 1.0** (1,3B, Apache-2.0 per pesi, codice e documentazione, ottobre 2026): testo, tabelle,
  timbri e «key information extraction»; lingue principali «Chinese and English»; vLLM, SGLang, llama.cpp, Ollama; GGUF
  Q4_K_M 0,53 GB più 0,90 GB ([model card](https://huggingface.co/openbmb/MiniCPM-OCR-1.0),
  [GGUF](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-gguf)). Primo su Real5 (§ 1.4).
- FATTO: **GLM-OCR** (0,9B dichiarati, pesi MIT, codice dell'SDK Apache-2.0): «Information Extraction» con richiesta
  in forma di schema JSON; vLLM, SGLang, Ollama; lingue elencate zh, en, fr, es, ru, de, ja, ko (non l'italiano)
  ([model card](https://huggingface.co/zai-org/GLM-OCR), [LICENSE SDK](https://github.com/zai-org/GLM-OCR/blob/main/LICENSE)).
  GGUF 0,95 GB più 0,48 GB ([file](https://huggingface.co/ggml-org/GLM-OCR-GGUF)).
- FATTO: **Xiaomi-OCR-0** (0,8B, Apache-2.0, da Qwen3.5-0.8B, 30/09/2026): parsing, VQA e KIE con schema JSON;
  dichiara 95,24 su Real5 e 96,83 su OmniDocBench v1.6; GGUF di terzi
  ([model card](https://huggingface.co/xiaomi-research/Xiaomi-OCR-0)). Nella classifica Real5 letta risulta 92,73:
  numeri diversi dalla model card, da chiarire.
- FATTO: **Qianfan-OCR** (4B, Apache-2.0): «Overall mean score of 87.9 across five public KIE benchmarks», contro 83,5
  di Qwen3-4B-VL e 79,2 di Gemini-3.1-Pro nella stessa tabella; 192 lingue dichiarate; 1,024 pagine al secondo su una
  A100 ([model card](https://huggingface.co/baidu/Qianfan-OCR)). Il produttore dichiara.
- FATTO: **dots.ocr** (3B, MIT), **DeepSeek-OCR** (MIT) e **DeepSeek-OCR-2** (Apache-2.0), **Unlimited-OCR** e
  **Unlimited-OCR-2** (Baidu, MIT, ottobre 2026, pensato per documenti di molte pagine), **LightOnOCR-2-1B**
  (Apache-2.0, italiano tra le lingue), **Infinity-Parser2-Flash** (Apache-2.0, «primarily supports English and
  Chinese»), **GOT-OCR2** (Apache-2.0), **MonkeyOCR-pro-3B** (Apache-2.0 nel README, ma «do not yet fully support
  for photographed text, handwritten content […] or multilingual text») (model card: [dots.ocr](https://huggingface.co/rednote-hilab/dots.ocr),
  [DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR), [DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2),
  [Unlimited-OCR-2](https://huggingface.co/baidu/Unlimited-OCR-2), [LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B),
  [Infinity-Parser2-Flash](https://huggingface.co/infly/Infinity-Parser2-Flash), [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0),
  [MonkeyOCR-pro-3B](https://huggingface.co/echo840/MonkeyOCR-pro-3B)).
- FATTO, licenze da escludere o da valutare: **HunyuanOCR** «DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND
  SOUTH KOREA» ([LICENSE](https://huggingface.co/tencent/HunyuanOCR/blob/main/LICENSE)); **jina-ocr-v1** CC BY-NC 4.0
  ([model card](https://huggingface.co/jinaai/jina-ocr-v1)); **Nemotron Parse 2.0** e **Nemotron 3.5 Parse** sotto
  OpenMDW-1.1 (permesso ampio, «free of charge, to deal in the Model Materials without restriction»), ottimizzati per
  GPU NVIDIA ([model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0), [OpenMDW-1.1](https://openmdw.ai/license/1-1/));
  **LFM2.5-VL** (Liquid) licenza propria con limite all'uso commerciale sopra 10 milioni di dollari di ricavi annui
  ([LICENSE](https://huggingface.co/LiquidAI/LFM2.5-VL-1.6B/blob/main/LICENSE)).

Esecuzione senza scheda grafica:

- FATTO: llama.cpp (MIT) esegue modelli con immagini (Gemma 3 e 4, Qwen2.5-VL, Qwen3-VL, InternVL, Pixtral, Mistral
  Small, SmolVLM) e avverte che i modelli OCR (PaddleOCR-VL, GLM-OCR, DeepSeek-OCR, dots.ocr, HunyuanOCR) «are trained
  with specific prompt and input structure» ([multimodal.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md),
  [LICENSE](https://github.com/ggml-org/llama.cpp/blob/master/LICENSE)).
- FATTO: tempi pubblicati dagli autori quasi solo su GPU: SmolDocling 0,35 s per pagina su A100; Qianfan-OCR 1,024
  pagine/s su A100; Surya 2.5 4,5 pagine/s su H100; olmOCR «requires a GPU» (fonti sopra). L'unica misura senza GPU
  NVIDIA trovata è di Surya 2.5 con llama.cpp su Apple M4 Max (Metal, non CPU): mediana 38,9 s per pagina con 8
  richieste in parallelo ([model card](https://huggingface.co/datalab-to/surya-ocr-2.5)).
- **Non trovato**: tempi pubblicati da fonti primarie per PaddleOCR-VL, MiniCPM-OCR, GLM-OCR, Qwen3-VL o Gemma 4 su
  una CPU x86 per una pagina A4 intera. **Da misurare.**

### 3.4 Uscita strutturata (JSON valido)

- FATTO: llama.cpp converte uno schema JSON in grammatica (GBNF): nel server si passa `json_schema` o
  `response_format` con lo schema ([grammars/README.md](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md),
  [server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)). Avvertenze: «The model
  has no visibility into the schema», quindi lo schema va descritto anche nella richiesta; alcune parti di JSON
  Schema non sono supportate e «Unsupported features are skipped silently» (stessa pagina).
- FATTO: vLLM (Apache-2.0) genera uscite strutturate con xgrammar o llguidance come motori
  ([structured_outputs.md](https://github.com/vllm-project/vllm/blob/main/docs/features/structured_outputs.md)).
  Outlines (Apache-2.0) dichiara «Guaranteed valid structure» con modelli Pydantic
  ([README](https://github.com/dottxt-ai/outlines)).
- FATTO: GLM-OCR, Xiaomi-OCR-0 e MiniCPM-OCR accettano uno schema JSON nella richiesta per l'estrazione di campi
  (model card sopra).
- DEDUZIONE: lo schema garantisce la forma (campi presenti, numeri dove servono numeri), non il valore giusto. Il
  modello può «inventare» una riga plausibile. Per questo servono i controlli a valle e il confronto con la foto
  (192).

Schema proposto (bozza da rivedere con l'utente):

```json
{
  "tipo_documento": "ddt | lettera_di_vettura | altro",
  "fornitore_letto": "string",
  "numero_ddt": "string",
  "data_ddt": "AAAA-MM-GG",
  "pagina": "number", "pagine_totali": "number | null",
  "ordini_ufp_citati": ["string"],
  "conferme_fornitore_citate": ["string"],
  "colli_totali": "number | null",
  "righe": [
    {"tipo_riga": "merce | sconto_merce | imballo_a_rendere | intestazione | riferimento | testo",
     "codice_fornitore": "string", "ean": "string | null", "descrizione": "string",
     "quantita": "number", "unita": "string",
     "ordine_ufp": "string | null", "saldo_o_acconto": "saldo | acconto | null",
     "segni_a_mano": "boolean"}
  ]
}
```

I campi `tipo_documento`, `tipo_riga`, i due tipi di riferimento d'ordine e `segni_a_mano` vengono da quanto visto
sulle bolle vere di UFP (sezione dedicata).

Controlli a valle (DEDUZIONE, proposta):

0. **Codici stampati prima di tutto**: si leggono con zxing-cpp tutti i barcode e i DataMatrix della pagina; un EAN
   letto vale più del testo letto, un DataMatrix con numero e data vale più dell'OCR della testata; se il DataMatrix
   è lo stesso su più pagine, le pagine sono dello stesso DDT.
1. **Fornitore**: il nome o la partita IVA letti devono corrispondere al fornitore scelto (183); se no, avviso.
2. **Numero e data**: formato della data valido e non nel futuro; il numero ha lo stesso aspetto dei numeri già
   confermati di quel fornitore (cifre, barre, prefissi); stesso fornitore, numero e data di un DDT già registrato →
   avviso di doppione (86).
3. **Ordine citato**: il numero d'ordine di UFP letto (per gruppo di righe, se la bolla ne cita più d'uno) esiste tra
   gli ordini aperti del fornitore (70); le righe di quel gruppo si abbinano prima a quell'ordine.
3b. **Righe che non sono merce**: intestazioni, riferimenti, testi e imballi a rendere non diventano righe di merce;
   lo sconto merce sì, ma marcato.
4. **Righe**: ogni codice letto si cerca tra i codici del fornitore degli articoli negli ordini aperti, con tolleranza
   per i segni che si confondono (89) e con la conferma del responsabile se differisce anche di poco (158). Un codice
   senza corrispondenza diventa «da controllare», non una riga nuova automatica.
5. **Quantità**: numero positivo, unità coerente con l'articolo; confronto con il residuo dell'ordine; se la bolla
   porta un totale di pezzi o colli, somma delle righe contro il totale. Se accanto alla quantità stampata c'è un
   numero scritto a mano, la riga va segnalata e non proposta.
6. **Righe mancanti**: se il modello legge meno righe di quante ne mostra la pagina (per esempio numeri di riga
   saltati), avviso «lettura incompleta».
7. Tutto questo produce **proposte** di quantità in bolla, che l'operatore vede accanto alla foto alla chiusura del
   DDT (192); la quantità contata resta quella delle letture della merce (183, 186).

### 3.5 Hardware

- FATTO (progetto): la sessione di Claude ha 4 processori e 16 GB; PaddleOCR a piena risoluzione esauriva la memoria
  e si usa la foto ridotta a 1.280 pixel (`docs/architettura.md`, «Script del calcolo»).
- DEDUZIONE (dimensioni dei file sopra): in 4 bit un modello generale da 8–9 miliardi occupa circa 6–7 GB di file
  (modello più parte visiva), più la memoria per il contesto; un lettore specializzato da 1 miliardo circa 1–2 GB.
  Entrambi entrano in un server con 16 GB di RAM; i tempi su CPU sono da misurare.
- DEDUZIONE: con una scheda grafica NVIDIA da 12 GB o più entrano i modelli da 8B in 8 bit (Ministral 3 8B dichiara 12
  GB in FP8; olmOCR chiede almeno 12 GB, fonti sopra). Un modello da 24B (Mistral Small 3.2) richiede ~55 GB in bf16:
  fuori portata per un piccolo server.
- Quanto tempo è accettabile: per numero e data, all'apertura del DDT, pochi secondi (IPOTESI, da decidere con
  l'utente); per le righe, entro la chiusura del DDT (DEDUZIONE dalla 192). La decisione 195 non copre la lettura
  della bolla.

## 4. Addestrare, adattare o scrivere regole per fornitore

### 4.1 Cosa dicono le fonti sulla quantità di dati

- FATTO: DocILE (fatture e documenti commerciali in inglese) ha 5.180 documenti di addestramento, 500 di validazione e
  1.000 di prova; nella prova il 25% è di moduli mai visti, il 25% di moduli con al massimo 3 esempi visti, il 50% di
  moduli con più esempi. Il miglior risultato pubblicato sulle righe (Line Item Recognition) è F1 0,721 con
  LayoutLMv3 ([arXiv 2302.05658](https://arxiv.org/pdf/2302.05658), tabella 3, 2023).
- FATTO: CORD ha 800 scontrini di addestramento; Donut addestrato arriva a 91,3 TED ([CORD](https://github.com/clovaai/cord),
  [Donut](https://github.com/clovaai/donut)). FUNSD ha 199 moduli in tutto ([FUNSD](https://guillaumejaume.github.io/FUNSD/)).
- FATTO: un esempio ufficiale di adattamento di MiniCPM-OCR 1.0 (scrittura a mano francese, 10.138 righe di testo,
  3 epoche, 34 minuti su 8 GPU A100) porta il CER da 5,67% a 2,98%
  ([guida LLaMA-Factory](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamafactory_minicpm_ocr_french_en.md)).
- FATTO (già nella ricerca del 18/11, § 2.2): il servizio in cloud di Microsoft dichiara un modello personalizzato con
  «only five examples of the same form or document type»: qui solo come termine di paragone, non si usa (cloud).
- **Non trovato**: quante bolle servono per adattare con LoRA un modello recente a DDT italiani. **Da misurare.**

### 4.2 Le tre strade

| Strada | Pro | Contro | Quando |
|---|---|---|---|
| **Modello generale senza addestramento** + schema JSON + controlli | Funziona dal primo giorno anche con fornitori occasionali; nessun dato da annotare per partire | Errori non sistematici difficili da prevedere; può inventare righe; più lento | Punto di partenza (proposta) |
| **Regole o modello per fornitore** (zone fisse, parole delle colonne, formato del numero) | Molto preciso su un modulo pulito e stabile; veloce | Un lavoro per ogni fornitore; si rompe se il fornitore cambia modulo o la foto è storta; inutile per gli occasionali | Solo per i 2–3 fornitori più frequenti, se la prova mostra errori ripetuti |
| **Adattamento del modello** (LoRA) su bolle annotate | Corregge errori sistematici su tutti i moduli visti; i dati crescono con le conferme | Servono GPU per addestrare, bolle annotate (numero da misurare), una nuova prova a ogni versione | Dopo la prova, se il modello generale sbaglia sempre allo stesso modo |

DEDUZIONE: per un magazzino con pochi fornitori ricorrenti e molti occasionali conviene un modello generale, aiutato
da due cose che il programma ha già:

1. **Gli ordini aperti del fornitore scelto** (183): trasformano la lettura del codice in una scelta tra pochi codici
   attesi, come per il codice stampato (89, 145).
2. **Una «memoria» per fornitore** costruita dalle conferme: formato del numero DDT, nomi delle colonne, unità usate,
   corrispondenza codice del fornitore ↔ articolo (già prevista, 71). Non è un addestramento: sono dati che il
   programma usa nei controlli e che si possono mettere nella richiesta al modello come esempi (few-shot). Che gli
   esempi nella richiesta migliorino la lettura delle bolle è un'IPOTESI da misurare.

Ogni bolla confermata dall'operatore (192) diventa una bolla annotata: se un giorno servirà l'adattamento, i dati ci
saranno già. Le bolle restano dati dell'azienda: dove conservarle è una decisione dell'utente (domande aperte).

### 4.3 Strumenti di annotazione

- FATTO: Label Studio è Apache-2.0 ([LICENSE](https://github.com/HumanSignal/label-studio/blob/master/LICENSE)),
  versione 1.23.2 ([PyPI](https://pypi.org/project/label-studio/)); il modello «Optical Character Recognition» permette
  di disegnare riquadri e poligoni e trascrivere il testo di ogni zona ([modello OCR](https://labelstud.io/templates/optical_character_recognition)).
- DEDUZIONE: per la prova proposta non servono riquadri: basta la verità in un foglio di calcolo (testata e righe),
  perché si misura il valore letto, non la posizione. Label Studio serve solo se si decide di addestrare un modello
  che ha bisogno delle posizioni.

## 5. Come si misura l'affidabilità

### 5.1 Metriche delle fonti

- FATTO: OmniDocBench usa la distanza di modifica normalizzata per il testo e TEDS per le tabelle
  ([README](https://github.com/opendatalab/OmniDocBench)). CER = «total character edit distance divided by the total
  number of reference characters» ([guida MiniCPM-OCR](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamafactory_minicpm_ocr_french_en.md)).
- FATTO: DocILE misura le righe con «the micro F1 score over all line item fields»: un campo è giusto se è giusto e
  assegnato alla riga giusta; le righe previste e vere si abbinano cercando «the maximum matching […] maximizing the
  overall recall» ([arXiv 2302.05658](https://arxiv.org/pdf/2302.05658), § 4.2).
- FATTO: Donut riporta su CORD sia un'accuratezza ad albero (TED) sia l'F1 sui campi ([README](https://github.com/clovaai/donut)).

### 5.2 Metriche proposte per le bolle (DEDUZIONE)

- **Testata, per campo**: numero DDT, data, ordini citati, fornitore: giusto/sbagliato/vuoto dopo una normalizzazione
  scritta prima (spazi, zeri iniziali, formato della data).
- **Righe**: le righe lette si abbinano a quelle vere come in DocILE; poi
  - richiamo = righe vere trovate / righe vere; precisione = righe lette giuste / righe lette;
  - **riga esatta** = codice, quantità e unità tutti giusti;
  - **quantità esatta** sulle righe abbinate (il numero che conta per la 192);
  - CER del codice, per capire se l'errore è un segno confuso (89).
- **Bolla perfetta**: testata e tutte le righe esatte.
- **Errori silenziosi**: valori sbagliati che passano tutti i controlli del § 3.4 senza avviso. È la misura più
  importante: un errore segnalato costa un tocco, uno silenzioso arriva al responsabile come differenza falsa.
- **Tempi** per pagina, solo nella sessione di Claude e solo per confrontare (143).

## Tabella finale dei candidati

Licenze lette il 18/11/2026 nei file indicati nelle sezioni sopra. «Uso commerciale» per i pesi; non è un parere legale.
«CPU» = gli autori indicano un modo per eseguirlo senza GPU (non dice niente sulla velocità). Memoria = dimensione dei
file (pesi in 4 bit quando c'è un GGUF) o dichiarazione degli autori; la RAM vera è da misurare.

| Nome | Cosa fa | Licenza codice | Licenza pesi | Uso commerciale | CPU | Memoria (fonte) | Italiano | Link |
|---|---|---|---|---|---|---|---|---|
| zxing-cpp 3.1.1 | Barcode e DataMatrix stampati sulla bolla | Apache-2.0 | — | Sì | Sì (anche WebAssembly) | — | — | [repo](https://github.com/zxing-cpp/zxing-cpp) |
| OpenCV / OpenCV.js | Ritaglio, prospettiva, soglia adattiva | Apache-2.0 | — | Sì | Sì (anche browser) | ~15 MB (npm) | — | [repo](https://github.com/opencv/opencv) |
| jscanify | Trova e ritaglia il foglio nel browser | MIT | — | Sì | Sì (browser) | — | — | [repo](https://github.com/puffinsoft/jscanify) |
| UVDoc | Raddrizza fogli piegati | MIT | In PaddleOCR (Apache-2.0) | Sì | Sì, 870 ms su Xeon | 30 MB | — | [repo](https://github.com/tanguymagne/UVDoc) |
| DocTr (Hao Feng) | Raddrizzamento | Non commerciale | Non commerciale | **No** | — | — | — | [LICENSE](https://github.com/fh2019ustc/DocTr/blob/main/LICENSE.md) |
| ML Kit Document Scanner / VisionKit | Scanner di sistema | Proprietari | — | Solo app native | Sul telefono | — | — | [ML Kit](https://developers.google.com/ml-kit/vision/doc-scanner) |
| pdfplumber / pdfminer.six | Testo e posizioni dai PDF con testo | MIT | — | Sì | Sì | — | Sì (testo del PDF) | [repo](https://github.com/jsvine/pdfplumber) |
| PyMuPDF | PDF | AGPL-3.0 o commerciale | — | Con licenza Artifex | Sì | — | — | [COPYING](https://github.com/pymupdf/PyMuPDF/blob/main/COPYING) |
| Camelot / Tabula | Tabelle dai PDF con testo | MIT | — | Sì | Sì (Tabula: Java) | — | — | [Camelot](https://github.com/camelot-dev/camelot) |
| Docling (+ TableFormer) | PDF e immagini → struttura | MIT | CDLA-Permissive-2.0 / Apache-2.0 | Sì | Sì | — | Testo PDF sì; OCR secondo il motore | [repo](https://github.com/docling-project/docling) |
| Marker / Surya / Chandra | PDF → Markdown, OCR | Apache-2.0 | OpenRAIL-M modificata | Solo sotto 5 (Marker, Surya) o 2 (Chandra) milioni di $ | Surya: llama.cpp | Surya 2.5: picco 4,3–4,8 GB su M4 Max | Non verificato | [Marker](https://github.com/datalab-to/marker) |
| MinerU / MinerU2.5 | PDF → Markdown | MinerU License (Apache + soglie) | AGPL-3.0 (etichetta HF) | Da chiarire | — | 1,2B | zh, en | [LICENSE](https://github.com/opendatalab/MinerU/blob/master/LICENSE.md) |
| olmOCR 2 | PDF → testo | Apache-2.0 | Apache-2.0 | Sì | No («requires a GPU») | GPU ≥12 GB | en | [repo](https://github.com/allenai/olmocr) |
| PaddleOCR PP-OCRv5/v6 + PP-StructureV3 | OCR + struttura | Apache-2.0 | Apache-2.0 | Sì | Sì | 7,7 GB di picco misurati nella sessione | Sì (PP-OCRv5 latino) | [repo](https://github.com/PaddlePaddle/PaddleOCR) |
| Tesseract | OCR | Apache-2.0 | Apache-2.0 | Sì | Sì | — | Sì | [repo](https://github.com/tesseract-ocr/tesseract) |
| docTR / EasyOCR / RapidOCR | OCR | Apache-2.0 | Apache-2.0 | Sì | Sì | — | docTR vocabolario sì; EasyOCR 80+ lingue; RapidOCR zh/en predefiniti | [docTR](https://github.com/mindee/doctr) |
| Donut | Lettura documenti da addestrare | MIT | MIT | Sì | Sì | — | No (pre-addestramento en, zh, ja, ko) | [repo](https://github.com/clovaai/donut) |
| LayoutLMv3 | Lettura documenti da addestrare | CC BY-NC-SA 4.0 | CC BY-NC-SA 4.0 | **No** | Sì | 125M | en | [card](https://huggingface.co/microsoft/layoutlmv3-base) |
| LiLT / UDOP | Lettura documenti da addestrare | MIT | MIT | Sì | Sì | 131M / 742M | en | [LiLT](https://github.com/jpWang/LiLT) |
| **PaddleOCR-VL-1.6** | Pagina → Markdown/JSON, tabelle, timbri | Apache-2.0 | Apache-2.0 | Sì | Sì (Paddle, Transformers, llama.cpp) | GGUF 0,94 + 0,88 GB | 109 lingue dichiarate (v1.0), italiano non elencato nella pagina letta | [card](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6) |
| MiniCPM-OCR 1.0 | Pagina → Markdown/JSON, KIE | Apache-2.0 | Apache-2.0 | Sì | llama.cpp, Ollama | GGUF 0,53 + 0,90 GB | Principali zh, en | [card](https://huggingface.co/openbmb/MiniCPM-OCR-1.0) |
| GLM-OCR | Parsing e KIE con schema JSON | Apache-2.0 (SDK) | MIT | Sì | llama.cpp (GGUF ggml-org), Ollama | GGUF 0,95 + 0,48 GB | Non elencato | [card](https://huggingface.co/zai-org/GLM-OCR) |
| Xiaomi-OCR-0 | Parsing, KIE con schema | Apache-2.0 | Apache-2.0 | Sì | GGUF di terzi | 0,87B | Non dichiarato | [card](https://huggingface.co/xiaomi-research/Xiaomi-OCR-0) |
| Qianfan-OCR | Parsing, KIE | — | Apache-2.0 | Sì | Non indicato | 4,7B | 192 lingue dichiarate | [card](https://huggingface.co/baidu/Qianfan-OCR) |
| dots.ocr | Parsing multilingue | MIT | MIT | Sì | GGUF ggml-org | 3B | Multilingue dichiarato | [card](https://huggingface.co/rednote-hilab/dots.ocr) |
| DeepSeek-OCR / OCR-2 | Parsing | MIT / Apache-2.0 | MIT / Apache-2.0 | Sì | llama.cpp (OCR 1) | 3,3B | Multilingue dichiarato | [card](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) |
| Unlimited-OCR 2 | Parsing di documenti lunghi | MIT | MIT | Sì | Non indicato (GPU nei test) | 3,3B | Multilingue dichiarato | [card](https://huggingface.co/baidu/Unlimited-OCR-2) |
| LightOnOCR-2-1B | Pagina → testo | — | Apache-2.0 | Sì | Transformers su CPU | 1,0B | Sì (elencato) | [card](https://huggingface.co/lightonai/LightOnOCR-2-1B) |
| granite-docling / SmolDocling | Pagina → DocTags | Apache-2.0 | Apache-2.0 / CDLA-P-2.0 | Sì | Sì (Transformers, ONNX, MLX) | 258M | en (altre sperimentali) | [card](https://huggingface.co/ibm-granite/granite-docling-258M) |
| Nanonets-OCR-s / OCR2-3B, OCRFlux-3B | Pagina → Markdown | — | Non indicata / Qwen Research (base 3B) | **Non chiaro, probabilmente no** | GGUF di terzi | 3,75B | OCR2: sì (elencato) | [card](https://huggingface.co/nanonets/Nanonets-OCR2-3B) |
| jina-ocr-v1 | Parsing | — | CC BY-NC 4.0 | **No** | — | 3,4B | Multilingue | [card](https://huggingface.co/jinaai/jina-ocr-v1) |
| HunyuanOCR | Parsing | — | Tencent, esclusa la UE | **No in Italia** | llama.cpp | 1,1B | — | [LICENSE](https://huggingface.co/tencent/HunyuanOCR/blob/main/LICENSE) |
| Nemotron Parse 2.0 / 3.5 | Parsing | — | OpenMDW-1.1 | Sì (licenza ampia) | Pensato per GPU NVIDIA | 0,6–0,9B | Tokenizer più multilingue | [card](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0) |
| **Qwen3-VL 4B / 8B** | Modello generale, OCR e KIE | Apache-2.0 | Apache-2.0 | Sì | llama.cpp, GGUF ufficiali | 8B: 5,03 + 0,75 GB; 4B: 2,50 + 0,45 GB | 39 lingue OCR, italiano non verificato | [card](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) |
| Qwen3.5 4B / 9B | Modello generale multimodale | Apache-2.0 | Apache-2.0 | Sì | GGUF di terzi | 9B: 5,68 + 0,92 GB | 201 lingue dichiarate | [card](https://huggingface.co/Qwen/Qwen3.5-9B) |
| Qwen2.5-VL 3B / 7B / 72B | Modello generale | Apache-2.0 | Ricerca / Apache-2.0 / Qwen | 3B no; 7B sì; 72B sì sotto 100M utenti | llama.cpp | — | — | [LICENSE 3B](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/blob/main/LICENSE) |
| Gemma 4 E2B / E4B | Modello generale | Apache-2.0 | Apache-2.0 | Sì | llama.cpp | E4B: 4,98 + 0,99 GB | 35+ lingue (140+ in addestramento) | [card](https://huggingface.co/google/gemma-4-E4B-it) |
| Gemma 3 / 3n | Modello generale | — | Gemma Terms | Sì, con politica d'uso | llama.cpp | — | — | [termini](https://ai.google.dev/gemma/terms) |
| InternVL3.5 2B/4B/8B | Modello generale | Apache-2.0 | Apache-2.0 | Sì | llama.cpp (InternVL3) | 8,5B | Multilingue | [card](https://huggingface.co/OpenGVLab/InternVL3_5-8B) |
| MiniCPM-V 4.5 | Modello generale | Apache-2.0 | Apache-2.0 | Sì | llama.cpp, Ollama | 8,7B | Multilingue | [card](https://huggingface.co/openbmb/MiniCPM-V-4_5) |
| Mistral Small 3.2 / Pixtral 12B / Ministral 3 8B | Modello generale | Apache-2.0 | Apache-2.0 | Sì | llama.cpp (Pixtral, Mistral Small 3.1) | 24B: ~55 GB bf16; Ministral 8B: 12 GB FP8 | Sì (elencato) | [card](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506) |
| Florence-2 / SmolVLM | Piccoli modelli generali | MIT / Apache-2.0 | MIT / Apache-2.0 | Sì | Sì | 0,26–2,2B | en | [Florence-2](https://huggingface.co/microsoft/Florence-2-large) |
| llama.cpp / vLLM / Outlines | Esecuzione e JSON vincolato | MIT / Apache-2.0 / Apache-2.0 | — | Sì | llama.cpp sì; vLLM soprattutto GPU | — | — | [llama.cpp](https://github.com/ggml-org/llama.cpp) |
| Label Studio | Annotazione | Apache-2.0 | — | Sì | Sì | — | — | [repo](https://github.com/HumanSignal/label-studio) |

## Proposta di prova su bolle vere

Tutto quello che segue è una **proposta**; le scelte segnate **da decidere** spettano all'utente. Lo stile è quello della
prova visiva (`docs/architettura.md`, «Prova di accuratezza visiva»; ticket 08 e 09).

### Cosa decide

Se la lettura automatica delle righe può proporre la quantità in bolla alla chiusura del DDT (192, 193), con quale
sistema, e per numero e data all'apertura (184) quale sistema basta.

### Bolle

- **Quante** (da decidere): proposta 100–120 bolle di UFP. Con 100 bolle, un risultato del 95% ha un intervallo al
  95% da circa 88,8% a 97,8%; con 500 righe, un 95% sta tra 92,7% e 96,6% (calcolo nostro, intervallo di Wilson). Le
  righe danno numeri più stretti della testata.
- **Quali fornitori** (da decidere): tutti i ricorrenti che portano la maggior parte delle bolle (proposta 8–12, circa
  8 bolle ciascuno) più 20–30 bolle di fornitori occasionali (1–2 ciascuno). Scelte a caso tra le bolle arrivate, come
  gli articoli della prova visiva (134).
- **Divisione per fornitore**: come in DocILE, una parte dei fornitori (proposta: un terzo dei ricorrenti) resta fuori
  dalla prima metà, per misurare il caso del «modulo mai visto». Le soglie e i controlli si tarano sulla prima metà e
  valgono i numeri della seconda, come nella prova visiva (145).
- **Fornitori già visti**: AGB/Alban Giacomo, ISEO Serrature e SAIT Abrasivi coprono già tre impaginazioni diverse
  (tabella su più pagine, tabella con barcode per riga, blocchi per posizione): proposta di includerli se sono tra i
  ricorrenti (da confermare con l'utente).
- **Foto**: ogni bolla di carta fotografata due volte dal browser dell'iPhone, a piena risoluzione: una «bene» (foglio
  sul tavolo, luce normale) e una «come capita» (in mano o sul collo, un po' storta). Palmare e Android dopo, come nella
  prova visiva (155). Le bolle di più pagine si fotografano tutte, nell'ordine, una foto per pagina: si misura anche
  se il programma rimette insieme le pagine dello stesso DDT.
- **Bolle con e senza segni**: nel nuovo flusso la foto si fa all'apertura, prima delle spunte e delle correzioni
  (184); le bolle d'archivio invece hanno spunte, correzioni a mano, timbri ed evidenziatore. Proposta: quando si può,
  fotografare bolle nuove al loro arrivo, prima dei segni; le bolle d'archivio si tengono come gruppo a parte, «con
  segni», e i numeri si riportano separati.
- **Lettere di vettura**: proposta di mettere nella prova anche 5–10 lettere di vettura dei corrieri (come quella
  SUSA), per misurare se il programma le riconosce e non crea un DDT.
- **PDF**: quando l'ufficio ha la versione digitale, anche il PDF (proposta: tutti quelli disponibili tra le bolle
  scelte), per provare la via del testo del PDF e confrontarla con la foto della stessa bolla.

### Cosa si copre (da decidere con l'utente)

- Nomi, indirizzi e riferimenti dei clienti finali (destinazione, riferimenti cliente sulle righe, 70), firme, targhe;
  prezzi, se la bolla li porta e l'utente lo chiede.
- DEDUZIONE: la copertura va fatta **sull'immagine** (rettangolo pieno salvato nei pixel) prima che la bolla esca dal
  computer dell'ufficio. Su un PDF con testo, un rettangolo disegnato sopra non toglie il testo sotto: serve uno
  strumento che cancelli davvero il testo, oppure si tiene solo l'immagine del PDF. Da verificare con lo strumento
  scelto.
- Le zone coperte non entrano nella verità e non si misurano.

### Verità scritta a mano

Un foglio di calcolo per bolla, scritto guardando la bolla (non l'uscita dei sistemi):

- **Testata**: fornitore, numero DDT com'è stampato, data, ordini citati, numero colli o totale pezzi se c'è, numero di
  pagine.
- **Righe**: tipo di riga (merce, sconto merce, imballo a rendere, intestazione Saldo/Acconto, riferimento, testo),
  codice del fornitore, EAN se stampato, descrizione, quantità, unità, numero d'ordine di UFP del gruppo, numero di
  conferma del fornitore, Saldo o Acconto, pagina; più due colonne: «scritto a mano o corretto» e «coperto da timbro»,
  per dividere i risultati.
- **Documento**: DDT o lettera di vettura; quali foto sono pagine dello stesso DDT.
- **Contesto**: per ogni riga, se l'articolo era in un ordine aperto del fornitore quel giorno (sì/no), per misurare
  l'aiuto dell'abbinamento (§ 3.4).
- Proposta: una seconda persona ricontrolla il 10% delle bolle, per stimare gli errori della verità.

### Sistemi a confronto (proposta: 3 più la via del PDF)

**Passo 0, comune a tutti**: zxing-cpp (Apache-2.0) legge barcode e DataMatrix di ogni pagina prima del resto; quello
che legge (EAN di riga, numero e data dal DataMatrix, pagine dello stesso DDT) prevale sull'OCR. Si misura anche da
solo: per quanti fornitori e quante righe basta (sulla bolla ISEO vista, 8 righe su 9; il DataMatrix AGB su 3 pagine
su 4). Dopo ogni sistema, lo stesso abbinamento: prima per numero d'ordine di UFP del gruppo di righe, poi per codice
del fornitore o EAN tra gli ordini aperti del fornitore (70, 183).

| # | Sistema | Perché | Licenza | Requisiti |
|---|---|---|---|---|
| A | **PaddleOCR (PP-OCRv5 latino o PP-OCRv6) + regole + ordini aperti** | Già nel progetto (145); veloce; termine di paragone «classico» | Apache-2.0 | CPU; ~7,7 GB di picco misurati nella sessione |
| B | **PaddleOCR-VL-1.6 → Markdown/JSON + regole + ordini aperti** | Tra i primi su OmniDocBench e Real5, piccolo, stessa famiglia di A, molte lingue | Apache-2.0 | CPU (Paddle o llama.cpp), file ~1,8 GB; tempi da misurare |
| C | **Qwen3-VL-8B-Instruct con schema JSON (llama.cpp) + ordini aperti**; anche il 4B per i tempi | Modello generale che scrive direttamente testata e righe; DocVQA 96,1 e OCRBench 896 dichiarati; GGUF ufficiali | Apache-2.0 | CPU con ~6 GB di file in 4 bit; tempi da misurare |
| D | **PDF con testo: pdfplumber → stesse regole di A e lo stesso schema di C (solo testo)** | Quando c'è il PDF non serve leggere l'immagine | MIT | CPU, leggero |

Motivi delle esclusioni: licenze non commerciali o fuori UE (§ 3.3); Docling e granite-docling dichiarati per
l'inglese; MiniCPM-OCR 1.0 e GLM-OCR sono alternative forti a B (MiniCPM-OCR è primo su Real5), ma dichiarano cinese
e inglese come lingue principali e GLM-OCR non elenca l'italiano: **da decidere** se sostituire B con uno di loro o
aggiungerlo come quarto. Qwen3.5-9B e Gemma 4 E4B sono alternative a C con licenza Apache-2.0 (Qwen3.5 dichiara 201
lingue): proposta di tenerle di riserva se C non convince.

Ogni sistema si prova sulla foto «bene», sulla foto «come capita», con e senza ritaglio e raddrizzamento (jscanify o
OpenCV, UVDoc), e con e senza la soglia adattiva (§ 1.3).

### Cosa si misura

Le metriche del § 5.2: testata per campo, righe (richiamo, precisione, riga esatta, quantità esatta), CER dei codici,
bolla perfetta, **errori silenziosi** dopo i controlli, tutto diviso per foto «bene» / «come capita» / PDF, per
fornitore visto / mai visto, per bolle con e senza segni a mano, per righe stampate / scritte a mano. In più, dalle
bolle vere: righe non di merce scartate bene e righe di merce scartate per sbaglio; numero d'ordine di UFP giusto per
gruppo di righe; pagine rimesse insieme nel DDT giusto; lettere di vettura riconosciute; quante righe e testate si
leggono dai soli codici stampati (passo 0). Tempi per pagina nella sessione di Claude (CPU,
4 processori), solo per confrontare i sistemi (143); la macchina vera si misura quando si sceglie il server.

### Traguardi (da decidere con l'utente)

Proposte da cui partire, con un esempio come per la prova visiva:

1. **Numero e data** (proposta di numero e data all'apertura, 184): giusti in almeno 95 bolle su 100 dalla foto
   «come capita». Se il numero è sbagliato l'operatore lo corregge comunque prima di confermare.
2. **Righe** (quantità in bolla proposta alla chiusura, 192): codice e quantità giusti in almeno 95 righe su 100 tra
   quelle lette, **e** non più di 1 riga su 100 sbagliata senza avviso. Esempio: su 500 righe, al massimo 5 errori
   silenziosi.
3. **Tempo**: numero e data entro pochi secondi; righe entro la durata tipica di un ricevimento (da stabilire con
   l'utente).
4. Se un sistema raggiunge 1 e non 2, si usa solo per la testata e le righe restano a mano (192); se raggiunge 2 solo
   per alcuni fornitori, si può attivare per fornitore (da decidere).

### Dove eseguire la prova

- Calcolo e tempi nella sessione di Claude, come per la prova visiva (143): niente computer o server aziendali finché
  non c'è una versione da provare.
- Script nel repository del progetto, come `prova-visiva/script/`, senza bolle; nel repository pubblico solo numeri e
  sigle anonime (fornitore F01, F02…, bolla B001…), come la 129.

### Dove conservare le bolle (da decidere: solo opzioni)

La decisione 130 oggi esclude i documenti (DDT, ordini) dalle foto della prova visiva: per la prova sulle bolle serve
una decisione nuova. Opzioni:

1. Una cartella separata nel repository privato della prova visiva (`prova-visiva-foto`, 128).
2. Un nuovo repository GitHub privato solo per le bolle.
3. Solo bolle coperte e ritagliate, con la tabella sigla → fornitore vero nel repository privato (come la 129).
4. Bolle sintetiche (fatte a mano a imitazione dei moduli dei fornitori) per provare gli script, come la prova
   sintetica della prova visiva: i numeri non valgono per la scelta.

Per ognuna resta da decidere cosa succede dopo la prova (come la 131: tenerle per rifare la prova o per adattare il
modello, cancellarle su richiesta).

## Domande aperte per l'utente

1. Dove si conservano le bolle della prova (opzioni sopra) e cosa succede dopo la prova?
2. Quante bolle e di quali fornitori: quanti sono i fornitori ricorrenti di UFP e quale parte delle bolle portano?
3. Quanti fornitori mandano anche il PDF del DDT, e chi in ufficio lo riceve?
4. Cosa si copre sulle bolle: solo i dati dei clienti finali, o anche prezzi, firme, targhe?
5. Le bolle di UFP portano spesso quantità corrette a mano, timbri sopra le righe, più pagine?
6. Quali traguardi: vanno bene le proposte (95 su 100 per numero e data; 95 su 100 per le righe con al massimo 1
   errore silenzioso su 100)? Quanto può aspettare l'operatore per numero e data?
7. Va bene un modello generale da 8 miliardi (C), che sul server in sede chiede circa 6 GB solo per i file, oppure si
   preferisce restare su modelli da 1 miliardo (A, B)?
8. Se la prova va bene per pochi fornitori, si attiva la lettura delle righe solo per quelli?
9. AGB, ISEO e SAIT sono tra i fornitori ricorrenti? Quanti altri fornitori stampano barcode di riga o un DataMatrix?
10. L'ufficio registra sull'ordine di UFP anche il numero di conferma del fornitore (per esempio quello di AGB e
    ISEO)? Se sì, il programma può usarlo per l'abbinamento.
11. Lo sconto merce (stesso articolo su due posizioni) deve restare distinto nella quantità in bolla, o basta la somma?

## Fonti

Pagine, file e articoli aperti il 18/11/2026. Tra parentesi la data della pagina o del rilascio quando c'è.

Foto, ritaglio, raddrizzamento
- https://github.com/opencv/opencv/blob/master/LICENSE
- https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.markdown
- https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.markdown
- https://github.com/opencv/opencv/blob/4.x/doc/js_tutorials/js_setup/js_intro/js_intro.markdown
- https://registry.npmjs.org/@techstark/opencv-js/latest
- https://github.com/puffinsoft/jscanify · https://github.com/puffinsoft/jscanify/blob/master/LICENSE · https://registry.npmjs.org/jscanify (1.4.3, 20/07/2026)
- https://github.com/tanguymagne/UVDoc · https://github.com/tanguymagne/UVDoc/blob/main/LICENSE
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/module_usage/text_image_unwarping.en.md
- https://github.com/ZZZHANG-jx/DocRes · https://github.com/ZZZHANG-jx/DocRes/blob/master/LICENSE
- https://github.com/fh2019ustc/DocTr/blob/main/LICENSE.md
- https://developers.google.com/ml-kit/vision/doc-scanner · https://developers.google.com/ml-kit/vision/doc-scanner/android
- https://developer.apple.com/tutorials/data/documentation/visionkit/vndocumentcameraviewcontroller.json (pagina HTML non leggibile come testo)
- https://github.com/mdn/browser-compat-data/blob/main/html/elements/input.json · https://github.com/mdn/browser-compat-data/blob/main/api/ImageCapture.json
- https://huggingface.co/datasets/PaddlePaddle/Real5-OmniDocBench · https://arxiv.org/abs/2603.04205
- Non raggiungibili: docs.opencv.org (403 Forbidden); al loro posto i sorgenti della documentazione su GitHub.

PDF
- https://github.com/jsvine/pdfplumber · https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt · https://pypi.org/project/pdfplumber/ (0.11.10, 15/06/2026)
- https://github.com/pdfminer/pdfminer.six/blob/master/LICENSE
- https://github.com/pymupdf/PyMuPDF/blob/main/COPYING · https://pypi.org/project/pymupdf/ (2.1, 02/11/2026)
- https://gitlab.freedesktop.org/poppler/poppler/-/blob/master/COPYING · https://gitlab.freedesktop.org/poppler/poppler/-/blob/master/README.md
- https://pypi.org/project/pypdfium2/ · https://registry.npmjs.org/pdfjs-dist/latest
- https://github.com/camelot-dev/camelot · https://github.com/camelot-dev/camelot/blob/master/LICENSE
- https://github.com/chezou/tabula-py · https://github.com/tabulapdf/tabula-java/blob/master/LICENSE
- https://github.com/docling-project/docling · https://github.com/docling-project/docling/blob/main/LICENSE · https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py · https://pypi.org/project/docling/ (2.150.1, 14/11/2026)
- https://huggingface.co/docling-project/docling-models · https://github.com/docling-project/docling-ibm-models/blob/main/LICENSE
- https://huggingface.co/ibm-granite/granite-docling-258M · https://huggingface.co/ds4sd/SmolDocling-256M-preview
- https://github.com/datalab-to/marker · https://github.com/datalab-to/marker/blob/master/LICENSE · https://github.com/datalab-to/surya · https://github.com/datalab-to/surya/blob/master/LICENSE · https://huggingface.co/datalab-to/chandra-ocr-2 · https://huggingface.co/datalab-to/surya-ocr-2.5
- https://github.com/opendatalab/MinerU/blob/master/LICENSE.md · https://huggingface.co/api/models/opendatalab/MinerU2.5-2509-1.2B
- https://github.com/allenai/olmocr · https://github.com/allenai/olmocr/blob/main/LICENSE · https://huggingface.co/allenai/olmOCR-2-7B-1025

OCR classici
- https://github.com/PaddlePaddle/PaddleOCR · https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE · https://pypi.org/project/paddleocr/ (3.7.0, 11/06/2026)
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.en.md
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/PP-StructureV3.en.md
- https://huggingface.co/PaddlePaddle/PP-OCRv6_medium_rec
- https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE · https://github.com/tesseract-ocr/tessdata_best
- https://github.com/mindee/doctr · https://github.com/mindee/doctr/blob/main/doctr/datasets/vocabs.py
- https://github.com/JaidedAI/EasyOCR · https://pypi.org/project/easyocr/ · https://github.com/RapidAI/RapidOCR

Modelli di comprensione e dataset
- https://github.com/clovaai/donut · https://huggingface.co/naver-clova-ix/donut-base · https://github.com/clovaai/cord
- https://huggingface.co/microsoft/layoutlmv3-base · https://github.com/microsoft/unilm/tree/master/layoutlmv3
- https://github.com/jpWang/LiLT · https://huggingface.co/microsoft/udop-large · https://guillaumejaume.github.io/FUNSD/
- https://arxiv.org/pdf/2302.05658 (DocILE, 2023) · https://arxiv.org/abs/2111.15664 · https://arxiv.org/abs/2204.08387 (abstract senza i numeri)

Modelli che leggono immagini
- https://github.com/opendatalab/OmniDocBench (classifica v1.6, aggiornata al 12/11/2026)
- https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6 · https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6-GGUF · https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/PaddleOCR-VL.en.md
- https://huggingface.co/openbmb/MiniCPM-OCR-1.0 · https://huggingface.co/openbmb/MiniCPM-OCR-1.0-gguf · https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamafactory_minicpm_ocr_french_en.md
- https://huggingface.co/zai-org/GLM-OCR · https://github.com/zai-org/GLM-OCR/blob/main/LICENSE · https://huggingface.co/ggml-org/GLM-OCR-GGUF
- https://huggingface.co/xiaomi-research/Xiaomi-OCR-0 · https://huggingface.co/baidu/Qianfan-OCR · https://huggingface.co/baidu/Unlimited-OCR-2
- https://huggingface.co/rednote-hilab/dots.ocr · https://huggingface.co/deepseek-ai/DeepSeek-OCR · https://huggingface.co/deepseek-ai/DeepSeek-OCR-2
- https://huggingface.co/lightonai/LightOnOCR-2-1B · https://huggingface.co/infly/Infinity-Parser2-Flash · https://huggingface.co/stepfun-ai/GOT-OCR2_0 · https://huggingface.co/echo840/MonkeyOCR-pro-3B
- https://huggingface.co/nanonets/Nanonets-OCR2-3B · https://huggingface.co/api/models/ChatDOC/OCRFlux-3B · https://huggingface.co/jinaai/jina-ocr-v1
- https://huggingface.co/tencent/HunyuanOCR/blob/main/LICENSE · https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0 · https://openmdw.ai/license/1-1/ · https://huggingface.co/LiquidAI/LFM2.5-VL-1.6B/blob/main/LICENSE
- https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct · https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct-GGUF · https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct-GGUF · https://arxiv.org/pdf/2511.21631 (rapporto tecnico Qwen3-VL) · https://github.com/QwenLM/Qwen3-VL
- https://huggingface.co/Qwen/Qwen3.5-9B · https://huggingface.co/unsloth/Qwen3.5-9B-GGUF · https://huggingface.co/api/models/Qwen/Qwen3.6-35B-A3B
- https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/blob/main/LICENSE · https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct/blob/main/LICENSE
- https://huggingface.co/google/gemma-4-E4B-it · https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF · https://ai.google.dev/gemma/docs/gemma_4_license (porta a https://gemma.ai/resources/apache-2/) · https://ai.google.dev/gemma/terms (01/04/2026)
- https://huggingface.co/OpenGVLab/InternVL3_5-8B · https://huggingface.co/openbmb/MiniCPM-V-4_5
- https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506 · https://huggingface.co/mistralai/Pixtral-12B-2409 · https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512
- https://huggingface.co/microsoft/Florence-2-large · https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct

Esecuzione e uscita strutturata
- https://github.com/ggml-org/llama.cpp/blob/master/LICENSE · https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
- https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md · https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/vllm-project/vllm/blob/main/docs/features/structured_outputs.md · https://github.com/vllm-project/vllm/blob/main/LICENSE
- https://github.com/dottxt-ai/outlines · https://github.com/mlc-ai/xgrammar/blob/main/LICENSE

Annotazione
- https://github.com/HumanSignal/label-studio/blob/master/LICENSE · https://pypi.org/project/label-studio/ · https://labelstud.io/templates/optical_character_recognition

Bolle vere di UFP
- 10 foto di DDT (AGB/Alban Giacomo, ISEO Serrature, SAIT Abrasivi) e una lettera di vettura SUSA, mostrate
  dall'utente in chat il 18/11/2026 e descritte dall'agente principale, con la sua prova di zxing-cpp 3.1.1; non
  riprodotte nel repository.
- https://github.com/zxing-cpp/zxing-cpp (licenza verificata nella ricerca del 15/11/2026, § G)

Documenti del progetto
- `docs/decisioni.md` (decisioni 40, 70, 73, 86, 89, 92, 121, 126, 128–131, 143, 145, 158, 183–186, 192, 193, 195)
- `docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 2)
- `docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (§ G, § H)
- `docs/architettura.md` («Prova di accuratezza visiva», «Script del calcolo»)
- `.scratch/architettura/issues/08-piano-prova-visiva.md`, `09-esecuzione-prova-visiva.md`, `24-ricerca-lettura-bolle.md`

Non raggiungibili o non usati: le API di GitHub non sono abilitate per questa sessione (si sono letti i file grezzi);
la pagina della licenza FUNSD non mostrava il testo della licenza; gli abstract di arXiv di Donut e LayoutLMv3 non
riportano i numeri (presi dai README degli autori).
