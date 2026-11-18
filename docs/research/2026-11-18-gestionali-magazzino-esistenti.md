# Gestionali di magazzino esistenti: funzioni in più e difetti da evitare

Data: 18/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina o file aperto il 18/11/2026). **DEDUZIONE** =
conclusione nostra a partire dai fatti. **IPOTESI** = da verificare. **ESPERIENZA RIFERITA** = un utente racconta
qualcosa in un forum o in una community: è un racconto, non un fatto verificato, e non dice quanto spesso succede.
"Il produttore dichiara" = affermazione commerciale. "Fonte secondaria" = non viene dal produttore né da un ente
ufficiale. Le date tra parentesi sono quelle della pagina (per Microsoft Learn il campo `ms.date`), quando la pagina le
mostra; altrimenti "senza data".

Questa ricerca non prende decisioni: dove serve una scelta scrive **proposta** o **da decidere**. I numeri tra
parentesi senza altra indicazione sono decisioni di `docs/decisioni.md`.

## Domanda

Ticket «Gestionali di magazzino esistenti: funzioni in più e difetti da evitare» (decisione 180). Come funzionano i
gestionali di magazzino esistenti, quali funzioni hanno che la base non ha, quali difetti riferiscono i loro utenti, e
cosa ne ricaviamo per la base. Attenzione particolare a:

- ingresso del DDT del fornitore e abbinamento agli ordini fornitore (183);
- elenchi delle cose in sospeso per sezione (181);
- sezione «Documenti» con storico e log (182);
- tasti «Annulla» e «Conferma» (180).

La ricerca su Ad Hoc Revolution e ARS Logistica è già in
`docs/research/2026-11-15-adhoc-revolution-ars-logistica.md`: qui non si ripete. Per ARS si usano solo i fatti che
l'utente ha riferito sul suo uso in UFP, già scritti in `docs/architettura.md` e nella decisione 183.

## Prodotti scelti e perché

Criteri: documentazione pubblica leggibile (per citare fatti e non dichiarazioni commerciali), varietà di taglia (dalla
piccola impresa al grande magazzino), prodotti vicini ai due magazzini di prova (UFP con un gestionale italiano,
magazzino Shopify senza gestionale), e una community ufficiale dove gli utenti scrivono i loro problemi.

| Prodotto | Tipo | Perché | Cosa si è letto |
|---|---|---|---|
| Odoo 19 Inventory e Barcode | Gestionale completo, PMI e medie | Documentazione open source molto dettagliata; app Barcode per telefono e palmare; forum ufficiale molto attivo | Sorgenti della documentazione (ramo 19.0 di `odoo/documentation`, scaricato il 18/11/2026), forum ufficiale |
| Microsoft Dynamics 365 Business Central | Gestionale per PMI | Molto diffuso nelle PMI; documentazione pubblica con date; funzioni «Undo» e agenti AI sui documenti | Sorgenti della documentazione (`MicrosoftDocs/dynamics365smb-docs`, ramo main, ultimo aggiornamento 17/11/2026) |
| Dynamics 365 Supply Chain Management, app Warehouse Management | WMS di fascia alta | App mobile per palmari, ricevimento da ASN e carichi, tolleranze | Microsoft Learn |
| SAP Business One e SAP EWM | Gestionale PMI e WMS di fascia alta | Riferimento classico per «ricevimento contro ordine» e «ASN» | SAP Learning, help.sap.com, una nota della base di conoscenza SAP |
| Oracle NetSuite WMS | WMS in cloud per medie imprese | Ricevimento da telefono, ricerca ordini per articolo, blocchi contro il doppio lavoro | docs.oracle.com |
| Oracle Warehouse Management Cloud | WMS di fascia alta | Ricevimento «blind» e per collo con ASN | docs.oracle.com (release 25D) |
| Shopify (ordini d'acquisto, trasferimenti, POS) | Commercio elettronico | È il sistema del secondo magazzino di prova; Stocky è stato chiuso nel 2026 | help.shopify.com, Shopify Community |
| Zoho Inventory, inFlow, Katana | Gestionali di magazzino per piccole imprese | Ricevimento semplice, spesso usati con Shopify | Centri di assistenza ufficiali; community Zoho |
| ShipStation | Spedizioni | Distinte di ritiro (manifest) per corriere | Documentazione ufficiale, community ufficiale |
| Acumatica | Gestionale con WMS | Solo per le esperienze riferite nella sua community ufficiale | community.acumatica.com |
| Danea Easyfatt, TeamSystem | Italiani per piccole imprese | Pratica italiana del DDT | Un articolo TeamSystem (fonte secondaria); la guida PDF di Danea non è leggibile come testo |
| Mecalux Easy WMS | WMS europeo | Citato nel ticket | Nessuna pagina d'uso trovata; solo articoli di blog nei risultati di ricerca, non letti: non citato |

Non coperti, con il motivo: Manhattan, Infor, Sage X3, Generix/Reflex e i WMS italiani di Gamma, Sme.UP, Replica,
Mago4 (Microarea) non hanno documentazione d'uso pubblica trovata in questa sessione; Fishbowl, Cin7, Unleashed, Sortly
sono simili a Zoho/inFlow/Katana e non aggiungevano funzioni diverse nel tempo disponibile.

**Siti di recensioni.** G2, Capterra, TrustRadius e Software Advice hanno risposto «403 Forbidden» e Reddit non è
raggiungibile da questa sessione: nessuna recensione di quei siti è stata letta né citata. Le esperienze riferite
vengono solo da community e forum ufficiali (Odoo, Shopify, Microsoft/Dynamics, Oracle, Zoho, Acumatica, ShipStation)
e da Mibuso (forum storico di Business Central).

## Sintesi

1. **Tutti i prodotti letti ricevono «contro ordine»**: il documento di entrata nasce da uno o più ordini fornitore
   aperti, e l'operatore conta contro le righe attese. La base fa lo stesso con le righe aperte del fornitore (104).
   (FATTO sui prodotti; DEDUZIONE sul confronto)
2. **Un documento di entrata per più ordini è normale nei prodotti più completi**: Business Central riempie una
   ricevuta di magazzino con «Get Source Documents» o con filtri salvati; SAP Business One copia righe da più documenti
   con «Copy From». Odoo crea invece una ricevuta per ogni ordine confermato. (FATTO)
3. **La ricerca dell'ordine per articolo esiste**: NetSuite WMS offre «Find PO by Item». È il ripiego che la base ha
   già scelto (183). (FATTO)
4. **L'ASN (avviso di spedizione) è la via dei grandi**: SAP EWM, Dynamics SCM e Oracle WMS Cloud partono dall'ASN o
   dal carico atteso; con lo SSCC del pallet (codice GS1 a 18 cifre) Oracle riconosce il contenuto del collo descritto
   nell'ASN. Senza ASN, SAP lavora con un «expected goods receipt» e Oracle con il ricevimento «blind». (FATTO)
5. **Il DDT italiano non ha una forma obbligatoria**: il DPR 472/1996 (art. 1, c. 3) ne fissa solo il contenuto (data,
   cedente, cessionario, eventuale vettore, natura, qualità e quantità dei beni). Non abbiamo trovato alcuna norma che
   renda obbligatorio un DDT elettronico tra privati. Esiste un profilo italiano Peppol per il DDT (2020), ma in quella
   data l'NSO della sanità gestiva solo gli ordini. (FATTO; l'assenza di obbligo è DEDUZIONE da ciò che si è trovato)
6. **La fattura elettronica differita porta i riferimenti dei DDT e dell'ordine**: blocchi FatturaPA 2.1.8 `DatiDDT`
   (numero, data, righe) e 2.1.2 `DatiOrdineAcquisto`, più il `CodiceArticolo` di riga. Arriva dopo la merce, ma
   permette una riconciliazione a valle. (FATTO; uso per la base = proposta)
7. **La «document AI» ha modelli pronti per le fatture, non per i DDT**: Azure e Google non hanno un modello pronto per i DDT (solo
   modelli addestrabili con pochi esempi); Mindee ne ha uno che estrae solo i campi di testata (data, numero, fornitore,
   cliente, totale), non le righe; l'agente di Business Central elabora fatture e note di credito in PDF, non DDT.
   Sono tutti servizi in cloud. (FATTO)
8. **Business Central impara gli abbinamenti**: quando l'utente conferma l'abbinamento di una riga di fattura a una
   riga d'ordine, può creare un «item reference», cioè il codice del fornitore per quell'articolo. È lo stesso principio
   della decisione 71. (FATTO; confronto = DEDUZIONE)
9. **Sulle quantità diverse i prodotti offrono tolleranze**: Business Central ha i codici di sovra-ricevimento con
   tolleranza; Dynamics SCM ha la percentuale di sovra-consegna sulla riga e tre comportamenti (permetti, blocca,
   blocca solo sui carichi chiusi). La base accetta tutto e segnala l'eccedenza (32). (FATTO; confronto = DEDUZIONE)
10. **Il residuo è il punto delicato**: Odoo chiede alla validazione se creare un «backorder» (sempre, mai, chiedi); un
    utente racconta di aver scelto «nessun backorder» per sbaglio senza poter tornare indietro. Nella base il residuo
    resta aperto finché lo chiude il responsabile (33). (FATTO ed ESPERIENZA RIFERITA)
11. **Annullare dopo la registrazione è quasi sempre una contro-registrazione**: Business Central «Undo Receipt»
    aggiunge una riga correttiva; SAP Business One annulla con un documento di storno e blocca se esistono documenti
    successivi; Shopify permette di correggere le quantità accettate; Katana riporta l'ordine a modificabile. La base ha
    già le correzioni collegate (74, 81). (FATTO)
12. **Le conferme vengono ignorate**: in Odoo un utente riferisce che i colleghi validavano senza scansionare,
    ignorando l'avviso; la risposta è togliere il permesso di validare senza scansione. Per la base: dove l'errore è
    grave, impedire o mandare al responsabile; dove è frequente e rimediabile, registrare e offrire «Annulla» (99).
    (ESPERIENZA RIFERITA; regola = proposta)
