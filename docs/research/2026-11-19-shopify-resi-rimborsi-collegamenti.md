# Shopify: resi, rimborsi, comunicazione con il cliente e collegamenti

Data: 19/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina aperta il 19/11/2026). **DEDUZIONE** = conclusione
nostra a partire dai fatti. **IPOTESI** = da verificare con una prova su un negozio di sviluppo o con un consulente.
"Non verificato" = viene dalla memoria o da fonti non ufficiali (forum, schede di marketing), senza conferma su una
pagina ufficiale aperta. Nulla di questo file è un parere legale: le parti di legge riportano il testo delle norme e le
nostre deduzioni, da far confermare a chi segue la parte legale del negozio.

Ricerca precedente, da non ripetere: `docs/research/2026-11-15-shopify-ordini-evasione-giacenze.md` (ordini, evasione,
giacenze, webhook, autenticazione, limiti, versioni). Aggiornamenti a quella ricerca: in fondo alla sezione 4.

## Domanda

Nel magazzino che vende solo con Shopify i resi dei clienti sono tutti a mano (decisione 321): arrivano le scatole, si
guardano le etichette, si decide come rimborsare, una persona si accorda con il cliente per WhatsApp o email tra credito
del negozio e rimborso sul metodo di pagamento originale. Con il modello di traffico della base (il server in sede
interroga Shopify ogni 5 minuti, niente webhook in entrata, decisione 54; app creata dall'organizzazione del negozio nel
Dev Dashboard con client credentials, decisione 53) e con quanto già deciso (210–212: «Ricevi reso» parte dall'ordine
spedito, esito per pezzo scritto con `reverseFulfillmentOrderDispose`, rimborso, credito e cambio restano a una persona su
Shopify), cosa si può fare in automatico per:

1. i resi su Shopify (come nascono, regole, stati, etichette, cambio, API, permessi, cosa resta solo nel pannello);
2. i rimborsi (metodo originale, credito del negozio, carte regalo, limiti per metodo di pagamento) e la legge
   italiana/UE (recesso e garanzia);
3. la comunicazione con il cliente (notifiche Shopify, email, Flow, WhatsApp Business Platform);
4. tutto ciò a cui ci si può collegare da Shopify solo in uscita, a intervalli;
5. le app per i resi già esistenti;
6. le due idee dell'utente (A: scelta del rimborso sul sito; B: casella email dei resi letta da un'automazione con un LLM).

## Sintesi

1. **Versione API: la stabile corrente è ancora la 2026-10** (accessibile fino al 16/10/2027); 2027-01 è release
   candidate. (FATTO, [Versioning](https://shopify.dev/docs/api/usage/versioning))
2. **Un reso Shopify nasce in tre modi:** richiesta del cliente dal sito (resi self-service, solo con i **nuovi** account
   cliente), reso creato dal negozio nel pannello, reso creato da un'app via API (`returnRequest` = da approvare,
   `returnCreate` = già approvato). Si rendono solo pezzi **evasi**. (FATTO)
3. **Stati:** reso `REQUESTED` → `OPEN` (approvato) o `DECLINED`; poi `CLOSED` o `CANCELED`. L'approvazione crea un
   *reverse fulfillment order* (`OPEN`/`CLOSED`/`CANCELED`) su cui si registra l'esito per pezzo (`RESTOCKED`,
   `NOT_RESTOCKED`, `MISSING`, `PROCESSING_REQUIRED`). Con `RESTOCKED` "la quantità disponibile aumenta"; ogni unità si
   può "disporre" **una sola volta** e la disposizione non si cambia. Questo conferma la decisione 212. (FATTO)
4. **Interrogare a intervalli si può**, ma non esiste una query `returns` di primo livello: si cercano gli ordini con il
   filtro `return_status:return_requested` (o `in_progress`) e se ne leggono i `returns`. (FATTO sul filtro; FATTO che la
   pagina `queries/returns` non esiste nella 2026-10)
5. **Trovare un reso dal tracking dell'etichetta di reso:** nessun filtro di ricerca per numero di tracking negli
   ordini; il tracking del reso è leggibile solo dentro il reso (`ReverseDelivery`). Shopify dice anche che il reso
   non contiene lo stato della spedizione (in viaggio, consegnato). Quindi il riconoscimento della scatola dal barcode
   va fatto da **un nostro indice** dei tracking dei resi aperti, riletto a ogni giro. (FATTO sui limiti; DEDUZIONE
   sulla soluzione)
6. **Etichette di reso di Shopify Shipping: solo Stati Uniti e Canada.** In Italia Shopify Shipping esiste per le
   spedizioni in uscita (BRT e Poste Italiane solo nazionali, DHL Express), ma l'etichetta di reso dal pannello no: si
   carica un'etichetta propria (PDF/PNG/JPEG o URL, con tracking) o si crea il reso senza etichetta. Da API:
   `reverseDeliveryCreateWithShipping` con file e tracking; attenzione, **avvisa il cliente in automatico** (`notifyCustomer`
   vale `true` di serie). (FATTO)
