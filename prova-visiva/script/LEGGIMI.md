# Script della prova visiva

Calcolano i numeri della prova di accuratezza visiva (sezione «Prova di accuratezza visiva» di
`docs/architettura.md`, decisioni 128–159). Sono solo codice: foto, codici veri e tabella delle sigle stanno nel
repository privato `prova-visiva-foto`; le impronte in una cartella di lavoro fuori dai repository. Nel repository
del progetto entrano solo i risultati in numeri, con le sigle anonime (129).

## Preparazione

```bash
python3 -m venv /percorso/venv
/percorso/venv/bin/pip install -r prova-visiva/script/requirements.txt
```

I modelli si scaricano da Hugging Face al primo uso (circa 5 GB in tutto). Per PaddleOCR serve
`PADDLE_PDX_MODEL_SOURCE=huggingface`, che `etichette.py` imposta da solo.

## Ordine

Si lanciano dalla cartella `prova-visiva/script`, uno alla volta: insieme possono esaurire la memoria.

| Passo | Comando | Cosa fa |
|---|---|---|
| 1 | `python prepara.py --privato P` | Apre gli ZIP di `P/da-caricare`, sistema foto ed elenchi, aggiorna `P/sigle.csv`, segnala i problemi (153) |
| 2 | `python impronte.py --privato P --cache C` | Impronte dei sei modelli, con il riquadro e con il ritaglio OWLv2, e tempi (146, 147, 143) |
| 3 | `python valuta.py --privato P --cache C --uscita prova-visiva/risultati/AAAA-MM-GG` | Numeri sull'aspetto: attesi, foto di riferimento, dispositivi, soglie (135–145) |
| 4 | `python etichette.py --privato P --cache C --uscita prova-visiva/risultati/AAAA-MM-GG` | Lettura di codice stampato e quantità con PaddleOCR (89, 93, 142) |

`P` è il repository privato clonato, `C` una cartella di lavoro qualsiasi fuori dai repository (si può cancellare:
gli script rifanno solo ciò che manca). Dopo il passo 1 si fa il commit nel repository privato; dopo i passi 3 e 4
si controlla che i risultati contengano solo sigle e numeri, poi si fa il commit nel repository del progetto.

## Prova sintetica

`prova_sintetica.py` crea un finto repository privato con «foto» ricavate da poche immagini (ruotate, spostate,
schiarite), nel formato della pagina di scatto. Serve a controllare che la catena giri; i numeri che ne escono non
valgono niente. Il finto repository va tenuto fuori dai repository veri.

```bash
python prova_sintetica.py --immagini P/esempi --uscita /tmp/sint/privato --etichette verita.csv
```

## Scelte da sapere

- Modelli da timm: SigLIP 2 B/16 e L/16 a 512 px, PE-Core B/16 a 224 e L/14 a 336, DINOv2 B/14, TIPSv2 B/14
  (146). Si usa l'impronta che timm restituisce con `num_classes=0` e la trasformazione standard del modello.
- Ritaglio OWLv2 (147): senza testo, l'oggetto più probabile con il centro nel riquadro e almeno il 5% della foto.
- Punteggio di un articolo: la somiglianza più alta tra la foto di arrivo e le sue foto di riferimento.
- Articoli attesi: per ogni foto di arrivo si pescano a caso gli altri attesi tra tutti gli articoli della prova,
  20 volte; l'intervallo al 95% si calcola sul numero di foto, non sulle ripetizioni.
- Soglie (145): si dividono per articolo le foto di arrivo in due metà; sulla prima si sceglie la soglia
  «convincente» più alta che rispetta il traguardo, poi quella del «non lo so»; sulla seconda si controllano.
- «Ricerca in tutto» nella prova vuol dire tra i circa 540 articoli della prova, non tra i 35.000 di un catalogo
  vero (18): quel caso è più facile nella prova che nella realtà.
- Confronto dei codici (89): anche «L» vale 1, perché dopo il passaggio in maiuscolo la «l» minuscola non si
  distingue più.
- PaddleOCR gira con `enable_mkldnn=False`: con Paddle 3.3.1 l'accelerazione oneDNN dà un errore su questi modelli.