13. **Gli elenchi delle cose in sospeso nei prodotti hanno quattro filtri ricorrenti**: da fare, in ritardo, non
    assegnati, in attesa (Odoo: schede «# To Process», «Back Orders», cruscotto «Late receptions» e «Transfers to be
    assigned» con i dieci più vecchi in ritardo; Business Central: campo «Assigned User ID» con cui ci si prende un
    lavoro). (FATTO; uso per la base = proposta)
14. **Lo storico ha due livelli**: i movimenti (Odoo «Moves History»: data, documento, articolo, da, a, quantità) e il
    registro delle modifiche ai dati (Business Central «Change Log», per tabelle e campi scelti, con politiche di
    conservazione). La base registra già movimenti e scansioni con chi, quando e dispositivo (27, 74, 86). (FATTO)
15. **Inventario cieco di serie**: in Odoo la conta da palmare non mostra la quantità attesa, perché (traduzione nostra)
    mostrarla porta a fidarsi di quella invece di contare; si accende solo per scelta. Business Central impedisce di contare due volte lo
    stesso articolo con le «registrazioni» divise per persona. (FATTO)
16. **Prestazioni con cataloghi grandi**: nel forum Odoo un utente riferisce 50 secondi per aprire un ordine perché
    l'app caricava 64.000 articoli; un altro riferisce un minuto per articolo in un inventario con 70–80 righe. UFP ha
    fino a 35.000 articoli (5): serve un requisito di velocità misurabile. (ESPERIENZA RIFERITA; requisito = proposta)
17. **La rete cade anche nei WMS grandi**: un utente di Dynamics SCM riferisce palmari che si scollegano a intermittenza;
    il POS di Shopify richiede internet per ricevere i trasferimenti. La base ha già scelto server in rete interna e
    operazione in attesa sul dispositivo (23, 127). (ESPERIENZA RIFERITA e FATTO)
18. **Le giacenze di Shopify vengono sovrascritte da più app**: utenti riferiscono app di magazzino che scrivono
    «Available» invece di «On hand», o riportano le giacenze a zero. La base manda variazioni, non valori assoluti (52),
    e ha già «differenze con il sistema d'origine» tra le cose da controllare. (ESPERIENZA RIFERITA; confronto =
    DEDUZIONE)
19. **Funzioni che la base non ha e che ricorrono in quasi tutti i prodotti**: resi (da cliente e al fornitore),
    inventario ciclico, stampa di documenti ed etichette, scarto («scrap») della merce danneggiata. Sono già nella
    nebbia della mappa (160, 175) tranne lo scarto. (DEDUZIONE)

## 1. Funzioni, per tema

Per ogni tema: come lo fanno i prodotti, cosa ha la base (secondo `docs/architettura.md`), cosa manca.

### 1.1 Ricevimento: come nasce il documento di entrata

**Come lo fanno**

- FATTO (Odoo): confermato l'ordine d'acquisto, compare il pulsante «Receipt» che apre la ricevuta di magazzino (WH/IN)
  già legata a quell'ordine. Nell'app Barcode si apre «Operations → Receipts», si sceglie la ricevuta, si scansiona
  ogni prodotto o confezione; il tasto «+#» (per esempio «+12») riempie la quantità ordinata; poi «Validate».
  [receipts_delivery_one_step.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.rst),
  [barcode/operations/receipts_deliveries.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/receipts_deliveries.rst)
- FATTO (Odoo): scansionare il codice dell'operazione «Receipts WHIN» «will always create a *new* instance of that
  operation, and will not match an already scheduled order»; per ritrovare una ricevuta prevista bisogna stamparne il
  foglio con il suo barcode.
  [barcode/setup/operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst)
