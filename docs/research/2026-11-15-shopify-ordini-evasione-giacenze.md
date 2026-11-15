# Shopify: ordini, evasione e giacenze viste da un gestionale esterno

Data: 15/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina aperta il 15/11/2026). **DEDUZIONE** = conclusione
nostra a partire dai fatti. **IPOTESI** = da verificare con una prova su un negozio reale o di sviluppo.
"Non verificato" = viene dalla memoria o da fonti non ufficiali, senza conferma su shopify.dev.

## Domanda

Cosa espone Shopify, con le sue API ufficiali attuali, a un gestionale di magazzino esterno che deve:

1. importare gli ordini cliente e le loro righe, con date e stato;
2. segnare l'evasione e la spedizione;
3. leggere e scrivere le giacenze, e capire chi è la fonte di verità;
4. ricevere le notifiche delle modifiche, sapendo che il nostro server sta in sede e spesso non ha un indirizzo pubblico;
5. autenticarsi come app di un solo negozio, rispettare i limiti di frequenza e seguire le versioni delle API;
6. confrontare i concetti di Shopify con i nostri (ordine, riga, evasione, giacenza impegnata, location).

Contesto: base generica di gestionale di magazzino, in locale sulla rete aziendale, che assegna le scorte agli ordini né
evasi né spediti dal più vecchio (decisioni 2, 16, 21). Un magazzino reale non ha un gestionale e vende solo con
Shopify: lì il nostro prodotto diventa il gestionale principale (decisione 19). Un altro usa la giacenza «VEND» per la
merce già venduta che arriva e va subito al cliente (decisione 15). Non serve codice.

## Sintesi

1. **API da usare: GraphQL Admin API, versione stabile corrente 2026-10.** La REST Admin API è "legacy" dal 1/10/2024 e
   dal 1/4/2025 le nuove app pubbliche devono usare solo GraphQL. Esce una versione ogni tre mesi, ognuna resta
   accessibile almeno 12 mesi; la 2026-10 resta accessibile fino al 16/10/2027. (FATTO)
