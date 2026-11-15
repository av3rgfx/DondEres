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

- Creazione delle proposte d'ordine al fornitore e vendita al banco come fonte di ordini: risolte nella sezione «Fonti
  dei dati e collegamenti».
- Prelievo con palmare industriale oppure con telefono: ticket «App nativa o web app».
- Come entra il DDT nel programma (foto del cartaceo, versione digitale, solo numero), resi al fornitore,
  ottimizzazione del venduto in UFP: sezione «Not yet specified» della mappa.
- Corrispondenza con Shopify: un pezzo prelevato resta «committed» per Shopify fino al Fulfillment (ricerca
  `docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md`); il connettore lo traduce.

## Fonti dei dati e collegamenti

Dal ticket «Fonti degli ordini e collegamento ai gestionali esistenti», chiuso il 15/11/2026. Decisioni 19, 23 e
49–67. Ricerche: `docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md` e
`docs/research/2026-11-15-adhoc-revolution-ars-logistica.md`.

### Due modi di lavorare

| Modo | Quando | Da dove arrivano i dati |
|---|---|---|
| Gestionale principale | Il magazzino non ha un gestionale (magazzino Shopify) | Inserimento a mano, file, canali di vendita come Shopify |
| Accanto a un gestionale | Il magazzino ha già un gestionale (UFP con Ad Hoc Revolution) | Il gestionale, tramite file o connettore |

In tutti e due i casi il lavoro fisico (ricevimento, identificazione, prelievo, spedizione, inventario) lo fa il
programma. In UFP prende il posto di ARS Logistica, che non registra più movimenti (50).

### Chi comanda su un dato

Su ogni dato comanda il sistema che l'ha creato, il suo **sistema d'origine** (49).

- Un articolo o un ordine importato si cambia solo nel sistema d'origine. Il programma lo aggiorna a ogni scambio e
  non lo modifica; ci aggiunge i propri dati: foto di riferimento, codici in più, ubicazioni, assegnazioni, stati di
  magazzino.
- Ciò che nasce nel programma lo comanda il programma: ordini fornitore e proposte d'ordine del magazzino Shopify (46),
  ordini al banco (65), articoli nuovi da foto quando non c'è un gestionale.
- Ogni dato importato conserva il codice che ha nel sistema d'origine (numero d'ordine e di riga, codice articolo): così
  non si creano doppioni e i documenti tornano alla riga giusta (66).
- Le differenze che non tornano (per esempio una riga ridotta sotto quanto già spedito) diventano un avviso per il
  responsabile, non una correzione automatica.

| Dato | Gestionale principale | Accanto a un gestionale | Magazzino Shopify |
|---|---|---|---|
| Articoli | Programma (a mano, file) | Gestionale; articolo nuovo da foto provvisorio (59) | Shopify, una variante = un articolo (60); quelli fuori dal sito, programma |
| Fornitori | Programma | Gestionale | Programma |
| Ordini fornitore | Programma | Gestionale | Programma, anche dalle proposte con riferimento cliente (46) |
| Ordini cliente | Programma, file, canali di vendita | Gestionale | Shopify; banco nel programma |
| Ordini al banco | Programma (65) | Programma, poi mandati al gestionale (65) | Programma |
| Movimenti, assegnazioni, VEND | Programma | Programma, restituiti come documenti (61) | Programma |

### Ordini importati

- **Data per «dal più vecchio»**: la data dell'ordine nel sistema d'origine; per Shopify data e ora d'acquisto. A parità
  vale il numero d'ordine (16, 66). Il numero d'ordine di Shopify non è garantito in sequenza: per Shopify decide l'ora.
- **Articolo sconosciuto**: la riga entra lo stesso, resta senza merce e il responsabile vede un avviso (66).
- **Ordini non pagati**: entrano ma non ricevono merce, «in attesa di pagamento»; una volta pagati tornano in coda con
  la loro data. Scelta per magazzino, accesa di serie (63).
- **Ordine annullato o ridotto all'origine** (62):

| Dove è la merce | Cosa fa il programma |
|---|---|
| Assegnata o in VEND, non prelevata | La libera e rifà l'assegnazione dal più vecchio (37) |
| Già prelevata | Avvisa e crea il compito «rimetti a posto»; i pezzi tornano liberi quando l'operatore li ubica |
| Già spedita | Non cambia nulla e lo segnala al responsabile |

### Vendita al banco

- È un ordine cliente come gli altri, segnato «banco», che si preleva e si spedisce subito (56).
- Nasce sul telefono: chi vende sceglie il cliente (uno preciso, quello generico delle vendite al banco o nessuno),
  scansiona articoli e ubicazione, conferma (65). Accanto a un gestionale l'ordine va poi al gestionale, dove si fanno i
  documenti di vendita.
