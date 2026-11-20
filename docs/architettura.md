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
| Da rendere | Decisa per il reso al fornitore, in attesa di partire (207); nell'area resi se il magazzino usa le ubicazioni (217) | No, finché il reso non parte o il fornitore non lo rifiuta (214) |

La spedizione fa uscire il pezzo dal magazzino. La quantità che un operatore vede come prelevabile è sempre:

```
prelevabile = in magazzino − assegnato − in VEND − prelevato − in attesa di decisione − da rendere
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
persona lo manda al fornitore. Il programma non lo invia da solo (64). Precisata dalla 311: parte con «Invia al fornitore»,
sezione «Punti di estensione».

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
- **Resi del cliente**: richieste, esiti, rimborsi, credito del negozio e il modulo della scelta del rimborso nella
  pagina dell'ordine stanno in «Resi» → «Reso del cliente nel magazzino Shopify» (322–343).

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
| Utente | Nome, ruolo (operatore o responsabile), PIN o password, mail aziendale facoltativa, attivo sì o no | 27, 80, 223 |
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
- Tempi massimi con il catalogo intero: esito di una lettura entro 1 secondo, schermate e ricerche entro 2 (195).
- Un DDT si trova sempre, in qualsiasi stato, con le sue righe, i carichi mandati e quelli in coda.
- Lo stesso codice su due righe d'ordine resta su due righe; un codice non si «indovina» da uno simile.

### Prezzi

Accesi per magazzino, spenti di serie (83). Con un gestionale accanto vengono da lì, a ogni scambio, e nel programma si
leggono soltanto; quando il programma è il gestionale principale si inseriscono a mano o da file. Al banco si mostra il
prezzo di vendita dell'articolo, uguale per tutti: listini e sconti del cliente li applica il gestionale (84). Il costo
d'acquisto lo vede solo il responsabile (85).

### Spazio per le estensioni

- Seriali, lotti e scadenze (17): giacenze e movimenti hanno posto per una «partita» facoltativa, vuota nella base.
- Campi aggiuntivi su articoli, ordini, clienti e fornitori: li crea l'admin in «Configurazione» (306); seriali, lotti e
  scadenze con un modulo nel punto d'aggancio «Partita» (314). Sezione «Punti di estensione».

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
- Inventario periodico: sezione «Inventario periodico» (decisioni 227–245).

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

Quando il codice scritto sulla scatola è diverso, anche di poco, da quello dell'articolo che corrisponde (per esempio
perché il fornitore lo ha cambiato), l'abbinamento lo conferma il responsabile: carica lo stesso la merce su
quell'articolo oppure aspetta di aver aggiornato il codice nel gestionale (158). Finché il responsabile non risponde, la
riga resta ferma come per l'articolo provvisorio (112), e il codice nuovo confermato diventa un codice del fornitore
dell'articolo (71); le schermate si disegnano nel ticket «Percorso delle schermate» (159).

Nel programma finito il codice non si scrive a mano: scriverlo resta il ripiego del «non lo so» (98, 151). Il barcode
della scatola spesso porta un codice diverso dal codice articolo e non distingue colore o variante; in UFP il codice
scritto sulla scatola è quasi sempre il codice articolo (157).

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
termini dei fornitori di un magazzino, in «Configurazione»; un formato con regole proprie richiede un lettore di
etichette (304, sezione «Punti di estensione»).

### Rimandato ad altri ticket

- Dove girano lettura del barcode, del testo e confronto dell'aspetto: ticket «Divisione tra telefono, computer e server
  in sede» e «App nativa o web app».
- Le schermate (scheda «È questo», scelta tra più codici, «× colli», uscite del «non lo so»): ticket «Percorso delle
  schermate».
- Chi può creare l'articolo nuovo dall'uscita «Articolo nuovo»: sezione «Articolo nuovo da foto».
- Formati di etichette dei fornitori con regole proprie: lettore di etichette (304), sezione «Punti di estensione».

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
- la ricarica della pagina a metà DDT, e la chiusura e riapertura del browser, senza perdere letture e senza doppioni
  (201; difetto riferito da utenti di Odoo 17);
- prima della consegna, una prova di carico sul server in sede con il catalogo intero e più telefoni insieme, per i
  tempi massimi della 195.

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

Dal ticket «Piano della prova di accuratezza visiva», chiuso il 17/11/2026. Decisioni 12 e 128–148. La prova decide il
modello visivo (12) e dà i numeri lasciati aperti dal percorso di identificazione (sezione «Da fissare con la prova
visiva»). La esegue il ticket «Esecuzione della prova visiva e scelta del modello». Ricerche:
`docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` (§A, §C, §I) e
`docs/research/2026-11-15-modelli-visivi-riconoscimento-articoli.md` (§1, raccomandazione),
`docs/research/2026-11-17-locateanything-nvidia.md`, `docs/research/2026-11-17-modelli-visivi-recenti.md`.

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

### Articoli

- Articoli di UFP; il magazzino Shopify fa, se possibile, una seconda prova con lo stesso piano (132).
- 200 articoli a catalogo e 40 lasciati fuori dal catalogo, fotografati solo come merce in arrivo: servono a misurare
  quante volte il programma dice «non lo so» invece di indovinare (133).
- Scelti a caso tra gli articoli che arrivano: la prova misura il caso di tutti i giorni (134).

### Foto

| Foto | Quante | Come | A cosa servono |
|---|---|---|---|
| Di riferimento | 3 per articolo a catalogo: davanti, etichetta, altro lato (135) | Come all'inserimento guidato di un articolo nuovo (106) | Sono ciò che il programma conosce; si misura con 1 e con 3 |
| Di arrivo | 3 per articolo, anche per quelli fuori catalogo (135), per ora tutte con l'iPhone; poi 1 per articolo con il palmare e 1 con l'Android (155) | Come in un ricevimento vero: in giorni o momenti diversi, luce normale (137) | Sono ciò che il programma deve riconoscere; mai usate come riferimento |

Stima con 200 + 40 articoli: 200 × 6 + 40 × 3 = 1.320 foto, circa 7 ore di scatti a 20 secondi per foto (deduzione).

**Pagina di scatto** (136): una pagina web, aperta dal browser del telefono come il programma vero, quindi con la stessa
fotocamera vista dal browser. Si legge il codice dell'articolo, si scattano le foto guidate, la pagina dà a ogni foto un
nome con articolo, tipo di foto, giorno e dispositivo. Le foto restano sul telefono; a fine giro si passano al computer e
si caricano nel repository privato (128). La pagina è solo codice, senza dati, su un indirizzo sicuro (per esempio
GitHub Pages), perché il browser apre la fotocamera solo da lì. La prepara il ticket «Esecuzione della prova visiva e
scelta del modello».

**Articoli di contorno** (139): 300 articoli in più, una sola foto davanti ciascuno; non si cercano mai, affollano la
ricerca. Con loro si provano 20, 100, 200 e 500 articoli attesi (138, 139).

Totale stimato: 200 × 6 + 40 × 3 + 300 × 1 = 1.620 foto con l'iPhone, circa 9 ore di scatti a 20 secondi per foto,
più 240 × 2 = 480 foto di arrivo con palmare e Android quando ci sono (deduzione, 155).

**Esecuzione** (decisioni 149–158). La pagina di scatto è in `prova-visiva/pagina-scatto/index.html` ed è pubblicata
con GitHub Pages dal ramo `gh-pages`, che contiene solo la pagina: https://av3rgfx.github.io/DondEres/ (149). L'utente
l'ha provata sull'iPhone il 17/11/2026: funziona (versione 1). Come lavora:

- **Dispositivo**: tipo, nome breve e sigla di chi scatta, impostati una volta; finiscono nel nome di ogni foto.
- **Riferimento**: si scrive il codice articolo (o lo legge il grilletto del palmare), poi tre foto guidate; dopo
  l'etichetta la pagina chiede codice stampato e quantità, con un tasto «uguale al codice articolo» (142, 157).
- **Arrivo**: si sceglie l'articolo dall'elenco di quelli fotografati come riferimento sullo stesso telefono, cercandolo
  con qualche cifra; il codice si scrive solo per gli articoli fuori catalogo (156). L'elenco registra se il codice è
  stato scelto o scritto.
- **Contorno**: si scrive il codice, una foto davanti.
- **Foto**: dal video del browser, lato lungo al massimo 1.920 pixel, JPEG; il riquadro al centro copre il 70% della foto
  in larghezza e altezza e le sue misure entrano nell'elenco, per il ritaglio della prova (145, 147).
- **Fine giro**: le foto restano nel browser del telefono finché si esportano in ZIP da al massimo 24 MB, con un elenco
  CSV; l'utente li carica nella cartella `da-caricare` del repository privato, l'agente li apre e li sistema (153).
  Safari può cancellare i dati di un sito non usato per 7 giorni: si esporta a fine giornata.
- Per palmare e Android, che non hanno l'elenco degli articoli fotografati sull'iPhone, servirà portarlo su quei
  dispositivi o scrivere il codice (da decidere quando ci sono, 159). Per ora scatta solo l'utente; la seconda persona
  della 137 arriva con palmare e Android (159).

Le quattro foto d'esempio mandate dall'utente (nel repository privato, cartella `esempi`, fuori dalla prova) mostrano
etichette di fornitori con il codice preceduto da parole come «Art.» o «Articolo», la quantità con «Pz.» o «Quantità»,
spesso un disegno del prodotto, a volte barcode e codice QR, e codici con lettere e numeri mescolati, anche minuscoli
(deduzione: le parole di quantità della 93 e i segni che si confondono della 89 servono davvero).

**Script del calcolo** (17/11/2026, in `prova-visiva/script/`, istruzioni in `LEGGIMI.md` della stessa cartella):
`prepara.py` apre gli ZIP e assegna le sigle, `impronte.py` calcola le impronte dei sei modelli con il riquadro e con
il ritaglio OWLv2, `valuta.py` calcola i numeri sull'aspetto e le soglie, `etichette.py` misura la lettura di codice e
quantità con PaddleOCR. Provati su una prova sintetica ricavata dalle quattro foto d'esempio (`prova_sintetica.py`):
la catena gira da capo a fondo e nei risultati non compaiono codici; i numeri della prova sintetica non valgono
niente. Scelte fatte negli script (deduzioni):

- Punteggio di un articolo: la somiglianza più alta tra la foto di arrivo e le sue foto di riferimento.
- Ritaglio OWLv2 senza testo: l'oggetto più probabile con il centro nel riquadro; a volte prende un'etichetta o una
  sola delle scatole impilate, ed è quello che la prova deve misurare.
- Articoli attesi pescati a caso 20 volte per foto; intervallo al 95% calcolato sul numero di foto.
- OCR sulla foto intera, con il testo cercato sulla foto ridotta a 1.280 pixel (a piena risoluzione PaddleOCR esaurisce
  i 16 GB della sessione); con «L» uguale a 1 nel confronto dei codici, perché in maiuscolo la «l» non si distingue.
- Tempi su CPU di questa sessione (4 processori), una foto per volta, solo per confrontare: PE-Core B 0,12 s, TIPSv2 B
  0,6 s, SigLIP 2 B 0,6 s, DINOv2 B 0,9 s, PE-Core L 1,1 s, SigLIP 2 L 2,3 s; ritaglio OWLv2 circa 4 s; OCR circa
  18 s per foto, con un picco di memoria di 7,7 GB. Sono tempi misurati mentre girava poco altro, sulle foto sintetiche.

Due punti da decidere con i primi numeri veri:

- Nella prova «cercare in tutto il catalogo» vuol dire cercare tra circa 540 articoli, non tra 35.000 (18): è molto più
  facile che nella realtà. La regola della 145 (soglia «convincente» più severa che rispetta il traguardo) porta quindi
  a mandare quasi tutte le foto alla ricerca in tutto il catalogo, che nella prova sembra gratis. Proposta: scegliere
  la soglia «convincente» in modo che le foto convinte su un articolo sbagliato restino sotto una quota fissata, e
  misurare a parte quanto peggiora la ricerca in tutto il catalogo al crescere degli articoli (500 e oltre).
- Una soglia scelta proprio al limite sulla prima metà, sulla seconda sta sotto il traguardo circa una volta su due,
  anche con un buon modello (visto sulla prova con impronte finte). Proposta: tenere un piccolo margine, oppure
  giudicare il traguardo con l'intervallo al 95%.

### Modelli

| Modello | Licenza | Taglie | Ruolo |
|---|---|---|---|
| SigLIP 2 | Apache-2.0 | media e grande | Candidato (146) |
| PE-Core | Apache-2.0 | media e grande | Candidato (146) |
| DINOv2 | Apache-2.0 | media | Candidato e termine di paragone (146) |
| TIPSv2 (Google, aprile 2026) | Apache-2.0 | media | Candidato nuovo, senza risultati pubblici sui prodotti (146) |
| DINOv3 | Licenza propria di Meta | media e grande | Solo confronto, dopo che l'utente ha letto la licenza e ottenuto l'accesso; nel prodotto solo se vince nettamente e l'utente accetta la licenza (141) |

La ricerca del 17/11/2026 non ha trovato modelli recenti con licenza commerciale migliori di SigLIP 2 e PE-Core sui
prodotti. C-RADIO di NVIDIA resta fuori per la licenza propria e la mancanza di risultati sui prodotti (148).
LocateAnything di NVIDIA non entra: localizza oggetti descritti a parole ma non riconosce quale articolo è, e la
licenza esclude l'uso commerciale (`docs/research/2026-11-17-locateanything-nvidia.md`).

### Cosa si misura

- **Aspetto**: articolo giusto al primo posto e tra le prime 5 proposte, con 20, 100, 200 e 500 articoli attesi, con 1 e
  con 3 foto di riferimento, diviso per dispositivo (135, 137, 139).
- **Codice stampato e quantità**: quante volte si leggono giusti, confrontati con quanto scritto da chi scatta (142).
- **Tempi**: solo nella sessione di Claude, per confrontare i modelli; la macchina vera quando si sceglie il server
  (143).

### Quando un modello basta

Con 100 articoli attesi, l'articolo giusto è tra le 5 proposte in almeno 95 arrivi su 100. Tra i modelli che ci
arrivano si sceglie il più veloce; se nessuno ci arriva, si studia l'adattamento (144).

### Come si calcola

Deduzioni confermate con la decisione 145.

- **Due metà.** Le foto di arrivo si dividono a caso in due metà: con la prima si scelgono le soglie, con la seconda si
  controllano. I numeri che contano sono quelli della seconda.
- **Soglie.** La soglia del «non lo so» (24) e quella dell'articolo «convincente» tra gli attesi (88) sono le più severe
  che rispettano ancora il traguardo (144). Si riporta quanti dei 40 articoli fuori catalogo ricevono «non lo so» e quanti
  articoli a catalogo lo ricevono per sbaglio.
- **Tetto di foto per articolo** (96): la prova confronta solo 1 e 3 foto; si parte da 10 e si rivede con lo storico
  delle identificazioni (104).
- **Codice stampato e quantità**: letti sul server con PaddleOCR (Apache-2.0), con il confronto dei segni che si
  confondono (89) e le parole di quantità (93); la verità è quanto scrive chi scatta (142).
- **Ritaglio**: ogni modello si misura con il riquadro al centro della pagina di scatto e con il ritaglio automatico
  della scatola (OWLv2, senza addestramento). Se il ritaglio aiuta molto entra nel programma, tenendo conto del lavoro in
  più per il server (147).
- **Articoli attesi simulati**: per ogni foto di arrivo si cerca tra l'articolo giusto e altri articoli presi a caso,
  fino a 20, 100, 200 o 500 (di contorno compresi), oltre che tra gli articoli lasciati fuori catalogo, che non hanno un
  giusto (deduzione).

### Lista delle foto da scattare

1. **Prima.** Fatto il 17/11/2026: repository privato `prova-visiva-foto` creato dall'utente e collegato alla sessione,
   pagina di scatto pubblicata e provata sull'iPhone (149). Se l'utente vuole DINOv3, ne legge la licenza e chiede
   l'accesso quando le foto ci sono (141, 154). Resta da fare: scegliere a caso, tra gli articoli che arrivano, 200
   articoli da mettere a catalogo, 40 da lasciare fuori e 300 di contorno (133, 134, 139).
2. **Foto di riferimento**, dalla pagina di scatto: per ognuno dei 200, davanti, etichetta (scrivendo codice stampato e
   quantità, vuoti se non ci sono) e altro lato; per ognuno dei 300 di contorno, solo davanti (135, 139, 142).
3. **Foto di arrivo**, in almeno due giorni e da almeno due persone: 3 per ognuno dei 200 e dei 40, per ora tutte con
   l'iPhone, poi 1 con il palmare e 1 con l'Android (155); con la merce come arriva, la luce normale e, quando si può,
   un collo diverso da quello delle foto di riferimento (135, 137, 145).
4. **A fine giro**: «Esporta le foto nuove» nella pagina, ZIP dal telefono al computer, poi nella cartella
   `da-caricare` del repository privato (128, 136, 153).
5. **Sempre**: solo scatole ed etichette; con un volto, un documento o il nome di un cliente la foto si rifà da
   un'altra faccia (130).

Totale: circa 1.620 foto e 9 ore di scatti con l'iPhone, più 480 foto di arrivo con palmare e Android quando ci sono
(deduzione, a 20 secondi per foto).

### Rimandato ad altri ticket o alla nebbia della mappa

- Pagina di scatto, script, calcolo, numeri e scelta del modello: ticket «Esecuzione della prova visiva e scelta del
  modello».
- Tempi sulla macchina vera e requisiti del server: «Server in sede: requisiti minimi» nella nebbia della mappa e ticket
  «Divisione tra telefono, computer e server in sede» (143).
- Adattamento del modello, se nessun modello raggiunge il traguardo: nebbia della mappa (144).
- Seconda prova sul magazzino Shopify, facoltativa, con lo stesso piano (132).
- Prove su dispositivi veri, compreso il tempo della rete dal telefono al server: sezione «Prove su dispositivi veri»
  (127).


## Percorso delle schermate

Dal ticket «Percorso delle schermate», chiuso il 17/11/2026. Decisioni 160–179. Qui si decide quali schermate ci sono e
in che ordine; colori, caratteri e stile vengono con il ticket «Aspetto grafico» (14).

Completato il 18/11/2026 nel ticket «Completezza del percorso delle schermate» (decisioni 180–201), dopo la ricerca
`docs/research/2026-11-18-gestionali-magazzino-esistenti.md` e l'analisi più sotto. Domande dei due giri nella pagina
privata https://claude.ai/artifact/13EHJFJ3ZbM8QNXU1dTkag.

Prototipo usa e getta a fil di ferro, con dati inventati e fotocamera simulata: `prototipi/percorso-schermate/index.html`,
pubblicato anche come pagina privata per il telefono dell'utente (https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur).
Si apre con un doppio clic o da un server locale; «Scenari» simula rete assente, uscita dopo 30 minuti, scambio bloccato
e il passaggio tra magazzino con i piani (come UFP) e con la coda (come Shopify). Le domande dei quattro giri sono in
una pagina privata (https://claude.ai/artifact/BpARZrpffCDENtsKzZgTSZ).

### Schermate della base

Elenco confermato (160), con i nomi cambiati dopo (178). Il responsabile ha le stesse schermate dell'operatore, più le
sue.

| Gruppo | Schermate |
|---|---|
| Entrare | Prima apertura dal QR (127); guida a «Fotocamera: Consenti» su iPhone, con la barra di Safari visibile, e cosa fare se il permesso è negato (124); accesso con nome e PIN, o password per il responsabile (80); uscita dopo 30 minuti senza perdere il lavoro |
| Ricevimento | DDT in sospeso e «Nuovo DDT»: fornitore, foto della bolla, numero e data letti da confermare, ordine citato, avviso di possibile doppione (86, 184); schermata del DDT con le righe nate dalle letture e «Attesi dal fornitore» da guardare (183, 186); «Aggiungi a mano» per articolo o per ordine (185); «Danneggiata» (191); registrato con «Annulla» e quantità (99); «È questo» / «No, è un altro» (90); scelta tra più articoli (91) o più codici (102); due quantità lette (93), «× colli» (94), «come l'ultima volta» (100); «non è tra gli attesi» (88); «Collego questo barcode?» (92); «codice simile, controlla» (89); codice diverso (158, 166); unità mai vista (72); «non lo so» con le sue uscite (98); correzione a DDT aperto (81); «Chiudi DDT» con riepilogo, quantità in bolla e scelta sulla riga ferma (82, 190, 192) |
| Articolo nuovo | Righe attese senza articolo, in cima (109); tre foto guidate, con gli avvisi di foto mossa o buia (106); scheda con i campi compilati (107); parole dell'etichetta da toccare (108); «È uno di questi?» (110) |
| Dopo il ricevimento | Da mettere a posto, per fornitore e dentro per DDT, proposto alla chiusura del DDT (69, 163, 194); rimetti a posto (62); posto VEND, se acceso (47) |
| Uscita | Piani di spedizione, per chi pianifica (167, 169); prelievo dai piani o dalla coda (167, 168); prelievo guidato con stop se l'articolo è un altro (97, 103, 164); fine della preparazione (171); spedizione (172, 173); vendita assistita (65, 58, 84, 178) |
| Sempre | Cose in sospeso in cima a ogni sezione (187); «Documenti» con storico per categoria e registro (189); «Cerca» sopra ogni lavoro (197) e dalla prima schermata: scheda, giacenze per ubicazione e stato, codici, prezzo; conta un'ubicazione da «Cerca e conta» (77, 244); inventario (229); «Aggiungi foto» (117); «Segna danneggiati» (191); rete assente, operazione in attesa o persa (23, 127) |
| Responsabile | Da controllare (86), con le sue uscite: tenere o rendere la merce non prevista (45), confermare conteggi, collegamenti e codici diversi (71, 158), approvare conversioni (72); articolo da confermare: Conferma, Unisci, Rifiuta (114); correzioni dopo la chiusura (81); scambio: avvisi e «aggiorna ora» (54); utenti con ruolo, mansioni e permessi (177); configurazione iniziale; «È disponibile un aggiornamento» (125); costo d'acquisto (85) |

Fuori: resi e inventario periodico hanno sezioni proprie («Resi», «Inventario periodico», 200); la lettura automatica della bolla ha un ticket di ricerca
(193); il catalogo visivo nella vendita assistita e la procedura guidata della configurazione iniziale restano nella
nebbia della mappa.

### Chi vede cosa

| Cosa | Decide | Decisioni |
|---|---|---|
| Cosa si può fare | I permessi che l'admin dà all'account, da sommare: Admin (utenti, permessi, configurazione, aggiornamenti), Responsabile di magazzino («Da controllare» di magazzino, inventari, articoli da confermare, resi, correzioni, costo d'acquisto), Responsabile dei piani (piani, preparazioni, avvisi della preparazione, spedizioni). Nelle sezioni di questa specifica «il responsabile» è il responsabile di magazzino, salvo piani e preparazione (responsabile dei piani) e utenti, configurazione e aggiornamenti (admin) | 27, 263, 264 |
| Lavori in più per un operatore | Il permesso «Responsabile dei piani» (al posto di «Pianifica le spedizioni», nessuno di serie) e «Conferma le spedizioni» (tutti di serie; l'admin lo può togliere). Senza il secondo la schermata «Spedisci» non c'è. Gli avvisi della preparazione vanno al responsabile dei piani; le conte fatte al prelievo anche al responsabile di magazzino | 169, 173, 264, 265 |
| Testi | Interfaccia pulita: parole brevi o icone, niente frasi di spiegazione; un «ⓘ» accanto al titolo di ogni schermata con poche righe su come si lavora; avvisi che servono per non sbagliare sempre visibili, brevi. La quantità che si può ancora dare o vendere si chiama «Disponibilità» | 261, 262, 266 |
| Cosa si vede per primo | Le mansioni, una o più per utente: magazziniere (ricevere, mettere a posto, rimettere a posto, cercare e contare) e preparatore (prelevare, vendita assistita, cercare) | 176, 177 |

**Prima schermata.** In grande un pulsante per ogni lavoro delle mansioni dell'utente, con il numero di cose che
aspettano; sotto, «Altri lavori» solo con i lavori che il responsabile gli dà in più nella sua scheda utente, uno per
uno, e quelli dei permessi («Spedisci», «Piani di spedizione»); senza, «Altri lavori» non c'è. Vale per tutte le
mansioni (250, 254). Con più mansioni la schermata le unisce.
Il responsabile vede tutti i lavori, più «Da controllare», «Piani di spedizione», «Utenti» e «Configurazione», e gli
avvisi di aggiornamento e di scambio bloccato (161, 177, 179).

### Ricevimento

1. **Ricevi DDT** → cose in sospeso (DDT miei, di colleghi, fermi, vecchi) e «Nuovo DDT» (187). Più persone lavorano
   sullo stesso DDT, anche in giorni diversi (68).
2. **Nuovo DDT** (184): si sceglie il fornitore (prima quelli con ordini aperti), si fotografa la bolla, il programma
   propone numero e data letti dalla foto e l'ordine citato; l'operatore li conferma o li scrive se la lettura non
   riesce. Senza bolla si continua senza foto. «Annulla» torna indietro senza creare niente.
3. **Schermata del DDT**: in alto l'inquadratura, sempre accesa; sotto le righe nate dalle letture, ognuna con l'ordine
   fornitore su cui è andata (prima l'ordine citato dalla bolla, poi quelli con il riferimento di un cliente, poi il più
   vecchio, 70), il cliente se c'è e la quantità ordinata, colorate per stato (in parte, completa, ferma). «Attesi dal
   fornitore» si apre per guardare le righe ancora attese; non riempie niente (186). In alto a destra «Chiudi DDT»
   (162, 183).
3. **A ogni inquadratura** il programma mostra solo l'esito (87). Un barcode su un solo articolo si registra senza
   tocchi, con un avviso «Registrato … · Annulla · Modifica» (99): si passa alla scatola successiva senza toccare lo
   schermo. Gli altri esiti aprono una scheda dal basso, sopra la schermata del DDT: proposte con foto, «È questo»,
   due quantità, «non è tra gli attesi», «Collego questo barcode?», «non lo so» (tabella «Cosa vede l'operatore» nella
   sezione «Percorso di identificazione»). La scheda della quantità ha più e meno, «× colli» e il consiglio «come
   l'ultima volta».
4. **Aggiungi a mano** (185, 224), quando una scatola non si legge. Prima scheda **«Dalla bolla»**: le righe della
   bolla non ancora trovate, nell'ordine del foglio (dalla lettura della bolla dove è accesa, altrove dall'ordine
   citato); si tocca la riga e si scrive il contato. Una riga senza ordine aperto si cerca a mano; se l'ordine manca
   davvero, «Manca l'ordine»: la riga diventa ferma (82) e va al responsabile, che crea l'ordine nel gestionale; al
   primo scambio la riga riparte con un carico suo, il resto del DDT si chiude con le righe pronte. Poi scheda «Per articolo» (gli articoli che il fornitore deve
   ancora mandare; toccato uno, gli ordini che lo contengono nell'ordine dell'abbinamento, con data, quantità mancante e
   cliente, il primo già proposto) e scheda «Per ordine» (gli ordini aperti del fornitore; dentro, gli articoli). Se la
   scatola aveva un barcode non riconosciuto, alla registrazione si propone di collegarlo (92).
5. **Danneggiata** (191), nella scheda della quantità: si conta, va da parte, non si assegna e va al responsabile.
6. **Righe che aspettano il responsabile** (codice diverso, unità mai vista): la riga diventa ferma e l'operatore mette
   la scatola da parte e continua; il responsabile decide da «Da controllare», oppure subito sullo stesso telefono con
   la sua password, senza far uscire l'operatore (166).
7. **Toccando una riga** si vede cosa è stato contato e si corregge l'ultima lettura, finché il DDT è aperto (81); una
   riga attesa senza articolo a catalogo si tocca in «Attesi dal fornitore» per creare l'articolo (109).
8. **Chiudi DDT** è una schermata di riepilogo (190, 192): foto della bolla; righe pronte con contati, ordinati e in
   bolla; righe ferme; danneggiati; attesi non arrivati. Guardando la bolla si tocca solo la riga dove la bolla dice
   un'altra quantità, e un atteso non arrivato se la bolla lo porta. Sotto, «Cosa succede se chiudi»: carico al
   gestionale, carico a parte per la riga ferma (82), differenze al responsabile, DDT che non si riapre (81). Tasti
   «Torna al DDT» e «Chiudi DDT» (o «Chiudi con le righe pronte»); poi «Metti a posto adesso» oppure «Più tardi» (163).

**Articolo nuovo**, dall'uscita del «non lo so» o da una riga senza articolo: righe che lo aspettano → tre foto guidate
→ dati (codice letto, descrizione con le parole da toccare, unità) → «È uno di questi?» → salvato «da confermare» e
torna alla scheda della quantità del DDT (105–110).

**Metti a posto**: area di ricevimento divisa per fornitore e dentro per DDT (194) e, sotto, «Rimetti a posto». Toccato un articolo: ubicazione
abituale proposta → scansione dell'ubicazione vera → quantità (69, 75).

### Preparazione e spedizione

Cambiamenti rispetto a oggi in UFP, proposti dall'agente e accettati: la copertura di ogni ordine si vede mentre si
crea il piano; la sigla è sostituita dal nome di chi ha fatto l'accesso; «spedito» si segna al ritiro, per corriere.

| Passo | Con i piani (UFP) | Con la coda (Shopify) | Decisioni |
|---|---|---|---|
| Chi dà il lavoro | Chi ha il permesso «Pianifica le spedizioni» crea il piano: titolo libero (proposto dall'agente dell'ordine, se il gestionale lo manda), preparatore, ordini con la loro copertura (completo, «3 di 5», niente). Un ordine arriva ai preparatori solo dentro un piano | Nessuno: «Prossimo ordine» dà l'ordine pronto più vecchio | 165, 167–169, 175 |
| Cosa vede il preparatore | Prima i suoi piani, poi quelli dei colleghi (di serie; si spegne per magazzino); accanto a ogni ordine l'avviso «N articoli non bastano», che aperto dice servono e disponibili | Il numero di ordini in coda e «Prossimo ordine» | 167, 168, 249, 250, 253 |
| Prendere un ordine | Chi lo apre lo prende; gli altri vedono «in preparazione da…»; chi pianifica riassegna | Chi lo riceve dalla coda lo prende; il responsabile rimette in coda un ordine lasciato a metà | 170, 175 |
| Prelievo | L'ordine si apre sull'elenco degli articoli (sotto, «Elenco del prelievo»); si preleva un articolo alla volta o con «Prelievo guidato», in ordine di ubicazione: scansione dell'ubicazione, inquadratura dell'articolo (stop se è un altro), quantità; la merce in VEND si prende dal suo posto; «Correggi giacenza» corregge la giacenza sul momento | Uguale | 76, 97, 103, 164, 246, 256, 270–284 |
| Fine | Colli, chili, «Preparato da» già compilato con chi ha fatto l'accesso e modificabile (se cambia, si registrano tutti e due i nomi), corriere in grande con l'indicazione del suo posto. L'ordine è evaso e al gestionale va il documento di prelievo | Uguale; a Shopify non si manda niente | 21, 52, 61, 171, 174, 175 |
| Spedizione | «Spedisci», per chi ha il permesso: ordini pronti divisi per corriere (e «Senza corriere»); si toccano quelli che restano; «Ritirato da …» segna spediti gli altri | Uguale; la spedizione si segna anche su Shopify | 52, 61, 172, 173, 175 |

**Elenco del prelievo** (ticket «Elenco del prelievo e correzione della quantità», 19/11/2026, decisioni 270–299;
domande in tre giri e riepilogo confermato nella pagina privata https://claude.ai/artifact/SdXpDTDFxGAs76mx17cNb5; prototipo con
l'ordine d'esempio 1060 di 15 articoli):

- **Apertura** (270, 282): aprendo un ordine si vede l'elenco degli articoli in ordine di ubicazione, con ubicazione e
  codice sopra, descrizione sotto, quantità a destra (completa, «1 di 3» se coperta in parte, «non risulta»). In cima
  **«Prelievo guidato»** e **«Sospendi»**; quando non resta niente da prendere, al loro posto «Fine preparazione».
- **Gruppi** (274, 281): «Da prendere» in alto; poi «Restano aperti», con quanti pezzi mancano di ogni articolo lasciato
  con «Concludi senza» o «Prosegui»; infine «Presi», chiuso, con solo ciò che si è preso davvero (un articolo preso in
  parte sta sia in «Presi» sia in «Restano aperti»). Le righe che non risultano stanno in fondo a «Da prendere» (257).
- **Toccando un articolo da prendere** (293, 294; prima la riga si allargava, 271, 272) si entra subito nell'articolo:
  in alto le giacenze per ubicazione con giacenza e disponibilità (258, 268), con l'abituale già scelta; toccandone
  un'altra si preleva da lì. Poi ubicazione, articolo, quantità e «Preso» (280), e si torna all'elenco. Lì ci sono anche
  **«Correggi giacenza»** e, sui coperti in parte, al posto di «Preso», **«Sospendi»** e **«Concludi senza»**: si prende
  quello che c'è e il resto resta aperto (279). Su un articolo che non risulta: «Correggi giacenza», «Sospendi» e
  «Concludi senza». Nell'elenco le giacenze non si toccano: i preparatori di UFP sono abituati a sceglierle dentro
  l'articolo.
- **Toccando un articolo preso** (295) la riga in «Presi» si allarga con **«Elimina»**, che toglie subito il prelievo
  (correzione collegata, 74; per esempio un articolo confermato a mano che non si ha in mano), e **«Rimetti a posto»**,
  che porta all'ubicazione da cui era stato preso: scansionandola il ritorno si conferma da solo, oppure si tocca
  «Conferma» senza scansionare (300). In tutti e due i casi l'articolo torna da prendere. Deduzione dell'agente: se era stato preso dall'area di
  ricevimento, «Rimetti a posto» porta alla sua ubicazione abituale.
- **Inquadrare dall'elenco** (276, 294): con l'elenco aperto, inquadrando o sparando un articolo dell'ordine si entra nel
  suo articolo; un articolo che non è nell'ordine dà lo stop (97). Al telefono un tasto in alto apre l'inquadratura; il
  palmare legge sempre con il grilletto.
- **Dall'area di ricevimento** (297, 69): tra le giacenze compare l'area di ricevimento (nome scelto alla
  configurazione; in UFP «CHECK», lo scarico in fondo al magazzino). Scelta lei, l'ubicazione non si scansiona e
  l'articolo si inquadra oppure si tocca «Conferma» (300).
- **Prelievo guidato** (164, 270, 272, 275): un articolo dopo l'altro, in ordine di ubicazione, con «‹» per tornare
  all'elenco. Su un articolo che non basta i tasti sono «Sospendi» e **«Prosegui»** (prende quello che c'è e passa al
  prossimo, il resto resta aperto) finché restano altri articoli; sull'ultimo «Concludi senza». Con l'ubicazione in conta
  da un collega (233) l'avviso resta e c'è **«Più tardi»**: la riga passa in fondo e torna quando si sono finite le
  altre; si può anche toccare un'altra ubicazione tra le giacenze. «Aspetto» non c'è più.
- **Quantità diversa da quella proposta** (283, 289): prima di registrarla, di più o di meno, il programma chiede
  conferma con i due numeri («Prendi 7 3PR-110? Ne servono 6: 1 in più» · «Cambia» / «Prendi 7»). Dopo, nessun
  messaggio al preparatore: il responsabile dei piani lo trova tra le cose da controllare (198, 264). Con 0 e «Concludi
  senza» (o «Prosegui») l'articolo resta aperto per intero: serve quando al cliente non serve una parte.
- **Correggi giacenza** (273, 256): sostituisce «Ne trovo di più» e «Ne trovo meno». Una scheda chiede «Quanti ce ne sono
  in C-02-4?», con sotto «Risultano 5»; il numero vale subito, come «Conta un'ubicazione», e si torna alla stessa riga, al
  punto della quantità. Le regole dietro restano quelle della 251 e della 252.
- **Tastierino** (284, 290, 291): al telefono e al palmare ogni quantità del programma (prelievo, ricevimento, conte,
  «Correggi giacenza», vendita assistita, colli e chili) si scrive con il tastierino del programma, che sale dal basso
  toccando il numero: 0–9, cancella, «OK», la virgola dove serve; «−» e «+» restano. La tastiera del telefono non si apre.
  Al computer si scrive con la tastiera e accanto al campo un'icona a forma di calcolatrice apre lo stesso tastierino.

**Ciò che resta da spedire** (285–288; fatti di UFP riferiti dall'utente il 19/11/2026):

- Il resto resta nello stesso ordine e parte dopo, segnato «resto» (248). Con i piani, dopo «Ordine pronto» il preparatore
  non vede più l'ordine: il resto lo segue solo il responsabile dei piani, e non torna da solo a un preparatore.
- **Con la coda** (296): il resto torna in coda da solo quando la merce lo copre, e il responsabile lo vede in «Da
  completare». In Configurazione «Con la coda, i resti»: «tornano in coda da soli» (di serie) o «passano dal
  responsabile», che li rimette in coda.
- **«Da completare»** in «Piani di spedizione» (286), sempre visibile al responsabile dei piani, in due gruppi: «Merce
  arrivata» (resti coperti e ordini sospesi da riprendere) e «Aspettano merce» (cosa manca e da quando). Il numero sul
  pulsante conta quelli con la merce arrivata.
- **Avviso** (287): appena la merce che manca è registrata al ricevimento, «Arrivato: 2 SF-09 per l'ordine 1060 (resto)»
  in «Da controllare» del responsabile dei piani e in «Da completare». La merce è già prelevabile anche dall'area di
  ricevimento (69).
- **Piano del resto** (288): «Crea piano» nell'avviso, o toccando il resto in «Da completare», apre il nuovo piano con il
  resto già dentro; il preparatore proposto è chi ha preparato la prima parte, e si cambia. Nel nuovo piano i resti con
  la merce arrivata stanno in cima. Un ordine sospeso torna di solito a chi l'aveva preso (247). Nel nuovo piano l'elenco
  degli ordini non ancora in un piano si chiama «Ordini da assegnare» (298).

**Vista da computer** (292): i responsabili e l'admin lavorano quasi sempre dal computer; aspetto e schermate si
progettano anche per il computer nel ticket «Aspetto grafico». Il prototipo resta una colonna larga come un telefono.

Piani e coda seguono le stesse regole: solo ordini pagati (63), ordini coperti in parte secondo la scelta del magazzino
(165). Nel nuovo piano un ordine con un articolo assente o con più pezzi della disponibilità dà un avviso che non blocca:
chiuso dice quanti articoli non bastano, aperto dice per ognuno servono e disponibili; l'ordine si aggiunge lo stesso
(249).

**Quando manca qualcosa al prelievo** (246–248, 251, 252, 255–257; correzione dell'utente del 18/11/2026):

- Sulla riga che non si completa il preparatore sceglie **«Sospendi»** o **«Concludi senza»** (nel prelievo guidato
  «Prosegui», 272). Se l'articolo
  risultava e non c'è, lo vede anche il responsabile, con la proposta di contare l'ubicazione (244).
- **Ordine sospeso** (247): anche per giorni. La merce già presa resta prelevata per quell'ordine e non va ad altri. Di
  serie non si registra dove resta il pacco (oggi sul tavolo del preparatore, con il riferimento); per magazzino si
  accende un'ubicazione per gli ordini sospesi (di serie «SOSPESI») e allora si inquadra dove resta. L'ordine sta nei
  «Fermi» di «Preleva» con il motivo; chi pianifica lo vede e può darlo a un altro (170). Quando arriva il mancante passa
  a **«Da riprendere»**.
- **Concludi senza** (248): il resto resta aperto sullo stesso ordine e riceve la merce appena arriva, dal più vecchio
  (16). Quando è coperto l'ordine torna da preparare: con i piani va in «Da completare» del responsabile dei piani, che crea il piano (285–288), segnato «resto»; con la
  coda di nuovo in coda. Al gestionale e a Shopify parte una spedizione per volta (su Shopify due evasioni dello stesso
  ordine).
- **Correggi giacenza** (251, 252, 256, 273; prima «Ne trovo di più» e «Ne trovo meno»): un passo solo per il preparatore. Scrive quanti pezzi ci sono
  nell'ubicazione; la giacenza si corregge subito, come con «Conta un'ubicazione», e lui torna alla stessa riga, al
  punto della quantità, e preleva. Se ne restano meno di quelli che servono, sospende o conclude senza. Dietro, i pezzi
  trovati vanno all'ordine in preparazione (eccezione alla regola del più vecchio, perché la merce è già in mano); il
  responsabile trova la conta tra le cose da controllare, con gli ordini più vecchi che quei pezzi li aspettavano.
- **Giacenze sulla riga** (258, 268): fin dall'inizio della riga, sotto l'articolo, la giacenza in ogni ubicazione e in
  tutto il magazzino e la disponibilità; di serie è scelta l'abituale, se ne tocca un'altra per prelevare da lì. Le righe in VEND si prendono solo
  dal loro posto. Con le quantità sotto gli occhi, «Correggi giacenza» non è una conta cieca, come la conta aperta
  dalla scheda dell'articolo (244).
- **Righe che non risultano** (257): compaiono in fondo al prelievo, con «Non risulta. Se lo trovi, correggi la giacenza»; un
  ordine con un articolo che non risulta si apre lo stesso.
- **Niente da prendere** (268): se a fine prelievo non si è preso nessun pezzo,
  l'ordine non può diventare pronto; il preparatore lo lascia (torna da preparare quando arriva la merce) o lo
  sospende.
- La scelta «Ordini coperti in parte si prelevano» (165) resta: se è «no», un ordine coperto in parte non entra in coda;
  con i piani chi pianifica vede l'avviso e decide (255). Un ordine pronto troppo tardi per il corriere resta pronto e parte con il ritiro successivo (172). Il corriere
viene dall'ordine nel sistema d'origine (su Shopify il metodo di spedizione) o lo sceglie chi pianifica (175).

### Vendita assistita

È il lavoro che la base chiamava «banco» (178). Passi della 65: cliente (uno preciso, quello generico o nessuno) →
inquadratura dell'articolo e scansione dell'ubicazione, con il prezzo di vendita a schermo e il costo solo per il
responsabile (84, 85) → se la merce libera non basta, l'avviso con l'ordine a cui verrebbe tolta (58) → «Conferma: crea
l'ordine nel gestionale». Una vendita non confermata resta tra le cose in sospeso con cliente e articoli; la merce non
si toglie a nessuno finché non si conferma; alla conferma il programma ricontrolla la disponibilità e avvisa se nel
frattempo qualcosa è finito; «Annulla vendita» la toglie con una conferma (188). Alla conferma non si sceglie come esce la merce: in UFP l'ordine si crea in Ad Hoc, dove si
fanno e si stampano le ricevute, e il resto si fa lì (178). In UFP la vendita assistita serve al banco e anche a
preparare una vendita o un pacco per un agente o da spedire (176).

Giacenze e ricerca (258–260, 277): gli articoli della vendita usano lo stesso elenco del prelievo; toccando una riga si
vedono le giacenze per ubicazione e la disponibilità e si sceglie da dove prenderlo (di serie l'abituale), con i tasti
«Quantità» ed «Elimina», che toglie l'articolo dalla vendita (con «Annulla» per qualche secondo, 190). Da «Cerca» un articolo si aggiunge alla vendita con la quantità,
senza inquadrarlo, con le stesse regole della lettura; nel registro risulta aggiunto a mano.

### Cose in sospeso

In cima a ogni sezione (181, 187), quattro gruppi, ognuno dal più vecchio: **i miei, in corso**; **di colleghi**, con
chi e da quanto; **fermi**, con il motivo; **vecchi**, oltre 2 giorni (si cambia per magazzino). Il numero sul pulsante
della prima schermata conta ciò che tocca a chi ha fatto l'accesso.

| Sezione | Cosa è in sospeso |
|---|---|
| Ricevi | DDT aperti; fermi se hanno una riga che aspetta il responsabile |
| Metti a posto | L'area di ricevimento, per fornitore e DDT (194), e «Rimetti a posto» |
| Preleva | Ordini presi e non finiti, con da quanto; fermi con il motivo; vecchi da liberare (170, 175) |
| Spedisci | Ordini pronti per corriere, con da quando; vecchi da controllare |
| Vendita assistita | Vendite non confermate (188) |
| Da controllare (responsabile) | Tutto ciò che aspetta una sua decisione (86) |

### Documenti

Due viste dello stesso storico (182, 189):

- **Documenti**, per categoria: DDT (con foto della bolla, righe, cronologia), preparazioni, spedizioni per corriere e
  giorno, vendite assistite, conteggi e correzioni, scambi con il gestionale. Ricerca per numero, articolo, cliente.
- **Registro**: ogni operazione in ordine di tempo, con chi, quando, da quale dispositivo ed esito (salvata, in attesa,
  non riuscita, inviata), compresi accessi, uscite, decisioni del responsabile e modifiche di configurazione. Filtri per
  persona, dispositivo, articolo, documento, esito.

Tutti vedono i documenti; il registro completo lo vede il responsabile, l'operatore vede le sue operazioni. Il costo
d'acquisto resta al responsabile (85). Il responsabile esporta in file (foglio di calcolo e PDF) un periodo o una
categoria; niente si cancella da solo (199).

### Annulla e Conferma

Regola unica (190):

| Tipo di azione | Esempi | Comportamento |
|---|---|---|
| Frequente | Lettura, quantità, messa a posto, presa di un ordine | Si registra subito; «Annulla» per qualche secondo, poi «Modifica» dalla riga finché il documento è aperto |
| Chiude un documento | «Chiudi DDT», «Ordine pronto», «Ritirato da…» | Riepilogo delle conseguenze e tasto con il verbo; «Torna indietro» |
| Tocca altri ordini o il lavoro di altri | Togliere merce a un altro ordine (58), riassegnare un ordine (170) | Conferma che nomina ciò che si tocca |
| Grave | Rifiutare un articolo (114), chiudere un residuo (33), scartare merce (191) | Solo il responsabile, con conferma |

Annullare non cancella: crea una correzione collegata, visibile nel registro (74). Nessun «Sei sicuro?» generico; nessun
tasto che riempie le quantità attese (186). Ogni scheda che si apre dal basso ha il suo «Annulla»; nelle procedure a
passi (nuovo DDT, nuovo piano) «Annulla» torna indietro senza creare niente (201).

### Merce danneggiata

Si segna al ricevimento («Danneggiata» nella scheda della quantità) e dalla scheda dell'articolo («Segna danneggiati»)
per la merce già a magazzino: si conta, non si assegna a nessun ordine e va al responsabile, che decide se tenerla,
renderla al fornitore o scartarla (191). Lo scarto manda uno scarico al gestionale.

### Tempi, suoni e ricerca durante il lavoro

- **Tempi massimi** (195), con il catalogo intero e più telefoni insieme, misurati sul server in sede prima della
  consegna: esito di un barcode o di un codice entro 1 secondo; schermate e ricerche entro 2 secondi. Il riconoscimento
  dall'immagine ha i suoi tempi nella prova visiva (143).
- **Suoni** (196): lettura riuscita con suono breve e vibrazione dove il telefono la permette; suono diverso per riga
  ferma o errore; il messaggio a schermo c'è sempre; volume per telefono, spegnibile.
- **Cerca** (197): in ogni lavoro un tasto apre la ricerca sopra (scheda, giacenze, conta); chiudendola si torna al
  punto.
- **Prelievo oltre il richiesto** (198, 201, 283): conferma prima di registrarlo, si accetta e i pezzi escono come prelevati per l'ordine; il
  responsabile sceglie se cambiare l'ordine nel gestionale o rimettere il di più a magazzino con una correzione.

### La preparazione oggi in UFP

Fatto riferito dall'utente il 17/11/2026, nella nota alla domanda sulla prima schermata:

1. Due persone al computer (supervisori o operatori) creano i **piani di spedizione**. Il titolo del piano è il nome
   dell'agente che ha fatto la vendita, scritto da chi crea il piano.
2. Un piano contiene più ordini ed è assegnato a un preparatore. Chi crea il piano vede subito le quantità disponibili
   degli articoli degli ordini, e decide se dare un ordine coperto in parte (165).
3. Il preparatore vede prima i suoi piani, poi quelli degli altri preparatori, divisi e ordinati: se serve aiuta un
   collega facendo i suoi piani.
4. Entrato in un piano, sceglie un ordine e parte il prelievo guidato.
5. Alla fine conferma il numero dei colli e i chili, firma con la propria sigla (chi ha preparato) e vede con quale
   corriere parte la merce (per esempio BARTOLINI, GLS). I colli vanno nel posto del loro corriere; la spedizione la
   conferma l'operatore, non il preparatore, quando la merce parte davvero (172).

Gli agenti portano gli ordini di persona; gli ordini degli agenti stanno in Ad Hoc, e chi crea i piani deve vederli:
serve il collegamento con Ad Hoc della specializzazione (178). Nel magazzino Shopify oggi si lavora con fogli di carta.

### Analisi del 18/11/2026: cosa manca alla base

Scritta dall'agente all'inizio del ticket «Completezza del percorso delle schermate», sulla base della ricerca
`docs/research/2026-11-18-gestionali-magazzino-esistenti.md` e dei fatti riferiti dall'utente su UFP. Non contiene
decisioni: le scelte dell'utente sono nei giri di domande del ticket e in `docs/decisioni.md`. Priorità = deduzione
dell'agente.

**Come si lavora oggi in UFP e cosa cambia** (fatti riferiti dall'utente, ticket «Modello dei dati» e «Percorso delle
schermate»):

| Oggi con ARS | Nella base | Stato |
|---|---|---|
| Controllo a penna sulla bolla, poi DDT al computer importando a mano le righe dagli ordini, poi lista «Libera» al palmare: la stessa merce si registra due volte | Un passaggio dal telefono: le righe nascono dalle letture (68, 183) | Deciso |
| Scansioni perse dopo «Sospendi»; un DDT corretto cancellandolo e rifacendolo | Salvataggio immediato con esito, correzioni collegate, DDT sempre ritrovabile (74, 81) | Deciso; da provare |
| Piani di spedizione per agente, firma con la sigla, spedizione confermata dall'operatore | Piani con copertura visibile, nome di chi ha fatto l'accesso, «Spedisci» per corriere (167–174) | Deciso |
| Vendita al banco da telefono: cliente, articoli e ubicazione, conferma; ricevute in Ad Hoc | Vendita assistita con gli stessi passi (178) | Deciso; manca cosa succede se resta a metà |
| La bolla di carta si scansiona e si carica in ufficio | Nessuna decisione su foto o archivio della bolla | Manca |

**Cosa manca rispetto ai gestionali esistenti.** Le funzioni ricorrenti nei prodotti letti che la base non ha:

| Mancanza | Dove nei prodotti | Priorità UFP / Shopify |
|---|---|---|
| Elenchi delle cose in sospeso per sezione (181) | Cruscotto di Odoo: da fare, in ritardo, senza responsabile, i più vecchi | Alta / Alta |
| «Documenti» con storico per documento e registro delle operazioni (182) | «Moves History» di Odoo, «Change Log» di Business Central | Alta / Alta |
| Regola unica per «Annulla» e «Conferma» (180) | Contro-registrazioni in Business Central e SAP B1; «Annulla» prima della validazione in Odoo | Alta / Alta |
| Foto e archivio della bolla | Nessun prodotto la legge in modo affidabile; servizi solo in cloud e solo per la testata | Alta / Media |
| Merce danneggiata e scarto | «Scrap» di Odoo; reso del danneggiato in SAP B1 | Media / Media |
| Resi da cliente e al fornitore | In tutti i prodotti | Media / Alta |
| Inventario periodico con conta cieca | Odoo, Business Central | Media / Media |
| Etichette e distinta del corriere | ShipStation, Odoo | Media / Media (dipende dalle domande 21–22 al rivenditore) |
| Requisito di velocità con 35.000 articoli | Lentezza riferita in Odoo con cataloghi grandi | Alta / Media |
| Avviso se Shopify cambia una giacenza che la base non ha mandato | Giacenze sovrascritte da altre app, riferito | — / Alta |

**Difetti riferiti da non ripetere** (esperienze di utenti, non fatti verificati):

- Validare senza aver scansionato, ignorando l'avviso (Odoo): la base non ha un tasto «riempi con l'atteso».
- Residuo chiuso per sbaglio senza ritorno (Odoo): nella base lo chiude solo il responsabile (33).
- Dopo una ricarica a metà la quantità attesa si riscrive (Odoo 17): nella base l'atteso viene dall'ordine; da provare.
- Lentezza con molti articoli (Odoo): serve un tempo massimo misurabile per l'esito di una scansione.
- Ordini «presi» e mai finiti (NetSuite, blocchi che restano): mostrare da quanto un ordine è preso (170).
- Giacenze Shopify riportate a zero o scritte sul valore sbagliato da altre app: la base manda variazioni (52).

**DDT: soluzioni migliori di quella attuale (183).** La 183 coincide già con le soluzioni dei prodotti per PMI più
completi (Business Central mette più ordini in un'entrata, NetSuite cerca l'ordine per articolo). Ciò che si può
aggiungere, dal più economico:

1. Foto della bolla all'apertura del DDT, salvata con il DDT e visibile in «Documenti»: archivio e controllo delle
   differenze con la bolla (73) senza scansioni in ufficio.
2. Numero e data proposti dalla foto, letti in sede (PaddleOCR, 145), confermati dall'operatore; servono anche all'avviso
   di doppione (86). Da provare su DDT veri.
3. Numero d'ordine stampato sulla bolla, se c'è: le letture vanno prima su quell'ordine (70).
4. Righe della bolla lette solo come «quantità in bolla», mai come quantità contata: da provare fornitore per fornitore.
5. Avvisi di spedizione elettronici dei fornitori (EDI, Peppol) e riconciliazione con la fattura differita: punti
   d'estensione e specializzazione, non base.

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Ordini coperti in parte si prelevano | sì, no | sì | 165 |
| I preparatori vedono il lavoro dei colleghi | sì, no | sì | 250, 253 |
| Ubicazione per gli ordini sospesi | spenta, accesa (con nome) | spenta; nome di serie «SOSPESI» | 247, 255 |
| Piani di spedizione | accesi, spenti (si lavora con la coda) | spenti | 167, 175 |
| Chili a fine preparazione | richiesti, facoltativi | richiesti | 171, 175 |
| «Vecchi» nelle cose in sospeso dopo | giorni | 2 | 187 |

Per utente: ruolo, mansioni, lavori in più, permessi «Pianifica le spedizioni» e «Conferma le spedizioni» (169, 173,
177, 254). Per
telefono: volume dei suoni, spenti o accesi (196).

### Rimandato ad altri ticket o alla nebbia della mappa

- Colori, caratteri, disposizione e stile: ticket «Aspetto grafico».
- Prove con la fotocamera vera su iPhone, Android e palmare: sezione «Prove su dispositivi veri» (127).
- Agente e corriere sull'ordine in Ad Hoc, colli e peso restituiti: domande 21 e 22 per il rivenditore; collegamento con
  Ad Hoc nella specializzazione (51, 178).
- Cosa succede in UFP alla merce di una vendita assistita che non parte subito (pacco per un agente o da spedire):
  sezione «Punti di estensione» (308, 317).
- Resi e inventario periodico: sezioni «Resi» e «Inventario periodico» (200, 207–226, 227–245).
- Lettura automatica di tutti i dati della bolla, da foto o PDF (193): ticket «Lettura automatica delle bolle».
- Confronto tra merce caricata e fattura: punto d'aggancio facoltativo, sezione «Punti di estensione» (192, 310).
- Catalogo visivo nella vendita assistita, procedura guidata della configurazione: nebbia della mappa.

## Lettura automatica delle bolle

Dalla ricerca «Lettura automatica delle bolle», chiusa il 18/11/2026: `docs/research/2026-11-18-lettura-automatica-bolle.md`.
Decisioni 192, 193 e 202–206. La prova la esegue il ticket «Esecuzione della prova di lettura delle bolle». Domande
nella pagina privata https://claude.ai/artifact/KQtNpyrXjbywxnz1iGKnGY.

### Cosa si sa

- Testata (fornitore, numero, data, ordine citato): leggibile in sede con strumenti a licenza commerciale. Righe con
  codice e quantità: leggibili da modelli recenti in sede, ma nessuna fonte li misura su bolle italiane. Finché la prova
  non dice il contrario, le quantità in bolla entrano come nella 192; quelle lette restano «quantità in bolla», mai
  contate (183, 193).
- Sulle bolle vere di UFP (3 fornitori, viste il 18/11/2026) una parte dei dati è già in codici stampati: il DataMatrix
  di AGB porta numero e data del DDT, i barcode di ISEO l'EAN di ogni riga. Si leggono senza riconoscere il testo
  (zxing-cpp, Apache-2.0); il DataMatrix tiene anche insieme le pagine dello stesso DDT.
- Ogni bolla porta due numeri d'ordine: la conferma del fornitore e l'ordine di UFP, scritto in posti diversi per ogni
  fornitore. L'abbinamento usa quello di UFP (70).
- Righe che non sono merce, da scartare: intestazioni «Saldo» e «Acconto», righe con il solo numero d'ordine,
  riferimenti del cliente, pallet a rendere, testi legali, merce in sconto (da distinguere o sommare: da chiarire).
- Strumenti esclusi per licenza: LayoutLMv3, DocTr, Qwen2.5-VL-3B e derivati (Nanonets-OCR, OCRFlux), Marker, Surya e
  Chandra (soglia di ricavi), HunyuanOCR (esclude l'UE), jina-ocr. Da evitare dentro il programma: PyMuPDF (AGPL),
  Poppler (GPL).
- Gli scanner di documenti di Android e iPhone funzionano solo nelle app native: nella web app (121) ritaglio e
  raddrizzamento si fanno con OpenCV.js o jscanify.

### Come si legge una bolla (proposta da provare)

1. **Codici stampati** su ogni pagina (zxing): numero e data dal DataMatrix, EAN delle righe. Dove ci sono, valgono più
   del testo letto.
2. **Foto o PDF.** Dal PDF con testo si legge il testo senza riconoscimento (pdfplumber, MIT). Dalla foto: ritaglio,
   raddrizzamento, contrasto, poi uno dei sistemi della prova.
3. **Uscita in uno schema fisso** (tipo di documento, testata, righe con il loro tipo, ordine di UFP, Saldo/Acconto,
   segni a mano), vincolato in JSON dove il sistema lo permette.
4. **Controlli sugli ordini aperti** del fornitore scelto: numero d'ordine di UFP per gruppo di righe, poi codice o EAN,
   poi quantità residua. Un codice che non c'è negli ordini aperti è un avviso, non una riga.
5. **Numero e data** si propongono all'apertura del DDT (184); **le righe** alla chiusura (192), quindi il server ha il
   tempo del conteggio per leggerle.

Addestrare un modello non è il primo passo: modello generale, controlli e «memoria» delle correzioni per fornitore;
un adattamento solo se la prova mostra errori ripetuti (ricerca, §4).

### Piano della prova

| Cosa | Scelta | Decisione |
|---|---|---|
| Dove stanno le bolle | Cartella «bolle» del repository privato `prova-visiva-foto`; nel pubblico solo script e numeri, con sigle F01, B001…; tabella delle sigle nel privato; tenute dopo la prova, cancellate su richiesta di UFP | 202 (eccezione alla 130) |
| Cosa si copre | Nomi e riferimenti dei clienti finali, firme, targhe, con un rettangolo pieno nell'immagine; del PDF si tiene l'immagine; le zone coperte non si misurano | 203 |
| Quante | 100–120 bolle scelte a caso: 8–12 fornitori ricorrenti (circa 8 bolle ciascuno) più 20–30 bolle di occasionali; due foto per bolla («bene» e «come capita»), tutte le pagine; PDF quando c'è; 5–10 lettere di vettura; bolle d'archivio con segni a penna in un gruppo a parte; un terzo dei ricorrenti fuori dalla prima metà; primo giro di 20 | 204 |
| Sistemi | Passo comune: codici stampati (zxing-cpp). A PaddleOCR con regole; B PaddleOCR-VL-1.6; C Qwen3-VL-8B con schema JSON (e 4B per i tempi); D pdfplumber per i PDF con testo. Stesso abbinamento per tutti | 205 |
| Traguardi | Numero e data giusti in 95 bolle su 100 dalla foto «come capita»; righe: codice e quantità giusti in 95 su 100 e al massimo 1 errore senza avviso su 100. Solo il primo: lettura solo della testata. Righe buone solo per alcuni fornitori: si accende per fornitore | 206 |
| Dove si calcola | Nella sessione di Claude, come la prova visiva; si riportano tempi e memoria di ogni sistema | 143 (per analogia) |

**Verità scritta a mano**, guardando la bolla: testata (fornitore, numero com'è stampato, data, ordini citati, pagine);
per ogni riga tipo di riga, codice, EAN, descrizione, quantità, unità, ordine di UFP, conferma del fornitore, Saldo o
Acconto, pagina, «scritto o corretto a mano», «coperto da timbro»; se l'articolo era in un ordine aperto quel giorno.
Una seconda persona ricontrolla il 10% (proposta della ricerca).

**Cosa si misura**: testata per campo; righe (trovate, giuste, quantità giusta); errori senza avviso dopo i controlli;
righe non di merce scartate bene; pagine rimesse insieme; lettere di vettura riconosciute; quanto si legge dai soli
codici stampati. Tutto diviso per foto «bene», «come capita» e PDF, per fornitore visto o mai visto, per bolle con o
senza segni.

**Principio dell'utente** (nota alla 206): conta che il carico dei DDT in Ad Hoc diventi veloce; ciò che non si
automatizza ha una procedura guidata, senza passaggi ripetuti.

### Rimandato

- Dove gira la lettura (telefono o server) e il caso del magazzino Shopify con un solo PC fisso: secondo giro del
  ticket «Resi», nella stessa pagina (nota alla 205).
- Requisiti minimi del server in sede: nebbia della mappa, con i numeri della prova.

## Resi

Dal ticket «Resi», chiuso il 18/11/2026, e dal ticket «Resi del cliente nel magazzino Shopify», chiuso il 19/11/2026 (decisioni 321–343, sotto). Decisioni 207–226 (la 214 precisa la 208, la 223 precisa la 215). Fonti: ricerca
`docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 1.8), documentazione Shopify sui resi (link nel ticket),
due mail di reso e due di segnalazione mostrate dall'utente in chat (fatti annotati sotto, senza nomi). Domande nella
pagina privata https://claude.ai/artifact/KQtNpyrXjbywxnz1iGKnGY; schermate nel prototipo
`prototipi/percorso-schermate/index.html` (https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata).