2. **Ordini: tutto quello che serve c'è.** `Order` ha `createdAt`, `processedAt`, `updatedAt`, `cancelledAt`, `name`
   (es. «#1001»), `displayFulfillmentStatus`, `test`; le righe (`LineItem`) hanno `quantity`, `currentQuantity`,
   `unfulfilledQuantity`, `sku`, `variant`. Di base si leggono solo gli ordini degli **ultimi 60 giorni**; per quelli più
   vecchi serve lo scope `read_all_orders`, che per un'app del proprio negozio non richiede approvazione. (FATTO)
3. **Evasione: si lavora sui `FulfillmentOrder`, non sull'ordine.** Shopify divide da solo ogni ordine in uno o più
   FulfillmentOrder, ognuno assegnato a una location; il magazzino li chiude creando `Fulfillment` (spedizioni), anche
   parziali, con numero di tracking. Il nostro «spedito» corrisponde al `Fulfillment` di Shopify; il nostro «evaso»
   (prelevato e pronto) non ha un equivalente preciso: il più vicino è segnare il FulfillmentOrder «in corso».
   (FATTO sul modello; DEDUZIONE sulla corrispondenza)
4. **Giacenze: Shopify tiene i suoi conti per location** con quantità con nome: `available`, `committed`,
   `reserved`, `damaged`, `safety_stock`, `quality_control`, `incoming`, `on_hand`. `committed` lo gestisce solo Shopify
   (gli ordini non evasi); un'app non può scriverlo. Shopify dice di usare l'impostazione assoluta
   (`inventorySetQuantities`) solo se chi chiama è la fonte di verità, altrimenti le variazioni (`inventoryAdjustQuantities`).
   Dalla versione 2026-04 queste scritture richiedono una chiave di idempotenza e il controllo "valore atteso"
   (`changeFromQuantity`). (FATTO)
5. **Notifiche: i webhook HTTPS richiedono che Shopify raggiunga il nostro server** (timeout 5 secondi, 8 tentativi in
   4 ore, poi la sottoscrizione creata via API viene cancellata). Le alternative ufficiali sono Google Cloud Pub/Sub e
   Amazon EventBridge, che però sono servizi cloud. Shopify stesso dice che i webhook non sono garantiti e consiglia un
   **lavoro periodico di riallineamento** che interroga le API con il filtro `updated_at`. (FATTO) Per un server in sede
   senza indirizzo pubblico la via più semplice è **solo interrogazione periodica** (polling) dal nostro server verso
   Shopify; Pub/Sub in modalità "pull" è un'alternativa che non richiede porte aperte ma introduce un account Google
   Cloud. (DEDUZIONE)
6. **Autenticazione:** dal 1/1/2026 non si creano più le vecchie "custom app" dal pannello di Shopify; le nuove app si
   creano nel **Dev Dashboard**. Per un server che lavora sul negozio della propria organizzazione c'è il
   **client credentials grant**: client ID + segreto → token valido 24 ore, da rinnovare. Funziona solo se app e negozio
   sono della stessa organizzazione Shopify. (FATTO)
7. **Limiti:** costo per query calcolato in punti; 100 punti/secondo sul piano Standard, 200 Advanced, 1000 Plus,
   2000 Enterprise; una singola query non può superare 1000 punti. Le bulk operations non hanno questi limiti e
   servono per l'importazione iniziale. (FATTO)
8. **Conclusione per l'architettura (DEDUZIONE):** il collegamento a Shopify serve a uno solo dei due magazzini noti,
   ha regole proprie (FulfillmentOrder, quantità con nome, 60 giorni, versioni trimestrali) e cambia ogni tre mesi.
   Conviene che la base definisca un **punto di estensione "canale di vendita"** neutro e che il connettore Shopify sia
   un modulo separato che lo implementa (specializzazione o modulo opzionale), non parte del nucleo.

## 1. Importare ordini e righe

### FATTI

- `Order` rappresenta la richiesta di acquisto di un cliente, dal checkout all'evasione.
  [Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order)
- Campi utili ([Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order)):
  - `name`: identificativo mostrato nel pannello e al cliente (es. «#1001», «EN1001»); non è unico tra negozi diversi.
  - `number`: numero usato per costruire `name`; **non è garantito sequenziale né unico**.
  - `createdAt`: data e ora di creazione, fissata al completamento del checkout, non cambia nel tempo.
  - `processedAt`: data e ora di elaborazione, che può essere diversa da `createdAt`.
  - `updatedAt`: ultima modifica. `cancelledAt` e `cancelReason`: annullamento.
  - `closed` / `closedAt`: un ordine è chiuso quando le righe sono evase o annullate e i pagamenti sono completi.
  - `confirmed`: "se la giacenza è stata riservata per l'ordine".
  - `displayFulfillmentStatus`: stato di evasione come lo vede il negoziante; per l'elaborazione dettagliata la
    documentazione rimanda a `FulfillmentOrder`.
  - `test`: ordine di prova (gateway di test); non si converte in ordine vero.
  - `edited`: se l'ordine ha subito modifiche (righe aggiunte o tolte, quantità, prezzi).
  - `fulfillmentOrders`, `fulfillments`, `lineItems`, `shippingAddress`, `tags`, `note`, `sourceName`.
- Valori di `displayFulfillmentStatus`: `UNFULFILLED`, `PARTIALLY_FULFILLED`, `FULFILLED`, `IN_PROGRESS`, `ON_HOLD`,
  `SCHEDULED`, `REQUEST_DECLINED`, `FULFILLMENT_NOT_REQUIRED`; `OPEN`, `PENDING_FULFILLMENT` e `RESTOCKED` sono
  sostituiti da altri valori.
  [OrderDisplayFulfillmentStatus](https://shopify.dev/docs/api/admin-graphql/latest/enums/OrderDisplayFulfillmentStatus)
- Nella 2026-10 `displayFulfillmentStatus` può restituire `FULFILLMENT_NOT_REQUIRED` invece di `UNFULFILLED` per ordini
  senza quantità ancora da evadere; chi mappa tutti gli stati deve gestire il nuovo valore.
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10) (voce del 3/7/2026)
- Sempre nella 2026-10: gli acquirenti possono chiedere di togliere righe non evase (`RequestedOrderEdit`, con tre nuovi
  argomenti webhook); `orderCancel` restituisce un `jobResult`.
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)
- Campi della riga `LineItem` ([LineItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem)):
  - `quantity`: unità ordinate, **comprese** quelle rimborsate e rimosse.
  - `currentQuantity`: unità ordinate, **escluse** quelle rimborsate e rimosse.
  - `unfulfilledQuantity`: unità non ancora evase.
  - `nonFulfillableQuantity`: unità che non si possono evadere (es. rimborsate).
  - `sku`, `variant`, `product`, `name`, `title` (titolo al momento dell'ordine), `requiresShipping`, `restockable`.
  - Deprecati: `fulfillableQuantity`, `fulfillmentService`, `fulfillmentStatus`.
- La query `orders` supporta paginazione a cursore (`first`/`after`), ordinamento (`sortKey`, predefinito
  `PROCESSED_AT`) e filtri testuali, tra cui `created_at`, `updated_at`, `processed_at`, `status`
  (open, closed, cancelled, not_closed), `fulfillment_status`, `financial_status`, `location_id`, `sku`, `test`.
  Esempio dalla pagina: `updated_at:>2019-12-01`.
  [orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)
- **60 giorni:** "di base sono accessibili solo gli ultimi 60 giorni di ordini" dall'oggetto `Order`; per i più vecchi
  serve `read_all_orders`, che non dà accesso da solo ma estende `read_orders`/`write_orders`.
  [Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order),
  [Access scopes](https://shopify.dev/docs/api/usage/access-scopes)
- Per le app custom (Dev Dashboard, organizzazione del negoziante) `read_all_orders` **non richiede approvazione** di
  Shopify: si aggiunge alla configurazione e si rilascia una nuova versione. Per le app pubbliche serve una richiesta.
  [Access scopes](https://shopify.dev/docs/api/usage/access-scopes)
- **Dati protetti dei clienti:** nome, indirizzo, email e telefono sono dati protetti, da richiedere campo per campo;
  i campi non approvati tornano `null` con un errore nella risposta (HTTP 200). Nella tabella dei livelli le app custom
  risultano "Always available" per i livelli 1 e 2.
  [Protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data)
- Paginazione: gli array in ingresso hanno al massimo 250 elementi; le liste di oggetti si fermano a 25.000.
  [API limits](https://shopify.dev/docs/api/usage/limits)

### DEDUZIONI

- La **data per l'ordinamento "dal più vecchio"** è `createdAt` (fissa). `processedAt` può differire (es. ordini
  importati). Quale usare è una scelta da registrare; `createdAt` è la più vicina alla nostra regola.
- **A parità di data vale il numero d'ordine** (decisione 16): con Shopify il numero non è garantito sequenziale né
  unico, quindi il nostro criterio di spareggio deve basarsi su un dato nostro (es. un progressivo assegnato
  all'importazione, o l'`id` di Shopify), non su `number`.
- La quantità da assegnare per riga è `unfulfilledQuantity` (o la `remainingQuantity` del FulfillmentOrder, sezione 2),
  non `quantity`, che include rimborsi e rimozioni.
- Gli ordini di prova (`test`) e quelli senza spedizione fisica (`requiresShipping` falso) vanno esclusi
  dall'assegnazione o trattati a parte.
- Il limite dei 60 giorni conta per l'importazione iniziale e per il riallineamento: senza `read_all_orders` un ordine
  rimasto aperto da più di due mesi sparisce dalla vista.
- Gli **ordini modificati** (`edited`, webhook `orders/edited`) cambiano le righe dopo l'importazione: il connettore deve
  poter aggiornare righe e quantità, e la nostra assegnazione deve rifarsi (decisione 16 già lo prevede).

## 2. Evasione e spedizione

### FATTI

- Un `FulfillmentOrder` rappresenta "un articolo o un gruppo di articoli di un ordine" che si prevede di evadere dalla
  **stessa location**; un ordine può averne più d'uno, anche nella stessa location. Shopify li crea da solo: "non è
  possibile creare manualmente i fulfillment order". Dopo la creazione dell'ordine un processo di instradamento decide
  le location e assegna i FulfillmentOrder.
  [FulfillmentOrder](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder)
- Campi: `assignedLocation`, `deliveryMethod`, `fulfillAt`, `fulfillBy`, `lineItems`, `requestStatus`,
  `supportedActions`, `fulfillmentHolds`, `order`. Le righe `FulfillmentOrderLineItem` hanno `totalQuantity`,
  `remainingQuantity`, `lineItem`, `inventoryItemId`, `sku`, `variant`.
  [FulfillmentOrder](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder),
  [FulfillmentOrderLineItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrderLineItem)
- Stati citati: `OPEN`, `SCHEDULED`, `ON_HOLD`, `IN_PROGRESS`, `INCOMPLETE`, `CLOSED`, `CANCELLED`. Dopo un'evasione
  parziale il FulfillmentOrder passa a `IN_PROGRESS`; dopo quella completa a `CLOSED`, che "non ha azioni supportate e
  non si può cambiare".
  [Build fulfillment solutions](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions),
  [FulfillmentOrder](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder)
- `Fulfillment` rappresenta "la spedizione fisica dei prodotti al cliente".
  [Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order)
- `fulfillmentCreate` crea un Fulfillment per uno o più FulfillmentOrder dello **stesso ordine e della stessa
  location**; si possono indicare righe e quantità (evasione parziale) o ometterle per evadere tutto; accetta dati di
  tracking (`company`, `number`, `url`) e `notifyCustomer`. Scope: uno tra `write_merchant_managed_fulfillment_orders`,
  `write_assigned_fulfillment_orders`, `write_third_party_fulfillment_orders`; l'utente deve avere il permesso
  `fulfill_and_ship_orders`.
  [fulfillmentCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreate),
  [Build fulfillment solutions](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions)
- Dalla 2024-10 si possono creare Fulfillment solo per FulfillmentOrder assegnati a una location gestita dal negoziante
  o a un servizio di evasione di proprietà dell'app.
  [Build fulfillment solutions](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions)
- `fulfillmentTrackingInfoUpdate` aggiorna corriere, numeri e URL di tracking di un Fulfillment, anche con più colli.
  [fulfillmentTrackingInfoUpdate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentTrackingInfoUpdate)
- `fulfillmentOrderReportProgress` "riporta l'avanzamento di un fulfillment order aperto o in corso"; il risultato è
  descritto come il FulfillmentOrder "su cui è stato indicato un aggiornamento 'segna come in corso'".
  [fulfillmentOrderReportProgress](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentOrderReportProgress)
- `fulfillmentOrderMove` sposta un FulfillmentOrder su un'altra location (solo location gestite dal negoziante).
  [Build fulfillment solutions](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions)
- **Due tipi di app per l'evasione:**
  - *App di gestione ordini* (order management app): evade per conto del negoziante dalle location del negoziante.
    [Order management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps)
  - *App servizio di evasione* (fulfillment service app): magazzino terzo; con `fulfillmentServiceCreate` Shopify crea
    una **location apposita**; il negoziante invia richieste di evasione che il servizio accetta o rifiuta, e solo dopo
    l'accettazione può creare Fulfillment. Shopify invia le richieste a `<callbackUrl>/fulfillment_order_notification`,
    chiama `/fetch_tracking_numbers.json` ogni ora se il tracking è attivo e `/fetch_stock.json` se il servizio gestisce
    la giacenza (richiesta completa una volta l'ora).
    [Fulfillment service apps](https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps),
    [Build for fulfillment services](https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps/build-for-fulfillment-services),
    [fulfillmentServiceCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentServiceCreate)
  - Se l'app non gestisce una location di servizio ma lavora sulle location del negoziante, la documentazione indica
    le app di gestione ordini.
    [Fulfillment service apps](https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps)
- **Prossima generazione dell'evasione:** spedizione e ritiro nello stesso ordine, spedizione divisa che diventa
  predefinita per i checkout idonei, spedizioni gestite dai Markets. "Tutte le app devono essere compatibili entro il
  1° luglio 2027." L'articolo avverte che le integrazioni che lavorano a livello di **ordine** invece che di
  **fulfillment order** possono rompersi.
  [Next-gen fulfillment](https://shopify.dev/changelog/blog/next-gen-fulfillment)

### DEDUZIONI

- Per un magazzino che **è** la location del negoziante (il caso del magazzino solo Shopify) la strada è l'**app di
  gestione ordini** sulle location del negoziante, non il servizio di evasione: il servizio crea una location nuova e
  vuole un `callbackUrl` raggiungibile da Shopify, che il nostro server in sede spesso non ha.
- Corrispondenza con la decisione 21:
  - «spedito» (merce uscita) → `fulfillmentCreate` con tracking. È l'unico passo che Shopify registra come evasione.
  - «evaso» (prelevato e pronto) → nessun equivalente esatto; si può segnare il FulfillmentOrder «in corso» con
    `fulfillmentOrderReportProgress`, oppure non comunicarlo a Shopify. Se lo segniamo come Fulfillment, il cliente
    potrebbe ricevere la notifica di spedizione prima che la merce esca.
- Poiché un ordine può avere più FulfillmentOrder e la spedizione divisa diventa predefinita entro luglio 2027, il
  connettore deve ragionare per **FulfillmentOrder e sue righe**, non per ordine intero.

## 3. Giacenze

### FATTI

- Modello: `InventoryItem` rappresenta la giacenza di una variante di prodotto (con `sku`, `tracked`,
  `requiresShipping`, `inventoryLevels`); `InventoryLevel` collega un InventoryItem a una `Location` e ha le
  `quantities(names:)` e `isActive`; `Location` è "un luogo fisico dove il negoziante tiene ed evade la merce".
  [InventoryItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem),
  [InventoryLevel](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel),
  [Location](https://shopify.dev/docs/api/admin-graphql/latest/objects/Location)
- Nella 2026-10 l'InventoryItem ha un campo `variants` (lista delle varianti che lo usano) e il campo singolo `variant`
  è deprecato. [InventoryItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem)
- Quantità con nome e scrivibilità
  ([Manage quantities and states](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states)):

  | Nome | Significato | Come si scrive |
  |---|---|---|
  | `available` | vendibile | set, adjust, move |
  | `committed` | impegnata da ordini non evasi, bozze riservate, trasferimenti pronti | **non scrivibile**, la gestisce Shopify |
  | `reserved` | in attesa, es. tenuta per un cliente | adjust, move |
  | `damaged` | danneggiata | adjust, move |
  | `safety_stock` | scorta di sicurezza contro la vendita oltre giacenza | adjust, move |
  | `quality_control` | in controllo qualità | adjust, move |
  | `incoming` | in arrivo, non ancora ricevuta | solo adjust |
  | `on_hand` | somma di available, committed, reserved, damaged, safety_stock, quality_control (non incoming) | solo set |

- Nel pannello di Shopify reserved, damaged, safety_stock e quality_control compaiono come «Non disponibile».
  Definizioni per il negoziante: "on hand" = tutte le unità nella location; "committed" = unità messe da parte e non
  vendibili, "come le unità in un ordine non evaso".
  [Inventory states (Help Center)](https://help.shopify.com/en/manual/products/inventory/fundamentals/inventory-states)
- Effetto degli ordini: Shopify diminuisce `available` per le varianti incluse in un ordine; dopo l'evasione diminuisce
  `committed`.
  [Inventory management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps)
- Vendita oltre giacenza: la variante ha `inventoryPolicy` = `DENY` (non si compra se esaurita) o `CONTINUE` (si compra
  anche se esaurita).
  [ProductVariantInventoryPolicy](https://shopify.dev/docs/api/admin-graphql/latest/enums/ProductVariantInventoryPolicy)
- Scritture:
  - `inventorySetQuantities` imposta valori assoluti di `available` o `on_hand`. La documentazione dice di usarla solo
    quando si chiama per conto del sistema che è **fonte di verità** della giacenza; altrimenti consiglia
    `inventoryAdjustQuantities`.
    [inventorySetQuantities](https://shopify.dev/docs/api/admin-graphql/latest/mutations/inventorySetQuantities)
  - `inventoryAdjustQuantities` applica variazioni (delta); `inventoryMoveQuantities` sposta tra stati.
  - **Controllo del valore atteso:** dalla 2026-04 ogni quantità deve avere `changeFromQuantity`; se il valore salvato
    è diverso la scrittura fallisce con `CHANGE_FROM_QUANTITY_STALE`. Si può passare `null` per saltare il controllo,
    "se sei la fonte di verità".
  - **Idempotenza:** la direttiva `@idempotent(key: ...)` è disponibile dalla 2026-01 ed è **obbligatoria** per queste
    scritture dalla 2026-04.
  - `reason` (es. `correction`, `received`, `cycle_count_available`, `shrinkage`, `damaged`) e
    `referenceDocumentUri` (URI libero che indica la causa, visibile nella cronologia del negoziante).
    `ledgerDocumentUri` (riferimento al movimento nel sistema esterno) è obbligatorio per gli stati diversi da
    `available` e vietato per `available`.
  - Dalla 2026-04 una scrittura su una location dove l'articolo non è attivo crea un livello **inattivo**; va attivato
    con `inventoryActivate` per poter vendere o evadere.
  [Manage quantities and states](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states),
  [inventorySetQuantities](https://shopify.dev/docs/api/admin-graphql/latest/mutations/inventorySetQuantities)

### DEDUZIONI

- **Fonte di verità.** Nel magazzino solo Shopify il nostro prodotto è il gestionale principale: la giacenza fisica
  (`on_hand`) la sappiamo noi, perché registriamo arrivi, rettifiche e uscite. L'impegno verso gli ordini web
  (`committed`) invece lo calcola Shopify al momento dell'ordine e noi non possiamo scriverlo. Quindi la verità è
  divisa: noi per il fisico, Shopify per l'impegno dei suoi ordini.
- **Cosa scrivere.** Scrivere `available` in modo assoluto rischia di cancellare un ordine arrivato nel frattempo
  (Shopify sposta l'unità da available a committed). Un nuovo ordine invece non cambia `on_hand`. Le opzioni sensate:
  (a) mandare solo **variazioni** (`inventoryAdjustQuantities` su `available`) per arrivi e rettifiche, e lasciare che il
  `Fulfillment` scali la merce uscita; (b) impostare `on_hand` assoluto con il controllo del valore atteso.
  In entrambi i casi bisogna evitare di **scalare due volte** la stessa uscita (una volta col Fulfillment, una volta con
  la nostra sincronizzazione). Va scelto e provato. (IPOTESI da verificare su un negozio di sviluppo)
- **Assegnazione diversa.** Shopify impegna la merce ordine per ordine al momento dell'acquisto e, con `CONTINUE`,
  lascia `available` andare sotto zero. Non fa un'assegnazione "dal più vecchio, con parziali, rifatta a ogni
  variazione" come la nostra (decisione 16). Le due logiche convivono: Shopify dice quanto è impegnato in totale, noi
  decidiamo quali ordini ricevono la merce fisica. La nostra assegnazione resta nella base.
- **VEND (decisione 15).** La merce già venduta che arriva corrisponde, in Shopify, a un ordine già impegnato con
  giacenza insufficiente. All'arrivo si registra l'entrata (variazione su `available` con motivo `received`) e poi il
  Fulfillment. «VEND» è un nostro concetto e non serve una quantità con nome apposita in Shopify; `reserved` esiste ma
  servirebbe a tutt'altro (merce tenuta per un cliente). (DEDUZIONE)
- La merce **prelevata ma non spedita** («evaso») per Shopify resta `committed` fino al Fulfillment: coerente con la
  nostra definizione, perché fisicamente è ancora in magazzino.
- `incoming` potrebbe riflettere gli ordini fornitore in arrivo, se il negoziante lo vuole vedere in Shopify; non è
  necessario per l'assegnazione.

## 4. Notifiche delle modifiche

### FATTI

- Una sottoscrizione webhook consegna a "un URL, un URI Google Pub/Sub o un ARN Amazon EventBridge".
  Shopify "non garantisce l'ordine all'interno di un argomento"; "la consegna non è sempre garantita"; per ordinare
  gli eventi si usa l'intestazione `X-Shopify-Triggered-At` o `updated_at`; i duplicati si scartano con
  `X-Shopify-Webhook-Id`; ogni consegna è firmata (`X-Shopify-Hmac-Sha256`). Shopify consiglia **lavori di
  riallineamento** che leggono periodicamente i dati.
  [Webhooks](https://shopify.dev/docs/apps/build/webhooks),
  [Best practices](https://shopify.dev/docs/apps/build/webhooks/best-practices)
- Consegna HTTPS: Shopify verifica i certificati SSL; timeout di connessione 1 secondo e di 5 secondi per l'intera
  richiesta; qualsiasi risposta diversa da 200 (anche i redirect) è un errore; **8 tentativi nelle 4 ore successive**;
  dopo 8 errori consecutivi la sottoscrizione creata via Admin API viene **cancellata** e parte un'email di avviso.
  [HTTPS delivery](https://shopify.dev/docs/apps/build/webhooks/subscribe/https)
- Google Pub/Sub: Shopify lo raccomanda come soluzione cloud; si crea un topic, si concede il ruolo Publisher
  all'account `delivery@shopify-pubsub-webhooks.iam.gserviceaccount.com`, l'indirizzo è `pubsub://{project-id}:{topic-id}`.
  [Get started](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started)
- Amazon EventBridge: indirizzo nel formato
  `arn:aws:events:<regione>::event-source/aws.partner/shopify.com/<APP-ID>/<nome>`. La vecchia mutazione dedicata
  `eventBridgeWebhookSubscriptionCreate` è deprecata: "usare invece webhookSubscriptionCreate".
  [Get started](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started),
  [eventBridgeWebhookSubscriptionCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/eventbridgewebhooksubscriptioncreate)
- **Next Gen Events** (generalmente disponibili dal 1/10/2026 con la 2026-10): "il successore dei webhook classici".
  Ogni sottoscrizione dichiara quali cambiamenti ricevere (`triggers`), quali dati (`query` GraphQL) e quali risultati
  consegnare (`query_filter`); si configurano in `shopify.app.toml`. 18 argomenti, tra cui `Order`,
  `FulfillmentOrder`, `InventoryItem`, `Location` (InventoryLevel non è citato). "Le integrazioni con i webhook classici
  esistenti continueranno a funzionare"; nessuna data di deprecazione annunciata.
  [Next Gen Events](https://shopify.dev/changelog/blog/next-generation-events-are-now-generally-available),
  [Release notes 2026-10](https://shopify.dev/changelog/release-notes/2026-10)
- Nelle sottoscrizioni Pub/Sub "pull" è il client che chiede i messaggi al server Pub/Sub.
  [Google Cloud, Pull subscriptions](https://docs.cloud.google.com/pubsub/docs/pull)
- Argomenti utili (tutti presenti nella 2026-10): `ORDERS_CREATE`, `ORDERS_UPDATED`, `ORDERS_CANCELLED`, `ORDERS_EDITED`,
  `ORDERS_FULFILLED`, `ORDERS_PARTIALLY_FULFILLED`, `FULFILLMENT_ORDERS_MOVED`, `FULFILLMENT_ORDERS_PLACED_ON_HOLD`,
  `FULFILLMENT_ORDERS_HOLD_RELEASED`, `FULFILLMENTS_CREATE`, `FULFILLMENTS_UPDATE`, `INVENTORY_LEVELS_UPDATE`,
  `INVENTORY_ITEMS_UPDATE`, `LOCATIONS_UPDATE`, `BULK_OPERATIONS_FINISH`, `APP_UNINSTALLED`.
  [WebhookSubscriptionTopic](https://shopify.dev/docs/api/admin-graphql/latest/enums/WebhookSubscriptionTopic)
- Interrogazione periodica: molte query supportano il filtro `updated_at` per leggere solo ciò che è cambiato
  dall'ultimo passaggio. [Best practices](https://shopify.dev/docs/apps/build/webhooks/best-practices),
  [orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)
- **Bulk operations:** `bulkOperationRunQuery` esegue in modo asincrono una query su qualsiasi connessione e produce un
  file JSONL scaricabile (link valido una settimana); fine segnalata dal webhook `bulk_operations/finish` o
  interrogando `bulkOperation(id:)`; dalla 2026-01 fino a 5 operazioni in parallelo per negozio e app; massimo 5
  connessioni e 2 livelli di annidamento; devono finire entro 10 giorni. Le app create nel Dev Dashboard non devono
  abilitarle.
  [Bulk operations](https://shopify.dev/docs/api/usage/bulk-operations/queries)

### DEDUZIONI

- Con un server in sede senza indirizzo pubblico i webhook HTTPS **non arrivano**. Per riceverli servirebbe esporre un
  indirizzo pubblico con certificato valido (porta aperta, proxy o tunnel), che tocca la sicurezza della rete
  aziendale: è una scelta dell'azienda, non nostra.
- Opzioni, dalla più semplice:
  1. **Solo polling** dal nostro server verso Shopify (solo traffico in uscita): ogni N minuti `orders` con
     `updated_at:>ultimo_passaggio`, più FulfillmentOrder e livelli di giacenza. È comunque il riallineamento che
     Shopify consiglia, quindi va fatto in ogni caso. Il ritardo è l'intervallo scelto.
  2. **Pub/Sub in pull:** Shopify pubblica su Google Cloud, il nostro server legge in uscita. Niente porte aperte, ma
     serve un account Google Cloud e un dato aziendale passa da un servizio in più.
  3. **EventBridge:** analogo, con AWS; per leggerlo da un server in sede serve un ulteriore servizio AWS (es. una coda),
     non documentato da Shopify. (IPOTESI)
  4. **Webhook HTTPS** verso un indirizzo pubblico: il più immediato, ma richiede raggiungibilità e risposta in 5 s.
- Con il nostro volume (un negozio) il polling ogni pochi minuti sta largamente nei limiti (sezione 5). Per
  l'importazione iniziale, o per riallineamenti estesi, si usano le bulk operations.
- La decisione 23 (senza rete il lavoro si ferma ma nulla si perde) vale anche verso Shopify: le scritture verso
  Shopify vanno messe in una coda persistente e ritentate; la chiave di idempotenza obbligatoria aiuta a non applicarle
  due volte.

## 5. Autenticazione, limiti e versioni

### FATTI

- **App create dal pannello (legacy):** "non è più possibile creare queste app"; le custom app create prima del
  1/1/2026 si gestiscono ancora dal pannello. Le nuove custom app si creano e gestiscono nel **Dev Dashboard**.
  [Authentication and authorization](https://shopify.dev/docs/apps/build/authentication-authorization),
  [Custom apps (Help Center)](https://help.shopify.com/en/manual/apps/app-types/custom-apps)
- Metodi: token exchange per app incorporate nel pannello; authorization code grant per app fuori dal pannello;
  **client credentials grant** per un'integrazione lato server che lavora sui negozi della propria organizzazione.
  I token offline persistono tra le sessioni e servono per lavori in background.
  [Authentication and authorization](https://shopify.dev/docs/apps/build/authentication-authorization)
- **Client credentials grant:** POST a `https://{negozio}.myshopify.com/admin/oauth/access_token` con
  `grant_type=client_credentials`, `client_id`, `client_secret`; "i token scadono dopo 24 ore" (`expires_in` 86399);
  "funziona solo quando app e negozio appartengono alla stessa organizzazione Shopify"; il segreto va tenuto fuori dal
  controllo versione.
  [Client credentials grant](https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/client-credentials-grant)
- Ogni richiesta GraphQL porta il token nell'intestazione `X-Shopify-Access-Token`; endpoint
  `https://{negozio}.myshopify.com/admin/api/2026-10/graphql.json`.
  [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql)
- **Scope** utili: `read_orders`/`write_orders` (+ `read_all_orders`), `read_inventory`/`write_inventory`,
  `read_locations`, `read_merchant_managed_fulfillment_orders`/`write_merchant_managed_fulfillment_orders`.
  La pagina degli scope indica che gli scope dei FulfillmentOrder richiedono approvazione di Shopify.
  [Access scopes](https://shopify.dev/docs/api/usage/access-scopes)
- **Limiti GraphQL:** costo calcolato in punti per ogni campo; 100 punti/s (Standard), 200 (Advanced), 1000 (Plus),
  2000 (Enterprise); una query non può superare 1000 punti; la risposta riporta `extensions.cost.throttleStatus`
  (`maximumAvailable`, `currentlyAvailable`, `restoreRate`); oltre il limite l'errore è `THROTTLED`. Le bulk operations
  non hanno questi limiti.
  [GraphQL Admin rate limits](https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits),
  [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql)
- Attesa consigliata dopo un rifiuto per limite: un secondo. Shopify può ridurre temporaneamente i limiti.
  [API limits](https://shopify.dev/docs/api/usage/limits)
- **Versioni:** una ogni tre mesi (1° giorno del trimestre, 17:00 UTC); ognuna supportata almeno 12 mesi, con almeno
  9 mesi di sovrapposizione. Stabili oggi: 2026-01 (fino al 16/1/2027), 2026-04 (16/4/2027), 2026-07 (16/7/2027),
  **2026-10 (ultima stabile, fino al 16/10/2027)**; release candidate 2027-01. Se si chiede una versione non più
  accessibile, Shopify risponde con la più vecchia accessibile ("fall forward") e lo segnala in `X-Shopify-API-Version`.
  [Versioning](https://shopify.dev/docs/api/usage/versioning)
- **REST:** "legacy dal 1° ottobre 2024"; "dal 1° aprile 2025 tutte le nuove app pubbliche devono usare solo la GraphQL
  Admin API". [REST Admin API](https://shopify.dev/docs/api/admin-rest)

### DEDUZIONI

- Per il magazzino solo Shopify, se il negozio e l'app stanno nella stessa organizzazione Shopify del negoziante, il
  client credentials grant è il più adatto a un server in sede: niente redirect, niente pagina pubblica. Il server
  deve rinnovare il token ogni 24 ore e custodire il segreto. Se invece l'app la crea un'altra organizzazione (es. chi
  installa il prodotto), questo metodo non funziona e serve l'authorization code grant, che vuole un indirizzo di
  ritorno raggiungibile dal browser di chi installa (non necessariamente da Internet). (IPOTESI sull'ultimo punto)
- Il costo delle versioni trimestrali è reale: almeno un aggiornamento all'anno per non cadere nel "fall forward", e
  modifiche obbligate come quelle della 2026-04 (idempotenza, `changeFromQuantity`). Chi mantiene il connettore deve
  seguire il changelog.
- REST non va usata per un connettore nuovo.

## 6. Concetti a confronto (per il glossario e i punti di estensione)

| Nostro concetto | Concetto Shopify | Uguale? (DEDUZIONE) |
|---|---|---|
| Ordine cliente | `Order` | Simile. Shopify lo divide in `FulfillmentOrder` per location; noi abbiamo un solo magazzino (decisione 26). |
| Riga d'ordine | `LineItem` (e `FulfillmentOrderLineItem`) | Simile. Quantità da evadere = `unfulfilledQuantity` / `remainingQuantity`, non `quantity`. |
| Data dell'ordine | `createdAt` (fissa) / `processedAt` | Va scelta quale usare per "dal più vecchio". |
| Numero d'ordine | `name` / `number` | `number` non è garantito sequenziale né unico: non adatto allo spareggio. |
| Articolo | `ProductVariant` + `InventoryItem` (SKU) | Il nostro articolo corrisponde alla variante; il collegamento più stabile è l'`InventoryItem`/variante, lo SKU è testo libero (case-sensitive). |
| Magazzino / ubicazione | `Location` | **Diverso.** La Location Shopify è un intero luogo (negozio, magazzino); le nostre ubicazioni sono posti dentro il magazzino. Un nostro magazzino = una Location Shopify. |
| Giacenza fisica | `on_hand` | Simile. |
| Giacenza impegnata | `committed` | **Diverso nel metodo.** Shopify impegna al momento dell'ordine, per location, senza ordine di anzianità; noi assegniamo dal più vecchio con parziali. |
| Disponibile | `available` | Simile, ma in Shopify può andare sotto zero con `CONTINUE`. |
| Evaso (prelevato e pronto) | nessun equivalente; al massimo FulfillmentOrder `IN_PROGRESS` | **Diverso.** |
| Spedito (uscito) | `Fulfillment` (con tracking) | Simile; in Shopify "fulfilled" vuol dire spedito o consegnato. Attenzione al falso amico: "fulfilled" ≠ nostro «evaso». |
| Giacenza «VEND» | nessuno | Concetto nostro. |
| Movimento di magazzino | `InventoryAdjustmentGroup` con `reason`, `referenceDocumentUri`, `ledgerDocumentUri` | Simile: Shopify accetta il riferimento al nostro movimento. |
| Annullamento ordine | `cancelledAt`, `orders/cancelled` | Simile; libera l'impegno. |

### DEDUZIONI: come fare il punto di estensione "canale di vendita"

- Il nucleo non deve conoscere Shopify. Deve avere un'interfaccia neutra, implementata da ogni connettore (Shopify,
  i due gestionali esistenti della decisione 19, un import da file):
  - **importa ordini**: ordini e righe in un formato nostro, con identificativo esterno (canale + id), data
    d'ordine, stato, quantità ancora da evadere, articolo esterno; incrementale ("cambiati dopo X");
  - **notifica modifiche**: il connettore decide se usare polling, webhook o coda; il nucleo riceve solo "ordine X
    cambiato";
  - **restituisci movimenti**: evaso, spedito (con tracking e righe/quantità), entrate e rettifiche di giacenza;
  - **mappa articoli e luoghi**: articolo nostro ↔ articolo esterno (per Shopify: variante/InventoryItem), magazzino
    nostro ↔ luogo esterno (Location);
  - **capacità dichiarate**: per esempio "sa ricevere l'evaso", "sa ricevere la giacenza", "è fonte di verità degli
    ordini"; Shopify non riceve l'evaso, un altro gestionale forse sì.
- Il connettore deve gestire **coda persistente, ritentativi e idempotenza** verso il canale (decisione 23 e
  obbligo Shopify dalla 2026-04), e un **riallineamento periodico** che confronti i dati.
- Il connettore deve poter **suddividere** un nostro ordine in più parti esterne (FulfillmentOrder) e ricomporle.
- La scelta di chi è fonte di verità per ogni dato (ordini: canale; giacenza fisica: noi; impegno: entrambi con regole
  diverse) va scritta per ogni installazione.
- Dove metterlo: nel nucleo l'interfaccia; il connettore Shopify è un modulo separato, attivato solo dove serve.
  Shopify cambia versione ogni tre mesi; tenerlo fuori dal nucleo evita che ogni aggiornamento di Shopify tocchi la base.

## Cosa resta incerto

- **Next Gen Events:** non è chiaro con quali metodi di consegna funzionino (l'esempio mostra solo un `uri`) né se
  sostituiranno i webhook classici con una data. Non cambiano il problema della raggiungibilità del server in sede.
- **Approvazione degli scope dei FulfillmentOrder:** la pagina degli scope dice che richiedono approvazione di
  Shopify; non è chiaro se valga anche per una custom app della propria organizzazione. Da verificare creando l'app.
- **Dati protetti dei clienti per le app del Dev Dashboard:** la tabella dice "sempre disponibile" per le custom app,
  ma non nomina il Dev Dashboard; da verificare (serve almeno l'indirizzo di spedizione se stampiamo etichette).
- **Doppio scarico della giacenza:** come combinare Fulfillment e nostra sincronizzazione senza scalare due volte va
  provato su un negozio di sviluppo; la documentazione dice che dopo l'evasione Shopify diminuisce `committed`, e da
  `on_hand` = somma deduciamo che anche `on_hand` cala, ma non l'abbiamo letto in modo esplicito.
- **Organizzazione proprietaria dell'app:** il client credentials grant funziona solo se app e negozio sono della
  stessa organizzazione. Chi crea l'app per il magazzino solo Shopify (il negoziante o noi) cambia il metodo di
  autenticazione. È una domanda per l'utente.
- **EventBridge:** i passi di configurazione (sorgente creata nel Dev Dashboard, collegamento a un event bus) non sono
  stati letti su una pagina ufficiale aperta; non verificati.
- **Valori completi** dell'enum `FulfillmentOrderStatus` e dei sort key degli ordini: le pagine lette non li
  elencavano tutti.
- **InventoryItem con più varianti:** il campo `variants` (lista) fa pensare che un InventoryItem possa essere condiviso
  da più varianti; non abbiamo trovato la regola esplicita. Conta per la mappatura articolo ↔ variante.
- **Indirizzo pubblico:** se l'azienda accetta di esporre un endpoint (webhook) non dipende da Shopify: va chiesto.
- **Volumi reali** del magazzino solo Shopify (ordini al giorno, articoli) non sono noti: servono per scegliere
  l'intervallo di polling.

## Fonti

Versioni, autenticazione, limiti
- https://shopify.dev/docs/api/usage/versioning
- https://shopify.dev/docs/api/admin-graphql
- https://shopify.dev/docs/api/admin-rest
- https://shopify.dev/docs/api/usage/limits
- https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits
- https://shopify.dev/docs/api/usage/access-scopes
- https://shopify.dev/docs/apps/build/authentication-authorization
- https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/client-credentials-grant
- https://help.shopify.com/en/manual/apps/app-types/custom-apps
- https://shopify.dev/docs/apps/launch/protected-customer-data
- https://shopify.dev/changelog/release-notes/2026-10

Ordini ed evasione
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Order
- https://shopify.dev/docs/api/admin-graphql/latest/enums/OrderDisplayFulfillmentStatus
- https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem
- https://shopify.dev/docs/api/admin-graphql/latest/queries/orders
- https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder
- https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrderLineItem
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreate
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentTrackingInfoUpdate
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentOrderReportProgress
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentServiceCreate
- https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps
- https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions
- https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps
- https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps/build-for-fulfillment-services
- https://shopify.dev/changelog/blog/next-gen-fulfillment

Giacenze
- https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps
- https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/inventorySetQuantities
- https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem
- https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Location
- https://shopify.dev/docs/api/admin-graphql/latest/enums/ProductVariantInventoryPolicy
- https://help.shopify.com/en/manual/products/inventory/fundamentals/inventory-states

Notifiche
- https://shopify.dev/docs/apps/build/webhooks
- https://shopify.dev/docs/apps/build/webhooks/best-practices
- https://shopify.dev/docs/apps/build/webhooks/subscribe/https
- https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/eventbridgewebhooksubscriptioncreate
- https://shopify.dev/docs/api/admin-graphql/latest/enums/WebhookSubscriptionTopic
- https://shopify.dev/docs/api/usage/bulk-operations/queries
- https://shopify.dev/changelog/blog/next-generation-events-are-now-generally-available
- https://docs.cloud.google.com/pubsub/docs/pull (Google Cloud, per la modalità pull di Pub/Sub)
