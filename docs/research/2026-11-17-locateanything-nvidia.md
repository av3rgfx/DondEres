# LocateAnything di NVIDIA

Data: 17/11/2026. Domanda nata dalla nota dell'utente al giro 3 del ticket «Piano della prova di accuratezza visiva»:
ha senso usare LocateAnything per riconoscere gli articoli?

## Fatti

- È un modello che unisce immagine e testo (3 miliardi di parametri: encoder Moon-ViT, decoder Qwen2.5) per
  **localizzare**: data un'immagine e una frase, restituisce riquadri o punti. Copre rilevamento a vocabolario aperto,
  comprensione di espressioni («la scatola rossa a sinistra»), localizzazione di testo, di elementi di interfaccia e di
  impaginazione. La pagina non parla di riconoscere l'istanza esatta di un oggetto né di ricerca per somiglianza.
  [Pagina del progetto](https://research.nvidia.com/labs/lpr/locate-anything/), articolo arXiv:2605.27365.
- Licenza: «NVIDIA License», per uso non commerciale. La scheda del modello dice: «Commercial use is **not
  permitted**, except by NVIDIA and its affiliates» e «This released model is for research and development only».
  [Scheda su Hugging Face](https://huggingface.co/nvidia/LocateAnything-3B),
  [LICENSE](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE).
- Requisiti: GPU NVIDIA Ampere, Hopper, Lovelace o Blackwell, solo Linux, precisione BF16. In una prova su A100 con
  immagine 4K: circa 11,7 GB di memoria di picco e circa 8 s per l'esecuzione (scheda del modello).
- Codice: [NVlabs/Eagle, cartella Embodied](https://github.com/NVlabs/Eagle/tree/main/Embodied).

## Deduzioni

- Non risolve il nostro problema: dice *dove* è «una scatola» o «il codice», non *quale* dei 35.000 articoli è. Il
  riconoscimento dell'articolo resta la ricerca per somiglianza (analisi §4).
- Non si può usare nel prodotto: la licenza esclude l'uso commerciale. Richiede inoltre una scheda grafica potente,
  che il server in sede potrebbe non avere.
- Il compito che potrebbe svolgere (ritagliare la scatola o l'etichetta) ha alternative con licenza Apache-2.0 già
  indicate nelle ricerche (RF-DETR Nano/Small, D-FINE; `2026-11-15-modelli-visivi-riconoscimento-articoli.md` §3), da
  considerare solo se la prova mostra che il ritaglio serve.
