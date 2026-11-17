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
riferimento restano nel programma (59). Chi lo crea, con quali dati, e come si collega: sezione «Articolo nuovo da
foto».

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

## Modello dei dati

Dal ticket «Modello dei dati», chiuso il 16/11/2026. Decisioni 17, 26, 27, 37, 49, 59, 61, 66 e 68–86. Il ticket ha
tenuto conto del funzionamento attuale di ARS Logistica in UFP, descritto dall'utente in un documento che non sta nel
repository perché contiene dati personali; i fatti utili sono annotati nel ticket.

Qui si descrive cosa il programma ricorda e con quali regole, senza scegliere il database: lo stack è un ticket a parte.
I nomi delle entità sono quelli di `GLOSSARY.md`.

### Entità

**Catalogo**

| Entità | Cosa contiene | Note |
|---|---|---|
| Articolo | Descrizione, unità di magazzino, se si tiene a magazzino, ubicazione abituale facoltativa, provvisorio sì o no, da confermare sì o no, stato (attivo, rifiutato, unito a un altro articolo), chi l'ha creato, quando e da dove, prezzo di vendita e costo d'acquisto se i prezzi sono accesi | 37, 59, 72, 75, 78, 83, 105, 111, 114, 118 |
| Codice articolo | Valore com'è scritto, tipo (barcode, codice stampato, del fornitore, del produttore, interno), fornitore se è un suo codice, stato (confermato o da confermare) | Lo stesso codice può puntare a più articoli: allora il programma propone i candidati (24, 71) |
| Conversione | Articolo, fornitore, unità del fornitore, quantità nell'unità di magazzino, approvata da chi e quando | 72 |
| Foto di riferimento | Articolo, foto originale, impronta numerica, da dove viene (inserimento, conferma di un'identificazione), chi l'ha confermata | Filtri e tetto per articolo nella sezione «Percorso di identificazione» (96) |
| Contenuto del collo | Articolo, fornitore, ultimo contenuto confermato, chi e quando | Solo un consiglio, senza approvazione (100) |

**Ordini e persone esterne**

| Entità | Cosa contiene | Note |
|---|---|---|
| Fornitore | Codice, nome | |
| Cliente | Codice, nome; nient'altro | 79 |
| Ordine fornitore e righe | Numero, data, fornitore, riferimento cliente (sull'ordine o sulla riga); per riga: articolo, quantità ordinata, ricevuta, residuo | 39 |
| Proposta d'ordine | Ordine fornitore preparato dal programma, in attesa di conferma | 46 |
| Ordine cliente e righe | Numero, data, cliente, «banco» sì o no, stato (in attesa di pagamento, aperto, evaso, spedito); per riga: articolo, quantità, assegnata, prelevata, spedita | 21, 56, 63 |

**Ricevimento**

| Entità | Cosa contiene | Note |
|---|---|---|
| DDT | Numero del fornitore com'è scritto (con suffissi: «698/00»), numero interno, data, fornitore, stato (aperto o chiuso), carichi già mandati al gestionale | 40, 68, 82 |
| Riga del DDT | Articolo, riga d'ordine fornitore scelta, quantità in bolla (se nota), quantità contata, stato (pronta o ferma, con il motivo) | 70, 73, 82 |
| Scansione | DDT o prelievo, articolo, quantità, colli, come è stato identificato (barcode, codice stampato, aspetto, a mano), proposte mostrate, chi, quando, da quale dispositivo, esito | Ogni scansione è un dato a sé: due operatori sulla stessa riga sommano (86); identificazione registrata (104) |

**Giacenze e movimenti**

| Entità | Cosa contiene | Note |
|---|---|---|
| Ubicazione | Codice, tipo (normale, area di ricevimento, VEND, posto VEND) | Solo se il magazzino usa le ubicazioni (26); una sola area di ricevimento (86) |
| Giacenza | Articolo, ubicazione, stato della merce, quantità; mai sotto zero | Stati nella sezione «Ricevimento e assegnazione»; 77 |
| Assegnazione | Riga d'ordine cliente, articolo, quantità; nessuna ubicazione | 76 |
| Movimento | Tipo (carico, messa a posto, prelievo, spedizione, rettifica, correzione, passaggio in VEND), articolo, quantità, da e verso quale ubicazione o stato, documento d'origine (DDT, ordine), chi, quando, dispositivo, movimento corretto se è una correzione | 27, 74 |

**Lavoro e controllo**

| Entità | Cosa contiene | Note |
|---|---|---|
| Compito | Tipo (da mettere a posto, rimetti a posto), articolo, quantità, da dove | 62, 69 |
| Da controllare | Movimenti e avvisi per il responsabile: merce senza ordine, eccedenze, conteggi, collegamenti da confermare, differenze con la bolla, unità mai viste, possibili doppioni, differenze con il sistema d'origine | 31, 32, 45, 49, 71–73, 77, 86 |
| Coda di uscita | Documenti da mandare a gestionale o Shopify, con stato e tentativi | 54, 61 |
| Utente | Nome, ruolo (operatore o responsabile), PIN o password, attivo sì o no | 27, 80 |
| Configurazione | Le scelte per magazzino delle tabelle «Configurazione per magazzino» | |

**Provenienza.** Articoli, fornitori, clienti e ordini importati portano il sistema d'origine e il codice che hanno lì
(49, 66). Su quei campi il programma non scrive; ci aggiunge i propri dati.

### Ricevimento in un passaggio

Si fa tutto dal telefono (68): si apre il DDT, si scansiona, si chiude. Il computer resta possibile, non necessario.

1. Più operatori lavorano sullo stesso DDT, anche in giorni diversi. Non serve «sospendere»: ogni scansione è già salvata.
2. Per ogni articolo il programma sceglie la riga d'ordine fornitore: quella indicata sul DDT; se manca, prima le righe
   con il riferimento di un cliente, poi la più vecchia. L'operatore può cambiarla (70).
3. Un codice del fornitore sconosciuto lo collega l'operatore; il collegamento resta «da confermare» finché il
   responsabile non dice sì (71). Se dice no, il programma elenca i carichi fatti con quel collegamento, da correggere
   (86).
4. Un'unità del fornitore si converte con la conversione approvata; un'unità mai vista ferma la riga e la manda al
   responsabile (72).
5. La merce contata va nell'area di ricevimento: è già in giacenza e si assegna subito. La messa a posto si fa subito o
   più tardi, partendo dall'elenco «da mettere a posto»; il programma propone l'ubicazione abituale (69, 75).
6. Se la quantità in bolla è nota, le differenze con la contata vanno al responsabile (73).
7. «Chiudi DDT» manda un carico al gestionale. Se una riga è ferma, l'operatore sceglie se chiudere con le righe pronte
   (proposto) o aspettare; nel primo caso la riga ferma avrà poi un carico suo (61, 82).
8. Un DDT con stesso fornitore, numero e data di uno già registrato dà un avviso di possibile doppione (86).

Come entra la bolla nel programma (foto, file, solo numero) resta nella nebbia della mappa.

### Correzioni, rettifiche e storico

- Un movimento non si cancella mai. Un errore si corregge con una **correzione**, collegata al movimento sbagliato;
  giacenza e assegnazioni si rifanno da sole (74).
- Finché il DDT o il prelievo è aperto, corregge l'operatore che ha fatto il movimento; dopo la chiusura solo il
  responsabile, e al gestionale va una rettifica (81). Un DDT non si rifà da capo.
- Se la merce c'è ma non risulta, l'operatore conta l'ubicazione: la **rettifica** vale subito e va tra le cose da
  controllare (77). La giacenza non va mai sotto zero.
- Lo storico conserva per ogni movimento chi, quando, da quale dispositivo, cosa e con quale esito (27).

### Requisiti di affidabilità

Ricavati dai casi reali di UFP con ARS (scansioni perse dopo una sospensione, DDT non rintracciabile e rifatto) e dalla
decisione 23.

- Ogni scansione si salva sul server appena fatta e mostra il suo esito: salvata, in attesa, non riuscita.
- Ripetere un invio (doppio tocco, rete che torna, riapertura) non crea doppioni: ogni operazione ha la sua identità.
- Un DDT si trova sempre, in qualsiasi stato, con le sue righe, i carichi mandati e quelli in coda.
- Lo stesso codice su due righe d'ordine resta su due righe; un codice non si «indovina» da uno simile.

### Prezzi

Accesi per magazzino, spenti di serie (83). Con un gestionale accanto vengono da lì, a ogni scambio, e nel programma si
leggono soltanto; quando il programma è il gestionale principale si inseriscono a mano o da file. Al banco si mostra il
prezzo di vendita dell'articolo, uguale per tutti: listini e sconti del cliente li applica il gestionale (84). Il costo
d'acquisto lo vede solo il responsabile (85).

### Spazio per le estensioni

- Seriali, lotti e scadenze (17): giacenze e movimenti hanno posto per una «partita» facoltativa, vuota nella base.
- Campi aggiuntivi su articoli, ordini e clienti: si decide nel ticket «Punti di estensione per la specializzazione».

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Prezzi | accesi, spenti | spenti | 83 |
| Uscita automatica dal telefono | minuti senza uso | 30 | 80 |

### Rimandato ad altri ticket o alla nebbia della mappa

- Schermate del ricevimento, della messa a posto, della chiusura del DDT, delle cose da controllare e del banco: ticket
  «Percorso delle schermate».
- Foto di riferimento e impronte: risolte nella sezione «Percorso di identificazione e lettura della quantità».
- Prezzi, codici dei fornitori e conversioni da leggere in Ad Hoc: domande 17 e 18 in `docs/domande-rivenditore-ufp.md`.
- Catalogo visivo per la vendita al banco (idea dell'utente, 78 e 86): sezione «Not yet specified» della mappa.
- Inventario periodico: sezione «Not yet specified» della mappa; la rettifica per conteggio è già definita qui.

## Percorso di identificazione e lettura della quantità

Dal ticket «Percorso di identificazione e lettura della quantità», chiuso il 16/11/2026. Decisioni 6, 24, 25 e 87–104.
Ricerche: `docs/research/2026-11-15-modelli-visivi-riconoscimento-articoli.md` (§6, OCR e barcode) e
`docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (§C, rifiuto degli sconosciuti e ciclo di conferma).

Qui si descrive cosa vede e cosa fa l'operatore, non dove gira il calcolo: la divisione tra telefono e server è nel
ticket «Divisione tra telefono, computer e server in sede». Le soglie numeriche si fissano con la prova visiva (104).

### Un'inquadratura sola

L'operatore inquadra la scatola una volta. Il programma prova da solo, in quest'ordine, e si ferma al primo che basta
(87):

1. **Barcode.**
2. **Codice stampato**, letto come testo.
3. **Aspetto**, confrontato con le foto di riferimento.

Se nell'inquadratura ci sono codici di articoli diversi, il programma li mostra e l'operatore tocca quello giusto; non
registra nulla da solo. Due codici uguali sono lo stesso articolo (102).

### Articoli attesi

Il programma cerca prima tra gli **articoli attesi**; se lì non trova niente di convincente, cerca in tutto il catalogo e
avvisa «non è tra gli attesi» (88). Cosa è atteso dipende dal momento (97, 104):

| Momento | Articoli attesi | Se è un altro articolo |
|---|---|---|
| Ricevimento | Righe aperte di tutti gli ordini fornitore aperti del fornitore del DDT; in cima quelle indicate sul DDT (70) | Strada della merce non prevista (45, 48) |
| Prelievo | L'articolo della riga da prelevare | Stop con avviso: l'identificazione è un controllo |
| Messa a posto | L'elenco «da mettere a posto» | Avviso |
| Banco, conteggi | Nessuno: tutto il catalogo | — |

Al prelievo si inquadra anche l'articolo senza codici: se l'articolo da prelevare è tra le proposte dall'aspetto, un
tocco conferma; se non c'è, avviso (103).

### Cosa vede l'operatore

| Esito | Cosa vede | Tocchi | Decisione |
|---|---|---|---|
| Barcode su un solo articolo | Registrato subito, con la quantità letta se c'è; «Annulla» e quantità modificabile | 0 | 24, 99 |
| Barcode su più articoli | Le schede di quegli articoli, con foto; gli attesi in cima | 1 | 91 |
| Barcode da confermare | Scheda dell'articolo collegato; vale, ma chiede un tocco finché il responsabile non conferma | 1 | 71, 92 |
| Barcode sconosciuto | Si prosegue da soli con codice stampato e aspetto; trovato l'articolo, «Collego questo barcode?» | 1–2 | 92 |
| Codice stampato su un solo articolo | Scheda con foto: «È questo» / «No, è un altro» (apre le proposte dall'aspetto) | 1 | 90 |
| Codice stampato simile, un solo candidato tra gli attesi | Come sopra, con l'avviso «codice simile, controlla» | 1 | 89 |
| Aspetto | 3–5 proposte con foto | 1 | 24 |
| «Non lo so» | Riprova con un consiglio (più vicino, più luce), cerca scrivendo codice o descrizione, «Articolo nuovo» | — | 98 |

Un barcode sconosciuto collegato a un articolo segue le regole dei codici del fornitore: il collegamento vale subito, il
responsabile lo conferma, e se lo rifiuta il programma elenca i carichi fatti con quel collegamento (71, 86).

### Confronto del codice stampato

Un codice letto corrisponde a un codice a catalogo quando è uguale dopo aver trattato come equivalenti (89):

- i segni che si confondono: 0 e O; 1, I e l; 5 e S; 8 e B; 2 e Z;
- spazi, trattini e altri separatori, che si ignorano;
- maiuscole e minuscole.

Esempio: «A1O 0O1I» corrisponde ad A100011. Un carattere davvero diverso o mancante («A10001») si accetta solo se tra gli
attesi c'è un candidato solo, e con l'avviso. Non si cerca mai un codice «simile» in tutto il catalogo: è il requisito
«un codice non si indovina da uno simile» del modello dei dati. In ogni caso serve il tocco dell'operatore (24).

### Quantità

| Caso | Cosa propone il programma | Decisione |
|---|---|---|
| Numero nel barcode GS1 della scatola | Quel numero | 93 |
| Numero accanto a una parola di quantità (QTÀ, Q.TY, PZ, PCS, NR, CONF, «× 12») | Quel numero | 93 |
| Articolo che si conta a chili, metri o altra misura | Il valore in quell'unità sull'etichetta; con lordo e netto, il netto | 101 |
| Due numeri diversi | Li mostra entrambi; sceglie l'operatore, e la registrazione aspetta | 93, 99 |
| Unità del fornitore (CONF, coppie, tonnellate) | Convertita con la conversione approvata; un'unità mai vista ferma la riga | 72, 93 |
| Nulla di leggibile, ma un collo confermato in passato | L'ultimo contenuto del collo per articolo e fornitore, «come l'ultima volta» | 100 |
| Nulla di leggibile e nessun precedente | 1 per gli articoli a pezzi; vuoto per le altre unità | 95 |

Ogni proposta resta modificabile (25). Lotto, peso o misure non diventano mai la quantità di un articolo che si conta a
pezzi. Lotti, scadenze e seriali scritti nel barcode GS1 si ignorano nella base (17, 104).

**Più colli uguali.** Si scansiona un collo e si scrive quanti colli sono; chi preferisce li scansiona tutti, e ogni
scansione aggiunge un collo. Ogni scansione resta un dato a sé (86, 94).

**Contenuto del collo.** Ogni volta che l'operatore conferma quanti pezzi ha un collo, il programma lo ricorda per
articolo e fornitore. È solo un consiglio: non serve l'approvazione del responsabile, a differenza delle conversioni
(72, 100).

### Foto di riferimento

Diventano foto di riferimento le foto delle identificazioni confermate da barcode, codice stampato o tocco
dell'operatore (96):

- si scartano le foto mosse;
- al massimo una per articolo per DDT;
- un tetto per articolo, che tiene le foto più diverse tra loro; il numero si fissa dopo la prova (104);
- ogni foto ricorda chi l'ha confermata, e il responsabile può toglierla;
- le foto di un collegamento da confermare aspettano la conferma; se il collegamento è rifiutato, si scartano.

Si conservano le foto originali, non solo le impronte: se cambia il modello visivo, le impronte si ricalcolano (analisi
§4.2).

### Cosa si registra

Ogni identificazione registra come è avvenuta (barcode, codice stampato, aspetto, scritto a mano), con quali proposte,
chi l'ha confermata e da quale dispositivo (104). Anche ogni «non lo so» resta nello storico (98). Serve allo storico dei
movimenti e a misurare, con l'uso, dove il riconoscimento sbaglia.

### Da fissare con la prova visiva

- Quando un candidato è «convincente» tra gli attesi e quando si passa al catalogo intero (88).
- Quando l'aspetto dice «non lo so» (24).
- Quante foto tenere per articolo (96).
- Quanto bene si leggono codice stampato e quantità dalle foto reali: il piano della prova decide se misurarlo.

### Configurazione per magazzino

Nessuna scelta nuova: il percorso è lo stesso in ogni magazzino. Le parole di quantità si possono ampliare con i
termini dei fornitori di un magazzino; dove stanno (configurazione o modulo) si decide nel ticket «Punti di estensione
per la specializzazione».

### Rimandato ad altri ticket

- Dove girano lettura del barcode, del testo e confronto dell'aspetto: ticket «Divisione tra telefono, computer e server
  in sede» e «App nativa o web app».
- Le schermate (scheda «È questo», scelta tra più codici, «× colli», uscite del «non lo so»): ticket «Percorso delle
  schermate».
- Chi può creare l'articolo nuovo dall'uscita «Articolo nuovo»: sezione «Articolo nuovo da foto».
- Formati di etichette dei fornitori con regole proprie: ticket «Punti di estensione per la specializzazione».

## Articolo nuovo da foto

Dal ticket «Inserimento di un articolo nuovo da foto», chiuso il 16/11/2026. Decisioni 8, 27, 49, 55, 59, 60, 96, 98 e
105–118. Ricerche: `docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (3–5 foto per articolo come punto
di partenza, ipotesi) e `docs/research/2026-11-15-progetti-simili-riconoscimento-prodotti.md` (da 1 a 8 foto le
risposte giuste passano dal 51% al 79% in un progetto pubblicato).

### Da dove si parte

| Dove | Chi | Come |
|---|---|---|
| «Non lo so» al ricevimento, alla messa a posto, al banco, nei conteggi | Operatore o responsabile | Uscita «Articolo nuovo» (98, 105) |
| Prelievo | — | Non compare: un articolo diverso da quello da prelevare ferma con un avviso (97, 118) |
| Catalogo, da telefono o computer | Responsabile | Inserimento a mano o da file; le foto sono facoltative (55, 118) |
| Scheda di un articolo esistente | Chiunque | «Aggiungi foto», con la stessa guida (117) |

### Il flusso

1. **Righe che aspettano un articolo.** Al ricevimento, in cima compaiono le righe attese degli ordini fornitore con un
   articolo sconosciuto o solo descritto, con codice e descrizione già compilati. Scelta la riga, la merce segue la sua
   strada: VEND se c'è il riferimento del cliente, altrimenti il carico normale (109). Senza una riga che lo aspetta,
   l'articolo nuovo trovato fuori dagli attesi segue la strada della merce non prevista (45, 48, 118).
2. **Foto.** Fino a tre, guidate da un riquadro: davanti, etichetta con il codice, altro lato. La prima è obbligatoria;
   il programma avvisa se una foto è mossa o buia (106). Sono le prime foto di riferimento e seguono le loro regole (96).
3. **Dati.** Obbligatori foto, descrizione e unità di magazzino (di serie «pezzo»). I codici letti dalle foto (barcode,
   codice stampato) si compilano da soli e si correggono; al ricevimento il fornitore viene dal DDT (107).
4. **Descrizione.** La scrive chi crea l'articolo; le parole lette sull'etichetta compaiono come pezzi da toccare
   (marca, misure, materiale). Un modello che scrive la descrizione da solo si valuta dopo la prova visiva (108).
5. **Controllo dei doppioni.** Prima di salvare il programma cerca in tutto il catalogo con codici, descrizione e
   aspetto e mostra fino a 3 articoli simili: «È uno di questi?». Se sì, non crea niente: foto e codice nuovo si
   collegano a quell'articolo, da confermare (71, 92, 110).
6. **Salvataggio.** Creato da un operatore, l'articolo è **da confermare** (105). Ricorda chi l'ha creato, quando, da
   quale dispositivo e da quale DDT o momento del lavoro (118).

### Nell'attesa e alla conferma

- L'articolo da confermare si usa come gli altri (messa a posto, prelievo, banco, conteggi) e porta il segno «da
  confermare» sulle schede (115).
- Il responsabile lo trova tra le cose da controllare e ha tre uscite (114):

| Uscita | Cosa succede |
|---|---|
| Conferma | Il responsabile corregge o completa i dati (ubicazione abituale, prezzi, «si tiene a magazzino», 107) e l'articolo è a catalogo come gli altri |
| Unisci a un articolo esistente | Codici e foto passano all'esistente, la giacenza si sposta con correzioni collegate (74); il nuovo resta nello storico come «unito a…» (111) |
| Rifiuta | L'articolo non si usa più; la merce già ricevuta va «in attesa di decisione» (45), le foto si scartano, i movimenti restano nello storico |

L'unione serve anche per un doppione scoperto più tardi, chiunque l'abbia creato (111).

### Secondo il modo di lavorare

| Modo | Cosa succede all'articolo nuovo |
|---|---|
| Gestionale principale | Confermato, è definitivo e lo comanda il programma (49, 118) |
| Accanto a un gestionale | È anche **provvisorio** (59): un'attesa diversa da «da confermare», e le due possono valere insieme (118) |
| Magazzino Shopify | Si crea nel programma solo se non è venduto sul sito (60); se poi compare su Shopify con lo stesso SKU o barcode, il programma propone al responsabile di collegarlo, e da lì comanda Shopify (116) |

**Accanto a un gestionale**:

- Alla chiusura del DDT la riga di un articolo provvisorio è una riga ferma (82): l'operatore sceglie se chiudere con le
  righe pronte, e la riga ferma parte con un carico suo appena il gestionale conosce l'articolo (112).
- Un ordine al banco con un articolo provvisorio aspetta in coda e parte verso il gestionale appena l'articolo è
  collegato (115).
- Il programma collega da solo l'articolo provvisorio a un articolo del gestionale che ha uno dei suoi codici (barcode,
  codice stampato, codice del fornitore). Se ne trova più d'uno, o nessuno dopo un giorno, lo segnala al responsabile,
  che sceglie a mano l'articolo del gestionale (113). Foto di riferimento, ubicazioni e storico restano nel programma.

### Configurazione per magazzino

Nessuna scelta nuova.

### Rimandato ad altri ticket o alla nebbia della mappa

- Schermate dell'inserimento, della guida alla ripresa, del controllo dei doppioni, dell'unione e delle uscite del
  responsabile: ticket «Percorso delle schermate».
- Se l'inserimento con 1 o 3 foto basta al riconoscimento dall'aspetto, e quanto bene si leggono le parole
  dell'etichetta: ticket «Piano della prova di accuratezza visiva».
- Descrizione proposta da un modello che legge immagini e scrive testo: sezione «Not yet specified» della mappa.
- Cosa si fa della merce di un articolo rifiutato che si rende al fornitore: resi al fornitore, sezione «Not yet
  specified» della mappa.

## Dispositivi e forma del programma

Dal ticket «App nativa o web app», chiuso il 16/11/2026. Decisioni 9, 22, 23, 27, 80, 87 e 119–127. Ricerche:
`docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (§G OCR e barcode, §H fotocamera da web app) e
`docs/research/2026-11-15-modelli-visivi-riconoscimento-articoli.md` (§6).

### Dispositivi

| Dispositivo | Di chi | Come legge il barcode | Codice stampato e aspetto |
|---|---|---|---|
| Telefono Android | Azienda o dipendente (120) | Fotocamera, con il lettore di Chrome (`BarcodeDetector`) | Fotocamera |
| iPhone | Azienda o dipendente (120) | Fotocamera, con una libreria inclusa nella pagina (zxing-cpp in WebAssembly) | Fotocamera |
| Palmare industriale Android | Azienda (119) | Grilletto | Fotocamera |
| Computer con telecamera | Azienda | Telecamera, con il lettore del browser dove c'è, altrimenti la libreria | Telecamera |

Il codice stampato si legge sul server, con la foto che viaggia sulla rete interna (121, 127). Dove gira ogni altro passo
dell'identificazione lo decide il ticket «Divisione tra telefono, computer e server in sede».

IPOTESI da verificare sul palmare di UFP: il lettore a grilletto scrive il codice nel campo attivo come una tastiera
(per esempio il profilo «tastiera» di Zebra DataWedge), quindi la pagina tiene sempre pronto un campo che lo riceve
nelle schermate di identificazione.

### Una web app servita dal server in sede

- Su ogni dispositivo il programma si apre dal browser; non si installa nulla (121, 122). Lo serve il **server in
  sede**, che tiene anche i dati; la base non funziona senza (126).
- C'è una sola versione del programma, sul server: tutti i dispositivi usano la stessa (127).
- Il server si raggiunge solo dalla rete interna del magazzino: è il motivo della scelta (121).
- **Prima apertura**: si inquadra un QR stampato in magazzino con l'indirizzo del programma (127). Su Android e sul
  computer si può aggiungere un'icona.
- **iPhone**: si usa da Safari, con «Fotocamera: Consenti» impostato una volta nelle impostazioni del sito; la prima
  apertura guida l'operatore (124). Le web app aggiunte alla schermata Home richiedono di nuovo il permesso, soprattutto
  se la fotocamera è accesa quando lo schermo si spegne ([WebKit bug 280394](https://bugs.webkit.org/show_bug.cgi?id=280394),
  aperto, ultimo aggiornamento 08/07/2026); l'icona sulla Home si adotta solo se la prova su un iPhone vero lo permette.
  L'impostazione per sito di Safari è descritta da guide di terzi
  ([MacRumors](https://www.macrumors.com/how-to/access-website-settings-in-safari/)), non da Apple: va provata.
- **Fotocamera**: si accende solo nelle schermate che la usano e si spegne quando lo schermo si spegne o si cambia
  schermata (127).
- **Telefoni personali**: quando un dipendente se ne va basta disattivarne l'utente (27); sul telefono resta al
  massimo un segnalibro (127). Sui telefoni condivisi vale l'accesso con nome e PIN (80).

### Collegamento sicuro

Il browser dà la fotocamera solo a una pagina in contesto sicuro: `https`, oppure `localhost`; un indirizzo di rete
locale in `http` non lo è ([MDN, Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)).
Il certificato deve essere riconosciuto dal dispositivo (123):

| Magazzino | Certificato | Lavoro sui dispositivi | Internet |
|---|---|---|---|
| Con un dominio | Del dominio dell'azienda (per esempio magazzino.azienda.it), gratuito, rinnovato dal server da solo con la sfida DNS di Let's Encrypt ([tipi di sfida](https://letsencrypt.org/docs/challenge-types/)) | Nessuno | Solo per il rinnovo, verso il gestore del DNS |
| Senza dominio | Interno, creato dal server | Installarlo e renderlo attendibile su ogni dispositivo, anche personale, e a ogni dispositivo nuovo | No |

- Con il dominio il nome diventa pubblico (i certificati sono registrati in elenchi pubblici), ma da fuori non porta
  a nulla: il server resta sulla rete interna.
- IPOTESI da verificare in magazzino: alcuni router scartano le risposte DNS pubbliche che puntano a un indirizzo
  interno; in quel caso il nome si risolve con il DNS interno.

### Rete assente

L'operazione in corso (23) resta nella memoria del browser del dispositivo, legata all'utente che l'ha fatta, e parte
una volta sola quando la rete torna. Se qualcuno cancella i dati del browser prima, si perde: al rientro il programma
lo dice (127).

### Aggiornamenti

| Tipo | Chi decide | Quando |
|---|---|---|
| Normale | Il responsabile, dall'avviso «È disponibile un aggiornamento» | Quando sceglie, per esempio a fine giornata |
| Importante, come la correzione di un errore | Nessuno: è obbligatorio | Da solo, di notte |

In tutti e due i casi prima si fa una copia di sicurezza e i dispositivi aperti si ricaricano alla prima pausa, senza
perdere l'operazione in corso (125).

Da decidere con l'installazione (proposta non ancora confermata): chi segna un aggiornamento come importante; il
ritorno da solo alla versione precedente se dopo un aggiornamento notturno il programma non riparte; l'avviso al
responsabile il mattino dopo.

### Prove su dispositivi veri

Prima di scegliere lo stack (127):

- un iPhone: permesso della fotocamera in Safari con «Consenti» e, per confronto, dall'icona sulla Home (124);
- un telefono Android: lettura del barcode con il lettore di Chrome;
- un palmare di UFP: grilletto (ipotesi della tastiera) e fotocamera (119);
- il collegamento sicuro con il router di un magazzino vero (123).

### Configurazione per magazzino

- Dominio dell'azienda oppure certificato interno (123).

### Rimandato ad altri ticket o alla nebbia della mappa

- Cosa gira sul dispositivo e cosa sul server per ogni inquadratura, cosa viaggia in rete: ticket «Divisione tra
  telefono, computer e server in sede».
- Librerie del browser, del server e del meccanismo di aggiornamento: ticket «Stack».
- Schermate della prima apertura dal QR, della guida a «Consenti» su iPhone, dell'avviso di aggiornamento, del campo
  per il grilletto; la barra di Safari visibile su iPhone: ticket «Percorso delle schermate».
- Foto «di arrivo» della prova scattate dal browser dei telefoni: ticket «Piano della prova di accuratezza visiva».
- Procedura guidata, rinnovo del certificato, copie di sicurezza, ritorno alla versione precedente: installazione e
  configurazione iniziale, sezione «Not yet specified» della mappa.

## Prova di accuratezza visiva

Dal ticket «Piano della prova di accuratezza visiva», in corso dal 17/11/2026. Decisioni 12 e 128–. La prova decide il
modello visivo (12) e dà i numeri lasciati aperti dal percorso di identificazione (sezione «Da fissare con la prova
visiva»). La esegue il ticket «Esecuzione della prova visiva e scelta del modello». Ricerche:
`docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (§A, §C, §I) e
`docs/research/2026-11-15-modelli-visivi-riconoscimento-articoli.md` (§1, raccomandazione).

### Dove stanno le foto

| Cosa | Dove | Chi lo vede |
|---|---|---|
| Foto della prova | Repository GitHub privato e separato, solo per la prova (128) | Il proprietario e chi invita |
| Tabella sigla anonima → codice vero dell'articolo | Stesso repository privato (129) | Come sopra |
| Piano, script, risultati in numeri con le sigle anonime (A001, A002…) | Repository del progetto, pubblico (129) | Chiunque |

- Nelle foto solo scatole ed etichette; una foto con un volto, un documento o il nome di un cliente si rifà da un'altra
  faccia della scatola (130).
- Le foto restano dopo la prova, per rifarla con un modello nuovo e per l'eventuale adattamento del modello; si
  cancellano se il magazzino che le ha fornite lo chiede (131).

