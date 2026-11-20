# Confronti per lo stack: schermate, canale aperto, installazione, posta dalla casella del responsabile

Data: 20/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina aperta il 20/11/2026) oppure misurato da me con il
comando indicato. **DEDUZIONE** = conclusione nostra a partire dai fatti. **IPOTESI** = da verificare con una prova.
**Non verificato** = dalla memoria o da fonti non ufficiali, senza conferma su una pagina ufficiale aperta. **Fonte di
parte** = l'unica fonte è chi produce o promuove lo strumento.

Ricerca precedente, da non ripetere: `docs/research/2026-11-20-librerie-stack.md` (versioni e licenze di Django,
Python, uvicorn, granian, psycopg, PostgreSQL, pgvector, Procrastinate, htmx 2/4, barcode, Caddy, Docker Engine e
Desktop, Compose, NVIDIA Container Toolkit, Podman, Watchtower; limiti SSE con HTTP/1.1; LISTEN/NOTIFY; SMTP AUTH di
Microsoft 365 spento a fine dicembre 2026; Google senza password dal 14/03/2025). Qui si rimanda a quella per tutto ciò
che c'è già e si aggiungono i confronti.

## Domanda

Con lo stack deciso (web app servita da un server in sede sulla rete interna; Python + Django + PostgreSQL; telefoni
Android e iPhone, palmari Android a grilletto, computer):

- **A.** Schermate preparate dal server con htmx, oppure app nel browser con un framework (React, Svelte, Vue), oppure
  una via di mezzo (htmx con «isole», Web Components/Lit, Alpine.js)? Contesto: molte schermate da gestionale (DDT,
  prelievo guidato, inventario, resi, Configurazione), uso soprattutto da telefono e palmare anche economici, versione da
  computer più ricca per i responsabili, fotocamera sempre accesa, operazioni in attesa in IndexedDB, canale aperto per
  aggiornare pezzi di schermo, niente lavoro senza rete, WCAG 2.2 AA, esito in 1–2 s.
- **B.** Canale aperto server → dispositivi: SSE, WebSocket, richieste a intervalli. Redis/Valkey, Django Channels,
  streaming di Django, LISTEN/NOTIFY; riconnessione, proxy, HTTP/2, telefoni in standby.
- **C.** Contenitori o macchine virtuali; buone pratiche di Compose; Windows con WSL2; GPU; Podman; Django in
  produzione (server ASGI, processi, connessioni al database, statici); PostgreSQL in contenitore.
- **D.** Posta inviata «dalla casella del responsabile con copia a lui»: Microsoft 365, Google Workspace, Aruba,
  Register.it; librerie Python.

## Sintesi

1. **La documentazione di htmx dice da sola dove htmx non va bene**: interfacce con molte dipendenze dinamiche fra
   parti dello schermo, **lavoro senza rete**, aggiornamenti molto frequenti dello stato (ogni input → richiesta),
   librerie di componenti fatte per React (shadcn/ui). Va bene per CRUD, moduli salvati nel database, aree di schermo
   ben delimitate. Il nostro caso è soprattutto CRUD con aree delimitate **e** niente lavoro senza rete: rientra nel
   caso favorevole; fanno eccezione fotocamera e coda in IndexedDB, che richiedono JavaScript proprio in ogni caso.
   (FATTO, saggio di Carson Gross sul sito htmx: fonte di parte)
2. **Peso del JavaScript misurato sui pacchetti npm di oggi** (gzip -9, file distribuiti): htmx 4.0.2 **13,4 KB**
   (+2,4 KB `hx-sse`), htmx 2.0.11 16,8 KB, Lit ~6,2 KB, Preact 5,0 KB, Alpine 19,9 KB, Vue 3.5 runtime 43,0 KB,
   **React DOM 19.3 client 110,5 KB** (file non minificato: con un bundler sarà meno, non misurato). Su un telefono
   economico lo stesso JavaScript costa **oltre 6 volte** il tempo di un telefono di fascia alta (V8, 2019). (FATTO)
3. **Il caso Contexte (React → htmx)** riporta −67% di codice, da 255 a 9 dipendenze JavaScript, caricamento da 2–6 s a
   1–2 s, memoria da 75 a 45 MB; è **pubblicato sul sito di htmx** e dice esso stesso che l'app era «estremamente
   adatta» all'ipermedia e che non tutte vedranno questi numeri. (FATTO, fonte di parte)
4. **Animate UI non è MIT puro**: licenza «MIT + Commons Clause» (vietato rivendere o ridistribuire i componenti come
   tali). shadcn/ui è MIT. Animate UI ha senso solo con React. (FATTO)
5. **View Transitions API ora c'è ovunque nei motori principali**: Chrome 111, **Safari 18** (iOS 18), **Firefox 144**
   per le transizioni nello stesso documento; fra pagine diverse (`@view-transition`) Chrome 126 e Safari 18.2, Firefox
   solo in anteprima. htmx 4 le supporta ma **spente per default**; React 19.3 (09/09/2026) ha reso stabile
   `<ViewTransition>`. (FATTO, MDN browser-compat-data)
6. **Redis non è più BSD dal 7.4**: 7.4 RSALv2/SSPLv1; **da Redis 8 si può scegliere anche AGPLv3** (annuncio
   01/05/2025). Ultima stabile 8.10.3. **Valkey** (fork di Redis 7.2.4, Linux Foundation dal 28/03/2024) è **BSD-3**,
   ultima 9.2.0 (18/11/2026). Per noi Redis non serve: il campanello è LISTEN/NOTIFY. (FATTO + DEDUZIONE)
7. **Django Channels è fermo**: ultima 4.3.2 del 20/11/2025, classificatori fino a **Django 6.0** (non 6.1); l'unico
   channel layer ufficiale per la produzione è **channels_redis**. Per SSE non serve Channels: basta
   `StreamingHttpResponse` asincrona sotto ASGI. (FATTO)
8. **PgBouncer in modalità transaction rompe LISTEN** («Never») e i lock di sessione: chi ascolta LISTEN deve usare una
   connessione diretta (o pooler in modalità session). (FATTO)
9. **iPhone e connessioni aperte**: bug WebKit 308073 (aperto, febbraio 2026, Safari 26.3) — dopo il ritorno da
   background **un nuovo WebSocket verso un server in LAN resta bloccato in «connessione»** finché non si ricarica la
   pagina. Per EventSource non ho trovato documentazione Apple. Chrome consiglia di chiudere le connessioni quando la
   pagina è nascosta/congelata e riaprirle al ritorno. Questo pesa a favore di **SSE + riallineamento dello stato** e
   contro WebSocket. (FATTO + DEDUZIONE)
10. **Contenitori contro VM (IBM Research, 2014)**: Docker uguale al nativo su CPU e memoria; KVM −22% in compressione,
    metà degli IOPS casuali, MySQL oltre −40%; ma la **rete NAT di Docker raddoppia la latenza** di una richiesta-risposta
    e i file nello strato AUFS costano: usare volumi. Misure vecchie (Docker 1.0, kernel 3.11). (FATTO)
11. **Docker Machine è archiviato (18/07/2025)** e la documentazione lo dà «non più mantenuto». **Il driver di log di
    default di Docker non ruota i log**: usare il driver `local` o `max-size`/`max-file`. (FATTO)
12. **WSL2**: file del progetto e volumi vanno nel filesystem Linux, non in `/mnt/c` (più lento, niente notifiche di
    modifica); WSL2 di default è in **NAT** e non è raggiungibile dalla LAN senza `netsh portproxy` o la modalità
    **mirrored** (Windows 11 22H2+). GPU in WSL2: solo driver Windows, `--gpus all`, NVML parziale. (FATTO)
13. **Posta Microsoft 365 «a nome di alcune caselle»**: la via attuale è **RBAC for Applications** di Exchange Online
    (ruolo `Application Mail.Send` limitato a un gruppo/ambito di caselle), che **sostituisce le Application Access
    Policy**; attenzione: il permesso va **tolto** da Entra ID, altrimenti l'ambito non limita nulla; le modifiche
    impiegano **da 30 minuti a 2 ore**. (FATTO)
