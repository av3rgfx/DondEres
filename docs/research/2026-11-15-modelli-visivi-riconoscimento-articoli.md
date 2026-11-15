# Modelli visivi per riconoscere gli articoli in arrivo

Data: 15/11/2026

Stato: BOZZA in corso di stesura.

## Domanda

Quali modelli visivi pronti sono adatti, tra quali famiglie di approccio scegliere, e quale raccomandare per
identificare il tipo di articolo (SKU) inquadrato con il telefono, in locale, su un catalogo fino a 35.000 articoli?

## 1. Encoder "foundation" per embedding e ricerca per somiglianza

- DINOv3: codice e pesi sotto "DINOv3 License" (non Apache), pesi su richiesta.
  [repo](https://github.com/facebookresearch/dinov3), [LICENSE.md](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md)
- DINOv2: codice e pesi Apache-2.0. [repo](https://github.com/facebookresearch/dinov2)
- SigLIP 2: Apache-2.0 sul model card. [HF](https://huggingface.co/google/siglip2-base-patch16-naflex)
- MobileCLIP/MobileCLIP2: codice MIT, pesi solo ricerca non commerciale.
  [repo](https://github.com/apple/ml-mobileclip), [LICENSE_MODELS](https://github.com/apple/ml-mobileclip/blob/main/LICENSE_MODELS)
- Perception Encoder: codice e pesi PE Apache-2.0. [repo](https://github.com/facebookresearch/perception_models)

(da completare)
