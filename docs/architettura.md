# Architettura della base generica

Specifica della base generica, in costruzione. Ogni sezione nasce da un ticket della mappa
`.scratch/architettura/map.md`. Le decisioni dell'utente sono in `docs/decisioni.md`: qui si citano per numero, senza
ripeterne il testo. I termini sono definiti in `GLOSSARY.md`.

## Ricevimento e assegnazione

Dal ticket «Regole all'arrivo: carico normale e merce venduta (VEND)», chiuso il 15/11/2026. Decisioni 15, 16, 21,
26 e 30–48 (la 44 sostituisce la 29, la 42 corregge la 15).

### Stati della merce

Un pezzo presente in magazzino si trova sempre in uno di questi stati:

| Stato | Cosa vuol dire | Si assegna di nuovo? |
|---|---|---|
| Libero | In giacenza, in ubicazione se il magazzino le usa | Sì, dal più vecchio |
| Assegnato | Riservato a una riga d'ordine cliente (anche in parte) | Sì, a ogni variazione di giacenza (16) |
| In VEND | Arrivato con un ordine fornitore fatto per quel cliente | No, salvo annullamento (34) |
| Prelevato | Preso dall'operatore; l'ordine è evaso e la merce aspetta la spedizione (21, 36) | No |
| In attesa di decisione | Merce non prevista, caricata ma non ubicata (45) | No, finché il responsabile non la tiene (48) |

La spedizione fa uscire il pezzo dal magazzino. La quantità che un operatore vede come prelevabile è sempre:

```
prelevabile = in magazzino − assegnato − in VEND − prelevato − in attesa di decisione
```

### Il ricevimento

1. **Si carica il DDT** (40). Senza DDT la merce non si riceve. Il DDT rimanda agli ordini fornitore che la consegna
   chiude in tutto o in parte.
2. **Si scansiona la merce** e il programma la confronta con le righe attese di quegli ordini.
3. **Ogni riga prende una di tre strade**, in base all'ordine fornitore da cui arriva:

| Strada | Quando | Cosa succede |
|---|---|---|
| VEND | L'ordine fornitore, o la sua riga, porta il riferimento del cliente e VEND è acceso | I pezzi vanno in VEND per quella riga d'ordine cliente |
| Carico normale | Ordine di magazzino, senza riferimento cliente | I pezzi entrano liberi, vanno in ubicazione e si assegnano dal più vecchio |
| Merce non prevista | Nessun ordine fornitore aperto la prevede | Caricata e segnata «senza ordine», in attesa della decisione del responsabile |

4. **Quantità diverse dall'atteso.** Se arriva di più, si accetta tutto: il residuo va a 0 e l'eccedenza viene
   segnalata al responsabile (32). Se arriva di meno, la riga resta aperta con il residuo finché arriva il resto o il
   responsabile la chiude (33).

### Strada VEND

- **Da dove nasce.** Solo dal riferimento del cliente scritto sull'ordine fornitore (44). Il programma non collega da
  solo un ordine cliente alla merce in arrivo; senza riferimento la merce segue il carico normale.
- **Chi scrive il riferimento.** In UFP lo scrive chi ordina al fornitore (44). Nel magazzino Shopify lo scrive il
  programma: per un ordine del sito con un articolo mancante prepara la proposta d'ordine al fornitore con il
  riferimento già compilato, e una persona la conferma (46).
- **Dove sta il riferimento.** Di solito sull'ordine fornitore intero; il magazzino può scegliere di metterlo su ogni
  riga (39).
- **Precedenza.** Il collegamento vince sulla regola «dal più vecchio»: i pezzi vanno al loro cliente anche se ordini
  più vecchi aspettano lo stesso articolo (34). A quel cliente si spediscono gli articoli ordinati per lui, anche se
  nel frattempo c'è giacenza; le quantità aggiunte senza ordine fornitore con riferimento si coprono dalla giacenza,
  secondo disponibilità (35).
- **Dove sta fisicamente.** VEND è sempre un conto nel programma; il magazzino può collegarlo a un'area fisica (30).
  Se lo sceglie alla configurazione, l'area ha posti numerati (VEND1, VEND2…): un posto per ogni ordine cliente,
  proposto dal programma (lo stesso se l'ordine ne ha già uno, altrimenti il primo libero) e confermato scansionando
  l'etichetta del posto (47).
- **Quando esce.** Con il prelievo confermato dall'operatore (36).

### Strada del carico normale

I pezzi entrano liberi e si assegnano alle righe d'ordine cliente né evase né spedite, dal più vecchio; a parità di
data vale il numero d'ordine. Una riga può essere coperta in parte. L'assegnazione si rifà da sola a ogni variazione
della merce libera (16, 21).

### Merce non prevista

L'operatore la registra (31); resta senza ubicazione e non si assegna agli ordini cliente (45, 48). Il responsabile la
trova tra i movimenti da controllare e decide se tenerla (va in ubicazione e diventa libera) o renderla al fornitore.

### Annullamento di un ordine cliente

I pezzi in VEND o assegnati tornano liberi e si assegnano dal più vecchio. Fisicamente vanno nella loro ubicazione, se
l'articolo si tiene a magazzino e ne ha una. Se l'articolo non si tiene a magazzino, decide il responsabile se renderlo
al fornitore o ubicarlo e tenerlo (37, 41). Se l'ordine era solo collegato e la merce non era ancora arrivata, il
collegamento cade e i pezzi in arrivo seguono il carico normale (deduzione dalle decisioni 37 e 44).

### Configurazione per magazzino

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| VEND | acceso, spento | spento | 38 |
| Riferimento cliente | sull'ordine intero, su ogni riga | sull'ordine intero | 39 |
| Posti VEND | un'area senza posti, posti numerati | da scegliere alla configurazione | 47 |
| Ubicazioni | sì, no | da scegliere alla configurazione | 26 |

### I due magazzini di prova

Servono a verificare la base, non sono la sua specializzazione (4).

- **UFP** affianca Ad Hoc Revolution e ARS Logistica (19, 42). Usa il carico normale e VEND. Gli ordini dei clienti
  arrivano per telefono o email; per un articolo che non è a magazzino o non è a catalogo si ordina al fornitore con il
  riferimento del cliente (44). Oggi VEND è un tavolo con gli articoli venduti pronti per la spedizione. Vende anche al
  banco.
- **Magazzino Shopify**: la base è il gestionale principale (19). Oggi la merce venduta si carica senza ubicarla e si
  mette su un tavolo con un biglietto che dice di chi è. Con la base usa VEND, con il riferimento preso dagli ordini del
  sito (46).

### Rimandato ad altri ticket o alla nebbia della mappa

- Creazione delle proposte d'ordine al fornitore e vendita al banco come fonte di ordini: ticket «Fonti degli ordini e
  collegamento ai gestionali esistenti».
- Prelievo con palmare industriale oppure con telefono: ticket «App nativa o web app».
- Come entra il DDT nel programma (foto del cartaceo, versione digitale, solo numero), resi al fornitore,
  ottimizzazione del venduto in UFP: sezione «Not yet specified» della mappa.
- Corrispondenza con Shopify: un pezzo prelevato resta «committed» per Shopify fino al Fulfillment (ricerca
  `docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md`); il connettore lo traduce.