### Come si lavora oggi in UFP

Fatti mostrati dall'utente il 18/11/2026:

- **Differenze tra bolla e merce contata** (mancanti o in più): l'ufficio scrive al fornitore con un modello fisso,
  con una tabella «codice / quantità indicata in DDT / quantità ricevuta / differenza / note» e la richiesta di mandare
  il mancante oppure emettere una nota di credito; allega la bolla fotografata, con le correzioni a penna.
- **Reso per eccedenza** (arrivati 32 pezzi invece di 3): accordo per telefono, mail dell'ufficio acquisti che conferma
  il reso dei pezzi in più; poi l'ufficio manda il DDT di restituzione in PDF (causale «Reso a fornitori», dicitura
  «reso per accredito», riferimento al DDT del fornitore, porto assegnato, corriere del fornitore); il fornitore
  risponde con il giorno del ritiro.
- In magazzino c'è già un'ubicazione «RESIF» per i resi ai fornitori (nota alla 217).

### Reso al fornitore

**Da dove nasce** (207). «Rendi al fornitore» del responsabile, da «Da controllare» (merce non prevista, 45; articolo
rifiutato, 114; merce danneggiata, 191; eccedenza, 32; pezzi rimasti dopo un annullamento, 37 e 41; reso di un cliente
non rivendibile, 211) o dalla scheda di un articolo per merce libera. I pezzi passano a **Da rendere**; se erano
assegnati, l'assegnazione si rifà e la conferma nomina gli ordini che li perdono (16, 190, deduzione). Nei magazzini con
le ubicazioni nasce il compito «Porta nell'area resi» (217).