- Si prende prima la merce libera. Se non basta, il programma mostra a quali ordini verrebbe tolta e chi vende decide;
  se conferma, l'assegnazione si rifà e il movimento va tra quelli da controllare. La merce in VEND non si tocca (58).

### Articolo nuovo da foto con un gestionale accanto

Nasce **provvisorio** nel programma e si può ricevere subito. Il responsabile lo crea anche nel gestionale, con prezzi e
IVA. Al primo scambio il programma lo riconosce dal codice e lo collega: da lì comanda il gestionale, le foto di
riferimento restano nel programma (59). Chi può crearlo e quali dati servono: ticket «Inserimento di un articolo nuovo
da foto».

### Cosa entra e cosa esce

Nella base (51, 55):

- **inserimento a mano** di articoli, fornitori, ordini fornitore e ordini cliente;
- **importazione da file** degli stessi dati, per il primo caricamento (fino a 35.000 articoli) e per gli aggiornamenti;
- **esportazione su file** dei movimenti;
- un **punto d'aggancio per i connettori**, che traducono da e verso un sistema esterno.

Verso il gestionale il programma restituisce **un documento per ogni fatto di magazzino**, appena il fatto si chiude:
un carico per DDT ricevuto, uno per ordine prelevato, uno per spedizione, una rettifica per correzione (61). Con lo
scambio a file sono righe di un file; con un connettore, i documenti del gestionale.

Un ordine fornitore confermato nel programma diventa un documento (PDF e file) con il riferimento del cliente; una
persona lo manda al fornitore. Il programma non lo invia da solo (64).

### Collegamenti previsti

| Collegamento | Dove sta | Note |
|---|---|---|
| Scambio a file | Nella base | Via generale per qualsiasi gestionale e via di riserva (51) |
| Shopify | Modulo consegnato con la base, spento di serie | Da aggiornare almeno una volta l'anno (versioni trimestrali dell'API) |
| Ad Hoc Revolution | Specializzazione per UFP | Si progetta con le risposte del rivenditore (57) |
| ARS Logistica | Nessuno | Il programma ne prende il posto (50, 67) |

### Connettore Shopify

- **L'app** la crea l'organizzazione che possiede il negozio, dal proprio account, con le istruzioni del prodotto; il
  programma rinnova da solo l'accesso (53). Per un'app della stessa organizzazione Shopify prevede l'accesso più
  semplice e non chiede approvazioni (ricerca).
- **Dal sito**: prodotti e varianti (60), ordini e loro modifiche, annullamenti, pagamenti. Il programma considera solo
  la parte di ordine assegnata al suo magazzino (66).
- **Verso il sito**: arrivi e rettifiche come variazioni di quantità, e le spedizioni; Shopify scala da sé la merce
  spedita. «Evaso» non si manda (52). Va provato su un negozio di sviluppo come non scalare due volte la stessa uscita
  (ricerca, §3).
- **Il riferimento cliente** delle proposte d'ordine lo prende dall'ordine del sito (46).

### Scambio e guasti

- Il programma chiede le novità ogni 5 minuti (valore cambiabile), e subito con «aggiorna ora» o quando si apre una
  schermata che ne ha bisogno, come quella del banco (54). Il traffico parte sempre dal programma: nessun sistema
  esterno deve raggiungere il server in sede.
- Se lo scambio non riesce si continua a lavorare con gli ultimi dati. Ciò che va inviato resta in una coda conservata
  sul server e parte appena lo scambio torna, una volta sola. Dopo 15 minuti di errori il responsabile vede un avviso
  (23, 54).

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Modo | gestionale principale, accanto a un gestionale | da scegliere | 19 |
| Connettore Shopify | acceso, spento | spento | 51 |
| Intervallo di scambio | minuti | 5 | 54 |
| Solo ordini pagati ricevono merce | sì, no | sì | 63 |

### Rimandato ad altri ticket o alla specializzazione

- Domande al rivenditore di UFP: `docs/domande-rivenditore-ufp.md`. Le risposte servono al connettore Ad Hoc.
- Un articolo in più ubicazioni e prelievo con scansione dell'ubicazione (fatto riferito per UFP): ticket «Modello dei
  dati» e «Percorso delle schermate».
- Schermate del banco, del compito «rimetti a posto» e degli avvisi: ticket «Percorso delle schermate».
- Come entra il DDT nel programma: sezione «Not yet specified» della mappa.