7. **Il cliente sul sito non sceglie tra rimborso, credito o cambio:** la richiesta self-service raccoglie pezzi,
   quantità, motivo e una nota di 300 caratteri; il metodo di rimborso lo sceglie chi elabora il reso (Metodo originale,
   Credito del negozio, o entrambi). (FATTO sui campi; DEDUZIONE dall'assenza del campo nelle pagine lette)
8. **Un'app può eseguire rimborsi:** `returnProcess` (consigliata dalla 2025-07) rimborsa sul metodo originale e/o in
   credito del negozio (`refundMethods.storeCreditRefund`, con scadenza facoltativa) e registra l'esito per pezzo;
   `refundCreate` rimborsa anche senza reso (idempotenza obbligatoria dalla 2026-04). Il credito del negozio richiede i
   **nuovi account cliente** (non c'è sui vecchi) ed è limitato a meno di 15.000 USD per account. (FATTO)
9. **Limiti per metodo di pagamento:** Shopify Payments (attivo in Italia) rimborsa "di solito fino a 120 giorni";
   PayPal entro 180 giorni dal pagamento; contrassegno e bonifico (pagamenti manuali) non passano da Shopify: il rimborso
   si fa fuori e su Shopify si **registra** soltanto. (FATTO)
10. **Legge (recesso, contratti a distanza):** 14 giorni per recedere dalla consegna; rimborso entro 14 giorni da quando
    il negozio è **informato** del recesso, con lo stesso mezzo di pagamento "salvo che il consumatore abbia espressamente
    convenuto altrimenti" e senza costi per lui; il negozio può trattenere il rimborso finché non riceve la merce o la
    prova della spedizione. Dal 19/6/2026 (contratti successivi) il sito deve avere una **funzione di recesso online**
    («recedere dal contratto qui», «conferma recesso», avviso di ricevimento su supporto durevole). Il recesso si può
    comunicare anche con "qualsiasi altra dichiarazione esplicita", quindi **anche per email**. La garanzia legale
    (difetto, 2 anni) è un'altra cosa, con altri rimedi. (FATTO, Codice del consumo artt. 52–59, 54-bis, 133, 135-bis)
11. **Credito del negozio al posto del rimborso:** per un recesso si può dare solo con accordo **espresso** del cliente;
    l'accordo di oggi per WhatsApp o email va conservato. (DEDUZIONE dall'art. 56; da confermare con chi segue la parte
    legale)
12. **Comunicazione:** Shopify manda da sé le notifiche dei resi (richiesta ricevuta, approvata, rifiutata, etichetta,
    rimborso, credito), modificabili e traducibili; un'app non ha una mutation per mandare un'email libera al cliente
    (solo email d'invito o di fattura); Flow manda email interne solo allo staff. La mail dal programma (SMTP o API della
    casella aziendale) resta la via per i testi liberi (già decisa per i fornitori, 223 e 311). (FATTO; DEDUZIONE)
13. **WhatsApp Business Platform (Cloud API):** si paga per messaggio consegnato (dal 1/7/2025); fuori dalla finestra di
    24 ore dall'ultimo messaggio del cliente si possono mandare solo **modelli approvati**; serve l'opt-in del cliente;
    dal 1/10/2026 sono a pagamento anche i messaggi di servizio oltre 1.000 al mese per numero. **I messaggi in arrivo
    arrivano solo con un webhook HTTPS pubblico con certificato valido**: non compatibile con il server in sede così
    com'è (decisione 54). Le tariffe per l'Italia non si leggono nel testo delle pagine (sono in un selettore e in file
    CSV non raggiungibili). (FATTO; DEDUZIONE sul server)
14. **App per i resi:** molte (AfterShip, Loop, ReturnGO, Return Prime, Rich Returns, Redo, easyReturns, Sendcloud,
    Outvio, Qapla'); quasi nessuna nomina i corrieri italiani BRT e Poste Italiane per le etichette di reso; poche hanno
    l'italiano. Non tutte dicono se scrivono i resi di Shopify; AfterShip sì (usa la Return API). Se un'app e il nostro
    programma registrano entrambi l'esito, conta chi arriva primo: Shopify accetta una sola disposizione per unità.
    (FATTO sulle schede; DEDUZIONE sul rischio)
15. **Le due idee dell'utente:** (A) far scegliere al cliente il rimborso sul sito richiede un'estensione dell'account
    cliente (nuovi account), che può salvare la scelta in un metafield dell'ordine leggibile dal nostro server a
    intervalli; (B) leggere una casella resi a intervalli (IMAP con OAuth, Microsoft Graph, Gmail API) è solo traffico in
    uscita, compatibile con la 54; n8n self-hosted è permesso per uso interno, ma nel nostro **prodotto** sarebbe zona
    grigia di licenza; un LLM in cloud è un responsabile del trattamento (art. 28 GDPR) e le mail dei clienti sono un
    canale di istruzioni nascoste: la conferma di una persona prima di scrivere su Shopify è necessaria. (FATTO;
    DEDUZIONE)

## 1. Resi su Shopify

### 1.1 Come nasce un reso

#### FATTI

- Dal pannello: Ordini → ordine → **Return** (o *More actions* → *Return* se ci sono pezzi non evasi); quantità, **motivo
  del reso** per pezzo, eventuali costo di rimessa a magazzino (*restocking fee*) e spese di reso, eventuali articoli di
  cambio, poi l'opzione di spedizione del reso e *Create return*. Serve essere proprietario o avere il permesso
  **Return**.
  [Creating returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns)
- Dal sito (self-service): il cliente invia la richiesta dalla pagina di stato dell'ordine nel suo account cliente;
  "Legacy customer accounts don't display return or cancellation options". Può aprire l'ordine dal link nell'email
  senza accedere, ma per inviare la richiesta deve accedere con un codice di 6 cifre mandato per email ("A password isn't
  required"). Si rendono solo pezzi evasi (anche in viaggio); si annullano solo pezzi non spediti.
  [Self-serve setup](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup)
- Si attivano in Impostazioni → Account cliente (sezione *Order actions* → *Return*/*Cancel*, oppure *Self-serve returns
  and cancellations*). Sui piani Advanced e Plus si possono attivare per mercato; sugli altri piani solo per tutti i
  mercati. Le richieste si approvano o rifiutano nel pannello; la pagina non descrive un'approvazione automatica.
  [Self-serve setup](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup),
  [Self-serve returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns)
- Da un'app: `returnRequest` crea un reso `REQUESTED` da approvare; `returnCreate` crea un reso già `OPEN` "quando
  l'approvazione avviene fuori da Shopify"; serve almeno una riga evasa e non rimborsata. Le app di terzi possono anche
  costruire un portale con la Customer Account API (`orderRequestReturn`, versione 2025-04 o successiva).
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management),
  [Build self-serve returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-self-serve-returns)
- Limiti generali: "You can only return items that have been fulfilled"; un reso su un ordine archiviato lo de-archivia;
  "You can manage returns only using the GraphQL Admin API" (niente REST).
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps)
- Resi in negozio (POS): le regole di reso del POS richiedono Shopify POS Pro.
  [Return rules](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules)
  Non approfondito: il magazzino vende solo online.

#### DEDUZIONI

- Il caso di oggi (cliente che scrive per WhatsApp o email, scatola che arriva) è un reso **creato dal negozio**: oggi
  nessuno lo crea su Shopify, quindi la lista "resi aperti sul sito" della decisione 210 oggi sarebbe vuota. Perché il
  programma veda un reso, qualcuno (cliente dal sito, persona nel pannello, o il programma con `returnCreate`) deve
  crearlo.
- I resi self-service richiedono i **nuovi account cliente**: è un'impostazione del negozio da verificare (domanda per
  l'utente). La stessa condizione vale per il credito del negozio (sezione 2) e per le estensioni dell'idea A (sezione 6).

### 1.2 Regole di reso, motivi, costi

#### FATTI

- Regole di reso: finestra (Nessun reso, 14, 30, 90 giorni, illimitata o giorni a scelta), che parte dalla consegna di
  ogni pezzo o dell'ultimo pezzo; eccezioni per collezioni, prodotti o varianti (vale la finestra più breve); spese di
  reso gratuite, a forfait (una volta per reso) o etichetta a carico del cliente; costo di rimessa a magazzino in
  percentuale, che "aren't automatically deducted from refunds"; articoli in **vendita finale** non rendibili; regole per
  mercato; le modifiche valgono solo per gli ordini futuri. Per i venditori UE: finestra di almeno 14 giorni dalla
  consegna dell'ultimo pezzo.
  [Return rules](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules)
- Dalla 2026-10 le regole sono leggibili da API: `returnPolicyProfiles` (scope `read_legal_policies`) con
  `returnRules.canAcceptReturns`, `returnWindowDays`, `returnWindowStartingFrom`, `extendWindowToBusinessDay`.
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10),
  [ReturnPolicyProfile](https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnPolicyProfile),
  [ReturnPoliciesReturnRules](https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnPoliciesReturnRules)
- **Nuovo modello dei motivi (2026-01):** `ReturnReasonDefinition` con `handle` stabile (es. "arrived-late", "quality")
  e `name` tradotto nella lingua richiesta; Shopify suggerisce un sottoinsieme per categoria di prodotto, ma via API si
  può usare qualsiasi motivo della libreria (`returnReasonDefinitions`, scope `read_returns`). Il vecchio enum
  `returnReason` (es. `DEFECTIVE`, `UNWANTED`, `WRONG_ITEM`) è **deprecato**. Sulla riga del reso restano
  `returnReasonNote` (255 caratteri) e `customerNote` (300 caratteri).
  [Release notes 2026-01](https://shopify.dev/changelog/release-notes/2026-01),
  [ReturnReasonDefinition](https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnReasonDefinition),
  [returnReasonDefinitions](https://shopify.dev/docs/api/admin-graphql/latest/queries/returnReasonDefinitions),
  [ReturnLineItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnLineItem),
  [ReturnReason](https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnReason)
- Rifiuto: `returnDeclineRequest` richiede un motivo tra `FINAL_SALE`, `RETURN_PERIOD_ENDED`, `OTHER`; è permanente.
  [ReturnDeclineReason](https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnDeclineReason),
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management)
- Spese: `returnShippingFee` sul reso, `restockingFee` in percentuale per riga; dalla 2026-10 l'imposta sulla spesa di
  reso è leggibile (`taxAmountSet`, `finalizedTaxAmountSet`).
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management),
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)

#### DEDUZIONI

- Il motivo scritto dal cliente (o dalla persona) è un dato utile per «Ricevi reso»: un motivo tipo «difettoso» o
  «articolo sbagliato» fa pensare alla garanzia o a un nostro errore di spedizione, non al recesso (sezione 2.3), e
  cambia chi paga la spedizione di ritorno.
- Il costo di rimessa a magazzino su un **recesso** va maneggiato con cautela: l'art. 56 rende nulla ogni clausola che
  limiti il rimborso, e il consumatore risponde solo della diminuzione di valore per manipolazione oltre il necessario
  (art. 57). Da far valutare a chi segue la parte legale prima di attivarlo. (DEDUZIONE)

### 1.3 Stati del reso e del reverse fulfillment order

#### FATTI

- `ReturnStatus`: `REQUESTED`, `OPEN`, `DECLINED`, `CLOSED`, `CANCELED`. `returnApproveRequest` porta a `OPEN` e crea il
  reverse fulfillment order; approvazione e rifiuto sono permanenti; un reso `REQUESTED` non si annulla, si approva o si
  rifiuta. `returnProcess` chiude il reso quando tutti i pezzi sono elaborati e c'è la decisione di rimessa a magazzino;
  `returnClose` lo chiude in ogni momento; `returnReopen` riapre un reso chiuso; `returnCancel` solo su resi `OPEN` non
  rimborsati, senza disposizioni e senza etichetta Shopify Shipping.
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps),
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management),
  [ReturnStatus](https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnStatus)
- Stato aggregato sull'ordine (`Order.returnStatus`, filtro `return_status` della query `orders`): `RETURN_REQUESTED`,
  `IN_PROGRESS`, `INSPECTION_COMPLETE`, `RETURNED`, `RETURN_FAILED`, `NO_RETURN`.
  [OrderReturnStatus](https://shopify.dev/docs/api/admin-graphql/latest/enums/OrderReturnStatus),
  [orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)
- `ReverseFulfillmentOrderStatus`: `OPEN`, `CLOSED`, `CANCELED`. Può esserci più di un reverse fulfillment order per reso
  nella stessa location.
  [ReverseFulfillmentOrderStatus](https://shopify.dev/docs/api/admin-graphql/latest/enums/ReverseFulfillmentOrderStatus),
  [Manage reverse fulfillment orders](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-fulfillment-orders)
- Esiti per pezzo (`reverseFulfillmentOrderDispose`, scope `write_returns`): `RESTOCKED` (richiede `locationId`; "The
  quantity of available inventory is incremented, and the item can't be returned again"), `NOT_RESTOCKED`, `MISSING`,
  `PROCESSING_REQUIRED`. "You can only dispose reverse fulfillment orders once on every unit of each item"; "After a
  disposition is made, your app can't update the disposition". Il vecchio `reverseDeliveryDispose` non esiste più nelle
  versioni supportate.
  [ReverseFulfillmentOrderDispositionType](https://shopify.dev/docs/api/admin-graphql/latest/enums/ReverseFulfillmentOrderDispositionType),
  [ReverseFulfillmentOrderDisposeInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReverseFulfillmentOrderDisposeInput),
  [Manage reverse fulfillment orders](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-fulfillment-orders),
  [Manage reverse deliveries](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-deliveries)
- Nel pannello, «Process return» fa scegliere per pezzo *Restock at* una location; il reso si chiude da solo quando ogni
  pezzo è elaborato e rimesso a magazzino; non si tolgono dal reso pezzi già rimborsati o rimessi.
  [Processing returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns)
- Dal 2025-07 l'elaborazione (`returnProcess`) è parte del ciclo del reso: conferma i pezzi, rilascia i cambi e aggiorna i
  rapporti finanziari; Shopify chiede alle app di passare a `returnProcess`.
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps)

#### DEDUZIONI

- La decisione 212 è coerente con la documentazione: `RESTOCKED` aumenta il disponibile, una volta sola per unità, quindi
  non va mandata in più una variazione di giacenza.
- Dopo il nostro `reverseFulfillmentOrderDispose` il reso resta **aperto** finché qualcuno non lo elabora (rimborso o
  `returnProcess`) o lo chiude. La persona che poi rimborsa nel pannello vedrà i pezzi già disposti; che il pannello non
  proponga di rimetterli a magazzino una seconda volta è molto probabile (una disposizione per unità) ma va provato.
  (IPOTESI)
- `PROCESSING_REQUIRED` corrisponde al nostro «Da controllare» (211): quando il responsabile decide, servirà una seconda
  scrittura. Non è chiaro se un'unità già `PROCESSING_REQUIRED` accetti poi `RESTOCKED`, visto che "una disposizione per
  unità" e "non si aggiorna". (IPOTESI da provare: potrebbe convenire **non** scrivere nulla finché il responsabile non
  decide)

### 1.4 Etichette di reso e tracking

#### FATTI

- Nel pannello: "Create a return label in Shopify" è disponibile solo con una location nello stesso paese del cliente e
  se il paese è Stati Uniti o Canada; altrimenti "Upload a return label" (PDF, PNG, JPEG o URL, con tracking e corriere
  facoltativi) o "No shipping required".
  [Creating returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns)
- Shopify Shipping in Italia, per le spedizioni: BRT solo nazionale, niente ritiri, nome del negozio massimo 25 caratteri
  e via massimo 35; Poste Italiane solo nazionale, con cinque servizi; DHL Express per l'estero (pagina DHL citata da
  una ricerca, non aperta).
  [BRT](https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/shipping-labels/shipping-carriers/brt),
  [Poste Italiane](https://help.shopify.com/en/manual/fulfillment/shopify-shipping/shipping-carriers/poste-italiane),
  [Elenco corrieri](https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/shipping-labels/shipping-carriers)
- Da API: `reverseDeliveryCreateWithShipping` (scope `write_returns`) crea la spedizione di ritorno con file
  dell'etichetta (URL, anche da `stagedUploadsCreate`) e tracking (`number`, `url`; l'URL va dato se il corriere non è
  supportato da Shopify); `notifyCustomer` **vale `true` di serie** e manda al cliente le istruzioni se l'ordine ha
  un'email. `reverseDeliveryShippingUpdate` aggiorna etichetta e tracking.
  [reverseDeliveryCreateWithShipping](https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseDeliveryCreateWithShipping),
  [reverseDeliveryShippingUpdate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseDeliveryShippingUpdate),
  [ReverseDeliveryTrackingInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReverseDeliveryTrackingInput)
- "A reverse delivery doesn't include package tracking information. For example, an app can't query if an item is in
  transit, if a shipping label has been scanned, or if the item has been delivered". Più spedizioni di ritorno per uno
  stesso reso sono possibili.
  [Manage reverse deliveries](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-deliveries)
- La query `orders` non ha un filtro per numero di tracking; i filtri disponibili includono `name`, `email`,
  `return_status`, `updated_at`, `sku`, `tag`, `confirmation_number`, `payment_id` e altri (elenco nella pagina).
  [orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)
- Acquisto di etichette Shopify Shipping da API (nuovo, 2026-07): `shippingLabelPurchase`, asincrono, per **fulfillment
  order** (spedizioni in uscita), con `write_orders` + scope dei fulfillment order + permesso utente
  `buy_shipping_labels`; FedEx non supportato; il negozio deve aver accettato i termini di Shopify Shipping.
  [shippingLabelPurchase](https://shopify.dev/docs/api/admin-graphql/latest/mutations/shippingLabelPurchase),
  [Release notes 2026-07](https://shopify.dev/changelog/release-notes/2026-07)

#### DEDUZIONI

- In Italia l'etichetta di reso arriva da fuori Shopify: contratto con il corriere, app di spedizione, o il cliente spedisce
  da sé. Il programma può caricarla con `reverseDeliveryCreateWithShipping` (o una persona nel pannello). Se la carica il
  programma, `notifyCustomer` va scelto apposta: lasciato di serie manda un'email al cliente.
- **Riconoscere la scatola dal barcode:** il tracking letto sull'etichetta di reso va confrontato con un **indice nostro**
  dei tracking delle spedizioni di ritorno dei resi aperti (letti a ogni giro dai `returns` degli ordini con
  `return_status` aperto). Se il cliente spedisce da sé e nessuno registra il tracking, la scatola si riconosce solo da
  altro (nome, numero d'ordine scritto, contenuto), come oggi.
- `shippingLabelPurchase` richiede un permesso **dell'utente** (`buy_shipping_labels`); con il client credentials non c'è
  un utente collegato. Come Shopify applichi i permessi utente a un token senza utente non è scritto nelle pagine lette.
  (IPOTESI da provare; vale anche per `returnRefund`, che chiede `refund_orders`)

### 1.5 Cambio (exchange)

#### FATTI

- `exchangeLineItems` (variante e quantità) in `returnCreate`/`returnCalculate`; i pezzi di cambio creano fulfillment
  order `ON_HOLD` con motivo `AWAITING_RETURN_ITEMS`, rilasciati da `returnProcess`. Dalla 2026-10 `ExchangeLineItem` ha
  `productId`, `title`, `variantSku`, `variantTitle`.
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management),
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)
- Nel pannello: niente articoli personalizzati come cambio; niente cambi su ordini con dazi; la giacenza del cambio "isn't
  reserved until you process the return"; se il cliente deve una differenza, paga dopo l'elaborazione o con fattura.
  [Creating returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns)

#### DEDUZIONI

- Un cambio diventa per noi un **nuovo fulfillment order** in attesa: entra nell'assegnazione dal più vecchio (16) solo
  quando Shopify lo rilascia. La data da usare per l'ordinamento (quella dell'ordine originale o quella del rilascio) è
  una scelta da fare.

### 1.6 API principali e interrogazione a intervalli

#### FATTI

- Query: `returnableFulfillments(orderId:)` (pezzi rendibili), `return(id:)`, `reverseFulfillmentOrder(id:)`,
  `reverseDelivery(id:)`, `returnReasonDefinitions`; `Order.returns` (connessione) e `Order.returnStatus`. Campi del
  `Return`: `name`, `status`, `createdAt`, `requestApprovedAt`, `closedAt`, `order`, `returnLineItems`,
  `exchangeLineItems`, `reverseFulfillmentOrders`, `refunds`, `transactions` (dalla 2026-01), `returnShippingFees`,
  `staffMember`, `suggestedFinancialOutcome`, `totalQuantity`, `decline`.
  [Return](https://shopify.dev/docs/api/admin-graphql/latest/objects/Return),
  [Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order),
  [returnableFulfillments](https://shopify.dev/docs/api/admin-graphql/latest/queries/returnableFulfillments)
- La pagina `queries/returns` non esiste nella 2026-10 (la documentazione risponde "Page not found"): non c'è una lista
  dei resi di primo livello.
- Filtri della query `orders` utili: `return_status:return_requested`, `return_status:in_progress`, `updated_at:>…`.
  [orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)
- Mutation: `returnRequest`, `returnApproveRequest`, `returnDeclineRequest`, `returnCreate`, `returnProcess`,
  `returnClose`, `returnReopen`, `returnCancel`, `removeFromReturn`, `reverseDeliveryCreateWithShipping`,
  `reverseDeliveryShippingUpdate`, `reverseFulfillmentOrderDispose`. `returnRefund` è deprecata ("Use returnProcess").
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps),
  [returnRefund](https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRefund)
- Webhook dei resi (non usabili da noi senza indirizzo pubblico): `returns/request`, `returns/approve`, `returns/decline`,
  `returns/process`, `returns/close`, `returns/reopen`, `returns/cancel`, `returns/update`, `refunds/create`,
  `reverse_fulfillment_orders/dispose`, `reverse_deliveries/attach_deliverable`.
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps)

#### DEDUZIONI

- Giro ogni 5 minuti per i resi: `orders(query: "return_status:return_requested OR return_status:in_progress")` più
  `updated_at:>ultimo_giro` per accorgersi di chiusure e rimborsi; per ogni ordine `returns` con righe, reverse
  fulfillment order, spedizioni di ritorno (tracking) e rimborsi. Che la creazione o la modifica di un reso aggiorni
  `Order.updatedAt` non è scritto: senza questa certezza il giro deve rileggere tutti gli ordini con reso aperto, non
  solo quelli cambiati. (IPOTESI da provare)
- I resi contano anche per l'assegnazione: un ordine con reso aperto è già spedito e non entra nell'assegnazione; ma un
  cambio rilasciato sì (1.5).

### 1.7 Permessi

#### FATTI

- `read_returns`/`write_returns`: "The `Return` object, the reverse logistics objects, such as `ReverseDelivery` and
  `ReverseFulfillmentOrder`, and the return mutations". Non sono tra gli scope che richiedono approvazione di Shopify.
  Le alternative `read_marketplace_returns`/`write_marketplace_returns` richiedono approvazione.
  [Access scopes](https://shopify.dev/docs/api/usage/access-scopes)
- Le guide sui resi chiedono anche di rispettare i requisiti sui **dati protetti dei clienti**.
  [Manage reverse fulfillment orders](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-fulfillment-orders)
- Altri scope: rimborsi con `write_orders` (`refundCreate`); credito del negozio con `read_store_credit_accounts`,
  `write_store_credit_account_transactions`; carte regalo con `write_gift_cards`; regole di reso con
  `read_legal_policies`.
  [refundCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/refundCreate),
  [storeCreditAccountCredit](https://shopify.dev/docs/api/admin-graphql/latest/mutations/storeCreditAccountCredit),
  [giftCardCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/giftCardCreate),
  [Access scopes](https://shopify.dev/docs/api/usage/access-scopes)
- Permessi dello staff nel pannello: **Return** per creare resi; **Refund to original payment** e/o **Refund to store
  credit** per rimborsare; **Store credit** + **Edit store credit** per dare credito a mano.
  [Creating returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns),
  [Processing returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns),
  [Store credit](https://help.shopify.com/en/manual/customers/store-credit)

### 1.8 Cosa resta solo nel pannello di Shopify

#### FATTI

- Attivare i resi self-service, impostare regole di reso (le si legge da API dal 2026-10, l'assegnazione a un mercato
  si scrive con `write_markets`), modificare i modelli delle notifiche.
  [Self-serve setup](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup),
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)
- Creare un'etichetta di reso Shopify Shipping (solo USA/Canada, dal pannello); l'API `shippingLabelPurchase` è per
  fulfillment order, non per i resi.
  [Creating returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns),
  [shippingLabelPurchase](https://shopify.dev/docs/api/admin-graphql/latest/mutations/shippingLabelPurchase)

#### DEDUZIONI

- Tutto il resto del ciclo del reso (creare, approvare, rifiutare, etichetta caricata, esito, rimborso, credito, chiusura)
  si fa anche da API. "Resta a una persona" (212) è quindi una **scelta**, non un limite di Shopify.

## 2. Rimborsi

### 2.1 Cosa offre Shopify

#### FATTI

- `returnProcess` (scope `write_returns`): conferma pezzi di reso e di cambio, registra le disposizioni per riga
  (`returnLineItems[].dispositions`), crea i fulfillment order dei cambi e "optionally issuing refunds";
  `financialTransfer.issueRefund` con `orderTransactions` (transazione d'origine e importo) e `refundMethods` (oggi solo
  `storeCreditRefund` con `amount` ed `expiresAt` facoltativo); `refundShipping`, `refundDuties`; `notifyCustomer` (di
  serie `false`); `allowOverRefunding`: "Refunds issued as store credit can't exceed the amount paid".
  [returnProcess](https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnProcess),
  [ReturnProcessInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReturnProcessInput),
  [ReturnProcessRefundInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReturnProcessRefundInput),
  [RefundMethodInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/RefundMethodInput),
  [StoreCreditRefundInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/StoreCreditRefundInput)
- `Return.suggestedFinancialOutcome` propone importi (rimborso, tasse, spedizione, sconti) dato `refundMethodAllocation`
  `ORIGINAL_PAYMENT_METHODS` o `STORE_CREDIT`. Si può rimborsare in parte o più tardi.
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management),
  [RefundMethodAllocation](https://shopify.dev/docs/api/admin-graphql/latest/enums/RefundMethodAllocation)
- `refundCreate` (scope `write_orders`): rimborso di righe (con eventuale rimessa a magazzino), spedizione, dazi, metodi
  diversi, credito del negozio "when enabled"; `notify` per avvisare il cliente; `processedAt` per registrare rimborsi
  fatti fuori (2026-01). **Chiave di idempotenza obbligatoria dalla 2026-04.**
  [refundCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/refundCreate),
  [RefundInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/RefundInput),
  [Release notes 2026-01](https://shopify.dev/changelog/release-notes/2026-01),
  [Release notes 2026-04](https://shopify.dev/changelog/release-notes/2026-04)
- Credito del negozio: `storeCreditAccountCredit` (scope `write_store_credit_account_transactions`) accredita un cliente
  (crea il conto se manca, per valuta), con `expiresAt` facoltativo e `notify` (di serie `false`, dalla 2026-01 manda
  l'email "store credit issued"); dalla 2027-01 (RC) una nota visibile solo al negozio.
  [storeCreditAccountCredit](https://shopify.dev/docs/api/admin-graphql/latest/mutations/storeCreditAccountCredit),
  [StoreCreditAccountCreditInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/StoreCreditAccountCreditInput),
  [Release notes 2027-01](https://shopify.dev/changelog/release-notes/2027-01)
- Credito del negozio, dal centro assistenza: "Store credit isn't available for legacy customer accounts"; meno di
  15.000 USD per account; il cliente lo usa nel negozio online, POS e Shop (non su bozze e ordini modificati); deve usare
  tutto il saldo; scadenza per singolo accredito, con l'avvertenza di verificare le leggi del paese; per i negozi creati
  dal 12/5/2025 le commissioni di terzi si applicano alla parte pagata con credito.
  [Store credit](https://help.shopify.com/en/manual/customers/store-credit)
- Carte regalo: `giftCardCreate` (scope `write_gift_cards`), assegnabile a un cliente, con codice, scadenza e notifica al
  destinatario; dalla 2026-04 si leggono le impostazioni di scadenza predefinite.
  [giftCardCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/giftCardCreate),
  [Release notes 2026-04](https://shopify.dev/changelog/release-notes/2026-04)
- Nel pannello: metodo di rimborso Originale, Credito del negozio, o entrambi; "Send notification once refund is
  finalized" selezionato di serie; spese di reso applicate alla prima elaborazione.
  [Processing returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns)
- Rimborsi in generale: alcuni metodi non si rimborsano sull'originale (esempio OXXO); il sovra-rimborso sull'originale
  è solo per Shopify Payments e richiede un permesso; non si rimborsa la spedizione se c'è uno sconto di spedizione
  gratuita a livello d'ordine; notifica al cliente attiva di serie.
  [Refunding orders](https://help.shopify.com/en/manual/fulfillment/managing-orders/refunding-orders)

#### DEDUZIONI

- Un'app **può eseguire** rimborsi e credito; con `returnProcess` lo fa nello stesso passo in cui registra l'esito dei
  pezzi. Proporre senza eseguire (preparare l'importo con `suggestedFinancialOutcome` e lasciare il clic alla persona nel
  pannello) è anche possibile.
- Le **carte regalo** come rimborso creano differenze nei rapporti (AfterShip lo scrive per sé, sezione 5) e non sono il
  credito del negozio di Shopify; il credito del negozio è lo strumento previsto, ma solo con i nuovi account cliente.

### 2.2 Limiti per metodo di pagamento

#### FATTI

- Shopify Payments è disponibile in Italia (carte, pagamenti accelerati, metodi locali).
  [Supported countries](https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries),
  [Italy](https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries/italy)
- Shopify Payments: "You can usually issue a refund up to 120 days"; *Pending* fino a 2 giorni lavorativi; fino a 10
  giorni lavorativi perché il cliente riceva i fondi; la commissione della transazione originale non si recupera; se il
  saldo non basta, fuori da USA, Canada e Regno Unito l'importo viene preso dai pagamenti successivi.
  [Refunds (Shopify Payments)](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/refunds)
- Un rimborso può fallire se supera l'importo originale, se c'è una contestazione aperta, o se la transazione è fuori dal
  periodo ammesso dal fornitore di pagamento. Se si rimborsa fuori da Shopify (es. bonifico), si registra il rimborso
  deselezionando, se c'è, l'opzione che lo eseguirebbe di nuovo.
  [Refunds troubleshooting](https://help.shopify.com/en/manual/payments/shopify-payments/refunds-troubleshooting)
- Altri metodi Shopify Payments: Klarna e Satispay rimborsabili fino a 180 giorni (dai risultati di ricerca sulle pagine
  Klarna e Satispay del centro assistenza, non aperte: non verificato).
- PayPal (Italia): "Puoi inviare un rimborso completo o parziale entro 180 giorni dalla data del pagamento".
  [PayPal, rimborsi](https://www.paypal.com/it/cshelp/article/how-do-i-issue-a-refund-help101)
- Pagamenti manuali: contrassegno, vaglia, bonifico; l'ordine resta "da pagare" finché il negozio non lo segna pagato.
  La pagina non parla di rimborsi.
  [Manual payments](https://help.shopify.com/en/manual/payments/manual-payments)

#### DEDUZIONI

- Con contrassegno e bonifico il programma (o Shopify) può solo **registrare** il rimborso; il denaro va restituito a mano
  (bonifico al cliente), servono i dati bancari del cliente. È il caso dove una persona resta comunque necessaria.
- Il limite di 120 giorni di Shopify Payments supera i 14 + 14 giorni del recesso; può contare per la garanzia (2 anni),
  dove dopo 120 giorni il rimborso sull'originale può non riuscire e serve un bonifico.

### 2.3 Legge italiana e UE (contratti a distanza con consumatori)

Vale per clienti consumatori; per clienti con partita IVA (B2B) queste regole non si applicano allo stesso modo.
Che i clienti siano soprattutto consumatori italiani o UE è un'ipotesi del contesto, da confermare.

#### FATTI

- **Recesso:** 14 giorni "senza dover fornire alcuna motivazione"; per i beni il periodo decorre dal possesso fisico
  dell'ultimo bene. Se il negozio non informa sul diritto di recesso, il periodo si allunga di 12 mesi.
  [Codice del consumo, art. 52](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art52),
  [art. 53](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art53),
  [Direttiva 2011/83/UE, art. 9](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:02011L0083-20220528)
- **Come si recede:** modulo tipo "oppure … una qualsiasi altra dichiarazione esplicita della sua decisione di recedere";
  il negozio può offrire un modulo sul sito e allora conferma il ricevimento su supporto durevole.
  [art. 54](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art54)
- **Funzione di recesso online (nuova):** per i contratti a distanza conclusi con un'interfaccia online, il negozio deve
  offrire una funzione indicata con "recedere dal contratto qui" (o equivalente), sempre disponibile per tutto il periodo
  di recesso, ben visibile; il cliente fornisce nome, contratto e mezzo elettronico per la conferma; poi "conferma
  recesso"; il negozio manda "senza indebito ritardo" un avviso di ricevimento su supporto durevole con contenuto, data
  e ora. Introdotta dal d.lgs. 31/12/2025 n. 209, si applica dal 19/6/2026 ai contratti successivi (recepisce la
  direttiva (UE) 2023/2673, art. 11-bis della 2011/83).
  [art. 54-bis](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art54bis),
  [Direttiva (UE) 2023/2673](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32023L2673)
- Shopify dice che le sue regole di reso e annullamento "help meet the electronic withdrawal function requirement" e
  suggerisce: resi self-service attivi, annullamento fino all'evasione, finestra di almeno 14 giorni.
  [EU right of withdrawal](https://help.shopify.com/en/manual/compliance/legal/eu-right-of-withdrawal),
  [Return rules](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules)
- Nei forum di Shopify si discute se il flusso con accesso tramite codice email basti, visto che la funzione deve
  essere "facilmente accessibile"; ci sono app che offrono un modulo senza accesso. (Non verificato: fonti di comunità e
  schede di app, es. [discussione](https://community.shopify.dev/t/new-eu-withdrawal-button-required-by-june-19-2026/35121))
- **Rimborso:** "tutti i pagamenti ricevuti …, eventualmente comprensivi delle spese di consegna, senza indebito ritardo e
  comunque entro quattordici giorni dal giorno in cui è informato della decisione"; "utilizzando lo stesso mezzo di
  pagamento usato dal consumatore per la transazione iniziale, salvo che il consumatore abbia espressamente convenuto
  altrimenti e a condizione che questi non debba sostenere alcun costo"; "È nulla qualsiasi clausola che preveda
  limitazioni al rimborso"; non si rimborsa il sovrapprezzo di una consegna più cara scelta dal cliente; "il professionista
  può trattenere il rimborso finchè non abbia ricevuto i beni oppure finchè il consumatore non abbia dimostrato di aver
  rispedito i beni, a seconda di quale situazione si verifichi per prima".
  [art. 56](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art56),
  [Direttiva 2011/83/UE, art. 13](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:02011L0083-20220528)
- **Obblighi del cliente:** restituisce entro 14 giorni dalla comunicazione del recesso; sostiene "solo il costo diretto
  della restituzione", se informato; risponde solo della diminuzione di valore per manipolazione oltre quella necessaria.
  [art. 57](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art57)
- **Eccezioni** (es. beni su misura, deperibili, sigillati per igiene e aperti, audio/video/software sigillati e aperti).
  [art. 59](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art59)
- **Garanzia legale (difetto di conformità):** il venditore risponde dei difetti presenti alla consegna che si
  manifestano entro due anni; rimedi: ripristino (riparazione o sostituzione, a scelta del consumatore salvo
  impossibilità o costi sproporzionati), riduzione del prezzo o risoluzione; con la risoluzione il bene torna "a spese"
  del venditore e il prezzo si rimborsa al ricevimento del bene o della prova della spedizione.
  [art. 133](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art133),
  [art. 135-bis](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art135bis),
  [art. 135-quater](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art135quater)

#### DEDUZIONI (da far confermare a chi segue la parte legale)

- **I 14 giorni del rimborso partono dalla richiesta, non dall'arrivo della scatola.** Il negozio può aspettare la merce
  o la prova della spedizione: la prova più semplice è il tracking. Quindi la data della richiesta (sul sito o per
  email) e il tracking vanno registrati, e il programma può avvisare quando un rimborso si avvicina alla scadenza.
- **Credito del negozio al posto del rimborso, nel recesso:** solo se il cliente lo accetta in modo espresso e senza
  costi. L'accordo di oggi per WhatsApp o email è probabilmente valido, ma va **conservato** (chi, quando, cosa). Una
  scelta fatta dal cliente in un modulo (idea A) sarebbe un accordo espresso più facile da dimostrare. Proporre il
  credito come opzione predefinita o unica no.
- **Spese di reso trattenute:** ammesse solo per il "costo diretto della restituzione" se il cliente era informato; un
  costo di rimessa a magazzino su un recesso rischia di essere una limitazione nulla (art. 56). Per la garanzia la
  spedizione di ritorno è a carico del venditore.
- **Recesso e garanzia vanno distinti** al momento della richiesta: il motivo (difettoso, sbagliato, non piace) cambia
  rimedi, chi paga il ritorno e i tempi. Nel nostro esito per pezzo, «Danneggiato» non dice da solo se il danno c'era
  alla consegna (garanzia) o è del cliente (diminuzione di valore): serve la decisione del responsabile.
- **Una email che chiede il reso è già una dichiarazione di recesso valida** (art. 54, "qualsiasi altra dichiarazione
  esplicita"): conta la data di ricezione. Questo pesa sull'idea B.
- La funzione di recesso online (54-bis) è un obbligo del **sito**: con i resi self-service di Shopify il negozio
  probabilmente la copre, a condizione dei nuovi account cliente; se basti l'accesso con codice email è discusso. Non è
  compito del programma di magazzino, ma cambia da dove arrivano le richieste.

## 3. Comunicazione con il cliente

### FATTI

- Notifiche Shopify sui resi (Impostazioni → Notifiche → Resi): **Return request confirmation** ("Sent automatically …
  after they request a return using self-serve returns"), **Return request approved** (con le informazioni per la
  spedizione), **Return request declined** (messaggio modificabile prima dell'invio); l'etichetta caricata arriva in
  un'email separata. Lo staff riceve le richieste per email se riceve quelle degli ordini.
  [Self-serve setup](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup),
  [Return approved](https://help.shopify.com/en/manual/fulfillment/setup/notifications/exchange-notifications/return-approved)
- Rimborso: notifica di rimborso con importo e righe; credito del negozio: email se si seleziona "Notify customer".
  [Notification variables](https://help.shopify.com/en/manual/fulfillment/setup/notifications/email-variables),
  [Store credit](https://help.shopify.com/en/manual/customers/store-credit)
- I modelli si modificano (Liquid) e si traducono; il cliente riceve le email nella lingua in cui ha fatto l'ordine se
  la traduzione esiste, altrimenti nella lingua predefinita del negozio. (Dai risultati di ricerca sulle pagine
  [Email notifications](https://help.shopify.com/en/manual/fulfillment/setup/notifications/email-notifications) e
  [Checkout and notifications languages](https://help.shopify.com/en/manual/international/languages/checkout-and-notifications);
  la seconda non aperta: non verificato nei dettagli)
- Dall'API le notifiche partono secondo i flag: `returnProcess.notifyCustomer` (di serie `false`),
  `refundCreate.notify`, `reverseDeliveryCreateWithShipping.notifyCustomer` (di serie `true`),
  `storeCreditAccountCredit.notify` (di serie `false`), `fulfillmentCreate.notifyCustomer`.
  [returnProcess](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReturnProcessInput),
  [RefundInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/RefundInput),
  [reverseDeliveryCreateWithShipping](https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseDeliveryCreateWithShipping),
  [StoreCreditAccountCreditInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/StoreCreditAccountCreditInput)
- Email libere da un'app: l'input `EmailInput` (to, from, subject, body, customMessage) esiste solo per inviti
  all'account, fatture di ordini e bozze, e richieste di metodo di pagamento (`orderInvoiceSend`,
  `draftOrderInvoiceSend`, `customerSendAccountInviteEmail`, …); non abbiamo trovato una mutation generica "manda email al
  cliente".
  [EmailInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/EmailInput),
  [orderInvoiceSend](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend)
- Shopify Flow: app gratuita sui piani Basic, Grow, Advanced e Plus (*Send HTTP request* solo da Grow in su). Trigger
  per i resi: *Return requested/approved/declined/processed/closed/reopened/canceled*, *Refund created*. Azioni sui resi:
  solo *Cancel/Close/Reopen return*; poi *Send Admin API request*, tag e metafield sugli ordini. *Send internal email*
  "best used to send emails to staff", non per i clienti, e l'indirizzo non può venire da una variabile.
  [Shopify Flow](https://help.shopify.com/en/manual/shopify-flow),
  [Triggers](https://help.shopify.com/en/manual/shopify-flow/reference/triggers),
  [Actions](https://help.shopify.com/en/manual/shopify-flow/reference/actions),
  [Send internal email](https://help.shopify.com/en/manual/shopify-flow/reference/actions/send-email)
- Shopify Inbox: chat sul sito con assistente IA, gratuita, italiano tra le lingue; la scheda non nomina WhatsApp né
  un'API.
  [Shopify Inbox](https://apps.shopify.com/inbox)

### WhatsApp Business Platform (Cloud API): FATTI

- Requisiti: account Facebook o Meta gestito, registrazione come sviluppatore, app Meta con il caso d'uso WhatsApp, un
  portafoglio aziendale (business portfolio), un account di messaggistica e un numero.
  [Get started](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started)
- Limiti di invio: un portafoglio nuovo può raggiungere 250 numeri diversi in 24 ore fuori dalla finestra di servizio;
  2.000 dopo la verifica dell'azienda o 2.000 messaggi di qualità in 30 giorni, poi crescita automatica.
  [Messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits)
- **Modelli:** gli unici messaggi che si possono mandare fuori dalla finestra di servizio; categoria *marketing*,
  *utility* (transazionali) o *authentication*; revisione automatica fino a 24 ore; si mandano solo se `APPROVED`.
  [Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
- **Finestra di servizio (24 ore):** si apre e si rinnova a ogni messaggio del cliente; dentro si possono mandare
  messaggi liberi (di servizio); fuori solo modelli.
  [Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)
- **Opt-in:** obbligatorio prima di scrivere; può essere generico (non solo per WhatsApp) se conforme alle leggi locali;
  deve dire chiaramente che si accetta di ricevere messaggi e il nome dell'azienda.
  [Get opt-in](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in)
- **Prezzi:** dal 1/7/2025 per messaggio consegnato, per categoria e paese; i messaggi del cliente sono gratuiti; dal
  1/10/2026 sono di nuovo a pagamento i messaggi di servizio (gratis i primi 1.000 al mese per numero) e i modelli utility
  dentro la finestra di servizio; gratis tutto nella finestra di 7 giorni aperta da un annuncio "Click to WhatsApp";
  l'Italia è un mercato a sé, con tariffa marketing aumentata dal 1/7/2026; i prezzi cambiano al massimo il 1° di ogni
  trimestre. Le tariffe in euro sono in file CSV/PDF e in un selettore sul sito WhatsApp Business che non siamo riusciti a
  leggere: **importi per l'Italia non verificati**. A titolo di ordine di grandezza la pagina cita 0,68 centesimi di
  dollaro per un messaggio utility in Brasile.
  [Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing),
  [Platform pricing](https://whatsappbusiness.com/products/platform-pricing/)
- **Messaggi in arrivo e stato dei messaggi inviati arrivano con webhook** a "un server di tua scelta"; il server deve
  avere un certificato TLS valido ("Self-signed certificates are not supported"); per la produzione serve un endpoint
  proprio.
  [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview),
  [Create a webhook endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint)
- **App WhatsApp Business normale:** non ha API; un numero usato con l'app si può collegare anche alla Cloud API
  ("coexistence") solo tramite un Solution Partner o Tech Provider con *Embedded Signup*; i messaggi dall'app restano
  gratuiti, quelli via API si pagano; limite di 20 messaggi al secondo.
  [Onboard WhatsApp Business app users](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users)

### DEDUZIONI

- **In automatico senza problemi:** le notifiche Shopify (conferma richiesta, approvazione con etichetta, rifiuto,
  rimborso, credito), purché tradotte in italiano e con testi rivisti. Il programma decide solo se accenderle (flag).
- **Testi liberi al cliente** (es. «la scatola è arrivata, manca un pezzo»): dal programma via email aziendale (SMTP o API
  della casella), con la stessa logica delle mail ai fornitori (223, 311): anteprima e invio da una persona.
- **WhatsApp via API:** mandare modelli (es. «reso ricevuto», «rimborso fatto») è solo traffico in uscita e funziona dal
  server in sede; **ricevere le risposte no**, servono un indirizzo pubblico o un servizio intermedio in cloud (un
  fornitore WhatsApp o un piccolo ricevitore che il server interroga). Il WhatsApp di oggi, a mano dall'app, resta
  possibile e gratuito, ma il programma non lo vede.
- **Flow** non aiuta a scrivere ai clienti; può aiutare a etichettare gli ordini con reso, ma il nostro giro a intervalli
  lo fa già.

## 4. Tutto ciò a cui ci si può collegare (solo in uscita, a intervalli)

Piani Shopify citati nelle pagine lette: Basic, Grow, Advanced, Plus (più Starter/Retail). "Tutti" = la pagina non pone
limiti di piano.

| Area | Si legge | Si scrive | Permesso (scope) | Piano | Note per il server in sede senza webhook |
|---|---|---|---|---|---|
| Ordini | Sì | Sì (note, tag, modifiche, annullamento) | `read_orders`/`write_orders` + `read_all_orders` oltre 60 giorni | Tutti | Polling con `updated_at`; vedi ricerca del 15/11 |
| Evasioni e spedizioni | Sì | Sì (`fulfillmentCreate`, tracking) | scope dei fulfillment order (approvazione di Shopify) | Tutti | Vedi ricerca del 15/11 |
| Giacenze | Sì | Sì (variazioni, impostazioni assolute) | `read_inventory`/`write_inventory` | Tutti | Idempotenza e `changeFromQuantity` dalla 2026-04 |
| Prodotti e varianti | Sì | Sì | `read_products`/`write_products` | Tutti | Dalla 2026-10 `barcodes` (fino a 20) al posto di `barcode` ([2026-10](https://shopify.dev/changelog/release-notes/2026-10)) |
| Clienti | Sì (dati protetti campo per campo) | Sì | `read_customers`/`write_customers` + dati protetti | Tutti | Vedi ricerca del 15/11 |
| Resi | Sì | Sì (creare, approvare, rifiutare, etichetta, esito, elaborare, chiudere) | `read_returns`/`write_returns` | Tutti; self-service solo con nuovi account | Niente query `returns`: si passa da `orders` con `return_status` |
| Regole di reso | Sì (2026-10) | Solo l'assegnazione ai mercati | `read_legal_policies`; `write_markets` | Per mercato: Advanced e Plus | — |
| Motivi di reso | Sì | — | `read_returns` | Tutti | `handle` stabile, nome tradotto |
| Rimborsi | Sì (`Order.refunds`, `Return.refunds`) | Sì (`refundCreate`, `returnProcess`) | `write_orders` / `write_returns` | Tutti | Idempotenza obbligatoria su `refundCreate` |
| Credito del negozio | Sì | Sì (accredito, addebito) | `read_store_credit_accounts`, `read/write_store_credit_account_transactions` | Tutti (solo nuovi account cliente) | [Access scopes](https://shopify.dev/docs/api/usage/access-scopes) |
| Carte regalo | Sì | Sì | `read_gift_cards`/`write_gift_cards` | Non verificato | — |
| Transazioni dell'ordine | Sì (`OrderTransaction`) | Indirettamente (rimborsi, catture) | `read_orders` | Tutti | — |
| Shopify Payments: accrediti e movimenti | Sì (`ShopifyPaymentsPayout`, `ShopifyPaymentsBalanceTransaction`) | No | `read_shopify_payments_payouts` + permesso utente `view_payouts` | Con Shopify Payments | [Payout](https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout) |
| Etichette Shopify Shipping (uscita) | Sì (`ShippingLabel`) | Sì (`shippingLabelPurchase`, 2026-07) | `write_orders` + scope fulfillment order + permesso utente `buy_shipping_labels` | Non indicato nella pagina (servono i termini Shopify Shipping accettati) | In Italia: BRT e Poste solo nazionali, DHL Express; asincrono, si interroga lo stato |
| Etichette di reso | Sì (tracking nel reso) | Solo etichetta esterna caricata | `write_returns` | Tutti | Shopify Shipping per i resi solo USA/Canada |
| Tariffe dei corrieri al checkout (Carrier Service) | Sì | Sì | `write_shipping` | Advanced o più (o Grow annuale / a pagamento) | Shopify chiama un `callbackUrl` **pubblico**: non adatto al server in sede ([DeliveryCarrierService](https://shopify.dev/docs/api/admin-graphql/latest/objects/DeliveryCarrierService)) |
| Corrieri italiani (GLS, SDA, BRT con contratto proprio) | Tramite app di terzi | Tramite app | — | — | Es. Qapla', Logivery, GLS Shipping (schede in sezione 5) |
| Fatture elettroniche (SDI) | — | — | — | — | Nessuna pagina ufficiale Shopify trovata che le emetta; esistono app (Fatture Italia, FatturaFlow, Eurofattura) (non verificato oltre le schede) |
| Tasse | Righe d'imposta sugli ordini | — | `read_orders`; `read_taxes` richiede approvazione | — | — |
| Sconti | Sì | Sì | `read_discounts`/`write_discounts` | Tutti | `read_price_rules` rimosso dalla 2026-10 |
| Metafield | Sì | Sì | Lo scope della risorsa proprietaria | Tutti | Utile per salvare dati nostri sugli ordini (idea A) |
| Flow | — | Avvia flussi (`flowTriggerReceive`) | — | Basic, Grow, Advanced, Plus | Flow può chiamare l'Admin API, non il nostro server |

Fonti della tabella, oltre a quelle in riga: [Access scopes](https://shopify.dev/docs/api/usage/access-scopes),
[shippingLabelPurchase](https://shopify.dev/docs/api/admin-graphql/latest/mutations/shippingLabelPurchase),
[carrierServiceCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/carrierServiceCreate),
[ShopifyPaymentsBalanceTransaction](https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsBalanceTransaction),
[Fatture Italia](https://apps.shopify.com/fatture-italia), [FatturaFlow](https://apps.shopify.com/fatturaflow),
[Eurofattura](https://apps.shopify.com/eurofattura-it).

### Novità del changelog 2025–2026 sui resi (FATTI)

- 2025-07: `returnProcess` diventa il passo d'elaborazione; le app devono migrare.
  [Apps in returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps)
- 2025-01: `reverseDeliveryDispose` deprecata e poi rimossa; si usa `reverseFulfillmentOrderDispose`.
  [Manage reverse deliveries](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-deliveries)
- 2026-01: motivi `ReturnReasonDefinition`; `Return.transactions`; `refundCreate.processedAt`; idempotenza facoltativa
  su `refundCreate`; `notify` su `storeCreditAccountCredit`.
  [Release notes 2026-01](https://shopify.dev/changelog/release-notes/2026-01)
- 2026-04: idempotenza **obbligatoria** su `refundCreate`; in ShopifyQL i campi "returns" diventano "sales_reversals".
  [Release notes 2026-04](https://shopify.dev/changelog/release-notes/2026-04)
- 2026-07: `shippingLabelPurchase`.
  [Release notes 2026-07](https://shopify.dev/changelog/release-notes/2026-07)
- 2026-10: imposta sulle spese di reso; campi nuovi su `ExchangeLineItem`; `returnPolicyProfiles`.
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)
- 2027-01 (RC): nota del negozio sulle transazioni di credito.
  [Release notes 2027-01](https://shopify.dev/changelog/release-notes/2027-01)
- Requisiti "Built for Shopify" per le app di resi e cambi in vigore dal 1/12/2026 (citato da un risultato di ricerca
  sul changelog, pagina non aperta: non verificato).

### Aggiornamenti alla ricerca del 15/11/2026

- La versione stabile resta la 2026-10; la release candidate è la 2027-01. Nulla da correggere sulle date.
- Da aggiungere ai permessi dell'app (53, 226): `read_returns`, `write_returns`; se si accetta di rimborsare o dare
  credito dal programma anche `read_store_credit_accounts`, `write_store_credit_account_transactions` (e `write_orders`
  c'è già); per leggere le regole di reso `read_legal_policies`.
- Gli argomenti webhook dei resi esistono, ma per il nostro modello non servono: il giro a intervalli usa il filtro
  `return_status` sugli ordini.

## 5. App esistenti per i resi

Tutti i prezzi in USD dalle schede dell'App Store di Shopify, lette il 19/11/2026; possono cambiare.

| App | Cosa fa (dalla scheda) | Prezzo | Italiano | Corrieri nominati | Scrive i resi di Shopify? |
|---|---|---|---|---|---|
| Resi di Shopify (integrati) | Self-service, regole, motivi, cambi, credito, notifiche | Incluso | Notifiche traducibili | Etichette Shopify solo USA/CA; altrimenti etichetta caricata | Sì (sono loro) |
| [AfterShip Returns](https://apps.shopify.com/returns-center-by-aftership) | Portale, rimborsi automatici, cambi, sostituzioni, resi in negozio | Gratis (a carico del cliente) / 19 / 119 al mese con resi inclusi e costo per reso in più | Sì | Canada Post, FedEx, UPS, USPS | Sì, aggiorna lo stato tramite la Return API di Shopify ([guida](https://support.aftership.com/en/articles/15389545-auto-update-return-status-to-shopify-with-shopify-returns-api)); il credito lo dà come carta regalo ([guida](https://support.aftership.com/en/articles/15389471-understanding-returns-and-exchanges-in-shopify-with-aftership-returns)) |
| [Loop Returns](https://apps.shopify.com/loop-returns) | Portale, cambi istantanei, credito bonus, antifrode | Gratis oltre 5.000 ordini l'anno (etichette USA/CA) / da 340 al mese | Non indicato | Non nominati | Non indicato |
| [ReturnGO](https://apps.shopify.com/returngo) | Portale, approvazioni automatiche, credito, cambi | 147 / 297 al mese | Non indicato | Integrazione Sendcloud, Shippo, ShipStation | Non indicato |
| [Return Prime](https://apps.shopify.com/return-prime) | Portale, cambi, credito, rimborsi; "EU-compliant withdrawal button" | Gratis con 5 richieste, poi da 19,99 al mese | Non indicato | UPS, USPS | Non indicato |
| [Rich Returns](https://apps.shopify.com/rich-returns) | Portale, rimborsi automatici, cambi, carte regalo, credito | 19 / 39 / 99 / 199 al mese | Non indicato | UPS, USPS, Shippo, EasyPost, ShipStation | "Shopify Sync" senza dettagli |
| [Redo](https://apps.shopify.com/redo) | Resi e cambi, credito, helpdesk | Resi gratis (ricavi da altri servizi) | Non indicato | Non nominati | Non indicato |
| [easyReturns](https://apps.shopify.com/easyreturns-1) | Portale e modulo di recesso UE pubblici, etichette automatiche | Gratis (solo portali) / 19 / 39 / 59 al mese | No (tedesco, inglese) | DHL, DPD, GLS, Internetmarke | Non indicato |
| [Sendcloud](https://apps.shopify.com/sendcloud) | Spedizioni con portale resi (piano Premium) ed etichette di reso | Gratis / 40 / 124 / 249 al mese + 0,08–0,12 € a etichetta | Sì | "170+ carriers"; nominati DHL, DPD, Evri, PostNL, Royal Mail, UPS | Non indicato |
| [Outvio](https://apps.shopify.com/outvio) | Resi e cambi, etichette di ritiro e reso, credito | A ordine (non indicato) | No | Correos, DHL, DPD, FedEx, GLS, UPS | Non indicato |
| [Qapla'](https://apps.shopify.com/qapla) (italiana) | Etichette multicorriere, resi dal pannello o pagina self-service | A spedizioni (non indicato) | Sì | DHL Express, DPD, FedEx, GLS, Royal Mail, UPS | Non indicato |

### DEDUZIONI

- Nessuna scheda letta nomina insieme etichette di reso con **BRT e Poste Italiane**; GLS compare più spesso. Per un
  magazzino italiano l'etichetta di reso dipende più dal contratto con il corriere che dall'app di resi.
- **Doppia rimessa a magazzino:** se un'app di resi rimette a magazzino (con disposizione `RESTOCKED`) e poi il nostro
  programma prova a fare lo stesso, Shopify dovrebbe rifiutare la seconda disposizione (una per unità); il rischio vero è
  l'opposto: l'app rimette a magazzino un pezzo che noi giudichiamo danneggiato, o un'app che **non** usa i resi di
  Shopify e ripristina la giacenza con una variazione, che si somma alla nostra. Con un'app accanto bisogna decidere chi
  scrive l'esito, e spegnere la rimessa automatica nell'altro.
- **Affiancare un'app:** pro: portale cliente pronto, regole, scelta del rimborso, email, a volte modulo di recesso UE;
  contro: costo mensile e per reso, quasi tutte in inglese e pensate per USA, corrieri italiani assenti, un altro
  sistema da tenere allineato, dati dei clienti a un altro fornitore. **Tutto nel programma:** pro: un solo posto, regole
  nostre, nessun canone; contro: il portale cliente non lo fa il programma (vive sul sito), e scrivere rimborsi richiede
  cura (importi, idempotenza, legge). **Resi di Shopify + programma:** pro: gratis, i resi stanno già dove il programma li
  legge; contro: il cliente non sceglie il rimborso, servono i nuovi account cliente, etichetta di reso non automatica in
  Italia. La scelta è dell'utente.

## 6. Le due idee dell'utente

### 6.A Scelta del tipo di rimborso quando il cliente chiede il reso sul sito

#### FATTI

- La richiesta self-service di Shopify raccoglie motivo e condizione del prodotto; il metodo di rimborso lo sceglie chi
  elabora il reso (Original payment, Store credit, o entrambi).
  [Self-serve returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns),
  [Processing returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns)
- Nella Customer Account API, `orderRequestReturn` accetta per riga solo `lineItemId`, `quantity`,
  `returnReasonDefinitionId` e `customerNote` (300 caratteri); il campo `returnReason` è deprecato. Non c'è un campo per
  il metodo di rimborso; "the mutation doesn't directly create a return", crea una richiesta da approvare.
  [orderRequestReturn](https://shopify.dev/docs/api/customer/latest/mutations/orderRequestReturn),
  [RequestedLineItemInput](https://shopify.dev/docs/api/customer/latest/input-objects/RequestedLineItemInput),
  [Build self-serve returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-self-serve-returns)
- **Estensioni dell'account cliente:** solo sui nuovi account cliente; pagine *Order index* e *Order status* con azioni
  sull'ordine "such as requesting a return"; target `customer-account.order.action.menu-item.render` (solo un pulsante)
  collegato a una finestra modale o a una pagina intera; le estensioni chiamano la Customer Account API con richieste già
  autenticate e possono leggere e scrivere metafield; le scritture di metafield sono ammesse su `Customer`, `Order`,
  `Company`, `CompanyLocation`; la Customer Account API richiede il livello 1 dei dati protetti; l'accesso alla rete
  esterna (`network_access`) va abilitato a parte.
  [Building apps for customer accounts](https://shopify.dev/docs/apps/build/customer-accounts),
  [Order action menus](https://shopify.dev/docs/apps/build/customer-accounts/order-action-extensions),
  [Customer account UI extensions](https://shopify.dev/docs/api/customer-account-ui-extensions),
  [Metafield writes](https://shopify.dev/docs/apps/build/customer-accounts/metafields)
- Piano: nelle pagine lette non c'è un limite di piano per le estensioni dell'ordine; un changelog dice che i nuovi
  negozi di sviluppo le hanno su tutti i piani. Che valgano per un'app del Dev Dashboard di un solo negozio non è scritto.
  (Non verificato; [changelog](https://shopify.dev/changelog/posts/checkout-and-customer-account-ui-extensions-available-by-default-in-new-development-shops))
- **Ospiti:** il cliente apre l'ordine dal link dell'email senza accedere, ma per inviare la richiesta accede con un
  codice di 6 cifre mandato all'email dell'ordine, senza password.
  [Self-serve setup](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup)
- **Senza app, con il tema:** il modulo di contatto manda le richieste all'email del negozio; la pagina non parla di
  campi personalizzati né di dati salvati nel pannello; per moduli su misura suggerisce servizi esterni.
  [Contact page](https://help.shopify.com/en/manual/online-store/themes/customizing-themes/add-contact-page)
- Alcune app di resi (Return Prime, Rich Returns, Loop) promuovono "exchange-first" o "store credit over refunds".
  [Rich Returns](https://apps.shopify.com/rich-returns), [Return Prime](https://apps.shopify.com/return-prime)

#### DEDUZIONI

- Con i soli resi di Shopify la scelta del rimborso **non** arriva da sola: al massimo il cliente la scrive nella nota,
  testo libero che il programma può mostrare ma non interpretare con sicurezza.
- Con un'**estensione dell'account cliente** nella nostra app (stessa app del Dev Dashboard, se ammessa): il cliente
  sceglie «Rimborso sul metodo di pagamento» / «Credito del negozio» / «Cambio» al momento della richiesta; l'estensione
  invia la richiesta (`orderRequestReturn`) e scrive la scelta in un **metafield dell'ordine**; il nostro server la legge
  al giro successivo con l'Admin API. Il sito non deve mai raggiungere il server in sede. Costi: sviluppo e manutenzione
  di un'estensione (con il ciclo delle versioni trimestrali), nuovi account cliente obbligatori.
- La stessa scelta fatta dal cliente è anche la prova dell'**accordo espresso** sul credito (sezione 2.3), se il testo è
  chiaro e il rimborso sul metodo originale è un'opzione di pari evidenza.
- Un modulo del tema o una pagina esterna non crea un reso Shopify: diventa un'email (e si ricade nell'idea B).
- Per la funzione di recesso online (54-bis) conviene che il punto di partenza resti quello di Shopify o di un'app che lo
  dichiara conforme; un'estensione nostra lo affiancherebbe, non lo sostituirebbe.

### 6.B Casella email dedicata ai resi, letta da un'automazione con un LLM

#### FATTI

- **n8n, licenza:** "Sustainable Use License": uso e modifica "only for your own internal business purposes or for
  non-commercial or personal use"; distribuzione solo gratuita e non commerciale; i file `.ee` richiedono una licenza
  Enterprise. Le FAQ: si può usare "to help run your business" e "behind the scenes in your own product" se l'utente
  finale non costruisce o modifica i flussi; spedire n8n ai clienti come parte di un prodotto a pagamento "may sit in
  gray territory": chiedere a license@n8n.io.
  [LICENSE.md](https://github.com/n8n-io/n8n/blob/master/LICENSE.md),
  [License FAQ](https://docs.n8n.io/n8n-community-license/community-license/license-faq)
- **n8n, installazione:** Community edition gratuita in self-hosting; Docker (avvio rapido con SQLite) o PostgreSQL in
  produzione, Linux a 64 bit consigliato; per i soli flussi che chiamano servizi esterni serve accesso a Internet in
  uscita; i webhook pubblici servono solo per chi chiama n8n dall'esterno; "Don't expose the n8n process directly to the
  internet". Nodo *Email Trigger (IMAP)* per ricevere la posta da una casella.
  [Choose how to use n8n](https://docs.n8n.io/choose-how-to-use-n8n),
  [Production requirements](https://docs.n8n.io/deploy/host-n8n/install-options/production-requirements),
  [Email Trigger (IMAP)](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.emailimap)
- **Lettura della posta:** Microsoft 365 ha spento l'autenticazione di base per IMAP e POP in tutti i tenant; serve
  OAuth 2.0 o Microsoft Graph. Con Graph l'elenco dei messaggi richiede `Mail.ReadBasic`/`Mail.Read` (delegato) o
  `Mail.Read` applicativo per caselle di altri utenti.
  [Deprecation of Basic authentication](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/deprecation-of-basic-authentication-exchange-online),
  [List messages](https://learn.microsoft.com/en-us/graph/api/user-list-messages)
  Google Workspace: dal 14/3/2025 IMAP, SMTP e POP non funzionano con la sola password; servono OAuth o password per le
  app. Gmail API: `messages.list` con la sintassi di ricerca di Gmail; sincronizzazione parziale con `history.list` e
  `historyId`, oppure notifiche push.
  [Transition to OAuth](https://knowledge.workspace.google.com/admin/sync/transition-from-less-secure-apps-to-oauth),
  [messages.list](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/list),
  [Synchronizing clients](https://developers.google.com/workspace/gmail/api/guides/sync)
- **Casella condivisa Microsoft 365:** fino a 50 GB senza licenza, massimo 25 utenti, accesso di sola organizzazione.
  [About shared mailboxes](https://learn.microsoft.com/en-us/microsoft-365/admin/email/about-shared-mailboxes)
- **Creare il reso dopo la conferma:** `returnCreate` crea un reso già approvato quando "l'approvazione avviene fuori da
  Shopify".
  [Build return management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management)
- **GDPR:** il titolare ricorre solo a responsabili con garanzie sufficienti e con un contratto che fissi materia, durata,
  natura, finalità, tipi di dati e categorie di interessati (art. 28); minimizzazione e limitazione della conservazione
  (art. 5).
  [Regolamento (UE) 2016/679](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32016R0679)
- **Fornitori LLM in cloud:**
  - Anthropic (API): Anthropic è "data processor"; i dati "never used for model training without your express permission";
    il contenuto delle conversazioni non è conservato di serie, tranne per alcuni modelli ("Covered Models") che
    richiedono 30 giorni; conservazione zero su richiesta; contenuti segnalati e obblighi di legge a parte. Le condizioni
    commerciali incorporano un Data Processing Addendum e vietano di addestrare sui contenuti del cliente.
    [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention),
    [Commercial Terms](https://www.anthropic.com/legal/commercial-terms)
  - OpenAI (API): dati non usati per addestrare di serie; registri antiabuso conservati "up to 30 days"; conservazione
    zero previa approvazione. La pagina del DPA ha risposto 403: non verificato.
    [Your data](https://developers.openai.com/api/docs/guides/your-data)
  - Google (Gemini API): i servizi gratuiti usano i contenuti per migliorare i prodotti, con revisori umani; i servizi a
    pagamento no, con registrazione per un periodo limitato contro gli abusi; per utenti nello Spazio economico europeo si
    possono usare solo i servizi a pagamento; i dati a pagamento seguono il Data Processing Addendum.
    [Gemini API terms](https://aistudio.google.com/docs/terms)
- **Rischi:** OWASP LLM01:2025 *Prompt Injection*, anche indiretta "through external content the model processes";
  contromisure elencate: limitare il comportamento del modello, validare le uscite, filtrare ingressi e uscite, privilegi
  minimi, **approvazione umana per le azioni a rischio**, separare il contenuto esterno, prove avversarie.
  [OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

#### DEDUZIONI

- **Traffico:** leggere una casella con IMAP (OAuth), Graph o Gmail API a intervalli è solo traffico in uscita dal
  server: compatibile con la decisione 54. Le notifiche push (Gmail, Graph) invece vorrebbero un indirizzo pubblico.
- **n8n per il negozio** (installato dal negozio per sé): permesso dalla licenza. **n8n dentro il nostro prodotto** (che
  vuole essere una base per altri magazzini): zona grigia, da chiarire con n8n prima. Il programma può leggere la casella
  da sé con le stesse API, senza un secondo sistema da installare e aggiornare.
- **LLM in cloud:** i fornitori a pagamento offrono DPA e non addestrano sui dati; restano il trasferimento fuori UE da
  valutare, l'informativa ai clienti e la scelta di cosa mandare (solo il testo della mail, togliendo firme e allegati non
  necessari). **LLM locale** su un PC d'ufficio: i dati non escono, ma qualità e velocità su un PC normale vanno provate
  (vedi `docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md` per i limiti dell'hardware locale).
- **Cosa fa il modello e cosa no:** estrarre numero d'ordine, pezzi, motivo, scelta di rimborso e allegati (foto) e
  proporre una bozza di reso; mai creare resi, rimborsi o risposte da solo. Una persona vede la mail originale e lo
  storico con quel cliente, corregge, e conferma; solo allora il programma chiama `returnCreate`. Il numero d'ordine
  estratto va sempre confrontato con l'email del mittente e con l'ordine su Shopify (un'istruzione nascosta potrebbe
  indicare l'ordine di un altro).
- **Senza LLM** si ottiene già molto: regole semplici (numero d'ordine «#1234» nel testo, mittente = email dell'ordine)
  e una coda «Mail di reso da guardare» nel programma.
- **Risposta automatica con il link alla pagina dei resi:** semplice e senza LLM, porta il cliente nel flusso Shopify
  (dove nasce un reso vero) e manda l'avviso di ricevimento; ma la mail resta comunque una dichiarazione di recesso
  valida (art. 54), con la sua data: non si può ignorarla se il cliente non usa il link.
- **Indirizzo:** un sottodominio (es. `resi.dominio`) richiede DNS e configurazione di posta propri; un indirizzo sul
  dominio principale (casella condivisa o alias/inoltro, es. `resi@dominio`) basta per separare i resi. Un alias che
  inoltra a una casella principale complica la lettura automatica (le mail si mescolano): meglio una casella condivisa
  dedicata. (DEDUZIONE; nessuna fonte dice che il sottodominio serva)

## Conseguenze per il ticket «Resi del cliente nel magazzino Shopify»

### Cosa si può fare in automatico (dal server in sede, a intervalli)

- Vedere i resi aperti sul sito: ordini con `return_status` aperto, con righe, motivi, note, spedizioni di ritorno e
  tracking.
- Riconoscere la scatola dal barcode dell'etichetta di reso, **se** il tracking è registrato sul reso (indice nostro).
- Scrivere l'esito per pezzo (212) e, se si decide, caricare l'etichetta di reso, approvare o rifiutare la richiesta,
  creare il reso per i casi arrivati per email o WhatsApp (`returnCreate`).
- Proporre l'importo del rimborso (`suggestedFinancialOutcome`) e, se si decide, eseguirlo con `returnProcess`
  (metodo originale e/o credito del negozio), con la notifica Shopify al cliente.
- Avvisare il responsabile quando un rimborso si avvicina ai 14 giorni dalla richiesta.
- Mandare al cliente le notifiche Shopify; mandare email libere dalla casella aziendale; mandare modelli WhatsApp
  approvati (a pagamento).
- Leggere una casella resi a intervalli e preparare bozze di reso (con o senza LLM).

### Cosa non si può fare (senza abbellire)

- Etichette di reso Shopify Shipping in Italia: no (solo USA/Canada); serve un corriere o un'app.
- Sapere da Shopify se il pacco di reso è in viaggio o consegnato: no.
- Cercare un ordine per numero di tracking: no, solo con un indice nostro.
- Far scegliere al cliente il tipo di rimborso con i soli resi di Shopify: no; serve un'estensione o un'app.
- Ricevere i messaggi WhatsApp dei clienti sul server in sede senza un indirizzo pubblico o un servizio in cloud: no.
- Mandare email libere ai clienti tramite Shopify da un'app: no.
- Rimborsare dal programma contrassegno e bonifico: no, solo registrarli.
- Credito del negozio con i vecchi account cliente: no.

### Cosa richiede una persona

- Per legge: decidere recesso o garanzia nei casi dubbi; decidere sulla diminuzione di valore di un pezzo danneggiato;
  ottenere e conservare l'accordo espresso se si dà credito al posto del rimborso; restituire il denaro dei pagamenti
  manuali.
- Per Shopify: impostare regole di reso, resi self-service e notifiche nel pannello; eventuali permessi dell'utente se
  certe mutation li richiedono anche con il nostro token (da provare).
- Per prudenza: confermare ogni reso preparato da una mail (LLM o regole) prima che il programma lo crei.

### Scelte per l'utente (domande aperte)

1. **Chi decide il tipo di rimborso?** (a) una persona come oggi, su Shopify; (b) il cliente sul sito, con
   un'estensione dell'account cliente o un'app; (c) una regola fissa (es. sempre sul metodo originale, credito solo su
   richiesta). Conta per il lavoro della persona e per la prova dell'accordo sul credito.
2. **Il programma esegue i rimborsi o li prepara soltanto?** (a) solo prepara, la persona clicca su Shopify (212 di oggi);
   (b) esegue dopo una conferma nel programma; (c) esegue da solo per i casi semplici (pezzo integro, pagamento con carta).
   Conta per errori, permessi e responsabilità.
3. **I nuovi account cliente e i resi self-service sono attivi sul negozio?** Se no, attivarli (servono anche per il
   credito e per la funzione di recesso online)? Da verificare nel pannello.
4. **Etichetta di reso:** (a) il cliente spedisce da sé e manda il tracking; (b) il negozio fornisce un'etichetta del suo
   corriere (caricata dal programma o da una persona); (c) un'app di spedizioni o resi.
5. **Un'app di resi accanto al programma?** (a) no, resi di Shopify + programma; (b) sì, un'app (quale, e chi scrive
   l'esito); (c) un'estensione nostra solo per la scelta del rimborso.
6. **Credito del negozio o carta regalo** quando il cliente accetta il credito? Il credito di Shopify è lo strumento
   previsto (con i nuovi account); la carta regalo crea differenze nei rapporti.
7. **Spese di reso e costo di rimessa a magazzino:** trattenerle? Con quali regole, sentita la parte legale.
8. **Canale verso il cliente:** (a) notifiche Shopify + email dal programma; (b) in più modelli WhatsApp via API
   (costo per messaggio, opt-in, risposte non ricevibili dal server in sede); (c) WhatsApp a mano come oggi.
9. **Mail dei resi (idea B):** (a) risposta automatica con il link alla pagina dei resi; (b) il programma legge una
   casella dedicata e mette le mail in una coda da guardare (senza LLM); (c) come (b) con un LLM che prepara la bozza,
   in cloud (con DPA) o locale; (d) n8n al posto del programma per la lettura. Conta per GDPR, licenza e manutenzione.
10. **Indirizzo della casella:** casella condivisa sul dominio principale o alias/inoltro; il sottodominio non sembra
    necessario.
11. **«Da controllare» su Shopify:** scrivere subito `PROCESSING_REQUIRED` o aspettare la decisione del responsabile
    e scrivere una volta sola (dipende dalla prova sotto).

### Le due idee a confronto con le alternative (DEDUZIONE, nessuna scelta)

| Strada | Cosa arriva al programma | Costo e lavoro | Rischi | Dipende da |
|---|---|---|---|---|
| Come oggi, a mano | Niente; il reso si apre all'arrivo della scatola | Nessuno sviluppo | Scadenze di legge non seguite; accordo sul credito non conservato | — |
| Resi self-service di Shopify, senza estensione | Reso con pezzi, motivo, nota | Solo impostazioni | La scelta del rimborso resta in una nota libera o a voce | Nuovi account cliente |
| **A:** estensione dell'account cliente con scelta del rimborso | Reso + scelta in un metafield dell'ordine | Sviluppo e manutenzione dell'estensione | Versioni trimestrali; ammissibilità nell'app del Dev Dashboard da provare | Nuovi account cliente |
| App di resi del mercato | Reso Shopify (se l'app lo scrive) | Canone e costo per reso | Chi scrive l'esito; corrieri italiani; lingua | Scelta dell'app |
| Risposta automatica alle mail con il link alla pagina dei resi | Reso Shopify se il cliente usa il link | Minimo | La mail resta un recesso valido anche se il cliente non usa il link | Resi self-service attivi |
| **B1:** il programma legge la casella resi, coda da guardare, senza LLM | Mail con ordine riconosciuto da regole semplici | Lettura IMAP/Graph/Gmail con OAuth | Mail non riconosciute restano a mano | Casella dedicata |
| **B2:** come B1 con LLM che prepara la bozza, conferma di una persona | Bozza di reso da confermare, poi `returnCreate` | LLM in cloud (DPA, informativa) o locale (hardware) | Istruzioni nascoste nelle mail, errori di estrazione | Scelta del fornitore o del PC |
| **B3:** n8n al posto del programma per la lettura | Come B1/B2, via un secondo sistema | Installare e mantenere n8n | Licenza da chiarire se diventa parte del prodotto | Uso interno del negozio |

Le strade non si escludono: per esempio resi self-service attivi + risposta automatica con il link + coda delle mail
non riconosciute (B1) coprono i due canali senza LLM; A e B2 sono aggiunte sopra.

### Da provare su un negozio di sviluppo

- `reverseFulfillmentOrderDispose` con `RESTOCKED`: il disponibile sale una volta sola; poi «Process return» nel pannello
  non propone una seconda rimessa (212).
- Una unità `PROCESSING_REQUIRED` accetta in seguito `RESTOCKED` o `NOT_RESTOCKED`?
- La creazione, l'approvazione e la chiusura di un reso aggiornano `Order.updatedAt` (per il giro con `updated_at`)?
- `returnProcess` con `storeCreditRefund` e con rimborso sul metodo originale, con `notifyCustomer` vero e falso: quali
  email partono e in che lingua.
- `reverseDeliveryCreateWithShipping` con `notifyCustomer: false` e con un tracking BRT/Poste: cosa vede il cliente.
- Con il token client credentials, `returnProcess`, `refundCreate` e `shippingLabelPurchase` funzionano o chiedono un
  permesso utente?
- Un'estensione dell'account cliente nell'app del Dev Dashboard: si installa? scrive il metafield sull'ordine? il server
  lo legge?
- Un reso self-service da un ordine ospite: accesso con codice email e richiesta.
- La mail «Return request confirmation» basta come avviso di ricevimento del recesso (contenuto, data e ora)? (da far
  valutare anche alla parte legale)

## Fonti

Shopify, resi (shopify.dev)
- https://shopify.dev/docs/api/usage/versioning
- https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps
- https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management
- https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-self-serve-returns
- https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-fulfillment-orders
- https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/manage-reverse-deliveries
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Return
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnLineItem
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnReasonDefinition
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ReverseDelivery
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnPolicyProfile
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ReturnPoliciesReturnRules
- https://shopify.dev/docs/api/admin-graphql/latest/queries/returnReasonDefinitions
- https://shopify.dev/docs/api/admin-graphql/latest/queries/returnableFulfillments
- https://shopify.dev/docs/api/admin-graphql/latest/queries/orders
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Order
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnStatus
- https://shopify.dev/docs/api/admin-graphql/latest/enums/OrderReturnStatus
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ReverseFulfillmentOrderStatus
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ReverseFulfillmentOrderDispositionType
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnReason
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ReturnDeclineReason
- https://shopify.dev/docs/api/admin-graphql/latest/enums/RefundMethodAllocation
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRequest
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnProcess
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRefund
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseDeliveryCreateWithShipping
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseDeliveryShippingUpdate
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/reverseFulfillmentOrderDispose
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReturnProcessInput
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReturnProcessRefundInput
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/RefundMethodInput
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/StoreCreditRefundInput
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReverseFulfillmentOrderDisposeInput
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/ReverseDeliveryTrackingInput

Shopify, rimborsi, credito, collegamenti (shopify.dev)
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/refundCreate
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/RefundInput
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/storeCreditAccountCredit
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/StoreCreditAccountCreditInput
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/giftCardCreate
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/shippingLabelPurchase
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/carrierServiceCreate
- https://shopify.dev/docs/api/admin-graphql/latest/objects/DeliveryCarrierService
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout
- https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsBalanceTransaction
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/EmailInput
- https://shopify.dev/docs/api/usage/access-scopes
- https://shopify.dev/changelog/release-notes/2026-01
- https://shopify.dev/changelog/release-notes/2026-04
- https://shopify.dev/changelog/release-notes/2026-07
- https://shopify.dev/changelog/release-notes/2026-10
- https://shopify.dev/changelog/release-notes/2027-01

Shopify, account cliente e estensioni (shopify.dev)
- https://shopify.dev/docs/api/customer/latest/mutations/orderRequestReturn
- https://shopify.dev/docs/api/customer/latest/input-objects/RequestedLineItemInput
- https://shopify.dev/docs/apps/build/customer-accounts
- https://shopify.dev/docs/apps/build/customer-accounts/order-action-extensions
- https://shopify.dev/docs/api/customer-account-ui-extensions
- https://shopify.dev/docs/apps/build/customer-accounts/metafields
- https://shopify.dev/changelog/posts/checkout-and-customer-account-ui-extensions-available-by-default-in-new-development-shops

Shopify, centro assistenza (help.shopify.com)
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/creating-returns
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns
- https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup
- https://help.shopify.com/en/manual/compliance/legal/eu-right-of-withdrawal
- https://help.shopify.com/en/manual/customers/store-credit
- https://help.shopify.com/en/manual/fulfillment/managing-orders/refunding-orders
- https://help.shopify.com/en/manual/payments/shopify-payments/payouts/refunds
- https://help.shopify.com/en/manual/payments/shopify-payments/refunds-troubleshooting
- https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries
- https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries/italy
- https://help.shopify.com/en/manual/payments/manual-payments
- https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/shipping-labels/shipping-carriers
- https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/shipping-labels/shipping-carriers/brt
- https://help.shopify.com/en/manual/fulfillment/shopify-shipping/shipping-carriers/poste-italiane
- https://help.shopify.com/en/manual/fulfillment/setup/notifications/email-notifications
- https://help.shopify.com/en/manual/fulfillment/setup/notifications/email-variables
- https://help.shopify.com/en/manual/fulfillment/setup/notifications/exchange-notifications/return-approved
- https://help.shopify.com/en/manual/international/languages/checkout-and-notifications (non aperta)
- https://help.shopify.com/en/manual/shopify-flow
- https://help.shopify.com/en/manual/shopify-flow/reference/triggers
- https://help.shopify.com/en/manual/shopify-flow/reference/actions
- https://help.shopify.com/en/manual/shopify-flow/reference/actions/send-email
- https://help.shopify.com/en/manual/online-store/themes/customizing-themes/add-contact-page

App (Shopify App Store e documentazione dei fornitori)
- https://apps.shopify.com/inbox
- https://apps.shopify.com/returns-center-by-aftership
- https://support.aftership.com/en/articles/15389545-auto-update-return-status-to-shopify-with-shopify-returns-api
- https://support.aftership.com/en/articles/15389471-understanding-returns-and-exchanges-in-shopify-with-aftership-returns
- https://apps.shopify.com/loop-returns
- https://apps.shopify.com/returngo
- https://apps.shopify.com/return-prime
- https://apps.shopify.com/rich-returns
- https://apps.shopify.com/redo
- https://apps.shopify.com/easyreturns-1
- https://apps.shopify.com/sendcloud
- https://apps.shopify.com/outvio
- https://apps.shopify.com/qapla
- https://apps.shopify.com/fatture-italia
- https://apps.shopify.com/fatturaflow
- https://apps.shopify.com/eurofattura-it
- https://community.shopify.dev/t/new-eu-withdrawal-button-required-by-june-19-2026/35121 (forum, non fonte ufficiale)

Pagamenti
- https://www.paypal.com/it/cshelp/article/how-do-i-issue-a-refund-help101

Legge
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art52
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art53
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art54
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art54bis
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art56
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art57
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art59
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art133
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art135bis
- https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206~art135quater
- https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:02011L0083-20220528
- https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32023L2673
- https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32016R0679

WhatsApp (Meta)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started
- https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
- https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in
- https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint
- https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users
- https://whatsappbusiness.com/products/platform-pricing/

Posta, automazione, LLM
- https://github.com/n8n-io/n8n/blob/master/LICENSE.md
- https://docs.n8n.io/n8n-community-license/community-license/license-faq
- https://docs.n8n.io/choose-how-to-use-n8n
- https://docs.n8n.io/deploy/host-n8n/install-options/production-requirements
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.emailimap
- https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/deprecation-of-basic-authentication-exchange-online
- https://learn.microsoft.com/en-us/graph/api/user-list-messages
- https://learn.microsoft.com/en-us/microsoft-365/admin/email/about-shared-mailboxes
- https://knowledge.workspace.google.com/admin/sync/transition-from-less-secure-apps-to-oauth
- https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/list
- https://developers.google.com/workspace/gmail/api/guides/sync
- https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
- https://www.anthropic.com/legal/commercial-terms
- https://developers.openai.com/api/docs/guides/your-data
- https://aistudio.google.com/docs/terms
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