**Stati** (214):

| Stato | Cosa vuol dire | Chi lo fa avanzare |
|---|---|---|
| Da chiedere | Merce da rendere raccolta per fornitore | Il responsabile prepara la richiesta |
| Chiesto | Richiesta partita, si aspetta la risposta | Il responsabile segna la risposta |
| Autorizzato | Il fornitore accetta; «la rimanda» o «non la rimanda» (208), numero di autorizzazione se c'è | Il magazziniere prepara |
| Pronto | Pezzi inquadrati uno per uno, colli contati (216) | Chi consegna: «Ritirato da …» o «Consegnato al fornitore» |
| Partito | La merce esce dalla giacenza; va il documento di reso (209) | — |

Se il fornitore rifiuta, la merce torna al responsabile: tenerla o scartarla (214). «La rimanda» riapre il residuo della
riga d'ordine fornitore e i pezzi tornano attesi; eccedenze e merce senza ordine non riaprono niente (208). Un pezzo in
VEND reso con «la rimanda» torna a quel cliente quando arriva, perché il residuo riaperto porta ancora il riferimento
(34, 226).

**Richiesta di reso** (215, 223). Il programma prepara la mail: destinatario dal fornitore, oggetto con il DDT, righe
con quantità e motivo, allegati con la foto della bolla, il PDF delle righe, le foto dei danni e la riserva al corriere
(219). Anteprima modificabile; «Invia» la manda solo il responsabile, dalla sua mail aziendale salvata nel suo utente
(campo facoltativo). Senza mail nell'utente: «Copia testo» e «Scarica allegati». Il programma non legge le risposte.
Punto tecnico aperto (deduzione): mandare a nome di ogni responsabile chiede al server di posta dell'azienda il permesso
di inviare da quell'indirizzo (per esempio un accesso per utente o un invio autorizzato «per conto di»); si sceglie con
lo stack e all'installazione.