- FATTO (Business Central): quattro livelli, dal ricevimento direttamente sulla riga d'ordine fino a ricevuta e messa a
  posto separate. La ricevuta di magazzino si crea «push», da un singolo ordine («Create Warehouse Receipt»), o «pull»:
  gli ordini vengono «rilasciati» al magazzino e il magazziniere crea una ricevuta e vi porta le righe di uno o più
  ordini con «Get Source Documents» o con «Use Filters to Get Src. Docs.»; i filtri si salvano e si riusano.
  «Delete Qty. to Receive» azzera le quantità («useful if you're using a barcode scanner»), «Autofill Qty. to Receive»
  le riporta all'atteso.
  [warehouse-how-receive-items.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-receive-items.md)
  (27/01/2025)
- FATTO (SAP Business One): la ricevuta («Goods Receipt PO») si crea con «Copy From», che apre una procedura guidata per
  scegliere uno o più documenti di base e copiarne tutte o alcune righe; un ordine si può richiamare «as many times as
  needed, as long as the status is Open».
  [SAP Learning, Solving Issues in Purchasing](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing)
- FATTO (NetSuite WMS): da telefono si scansiona o scrive «PO # or Item»; per cercare un ordine ci sono «Find PO By
  Vendor», «Find PO by Item» o «Find PO by MPN». Se l'operatore non registra a mano la ricevuta, «NetSuite WMS
  automatically generates item receipts».
  [Receiving Orders](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1541435923.html) (senza data)
- FATTO (Zoho Inventory, inFlow, Katana): la ricevuta nasce dall'ordine, con «Receive» e la quantità per riga; Zoho
  permette «Save as In Transit» o «Save as Received» e la scansione dei barcode; inFlow ha da telefono «Receive» e la
  scansione degli articoli; Katana «Receive all» o «Partially receive».
  [Zoho](https://www.zoho.com/inventory/help/purchase-orders/purchase-receive.html),
  [inFlow](https://www.inflowinventory.com/support/cloud/how-do-i-partially-receive-products-on-a-purchase-order-in-inflow-cloud),
  [Katana](https://support.katanamrp.com/en/articles/5944995-receiving-a-purchase-order-po) (15/07/2026)
- FATTO (Shopify): l'ordine d'acquisto («Draft», poi «Ordered») non si riceve direttamente: si crea un trasferimento
  collegato, che si riceve «in full or partial»; per ogni articolo si registrano quantità accettate, rifiutate o
  annullate; il trasferimento resta «In progress» finché tutto è ricevuto.
  [Purchase orders](https://help.shopify.com/en/manual/products/inventory/purchase-orders),
  [Receiving and managing transfers](https://help.shopify.com/en/manual/inventory-and-locations/inventory-transfers/receiving-and-managing-transfers)
  (senza data)
- FATTO (SAP EWM, Dynamics SCM, Oracle WMS Cloud): con l'ASN del fornitore «SAP ERP creates the corresponding inbound
  delivery automatically»; senza ASN «you work with an expected goods receipt in SAP EWM»
  ([help.sap.com, EWM 9.4](https://help.sap.com/saphelp_ewm94/helpdata/en/4f/436d1b65581242e10000000a42189b/content.htm)).
  In Dynamics SCM il «carico in arrivo» (inbound load) rappresenta una spedizione del fornitore con uno o più ordini e si
  può creare dall'ASN; l'app mobile registra le quantità contro il carico
  ([Inbound load handling](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/inbound-load-handling),
  15/06/2026). In Oracle WMS Cloud il modulo «Receive LPN Shipment» chiede l'ASN e poi il collo; in modalità blind «will
  not prompt you to scan a PO nor ASN» e chiede solo di scansionare un collo
  ([Receive by ASN](https://docs.oracle.com/en/cloud/saas/warehouse-management/25d/owmol/receive-by-asn.html)).

**Cosa ha la base.** Il DDT si crea scegliendo il fornitore; le righe nascono dalle letture e si abbinano agli ordini
fornitore aperti (183, 70, 104); ripiego a mano per articolo (vedi tutti gli ordini che lo contengono) o per ordine
(183); più operatori sullo stesso DDT (68); avviso di possibile doppione (86); numero del fornitore com'è scritto
(modello dei dati).

**Cosa manca o è da decidere**

- DEDUZIONE: la base è più vicina a Business Central «pull» (un DDT, tutte le righe aperte del fornitore) che a Odoo
  (una ricevuta per ordine). È coerente con i DDT che chiudono più ordini.
- Proposta: un filtro sulle righe attese (per esempio solo gli ordini indicati sul DDT, o solo quelli con data di
  consegna vicina), come i filtri salvati di Business Central, se i fornitori di UFP hanno molti ordini aperti. Da
  decidere dopo aver visto quanti ordini aperti ha un fornitore tipico di UFP.
- Proposta: il QR o barcode del DDT stampato dal programma (come «PRINT PICKING OPERATION» di Odoo) per riaprirlo con
  una scansione; utile se il DDT resta aperto per giorni (68). Bassa priorità.

### 1.2 Quantità diverse, ricevimenti parziali, residuo

- FATTO (Odoo): ogni tipo di operazione ha «Create Backorder»: «Ask», «Always» o «Never» («the remaining products
  should be canceled»).
  [operation_type.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/operation_type.rst)
- FATTO (Business Central): se arriva di più, si scrive la quantità ricevuta; «If the increase is within the tolerance
  specified by an assigned over-receipt code» il campo «Over-Receipt Quantity» mostra l'eccedenza; oltre la tolleranza
  «the over-receipt isn't allowed».
  [warehouse-how-receive-items.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-receive-items.md)
- FATTO (Dynamics SCM): ogni registrazione parziale è una transazione a sé; con meno merce si riduce la riga del carico;
  con più merce il campo «Load over receipt» vale *Allow*, *Block* o *Block for closed loads only*, entro la percentuale
  di sovra-consegna copiata dalla riga d'ordine. La registrazione rende la merce prenotabile; la contabilizzazione
  («product receipt») è un passo successivo, con la scelta «Allow multiple product receipt per load» *No* / *Yes* /
  *Prompt*.
  [Inbound load handling](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/inbound-load-handling)
- FATTO (SAP Business One): meno merce → ricevuta parziale e l'ordine resta aperto; più merce → «you can increase the
  copied quantity»; articolo diverso → riga in più; righe non più attese → «close a particular row rather than the
  entire document».
  [SAP Learning](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing)
- FATTO (Shopify): le quantità rifiutate restano registrate sul trasferimento ma «doesn't change inventory quantities».
  [Receiving and managing transfers](https://help.shopify.com/en/manual/inventory-and-locations/inventory-transfers/receiving-and-managing-transfers)

**Cosa ha la base.** Si accetta tutto, eccedenza al responsabile (32); meno merce → riga aperta con residuo finché arriva
il resto o il responsabile la chiude (33); differenze con la bolla al responsabile (73); merce non prevista caricata e
non ubicata (45); chiusura con righe ferme a scelta dell'operatore (82); merce subito in giacenza e assegnabile
nell'area di ricevimento (69), carico al gestionale alla chiusura (61).

**Cosa manca o è da decidere**

- DEDUZIONE: la divisione di Dynamics SCM tra «registrato» (prenotabile) e «contabilizzato» corrisponde già alla base:
  area di ricevimento assegnabile (69) e carico al gestionale a «Chiudi DDT» (61).
- Da decidere: una tolleranza per magazzino o per fornitore (per esempio «oltre il 10% in più chiedi il
  responsabile»), invece di «si accetta tutto» (32). Oggi l'eccedenza va comunque al responsabile: la tolleranza
  servirebbe solo a non disturbarlo per differenze piccole. Bassa priorità.
- Da decidere: «rifiutata» come esito di riga (merce arrivata ma non accettata, per esempio danneggiata), come in Shopify.
  Vedi § 1.14.

### 1.3 Messa a posto

- FATTO (Odoo): regole di messa a posto per prodotto, categoria o tipo di imballo («When product arrives in» → «Store
  to»), più categorie di ubicazione con capacità.
  [putaway.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/putaway.rst)
- FATTO (Odoo): il «Reception report» assegna la merce in arrivo da un ordine d'acquisto a ordini cliente precisi, prima
  della validazione.
  [reception_report.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/reception_report.rst)
- FATTO (Business Central): «Post and Print» stampa la ricevuta come istruzione di messa a posto; con le messe a posto
  separate la merce «can't pick them until they're put away».
  [warehouse-how-receive-items.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-receive-items.md)

**Cosa ha la base.** Ubicazione abituale proposta (75), messa a posto subito o dall'elenco «da mettere a posto» (69,
163), VEND per la merce già venduta (44, 47).

**Cosa manca.** DEDUZIONE: il «Reception report» di Odoo fa a mano ciò che VEND fa da sé con il riferimento cliente.
Regole per categoria e capacità: possibile estensione, bassa priorità per i due magazzini di prova.

### 1.4 Prelievo: ordine singolo, batch, cluster, ondate

- FATTO (Odoo): *batch* = più prelievi insieme, da dividere dopo; *cluster* = più ordini insieme con un contenitore per
  ordine sul carrello, «eliminates the need for post-picking consolidation», ma «urgent orders cannot be prioritized»;
  *wave* = parti di prelievi diversi raggruppate per ubicazione, categoria o orario di spedizione, poi divise.
  [cluster.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/picking_methods/cluster.rst),
  [wave.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/picking_methods/wave.rst)
- FATTO (Business Central): se il responsabile non assegna, ci si prende un lavoro scrivendo il proprio utente in
  «Assigned User ID», «and the warehouse will avoid a duplication of effort».
  [warehouse-how-to-find-your-warehouse-assignments.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-to-find-your-warehouse-assignments.md)
  (24/06/2021)
- FATTO (NetSuite WMS): i «lock record» impediscono a due operatori di lavorare la stessa riga; «In some cases, the
  system might not unlock lock records as expected. A periodic script runs to unlock incorrectly locked records.»
  [Mobile Device Transactions](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156382533850.html)

**Cosa ha la base.** Un ordine alla volta, riga per riga in ordine di ubicazione (164); piani di spedizione o coda
«Prossimo ordine» (167, 168); un ordine preso da una sola persona, riassegnabile (170, 175).

**Cosa manca.** Giri su più ordini: già possibile estensione (164). DEDUZIONE dal caso NetSuite: un ordine «preso» e mai
finito resta bloccato; per la coda la base lo fa rimettere in coda dal responsabile (175), per i piani lo riassegna chi
pianifica (170). Proposta: mostrare da quanto tempo un ordine è «in preparazione da…» negli elenchi in sospeso (§ 1.9).

### 1.5 Imballo e spedizione

- FATTO (Odoo): «Put in Pack» mette i prodotti scansionati in un collo; una consegna può partire in più colli; alla
  validazione si possono stampare da sé bolla di consegna, etichette del corriere, etichetta e contenuto del collo; nel
  tipo di operazione si collega una bilancia; «Dispatch management» raggruppa per corriere e mezzo.
  [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst),
  [multipack.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/multipack.rst),
  [print_on_validation.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/print_on_validation.rst),
  [dispatch.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/dispatch.rst)
- FATTO (ShipStation): «A manifest is a physical or electronic document that provides a list of a specific day's
  shipments»; «Manifests will always be specific to a carrier, a warehouse location, and a ship date».
  [Manifests and SCAN forms](https://docs.shipstation.com/manifests-scanforms) (senza data)

**Cosa ha la base.** Colli e chili a fine preparazione (171), corriere in grande e posto dei colli (174), «Spedisci»
divisa per corriere con «Ritirato da…» (172, 173). DEDUZIONE: «Spedisci» fa già da distinta di ritiro per corriere e
giorno, senza stamparla.

**Cosa manca o è da decidere.** Stampa di etichette del corriere e della distinta (BRT, GLS) e numero di tracking: oggi
in UFP le fa Ad Hoc o il portale del corriere? Da chiedere al rivenditore (domande 21–22). Per il magazzino Shopify:
da decidere se le etichette restano su Shopify o un'app di spedizione.

### 1.6 Vendita al banco e POS

- FATTO (Odoo POS): dal POS si apre l'elenco «Quotations/Orders» delle vendite e si incassa un ordine nato altrove;
  «Ship Later» vende subito e spedisce dopo; «Log in with Employees» dà permessi base o avanzati a ciascun dipendente.
  [sales_order.rst](https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/shop/sales_order.rst),
  [ship_later.rst](https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/shop/ship_later.rst),
  [employee_login.rst](https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/employee_login.rst)
  (ramo 18.0)
- FATTO (Shopify POS): si ricevono i trasferimenti dal POS («Accept all» o per riga, scansionando o contando); servono
  i permessi «Inventory» e «Manage transfers», un abbonamento POS Pro e «an active internet connection».
  [Fulfilling and receiving transfers in Shopify POS](https://help.shopify.com/en/manual/sell-in-person/shopify-pos/inventory-management/fulfilling-and-receiving-transfers)
- FATTO (ARS Logistica, dalla ricerca precedente): la «vendita assistita» crea una lista di prelievo, e il documento di
  consegna si genera dal gestionale.

**Cosa ha la base.** Vendita assistita: cliente, articoli e ubicazione, avviso se si toglie merce ad altri ordini,
conferma che crea l'ordine nel gestionale (58, 65, 178). DEDUZIONE: la base è allineata ad ARS; incasso e ricevute
restano in Ad Hoc (178). Nulla da aggiungere per UFP; per il magazzino Shopify il banco non è emerso come bisogno.

### 1.7 Inventario

- FATTO (Odoo): la conta ciclica è per ubicazione, con una frequenza in giorni; il responsabile «Request a Count»
  assegnando persona e data, e il conteggio compare sul cruscotto del palmare; «Count Entire Locations» fa contare tutto
  ciò che c'è in un'ubicazione, anche ciò che non dovrebbe esserci. «When conducting an inventory count, the expected
  quantity of products is not displayed by default, as displaying expected quantities can result in users relying on
  this count instead of performing a new count.» La conta registrata «is recorded, but not yet applied» finché non si
  applica.
  [cycle_counts.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/cycle_counts.rst),
  [barcode/operations/adjustments.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/adjustments.rst),
  [count_products.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.rst)
- FATTO (Business Central): un «Physical Inventory Order» per l'intero inventario e più «recordings», una per gruppo di
  articoli e persona; «Business Central ensures that you can't record an item count twice».
  [inventory-how-count-inventory-with-documents.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/inventory-how-count-inventory-with-documents.md)
  (07/04/2026)

**Cosa ha la base.** «Conta un'ubicazione» quando la merce c'è ma non risulta: la rettifica vale subito e va al
responsabile (77). Inventario periodico fuori dal ticket (160).

**Cosa manca.** Proposta per il futuro ticket sull'inventario: conta cieca di serie (come Odoo), conte richieste dal
responsabile a una persona per ubicazione, conta in due fasi (contata → applicata dal responsabile) per l'inventario
completo, divisione per persona per evitare doppi conteggi. In UFP ARS fa oggi l'inventario anche «senza rete»
(ricerca precedente): da chiedere se lo usano.

### 1.8 Resi

- FATTO (Business Central): il reso al fornitore si fa con una nota di credito o un «purchase return order», che può
  prendere le righe da più documenti registrati («Get Posted Document Lines to Reverse») e riprendere il costo esatto
  d'acquisto.
  [purchasing-how-process-purchase-returns-cancellations.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/purchasing-how-process-purchase-returns-cancellations.md)
  (16/11/2026)
- FATTO (SAP Business One): «A Goods Return is used to return items received on a Goods Receipt PO»; per la merce
  danneggiata si parte da una «Goods Return Request».
  [SAP Learning](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing)
- FATTO (Odoo): il reso parte dal pulsante «Return» sulla consegna validata.
  [starshipit_shipping.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/starshipit_shipping.rst)
- Fonte secondaria (TeamSystem, aggiornato 14/10/2026): il DDT di reso accompagna la merce rispedita; deve avere una
  causale «che si tratta di un reso» e conviene citare «il riferimento al documento di vendita o al DDT originario».
  [teamsystem.com](https://www.teamsystem.com/magazine/gestione-impresa-e-partita-iva/ddt-reso-logistica-inversa/)

**Cosa ha la base.** Il responsabile può decidere di «rendere al fornitore» la merce non prevista (45) o quella di un
articolo rifiutato (114); i resi al fornitore sono nella nebbia (160). I resi da cliente non sono trattati.

**Da decidere.** Resi da cliente (soprattutto nel magazzino Shopify, dove arrivano da Shopify) e resi al fornitore,
con il loro DDT di reso: in UFP il DDT di reso lo emette Ad Hoc? Da chiedere al rivenditore.

### 1.9 Elenchi delle cose in sospeso, code di lavoro, cruscotti

- FATTO (Odoo): la panoramica di magazzino ha una scheda per tipo di operazione con «# To Process» e «Back Orders #»; il
  cruscotto «Warehouse Daily Operations» mostra «Late receptions», «Late deliveries», «Transfers to be assigned» (senza
  responsabile), gli aperti per persona e «the ten oldest open receipts with a past scheduled date»; le dashboard di
  analisi («Operation analysis», «Warehouse Metrics») sono visibili di serie solo agli amministratori.
  [dashboards.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/dashboards.rst),
  [multipack.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/multipack.rst)
- FATTO (Odoo): le conte richieste compaiono sul cruscotto dell'app Barcode con il numero di prodotti da contare.
  [adjustments.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/adjustments.rst)
- FATTO (Business Central): sul ruolo dell'utente il riquadro «Waiting Purchase E-Invoices» elenca le fatture
  elettroniche ancora da abbinare; «Linked Purchase Orders» quelle già collegate.
  [map-edocuments-with-copilot.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/map-edocuments-with-copilot.md)
  (02/10/2026)
- FATTO (Dynamics SCM): le «deviazioni» (detours) permettono di «"park" the current task, perform another task, and
  then return to the original task without losing any information».
  [warehouse-app-detours](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-app-detours)
  (08/04/2026)

**Cosa ha la base.** Prima schermata con un pulsante per lavoro e il numero di cose che aspettano (161, 177); «Da
controllare» per il responsabile (86); DDT aperti con righe complete (Percorso); «da mettere a posto» (163); elenchi
per sezione chiesti dall'utente (181).

**Proposta per gli elenchi in sospeso (181).** Una forma unica per tutte le sezioni, con i filtri che ricorrono nei
prodotti:

| Gruppo nell'elenco | Esempio ricevimento | Esempio preparazione | Esempio vendita assistita |
|---|---|---|---|
| In corso (iniziati da me) | DDT che ho aperto | Ordini che ho preso | Vendita lasciata a metà |
| In corso (da altri) | DDT con scansioni di colleghi, con chi e quando | «In preparazione da…» con da quanto tempo | — |
| Fermi, con il motivo | Righe che aspettano il responsabile (166) | Ordine coperto in parte in attesa | Articolo provvisorio da collegare (115) |
| Vecchi | Aperti da più di N giorni | Pronti ma non spediti (172) | — |

Ordinati dal più vecchio, come l'assegnazione. Il numero sul pulsante della prima schermata conta solo ciò che tocca a
quell'utente. DEDUZIONE: nessun prodotto letto distingue «in corso» da «mai iniziato» con la stessa chiarezza del
cruscotto Odoo; il criterio «più vecchi in ritardo» viene da lì. Il valore di N è da decidere.

### 1.10 Storico, registro delle operazioni, documenti

- FATTO (Odoo): «Moves History» elenca per ogni movimento data e ora, riferimento (per esempio il numero della
  ricevuta), prodotto, lotto, da, a, quantità; è accessibile solo agli amministratori. Ogni rettifica di inventario
  «simultaneously creates a stock move record».
  [moves_history.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/moves_history.rst),
  [count_products.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.rst)
- FATTO (Odoo): un backorder creato compare nella cronologia del documento originale («The backorder WH/OUT/XXXXX has
  been created»).
  [multipack.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/multipack.rst)
- FATTO (Business Central): il «Change Log» «lets you track all direct modifications a user makes to data», per le
  tabelle e i campi scelti; le voci si cancellano solo con una politica di conservazione per date.
  [across-log-changes.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/across-log-changes.md)
  (17/06/2026)
- FATTO (Business Central): sui documenti registrati si modificano solo pochi campi; «For more critical fields that
  affect the auditing trail, you must reverse or undo posting».
  [purchasing-how-record-purchases.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/purchasing-how-record-purchases.md)
- FATTO (Odoo): «PRINT PICKING OPERATION» stampa un PDF con il barcode del documento, «This can be scanned later to go
  directly to the operation»; «PRINT DELIVERY SLIP» stampa la bolla.
  [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst)

**Cosa ha la base.** Movimenti mai cancellati, correzioni collegate (74); storico con chi, quando, dispositivo, cosa,
esito (27); ogni scansione registrata con come è stata identificata e le proposte mostrate (86, 104); un DDT si trova
sempre in qualsiasi stato (requisiti di affidabilità); sezione «Documenti» chiesta (182).

**Proposta per «Documenti» (182).** Due viste dello stesso storico:

1. **Per documento**, divise per categoria: DDT, prelievi e preparazioni, spedizioni (per corriere e giorno), vendite
   assistite, rettifiche e conte, correzioni, scambi con gestionale e Shopify (con lo stato della coda di uscita, 54).
   Ogni documento si apre con le sue righe, i suoi movimenti e la sua cronologia (chi ha fatto cosa, quando, da quale
   dispositivo, compresi i cambi di «Preparato da», 175). Per il DDT anche la foto della bolla, se si decide di farla
   (§ 2.4).
2. **Registro delle operazioni** (log): tutto in ordine di tempo, filtrabile per persona, dispositivo, articolo,
   documento ed esito (salvata, in attesa, non riuscita). Comprende accessi, uscite, decisioni del responsabile,
   modifiche di configurazione e utenti.

Da decidere: chi vede cosa (in Odoo lo storico dei movimenti è solo per gli amministratori; per la base l'operatore
potrebbe vedere i propri documenti e il responsabile tutto), quanto a lungo si conservano registro e foto, e
l'esportazione in file (vedi § 3, tema «dati prigionieri»).

### 1.11 Permessi e ruoli

- FATTO (Odoo): «Allow full picking validation» (attivo di serie) permette di validare un trasferimento senza
  scansionare; si toglie per costringere alla scansione (forum, § 3). In Odoo le dashboard di analisi e lo storico dei
  movimenti sono di serie riservati agli amministratori.
  [Odoo forum 240334](https://www.odoo.com/forum/help-1/barcode-is-it-possible-to-prevent-users-from-validating-without-scanning-240334),
  [dashboards.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/dashboards.rst)
- FATTO (Dynamics SCM): ogni utente vede solo le voci del menu mobile assegnato al suo profilo.
  [warehouse-app-detours](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-app-detours)
- FATTO (Shopify POS): ricevere trasferimenti richiede i permessi «Inventory» e «Manage transfers».
  [help.shopify.com](https://help.shopify.com/en/manual/sell-in-person/shopify-pos/inventory-management/fulfilling-and-receiving-transfers)

**Cosa ha la base.** Ruoli operatore e responsabile (27), permessi «Pianifica le spedizioni» e «Conferma le spedizioni»
(169, 173), mansioni che decidono cosa si vede per primo (177). DEDUZIONE: la base è già allineata. Da decidere solo
la visibilità di «Documenti» (§ 1.10).

### 1.12 Annullare e confermare

- FATTO (Business Central): «Undo Receipt» sulla ricevuta registrata: «A corrective line is added under the selected
  receipt line»; le quantità ricevute sull'ordine tornano a zero.
  [finance-how-reverse-journal-posting.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/finance-how-reverse-journal-posting.md)
  (07/04/2026)
- FATTO (SAP Business One): «For incorrect entry of a Goods Receipt PO, you can cancel the document»; l'annullamento
  crea un documento di storno e «The purchase order is re-opened after cancellation»
  ([SAP Learning](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing)).
  Con un'impostazione attiva l'annullamento si blocca con «Cancellation is not possible; cancel target documents
  first» ([SAP KBA 3779589](https://userapps.support.sap.com/sap/support/knowledge/en/3779589), anteprima pubblica).
- FATTO (Shopify): dopo il ricevimento «you can edit the accepted, rejected, or canceled quantities in a received
  shipment to make corrections».
  [Undo a transfer](https://help.shopify.com/manual/products/inventory/transfers/cancel-transfer/)
- FATTO (Katana): «Use the **Revert** option to return the PO to an editable state».
  [Katana](https://support.katanamrp.com/en/articles/5944995-receiving-a-purchase-order-po)
- FATTO (Odoo): il comando «CANCEL» annulla un'operazione prima della validazione; il comando «VALIDATE» la conferma;
  dopo la validazione il rimedio è un reso o una rettifica (forum, § 3).
  [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst)

**Cosa ha la base.** Barcode certo registrato senza tocchi con «Annulla · Modifica» (99); correzione dell'ultima
scansione a DDT aperto (81); dopo la chiusura solo il responsabile, con rettifica al gestionale (81); «Chiudi DDT» con
scelta sulla riga ferma (82); «Spedito» solo al ritiro (172).

**Proposta di regola per «Annulla» e «Conferma».** DEDUZIONE da § 1.12 e § 3:

| Tipo di azione | Esempi | Comportamento proposto |
|---|---|---|
| Frequente e rimediabile | Scansione, quantità, messa a posto, presa di un ordine | Nessuna conferma: si registra e si mostra «Annulla» per qualche secondo, poi resta «Modifica» dalla riga finché il documento è aperto (99, 81) |
| Chiude un documento | «Chiudi DDT», fine preparazione, «Ritirato da…» | Una schermata di riepilogo con le conseguenze in parole semplici (cosa resta aperto, cosa va al gestionale, cosa va al responsabile), un tasto «Conferma» con il verbo dell'azione e un tasto per tornare indietro; niente domande sì/no generiche |
| Tocca il lavoro di altri o il gestionale | Togliere merce a un altro ordine (58), riassegnare un ordine (170) | Conferma con il nome di ciò che si tocca |
| Irreversibile o grave | Rifiutare un articolo (114), chiudere un residuo (33) | Solo il responsabile; conferma esplicita |

Ogni annullamento diventa una correzione collegata, mai una cancellazione (74), e compare nel registro (§ 1.10).

### 1.13 Uso da telefono e palmare

- FATTO (Odoo): l'app Barcode funziona con lettori USB, Bluetooth e palmari Android; «expects that the scanner works
  like an analogue keyboard»; per i Zebra va configurato DataWedge; consiglia Zebra TC21/TC26.
  [device_troubleshooting.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/device_troubleshooting.rst)
- FATTO (Odoo): i codici dei comandi (VALIDATE, CANCEL, PUT IN PACK, SCRAP) si stampano e si scansionano, «without the
  need to touch a screen».
  [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst)
- FATTO (Odoo): il lotto o la matricola si possono rendere a «Mandatory Scan», «the only way to input a required serial
  number or lot number is by scanning a barcode».
  [serial_numbers_lots.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/serial_numbers_lots.rst)
- FATTO (Dynamics SCM): l'app mobile gira su Windows, Android e iOS; il collegamento si configura scansionando un QR.
  [install-configure-warehouse-management-app](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/install-configure-warehouse-management-app)
  (29/09/2026)
- FATTO (Business Central): l'app per iOS e Android usa la fotocamera per leggere barcode 1D e 2D.
  [includes/barcode-mobile-app.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/includes/barcode-mobile-app.md)
- Non trovato nelle fonti lette: suoni o vibrazioni come conferma della scansione, e lavoro senza rete nelle app
  standard dei produttori.

**Cosa ha la base.** Fotocamera su telefono, grilletto sul palmare come tastiera (IPOTESI da provare), web app servita
in sede, QR alla prima apertura, rete assente con operazione in attesa (119–127).

**Da decidere.** Conferma della scansione con suono e vibrazione oltre che a schermo (per l'accessibilità, mai solo
suono). Un requisito di velocità misurabile con il catalogo di UFP (§ 3, tema «lentezza»). Codici dei comandi stampati:
non servono, perché la base registra senza tocchi il barcode certo (99).

### 1.14 Eccezioni

- FATTO (Odoo): «SCRAP» segna un prodotto scansionato come difettoso e lo sposta in un'ubicazione virtuale.
  [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst),
  [scrap_inventory.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/scrap_inventory.rst)
- FATTO (SAP Business One): articolo sostitutivo come riga in più; danneggiato → richiesta di reso.
  [SAP Learning](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing)
- FATTO (Oracle WMS Cloud): avviso se un attributo scansionato (per esempio il lotto) è diverso dall'ASN.
  [Receive by ASN](https://docs.oracle.com/en/cloud/saas/warehouse-management/25d/owmol/receive-by-asn.html)
- FATTO (Dynamics SCM): una deviazione «location inquiry» serve quando «the bar code is damaged and therefore
  unreadable».
  [warehouse-app-detours](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-app-detours)

**Cosa ha la base.** Articolo non atteso (88), codice simile (89), barcode sconosciuto (92), «non lo so» con le sue
uscite (98), codice diverso (158), unità mai vista (72), articolo nuovo (105–110), merce non prevista (45), eccedenze e
mancanze (32, 33). DEDUZIONE: per l'identificazione la base è più ricca dei prodotti letti.

**Manca.** Merce danneggiata o non conforme all'arrivo e in magazzino: nessuna decisione. Proposta: un esito di riga
«danneggiata» al ricevimento (contata, non assegnata, al responsabile, che decide se tenerla, renderla o scartarla) e
uno scarto dalla scheda dell'articolo. Da decidere.

## 2. Ingresso del DDT: soluzioni esistenti e possibili

### 2.1 Cosa dice la norma italiana

- FATTO: il DPR 472/1996, art. 1, c. 3, disciplina «il documento previsto dall'articolo 21, comma 4, terzo periodo,
  lettera a)» del DPR 633/1972; deve indicare data, generalità del cedente, del cessionario e dell'eventuale incaricato
  del trasporto, natura, qualità e quantità dei beni ceduti; per la conservazione rinvia all'art. 39 del DPR 633/1972.
  Il testo letto non prescrive una forma né una numerazione.
  [Normattiva, testo vigente al 01/01/2013](https://www.normattiva.it/eli/id/1996/09/12/096G0487/CONSOLIDATED/20130101)
- DEDUZIONE: il DDT può essere su carta o elettronico; non abbiamo trovato (ricerca su Agenzia delle Entrate e fonti
  di settore) alcuna norma che renda obbligatorio il DDT elettronico tra imprese. Va considerato «non trovato», non
  «escluso»: da confermare con il commercialista di UFP se serve.
- FATTO: AgID ha approvato nel 2020 il profilo italiano «PEPPOL BIS Despatch Advice 3.0» per il DDT, che «can be used
  for software developments»; l'approvazione «does NOT currently have any impact» sul Nodo di Smistamento degli Ordini
  (NSO), che «will continue to manage only the PEPPOL BIS 3 order formats relating to Orders».
  [AgID, 20/04/2020](https://peppol.agid.gov.it/en/news/result-ddt-consultation/)
  Lo stato attuale dell'NSO sul DDT non è stato verificato: la pagina della Ragioneria provata risponde «La pagina
  richiesta non è disponibile».
- FATTO: Peppol BIS Despatch Advice (versione 3.1 nella pagina) porta il riferimento all'ordine in testata o per riga
  (`OrderLineReference`), le quantità consegnate e in sospeso, e le unità di trasporto identificate da SSCC.
  [docs.peppol.eu](https://docs.peppol.eu/poacc/upgrade-3/profiles/30-despatchadvice/)
- FATTO: dal 9 luglio 2027 «The eFTI Regulation will apply in full»: le autorità degli Stati UE dovranno accettare le
  informazioni sul trasporto merci date in forma elettronica da piattaforme certificate. La pagina non dice che le
  imprese siano obbligate a usarle.
  [Commissione europea, eFTI](https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en)
- FATTO: nella FatturaPA (documentazione in vigore dal 01/04/2025) il blocco 2.1.8 `DatiDDT` è «da valorizzare nei casi
  di fattura "differita" per indicare il documento con cui è stato consegnato il bene», ripetibile per più DDT, con
  `NumeroDDT`, `DataDDT` e `RiferimentoNumeroLinea`; il blocco 2.1.2 `DatiOrdineAcquisto` porta numero e data
  dell'ordine; la riga ha `CodiceArticolo` (ripetibile).
  [fatturapa.gov.it, formato](https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/),
  [rappresentazione tabellare, fattura ordinaria (PDF)](https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.4/RappresentazioneTabellareFattOrdinaria-1.pdf)

### 2.2 Come entra il documento del fornitore nei prodotti

| Via | Chi la usa | Come funziona | Limiti |
|---|---|---|---|
| Contro l'ordine, senza documento del fornitore | Odoo, Zoho, inFlow, Katana, SAP B1, Shopify | Si apre la ricevuta dall'ordine e si conta | Una ricevuta per ordine (Odoo); il numero del DDT del fornitore è un campo scritto a mano o assente (FATTO dalle pagine lette, che non lo citano) |
| Un documento di entrata per più ordini | Business Central («Get Source Documents», filtri), SAP B1 («Copy From»), Dynamics SCM (carico con più ordini) | Il magazziniere sceglie gli ordini o li porta con un filtro | Serve sapere quali ordini sono nella consegna |
| Ricerca dell'ordine per articolo | NetSuite WMS («Find PO by Item») | Si scansiona l'articolo e si trova l'ordine | Pagina letta: non dice cosa succede se l'articolo è su più ordini |
| ASN / avviso di spedizione elettronico | SAP EWM, Dynamics SCM, Oracle WMS Cloud; EDI DESADV (GS1), Peppol Despatch Advice | Il fornitore manda prima della merce cosa arriva, con ordini, righe e colli (SSCC) | Serve un fornitore che lo mandi e un canale EDI o Peppol |
| Collo o pallet con SSCC | Oracle WMS Cloud («smart LPN»); Odoo (regola GS1 «(00)» → collo) | Una scansione dello SSCC fa riconoscere il contenuto descritto nell'ASN | Senza ASN lo SSCC identifica il collo ma non dice cosa c'è dentro |
| Ricevimento «blind» | Oracle WMS Cloud; Odoo (scansionando «WHIN» nasce una ricevuta nuova) | Si conta senza documento atteso e si riconcilia dopo | In Odoo non si aggancia alla ricevuta prevista: rischio di doppioni (FATTO dall'avviso nella documentazione) |
| Fattura elettronica abbinata agli ordini | Business Central (e-documents; Copilot e poi «Payables Agent») | Il numero d'ordine nel file collega fattura e ordine; le righe si abbinano per testo (≥80% di descrizione uguale) o con l'AI; l'abbinamento confermato può creare il codice del fornitore | Lavora sulla fattura, non sul DDT; le funzioni AI di Microsoft sono in cloud; il Copilot di abbinamento è dichiarato superato |
| PDF del documento letto da AI | Business Central «Payables Agent» (fatture e note di credito da una casella email) | Estrae i dati dal PDF e propone le righe d'ordine | Solo fatture e note di credito; email con PDF |

Fonti della tabella:
[Odoo operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst),
[Odoo gs1_nomenclature.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/gs1_nomenclature.rst),
[BC warehouse-how-receive-items.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-receive-items.md),
[BC map-edocuments-with-copilot.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/map-edocuments-with-copilot.md)
(02/10/2026),
[BC payables-agent.md](https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/payables-agent.md)
(03/11/2026),
[NetSuite](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1541435923.html),
[Oracle WMS Cloud](https://docs.oracle.com/en/cloud/saas/warehouse-management/25d/owmol/receive-by-asn.html),
[SAP EWM](https://help.sap.com/saphelp_ewm94/helpdata/en/4f/436d1b65581242e10000000a42189b/content.htm),
[Dynamics SCM](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/inbound-load-handling),
[SAP Learning](https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing).

Altri fatti utili:

- FATTO (GS1 Italy, maggio 2020): il DESADV «deve essere creato da chi effettua la consegna e deve rispecchiare quanto è
  fisicamente presente nel mezzo di trasporto»; può riferirsi all'ordine, al DDT e al contratto; «L'uso del SSCC nel
  DESADV, accelera il processo di ricezione della merce» con il «controllo incrociato» tra spedizione fisica e messaggio;
  gli standard EDI di GS1 Italy sono EANCOM ed EURITMO. Il documento riguarda la filiera del largo consumo e dice che
  «l'adozione procede per gradi».
  [Ottimizza il processo di consegna con il DESADV (PDF)](https://gs1it.org/files/sharing/1591179307/1615/ottimizza-il-processo-consegna-con-il-desadv.pdf)
- FATTO (servizi di lettura dei documenti): Azure Document Intelligence ha modelli pronti per fatture e scontrini, non
  per DDT; un modello di estrazione personalizzato richiede «only five examples of the same form or document type»
  ([model-overview](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview),
  05/06/2026). Google Document AI non ha un processore per DDT; il «Custom Extractor» generativo supporta ufficialmente
  solo l'inglese e alcune regioni ([processors-list](https://docs.cloud.google.com/document-ai/docs/processors-list)).
  Mindee ha un'API «Delivery Note» con sette campi di testata (data e numero di consegna, nome e indirizzo di fornitore e
  cliente, importo totale) e nessuna riga nella pagina letta
  ([docs.mindee.com](https://docs.mindee.com/v1/off-the-shelf-products/delivery-note)). Tutti e tre sono servizi in cloud
  (Mindee: tutti gli esempi chiamano `api.mindee.net`).
- FATTO (PaddleOCR, già scelto per il codice stampato, 145): oltre al riconoscimento del testo ha PP-StructureV3, che
  «converts complex PDFs and document images into Markdown and JSON files that preserve original structure», e
  PaddleOCR-VL, modello da 0,9 miliardi di parametri per l'analisi dei documenti.
  [paddleocr.ai](https://www.paddleocr.ai/latest/en/index.html) (pagina non più l'ultima versione; licenza non scritta
  nella pagina)

### 2.3 Limiti delle soluzioni

- DEDUZIONE: ASN, DESADV e Peppol funzionano solo se il fornitore li manda. Nelle fonti lette sono la via dei grandi
  magazzini e della grande distribuzione; per UFP non sappiamo se qualche fornitore li manda (IPOTESI: pochi o nessuno).
- DEDUZIONE: la fattura elettronica differita arriva dopo la merce (di norma a fine mese, IPOTESI per UFP) e passa da
  Ad Hoc: serve al controllo a valle (quantità fatturate contro ricevute), non al ricevimento.
- DEDUZIONE: la lettura automatica delle righe di un DDT cartaceo non è un prodotto maturo nelle fonti lette: i servizi
  pronti leggono solo la testata o vanno addestrati per ogni fornitore, e sono in cloud, contro la scelta del server
  in sede (121, 126). Con PaddleOCR in sede la testata (numero, data) è probabilmente leggibile; le righe dipendono dal
  modulo di ogni fornitore. IPOTESI da provare su DDT veri di UFP.
- DEDUZIONE: il ricevimento «blind» puro (nessun ordine in vista) toglie alla base l'aiuto degli articoli attesi per
  il riconoscimento visivo (104, 144). Non conviene come modo normale.
- DEDUZIONE: il DDT cartaceo resta comunque il documento che il trasportatore consegna; il numero del fornitore va
  registrato com'è scritto (modello dei dati, 86).

### 2.4 Cosa servirebbe per UFP e per il magazzino Shopify

Proposte, da decidere con l'utente. In ordine di costo crescente.

1. **Foto della bolla all'apertura del DDT** (archivio): una foto, salvata con il DDT e visibile in «Documenti».
   Risolve «DDT non rintracciabile» (caso ARS) e dà al responsabile la bolla per controllare le differenze (73).
2. **Numero e data letti dalla foto**: PaddleOCR in sede propone numero e data, l'operatore li conferma; serve anche
   all'avviso di doppione (86). IPOTESI da provare sui DDT veri.
3. **Righe della bolla come «quantità in bolla»** (73): se la lettura delle righe riesce per un fornitore, si
   precompilano le quantità in bolla, mai le quantità contate. Le righe contate restano quelle delle letture della merce
   (183). Da provare fornitore per fornitore; bassa priorità.
4. **Filtro degli ordini attesi** dal numero d'ordine stampato sul DDT, se il fornitore lo stampa (70 già usa l'ordine
   «indicato sul DDT»): letto dalla foto o scelto dall'elenco.
5. **File del fornitore** (CSV, XML Peppol Despatch Advice, DESADV): punto d'estensione per importare l'avviso di
   spedizione quando un fornitore lo manda. Per UFP solo se emerge un fornitore che lo fa.
6. **Riconciliazione con la fattura differita** (FatturaPA 2.1.8): nel collegamento con Ad Hoc della specializzazione,
   confronto tra quantità fatturate e quantità caricate per DDT, con le differenze in «Da controllare».
7. **Magazzino Shopify**: niente fattura elettronica dal gestionale (non c'è un gestionale). Le stesse vie 1–4 valgono;
   la 6 solo se il magazzino riceve le fatture XML in un modo che il programma può leggere (da decidere).

DEDUZIONE: la scelta della decisione 183 (righe dalle letture, ripiego per articolo o per ordine) coincide con la
soluzione dei prodotti PMI più completi (Business Central «pull» e NetSuite «Find PO by Item»). Nessun prodotto letto
crea le righe da un DDT cartaceo in modo affidabile; la novità della base è il riconoscimento della merce, non la
lettura della bolla.

## 3. Difetti riferiti dagli utenti

Tutte le voci sono ESPERIENZE RIFERITE da utenti in forum o community ufficiali, salvo dove è scritto FATTO (difetti
dichiarati dal produttore nella sua documentazione). Non dicono quanto il problema sia frequente. Niente nomi.

### 3.1 Conferme e validazioni

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| Gli operatori premevano «Validate» senza scansionare, ignoravano l'avviso e confermavano; la giacenza fisica non corrispondeva più. Rimedio indicato: togliere «Allow full picking validation» | [Odoo forum 240334](https://www.odoo.com/forum/help-1/barcode-is-it-possible-to-prevent-users-from-validating-without-scanning-240334), data non visibile | Le righe del DDT nascono solo dalle letture (183) e «Chiudi DDT» non riempie le quantità attese. Da tenere: nessun tasto «riempi con l'atteso» come «+#» di Odoo o «Autofill» di Business Central (proposta) |
| Scelto per sbaglio «nessun backorder» dopo la validazione: non si può annullare; il rimedio è duplicare il documento e rifarlo | [Odoo forum 165345](https://www.odoo.com/forum/help-1/accidentally-clicked-no-back-order-how-can-i-undo-it-165345), data non visibile | Il residuo resta aperto; solo il responsabile chiude una riga (33). Evitato |
| Lo scanner accetta più pezzi del dovuto nella consegna | [Odoo forum 255230](https://www.odoo.com/forum/help-1/avoid-over-scanning-of-products-odoo-13-community-255230), Odoo 13, data non visibile | Al prelievo la base dice «prendi 3 di 5» e si ferma se l'articolo è un altro (97, 103); che succede se se ne scansionano di più: da decidere (proposta: avviso e quantità non oltre il richiesto) |

### 3.2 Dati persi o sbagliati

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| Dopo una ricevuta parziale (10 di 15), ricaricando la pagina la quantità attesa diventa 10 e i 5 mancanti non si possono più ricevere | [Odoo community, contributors](https://test.odoo-community.org/groups/contributors-69/odoo-v17-barcode-app-issues-12409?mode=date), Odoo 17, 17/04/2024 | L'atteso viene dall'ordine fornitore e la ricezione non lo riscrive; ogni scansione è un dato a sé, salvato sul server (requisiti di affidabilità). Da provare con un test di ricarica a metà DDT |
| Spedizioni ricevute contando i cartoni, non i pezzi contro l'ordine: mancanze, danni e varianti sbagliate emergono dopo come differenze | [Shopify Community 630676](https://community.shopify.com/t/received-the-wrong-quantity/630676), 02/06/2026 | Si conta per articolo, riconosciuto dalla fotocamera (87); differenze con la bolla al responsabile (73). In parte evitato: «× colli» (94) moltiplica un contenuto che va confermato |
| Ricevendo 66 pezzi su 72, l'ordine d'acquisto collegato risulta ricevuto per 72; il supporto Shopify lo ha registrato come comportamento inatteso | [Shopify Community 629925](https://community.shopify.com/t/bug-in-the-auto-receive-behavior-between-a-po-and-its-linked-transfer/629925), 29/05/2026 | Il carico al gestionale porta le quantità contate (61). Evitato |
| (FATTO, documentazione) In Shopify un ricevimento sbagliato si corregge modificando le quantità accettate, rifiutate o annullate | [Undo a transfer](https://help.shopify.com/manual/products/inventory/transfers/cancel-transfer/) | Correzione collegata dell'operatore a DDT aperto, del responsabile dopo (74, 81), sempre visibile nello storico |
| (Caso UFP con ARS, riferito dall'utente) scansioni perse dopo una sospensione; DDT non rintracciabile e rifatto; righe importate a mano dagli ordini | `docs/architettura.md`, «Requisiti di affidabilità»; decisione 183 | Salvataggio immediato con esito, operazioni senza doppioni, DDT sempre ritrovabile, righe dalle letture. Evitato sulla carta; da provare |

### 3.3 Sincronizzazione delle giacenze

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| L'integrazione di un WMS di un logistico scrive in Shopify la quantità «Available» invece di «On hand»; il produttore non riconosce il difetto | [Shopify Community 408716](https://community.shopify.com/t/mintsoft-wms-3pl-updating-incorrect-onhand-available-stock-levels-in-shopify/408716), 15/04/2025 – 16/09/2025 | Il connettore manda variazioni di quantità e segna le spedizioni (52), con l'API GraphQL (ricerca Shopify). Evitato sulla carta |
| Dopo l'installazione dell'app di un centro di evasione le giacenze vanno a zero, e alcune continuano a tornare a zero anche dopo averla tolta | [Shopify Community 223390](https://community.shopify.com/t/my-stock-goes-to-0-due-to-third-party-app-installed/223390), 10/06/2023 | Non dipende dalla base. Le «differenze con il sistema d'origine» sono già tra le cose da controllare (modello dei dati). Da decidere: avviso al responsabile quando Shopify cambia una giacenza che la base non ha mandato |
| Con l'integrazione Shopify le giacenze di Zoho Inventory cambiano da sole a intervalli irregolari (per esempio +14 ripetuto) | [Zoho community](https://help.zoho.com/portal/en/community/topic/locations-inventory-change-by-itself-with-shopfiy-integration), data non visibile | Come sopra; ogni scambio è registrato nella coda di uscita (54) e andrebbe in «Documenti» (§ 1.10) |
| Stocky chiude il 31/08/2026; gli ordini d'acquisto nativi di Shopify «aren't exposed through its API», l'unica uscita è il CSV; i fornitori non si esportano | [Shopify Community 637085](https://community.shopify.com/t/637085), giugno–luglio 2026 | I dati stanno sul server in sede (126). Da decidere: esportazione in file di documenti e storico |

### 3.4 Lentezza e passaggi ripetuti

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| Aprire un ordine nell'app Barcode faceva caricare tutti i 64.000 articoli, circa 50 secondi | [Odoo forum 189275](https://www.odoo.com/forum/help-1/barcode-module-poor-performance-on-get-all-products-by-barcode-odoo-14-189275), Odoo 14, data non visibile | Non ancora coperto: UFP ha fino a 35.000 articoli (5). Proposta: requisito misurabile (per esempio esito di una scansione entro un tempo fissato con il catalogo intero) e prova di carico prima della consegna. Da decidere il valore |
| Inventario lento da 70–80 righe, fino a un minuto per articolo letto | [Odoo forum 125738](https://www.odoo.com/forum/help-1/inventory-adjustment-really-slow-125738), data non visibile | Come sopra; il futuro inventario va diviso per ubicazione (§ 1.7) |
| Prelievo: scansionare ogni pezzo è troppo lento e si torna alla carta; non si può segnare «prelevato» senza scansionare ogni pezzo; ritardi tra schermate; la tastiera copre i campi; troppe scansioni senza identificativi di collo | [Acumatica community](https://community.acumatica.com/distribution-6/wms-picking-is-anyone-having-success-10986), 10/08/2022 – 13/10/2026 | Una scansione per riga con la quantità (164), «× colli» (94); tastiera e campi: da provare sul prototipo e sui telefoni veri (skill mobile-native). In parte coperto |
| (FATTO, documentazione) Dynamics SCM offre le deviazioni con valori copiati e passi confermati da soli: «Auto-submit detour steps can make it faster and easier for workers to complete detour flows» | [warehouse-app-detours](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-app-detours) | La base ha «Cerca articolo» e «Conta» sempre disponibili (160). Da decidere: tornare al punto esatto del DDT dopo una ricerca |

### 3.5 Rete e dispositivi

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| Palmari che si scollegano a intermittenza dall'app di Dynamics SCM, con nuovi accessi; telefoni ed emulatore funzionano; causa non trovata | [dynamicsuser.net](https://www.dynamicsuser.net/t/d365f-o-warehouse-mobile-app-disconnection-issue/80375), 21/03/2024 | Rete assente con operazione in attesa (23, 127), uscita dopo 30 minuti senza perdere il lavoro (80). Da provare sul palmare di UFP |
| (FATTO, documentazione) Il POS di Shopify richiede internet per ricevere i trasferimenti | [help.shopify.com](https://help.shopify.com/en/manual/sell-in-person/shopify-pos/inventory-management/fulfilling-and-receiving-transfers) | Il server è in rete interna; internet serve solo allo scambio con Shopify (54). Evitato |
| (FATTO, documentazione) In NetSuite i blocchi contro il doppio lavoro a volte non si sbloccano; uno script periodico li libera | [NetSuite](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156382533850.html) | Un ordine preso da una persona (170): il responsabile o chi pianifica lo libera (170, 175). Proposta: mostrare da quanto è preso (§ 1.9) |
| «The scanner is too fast»: il lettore manda il tasto Tab prima che la ricerca sia finita e viene scelto «Create» invece dell'articolo; servito un modulo su misura | [Odoo forum 40809](https://www.odoo.com/forum/help-1/barcode-scanning-in-v7-cannot-auto-select-bc-openerp-doesnt-have-enough-time-to-search-the-db-40809), Odoo 7, data non visibile | IPOTESI già scritta: campo sempre pronto per il grilletto (architettura). Da provare |

### 3.6 Annullare dopo la registrazione

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| «Undo Receipt» impossibile dopo che un costo accessorio è stato fatturato su quella ricevuta: «You cannot undo line 10000, because an item charge has already been invoice[d]» | [Mibuso](https://forum.mibuso.com/discussion/55357/undo-receipt-when-item-charge-has-been-posted), 19/10/2012 | Nella base la correzione dopo la chiusura è sempre possibile al responsabile (81); ma in UFP il carico è già in Ad Hoc: se Ad Hoc rifiuta la rettifica (per esempio carico già fatturato), cosa succede? Da chiedere al rivenditore |
| (FATTO, base di conoscenza SAP) Annullare una ricevuta in SAP Business One può essere bloccato: «cancel target documents first» | [SAP KBA 3779589](https://userapps.support.sap.com/sap/support/knowledge/en/3779589) | Come sopra: la rettifica è un documento nuovo, non un annullamento a cascata (74). Da verificare con Ad Hoc |

### 3.7 Spedizione

| Esperienza riferita | Fonte e data | Come la base lo evita |
|---|---|---|
| Distinte USPS scansionate dal corriere ma colli che restano «Label Created» | [ShipStation community](https://community.shipstation.com/t5/ShipStation-Features/USPS-Scan-Forms-Not-Registering-Updating-Pickup-Scans/m-p/26387), 10/12/2024 – 03/04/2025 | Non la riguarda: «Spedito» è segnato da chi consegna i colli (172), non dal tracciamento del corriere. Da decidere se importare il tracking |

### 3.8 Doppioni

| Fatto o esperienza | Fonte | Come la base lo evita |
|---|---|---|
| (FATTO) In Odoo scansionare «WHIN» crea sempre una ricevuta nuova, anche se ne esiste una uguale | [operation_types.rst](https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst) | Avviso di possibile doppione con stesso fornitore, numero e data (86); DDT aperti in elenco (Percorso). Evitato |

## 4. Tabella finale: funzione o difetto → proposta per la base

La colonna «Priorità» è una DEDUZIONE nostra (alta, media, bassa) per ciascun magazzino di prova, non una decisione.

| Funzione o difetto | Proposta per la base | Priorità UFP / Shopify (deduzione) | Decisioni collegate |
|---|---|---|---|
| DDT da più ordini del fornitore | Già così; proposta: filtro sugli ordini attesi se un fornitore ne ha molti aperti | Media / Bassa | 70, 104, 183 |
| Ricerca per articolo → ordini che lo contengono | Già scelta; mostrare per ogni ordine data, residuo e riferimento cliente | Alta / Media | 70, 183 |
| Foto della bolla all'apertura del DDT | Proposta: foto salvata con il DDT, visibile in «Documenti» | Alta / Media | 40, 73, 182 |
| Numero e data letti dalla foto | Da provare con PaddleOCR in sede su DDT veri | Media / Bassa | 86, 145 |
| Righe della bolla lette dalla foto | Solo come «quantità in bolla»; da provare per fornitore | Bassa / Bassa | 73 |
| ASN, DESADV, Peppol Despatch Advice | Punto d'estensione per file del fornitore; non nella base | Bassa / Bassa | 51 |
| Riconciliazione con la fattura differita (FatturaPA 2.1.8) | Nella specializzazione per Ad Hoc | Media / — | 61, 178 |
| Abbinamenti imparati (codice del fornitore) | Già così (71); proporre anche dall'abbinamento a mano per articolo | Alta / Media | 71, 92, 183 |
| Tolleranza sulle eccedenze | Da decidere: soglia per magazzino sotto cui non si disturba il responsabile | Bassa / Bassa | 32 |
| Esito «danneggiata» e scarto | Da decidere: esito di riga al ricevimento e scarto dalla scheda articolo | Media / Media | 45, 74 |
| Resi da cliente | Da decidere, ticket a parte | Media / Alta | 160 |
| Resi al fornitore con DDT di reso | Da decidere, ticket a parte; in UFP chi emette il DDT di reso (Ad Hoc?) | Media / Media | 45, 114, 160 |
| Inventario ciclico e completo | Futuro ticket: conta cieca di serie, conte richieste, due fasi, divisione per persona | Media / Media | 77, 160 |
| Etichette e distinta del corriere | Da chiedere al rivenditore (UFP); per Shopify da decidere | Media / Media | 172, 174, domande 21–22 |
| Elenchi in sospeso per sezione | Proposta: in corso (miei, di altri), fermi con motivo, vecchi; dal più vecchio | Alta / Alta | 161, 177, 181 |
| «Documenti»: per documento e registro | Proposta: due viste dello stesso storico, con filtri; visibilità e conservazione da decidere | Alta / Alta | 27, 74, 86, 182 |
| Esportazione dei dati | Da decidere: esportazione in file di documenti e storico | Bassa / Media | 182 |
| Regola «Annulla» e «Conferma» | Proposta: annulla per le azioni frequenti, riepilogo con conseguenze per le chiusure, responsabile per le irreversibili | Alta / Alta | 74, 81, 82, 99, 172, 180 |
| Nessun «riempi con l'atteso» | Proposta: non introdurlo; per più colli uguali resta «× colli» | Alta / Alta | 94, 183 |
| Ricarica a metà DDT non perde nulla | Test da aggiungere alle prove | Alta / Alta | 23, 68, 127 |
| Lentezza con catalogo grande | Proposta: requisito di tempo per scansione con 35.000 articoli e prova di carico | Alta / Media | 5, 18 |
| Rete instabile sui palmari | Già coperto; prova sui palmari veri | Alta / Media | 23, 119, 127 |
| Suono e vibrazione alla scansione | Da decidere; mai solo suono | Media / Media | 87, 99 |
| Ordine «preso» e mai finito | Proposta: mostrare da quanto è preso; liberarlo come già deciso | Media / Media | 170, 175 |
| Giacenze Shopify cambiate da altre app | Da decidere: avviso al responsabile per variazioni non mandate dalla base | — / Alta | 49, 52, 54 |
| Rettifica rifiutata dal gestionale | Da chiedere al rivenditore: cosa fa Ad Hoc con una rettifica su un carico già fatturato | Media / — | 61, 81 |
| Tornare al punto esatto dopo una ricerca | Da decidere nel ticket «Completezza del percorso» | Media / Media | 160 |
| Giri su più ordini (batch, cluster, ondate) | Già estensione possibile | Bassa / Media | 164 |
| Regole di messa a posto per categoria | Estensione possibile | Bassa / Bassa | 75 |

## 5. Domande aperte per l'utente o il rivenditore

1. Quanti ordini aperti ha di solito un fornitore di UFP, e il DDT del fornitore stampa il numero d'ordine?
2. Qualche fornitore di UFP manda un avviso di spedizione elettronico (EDI, Peppol, file) o etichette SSCC sui pallet?
3. Si possono avere 5–10 DDT veri (con i dati dei clienti coperti) per provare la lettura di numero, data e righe?
4. In UFP chi emette il DDT di reso al fornitore e chi stampa etichette e distinte BRT/GLS?
5. Cosa fa Ad Hoc se arriva una rettifica su un carico già fatturato?
6. Nel magazzino Shopify arrivano resi dai clienti? Come si gestiscono oggi sulla carta?

## Fonti

Pagine e file aperti il 18/11/2026. Tra parentesi la data della pagina quando c'è.

Odoo (sorgenti della documentazione, ramo 19.0, scaricati il 18/11/2026; versione online in
https://www.odoo.com/documentation/19.0/)
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/operation_types.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/receipts_deliveries.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/adjustments.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/operations/gs1_nomenclature.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/serial_numbers_lots.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/barcode/setup/device_troubleshooting.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/putaway.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/picking_methods/cluster.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/picking_methods/wave.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/multipack.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/print_on_validation.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/dispatch.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/shipping_receiving/setup_configuration/starshipit_shipping.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/operation_type.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/reception_report.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/cycle_counts.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/scrap_inventory.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/moves_history.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/dashboards.rst
- https://github.com/odoo/documentation/blob/19.0/content/applications/inventory_and_mrp/purchase/advanced/edi.rst
- https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/shop/sales_order.rst
- https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/shop/ship_later.rst
- https://github.com/odoo/documentation/blob/18.0/content/applications/sales/point_of_sale/employee_login.rst

Odoo, forum e community (esperienze riferite)
- https://www.odoo.com/forum/help-1/barcode-is-it-possible-to-prevent-users-from-validating-without-scanning-240334
- https://www.odoo.com/forum/help-1/accidentally-clicked-no-back-order-how-can-i-undo-it-165345
- https://www.odoo.com/forum/help-1/avoid-over-scanning-of-products-odoo-13-community-255230
- https://www.odoo.com/forum/help-1/barcode-module-poor-performance-on-get-all-products-by-barcode-odoo-14-189275
- https://www.odoo.com/forum/help-1/inventory-adjustment-really-slow-125738
- https://test.odoo-community.org/groups/contributors-69/odoo-v17-barcode-app-issues-12409?mode=date (17/04/2024)
- https://www.odoo.com/forum/help-1/barcode-scanning-in-v7-cannot-auto-select-bc-openerp-doesnt-have-enough-time-to-search-the-db-40809


Microsoft Dynamics 365 Business Central (sorgenti di Microsoft Learn, `MicrosoftDocs/dynamics365smb-docs`, ramo main;
versione online in https://learn.microsoft.com/dynamics365/business-central/)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-receive-items.md (27/01/2025)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/finance-how-reverse-journal-posting.md (07/04/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/purchasing-how-process-purchase-returns-cancellations.md (16/11/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/purchasing-how-record-purchases.md
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/map-edocuments-with-copilot.md (02/10/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/payables-agent.md (03/11/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/inventory-how-count-inventory-with-documents.md (07/04/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/warehouse-how-to-find-your-warehouse-assignments.md (24/06/2021)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/across-log-changes.md (17/06/2026)
- https://github.com/MicrosoftDocs/dynamics365smb-docs/blob/main/business-central/includes/barcode-mobile-app.md (02/10/2023)
- https://forum.mibuso.com/discussion/55357/undo-receipt-when-item-charge-has-been-posted (19/10/2012)

Microsoft Dynamics 365 Supply Chain Management
- https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/inbound-load-handling (15/06/2026)
- https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/install-configure-warehouse-management-app (29/09/2026)
- https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-app-detours (08/04/2026)
- https://www.dynamicsuser.net/t/d365f-o-warehouse-mobile-app-disconnection-issue/80375 (21/03/2024)

SAP
- https://learning.sap.com/courses/managing-logistics-in-sap-business-one/solving-issues-in-purchasing
- https://help.sap.com/saphelp_ewm94/helpdata/en/4f/436d1b65581242e10000000a42189b/content.htm
- https://userapps.support.sap.com/sap/support/knowledge/en/3779589 (anteprima pubblica; il testo completo richiede l'accesso)

Oracle
- https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1541435923.html
- https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156382533850.html
- https://docs.oracle.com/en/cloud/saas/warehouse-management/25d/owmol/receive-by-asn.html

Shopify
- https://help.shopify.com/en/manual/products/inventory/purchase-orders
- https://help.shopify.com/en/manual/products/inventory/transfers
- https://help.shopify.com/en/manual/inventory-and-locations/inventory-transfers/receiving-and-managing-transfers
- https://help.shopify.com/manual/products/inventory/transfers/cancel-transfer/
- https://help.shopify.com/en/manual/sell-in-person/shopify-pos/inventory-management/fulfilling-and-receiving-transfers
- https://community.shopify.com/t/637085 (giugno–luglio 2026)
- https://community.shopify.com/t/received-the-wrong-quantity/630676 (02/06/2026)
- https://community.shopify.com/t/bug-in-the-auto-receive-behavior-between-a-po-and-its-linked-transfer/629925 (29/05/2026)
- https://community.shopify.com/t/mintsoft-wms-3pl-updating-incorrect-onhand-available-stock-levels-in-shopify/408716 (15/04/2025)
- https://community.shopify.com/t/my-stock-goes-to-0-due-to-third-party-app-installed/223390 (10/06/2023)

Altri gestionali e spedizioni
- https://www.zoho.com/inventory/help/purchase-orders/purchase-receive.html
- https://help.zoho.com/portal/en/community/topic/locations-inventory-change-by-itself-with-shopfiy-integration
- https://www.inflowinventory.com/support/cloud/how-do-i-partially-receive-products-on-a-purchase-order-in-inflow-cloud
- https://support.katanamrp.com/en/articles/5944995-receiving-a-purchase-order-po (15/07/2026)
- https://docs.shipstation.com/manifests-scanforms
- https://community.shipstation.com/t5/ShipStation-Features/USPS-Scan-Forms-Not-Registering-Updating-Pickup-Scans/m-p/26387 (10/12/2024)
- https://community.acumatica.com/distribution-6/wms-picking-is-anyone-having-success-10986 (10/08/2022 – 13/10/2026)
- https://www.teamsystem.com/magazine/gestione-impresa-e-partita-iva/ddt-reso-logistica-inversa/ (14/10/2026, fonte secondaria)
- https://www.danea.it/public/gestione-magazzino-guida.pdf (scaricato, testo non estraibile: non citato)

Norme, standard e servizi documentali
- https://www.normattiva.it/eli/id/1996/09/12/096G0487/CONSOLIDATED/20130101 (DPR 472/1996, testo vigente al 01/01/2013)
- https://peppol.agid.gov.it/en/news/result-ddt-consultation/ (20/04/2020)
- https://docs.peppol.eu/poacc/upgrade-3/profiles/30-despatchadvice/
- https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en
- https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/ (documentazione valida dal 01/04/2025)
- https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.4/RappresentazioneTabellareFattOrdinaria-1.pdf
- https://gs1it.org/files/sharing/1591179307/1615/ottimizza-il-processo-consegna-con-il-desadv.pdf (maggio 2020)
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview (05/06/2026)
- https://docs.cloud.google.com/document-ai/docs/processors-list
- https://docs.mindee.com/v1/off-the-shelf-products/delivery-note
- https://www.paddleocr.ai/latest/en/index.html

Pagine provate e non aperte: G2, Capterra, TrustRadius e Software Advice (403); Reddit (non raggiungibile); pagina NSO
della Ragioneria Generale dello Stato (pagina non disponibile); linee guida NSO 2025 su osservatoriocpi.unicatt.it
(404); https://www.gs1.org/standards/barcodes/application-identifiers/00 (403); una discussione della community Oracle
NetSuite sui doppi ricevimenti (503).