14. **Google Workspace**: delega a livello di dominio per un account di servizio (la configura un **super
    amministratore**, fino a 24 ore per l'effetto); `gmail.send` è uno scope «sensibile», ma con app di tipo
    **Internal** non serve la verifica di Google. (FATTO)
15. **Aruba e Register.it**: SMTP con **password** (Aruba `smtps.aruba.it:465`, Register.it
    `authsmtp.securemail.pro:465`); nessuna menzione di OAuth nelle guide ufficiali; Aruba prevede la **password per il
    programma di posta** quando è attiva la verifica in due passaggi (documentato per la PEC). (FATTO)

## A. Schermate

### FATTI: cos'è htmx e cosa non fa bene secondo i suoi autori

- htmx è una libreria JavaScript senza dipendenze che «permette di accedere a funzioni moderne del browser direttamente
  dall'HTML»: attributi `hx-get`/`hx-post`/… inviano richieste, `hx-trigger` sceglie l'evento, `hx-target` dove mettere
  la risposta, `hx-swap` come inserirla; il server restituisce **frammenti HTML**, non JSON. Niente build, basta un
  `<script>`. [Documentazione htmx 2](https://htmx.org/docs/)
- htmx 4 (differenze dalla 2): ereditarietà degli attributi **esplicita** (`:inherited`); le risposte 4xx/5xx vengono
  inserite per default; la cronologia ricarica la pagina dal server invece di una copia locale; **morphing incluso**
  (`innerMorph`, `outerMorph`, prima serviva Idiomorph); SSE e WebSocket come estensioni `hx-sse`/`hx-ws` distribuite
  nello stesso pacchetto. [Documentazione htmx 4](https://four.htmx.org/docs/)
- Saggio «When Should You Use Hypermedia?» (Carson Gross, autore di htmx, 23/10/2022; **fonte di parte**)
  [htmx.org](https://htmx.org/essays/when-to-use-hypermedia/):
  - adatto: app di testo e immagini, **CRUD** («se la meccanica principale è mostrare moduli e salvarli nel database,
    l'ipermedia funziona molto bene»), interfacce annidate con aree di aggiornamento ben definite, link profondi e primo
    caricamento veloce;
  - non adatto: **molte dipendenze dinamiche** fra parti dello schermo (esempio: un foglio di calcolo), **funzionamento
    completo senza rete** (Service Worker possibili ma complessi), **aggiornamenti molto frequenti** (es. giochi guidati
    dal mouse), librerie di componenti «copia e incolla» pensate per React come shadcn, squadra non convinta;
  - propone un approccio «di transizione» che mescola ipermedia e componenti da SPA, funzione per funzione.

### FATTI: versioni e licenze

Versioni dal registro npm (API JSON, 20/11/2026); htmx è nella ricerca precedente.

| Pacchetto | Licenza | Versione «latest» | Data | Note dalla fonte |
|---|---|---|---|---|
| react / react-dom | MIT | 19.3.1 | 14/10/2026 | 19.0 stabile dal 05/12/2024; **19.3 (09/09/2026)**: `<ViewTransition>` e Fragment Refs stabili. Dal 24/02/2026 React è nella React Foundation (Linux Foundation). [React 19](https://react.dev/blog/2024/12/05/react-19), [React 19.3](https://react.dev/blog/2026/09/09/react-19-3), [blog](https://react.dev/blog) |
| svelte | MIT | 5.59.1 | 20/11/2026 | un **compilatore** trasforma i componenti in JavaScript ottimizzato; SvelteKit è il framework applicativo. [Svelte](https://svelte.dev/docs/svelte/overview) |
| vue | MIT | 3.5.46 | 20/11/2026 | — [npm](https://www.npmjs.com/package/vue) |
| lit | BSD-3-Clause | 3.3.3 | 14/05/2026 | classe base per **Web Components**; «circa 5 KB minificato e compresso»; funziona in HTML semplice e con pagine preparate dal server. [Lit](https://lit.dev/docs/) |
| alpinejs | MIT | 3.17.5 | 20/10/2026 | direttive `x-data`, `x-on`, `x-show`…; **la build normale richiede `unsafe-eval` nella CSP** (usa il costruttore `Function`); esiste la build `@alpinejs/csp` con limiti (niente arrow function, template literal, `x-html`…). [Start](https://alpinejs.dev/start-here), [CSP](https://alpinejs.dev/advanced/csp) |
| preact | MIT | 11.2.0 | 06/11/2026 | alternativa leggera con API simile a React (non approfondita) |
| shadcn (CLI di shadcn/ui) | MIT ([LICENSE](https://raw.githubusercontent.com/shadcn-ui/ui/main/LICENSE.md)) | 4.23.0 | 27/10/2026 | «non è una libreria di componenti, è il modo di costruire la tua»: si copia il codice sorgente. [shadcn/ui](https://ui.shadcn.com/docs) |
| @animate-ui/react | **MIT + Commons Clause** ([LICENSE.md](https://raw.githubusercontent.com/imskyleen/animate-ui/main/LICENSE.md)) | 2.4.6 | 15/11/2026 | uso commerciale consentito «purché non si vendano o ridistribuiscano i componenti stessi nella forma originale, da soli o in un pacchetto» |
| motion (usato da Animate UI) | MIT | 14.14.0 | 13/11/2026 | — |

### FATTI: peso del codice scaricato (misura mia, riproducibile)

Metodo: `npm pack <pacchetto>@<versione>`, poi `wc -c` e `gzip -9c | wc -c` sui file distribuiti. Brotli non era
disponibile nella macchina. Non è il peso finale di un'app: un bundler toglie il codice non usato (tree shaking) e
aggiunge il codice dell'app.

| File | Minificato? | Byte | gzip -9 |
|---|---|---|---|
| htmx.org 4.0.2 `dist/htmx.min.js` | sì | 37.477 | **13.387** |
| htmx.org 4.0.2 `dist/ext/hx-sse.min.js` | sì | 5.912 | 2.356 |
| htmx.org 2.0.11 `dist/htmx.min.js` | sì | 52.182 | 16.838 |
| lit-html 3.3.3 + lit-element 4.2.2 + @lit/reactive-element 2.1.2 | sì | 14.739 | ~6.226 (somma dei tre file compressi separatamente) |
| preact 11.2.0 `dist/preact.mjs` | sì | 11.970 | 4.997 |
| alpinejs 3.17.5 `dist/cdn.min.js` | sì | 55.935 | 19.911 |
| vue 3.5.46 `vue.runtime.global.prod.js` (senza compilatore di template) | sì | 114.668 | 43.003 |
| vue 3.5.46 `vue.global.prod.js` (con compilatore) | sì | 174.069 | 63.285 |
| react-dom 19.3.1 `cjs/react-dom-client.production.js` | **no** (codice leggibile, 18.660 righe) | 625.168 | 110.528 |
| react 19.3.1 `cjs/react.production.js` | no | 18.040 | 4.626 |
| svelte 5.59.1 | — | non misurato: il runtime dipende da cosa il compilatore include | — |

- React 19 non distribuisce più un file minificato pronto per il browser (non ci sono build UMD nel pacchetto letto): il
  peso reale dopo la minificazione del bundler **non l'ho misurato** (nessun minificatore disponibile senza installare
  pacchetti). Togliendo solo commenti e rientri il file scende a 98.522 byte gzip.
- La documentazione di htmx 2 non dà un peso in KB; Lit dichiara «circa 5 KB» (coerente con la misura).

### FATTI: costo del JavaScript e reattività

- «The cost of JavaScript in 2019» (Addy Osmani, Mathias Bynens, team V8 di Chrome, 25/06/2019)
  [v8.dev](https://v8.dev/blog/cost-of-javascript-2019): i costi dominanti sono **scaricamento ed esecuzione**; lo
  stesso JavaScript (Reddit) impiega **3–4 volte** di più su un telefono medio (Moto G4) e **oltre 6 volte** su un
  telefono sotto i 100 dollari (Alcatel 1X) rispetto a un Pixel 3; consiglio di spezzare i pacchetti oltre **50–100 kB**
  e di spedire molto meno script ai telefoni. Misure del 2019: per i telefoni di oggi **non ho trovato** una misura
  primaria equivalente.
- **INP** (Interaction to Next Paint): misura la latenza di tocchi, clic e tasti per tutta la visita e riporta la
  peggiore (escludendo valori anomali); buono **≤ 200 ms**, da migliorare fino a 500 ms, scarso oltre; si valuta al
  **75° percentile** dei caricamenti reali. È il Core Web Vital che ha preso il posto di FID.
  [web.dev INP](https://web.dev/articles/inp)
- L'API su cui si basa INP (Event Timing, `interactionId`) c'è in Chrome 96, Firefox 144 e **Safari 26.2**.
  [BCD PerformanceEventTiming](https://github.com/mdn/browser-compat-data/blob/main/api/PerformanceEventTiming.json)

### FATTI: il caso Contexte (React → htmx)

Fonte: [htmx.org, «A Real World React → htmx Port»](https://htmx.org/essays/a-real-world-react-to-htmx-port/) (Carson
Gross, 29/09/2022), che riassume il talk di David Guillot a DjangoCon 2022. **Fonte di parte** (sito di htmx); il video
del talk non l'ho aperto.

| Misura | React | htmx (Django template) |
|---|---|---|
| Righe di codice | 21.500 | 7.200 (−67%) |
| Righe Python | 500 | 1.200 (+140%) |
| Dipendenze JavaScript | 255 | 9 |
| Tempo di build web | 40 s | 5 s |
| Primo caricamento fino all'interattività | 2–6 s | 1–2 s |
| Memoria | 75 MB | 45 MB |
| Sforzo | 2 anni di lavoro in React | circa 2 mesi di porting |

Avvertenze scritte nella pagina: app di contenuti (testo e immagini) «estremamente adatta all'ipermedia»; «non ci
aspettiamo che ogni applicazione veda numeri simili»; esperienza utente dichiarata invariata. Non indica hardware né
metodo di misura.

### FATTI: accessibilità con aggiornamenti parziali

- **WCAG 2.2, SC 4.1.3 Status Messages (livello AA)**: i messaggi di stato devono poter essere annunciati dalle
  tecnologie assistive **senza ricevere il focus**; tecniche: `role="status"` (esiti), `role="alert"` (errori e
  avvisi), regioni `aria-live`, `role="log"`. [Understanding 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- MDN: la regione live deve **esistere nella pagina prima** del cambiamento («il modo più affidabile è metterla nel
  markup iniziale»); se la si crea con JavaScript, aggiornarne il contenuto in un task successivo; `polite` per quasi
  tutto, `assertive` solo per l'urgente; **`aria-live` insieme a `role="alert"` fa parlare due volte VoiceOver su
  iOS**. [MDN Live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions)
- htmx: la documentazione raccomanda HTML semantico, focus visibile, etichette, contrasto; con `hx-boost` link e moduli
  funzionano anche senza JavaScript. Sul focus dice poco: `focus-scroll` (default spento), `hx-preserve` per tenere
  elementi fra uno scambio e l'altro, e il **morphing che «conserva meglio focus e stato dei video»**.
  [htmx 2](https://htmx.org/docs/), [htmx 4](https://four.htmx.org/docs/)
- React/Svelte/Vue: nelle pagine lette non c'è una gestione automatica del focus o degli annunci al cambio di schermata
  (in un'app nel browser il cambio di «pagina» non è una navigazione vera e il lettore di schermo non lo annuncia da
  sé: **dalla memoria, non verificato** su una fonte primaria in questa ricerca).
- Web Components: gli elementi personalizzati autonomi ci sono ovunque (Chrome 54, Firefox 63, Safari 10.1), ma
  l'estensione di elementi nativi (`is="..."`, «customized built-in») **non c'è in Safari**.
  [BCD CustomElementRegistry](https://github.com/mdn/browser-compat-data/blob/main/api/CustomElementRegistry.json)

### FATTI: View Transitions

Dati MDN browser-compat-data (ramo main, 20/11/2026); Chrome Android, Edge, WebView e Samsung Internet seguono Chrome;
Safari iOS segue Safari.

| Funzione | Chrome | Safari | Firefox |
|---|---|---|---|
| `document.startViewTransition()` (stesso documento) | 111 | **18** | **144** |
| opzione con `types` | 125 | 18.2 | 147 |
| `@view-transition` (fra pagine diverse) | 126 | 18.2 | solo anteprima |
| `ViewTransition.waitUntil()` | 144 | no | no |

Fonti: [Document.json](https://github.com/mdn/browser-compat-data/blob/main/api/Document.json),
[ViewTransition.json](https://github.com/mdn/browser-compat-data/blob/main/api/ViewTransition.json),
[view-transition.json](https://github.com/mdn/browser-compat-data/blob/main/css/at-rules/view-transition.json).

- htmx 2: `transition:true` in `hx-swap` o `htmx.config.globalViewTransitions`; se il browser non la supporta fa uno
  scambio normale. htmx 4: `htmx.config.transitions` **default `false`**; la dissolvenza di default di 250 ms è definita
  dalla documentazione stessa «un pessimo default» da sovrascrivere.
- React 19.3: `<ViewTransition>` stabile; animano solo gli aggiornamenti marcati come Transition.

### FATTI: integrazione con Django

| Pacchetto | Licenza | Versione e data | Note |
|---|---|---|---|
| django-htmx | MIT | 1.29.0, 05/08/2026 | «strumenti per le estensioni HTTP di htmx»; classificatori Django 5.2, 6.0, **6.1**. [docs](https://django-htmx.readthedocs.io/en/latest/), [PyPI](https://pypi.org/project/django-htmx/) |
| Django REST Framework | BSD-3-Clause | 3.18.3, 06/10/2026 | API JSON per un frontend nel browser. [PyPI](https://pypi.org/project/djangorestframework/) |
| Django Ninja | MIT | 1.8.0, 08/11/2026 | API con type hints e Pydantic, OpenAPI automatico, viste async; il benchmark linkato è nel repository dell'autore (**fonte di parte**). [sito](https://django-ninja.dev/), [PyPI](https://pypi.org/project/django-ninja/) |
| django-cotton | MIT | 2.9.0, 08/11/2026 | componenti di template (non approfondito). [PyPI](https://pypi.org/project/django-cotton/) |
| django-components | MIT | 1.0.0, 18/11/2026 | componenti di template (non approfondito). [PyPI](https://pypi.org/project/django-components/) |

### DEDUZIONI

- **Il nostro profilo è quello che il saggio di htmx dice adatto**: moduli, elenchi, conferme, aree di schermo ben
  delimitate (riga del prelievo, totale del DDT, stato della coda), esito dal server in 1–2 s, e soprattutto **niente
  lavoro senza rete**, che toglie l'argomento più forte a favore di un'app nel browser. Il limite «aggiornamenti molto
  frequenti» non ci riguarda: una lettura di barcode o un tocco al secondo con risposta del server in rete locale è nel
  campo di htmx.
- **Le parti che restano JavaScript proprio in ogni caso** sono le stesse con qualunque scelta: inquadratura della
  fotocamera (getUserMedia + BarcodeDetector/zxing), coda delle operazioni in IndexedDB con invio e conteggio, gestione
  di visibilità/riconnessione del canale. Con htmx vanno scritte come **moduli piccoli o Web Components** (Lit o
  elementi personalizzati senza libreria) e messe **fuori dalle aree che htmx sostituisce** (o protette con
  `hx-preserve`), così la telecamera non si spegne a ogni aggiornamento. Questa è di fatto la «via di mezzo»: htmx per
  le schermate, pochi componenti per fotocamera e coda.
- **Peso**: htmx 4 + `hx-sse` + un componente Lit ≈ 22 KB gzip; un'app React parte da almeno ~100 KB di sola libreria
  (prima del codice dell'app e di eventuali librerie di componenti). Sui palmari e Android economici il costo di
  esecuzione è moltiplicato (×3–6 nelle misure V8 del 2019). Con molte schermate un'app nel browser cresce con il
  numero di schermate; con htmx cresce il codice Python/template sul server. **Va misurato INP sui dispositivi veri**
  (IPOTESI: con htmx l'INP dipende soprattutto dal tempo di risposta del server e dallo scambio del DOM; con React anche
  dal rendering nel telefono).
- **Alpine.js** costa più di htmx (≈ 20 KB) e nella build normale richiede `unsafe-eval` nella CSP: se si vuole una CSP
  rigida (consigliabile per un gestionale) bisogna usare la build CSP, con limiti. È utile per piccoli stati locali
  (aprire/chiudere, contatori) ma non necessario se i pochi componenti sono Web Components.
- **Versione da computer più ricca** (tabelle ordinabili, filtri, più colonne): con htmx si fa con frammenti più grandi
  e richieste con parametri; una griglia molto interattiva (modifica in linea di molte celle con dipendenze) è il punto
  in cui un'«isola» JavaScript potrebbe servire. Da decidere quando si disegnano quelle schermate, non ora.
- **Accessibilità**: in entrambe le vie il lavoro è lo stesso e va fatto a mano: regioni `role="status"` /
  `aria-live` presenti dall'inizio **fuori** dai frammenti sostituiti (se htmx sostituisce la regione stessa con
  `outerHTML`, l'annuncio può perdersi: deduzione dalla regola MDN), focus spostato esplicitamente dopo gli esiti che
  cambiano contesto, niente doppio `role="alert"` + `aria-live`. Con htmx 4 il morphing aiuta a non perdere il focus
  negli aggiornamenti dal canale aperto.
- **Animazioni**: le View Transitions ora coprono Safari 18+ e Firefox 144+, quindi non servono librerie per le
  transizioni fra stati; in htmx 4 vanno accese esplicitamente e la durata di default va cambiata. Animate UI (React,
  licenza con Commons Clause) e shadcn/ui (React) hanno senso solo scegliendo React: con htmx non si usano.
- **Se React**: API JSON con DRF o Django Ninja (doppio modello dati: serializzatori + tipi nel frontend), build con
  Vite, routing nel browser; il caso Contexte (fonte di parte) indica l'ordine di grandezza della differenza di codice,
  non una previsione per noi.
- **htmx 2 o 4**: la 4 include `hx-sse` nello stesso pacchetto 0BSD, il che **risolve il dubbio di licenza**
  dell'estensione SSE per la 2.x segnalato nella ricerca precedente; resta il fatto che la 4 non è ancora «latest» su
  npm (lo sarà nel 2027).

## B. Canale aperto server → dispositivi

### FATTI: le tre tecniche

- **SSE (EventSource)**: solo server → browser, su una normale risposta HTTP `text/event-stream`; il browser **si
  riconnette da solo** e manda `Last-Event-ID`; con HTTP/1.1 massimo 6 connessioni per dominio fra tutte le schede, con
  HTTP/2 stream multiplexati (vedi ricerca precedente). Supporto: Chrome 6, Firefox 6, Safari 5.
  [BCD EventSource](https://github.com/mdn/browser-compat-data/blob/main/api/EventSource.json)
- **WebSocket**: bidirezionale; lo standard **non prevede la riconnessione automatica** (in caso di errore `error` e poi
  `close` con codice 1006; quando il documento sparisce si chiude con 1001).
  [WebSockets Standard](https://websockets.spec.whatwg.org/)
- **Richieste a intervalli (polling) e long polling**: normali richieste HTTP; Django cita il long polling fra i casi
  che sotto ASGI non bloccano altre richieste. [Django request/response](https://docs.djangoproject.com/en/6.1/ref/request-response/)

### FATTI: Django

- `StreamingHttpResponse`: sotto WSGI «Django è pensato per richieste brevi» e lo streaming «occupa un processo worker
  per tutta la durata»; sotto **ASGI** non blocca le altre richieste e «apre la possibilità di richieste lunghe … long
  polling e server-sent events». Iteratore **asincrono** sotto ASGI (altrimenti viene consumato tutto, vanificando lo
  streaming); niente `ETag`/`Content-Length`; alla disconnessione del client Django cancella la coroutine
  (`asyncio.CancelledError`). [Django request/response](https://docs.djangoproject.com/en/6.1/ref/request-response/)
- Django da solo **non gestisce WebSocket**: serve Django Channels (dalla struttura della documentazione di Channels;
  Django non ha un'API WebSocket nelle pagine lette).

| Componente | Licenza | Versione e data | Note |
|---|---|---|---|
| channels | BSD | 4.3.2, **20/11/2025** | classificatori Django 4.2–**6.0**, Python 3.9–3.14. [PyPI](https://pypi.org/project/channels/), [release notes](https://channels.readthedocs.io/en/latest/releases/index.html) |
| channels-redis | BSD | 4.3.0, 22/07/2025 | «l'unico channel layer ufficiale mantenuto da Django supportato in produzione»; `InMemoryChannelLayer` «non usare in produzione». [Channel layers](https://channels.readthedocs.io/en/latest/topics/channel_layers.html) |
| channels-postgres | MIT nei metadati PyPI, **BSD-3 nel file LICENSE** del repository | 1.1.4, 06/11/2025 | channel layer su PostgreSQL con `psycopg_pool`, tabelle proprie, coda `asyncio.Queue` in memoria, nessun benchmark. [PyPI](https://pypi.org/project/channels-postgres/), [repository](https://github.com/danidee10/channels_postgres) |
| daphne | BSD | 4.2.3, 21/07/2026 | server ASGI del progetto Channels. [PyPI](https://pypi.org/project/daphne/) |
| django-eventstream | MIT | 5.3.4, 29/05/2026 | SSE per Django in ASGI; eventi salvati opzionalmente nel database per 24 ore per riparare il flusso; fra processi diversi serve **Redis** o un proxy GRIP (Pushpin). [repository](https://github.com/fanout/django-eventstream) |

### FATTI: Redis e Valkey

| Progetto | Licenza | Ultima stabile | Fonte |
|---|---|---|---|
| Redis ≤ 7.2 | BSD-3 | 7.2.17 (26/10) | [licenze](https://redis.io/legal/licenses/) |
| Redis 7.4.x | RSALv2 **o** SSPLv1 (dal marzo 2024) | 7.4.12 (26/10) | idem |
| Redis 8.x | RSALv2 **o** SSPLv1 **o AGPLv3** (dal GA di Redis 8; annuncio 01/05/2025) | **8.10.3** (26/10; 8.12 in RC) | [LICENSE.txt](https://raw.githubusercontent.com/redis/redis/unstable/LICENSE.txt), [blog AGPLv3](https://redis.io/blog/agplv3/), [releases](https://github.com/redis/redis/releases) |
| Valkey | **BSD-3** | **9.2.0** (18/11/2026) | [COPYING](https://raw.githubusercontent.com/valkey-io/valkey/unstable/COPYING), [releases](https://github.com/valkey-io/valkey/releases) |
| redis-py | MIT | 8.1.0 (30/07/2026) | [PyPI](https://pypi.org/project/redis/) |
| valkey-py | MIT | 6.2.0 (12/10/2026) | [PyPI](https://pypi.org/project/valkey/) |

- Le date delle release di Redis su GitHub mostrano giorno e mese ma non l'anno (presumibilmente 2026).
- Valkey: annunciato dalla Linux Foundation il **28/03/2024** come alternativa open source che continua da **Redis
  7.2.4**, licenza BSD-3, con AWS, Google Cloud, Oracle, Ericsson, Snap.
  [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community)
- Cos'è Redis, in breve: archivio dati in memoria usato come cache, per code e per messaggistica (descrizione comune,
  non citata da una pagina letta). **Pub/Sub** di Redis: consegna **«at most once»** — se l'iscritto è disconnesso il
  messaggio «è perso per sempre»; per garanzie più forti la documentazione rimanda agli **Streams** (persistenti, at
  least once). [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)

### FATTI: proxy, HTTP/2, pool

- **Caddy** `reverse_proxy`: SSE (`text/event-stream`) inviato subito senza buffer (ricerca precedente); WebSocket
  supportato con upgrade, ma **le connessioni WebSocket vengono chiuse a ogni ricaricamento della configurazione**;
  `stream_close_delay` (es. 5m) evita una «mandria» di riconnessioni.
  [reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy)
- **PgBouncer** 1.26.1 (14/10/2026), licenza **ISC** ([COPYRIGHT](https://raw.githubusercontent.com/pgbouncer/pgbouncer/master/COPYRIGHT),
  [sito](https://www.pgbouncer.org/)). In modalità **transaction**: `LISTEN` **mai**, `SET` mai, lock consultivi di
  sessione mai, `WITH HOLD` cursor mai; `NOTIFY` sì; prepared statement di protocollo sì con
  `max_prepared_statements` ≠ 0. [Features](https://www.pgbouncer.org/features.html), [config](https://www.pgbouncer.org/config.html)
- Django: con un pooler in modalità transaction bisogna disattivare i cursori lato server
  (`DISABLE_SERVER_SIDE_CURSORS`). [Django databases](https://docs.djangoproject.com/en/6.1/ref/databases/)

### FATTI: telefoni con lo schermo spento o app in background

- **Page Visibility** (MDN): una pagina è «nascosta» anche quando **lo schermo del dispositivo è spento**; i timer nelle
  schede in background sono limitati (Chrome dopo 10 s, Firefox dopo 30 s, budget); le schede con **WebSocket** o
  WebRTC aperti non subiscono la limitazione dei timer. EventSource non è citato.
  [MDN Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API)
- **Page Lifecycle** (Philip Walton, Chrome, aggiornato 16/10/2026): il browser può **congelare** le pagine nascoste
  (timer e callback di rete non girano) o **scartarle**; consiglio: al `freeze` chiudere IndexedDB, «fermare il polling
  o chiudere i WebSocket», rilasciare i Web Lock; riaprire al `resume`; su mobile `pagehide`/`unload` spesso non
  arrivano, quindi lo stato «hidden» è l'ultimo momento affidabile per salvare.
  [Page Lifecycle API](https://developer.chrome.com/blog/page-lifecycle-api)
- **bfcache** (web.dev): alcuni browser non mettono in cache una pagina con WebSocket aperto; «Chrome (dal 149) e Safari
  non bloccano»; consiglio di chiudere le connessioni a `pagehide`/`freeze` e riaprirle a `pageshow`/`resume`.
  [web.dev bfcache](https://web.dev/articles/bfcache)
- **iPhone**: bug WebKit [308073](https://bugs.webkit.org/show_bug.cgi?id=308073) (aperto il 17/02/2026, stato NEW,
  gravità Major, Safari 26.3 / iOS 26.3): dopo più di 10 s in background, un nuovo `WebSocket` verso un server **in LAN
  via `ws://`** resta in `CONNECTING` senza eventi; `fetch()` allo stesso server funziona; solo il ricaricamento della
  pagina risolve; un commento (18/04/2026) dice che usare un **nome host** al posto dell'IP lo evita. Nessuna risposta
  degli ingegneri WebKit. Su EventSource in background su iOS **non ho trovato documentazione Apple o WebKit**.
- Android (Doze, standby): la documentazione Android riguarda le app native; per il comportamento di Chrome Android con
  EventSource a schermo spento **non ho trovato** una pagina specifica oltre a Page Lifecycle.

### DEDUZIONI

- **SSE è la scelta naturale**: il canale serve solo server → dispositivo (avvisi «la riga è cambiata», «ordine
  assegnato»), le azioni dell'operatore vanno già con richieste normali (POST e coda). SSE passa da Caddy senza
  configurazioni particolari, non si chiude ai ricaricamenti di Caddy come WebSocket, ha la riconnessione nel browser,
  e con HTTP/2 non ha il limite delle 6 connessioni. WebSocket aggiungerebbe Channels (fermo a Django 6.0) e
  channels_redis (quindi Redis), più il bug iOS su LAN.
- **Telefoni in standby: progettare per la perdita del canale**, non contro. Al passaggio a `hidden` chiudere
  l'EventSource; al ritorno visibile riaprirlo e **rileggere lo stato della schermata** dal server (un GET del
  frammento), invece di contare sugli eventi persi. `Last-Event-ID` è un'ottimizzazione, non la garanzia. Questo copre
  anche il caso iOS non documentato (IPOTESI da provare su un iPhone vero: EventSource dopo 1, 5, 30 minuti di schermo
  spento, in Safari e da schermata Home).
- **Più processi sul server**: ogni processo uvicorn/granian tiene una parte delle connessioni SSE; un evento nato in un
  processo (o in un lavoro in background) deve arrivare a tutti. Con PostgreSQL basta **una connessione LISTEN per
  processo** che smista in memoria alle connessioni SSE di quel processo; nessuna connessione al database per ogni
  telefono. Quella connessione LISTEN **non può passare da PgBouncer in modalità transaction**.
- **Redis/Valkey non servono** con questa architettura. Se un giorno servissero (cache condivisa, Channels), **Valkey
  (BSD-3)** evita le domande di licenza di Redis 8 (AGPLv3/RSAL/SSPL); per un uso interno senza modifiche AGPL non
  impone obblighi pratici nella lettura comune, ma **non è un parere legale**.
- **Polling**: resta il piano di riserva (ogni N secondi un GET leggero «c'è qualcosa di nuovo?») se in un ambiente
  SSE dovesse dare problemi (proxy aziendali che bufferizzano: non è il nostro caso con Caddy in sede). Costa richieste
  continue anche quando non succede nulla; il long polling occupa comunque una connessione come SSE senza i suoi
  vantaggi.

## C. Installazione

### FATTI: contenitori e macchine virtuali

- Docker: ogni VM avvia un sistema operativo completo con il **proprio kernel**; i contenitori **condividono il kernel**
  della macchina, sono più piccoli e partono più in fretta; l'isolamento di una VM è **più forte**.
  [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- **IBM Research Report RC25482** (Felter, Ferreira, Rajamony, Rubio, 21/07/2014; versione breve a ISPASS 2015,
  DOI 10.1109/ISPASS.2015.7095802) [PDF](https://www.read.seas.harvard.edu/~kohler/class/cs260r-s19/containerperf14.pdf):
  macchina IBM x3650 M4, 2× Xeon E5-2665 (16 core), 256 GB, Ubuntu 13.10, kernel 3.11, **Docker 1.0**, QEMU 1.5 (KVM).

  | Prova | Nativo | Docker | KVM |
  |---|---|---|---|
  | Compressione PXZ (MB/s) | 76,2 | 73,5 (−4%) | 59,2 (−22%); 62,2 ottimizzato (−18%) |
  | Linpack (GFLOPS) | 290,8 | 290,9 (0%) | 241,3 (−17%); 284,2 ottimizzato (−2%) |
  | Banda memoria (Stream) | — | quasi identica (differenza mediana 1,4% fra i tre) | idem |
  | Rete, banda TCP (nuttcp) | 9,3 Gbps | 9,3 Gbps (più CPU per byte con NAT) | 9,3 Gbps |
  | Rete, latenza richiesta-risposta (netperf) | — | **NAT di Docker: latenza raddoppiata** | +30 µs (+80%) |
  | Disco sequenziale (fio) | — | trascurabile | trascurabile (varianza ×4) |
  | Disco casuale (fio, IOPS) | — | nessun costo | **circa la metà**; latenza di lettura ×2–3 |
  | Redis | — | rete host = nativo; NAT: latenza fino a 1,11× con 100 connessioni | +83 µs per transazione |
  | MySQL (SysBench) | — | differenza che tende al 2% ad alta concorrenza; **AUFS costoso**, NAT poco | **oltre −40%** in tutti i casi |

  Conclusioni: «Docker uguaglia o supera KVM in ogni caso provato»; CPU e memoria quasi senza costo in entrambi; per
  carichi di I/O usare i **volumi** (non i file nello strato AUFS) e valutare la rete host; avvio di un contenitore
  sotto 1 s contro 11 s di una VM sulla loro macchina.
- Misure più recenti da fonti primarie: **non cercate a fondo e non lette**; i numeri sopra valgono per software del
  2014 (AUFS oggi è sostituito da overlay2: dalla memoria, non verificato qui).

### FATTI: Docker Machine

- Repository [docker/machine](https://github.com/docker/machine) **archiviato il 18/07/2025** (sola lettura). La
  documentazione: «non è più mantenuto, usare Docker Desktop o Docker Engine direttamente».
  [Retired products](https://docs.docker.com/retired/). Data di fine vita ufficiale: non indicata nella pagina.

### FATTI: Docker Compose e immagini, buone pratiche documentate

- **Riavvio**: `restart` vale `no` (default), `always`, `on-failure[:n]`, `unless-stopped`.
  [Compose services](https://docs.docker.com/reference/compose-file/services/); per la produzione la documentazione
  suggerisce `restart: always`, niente bind mount del codice, porte diverse, log meno verbosi, eventuale raccolta log.
  [Compose in production](https://docs.docker.com/compose/how-tos/production/)
- **Healthcheck e `depends_on: condition: service_healthy`**: esistono nella specifica (dettagli in pagine non lette).
- **Limiti di risorse**: `deploy.resources.limits` / `reservations` per `cpus`, `memory`, `pids`, `devices`; le GPU si
  chiedono con `devices` e `capabilities` (l'esempio NVIDIA della pagina usa `nvidia-compute`).
  [Compose deploy](https://docs.docker.com/reference/compose-file/deploy/)
- **Volumi nominati contro bind mount**: i volumi sono più facili da copiare e migrare, gestibili da CLI, condivisibili
  in sicurezza, indipendenti dalla struttura delle cartelle dell'host; scrivere in un volume è più veloce che nello
  strato scrivibile del contenitore. Bind mount quando host e contenitore devono vedere gli stessi file.
  [Volumes](https://docs.docker.com/engine/storage/volumes/)
- **Rete host**: niente NAT e niente userland-proxy (migliori prestazioni), ma nessun isolamento di rete; su Linux
  isolamento «come se il servizio girasse direttamente sull'host»; su Docker Desktop solo dalla 4.34 e con limiti.
  [Host network](https://docs.docker.com/engine/network/drivers/host/)
- **Log**: il driver di default `json-file` **non ruota i log**; la documentazione **raccomanda il driver `local`**, che
  ruota per default; esempio `max-size: 10m`, `max-file: 3`. [Logging](https://docs.docker.com/engine/logging/configure/)
- **Immagini**: build multi-stage per immagini finali piccole, immagine di base minima, **versione fissata fino al
  digest**, `.dockerignore`, niente pacchetti superflui, un compito per contenitore, ricostruire spesso per le patch.
  [Build best practices](https://docs.docker.com/build/building/best-practices/)

### FATTI: Windows con WSL2

- WSL2 è una VM leggera gestita con un vero kernel Linux; «prestazioni fra filesystem diversi»: WSL1 sì, WSL2 **no**;
  le prime versioni di WSL2 erano fino a 20× più veloci di WSL1 a scompattare un tar e 2–5× in `git clone`/`npm
  install`; per i file su Windows WSL1 resta più veloce. [Compare versions](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)
- Microsoft: tenere i file nel filesystem Linux (`/home/<utente>/...`), non in `/mnt/c/...`.
  [Filesystems](https://learn.microsoft.com/en-us/windows/wsl/filesystems). Docker: i bind mount da `/mnt/c` sono più
  lenti e i contenitori ricevono le **notifiche di modifica** solo per file nel filesystem Linux.
  [Docker WSL best practices](https://docs.docker.com/desktop/features/wsl/best-practices/)
- Rete: WSL2 di default usa **NAT** con IP che cambia al riavvio; per raggiungerlo dalla LAN serve `netsh interface
  portproxy` oppure la modalità **mirrored** (`networkingMode=mirrored`, Windows 11 22H2+), che permette di
  «connettersi a WSL direttamente dalla LAN»; firewall Hyper-V attivo per default (regole da aggiungere).
  [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking)
- **GPU NVIDIA in WSL2**: installare **solo il driver Windows** («non installare driver Linux in WSL»); Docker con
  NVIDIA Container Toolkit funziona ma solo `--gpus all` (nessuna scelta della singola GPU); NVML/`nvidia-smi` parziale;
  memoria pinned limitata; possibili prestazioni ridotte con managed memory.
  [CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html), [Docker Desktop GPU](https://docs.docker.com/desktop/features/gpu/)
  (licenza di Docker Desktop: ricerca precedente).

### FATTI: Podman

- Podman (Apache 2.0) e versioni: ricerca precedente. **`podman compose`** è un «sottile involucro» attorno a un
  provider esterno: **preferisce `docker-compose` se installato**, altrimenti `podman-compose`.
  [podman-compose(1)](https://docs.podman.io/en/latest/markdown/podman-compose.1.html)
- **podman-compose**: script Python che implementa la Compose Spec con Podman, senza demone e senza root; licenza
  **GPL-2.0-only**; 1.6.0 del 03/06/2026. [repository](https://github.com/containers/podman-compose),
  [PyPI](https://pypi.org/project/podman-compose/)

### FATTI: Django in produzione

- **uvicorn**: il gestore integrato `--workers` usa `spawn` (non pre-fork) e riavvia i processi morti; il modulo
  `uvicorn.workers` per Gunicorn è **deprecato** (pacchetto separato `uvicorn-worker`); `--proxy-headers` con
  `--forwarded-allow-ips` solo per proxy fidati. Nessuna formula per il numero di processi.
  [uvicorn deployment](https://uvicorn.dev/deployment/)
- **granian**: punto di partenza «un worker per core»; in contenitore «meglio 1 worker per contenitore»; non copiare i
  numeri pensati per Gunicorn/uvicorn; con più worker e riavvii su Linux serve kernel ≥ 5.14 e
  `net.ipv4.tcp_migrate_req`, altrimenti si possono perdere connessioni in coda.
  [README](https://raw.githubusercontent.com/emmett-framework/granian/master/README.md)
- **Connessioni al database**: con ASGI le connessioni persistenti vanno disattivate (`CONN_MAX_AGE = 0`) e si usa il
  pool di psycopg (`"OPTIONS": {"pool": True}` o un dizionario per `ConnectionPool`); vita delle connessioni con
  `max_lifetime`. [Django databases](https://docs.djangoproject.com/en/6.1/ref/databases/). psycopg-pool 3.3.3
  (22/09/2026), **LGPL-3.0-only**. [PyPI](https://pypi.org/project/psycopg-pool/)
- **File statici con Caddy**: `file_server` con `precompressed` serve file `.br`, `.zst`, `.gz` già compressi;
  `encode` comprime al volo in gzip/zstd. [file_server](https://caddyserver.com/docs/caddyfile/directives/file_server),
  [encode](https://caddyserver.com/docs/caddyfile/directives/encode)

### FATTI: PostgreSQL in contenitore

- `shared_buffers`: default tipico 128 MB; su un server dedicato con ≥ 1 GB di RAM «un valore iniziale ragionevole è
  il **25%** della memoria»; oltre il 40% difficilmente meglio; `work_mem` default 4 MB; `huge_pages` default `try`.
  [Resource consumption (PG 19)](https://www.postgresql.org/docs/current/runtime-config-resource.html)
- Immagine ufficiale `postgres`: fino a PG 17 il volume va su `/var/lib/postgresql/data`; **da PG 18 il volume è
  `/var/lib/postgresql`** con `PGDATA` per versione (es. `/var/lib/postgresql/18/docker`); `shm_size` da impostare in
  Compose (esempio 128mb); password da file (`POSTGRES_PASSWORD_FILE`); gli script di `/docker-entrypoint-initdb.d`
  girano solo con cartella dati vuota; impostazioni con `-c` o file di configurazione (con `listen_addresses = '*'`);
  Alpine supporta le localizzazioni solo via ICU da PG 15. [Docker Hub postgres](https://hub.docker.com/_/postgres)

### DEDUZIONI

- **Contenitori su Linux nativo** sono la scelta per un server in sede: costo trascurabile su CPU e memoria rispetto al
  nativo, migliori di una VM sull'I/O del database; una VM ha senso solo se l'IT dell'azienda vuole isolare il server
  (e si possono mettere i contenitori dentro una VM, accettando il costo misurato da IBM sull'I/O).
- **Le due trappole misurate da IBM esistono ancora in forma simile**: rete NAT e file nello strato del contenitore.
  Quindi: **volume nominato dedicato per PostgreSQL**; rete bridge di Compose fra i servizi interni (la latenza in più
  in rete locale è dell'ordine delle decine di microsecondi, irrilevante rispetto a 1–2 s: deduzione dai numeri del
  2014); rete host solo se una misura lo giustifica.
- **Compose di base**: `restart: unless-stopped` (o `always`), healthcheck su Django e PostgreSQL con `depends_on:
  service_healthy`, limiti di memoria per non far morire l'host, driver di log `local` (o `max-size`/`max-file`),
  immagini con versione e digest fissati, build multi-stage. Su PG 18 attenzione al **nuovo percorso del volume**.
- **Processi Django**: con SSE servono viste asincrone; il numero di processi va legato ai core (granian: uno per core
  come punto di partenza) e alle connessioni al database: **processi × dimensione del pool + una connessione LISTEN per
  processo + worker dei lavori in background** deve stare sotto `max_connections` di PostgreSQL. PgBouncer non serve
  con questi numeri (IPOTESI: decine di dispositivi, pochi processi); se servisse, solo in modalità session o con la
  connessione LISTEN diretta.
- **Server Windows**: possibile con WSL2 + Docker Engine dentro WSL (evita la licenza Desktop, ricerca precedente), ma
  servono file e volumi nel filesystem Linux e la rete **mirrored** o un `portproxy` perché telefoni e palmari
  raggiungano il server; è una configurazione in più da documentare e verificare. Linux resta più semplice.
- **Podman**: alternativa possibile, ma `podman compose` usa comunque docker-compose se c'è, e podman-compose è GPL-2.0
  (strumento usato, non incluso nel prodotto: deduzione). Nessun motivo forte per preferirlo a Docker Engine su Linux.
- **Docker Machine** non va considerato.

## D. Posta dalla casella del responsabile

### FATTI: Microsoft 365

- **Graph `sendMail`**: `POST /users/{id|upn}/sendMail`; permesso `Mail.Send` **delegato** (utente connesso) o
  **applicativo** (senza utente); `ccRecipients` supportato; salva in Posta inviata per default (`saveToSentItems`);
  risposta `202 Accepted` = accettato, non consegnato (limiti e throttling di Exchange Online).
  [user-sendmail](https://learn.microsoft.com/en-us/graph/api/user-sendmail). Allegati sotto **3 MB** nella stessa
  richiesta; da 3 a **150 MB** con una sessione di caricamento (richiede `Mail.ReadWrite`).
  [Large attachments](https://learn.microsoft.com/en-us/graph/outlook-large-attachments)
- **RBAC for Applications in Exchange Online** (pagina aggiornata il 27/10/2026)
  [application-rbac](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac):
  - permette di dare a un'applicazione un permesso **limitato a un insieme di caselle** (Management Scope con filtro,
    oppure Administrative Unit di Entra); «**sostituisce le Application Access Policy**»;
  - passi: `New-ServicePrincipal` (puntatore al service principal di Entra) → `New-ManagementScope` (es.
    `MemberOfGroup`) → `New-ManagementRoleAssignment -Role "Application Mail.Send" -App … -CustomResourceScope …` →
    `Test-ServicePrincipalAuthorization`;
  - ruoli disponibili fra cui **`Application Mail.Send`** e **`Application SMTP.SendAsApp`**; protocolli Graph ed EWS;
  - **i permessi si sommano**: se l'app ha anche `Mail.Send` concesso in Entra ID per tutta l'organizzazione, l'ambito
    non limita nulla; il permesso in Entra va tolto;
  - modifiche efficaci dopo una cache **da 30 minuti a 2 ore**; servono il ruolo Organization Management in Exchange e
    Exchange Administrator in Entra; gruppi annidati fuori ambito.
- La data di dismissione delle Application Access Policy **non l'ho trovata** su una fonte ufficiale (l'annuncio del
  2022 parlava di deprecarle dopo il rilascio generale di RBAC for Applications: citato da risultati di ricerca, non
  aperto).
- **SMTP con OAuth** [Microsoft Learn](https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth):
  - delegato: scope `https://outlook.office.com/SMTP.Send` (+ `offline_access` per il token di rinnovo), formato
    SASL XOAUTH2;
  - senza utente (client credentials): permesso applicativo `SMTP.SendAsApp`, consenso dell'amministratore,
    `New-ServicePrincipal`, poi **`Add-MailboxPermission … -AccessRights FullAccess`** per ogni casella (e
    `Add-RecipientPermission` SendAs se si manda come altro mittente); scope `https://outlook.office365.com/.default`.
  - L'autenticazione di base per SMTP AUTH si spegne a fine dicembre 2026 (ricerca precedente).
- Exchange Online blocca EWS dal 01/10/2026 (citato da risultati di ricerca su un post Microsoft, non aperto): non
  usare EWS.

### FATTI: Google Workspace

- **Delega a livello di dominio** per un account di servizio: la configura un **super amministratore** nella Console
  di amministrazione (Sicurezza → Accesso e controllo dei dati → Controlli API → Delega a livello di dominio) con l'ID
  client e gli scope; effetto **fino a 24 ore**; l'esempio della pagina è «leggere la Gmail o il calendario di
  qualunque utente». [Create credentials](https://developers.google.com/workspace/guides/create-credentials#optional_set_up_domain-wide_delegation_for_a_service_account)
- Scope `https://www.googleapis.com/auth/gmail.send` («inviare email per tuo conto»): classificato **sensibile**
  (verifica OAuth aggiuntiva per le app pubbliche). [Gmail scopes](https://developers.google.com/workspace/gmail/api/auth/scopes)
- App con tipo utente **Internal** (solo per progetti di un'organizzazione Workspace): verifica **non richiesta**, niente
  schermata «app non verificata» né limite di 100 utenti; l'amministratore può comunque bloccare o dover approvare
  l'app. [Configure OAuth consent](https://developers.google.com/workspace/guides/configure-oauth-consent),
  [When verification is not needed](https://support.google.com/cloud/answer/13464323?hl=en)
- Password per le app e fine delle password per SMTP: ricerca precedente.

### FATTI: Aruba e Register.it

- **Aruba** (caselle su dominio): `smtps.aruba.it`, porta **465** SSL/TLS (almeno TLS 1.2), «il server SMTP richiede
  sempre l'autenticazione con indirizzo email e relativa password»; senza SSL `smtp.<dominio>` porta 587 o 25
  (sconsigliato). Nessuna menzione di OAuth, verifica in due passaggi o password per le app nella pagina.
  [Parametri posta Aruba](https://guide.aruba.it/hosting-e-domini/email/configurazione-posta/parametri-configurazione-posta)
- **Aruba PEC**: con la **verifica in due passaggi** attiva bisogna generare una **password dedicata per il programma di
  posta** (non modificabile, rigenerabile); SMTP `smtps.pec.aruba.it:465`. Nessuna menzione di OAuth.
  [PEC su programmi di posta](https://guide.aruba.it/pec/configurazione-programmi-di-posta/client-posta-e-dispositivi-mobili)
- **Register.it**: `authsmtp.securemail.pro`, porta **465** SSL, utente = indirizzo completo, password scelta
  nell'Area Clienti; nessuna menzione di OAuth, 2FA, password per le app o limiti di invio.
  [Parametri email Register.it](https://www.register.it/assistenza/parametri-email/)

### FATTI: librerie Python

| Libreria | Licenza | Versione e data | Uso |
|---|---|---|---|
| msal | MIT | 1.39.0, 17/09/2026 | token Microsoft Entra (client credentials, codice di autorizzazione, rinnovo). [PyPI](https://pypi.org/project/msal/) |
| google-auth | Apache 2.0 | 2.62.2, 10/11/2026 | credenziali di account di servizio, anche con delega (`with_subject`: dalla memoria, non verificato qui). [PyPI](https://pypi.org/project/google-auth/) |
| google-auth-oauthlib | Apache 2.0 | 1.5.0, 29/09/2026 | flusso OAuth con l'utente. [PyPI](https://pypi.org/project/google-auth-oauthlib/) |
| google-api-python-client | Apache 2.0 | 2.202.0, 10/11/2026 | client della Gmail API (si può anche chiamare l'API REST direttamente). [PyPI](https://pypi.org/project/google-api-python-client/) |
| O365 | Apache 2.0 | 2.1.11, 16/11/2026 | client Graph di terze parti (non approfondito). [PyPI](https://pypi.org/project/O365/) |
| exchangelib | BSD-2-Clause | 5.6.0, 10/10/2025 | EWS: **da evitare** per il blocco di EWS. [PyPI](https://pypi.org/project/exchangelib/) |
| smtplib (libreria standard) | PSF | — | SMTP con password o XOAUTH2 (ricerca precedente) |

### DEDUZIONI

- **Microsoft 365 – via consigliata per «dalla casella del responsabile con copia a lui»**: app registrata una volta in
  Entra, **senza** `Mail.Send` concesso a livello di organizzazione, con **RBAC for Applications** `Application
  Mail.Send` limitato a un gruppo di posta «Responsabili Ripo»; invio con Graph `sendMail` sulla casella del
  responsabile e lui in `ccRecipients` (o in copia nascosta); il messaggio resta nella sua Posta inviata. Il segreto
  dell'app (meglio un **certificato** che una password client) sta sul server. Rischio: se il permesso viene concesso
  anche in Entra, l'app può scrivere a nome di **chiunque**; va verificato con `Test-ServicePrincipalAuthorization` e
  documentato per l'IT. Le modifiche ai responsabili impiegano fino a 2 ore.
- **Microsoft 365 – alternativa per utente (delegato)**: ogni responsabile accede una volta con il proprio account
  (OAuth, scope `Mail.Send` + `offline_access`); il server conserva un **token di rinnovo per persona** (dato sensibile
  da cifrare); se la persona cambia password o l'IT revoca, l'invio si ferma finché non riaccede. Meno lavoro per
  l'amministratore, più gestione per noi e per gli utenti.
- **SMTP con OAuth (SMTP.SendAsApp)** richiede `FullAccess` sulla casella (troppo ampio per un invio) e SMTP AUTH
  abilitato: peggiore di Graph per questo uso.
- **Google Workspace**: la delega a livello di dominio è potente (l'account di servizio può agire per qualunque utente
  con gli scope concessi): limitarla a `gmail.send` e custodire bene la chiave; in alternativa, accesso dell'utente con
  app **Internal** (niente verifica Google). La copia al responsabile si fa mettendolo in Cc nel messaggio MIME.
- **Aruba e Register.it**: solo SMTP con password della casella (o password per programma di posta dove esiste):
  bisogna salvare una password per ogni responsabile, cifrata, e prevedere l'errore «password cambiata». Per «copia a
  lui» basta il Cc; la copia in Posta inviata **non** avviene con SMTP (servirebbe IMAP APPEND: non verificato su
  Aruba/Register.it).
- **Adattatore di invio** (ricerca precedente) con quattro modalità: Graph applicativo con RBAC, Graph delegato, Gmail
  API (delega o utente), SMTP con password; la scelta si fa in Configurazione per azienda.

## Cosa resta incerto

- **Peso di React dopo la minificazione** e runtime reale di Svelte: non misurati (servirebbe un bundler).
- **Costo del JavaScript sui telefoni di oggi**: l'unica misura primaria trovata è del 2019 (V8); nessun dato sui
  palmari che userà il magazzino. Va misurato INP sui dispositivi veri.
- **Caso Contexte**: fonte di parte, senza metodo di misura; il talk originale non è stato aperto.
- **EventSource su iPhone e Android a schermo spento**: nessuna documentazione Apple/WebKit/Chrome specifica trovata;
  da provare.
- **Bug WebKit 308073**: aperto; non so se riguardi anche `wss://` con nome host (un commento dice che il nome host lo
  evita) né EventSource.
- **channels-postgres**: licenza discordante (MIT su PyPI, BSD-3 nel repository); se usi LISTEN/NOTIFY o polling non
  documentato; manutenzione non chiara.
- **Data di dismissione delle Application Access Policy**: non trovata su una fonte ufficiale aperta.
- **Aruba (caselle ordinarie) e Register.it**: OAuth, verifica in due passaggi e password per le app non documentati
  nelle pagine ufficiali lette; limiti di invio non indicati.
- **Misure contenitori/VM recenti**: solo IBM 2014 letto; nessuna misura primaria recente su overlay2.
- **Healthcheck e `depends_on`**: esistono nella specifica Compose ma le pagine di dettaglio non sono state lette.
- Date delle release Redis su GitHub senza anno.

## Fonti

Schermate
- htmx docs — https://htmx.org/docs/ ; htmx 4 — https://four.htmx.org/docs/
- When Should You Use Hypermedia? — https://htmx.org/essays/when-to-use-hypermedia/
- A Real World React → htmx Port — https://htmx.org/essays/a-real-world-react-to-htmx-port/
- React 19 — https://react.dev/blog/2024/12/05/react-19 ; React 19.3 — https://react.dev/blog/2026/09/09/react-19-3 ;
  blog — https://react.dev/blog
- Svelte — https://svelte.dev/docs/svelte/overview ; Lit — https://lit.dev/docs/
- Alpine.js — https://alpinejs.dev/start-here ; CSP — https://alpinejs.dev/advanced/csp
- shadcn/ui — https://ui.shadcn.com/docs ; LICENSE — https://raw.githubusercontent.com/shadcn-ui/ui/main/LICENSE.md
- Animate UI LICENSE — https://raw.githubusercontent.com/imskyleen/animate-ui/main/LICENSE.md
- Registro npm (20/11/2026; tarball scaricati con `npm pack`): react, react-dom, scheduler, svelte, vue, lit, lit-html,
  lit-element, @lit/reactive-element, alpinejs, preact, htmx.org, shadcn, @animate-ui/react, @animate-ui/cli, motion —
  https://www.npmjs.com/package/<nome>
- The cost of JavaScript in 2019 — https://v8.dev/blog/cost-of-javascript-2019
- INP — https://web.dev/articles/inp
- MDN browser-compat-data (Document, ViewTransition, view-transition, PerformanceEventTiming, CustomElementRegistry,
  EventSource) — https://github.com/mdn/browser-compat-data
- WCAG 2.2 Understanding 4.1.3 — https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- MDN ARIA live regions — https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
- django-htmx — https://django-htmx.readthedocs.io/en/latest/ ; Django Ninja — https://django-ninja.dev/
- PyPI (API JSON, 20/11/2026): django-htmx, djangorestframework, django-ninja, django-cotton, django-components,
  channels, channels-redis, channels-postgres, daphne, django-eventstream, redis, valkey, psycopg-pool, podman-compose,
  msal, google-auth, google-auth-oauthlib, google-api-python-client, O365, exchangelib — https://pypi.org/project/<nome>/

Canale aperto
- Django request/response — https://docs.djangoproject.com/en/6.1/ref/request-response/
- Django databases — https://docs.djangoproject.com/en/6.1/ref/databases/
- Channels, channel layers — https://channels.readthedocs.io/en/latest/topics/channel_layers.html ; release —
  https://channels.readthedocs.io/en/latest/releases/index.html
- channels_postgres — https://github.com/danidee10/channels_postgres
- django-eventstream — https://github.com/fanout/django-eventstream
- WebSockets Standard — https://websockets.spec.whatwg.org/
- Redis licenze — https://redis.io/legal/licenses/ ; AGPLv3 — https://redis.io/blog/agplv3/ ; LICENSE —
  https://raw.githubusercontent.com/redis/redis/unstable/LICENSE.txt ; releases — https://github.com/redis/redis/releases ;
  Pub/Sub — https://redis.io/docs/latest/develop/pubsub/
- Valkey — https://github.com/valkey-io/valkey/releases ; COPYING —
  https://raw.githubusercontent.com/valkey-io/valkey/unstable/COPYING ; Linux Foundation —
  https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community
- Caddy reverse_proxy — https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
- PgBouncer — https://www.pgbouncer.org/ ; features — https://www.pgbouncer.org/features.html ; config —
  https://www.pgbouncer.org/config.html ; COPYRIGHT — https://raw.githubusercontent.com/pgbouncer/pgbouncer/master/COPYRIGHT
- MDN Page Visibility — https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
- Page Lifecycle API — https://developer.chrome.com/blog/page-lifecycle-api
- bfcache — https://web.dev/articles/bfcache
- WebKit bug 308073 — https://bugs.webkit.org/show_bug.cgi?id=308073

Installazione
- Docker, what is a container — https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/
- IBM RC25482 (2014) — https://www.read.seas.harvard.edu/~kohler/class/cs260r-s19/containerperf14.pdf
- Docker Machine — https://github.com/docker/machine ; retired — https://docs.docker.com/retired/
- Compose services — https://docs.docker.com/reference/compose-file/services/ ; deploy —
  https://docs.docker.com/reference/compose-file/deploy/ ; production — https://docs.docker.com/compose/how-tos/production/
- Volumes — https://docs.docker.com/engine/storage/volumes/ ; host network —
  https://docs.docker.com/engine/network/drivers/host/ ; logging — https://docs.docker.com/engine/logging/configure/ ;
  build best practices — https://docs.docker.com/build/building/best-practices/
- WSL — https://learn.microsoft.com/en-us/windows/wsl/compare-versions ;
  https://learn.microsoft.com/en-us/windows/wsl/filesystems ; https://learn.microsoft.com/en-us/windows/wsl/networking
- Docker Desktop WSL — https://docs.docker.com/desktop/features/wsl/best-practices/ ; GPU —
  https://docs.docker.com/desktop/features/gpu/
- CUDA on WSL — https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- podman compose — https://docs.podman.io/en/latest/markdown/podman-compose.1.html ; podman-compose —
  https://github.com/containers/podman-compose
- uvicorn deployment — https://uvicorn.dev/deployment/ ; granian README —
  https://raw.githubusercontent.com/emmett-framework/granian/master/README.md
- Caddy file_server — https://caddyserver.com/docs/caddyfile/directives/file_server ; encode —
  https://caddyserver.com/docs/caddyfile/directives/encode
- PostgreSQL resource consumption — https://www.postgresql.org/docs/current/runtime-config-resource.html
- Docker Hub postgres — https://hub.docker.com/_/postgres

Posta
- Graph sendMail — https://learn.microsoft.com/en-us/graph/api/user-sendmail ; allegati grandi —
  https://learn.microsoft.com/en-us/graph/outlook-large-attachments
- RBAC for Applications — https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac
- OAuth IMAP/POP/SMTP — https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth
- Google, credenziali e delega — https://developers.google.com/workspace/guides/create-credentials ; scope Gmail —
  https://developers.google.com/workspace/gmail/api/auth/scopes ; consenso OAuth —
  https://developers.google.com/workspace/guides/configure-oauth-consent ; verifica non necessaria —
  https://support.google.com/cloud/answer/13464323?hl=en
- Aruba — https://guide.aruba.it/hosting-e-domini/email/configurazione-posta/parametri-configurazione-posta ; PEC —
  https://guide.aruba.it/pec/configurazione-programmi-di-posta/client-posta-e-dispositivi-mobili
- Register.it — https://www.register.it/assistenza/parametri-email/

Non raggiungibili o non lette
- `https://www.uvicorn.org/deployment/` non risolveva: letta la stessa pagina su `uvicorn.dev`.
- Il PDF IBM sul sito IBM (dominoweb) rispondeva 503: letta la copia sul sito di un corso di Harvard.
- `docs.gunicorn.org` reindirizza a `gunicorn.org` (non aperto); la pagina Docker «docker-overview» dava 404.
- Annunci Microsoft sulla deprecazione delle Application Access Policy (2022) e sul blocco di EWS (2026): visti solo nei
  risultati di ricerca.
- Installare un minificatore (esbuild) per misurare React non è stato consentito in questa sessione.