**Segnalazione delle differenze** (223). Le differenze di un DDT (bolla, contato, ordine) stanno insieme in «Da
controllare» con «Scrivi al fornitore»: la stessa tabella di oggi (codice, quantità indicata in DDT, ricevuta,
differenza, note), la foto della bolla, la richiesta di mandare il mancante o di una nota di credito. Alla risposta,
per riga: «Manda il mancante» (residuo aperto, 33), «Nota di credito» (residuo chiuso), per i pezzi in più «Rendi»
(207) o «Teniamo» (32).

**Documento di reso** (209). Gestionale principale: il programma stampa il DDT di reso con la sua numerazione, causale
di reso e riferimento al DDT del fornitore. Accanto a un gestionale: il programma manda il documento di reso e il DDT
lo fa il gestionale; in UFP lo fa l'ufficio con Ad Hoc (225); resta da sapere come Ad Hoc riceve il documento già
pronto (domanda 24).

### Reso del cliente

Base di ogni magazzino (decisioni 210–212, 220):

- **Ricevi reso** (210): si parte dall'ordine spedito, cercato per numero, cliente o inquadrando un articolo; nel
  magazzino Shopify in cima ci sono i resi aperti sul sito. Il documento del cliente, se c'è, si fotografa. Un pacco
  senza ordine trovato, o un articolo non spedito con quell'ordine, va al responsabile come merce non prevista (45).
- **Per ogni pezzo** (211): «Integro» (torna libero, va in «Metti a posto», si assegna dal più vecchio), «Da
  controllare» (al responsabile: rivendibile, da rendere al fornitore o da scartare), «Danneggiato» (191). Più pezzi di
  quelli spediti: si accettano e il di più va al responsabile (deduzione, come la 198).
- **Accanto a un gestionale** (220): alla chiusura va al gestionale un «reso da cliente» con il riferimento all'ordine e
  alla vendita; nota di credito e rimborso li fa il gestionale (domanda 27 al rivenditore).

### Reso del cliente nel magazzino Shopify

Dal ticket «Resi del cliente nel magazzino Shopify», chiuso il 19/11/2026. Decisioni 321–343; ricerca
`docs/research/2026-11-19-shopify-resi-rimborsi-collegamenti.md`; domande nella pagina privata
https://claude.ai/artifact/AR5aJVmctJ7FbEzbwyjCQd.

**Oggi** (321, 326, 331, fatti riferiti): le scatole arrivano, si controllano le etichette, una persona si accorda con
il cliente per WhatsApp o per mail tra credito del negozio e rimborso sul metodo di pagamento. Con il credito il negozio
fa ritirare il pacco: in Italia, Austria e Germania una persona prenota il ritiro GLS scrivendo al referente; nel resto
del mondo un'etichetta FedEx. Con il rimborso il cliente spedisce a sue spese. Molti clienti chiedono il reso solo per
mail. Niente è registrato in digitale.

**Su cosa si costruisce** (322). Sui resi di Shopify, letti e scritti dal programma: è una parte del collegamento
Shopify, senza app di resi in più. Tutto il traffico parte dal server in sede, a intervalli (54).

**Cosa Shopify permette e cosa no** (ricerca del 19/11/2026, sintesi):

| Si fa dal programma | Non si fa |
|---|---|
| Leggere i resi aperti (dagli ordini con `return_status`), con pezzi, motivo, nota e tracking | Etichette di reso Shopify in Italia (solo Stati Uniti e Canada) |
| Creare, approvare, rifiutare un reso; caricare un'etichetta propria | Sapere se il pacco del reso è in viaggio; cercare un ordine per tracking |
| Scrivere l'esito per pezzo (212) | Far scegliere il rimborso con il solo modulo di Shopify |
| Eseguire il rimborso sul metodo originale, in credito del negozio o diviso, con la notifica di Shopify | Mandare mail libere al cliente «tramite Shopify» |
| Leggere una casella di posta e mandare mail | Ricevere le risposte WhatsApp sul server in sede; rimborsare contrassegno e bonifico |

**Da dove arriva un reso**

- **Dal sito** (323, 330, 338). È la strada principale: resi self-service di Shopify con i nuovi account cliente (già
  accesi: il negozio usa il credito del negozio; i resi self-service si verificano nel pannello). Un modulo nostro nella
  pagina dell'ordine, parte del collegamento Shopify, chiede pezzi, motivo e «Come vuoi il rimborso?»: credito del
  negozio (con il ritiro o l'etichetta del negozio) o metodo di pagamento originale (spedisce il cliente). Nessuna delle
  due è già scelta. Con il credito in Italia, Austria e Germania chiede anche l'indirizzo del ritiro, proposto da quello
  di spedizione, con un campo di note; le disponibilità no. Il modulo manda la richiesta a Shopify e salva la scelta
  sull'ordine con data e ora: è la prova dell'accordo espresso sul credito. Finché il modulo non è provato su un negozio
  di sviluppo, il cliente scrive la scelta nella nota della richiesta; se usa il pulsante normale di Shopify, la chiede
  la persona.
- **Dalle mail** (324, 325, 333, 334, 340). Un indirizzo dedicato sul dominio dell'azienda (resi@ o assistenza@, nome
  da scegliere), con una regola nella casella principale che vi inoltra le mail dei clienti che parlano di reso; il
  programma legge solo quello. Ogni conversazione va in «Da controllare» con tutte le mail. Un modello linguistico, che
  si accende in «Configurazione», prepara la bozza (ordine, pezzi, motivo, scelta del rimborso, indirizzo); finché non
  si decide dove lavora (dopo una prova su mail vere, ancora da definire), resta spento e il programma riconosce ordine e
  cliente con regole semplici (numero d'ordine, mittente). Una persona conferma, corregge o respinge; solo alla conferma
  il programma crea il reso su Shopify. Alle mail risponde sempre una persona. Per legge la mail è già una richiesta di
  recesso valida: la data di arrivo conta per i 14 giorni.

**Richieste da approvare** (331, 339). Il responsabile vede ogni richiesta con giorni, pezzi, motivo e scelta del
rimborso, e tocca «Approva» o «Rifiuta» (con il motivo, che parte con la notifica di Shopify). Dopo «Approva»:

| Scelta del cliente | Paese | Cosa succede |
|---|---|---|
| Credito del negozio | Italia, Austria, Germania | Il programma mostra il riepilogo per il ritiro (reso, pezzi, credito, indirizzo, note); chi prenota scrive al referente GLS e segna «Ritiro prenotato per il …» |
| Credito del negozio | Resto del mondo | Una persona crea l'etichetta FedEx sul sito del corriere e la carica (PDF e tracking); il programma la mette sul reso e Shopify la manda al cliente (326) |
| Metodo di pagamento originale | Ovunque | Shopify manda al cliente l'approvazione; il cliente spedisce a sue spese |

Il cliente si avvisa con le notifiche di Shopify e con le mail del programma, dall'indirizzo dei resi; per WhatsApp il
programma prepara il testo da copiare (329). Niente WhatsApp automatico.

**All'arrivo.** «Ricevi reso» come nella base (210, 211). La scatola si riconosce dal tracking dell'etichetta quando
c'è: il programma tiene un elenco dei tracking dei resi aperti, riletto a ogni giro, perché Shopify non cerca per
tracking (343, deduzione). Senza tracking (ritiro GLS, spedizione del cliente) si cerca l'ordine. Alla chiusura il
programma scrive su Shopify l'esito di ogni pezzo (212); l'esito «Da controllare» si scrive una volta sola, alla
decisione del responsabile (343). Tutti i resi si trattano come recesso; un pezzo difettoso si segna «Da controllare»
o «Danneggiato» e il responsabile può renderlo al fornitore (332, 207).

**Rimborso** (327, 335, 341). Il programma propone il metodo scelto dal cliente; l'importo lo scrive il responsabile,
in un campo vuoto, e tocca «Conferma rimborso»: il programma lo esegue su Shopify (sul metodo originale, in credito del
negozio o diviso) e lo registra nel reso. Contrassegno e bonifico si restituiscono fuori da Shopify e nel programma si
segnano soltanto. Shopify Payments rimborsa di solito fino a 120 giorni, PayPal fino a 180 (ricerca).

**I 14 giorni** (328). Su ogni reso «giorno N di 14», contati dalla richiesta (sito o mail); dal 10° giorno avviso al
responsabile. Per legge il rimborso del recesso va fatto entro 14 giorni da quando il negozio ne è informato; si può
aspettare la merce o la prova che è partita.

**Niente cambi** per ora (336): il cliente prende il credito e fa un nuovo ordine.

**Documenti** (337). Una scheda per reso in «Documenti» → «Resi»: la richiesta (dal sito, o tutta la conversazione delle
mail), la scelta del rimborso con data e ora, ritiro o spedizione con il tracking, le foto e il documento del cliente,
l'esito di ogni pezzo, il rimborso eseguito, chi ha approvato e chi ha confermato.

**Permessi dell'app Shopify** in più (226, 343, ricerca § 1.7 e § 4): `read_returns` e `write_returns`; `write_orders`
per i rimborsi; `read_store_credit_accounts` e `write_store_credit_account_transactions` per il credito del negozio;
metafield dell'ordine per la scelta del rimborso; estensione dell'account cliente per il modulo.

**Da provare su un negozio di sviluppo** prima di accendere resi e rimborsi (212, 343; elenco completo nella ricerca):
l'esito `RESTOCKED` alza il disponibile una volta sola e «Elabora reso» nel pannello non lo ripete; un pezzo «Da
controllare» accetta poi l'esito finale; creare o chiudere un reso aggiorna l'ordine per il giro a intervalli;
`returnProcess` con credito e con rimborso, e quali mail partono e in che lingua; il token dell'app basta per rimborsi
ed etichette; il modulo nell'account cliente si installa con la nostra app e salva la scelta; reso di un ordine senza
account.

**Punti aperti per la parte legale** (342). Il programma non cambia per questi punti:

- Garanzia legale di 2 anni: per il Codice del consumo la deve chi vende al consumatore, anche se rivenditore, che poi
  può rivalersi sul fornitore (ricerca § 2.3; la rivalsa è una deduzione). Oggi i difetti si mandano al fornitore (332).
- Funzione di recesso online, obbligatoria dal 19/6/2026 (art. 54-bis): i resi self-service di Shopify dovrebbero
  coprirla; se basti l'accesso con il codice mandato per mail è discusso.
- Ritiro gratuito solo per chi sceglie il credito: il costo diretto del ritorno si può lasciare al cliente se lo sa
  prima; il credito al posto del rimborso vale solo con il suo accordo espresso, che il modulo conserva (330).

### Danni al trasporto

All'apertura del DDT, o con «Danneggiata», l'operatore segna «Collo rovinato all'arrivo» con una foto e «firmato con
riserva» sì o no (219). Foto e riserva finiscono nella richiesta di reso e nei «Documenti» del DDT. Pallet e imballi a
rendere non si contano (218).

### Schermate

Lavoro «Resi» della mansione magazziniere, con il numero sulla prima schermata (213): scheda «Dai clienti» (cose in
sospeso, resi aperti sul sito, «Ricevi reso»); nel magazzino Shopify il responsabile ha in più «Richieste da approvare» (331) e in «Da controllare» i resi
arrivati per mail (324) e scheda «Al fornitore» (Da chiedere, Chiesto, Autorizzato, Pronto,
Partito). Per il responsabile: «Rendi al fornitore» in «Da controllare» e nella scheda dell'articolo, richiesta di reso
in anteprima, risposta del fornitore. In «Documenti» la categoria «Resi». In «Metti a posto» il compito «Porta
nell'area resi». Nel nuovo DDT «Collo rovinato all'arrivo».

### Requisito sul carico

Il carico di articoli e DDT dev'essere semplice, veloce e molto più funzionale di quello di oggi in UFP; quando mancano
codici o quantità, il carico a mano ha una procedura guidata senza passaggi ripetuti (222). Vale per tutto il
ricevimento, non solo per i resi. Primo passo: la scheda «Dalla bolla» e «Manca l'ordine» (224), nella sezione
«Percorso delle schermate» → «Ricevimento».

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Nome dell'area resi | testo | «RESI» | 217 |
| Invio delle mail ai fornitori | dalla mail aziendale del responsabile, solo testo da copiare | solo testo da copiare finché non si collega il server di posta | 215, 223 |
| Resi del cliente dal collegamento Shopify (resi, esiti, rimborsi) | acceso, spento | spento finché non si prova su un negozio di sviluppo | 322, 343 |
| Modulo della scelta del rimborso nella pagina dell'ordine | acceso, spento (la scelta va nella nota) | spento finché non è provato | 330 |
| Spedizione del reso per scelta e paese | per ogni coppia: ritiro prenotato a mano, etichetta caricata, spedisce il cliente | magazzino Shopify: credito → ritiro GLS (Italia, Austria, Germania), etichetta FedEx (resto del mondo); rimborso → spedisce il cliente | 326, 331 |
| Indirizzo dei resi letto dal programma | indirizzo e accesso autorizzato alla casella | nessuno | 324, 334 |
| Modello che prepara le bozze dalle mail | acceso (servizio scelto dall'admin), spento | spento finché non si decide dove lavora | 324, 333, 340 |
| Avviso sui 14 giorni | giorno dell'avviso | 10° giorno | 328 |

## Inventario periodico

Dal ticket «Inventario periodico», chiuso il 18/11/2026 in tre giri. Decisioni 227–245 (la 236 e la 237 precisano la
230 e la 231; la 238 e la 244 precisano la 77). Fonti: ricerca
`docs/research/2026-11-18-gestionali-magazzino-esistenti.md` (§ 1.7, Odoo e Business Central) e
`docs/research/2026-11-15-adhoc-revolution-ars-logistica.md` (rilevazioni d'inventario di ARS). Domande nella pagina
privata https://claude.ai/artifact/QGQvc1pHzoQTsJBATiM1g5; schermate nel prototipo
`prototipi/percorso-schermate/index.html` (https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata).

### Come si lavora oggi

- **UFP** (227): l'inventario di tutto il magazzino si fa una volta l'anno, su carta o foglio di calcolo, e i numeri si
  ricopiano a mano in Ad Hoc. ARS non si usa per l'inventario. Durante l'anno una giacenza sbagliata si corregge sul
  momento, quando si può.
- **Magazzino Shopify** (228): lo stesso, con le giacenze corrette a mano su Shopify.

### Due modi di contare

| | Conta un'ubicazione | Inventario |
|---|---|---|
| Chi la avvia | L'operatore, quando la merce non torna: «Conta un'ubicazione» in «Cerca e conta» (244), o «Conta» dalla scheda dell'articolo | Il responsabile (229) |
| Cosa si conta | Un'ubicazione | Tutto (solo le ubicazioni normali, 239), alcune ubicazioni, alcuni articoli (in tutte le loro ubicazioni), la merce di un fornitore; senza ubicazioni (26) per articolo |
| Come si conta | Con la schermata dell'inventario: cieca e con la seconda conta, secondo la Configurazione (238, 244); aperta dalla scheda, chi conta ha già visto la giacenza | Vedi sotto |
| Quando vale | Subito; il responsabile la controlla dopo (77, 238) | Quando il responsabile approva la differenza (232) |

**Tutto il magazzino** (239): solo le ubicazioni normali. Area di ricevimento, area resi, posti VEND e merce prelevata
in attesa del corriere non entrano in un inventario di tutto.

**Scegliere cosa contare** (241): il programma non propone conte da solo. Ogni ubicazione mostra la data dell'ultima
conta; nel nuovo inventario il responsabile può prendere le ubicazioni «non contate da più di … giorni» o «con
differenze negli ultimi … giorni».

### Come si conta

1. **Si prende un'ubicazione** (234). Il responsabile può dare gruppi di ubicazioni a persone; ogni ubicazione la conta
   una persona sola: chi la apre la prende e gli altri la vedono **in conta da…**; chi finisce prende le libere.
2. **Conta cieca** (230): si inquadra ogni articolo trovato (stesso percorso di identificazione del ricevimento) e si
   scrive quanti pezzi; la quantità attesa non si vede. Il numero si scrive sempre (186).
3. **Seconda conta** (231): se il numero non torna con la giacenza, il programma chiede subito alla stessa persona di
   ricontare quell'articolo, senza dire l'atteso né il verso della differenza. Due numeri uguali: la differenza va al
   responsabile; diversi: vale il secondo.
4. **Articoli attesi non contati** (230): finita l'ubicazione, il programma chiede di ognuno «ce n'è?»: «Nessuno» vale
   come conta di zero (con la sua seconda conta), «Lo conto» riapre la conta.
5. **Chiusura dell'ubicazione** (233): il numero si confronta con la giacenza di quel momento; i movimenti successivi
   non creano differenze finte. Le conte che tornano segnano solo l'ubicazione come contata.

### Il lavoro continua

Durante un inventario si riceve, si mette a posto e si preleva (233). Chi deve prelevare o mettere a posto in
un'ubicazione in conta lo vede («C-02-4 in conta da Marco, da 3 minuti») e prende da un'altra ubicazione o aspetta.
Fermare il magazzino per l'inventario di fine anno resta una scelta di chi lo organizza, non del programma.

### Approvazione e documenti

- **Differenze d'inventario** (232): stanno nell'inventario e in «Da controllare». Il responsabile le approva una per
  una o tutte insieme; il riepilogo (190) dice le rettifiche e nomina gli ordini che perdono merce, perché
  l'assegnazione si rifà dal più vecchio (16). In alternativa chiede una nuova conta a un collega (231).
- **Cosa parte** (235): a ogni approvazione una rettifica per articolo al gestionale, o una variazione di quantità a
  Shopify (52, 61). In «Documenti» la categoria «Inventari» raccoglie conte, differenze, chi ha contato e chi ha
  approvato; si esporta (189, 199) con le sole quantità: articolo, ubicazione, contato, differenza. Il valore lo
  calcola il gestionale o chi fa il bilancio (242). Come Ad Hoc vuole ricevere l'inventario: domanda 28 per il
  rivenditore.
- **Chiusura** (240): le ubicazioni non contate restano come sono, senza rettifiche; il riepilogo le elenca e con un
  tocco diventano un nuovo inventario. Le differenze non ancora approvate restano in «Da controllare».

### Schermate

Confermate sul prototipo (243). Lavoro «Inventario» della mansione magazziniere, con il numero sulla prima schermata
(le ubicazioni che toccano a chi ha fatto l'accesso; per il responsabile le differenze da approvare). In cima le
ubicazioni in conta (le mie, di colleghi, 187); per ogni inventario aperto: le tue, libere, di colleghi, contate. Conta
di un'ubicazione con inquadratura, numero da scrivere, seconda conta, domanda sugli attesi non contati, «Ho finito
questa ubicazione» e «Lascia: torna libera». Il responsabile: «Nuovo inventario» (cosa contare, entro quando, a chi,
quantità attesa e seconda conta per quell'inventario), «Differenze da approvare» con il riepilogo, «Chiedi una nuova
conta», «Chiudi l'inventario». Al prelievo e alla messa a posto: «in conta da…» con un'altra ubicazione proposta. In
«Documenti» la categoria «Inventari».

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Quantità attesa a chi conta | nascosta, visibile; si cambia anche per un singolo inventario | nascosta | 230, 236 |
| Seconda conta se il numero non torna | accesa (la stessa persona, subito), spenta; si cambia anche per un singolo inventario | accesa | 231, 236, 237 |

### Casi limite

Deduzioni confermate con la chiusura (245):

- **Aree**: area di ricevimento, area resi e posti VEND, fuori da «tutto» (239), si contano scegliendole come
  ubicazioni in un inventario o con «Conta un'ubicazione».
- **Senza ubicazioni** (26): l'inventario è per articolo; «in conta da…» vale per l'articolo; stesse regole.
- **Merce fuori posto**: un articolo trovato dove non risulta si conta e dà una differenza in più in quell'ubicazione
  (di solito compensata da una in meno altrove); un articolo sconosciuto si inserisce come articolo nuovo «da
  confermare» (105).
- **Il responsabile che conta** conta cieco come gli altri; l'atteso lo vede nelle differenze.
- **Chiusura con qualcuno che conta**: il riepilogo nomina ubicazione e persona; si chiude lo stesso e quell'ubicazione
  passa con le non contate (240).
- **Permessi**: creare, approvare e chiudere spetta al responsabile (27); contano i magazzinieri e chi ha il lavoro tra
  gli «Altri lavori» (177).
- **Lasciata a metà**: «Lascia» rimette l'ubicazione tra le libere e la conta riparte da capo; un'ubicazione in conta da
  oltre 2 giorni va tra i vecchi delle cose in sospeso (187).
- **Tempi** (195): valgono anche qui; la prova di carico prima della consegna comprende un inventario con più telefoni.

### Rimandato

- Come Ad Hoc riceve l'inventario (rettifiche o rilevazione unica) e se ne calcola il valore: domanda 28 per il
  rivenditore; il collegamento sceglie una delle due forme (312), sezione «Punti di estensione».
- Colori e stile delle schermate: ticket «Aspetto grafico».

## Punti di estensione

Dal ticket «Punti di estensione per la specializzazione», chiuso il 19/11/2026. Decisioni 301–320; raccoglie anche i
punti lasciati alla specializzazione dalle decisioni 178, 192, 226 e dalle domande 24, 27 e 28 per il rivenditore.
Nelle sezioni precedenti «connettore» vuol dire «collegamento» (316).

### Base, configurazione e moduli

- Il codice della base è uno solo, uguale in ogni magazzino. Una specializzazione è fatta di scelte in «Configurazione»
  e di moduli che si agganciano a punti d'aggancio previsti; mai una copia modificata della base. Un bisogno che la
  base non prevede diventa un punto d'aggancio nuovo, utile a tutti (301).
- I moduli per ora li scriviamo solo noi: quelli consegnati con la base (scambio a file, Shopify) e quelli delle
  specializzazioni (Ad Hoc Revolution per UFP). Arrivano con gli aggiornamenti, già provati con quella versione; l'admin
  li accende e spegne in «Configurazione» → «Collegamenti» (302, 316). Le regole dei punti d'aggancio si scrivono in
  modo che si possano aprire ad altri più avanti.
- Cosa si fa senza programmare, in «Configurazione»: tutte le scelte per magazzino delle sezioni precedenti, più parole
  di quantità (304), campi aggiuntivi (306), logo, intestazione e piè di pagina dei documenti (313), nomi previsti
  (315), uscita della vendita assistita (317), confronto con la fattura (310), testo della mail dell'ordine fornitore
  (318). Gli altri testi dell'interfaccia sono uguali in ogni magazzino (315).

### Punti d'aggancio

| Punto d'aggancio | Cosa fa il modulo | Cosa resta alla base | Moduli previsti | Decisioni |
|---|---|---|---|---|
| Collegamento | Legge dal gestionale o dal negozio online articoli, fornitori, clienti, ordini, prezzi, campi aggiuntivi, chiusura degli ordini, fatture del fornitore; manda i documenti dei fatti di magazzino | Coda d'uscita, scambio a intervalli, codici del sistema d'origine, avvisi, «Da registrare nel gestionale» | Scambio a file (di serie), Shopify (con la base, spento), Ad Hoc Revolution (UFP) | 49–67, 303, 310, 312, 317 |
| Lettore di etichette | Legge codice e quantità da un formato di etichetta con regole proprie, per un fornitore | Barcode, GS1, parole di quantità, conversioni approvate (72, 93) | Nessuno: si scrive su etichette vere quando serve | 304 |
| Precedenza dell'assegnazione | Decide l'ordine in cui gli ordini ricevono la merce | Mai sotto zero, assegnazione in parte, VEND che vince (16, 37) | Nessuno: di serie «dal più vecchio» | 305 |
| Partita | Chiede lotto, scadenza o seriale al ricevimento, li mostra al prelievo, sceglie da quale partita prendere | Il posto per la partita su giacenze e movimenti (17) | Nessuno: UFP e il magazzino Shopify non ne hanno bisogno | 314 |

Un campo aggiuntivo si vede nella scheda e si cerca, ma non cambia le regole: per quello serve un modulo (306). Un
modello di documento con un'altra disposizione non è un punto d'aggancio (313).

### Il collegamento

Ogni collegamento dichiara cosa legge e quali documenti sa mandare (303). I documenti della base, uno per fatto di
magazzino, appena il fatto si chiude (61):

| Documento | Quando nasce | Decisioni |
|---|---|---|
| Carico | DDT ricevuto | 61 |
| Prelievo, spedizione | Ordine prelevato, spedito | 61 |
| Rettifica | Correzione approvata; differenza d'inventario approvata | 61, 235 |
| Rilevazione d'inventario | Chiusura di un inventario, se il collegamento la preferisce alle rettifiche (mai tutte e due) | 312 |
| Documento di reso al fornitore | Reso pronto a partire; il DDT di reso lo fa il gestionale | 209, 225 |
| Reso da cliente | Chiusura di un reso del cliente; nota di credito e rimborso li fa il gestionale | 220 |
| Ordine della vendita assistita | «Conferma: crea l'ordine nel gestionale» | 65, 178 |

Un documento che il collegamento non sa mandare va in «Documenti» → «Da registrare nel gestionale», con PDF e file e un
avviso al responsabile di magazzino; chi lo ricopia nel gestionale tocca «Registrato». Il lavoro in magazzino non si
ferma (303). Con il collegamento Ad Hoc vale per il documento di reso e il «reso da cliente» finché il rivenditore non
risponde alle domande 24 e 27.

Cosa può leggere in più, se il gestionale lo permette:

- **Chiusura dell'ordine** (ricevuta, DDT o fattura emessi nel gestionale): serve all'uscita della vendita assistita
  (317).
- **Fatture del fornitore**: il programma le confronta con i DDT caricati e mette le differenze in «Da controllare», nel
  DDT, insieme a quelle con la bolla, con «Scrivi al fornitore» (223). Facoltativo, si accende in «Configurazione», solo
  con un collegamento che legge le fatture (310). Senza gestionale per ora non c'è.

### Con Ad Hoc in UFP

- **Ordini degli agenti** (178, 309): arrivano come gli altri ordini cliente, con il nome dell'agente (domanda 21); il
  responsabile dei piani li vede in «Ordini da assegnare», con l'agente su ogni riga e un filtro «Agente», e il titolo
  del piano si propone dall'agente.
- **Inventario** (312): finché il rivenditore non risponde alla domanda 28, Ad Hoc riceve le rettifiche.
- **Chi stampa cosa** (319): bolle, fatture, ricevute, ordini fornitore e DDT di reso li fa Ad Hoc, come oggi. Il
  programma stampa solo i suoi documenti: richiesta di reso, segnalazione delle differenze al fornitore, PDF «Da
  registrare nel gestionale». Dove il programma è il gestionale (magazzino Shopify) stampa anche ordini fornitore e DDT
  di reso.

**Vendita assistita** (178, 308, 317). Alla conferma la merce è prelevata per quell'ordine e non è più disponibile per
altri, anche se il pacco resta sul pancale dell'agente. L'ordine torna dal gestionale al primo scambio, collegato dal
nostro riferimento. In «Configurazione» → «Vendita assistita» l'admin sceglie quando la merce esce:

| Scelta | Quando c'è | Di serie |
|---|---|---|
| Quando il gestionale chiude l'ordine | Solo se il collegamento legge la chiusura | Con un gestionale accanto |
| Alla conferma | Sempre | Senza gestionale, o se il collegamento non legge la chiusura |

Finché la merce non esce, un pacco da spedire compare a chi fa i piani tra gli ordini già prelevati. In UFP il momento
candidato è il passaggio da OP a bolla al ritiro: prima di impostarlo si verifica con il rivenditore se il collegamento
lo vede e quando Ad Hoc scarica la giacenza (domanda 29).

### Ordini fornitore dal programma

Gli ordini fornitore che nascono nel programma (magazzino Shopify, proposte con il riferimento cliente) partono con
«Invia al fornitore», come le richieste di reso: anteprima con il testo della mail e il PDF allegato, dalla mail
aziendale del responsabile, con copia a lui (311, 223). Il testo parte da un testo di serie che l'admin scrive in
«Configurazione», con numero d'ordine e fornitore messi dal programma, e si corregge nell'anteprima (318). Senza server
di posta collegato restano «Copia testo» e «Scarica PDF» (215). La mail resta nei «Documenti» dell'ordine. Precisa la
64.

### Aggiornamenti senza rompere

- Ogni modulo dichiara con quale versione delle regole dei punti d'aggancio funziona (307).
- La base tiene valide le regole vecchie per almeno un anno dopo averle cambiate; ogni specializzazione nota si prova
  prima di pubblicare un aggiornamento.
- Prima di installare, il server controlla i moduli accesi. Se uno non va con la versione nuova, l'aggiornamento non
  parte, neanche quello obbligatorio di notte (125): il programma resta com'è e l'admin vede l'avviso, mandato anche a
  noi.

### Configurazione per magazzino (aggiunte)

| Scelta | Valori | Di serie | Decisione |
|---|---|---|---|
| Collegamenti | moduli accesi, spenti | Shopify spento (51); gli altri da scegliere alla configurazione | 302, 316 |
| Parole di quantità in più | elenco di parole | nessuna | 304 |
| Lettori di etichette | per fornitore, accesi, spenti | nessuno | 304 |
| Campi aggiuntivi | nome, tipo (testo, numero, data, sì/no, scelta da elenco), dove (articolo, ordine, cliente, fornitore) | nessuno | 306 |
| Documenti | logo, intestazione, piè di pagina | vuoti | 313 |
| Uscita della vendita assistita | alla conferma, quando il gestionale chiude l'ordine | vedi «Con Ad Hoc in UFP» | 317 |
| Confronto con la fattura | acceso, spento | spento | 310 |
| Testo della mail dell'ordine fornitore | testo | da scrivere alla configurazione | 318 |

### Rimandato

- Quando Ad Hoc scarica la giacenza e se il collegamento vede il passaggio da OP a bolla: domanda 29 per il
  rivenditore. Come Ad Hoc riceve documento di reso, «reso da cliente» e inventario, e se legge le fatture: domande 24,
  26, 27 e 28.
- Etichette e distinta del corriere: nebbia della mappa; se serviranno, diventano un collegamento in più.
- Come si scrivono i moduli (linguaggio, forma delle regole dei punti d'aggancio): ticket «Stack».

## Nome del prodotto

Ticket «Nome del prodotto» (decisione 20). Il prodotto non si chiamerà DondEres. Qui stanno i criteri e la rosa; la
verifica di marchi e domini è nel ticket «Unicità dei nomi scelti», il logo nel ticket del brand kit.

### Criteri (decisioni 344–351)

- Marchio vero, offerto anche ad altri magazzini: unico e registrabile (344).
- Si legge allo stesso modo in italiano e in inglese (345). Si evitano quindi le lettere che le due lingue leggono in
  modo diverso: «ce/ci», «ge/gi», «gn», «gli», «sc», «ch», «z», «h» iniziale, la «e» finale muta dell'inglese, gli
  accenti (deduzione).
- Fa venire in mente velocità e ordine (346).
- Parola vera modificata o composta (347), corta: una o due sillabe, fino a 5 lettere (348).
- Il dominio non decide il nome; nella verifica si controlla comunque che non sia già preso (349).
- Niente parole da startup né doppi sensi in italiano o nei dialetti; K, J, W, X, Y ammesse (350).
- «Kiln» resta un riferimento di stile per il brand kit, non per il nome (351).

### Rosa del secondo giro (decisioni 352 e 353)

Tenuti: Vekto, Kardo, Rivo, Dokra. In dubbio: Trako, Sorto, Rigo, Movo. Scartati: Pista, Ritmo, Dardo, Prelo, Snel,
Lampa, Vola, Ordo, Brio, Corso, Pronto. Deduzione, non detta dall'utente: sono state scartate tutte le parole vere
intere; restano nomi di due sillabe che finiscono in «-o» o «-a», spesso con il suono «k».

### Terzo giro e preferiti (decisioni 354–357)

Nomi nuovi, vicini a quelli tenuti: tenuti Velko e Kurso; in dubbio Varko, Venko, Arvo, Volko; scartato Karto (355).

| Ordine | Nome | Da dove viene | Si legge | Da controllare |
|---|---|---|---|---|
| 1 | Kurso | «corsa», «percorso»; in esperanto «corso, rotta» | «kùr-so» | In inglese può diventare «kèr-so» (345): prova a voce |
| 2 | Varko | il «varco» da cui passa la merce | «vàr-ko» | Può essere un cognome |
| 3 | Velko | «veloce», con il suono «k» | «vèl-ko» | Nei paesi slavi è un nome di persona |

I tre preferiti vanno alla verifica (356). Se nessuno è libero si riprende, nell'ordine, da Trako, Sorto, Rigo, Movo e
poi da Venko, Arvo, Volko (i nomi in dubbio del secondo giro e i nuovi segnati «Forse»), e il nome si
propone all'utente prima di sceglierlo (354). Il punto aperto su Vekto, Kardo, Rivo e Dokra (se entrano nella riserva) è chiuso
dalla verifica: hanno tutti un ostacolo forte (361).

Il nome definitivo lo sceglie l'utente dopo la verifica (357); con quel nome parte il brand kit, con Kiln come
riferimento di stile (351). Pagina delle domande, privata: https://claude.ai/artifact/7iL3QXfdar2NsqsjQSu9EC; copia nel
repository in `prototipi/nome-prodotto/index.html` (mostra l'ultimo giro).

### Verifica e nome scelto (decisioni 358–361)

Ticket «Unicità dei nomi scelti». Ricerca del 20/11/2026 in `docs/research/2026-11-20-unicita-nomi-prodotto.md`: marchi
in TMview (copia di EUIPO, UIBM e WIPO Madrid; i siti di EUIPO e UIBM non rispondevano), WIPO Global Brand Database e
registro tedesco, nelle classi 9, 35, 39 e 42; domini; prodotti con lo stesso nome. È preliminare, non un parere legale.

| Nome | Giudizio (deduzione) | Cosa pesa di più |
|---|---|---|
| Kurso | ostacolo forte | KURSO in Germania, software e SaaS, in uso (kurso.de) |
| **Varko** | ostacoli da valutare, i più bassi | nessun identico nel settore; omofoni «Varco» in altri settori e due domande italiane 2026 in classe 42 da leggere |
| Velko | ostacoli da valutare, vicini a forte | omofono Velco, software per flotte in Francia |
| Volko | sembra libero | solo WOLCO, servizi lontani |
| Trako, Sorto | ostacoli da valutare | TRAKO per fiere (35); Forto, logistica digitale |
| Rigo, Movo, Venko, Arvo, Vekto, Kardo, Rivo, Dokra | ostacolo forte | marchi identici nelle classi del prodotto |

Nessun `.com` è libero per nessun nome.

- **Nome: Varko** (358), il «varco» da cui passa la merce; si legge «vàr-ko» in italiano e in inglese.
- **Consulente in marchi** prima del deposito e prima di offrire il programma ad altri magazzini, con attenzione ai
  marchi «Varco»; intanto il nome si usa nel progetto e il brand kit parte, sapendo che un parere negativo li fa
  rifare (359).
- **Domini:** nessuna azione ora; varko.com, .it, .eu, .io, .app sono presi (360).
- Il brand kit parte con Varko, con Kiln come riferimento di stile (351). Nel codice e nei documenti già scritti il
  nome provvisorio DondEres resta finché non si decide come e quando cambiarlo (deduzione: è un cambio di testi, non di
  struttura).

Pagina delle domande, privata: https://claude.ai/artifact/QWapLTTybQqGXbrajL7ErH; copia nel repository in
`prototipi/unicita-nomi/index.html`.

## Brand kit

Ticket «Brand kit con la skill logo-design» (decisioni 20, 351, 358, 359). Il logo si fa con la skill logo-design di
kaankiziltug, nel suo percorso: brief, tre concetti, punto di controllo con l'utente, kit sulla strada scelta. Se il
consulente in marchi dà parere negativo su Varko, nome e logo si rifanno (359).

### Skill nel progetto (decisione 362)

- In `.claude/skills/logo-design` e `.agents/skills/logo-design`, uguali; versione del 13/11/2026 (commit `e9eaddc`),
  licenza MIT. Mai a livello globale.
- Senza `assets/library/svg/` (1.432 loghi di altre aziende, marchi dei loro proprietari, circa 12 MB). Restano le
  schede `catalog.json`, quindi la ricerca per categoria funziona; per vedere i loghi o fare il confronto «a scaffale»
  si scarica la stessa versione in una cartella temporanea della sessione:
  `git clone https://github.com/kaankiziltug/logo-design-skill` e `git checkout e9eaddc`, poi si passano i file a
  `preview_sheet.py --refs`.
- Gli script sono Python senza dipendenze e non usano la rete; per le immagini usano il Chromium già presente.

### Brief (decisioni 363–368)

| Voce | Scelta |
|---|---|
| Nome | **Varko**, iniziale maiuscola (365); il «varco» da cui passa la merce (358) |
| Carattere | veloce e ordinato (346), solido e preciso (363) |
| Lettere | geometriche e piene, come Kiln: cerchi e rette, una lettera con un dettaglio proprio (364) |
| Concetti | tre, di tre tipi: lettera V, nome scritto, simbolo con il nome (366) |
| Colore | bianco e nero fino al kit; poi lontano da rosso, verde e giallo, che nel programma dicono errore, fatto e attenzione (367) |
| Deve reggere | icona sul telefono e sui palmari, scheda del browser a 16 punti, testata delle schermate su telefono e computer, stampe in bianco e nero anche termiche (368) |
| Chi decide | l'utente |

Ricerca sulla categoria (deduzione, dalla raccolta della skill e dal settore): nei programmi di logistica e magazzino
ricorrono cubi e scatole in prospettiva, frecce, camion, codici a barre, spunte e i colori blu e arancione; si
evitano. La raccolta della skill non ha una categoria «logistica»: le più vicine sono commercio e trasporti.

### Concetti del giro 2

File in `prototipi/brand-kit/concetti/`: SVG fatti solo di forme piene (niente testo vivo), generati da `genera.py`
(lettere costruite a mano: linea di base 200, altezza della x 96, maiuscola 144, asta 30 su un'altezza di 256);
`concetti.png` è il foglio del punto di controllo. Tutti e sei i file passano `svg_audit.py` senza avvisi (100/100,
punteggio della skill); provati con `preview_sheet.py` a 16–256 punti, a un colore, in negativo, sfocati, specchiati e
accanto a Tidal, Vue, Dropbox, Kotlin e Vercel.

| | Concetto | Idea | Rischio visto nelle prove |
|---|---|---|---|
| A | Varco (consigliato) | la V non si chiude: in fondo resta il varco; la stessa V apre il nome | a 16 punti il varco sparisce; il vuoto può sembrare una Y |
| B | Mirino | il nome scritto, con la o fatta a mirino della telecamera | la o da sola sembra un salvagente, una croce o un bersaglio |
| C | Colli | due colli lasciano un varco largo un collo, il terzo ci passa sotto: insieme fanno la V | in grande sembra una faccina; struttura vicina a Tidal |

Pagina delle domande, privata: https://claude.ai/artifact/JQ2vwNwRMfT2qi4BDWNnX5; copia in
`prototipi/brand-kit/index.html` (mostra l'ultimo giro). Il primo giro è nella cronologia del repository.

### Esito del giro 2 (decisioni 369 e 370)

Nessuno dei tre concetti va al kit: si rivedono (369), motivo non indicato. Nel nome la «o» resta tonda (370). Prima di
disegnare tre concetti nuovi si chiede all'utente cosa non andava (idee, peso, lettere, semplicità, somiglianze, bisogno
del simbolo) e gli si fanno giudicare nove idee abbozzate: corsia, cartello di corsia, porta di carico, ripiani a V,
ingresso, spunta, monogramma Vk, V a filo, solo il nome. I tre concetti nuovi si scelgono dai «sì», poi dai «forse».

Risposte (decisioni 371–373): non andavano le idee e le lettere del nome; sì al cartello di corsia; forse a corsia,
porta di carico, ingresso e solo il nome; no a ripiani a V, monogramma Vk e V a filo; all'utente piace molto la K di
Kiln (deduzione: piace il modo, una lettera che porta l'idea e torna nel nome, non l'arco in sé, che resta di Kiln).

### Concetti del giro 3

File in `prototipi/brand-kit/concetti-2/`, generati da `genera.py` (lettere a spessore variabile: medio 22, leggero
16, sull'altezza della x di 96; V a 75 gradi; k con braccio e gamba a 45 gradi; «o» tonda, 370); `concetti.png` è il
foglio del punto di controllo; `dati_pagina.py` mette i tracciati nella pagina. Tutti i file passano `svg_audit.py`
senza avvisi. Scelte mie, da far confermare: ingresso escluso perché è anch'esso una V in un quadrato, come il cartello;
«solo il nome» è dentro tutti e tre.

| | Concetto | Idea | Rischio |
|---|---|---|---|
| A | Cartello di corsia (consigliato: l'unico «sì») | targa quadrata arrotondata con la V ritagliata e due fori per appenderla | lettera in un quadrato è comune tra le icone delle app; i fori spariscono a 16 punti |
| B | Corsia | la V a ripiani, uguale nel simbolo e nel nome | nel nome può sembrare stencil; a 16 punti resta una V piena |
| C | Porta di carico | il portone con la serranda alzata a metà | il più letterale: garage, o il carattere cinese per «porta» |

Un primo foro al centro della targa, sopra la V, sembrava un puntino sulla lettera, cioè il concetto «İ puntata» di
Kiln: l'ho spostato in due fori agli angoli.

### Giro 4: prima la lettera (decisioni 374 e 375)

Nessuno dei tre concetti del giro 3 va al kit; per le lettere del nome è preferito il peso medio (374). L'utente non
ama la V come logo e chiede di invertire l'ordine: prima una lettera bella da modificare, poi il logo, poi il nome a
partire dalla lettera (375). Nel giro 4 si chiede cosa succede a Varko (accantonato o tenuto, con le stesse regole del
nome o con regole riviste), si giudicano otto lettere abbozzate (K, R, S, M, A, Q, G, X, in `prototipi/brand-kit/lettere/`),
e si sceglie maiuscola o minuscola e se il nome comincia con la lettera. Conseguenza da tenere sulla mappa
(deduzione): con un nome nuovo serve una nuova verifica dei marchi, come per Varko (ticket «Unicità dei nomi scelti»), e
il consulente della 359 vale per il nome nuovo.

### Giro 5: concetti su R e Q (decisioni 376–379)

Varko si accantona e resta in riserva; il nome nuovo nasce dalla lettera, comincia con lei e segue le regole 344–350,
con una nuova verifica dei marchi e il consulente della 359 (376, 379). Lettere: sì a R e Q (377); maiuscole, perché
r e q minuscole hanno poco da modificare (378, scelta mia da confermare). File in `prototipi/brand-kit/concetti-3/`
(asta 44 su 256), tutti 100/100 in `svg_audit.py`; confronto a scaffale con Riot, Remix, Heroku Redis, Rollup, Qlik e
Quobyte: nessuna somiglianza forte.

| | Concetto | Idea | Rischio |
|---|---|---|---|
| A | R · Rampa (consigliato) | la gamba è un cuneo a 45 gradi, la rampa della baia di carico | gamba grande, la R pesa a destra; altre R a cuneo esistono |
| B | Q · Collo | la coda è un collo quadrato appoggiato all'anello | nomi quasi solo in «Qu» |
| C | Q · Nastro | rotolo di nastro da imballo, la coda si srotola con il taglio a dentini | a 16 punti i dentini spariscono; stesso limite sui nomi |

Ordine dei passi dopo la scelta: rosa di nomi che cominciano con la lettera, verifica dei marchi del nome scelto, kit.

### Giro 6: il nome in R (decisioni 380 e 381)

Logo: R · Rampa (380). Nome: dieci proposte che cominciano con la R, con le regole 344–350 (381): Rampo, Ramko (da
«rampa», legate al logo), Reko, Rulo, Rasto, Ripo, Rodo, Ranko, Roto, Rapo. Escluse prima di proporle (deduzioni da
fatti noti, non da una ricerca): Rako (marchio di piastrelle), Rolo (caramelle), Rekto (doppio senso di «retto»); Rivo
e Rigo hanno un marchio identico (361). Dopo i preferiti in ordine si fa la verifica dei marchi, come per Varko.

### Giro 7: verifica dei preferiti (decisioni 382 e 383)

Preferiti in ordine: 1. Reko, 2. Ripo, 3. Rodo (383); l'unico «sì» è Ripo (382). Ricerca in
`docs/research/2026-11-20-unicita-nomi-in-r.md`, **incompleta**: domini, App Store, GitHub e ricerca web sì; registri dei
marchi no (TMview blocca i programmi automatici e in questa sessione non è stato usato il browser automatico; EUIPO
eSearch non risponde). Giudizio provvisorio (deduzione): Reko ostacoli da valutare (REKO internazionale in classe 42,
app di trasporti), Ripo nessun ostacolo trovato finora, Rodo ostacoli da valutare (casa di moda italiana; «RODO» è il
GDPR in Polonia). Tutti i domini sono presi. Nel giro 7 l'utente sceglie come completare i registri e se il kit aspetta.

### Nome e kit (decisioni 384–387)

TMview non si carica dal browser automatico (384) e il blocco non si aggira (385). L'utente riporta i risultati UIBM
(sezione «Aggiornamento» della ricerca sui nomi in R, non controllati da noi) e sceglie per ora **Ripo** (386): se
cambia, il logo resta, perché l'iniziale è la R. La ricerca europea per somiglianza va al consulente (387).

Kit, giro 8: file in `prototipi/brand-kit/kit/`, generati da `genera.py`. La R del simbolo e quella del nome escono
dalla stessa funzione (occhiello alto due terzi, tratto dritto 1,33 raggi, gamba a cuneo a 45 gradi); il nome «Ripo» ha
le minuscole a peso medio (asta 22, 374) e la R un po' più spessa. Domande del giro: colore (indaco, prugna, petrolio,
blu elettrico, tutti con contrasto almeno 5,2 a 1 sul bianco), R a rampa o normale nel nome, puntino della i tondo o
quadrato, simbolo e nome separati o anche affiancati. Dopo le risposte: file finali (nero, bianco, a colori, icone,
favicon, manifest), tavola d'uso e guida di una pagina.

### Giro 9: la R più curva (decisioni 388–392)

Scelte del giro 8: blu elettrico #1F5BFF (388, contrasto 5,25 con il bianco; serve una variante chiara per il tema
scuro), puntino tondo (390), simbolo e nome separati (391). La R va ridisegnata più curva, dallo schizzo dell'utente
(389, `prototipi/brand-kit/concetti-4/schizzo-utente.jpg`, salvato senza i dati della foto); l'utente chiede anche idee
più ardite (392). File in `prototipi/brand-kit/concetti-4/`, generati da `genera.py` (ogni R è una funzione di altezza
e asta, usata per il simbolo e per il nome; le minuscole sono quelle del kit a peso medio). Tutti tra 99 e 100 in
`svg_audit.py`.

| | Concetto | Idea | Rischio |
|---|---|---|---|
| A | Il tuo schizzo · Gancio | la gamba scende e risale a U, staccata dall'asta | nel nome può leggersi «Ru»; a 16 punti la U si chiude |
| B | Ri (consigliato) | la U risale e diventa la i del nome, con il puntino: il simbolo dice «Ri» | lettura «Rj»; il più delicato in piccolo |
| C | Stencil | la R di A in tre pezzi, come le scritte a mascherina sulle casse | stencil comune nei marchi industriali |
| D | Scivolo | la rampa del giro 5 diventa curva, come lo scivolo a rulli | il più sobrio; coda sottile da ingrossare per le stampe termiche |

Un concetto «Muletto» (gamba con le forche) è stato scartato prima di mostrarlo: si leggeva «PL».

### Giro 10: vuoto tondo e gamba lunga (decisione 393)

Nessuna R del giro 9; lo schizzo non è più il riferimento; restano la gamba allungata e curva e il vuoto non
rettangolare (393). File in `prototipi/brand-kit/concetti-5/`: occhiello con un tratto dritto corto e un semicerchio
(il vuoto è quasi un semicerchio); tre gambe: **A · Arco** (arco pieno fino alla base), **B · Arco lungo** (lo stesso
arco steso in avanti, consigliato per la velocità della 346), **C · Scivolo** (concava, si assottiglia). Scartato prima di
mostrarlo un «Nastro» (gamba che corre lungo la base): si leggeva «RL». Rischio comune: la gamba ad arco è lo stesso
gesto della K di Kiln, va tenuta diversa nei dettagli.

### Giro 11: Arco lungo, tre versioni (decisione 394)

Scelta la R · Arco lungo (394); prima del kit tre versioni migliorate, in `prototipi/brand-kit/concetti-6/`
(`genera.py`). La gamba ora è un tratto lungo una curva di Bézier, con il contorno spostato lungo la normale e
ridisegnato con curve morbide: nel giro 10 era la differenza tra due ellissi e ingrossava a metà. Versioni: **A ·
Pulito** (spessore uguale, piede diritto; consigliata), **B · Affusolato** (si assottiglia fino a meno della metà e si
posa scivolando in avanti), **C · Slitta** (corre basso e la punta risale a 30 gradi). Tra 99 e 100 in `svg_audit.py`.

### Giro 12: la R costruita, dopo le ricerche (decisione 395)

Piacciono A · Pulito e C · Slitta del giro 11, non B (395). Ricerche dello stesso giorno:
`docs/research/2026-11-20-analisi-libreria-lettera-r.md` (261 loghi a lettera singola della raccolta della skill, prova a
scaffale) e `docs/research/2026-11-20-loghi-lettera-singola-fonti.md` (fonti dei progettisti). Indicazioni prese:
un dettaglio solo che nasce dalla lettera, spessore uniforme e fine netta, forme elementari e sagoma piena, il riquadro
non distingue, R e blu è il territorio di Revolut (#1326FD, R geometrica come icona e nel nome), una versione per i 16
punti e una misura minima di stampa da provare.

File in `prototipi/brand-kit/concetti-7/` (`genera.py`): **A · Pulito costruito** (occhiello più grande, gamba lunga
dello spessore dell'asta che nasce dove l'asta finisce; consigliata), **B · Slitta costruita** (la Slitta con spessore
costante), **C · Collo ritagliato** (radicale: la R è il vuoto dentro un collo pieno; costruita come contorno unico con
archi, così il ritaglio non lascia fili). Scartata prima di mostrarla una «Tre forme» (barra, anello, quarto d'anello
separati): si leggeva «IQ».

### Stato a fine sessione (decisioni 396 e 397)

- **Nome:** Ripo, per ora (386); Varko in riserva (376); ricerca europea dei marchi al consulente (387).
- **Logo:** R · Pulito costruito (396), `prototipi/brand-kit/concetti-7/pulito-simbolo.svg` e `pulito-nome.svg`.
- **Colore:** blu elettrico #1F5BFF (388). **Puntino della i:** tondo (390). **Simbolo e nome:** separati (391).
- **Da fare nel kit (397):** rifinitura ottica; R per i 16 punti; blu chiaro per il tema scuro; versioni nera, bianca,
  blu; icone (favicon, icone dell'app, manifest, con `export_variants.py` della skill); tavola d'uso
  (`presentation_board.py`); guida di una pagina (`templates/brand-guidelines-template.md`); confronto affiancato con
  Revolut e con le R della raccolta; misura minima di stampa da provare su una termica vera.

### Giro 13: il kit (in corso)

File finali in `brand/`, generati da `brand/genera.py` (Python senza dipendenze; per i PNG e il `favicon.ico` usa
`render_png.py` della skill). Il generatore è autonomo: non dipende dai prototipi.

- **Rifinitura ottica** della R · Pulito costruito (396): orizzontali dell'occhiello a 0,9 dell'asta, parte tonda a
  1,05, gamba a 0,95 e di spessore costante; il vuoto è un semi-ellisse; la gamba passa sotto il vuoto (controllo
  numerico nel generatore, almeno mezza unità di distacco); simbolo alzato di 2 su 256 (centro ottico). Versioni
  bianca e blu chiaro più sottili di un'unità su 256 (sul fondo scuro il chiaro sembra più pesante).
- **R per i 16 punti** (`svg/ripo-simbolo-16.svg`): disegnata sulla griglia di 16, asta di 3 pixel, orizzontali di 2,
  vuoto alto 4 e largo 3,5, gamba più corta. Solo per il favicon a 16; da 32 in su la R normale.
- **Nome «Ripo»** a peso medio (374): stesse correzioni sugli anelli di p e o (orizzontali a 0,9), spazi 12, 13 e 11.
- **Versioni**: `svg/ripo-simbolo-{nero,blu,bianco,blu-chiaro}.svg` e `svg/ripo-nome-…` uguali. Nero puro #000000
  per le stampe.
- **Icone** (`icone/`): `favicon.ico` (16 dalla R per i 16 punti, 32 e 48 dal simbolo), `favicon.svg`,
  `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, `maskable-512.png` (segno dentro la zona sicura
  dell'80 %), `icona-app.svg`, `site.webmanifest` (nome Ripo, lingua it), `head-snippet.html`. Non si usa
  `export_variants.py --web-icons`: userebbe la R per i 16 punti anche per le icone grandi.
- **Prova di stampa** (`prova-stampa.svg`, etichetta 100 x 70 mm, da stampare al 100 %): simbolo alto 4–10 mm, nome
  largo 12–30 mm. Calcolo a 203 dpi (8 punti per mm): con il simbolo a 5 mm il vuoto dell'occhiello misura circa
  0,8 mm (6 punti); con il nome a 15 mm lo stacco tra puntino e asta della i misura circa 0,5 mm (4 punti). Proposta:
  minimo 5 mm e 15 mm, da confermare con una stampa vera.
- **Tavola d'uso**: `presentation_board.py` della skill produce contesti generici in inglese (badge da evento, sito
  con un dominio che non è nostro), quindi non si usa; la tavola è nella pagina delle domande, con i contesti della
  368, e diventa un file dopo la conferma.
- **Confronto** con Revolut e Rakuten (icone di Simple Icons 13.0.0) e con le R della raccolta (Remix, Riot, Rax), in
  nero a 72, 48, 32, 24, 20 e 16 pixel: la gamba lunga e curva è l'unica del gruppo; Revolut ha gamba diritta e
  occhiello squadrato; la nostra R a peso 40 è la più leggera. I loghi altrui stanno solo nella pagina pubblicata e
  in una cartella temporanea, non nel repository (come la raccolta, 362).
- **Blu chiaro per il tema scuro**, candidati della stessa tinta del #1F5BFF (contrasto sul #121212 / sul #1C1C1E):
  #5280FF 5,25 / 4,77; #668FFF 6,19 / 5,62; #7A9EFF 7,28 / 6,61. Il blu elettrico sul nero ha 3,57.

Domande del giro 13 (pagina https://claude.ai/artifact/JQ2vwNwRMfT2qi4BDWNnX5, copia in
`prototipi/brand-kit/index.html` senza i loghi altrui): peso del simbolo (asta 40, 44 o 48 su 200), R per i 16 punti
sì o no, blu chiaro, fondo dell'icona dell'app (blu, bianco, nero), confronto sufficiente o gamba da rivedere, chi fa
la prova di stampa. Dopo le risposte: file rigenerati con le scelte, `brand/guida.md`, tavola d'uso come file,
riepilogo da confermare.
