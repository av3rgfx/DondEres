# Librerie e componenti per lo stack della base

Data: 20/11/2026

## Domanda

Quali versioni, licenze, stato di manutenzione e limiti documentati hanno i componenti candidati per la base del
gestionale (server Python/Django, PostgreSQL + pgvector, browser con htmx e SSE, lettura barcode nel browser, HTTPS in
rete interna, PDF e posta, installazione con contenitori, GitHub)? Cosa cambia per le scelte?

Contesto: web app servita da un server in sede sulla rete interna; telefoni Android/iPhone, palmari Android a
grilletto, computer. Ricerca esatta tra 175.000-350.000 impronte a 768-1024 dimensioni (vedi
`docs/research/2026-11-15-addestramento-ed-esecuzione-locale.md`). Lo stack non è ancora scelto: questo documento
raccoglie fatti, non decide.

Legenda: **FATTO** = verificato sulla fonte linkata (aperta il 20/11/2026); **DEDUZIONE** = ragionamento a partire dai
fatti; **IPOTESI** = da verificare con prove; **non verificato** = fonte non trovata o non leggibile.

Metodo: versioni da PyPI (API JSON), npm (registry), tag git (`git ls-remote`) e pagine «Releases» di GitHub; licenze
dai file LICENSE grezzi o dai metadati del registro. L'API di GitHub non era raggiungibile in questa sessione; le pagine
github.com sono state lette con uno strumento di estrazione testo.

## Sintesi

1. **Microsoft 365 spegne l'autenticazione di base per SMTP AUTH alla fine di dicembre 2026** (fra circa 6 settimane):
   disattivata per default nei tenant esistenti (l'amministratore può ancora riattivarla), non disponibile nei tenant
   nuovi; la data di rimozione definitiva sarà annunciata nella seconda metà del 2027. Google ha già spento le password
   «normali» per SMTP/IMAP il 14/03/2025 (restano le password per le app, sconsigliate). **Una base che invia posta deve
   nascere con OAuth (XOAUTH2) o Graph, o con un relay.** (FATTO)
2. **Django ha cambiato politica di versioni e supporto.** Ultima 6.1.3 (03/11/2026, Python ≥ 3.12). LTS attuale 5.2
   (supporto di sicurezza fino ad aprile 2028); **la prossima LTS 6.2 esce ad aprile 2027** (fino ad aprile 2030). Dal
   2028 versioni annuali «AAAA», ognuna con tre anni di supporto. (FATTO)
3. **Il framework Tasks di Django non esegue i lavori**: i backend di serie (`ImmediateBackend`, `DummyBackend`) sono
   solo per sviluppo e test. Per la produzione serve un backend esterno: `django-tasks-db` (ORM, worker
   `db_worker`) oppure una coda propria come Procrastinate (PostgreSQL, LISTEN/NOTIFY, attività periodiche cron). (FATTO)
4. **PostgreSQL 19 è uscito ieri (19/11/2026)**; PostgreSQL 14 ha finito il supporto il 12/11/2026. pgvector 0.8.7
   (01/10/2026) fa ricerca **esatta per default**; i limiti 2.000 (`vector`) / 4.000 (`halfvec`) dimensioni valgono
   **solo per gli indici**: in tabella si arriva a 16.000. La ricerca esatta si accelera con il parallelismo
   (`max_parallel_workers_per_gather`). Il supporto dichiarato a PostgreSQL 19 non l'ho trovato. (FATTO)
5. **htmx 4.0 è uscito (28/08/2026) ma su npm «latest» resta la 2.0.11**; il sito dice che la 4 diventerà «latest» nel
   2027. Partire con la 2.x significa una migrazione prevedibile entro 1-2 anni. (FATTO + DEDUZIONE)
6. **BarcodeDetector resta assente su iPhone (Safari 17+ solo dietro flag, anche iOS 26), su Chrome Windows/Linux e su
   Firefox**; c'è su Chrome Android e WebView Android. Il polyfill `barcode-detector` (MIT, 3.2.4 del 15/11/2026) usa
   zxing-cpp in WebAssembly (~1,04 MiB il .wasm di sola lettura) e **scarica il .wasm da jsDelivr per default**: in rete
   interna va servito in locale con `prepareZXingModule`. (FATTO)
7. **SSE**: con HTTP/1.1 il browser apre al massimo **6 connessioni per dominio, condivise fra tutte le schede**; con
   HTTP/2 il limite è negoziato (default 100). Caddy abilita HTTP/2 e HTTP/3 di serie e non bufferizza le risposte
   `text/event-stream`. (FATTO)
8. **Certificati**: nessun modulo Caddy né provider lego per **Aruba o Register.it**; ci sono OVH e Cloudflare. Per i
   gestori senza API la via documentata è la **delega CNAME di `_acme-challenge`** (Let's Encrypt, Caddy, acme-dns).
   Let's Encrypt accorcia i certificati: 64 giorni da febbraio 2027, 45 giorni da febbraio 2028. (FATTO)
9. **Watchtower è archiviato (17/12/2025)**: non usarlo per gli aggiornamenti automatici. **Docker Desktop è a
   pagamento** per aziende con ≥ 250 dipendenti o ≥ 10 milioni di dollari di fatturato; Docker Engine su Linux è
   Apache 2.0. (FATTO)
10. **Rinominare un repository GitHub reindirizza web, git e API, ma non l'indirizzo GitHub Pages di un sito di
    progetto** (`utente.github.io/NomeRepo`): la documentazione lo esclude esplicitamente e consiglia un dominio
    personalizzato. (FATTO)

## A. Server Python

### FATTI

| Componente | Licenza | Versione stabile e data | Python | Manutenzione | Fonte |
|---|---|---|---|---|---|
| Django | BSD-3-Clause | 6.1.3, 03/11/2026 | ≥ 3.12 (6.1: 3.12-3.15) | attiva | [download](https://www.djangoproject.com/download/), [PyPI](https://pypi.org/project/Django/) |
| Python | PSF | 3.15.2, 25/10/2026 | — | 3.15 bugfix fino a 10/2031 | [python.org](https://www.python.org/downloads/), [devguide](https://devguide.python.org/versions/) |
| uvicorn | BSD-3-Clause | 0.54.0, 25/09/2026 | ≥ 3.10 | rilasci regolari (0.52 → 0.54 nel 2026) | [PyPI](https://pypi.org/project/uvicorn/), [README](https://raw.githubusercontent.com/encode/uvicorn/main/README.md) |
| granian | BSD-3-Clause | 2.8.9, 20/11/2026 | ≥ 3.10 | «actively maintained» | [PyPI](https://pypi.org/project/granian/), [README](https://raw.githubusercontent.com/emmett-framework/granian/master/README.md) |
| psycopg 3 | **LGPL-3.0-only** | 3.3.9, 12/11/2026 | ≥ 3.10 | attiva | [PyPI](https://pypi.org/project/psycopg/), [LICENSE](https://raw.githubusercontent.com/psycopg/psycopg/master/LICENSE.txt) |
| FastAPI | MIT | 0.165.0, 18/11/2026 | ≥ 3.11 | attiva, ancora 0.x | [PyPI](https://pypi.org/project/fastapi/) |
| django-tasks (backport) | BSD-3-Clause | 0.12.0, 06/02/2026 | ≥ 3.10 | — | [PyPI](https://pypi.org/project/django-tasks/) |
| django-tasks-db | BSD-3-Clause | 0.13.0, 28/08/2026 | ≥ 3.10 | — | [PyPI](https://pypi.org/project/django-tasks-db/) |

**Django, supporto** ([pagina download](https://www.djangoproject.com/download/)):

| Serie | Ultima | Fine supporto principale | Fine supporto esteso (sicurezza) |
|---|---|---|---|
| 5.2 LTS | 5.2.19 | 03/12/2025 | aprile 2028 |
| 6.0 | 6.0.10 | 04/08/2026 | aprile 2027 |
| 6.1 | 6.1.3 | aprile 2027 | dicembre 2027 |
| 6.2 LTS (futura) | aprile 2027 | dicembre 2027 | aprile 2030 |
| 2028 (futura) | gennaio 2028 | gennaio 2029 | gennaio 2031 |

- «Django 6.2 è l'ultima versione con la politica precedente»; dal 2028 le versioni si chiamano «AAAA», escono ogni
  gennaio e **ognuna** ha tre anni di supporto. [download](https://www.djangoproject.com/download/)
- Python supportato: 5.2 → 3.10-3.14; 6.0 → 3.12-3.14; 6.1 → 3.12-3.15 (3.15 da 6.1.3).
  [FAQ installazione](https://docs.djangoproject.com/en/6.1/faq/install/)
- Django 6.1 supporta **PostgreSQL 15 e successivi**, con psycopg 3.1.12+ (consigliato) o psycopg2 2.9.9+; il pool di
  connessioni nativo funziona solo con psycopg (`psycopg[pool]`); con ASGI le connessioni persistenti vanno disattivate
  e si usa il pool. [Databases](https://docs.djangoproject.com/en/6.1/ref/databases/)
- **Python** ([devguide](https://devguide.python.org/versions/)): 3.15 (uscita 09/10/2026, fine 10/2031), 3.14 (fine
  10/2030), 3.13 (solo sicurezza, fine 10/2029), 3.12 (sicurezza, fine 10/2028); **3.10 a fine vita dal 01/10/2026**.

**Async e streaming (SSE) in Django**

- «Per le risposte lente in streaming, il long polling e simili» serve il deploy **ASGI**; sotto WSGI «senza la
  possibilità di richieste lunghe efficienti». [Async](https://docs.djangoproject.com/en/6.1/topics/async/)
- Sotto WSGI una `StreamingHttpResponse` «occupa un processo worker per tutta la durata della risposta».
  `StreamingHttpResponse` accetta un iteratore asincrono (`is_async`); se il client si disconnette Django cancella la
  coroutine (`asyncio.CancelledError`). [Request/response](https://docs.djangoproject.com/en/6.1/ref/request-response/)
- Un middleware sincrono fra il server ASGI e una vista asincrona costringe Django a tenere un thread per richiesta:
  «conta soprattutto quando si usa ASGI per … server-sent events o altre richieste lunghe, dove il thread in più per
  richiesta limita la concorrenza». Il middleware di serie di Django supporta sync e async.
  [Async](https://docs.djangoproject.com/en/6.1/topics/async/)

**Framework Tasks (Django 6.0+)**

- Introdotto in Django 6.0. [Note 6.0](https://docs.djangoproject.com/en/6.1/releases/6.0/)
- «Non fornisce un meccanismo di worker»; i backend di serie sono **`ImmediateBackend`** (default: esegue subito, nella
  richiesta) e **`DummyBackend`** (memorizza e non esegue), «solo per sviluppo e test». «I sistemi in produzione devono
  appoggiarsi a backend che forniscono un processo worker e una coda durevole», elencati nella pagina Community
  Ecosystem. Supporto async «in sviluppo». [Tasks](https://docs.djangoproject.com/en/6.1/topics/tasks/)
- La pagina [Community Ecosystem](https://www.djangoproject.com/community/ecosystem/) elenca: **django-tasks-db**
  (backend ORM), django-tasks-rq (RQ, quindi Redis), django-tasks (backport) e huey (Redis, SQLite, Postgres; usabile
  come backend Tasks).
- **django-tasks-db**: backend `django_tasks_db.DatabaseBackend`, worker `./manage.py db_worker`, pulizia con
  `prune_db_task_results`. Fino a django-tasks 0.12.0 il backend database era incluso nel backport, poi è stato
  separato. [PyPI django-tasks-db](https://pypi.org/project/django-tasks-db/), [PyPI django-tasks](https://pypi.org/project/django-tasks/)
- Non ho trovato nella documentazione di Django né in quella di django-tasks-db un meccanismo di **attività
  periodiche** (cron). (Assenza constatata nelle pagine lette, non affermata dalle fonti.)

**Server ASGI**

- uvicorn: «server web ASGI»; il README dichiara HTTP/1.1, HTTP/2 e WebSocket.
  [README](https://raw.githubusercontent.com/encode/uvicorn/main/README.md)
- granian: server HTTP in Rust (Hyper/Tokio), ASGI/3, RSGI e WSGI, HTTP/1 e HTTP/2 (HTTP/3 «eventualmente»), HTTPS,
  WebSocket, file statici; sconsigliato se l'applicazione usa `trio` o `gevent` o estensioni ASGI non implementate.
  [README](https://raw.githubusercontent.com/emmett-framework/granian/master/README.md)

**psycopg**: il pacchetto è LGPL-3.0-only (metadati PyPI e LICENSE). L'installazione `psycopg[binary]` include libpq
precompilata. [installazione](https://www.psycopg.org/psycopg3/docs/basic/install.html). Supporta LISTEN/NOTIFY con il
generatore `Connection.notifies()`, anche in async. [async](https://www.psycopg.org/psycopg3/docs/advanced/async.html)

### DEDUZIONI

- Per una base che parte ora: **Django 6.1 su Python 3.13 o 3.14** e migrazione pianificata a **6.2 LTS (aprile
  2027)**, che copre fino ad aprile 2030. Partire su 5.2 LTS vuol dire migrare due volte (a 6.x e poi oltre) entro il
  2028. Dal 2028 il ritmo annuale rende gli aggiornamenti più regolari e prevedibili.
- Il canale server → dispositivi con SSE richiede **ASGI** (uvicorn o granian) e viste asincrone con middleware
  asincrono; altrimenti ogni connessione aperta occupa un thread/processo.
- **Tasks di Django** dà un'API standard, ma l'esecuzione la porta un pacchetto esterno: `django-tasks-db` è il più
  semplice (stesso database, niente Redis) ma è ancora 0.x e senza cron documentato; Procrastinate è più completo
  (sezione B) ma ha un'API propria.
- LGPL di psycopg: si importa come libreria senza modificarla. Che questo non imponga obblighi sul codice del gestionale
  è la lettura comune della LGPL, **non un parere legale** e non verificato su una fonte ufficiale di psycopg 3.
- FastAPI è un'alternativa più leggera ma senza ORM, admin, migrazioni e autenticazione di serie; resta 0.x.

## B. Database

### FATTI: PostgreSQL

| Major | Minor attuale | Supportata | Prima uscita | Fine supporto |
|---|---|---|---|---|
| 19 | 19.0 | sì | 19/11/2026 | 19/11/2031 |
| 18 | 18.7 | sì | 25/09/2025 | 14/11/2030 |
| 17 | 17.12 | sì | 26/09/2024 | 08/11/2029 |
| 16 | 16.16 | sì | 14/09/2023 | 09/11/2028 |
| 15 | 15.20 | sì | 13/10/2022 | 11/11/2027 |
| 14 | 14.25 | **no** | 30/09/2021 | 12/11/2026 |

Fonte: [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/).

**LISTEN/NOTIFY** ([NOTIFY](https://www.postgresql.org/docs/current/sql-notify.html)):

- Payload: «nella configurazione di default deve essere più corto di **8000 byte**»; per dati grandi conviene salvarli
  in una tabella e inviare la chiave.
- Le notifiche inviate in una transazione arrivano **solo dopo il commit**; una sessione in ascolto le riceve solo fra
  una transazione e l'altra. Notifiche identiche (stesso canale e payload) nella stessa transazione arrivano una volta
  sola; l'ordine è garantito per transazione e fra transazioni nell'ordine di commit.
- Coda delle notifiche: 8 GB nell'installazione standard; se si riempie, le transazioni con NOTIFY falliscono al
  commit. Una sessione in LISTEN che resta a lungo in una transazione blocca la pulizia (avvisi nel log a metà coda).
- Le notifiche non si accumulano per chi non è in ascolto: vanno solo alle sessioni che hanno eseguito LISTEN (dedotto
  dal testo della pagina; non c'è persistenza).

### FATTI: pgvector

- Licenza PostgreSQL (stile BSD). Ultima versione **0.8.7 del 01/10/2026** (fix di un buffer overflow nella
  costruzione di indici IVFFlat); 0.9.0 in sviluppo, che **toglie il supporto a Postgres 13 e 14**. Il README dichiara
  «Postgres 13+». [README](https://github.com/pgvector/pgvector), [CHANGELOG](https://raw.githubusercontent.com/pgvector/pgvector/master/CHANGELOG.md),
  [LICENSE](https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE)
- «Per default pgvector esegue la ricerca esatta del vicino più prossimo, con recall perfetto»; HNSW e IVFFlat sono
  opzionali. [README, Indexing](https://github.com/pgvector/pgvector#indexing)
- **Ricerca esatta più veloce**: «per accelerare le query senza indice, aumentare `max_parallel_workers_per_gather`»;
  con vettori normalizzati a lunghezza 1 usare il prodotto interno (`<#>`). [README, Exact Search](https://github.com/pgvector/pgvector#exact-search)
- **Dimensioni**: `vector` occupa `4 × dimensioni + 8` byte, `halfvec` `2 × dimensioni + 8`; entrambi **fino a 16.000
  dimensioni** in tabella. I limiti **2.000 (`vector`) e 4.000 (`halfvec`)** valgono per gli indici HNSW e IVFFlat.
  [README, Reference](https://github.com/pgvector/pgvector#reference)
- Prestazioni: usare `halfvec` per un working set più piccolo e storage `PLAIN`
  (`CREATE TABLE items (embedding halfvec(...) STORAGE PLAIN)`); caricamento in blocco con `COPY ... FORMAT BINARY`.
  [README, Performance](https://github.com/pgvector/pgvector#performance)
- Supporto a Postgres 18 aggiunto in 0.8.x; **nessuna menzione di Postgres 19** nel CHANGELOG letto.
- Client Python: `pgvector` 0.5.1 (MIT, 09/10/2026), con integrazione Django. [PyPI](https://pypi.org/project/pgvector/),
  [README](https://github.com/pgvector/pgvector-python)

### FATTI: code di lavori su PostgreSQL

| Strumento | Licenza | Versione e data | Note dalla fonte |
|---|---|---|---|
| Procrastinate | MIT ([LICENSE](https://raw.githubusercontent.com/procrastinate-org/procrastinate/main/LICENSE.md)) | 3.12.0, 19/11/2026 ([PyPI](https://pypi.org/project/procrastinate/)) | Python 3.11+, PostgreSQL 13+, sync e async, integrazione Django (`procrastinate.contrib.django`), **attività periodiche** con sintassi cron (`@app.periodic`), retry, lock; usa **LISTEN** per sapere quando c'è un lavoro (una connessione dedicata); dipende da `psycopg[pool]`. Il README dice che il progetto «cerca altri manutentori». ([README](https://raw.githubusercontent.com/procrastinate-org/procrastinate/main/README.md), [Django](https://procrastinate.readthedocs.io/en/stable/howto/django/configuration.html), [periodiche](https://procrastinate.readthedocs.io/en/stable/howto/advanced/cron.html), [discussioni](https://procrastinate.readthedocs.io/en/stable/discussions.html)) |
| django-tasks-db | BSD-3-Clause | 0.13.0, 28/08/2026 | backend ORM del framework Tasks, worker `db_worker` (sezione A) |
| huey | MIT ([LICENSE](https://raw.githubusercontent.com/coleifer/huey/master/LICENSE)) | 3.5.4, 01/11/2026 ([PyPI](https://pypi.org/project/huey/)) | backend Redis, SQLite, Postgres; usabile come backend Tasks ([ecosystem](https://www.djangoproject.com/community/ecosystem/)) |
| django-q2 | MIT | 1.11.1, 26/08/2026 ([PyPI](https://pypi.org/project/django-q2/)) | non approfondito |

### DEDUZIONI

- **PostgreSQL 18** è la scelta prudente oggi: supportato fino al 2030 e con supporto pgvector dichiarato. La 19 è
  uscita ieri: conviene aspettare la conferma di compatibilità di pgvector (e qualche minor) prima di adottarla.
- Dimensionamento (calcolo mio, formula del README, senza indice né overhead di riga):

  | Impronte | 768 dim. `vector` | 768 dim. `halfvec` | 1024 dim. `vector` | 1024 dim. `halfvec` |
  |---|---|---|---|---|
  | 175.000 | 539 MB | 270 MB | 718 MB | 360 MB |
  | 350.000 | 1,08 GB | 540 MB | 1,44 GB | 720 MB |

  Con `halfvec` tutto sta comodamente in RAM su un server con 8-16 GB. Un `vector` a 768 dimensioni (3.080 byte) supera
  la soglia oltre cui PostgreSQL sposta i valori fuori riga (TOAST, ~2 KB: dalla memoria, non verificato in questa
  ricerca): per questo il README consiglia `STORAGE PLAIN`.
- La ricerca esatta in pgvector è una scansione sequenziale parallelizzabile: con 350.000 righe è plausibile restare in
  decine o poche centinaia di millisecondi (IPOTESI: **va misurata** sulla macchina; nessun dato pubblicato trovato).
  Se `halfvec` cambia l'ordine dei risultati rispetto a `vector` va misurato sul nostro insieme di prova.
- **LISTEN/NOTIFY è adatto come campanello** (avvisare che «l'ordine 123 è cambiato»), non come trasporto dei dati: 8000
  byte, nessuna persistenza, consegna solo dopo il commit. Chi si riconnette deve rileggere lo stato dal database (vedi
  SSE con `Last-Event-ID`, sezione C).
- Coda di lavori: con Django + PostgreSQL le due strade senza Redis sono **django-tasks-db** (API standard Django,
  minimale) e **Procrastinate** (più completo, cron incluso, ma un solo gruppo di manutentori che ne cerca altri). Il
  rischio di manutenzione va pesato; il passaggio dall'uno all'altro è più facile se i lavori sono scritti con l'API
  Tasks di Django (Procrastinate non risulta, nelle pagine lette, offrire un backend per Tasks: non verificato).

## C. Browser

### FATTI: htmx

| Pacchetto | Licenza | Versione | Data | Fonte |
|---|---|---|---|---|
| htmx.org 2.x («latest» su npm) | 0BSD | 2.0.11 | 22/09/2026 | [npm](https://www.npmjs.com/package/htmx.org) |
| htmx.org 4.x (tag «next») | 0BSD | 4.0.2 (4.0.0 del 28/08/2026) | 18/11/2026 | [npm](https://www.npmjs.com/package/htmx.org) |
| htmx-ext-sse (per htmx 2) | **non indicata** nei metadati npm; LICENSE del repository non trovato | 2.2.4 | 18/10/2025 | [npm](https://www.npmjs.com/package/htmx-ext-sse) |

- Dal sito: «htmx 4.0 è stato rilasciato! Non è marcato come latest su NPM perché chi usa la linea 2.x non venga
  aggiornato per sbaglio. Lo marcheremo latest **nel corso del 2027**.» [htmx.org](https://htmx.org/)
- Non esiste una versione 3 pubblicata su npm (elenco versioni del registro).
- htmx 4: lo streaming si fa con estensioni (`hx-sse`, `hx-ws`, `hx-multipart`). [documentazione htmx 4](https://four.htmx.org/docs/)
- Estensione SSE per htmx 2: si collega a un `EventSource`; aggiunge una propria **riconnessione con backoff
  esponenziale** sopra quella del browser, perché «in rari casi» quella del browser non funziona.
  [htmx SSE](https://htmx.org/extensions/sse/)

### FATTI: Server-Sent Events

- Il browser **si riconnette da solo** se la connessione si chiude; il server può fermare le riconnessioni rispondendo
  **204 No Content**. Alla riconnessione il browser invia l'intestazione **`Last-Event-ID`** con l'ultimo `id:` ricevuto.
  [HTML Living Standard, SSE](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- Il campo `retry:` imposta l'attesa prima di riconnettersi (millisecondi).
  [MDN, Using SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- «Se non usato su HTTP/2, SSE soffre di un limite al numero massimo di connessioni aperte … per browser e fissato a un
  numero molto basso (**6**)», per browser + dominio e **condiviso fra tutte le schede**; segnato «Won't fix» in Chrome
  e Firefox. «Con HTTP/2 il numero massimo di stream simultanei è negoziato tra server e client (default 100).»
  [MDN EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)

### FATTI: BarcodeDetector

Dati MDN [browser-compat-data, api/BarcodeDetector.json](https://github.com/mdn/browser-compat-data/blob/main/api/BarcodeDetector.json)
(ramo main, letto il 20/11/2026; stato «sperimentale»):

| Browser | Supporto |
|---|---|
| Chrome Android | sì, da 83 (anche WebView Android e Samsung Internet, che rispecchiano Chrome Android) |
| Chrome desktop | parziale: **solo ChromeOS e macOS** (Windows e Linux no) |
| Edge | solo macOS |
| Safari / Safari iOS (17 → 26.x) | **solo dietro flag** «Shape Detection API» (preferenza), da 17 |
| Firefox (desktop e Android) | no ([bug 1553738](https://bugzil.la/1553738)) |

### FATTI: zxing-wasm e barcode-detector (Sec-ant)

| Pacchetto | Licenza | Versione e data | Cosa fa | Fonte |
|---|---|---|---|---|
| zxing-wasm | MIT (codice proprio); zxing-cpp Apache 2.0; zint BSD-3 | 3.1.7, 15/11/2026 (rilasci mensili nel 2026) | zxing-cpp compilato in WebAssembly; sottopercorsi `full` (lettura+scrittura, .wasm ~1,46 MiB), `reader` (~1,04 MiB), `writer` (~636 KiB) | [README](https://github.com/Sec-ant/zxing-wasm), [npm](https://www.npmjs.com/package/zxing-wasm) |
| barcode-detector | MIT | 3.2.4, 15/11/2026 (rilasci mensili nel 2026) | ponyfill/polyfill dell'API Barcode Detection basato su zxing-wasm | [README](https://github.com/Sec-ant/barcode-detector), [npm](https://www.npmjs.com/package/barcode-detector) |

- Formati (barcode-detector): lineari codabar, code_39 (varianti), code_32, pzn, code_93, code_128, DataBar (varianti),
  dx_film_edge, ean_8, ean_13, ean_upc, isbn, itf, itf_14, upc_a, upc_e, telepen; matriciali aztec, data_matrix,
  maxi_code (solo immagini monocromatiche pure), pdf417 (anche compact/micro), qr_code (model 1/2), micro_qr_code,
  rm_qr_code. [README](https://github.com/Sec-ant/barcode-detector)
- **Polyfill**: registra `BarcodeDetector` solo se non esiste già; non controlla se l'implementazione nativa supporta
  tutti i formati. **Ponyfill**: da importare esplicitamente, usa sempre zxing. [README](https://github.com/Sec-ant/barcode-detector)
- **.wasm in locale**: per default il percorso del .wasm è un URL **jsDelivr**; per CSP o uso offline si cambia con
  `prepareZXingModule({ overrides: { locateFile } })`, oppure si passa il binario con `wasmBinary`. Sono esportati
  `ZXING_WASM_VERSION` e `ZXING_WASM_SHA256`. [zxing-wasm, Configuring .wasm Serving](https://github.com/Sec-ant/zxing-wasm#configuring-wasm-serving)

### FATTI: archiviazione nel browser

- IndexedDB può salvare **Blob e File** (clonazione strutturata).
  [MDN IndexedDB terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology)
- **Safari, limite di 7 giorni** (blog WebKit, 24/03/2020): ITP cancella «tutto lo storage scrivibile da script»
  (IndexedDB, LocalStorage, Media keys, SessionStorage, registrazioni dei Service Worker e cache) **dopo sette giorni di
  uso di Safari senza interazione dell'utente con il sito**. Le web app aggiunte alla schermata Home hanno un contatore
  proprio basato sul loro uso; WebKit «non si aspetta» cancellazioni per il primo livello in una web app e le
  considererebbe «un bug grave». [WebKit blog 10218](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/)
- **«Updates to Storage Policy»** (blog WebKit, 10/08/2023), da Safari 17 / iOS 17: quota per origine fino al **60%
  del disco** nelle app browser (15% nelle altre app con WebView); quota complessiva 80% (20%); Safari 17 non chiede più
  il permesso per usare più spazio; le web app standalone hanno le stesse quote. La cancellazione automatica avviene se
  si supera la quota complessiva, se il sistema è a corto di spazio o se il sito non viene usato per un certo tempo
  (ITP); ordine LRU per origine. Un'origine è esclusa se ha una pagina attiva o se il suo storage è **persistente**.
  `navigator.storage.persist()` è concesso da WebKit «in base a euristiche, come l'apertura come web app della
  schermata Home». [WebKit blog 14403](https://webkit.org/blog/14403/updates-to-storage-policy/)
- `StorageManager.persist()`: Chrome 55+, Firefox 57+, Safari 15.2+ (iOS idem). Firefox mostra una richiesta
  all'utente; Safari e Chromium decidono da soli in base all'interazione con il sito, senza chiedere. Dati persistenti
  si cancellano solo per scelta dell'utente.
  [BCD StorageManager](https://github.com/mdn/browser-compat-data/blob/main/api/StorageManager.json),
  [MDN quote e cancellazione](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
- `crypto.randomUUID()`: Chrome 92+, Firefox 95+, Safari 15.4+; **solo in contesto sicuro (HTTPS)**.
  [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/randomUUID),
  [BCD Crypto](https://github.com/mdn/browser-compat-data/blob/main/api/Crypto.json)

### DEDUZIONI

- **htmx**: scegliere 2.x oggi è sicuro (è la «latest») ma porta una migrazione alla 4 nel 2027-2028; partire dalla
  4.x evita la migrazione ma usa un ramo che il progetto stesso non indica ancora come predefinito. Decisione da
  prendere sapendo questo; la licenza dell'estensione SSE per la 2.x va verificata prima di adottarla.
- **SSE**: l'operatore che apre più schede sullo stesso server con HTTP/1.1 esaurisce presto le 6 connessioni (ogni
  scheda con un canale aperto ne consuma una, e le altre richieste aspettano). **HTTP/2 è di fatto obbligatorio**:
  richiede HTTPS, cosa che serve comunque per la fotocamera. Una sola connessione SSE per scheda, con eventi numerati
  (`id:`) e il server che usa `Last-Event-ID` (o semplicemente rimanda lo stato attuale) alla riconnessione.
- **Barcode**: sui palmari Android e telefoni Android la via nativa funziona; per iPhone e PC Windows/Linux serve il
  ponyfill. Conviene usare **sempre il ponyfill su iPhone/PC e il nativo solo dove c'è**, con il .wasm (~1 MiB, sola
  lettura) servito dal nostro server con `locateFile` e messo in cache. I palmari a grilletto in genere inviano il codice
  come tastiera (dalla memoria, non verificato qui): il barcode via fotocamera serve soprattutto a telefoni e PC.
- **Operazioni in attesa nel browser** (con foto 0,3-0,6 MB): IndexedDB con Blob va bene per dimensioni e quote
  (decine di foto = decine di MB, lontani dal 60% del disco). Il rischio vero è la **cancellazione su Safari dopo 7
  giorni senza uso** se l'app è usata nel browser e non dalla schermata Home, e la cancellazione per poco spazio se lo
  storage non è persistente. Quindi: chiedere `persist()`, consigliare l'installazione sulla schermata Home su iPhone,
  inviare al server appena c'è rete, e mostrare all'operatore quante operazioni sono ancora solo sul telefono.
- Gli identificativi delle operazioni in attesa si possono generare con `crypto.randomUUID()` (idempotenza lato
  server), possibile solo perché l'app è in HTTPS.

## D. HTTPS e rete

### FATTI: Caddy

- Licenza **Apache 2.0** ([LICENSE](https://raw.githubusercontent.com/caddyserver/caddy/master/LICENSE)); ultima
  **v2.11.9 del 05/11/2026** (v2.11.8 il 04/11, v2.11.7 il 03/10). [Releases](https://github.com/caddyserver/caddy/releases)
- HTTPS automatico per ogni sito con un host; per IP e nomi interni Caddy crea una **propria CA** (radice +
  intermedia; dati in `pki/authorities/local`; basata su Smallstep). «Funziona solo sulla macchina locale ed è
  considerata affidabile solo dove è installato il certificato radice.» Caddy prova a installare la radice nel trust
  store **del server**; per gli altri dispositivi «è responsabilità dell'amministratore» aggiungere la radice.
  L'intermedio ha vita più breve e si rinnova da solo. [Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
- Direttiva `tls internal`: certificati dalla CA interna; `tls { dns <provider> ... }` per la sfida DNS.
  [tls](https://caddyserver.com/docs/caddyfile/directives/tls)
- **Sfida DNS-01**: nessuna porta aperta, il server non deve essere raggiungibile da internet; servono le credenziali
  del provider DNS. Il supporto dei provider è «uno sforzo della comunità»: il modulo DNS va **inserito nella build**,
  scaricandola dalla [pagina download](https://caddyserver.com/download) con il modulo scelto oppure con
  `xcaddy build --with github.com/caddy-dns/REPOSITORY`.
  [Automatic HTTPS](https://caddyserver.com/docs/automatic-https), [wiki moduli DNS](https://caddy.community/t/how-to-use-dns-provider-modules-in-caddy-2/8148)
- **Delega CNAME**: «si possono usare record CNAME per delegare la risposta alla sfida ad altre zone DNS … utile se il
  provider DNS non ha un'API o non è supportato da un plugin». [Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
- Protocolli di default: **`h1 h2 h3`** (HTTP/1.1, HTTP/2, HTTP/3). [Global options](https://caddyserver.com/docs/caddyfile/options)
- `reverse_proxy`: le risposte con `Content-Type: text/event-stream` vengono **inviate subito**, senza buffer.
  [reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy)

### FATTI: provider DNS

- Moduli `caddy-dns` registrati nel catalogo Caddy: 67, fra cui **cloudflare, ovh**, acmedns, rfc2136, netcup, ionos,
  hetzner, gandi, route53… **Nessuno per Aruba o Register.it**; la ricerca «aruba» nell'organizzazione caddy-dns su
  GitHub dà 0 risultati. [API pacchetti Caddy](https://caddyserver.com/api/packages),
  [org caddy-dns](https://github.com/orgs/caddy-dns/repositories?q=aruba)
- **lego** (go-acme, MIT, [LICENSE](https://raw.githubusercontent.com/go-acme/lego/master/LICENSE)): ultima **v5.6.0 del 28/10/2026**. Nella cartella
  `providers/dns` (commit del 19/11/2026) ci sono **ovh, cloudflare** e anche **shellrent** (hoster con sito
  shellrent.com, da v4.16.0); **nessun provider Aruba o Register.it**.
  [Releases](https://github.com/go-acme/lego/releases), [providers/dns](https://github.com/go-acme/lego/tree/master/providers/dns)
- **Let's Encrypt**: DNS-01 mette un TXT su `_acme-challenge.<dominio>`; ha senso se il provider ha un'API; «si possono
  usare record CNAME o NS per delegare la risposta» a un server o zona dedicata. Propagazione lenta in alcuni provider
  (fino a un'ora). [Challenge types](https://letsencrypt.org/docs/challenge-types/)
- **acme-dns** (MIT): server DNS minimale con API REST solo per i TXT, pensato proprio per i CNAME di
  `_acme-challenge`; se le chiavi trapelano, il danno è limitato a quel TXT. Ultimo tag v2.0.2; stato archiviato non
  determinato con certezza (nessun avviso trovato). [README](https://github.com/joohoi/acme-dns)
- **Durata dei certificati Let's Encrypt** (blog, 02/12/2025): profilo predefinito a **64 giorni dal 10/02/2027** (riuso
  dell'autorizzazione 10 giorni) e **45 giorni dal 16/02/2028** (riuso 7 ore). Annunciato anche **DNS-PERSIST-01**
  (record TXT fisso, senza aggiornare il DNS a ogni rinnovo). [Let's Encrypt](https://letsencrypt.org/2025/12/02/from-90-to-45/)
- DNS-PERSIST-01: post del 18/02/2026 con produzione prevista nel Q2 2026; nel forum ufficiale (aprile-maggio 2026)
  risultava **solo in staging** (bozza draft-00). Risultati di ricerca riportano un rinvio dichiarato dallo staff a
  giugno 2026 in attesa di una questione aperta nella bozza IETF: **non ho trovato conferma che sia in produzione**.
  [post](https://letsencrypt.org/2026/02/18/dns-persist-01), [forum](https://community.letsencrypt.org/t/dns-persist-01-deployment-status-and-timeline/246468)

### DEDUZIONI

- Tre strade per un certificato valido sui telefoni:
  1. **Dominio aziendale + DNS-01** (es. `magazzino.azienda.it` che risolve all'IP interno): nessuna installazione sui
     dispositivi. Funziona subito con OVH o Cloudflare; con Aruba/Register.it serve **delegare con CNAME**
     `_acme-challenge.magazzino` a una zona con API (es. una zona su Cloudflare/OVH o un acme-dns) oppure spostare il DNS.
  2. **`tls internal`** (CA di Caddy): nessun dominio pubblico, ma la radice va installata su **ogni** telefono, palmare
     e PC (su iPhone: profilo + abilitazione manuale dell'attendibilità completa; dalla memoria, non verificato qui), e
     va rifatto per ogni dispositivo nuovo.
  3. CA aziendale esistente (se l'azienda ne ha una gestita via MDM): come 2 ma distribuita centralmente.
- Con i certificati da 45-64 giorni il rinnovo **deve** essere automatico: la strada 1 con DNS manuale non regge; la
  delega CNAME risolve una volta per tutte (finché DNS-PERSIST-01 non è in produzione).
- Il binario Caddy con modulo DNS è una build personalizzata: va ricostruita a ogni aggiornamento (pagina download o
  xcaddy), cosa da prevedere nella procedura di aggiornamento.

## E. PDF e posta

### FATTI

- **WeasyPrint**: BSD-3-Clause ([LICENSE](https://raw.githubusercontent.com/Kozea/WeasyPrint/main/LICENSE)); **70.0
  del 08/09/2026** ([PyPI](https://pypi.org/project/weasyprint/)). Richiede Python ≥ 3.10 e **Pango ≥ 1.44** (più
  HarfBuzz, fontconfig, GObject come librerie di sistema); se il Pango della distribuzione è troppo vecchio si può usare
  WeasyPrint 52.5. [First steps](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
- **Microsoft 365 / Exchange Online, SMTP AUTH con autenticazione di base** (blog Exchange Team, 27/01/2026,
  aggiornato 29/01/2026): comportamento invariato fino a dicembre 2026; **a fine dicembre 2026 disattivata per default
  nei tenant esistenti** (gli amministratori possono riattivarla); **non disponibile per default nei tenant creati dopo
  dicembre 2026**, dove OAuth è il metodo supportato; la **data di rimozione definitiva sarà annunciata nella seconda
  metà del 2027**. [Exchange Team blog](https://techcommunity.microsoft.com/blog/exchange/updated-exchange-online-smtp-auth-basic-authentication-deprecation-timeline/4489835)
- Alternative documentate da Microsoft per app e dispositivi
  ([Microsoft Learn](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365)):
  - **SMTP client submission con OAuth** (porta 587); l'autenticazione di base non è compatibile con i Security
    defaults di Entra ID.
  - **SMTP relay con connettore in ingresso**, autenticato da **certificato TLS** (consigliato) o **IP pubblico statico**
    non condiviso; porta 25.
  - **Direct Send** (non autenticato, solo verso caselle del proprio tenant) e **High Volume Email** (account HVE).
- OAuth per SMTP/IMAP/POP: formato **SASL XOAUTH2**; è ammesso il flusso **client credentials** (senza utente).
  [Microsoft Learn OAuth](https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth)
- **Microsoft Graph `sendMail`**: `POST /users/{id}/sendMail`, permesso `Mail.Send` (anche come permesso applicativo).
  [Graph user-sendmail](https://learn.microsoft.com/en-us/graph/api/user-sendmail)
- **Google Workspace / Gmail**: dal **14/03/2025** l'accesso con password a IMAP, SMTP, POP, CalDAV, CardDAV è spento
  per tutti gli account; si usa OAuth, «con l'eccezione delle password per le app».
  [Transition from less secure apps to OAuth](https://support.google.com/a/answer/14114704?hl=en)
- Password per le app: «non consigliate e non necessarie nella maggior parte dei casi»; codice di 16 cifre; solo con la
  **verifica in due passaggi** attiva. [Sign in with app passwords](https://support.google.com/accounts/answer/185833?hl=en)
- **Python**: `smtplib.SMTP.auth(mechanism, authobject)` e `imaplib.IMAP4.authenticate(mechanism, authobject)` accettano
  un meccanismo SASL qualsiasi annunciato dal server, con un oggetto che produce la risposta; **non c'è un aiuto
  XOAUTH2 già pronto** e il token va ottenuto a parte.
  [smtplib](https://docs.python.org/3/library/smtplib.html), [imaplib](https://docs.python.org/3/library/imaplib.html)

### DEDUZIONI

- WeasyPrint va bene per bolle e documenti da HTML/CSS; la dipendenza da Pango è un motivo in più per distribuire il
  server **in un contenitore** (librerie di sistema fissate).
- Posta in uscita: progettare un **adattatore di invio** con tre modalità: SMTP con password (server generici, Google
  con password per le app), **SMTP con XOAUTH2** (Microsoft 365, Google) e **Graph sendMail** (Microsoft 365), più il
  relay con connettore come opzione dell'IT. Per Microsoft 365 l'autenticazione di base **non va proprio prevista come
  default**: nei tenant nuovi non c'è già più, negli altri si spegne a fine dicembre 2026.
- La lettura della posta in arrivo (es. bolle via email, vedi `2026-11-18-lettura-automatica-bolle.md`) ha gli stessi
  vincoli: IMAP con XOAUTH2 o Graph.
- XOAUTH2 con `smtplib`/`imaplib` richiede poco codice, ma la gestione del token (MSAL per Microsoft, OAuth Google) è
  una dipendenza in più (librerie non verificate in questa ricerca).

## F. Installazione

### FATTI

| Componente | Licenza | Versione e data | Note | Fonte |
|---|---|---|---|---|
| Docker Engine (moby) | Apache 2.0 | 29.10.0, 16/11/2026 | installazione nativa su Linux (Ubuntu, Debian, RHEL, Fedora…) o binari statici | [LICENSE](https://raw.githubusercontent.com/moby/moby/master/LICENSE), [release notes](https://docs.docker.com/engine/release-notes/), [install](https://docs.docker.com/engine/install/) |
| Docker Desktop | proprietaria (Docker Subscription Service Agreement) | — | gratis per piccole imprese (**< 250 dipendenti E < 10 milioni di dollari** di fatturato), uso personale, istruzione, open source non commerciale; **a pagamento** per uso professionale nelle organizzazioni più grandi | [Docker Desktop license](https://docs.docker.com/subscription/desktop-license/) |
| Docker Compose | Apache 2.0 | v5.8.0, 17/11/2026 | la 5.8.0 aggiunge i «jobs» programmati | [LICENSE](https://raw.githubusercontent.com/docker/compose/main/LICENSE), [Releases](https://github.com/docker/compose/releases) |
| NVIDIA Container Toolkit | Apache 2.0 | v1.20.2, 17/11 (anno non mostrato, presumibilmente 2026) | serve il driver NVIDIA sull'host; `nvidia-ctk runtime configure --runtime=docker` modifica `/etc/docker/daemon.json`; supporta Docker, containerd, CRI-O, Podman | [LICENSE](https://raw.githubusercontent.com/NVIDIA/nvidia-container-toolkit/main/LICENSE), [Releases](https://github.com/NVIDIA/nvidia-container-toolkit/releases), [install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) |
| Watchtower | Apache 2.0 | ultimo tag v1.7.1 | **archiviato il 17/12/2025**; il README dice «questo progetto non è più mantenuto» | [repository](https://github.com/containrrr/watchtower), [README](https://raw.githubusercontent.com/containrrr/watchtower/main/README.md) |
| Podman | Apache 2.0 | v6.2.0, 10/11 (anno non mostrato; v5.8.10 nello stesso giorno) | alternativa a Docker | [LICENSE](https://raw.githubusercontent.com/containers/podman/main/LICENSE), [Releases](https://github.com/containers/podman/releases) |

- La pagina di Docker Engine precisa: «l'uso commerciale di Docker Engine **ottenuto tramite Docker Desktop**» nelle
  aziende oltre le soglie richiede l'abbonamento; la licenza di Docker Engine e dei progetti Moby «non cambia».
  [Docker Engine](https://docs.docker.com/engine/), [Desktop license](https://docs.docker.com/subscription/desktop-license/)
- NVIDIA segnala un problema noto: con i cgroup gestiti da systemd i contenitori possono perdere l'accesso alla GPU dopo
  un `systemctl daemon-reload`. [install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### DEDUZIONI

- Server in sede su **Linux con Docker Engine + Compose**: nessun costo di licenza. Su un server Windows servirebbe
  Docker Desktop (a pagamento oltre le soglie) o WSL con Docker Engine: va chiesto all'azienda che server ha.
- **Aggiornamenti senza Watchtower**: uno script/comando di aggiornamento esplicito (copia di sicurezza del database →
  scarico della nuova immagine con versione fissata → migrazioni → controllo di salute → in caso di errore ritorno
  all'immagine precedente e ripristino della copia). Le immagini vanno indicate con versione precisa, non `latest`,
  perché il ritorno indietro sia possibile.
- GPU NVIDIA nei contenitori: possibile e documentata, ma aggiunge driver sull'host e configurazione del runtime; da
  prevedere solo se le misure dicono che serve (vedi ricerca del 15/11).

## G. GitHub: rinomina di un repository

### FATTI

- «Quando rinomini un repository, tutte le informazioni esistenti, **con l'eccezione degli URL dei siti di progetto**,
  vengono reindirizzate automaticamente al nuovo nome» (issue, wiki, stelle, follower). `git clone`, `fetch` e `push`
  verso il vecchio indirizzo continuano a funzionare. Se il repository ha un sito GitHub Pages, GitHub **consiglia un
  dominio personalizzato** perché l'URL non dipenda dal nome. Le **GitHub Actions** ospitate in un repository rinominato
  **non** vengono reindirizzate. Se in futuro si crea un repository con il vecchio nome, i redirect smettono di
  funzionare. [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)
- Un sito di progetto si trova in `http(s)://<owner>.github.io/<repositoryname>`.
  [What is GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- API REST: usa redirect HTTP; **301** = spostamento permanente, da seguire e aggiornare nel codice. L'endpoint «Get a
  repository» elenca la risposta 301 «Moved permanently».
  [Best practices REST](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api),
  [Repos API](https://docs.github.com/en/rest/repos/repos)

### DEDUZIONI

- Dopo la rinomina `utente.github.io/VecchioNome` **non** porta al nuovo sito: i link pubblicati (documenti, QR,
  segnalibri) si rompono. Soluzioni: dominio personalizzato prima della rinomina, oppure lasciare un repository col
  vecchio nome con una pagina di rimando (ma questo annulla i redirect di git/web verso il repository rinominato, per
  l'avvertenza sopra: va scelto uno dei due).

## DEDUZIONI generali: cosa implicano i fatti per la base

Ipotesi di base: Python + Django, PostgreSQL + pgvector (ricerca esatta tra 175.000-350.000 impronte a 768-1024
dimensioni), canale aperto server → dispositivi, operazioni in attesa nel browser con una foto da 0,3-0,6 MB,
certificato del dominio aziendale o interno, aggiornamenti con copia di sicurezza e ritorno indietro.

1. **Versioni**: Django 6.1 (poi 6.2 LTS ad aprile 2027), Python 3.13/3.14, PostgreSQL 18 (19 dopo conferma pgvector),
   pgvector 0.8.7. Tutti con supporto oltre il 2028.
2. **Ricerca esatta in pgvector è sostenibile**: con `halfvec` 350.000 × 1024 dimensioni ≈ 720 MB, senza indice e senza
   limiti di dimensione (16.000); parallelismo per la velocità. Va misurato il tempo reale sulla macchina e il recupero
   `halfvec` vs `vector` sull'insieme di prova. Un indice HNSW resta possibile (fino a 4.000 dimensioni con `halfvec`)
   se un giorno servisse.
3. **Canale aperto**: SSE servito da Django sotto **ASGI** (uvicorn o granian), con **HTTP/2 obbligatorio** davanti
   (Caddy lo dà di serie e non bufferizza `text/event-stream`), eventi numerati e riallineamento dello stato alla
   riconnessione; **LISTEN/NOTIFY** solo come segnale interno fra processi (payload < 8000 byte, consegna dopo il commit).
   htmx 2.x + estensione SSE oppure htmx 4: scelta da fare sapendo che la 4 diventerà predefinita nel 2027.
4. **Lavori in background** (embedding delle foto, PDF, posta, import): API Tasks di Django + backend su PostgreSQL
   (django-tasks-db) oppure Procrastinate se servono cron e lock; niente Redis necessario.
5. **Operazioni in attesa**: IndexedDB con Blob, `persist()`, ID con `crypto.randomUUID()`, invio appena possibile e
   contatore visibile; su iPhone l'uso dalla schermata Home riduce il rischio della cancellazione dopo 7 giorni.
   Le quote non sono un problema per qualche decina di foto.
6. **Barcode nel browser**: nativo su Android, ponyfill zxing-wasm (~1 MiB, servito in locale) su iPhone e PC.
7. **Certificato**: preferire un sottodominio del dominio aziendale con DNS-01 (OVH/Cloudflare nativi; Aruba e
   Register.it solo con delega CNAME di `_acme-challenge`); `tls internal` solo se l'azienda accetta di installare la
   radice su ogni dispositivo. Rinnovo automatico obbligatorio (64 giorni dal 2027, 45 dal 2028).
8. **Posta**: OAuth/XOAUTH2 o Graph per Microsoft 365 (basic auth spenta a fine dicembre 2026), OAuth o password per le
   app per Google; relay con connettore come opzione dell'IT.
9. **Installazione e aggiornamenti**: Linux + Docker Engine + Compose (Apache 2.0, gratuiti); niente Watchtower
   (archiviato); aggiornamento con script esplicito: copia del database, immagini con versione fissata, migrazioni,
   controllo, ritorno all'immagine e alla copia precedenti in caso di errore. Caddy con modulo DNS è una build
   personalizzata da ricostruire a ogni aggiornamento.
10. **Licenze**: tutto permissivo (BSD, MIT, Apache 2.0, PostgreSQL, 0BSD) tranne **psycopg (LGPL-3.0)** e **Docker
    Desktop (commerciale oltre le soglie)**; da segnalare a chi decide.

## Cosa resta incerto

- **pgvector e PostgreSQL 19**: nessuna dichiarazione di supporto trovata (19 uscito il 19/11/2026).
- **Tempi reali della ricerca esatta** in pgvector con 175.000-350.000 righe: nessuna misura pubblicata trovata; da
  misurare.
- **DNS-PERSIST-01** di Let's Encrypt: stato in produzione non confermato da una fonte ufficiale recente.
- **Licenza di htmx-ext-sse**: il registro npm non la indica e non ho trovato il file LICENSE del repository
  htmx-extensions (404 sui percorsi provati).
- **acme-dns**: ultimo tag v2.0.2, ma data dell'ultimo rilascio e stato di archiviazione non letti con certezza.
- **Date** delle release di NVIDIA Container Toolkit e Podman: la pagina mostra giorno e mese, non l'anno.
- **Procrastinate come backend del framework Tasks di Django**: non trovato nelle pagine lette; non verificato.
- **TOAST oltre ~2 KB** e procedura di installazione della radice su iPhone/Android: dalla memoria, non verificati qui.
- **LGPL di psycopg**: nessuna nota ufficiale di psycopg 3 sull'uso in software chiuso letta; non è un parere legale.
- **Safari e Blob in IndexedDB**: il supporto generale è documentato da MDN, ma non ho cercato problemi specifici di
  WebKit con Blob grandi.
- I palmari a grilletto che inviano il codice come tastiera: comportamento tipico, non verificato su un modello.

## Fonti

Server Python
- Django download e supporto — https://www.djangoproject.com/download/
- Django FAQ Python — https://docs.djangoproject.com/en/6.1/faq/install/
- Django async — https://docs.djangoproject.com/en/6.1/topics/async/
- Django request/response — https://docs.djangoproject.com/en/6.1/ref/request-response/
- Django Tasks — https://docs.djangoproject.com/en/6.1/topics/tasks/ ; note 6.0 — https://docs.djangoproject.com/en/6.1/releases/6.0/
- Django databases — https://docs.djangoproject.com/en/6.1/ref/databases/
- Django Community Ecosystem — https://www.djangoproject.com/community/ecosystem/
- Python — https://www.python.org/downloads/ ; https://devguide.python.org/versions/
- PyPI (API JSON, 20/11/2026): Django, uvicorn, granian, psycopg, fastapi, procrastinate, django-tasks, django-tasks-db,
  huey, django-q2, weasyprint, pgvector — https://pypi.org/project/<nome>/
- uvicorn README — https://raw.githubusercontent.com/encode/uvicorn/main/README.md
- granian README — https://raw.githubusercontent.com/emmett-framework/granian/master/README.md
- psycopg LICENSE — https://raw.githubusercontent.com/psycopg/psycopg/master/LICENSE.txt ; installazione —
  https://www.psycopg.org/psycopg3/docs/basic/install.html ; async — https://www.psycopg.org/psycopg3/docs/advanced/async.html

Database
- PostgreSQL versioning — https://www.postgresql.org/support/versioning/
- PostgreSQL NOTIFY — https://www.postgresql.org/docs/current/sql-notify.html
- pgvector README — https://github.com/pgvector/pgvector ; CHANGELOG —
  https://raw.githubusercontent.com/pgvector/pgvector/master/CHANGELOG.md ; LICENSE —
  https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE
- pgvector-python — https://github.com/pgvector/pgvector-python
- Procrastinate — https://raw.githubusercontent.com/procrastinate-org/procrastinate/main/README.md ;
  https://procrastinate.readthedocs.io/en/stable/howto/django/configuration.html ;
  https://procrastinate.readthedocs.io/en/stable/howto/advanced/cron.html ;
  https://procrastinate.readthedocs.io/en/stable/discussions.html

Browser
- htmx — https://htmx.org/ ; htmx 4 — https://four.htmx.org/docs/ ; estensione SSE — https://htmx.org/extensions/sse/
- npm registry (20/11/2026): htmx.org, htmx-ext-sse, zxing-wasm, barcode-detector — https://www.npmjs.com/package/<nome>
- HTML Living Standard, SSE — https://html.spec.whatwg.org/multipage/server-sent-events.html
- MDN EventSource — https://developer.mozilla.org/en-US/docs/Web/API/EventSource ; Using SSE —
  https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- MDN browser-compat-data (BarcodeDetector, StorageManager, Crypto) — https://github.com/mdn/browser-compat-data
- zxing-wasm — https://github.com/Sec-ant/zxing-wasm ; barcode-detector — https://github.com/Sec-ant/barcode-detector
- WebKit, 7 giorni — https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
- WebKit, Updates to Storage Policy — https://webkit.org/blog/14403/updates-to-storage-policy/
- MDN quote e cancellazione — https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
- MDN IndexedDB — https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology
- MDN randomUUID — https://developer.mozilla.org/en-US/docs/Web/API/Crypto/randomUUID

HTTPS e rete
- Caddy Automatic HTTPS — https://caddyserver.com/docs/automatic-https ; tls —
  https://caddyserver.com/docs/caddyfile/directives/tls ; opzioni globali — https://caddyserver.com/docs/caddyfile/options ;
  reverse_proxy — https://caddyserver.com/docs/caddyfile/directives/reverse_proxy ; Releases —
  https://github.com/caddyserver/caddy/releases ; LICENSE — https://raw.githubusercontent.com/caddyserver/caddy/master/LICENSE
- Moduli DNS Caddy — https://caddy.community/t/how-to-use-dns-provider-modules-in-caddy-2/8148 ; catalogo —
  https://caddyserver.com/api/packages ; https://github.com/orgs/caddy-dns/repositories?q=aruba
- lego — https://github.com/go-acme/lego/releases ; https://github.com/go-acme/lego/tree/master/providers/dns
- Let's Encrypt challenge types — https://letsencrypt.org/docs/challenge-types/ ; 45 giorni —
  https://letsencrypt.org/2025/12/02/from-90-to-45/ ; DNS-PERSIST-01 — https://letsencrypt.org/2026/02/18/dns-persist-01 ;
  forum — https://community.letsencrypt.org/t/dns-persist-01-deployment-status-and-timeline/246468
- acme-dns — https://github.com/joohoi/acme-dns

PDF e posta
- WeasyPrint — https://doc.courtbouillon.org/weasyprint/stable/first_steps.html ; LICENSE —
  https://raw.githubusercontent.com/Kozea/WeasyPrint/main/LICENSE
- Exchange Team, SMTP AUTH — https://techcommunity.microsoft.com/blog/exchange/updated-exchange-online-smtp-auth-basic-authentication-deprecation-timeline/4489835
- Microsoft Learn, invio da app e dispositivi — https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365
- Microsoft Learn, OAuth IMAP/POP/SMTP — https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth
- Microsoft Graph sendMail — https://learn.microsoft.com/en-us/graph/api/user-sendmail
- Google, da app meno sicure a OAuth — https://support.google.com/a/answer/14114704?hl=en
- Google, password per le app — https://support.google.com/accounts/answer/185833?hl=en
- Python smtplib — https://docs.python.org/3/library/smtplib.html ; imaplib — https://docs.python.org/3/library/imaplib.html

Installazione
- Docker Engine — https://docs.docker.com/engine/ ; install — https://docs.docker.com/engine/install/ ; release notes —
  https://docs.docker.com/engine/release-notes/ ; LICENSE moby — https://raw.githubusercontent.com/moby/moby/master/LICENSE
- Docker Desktop license — https://docs.docker.com/subscription/desktop-license/
- Docker Compose — https://github.com/docker/compose/releases
- NVIDIA Container Toolkit — https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html ;
  https://github.com/NVIDIA/nvidia-container-toolkit/releases
- Watchtower — https://github.com/containrrr/watchtower
- Podman — https://github.com/containers/podman/releases

GitHub
- Renaming a repository — https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository
- What is GitHub Pages — https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- REST best practices — https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api ;
  Repos API — https://docs.github.com/en/rest/repos/repos

Non raggiungibili o non leggibili
- API GitHub e pagine github.com via curl bloccate in questa sessione: versioni da tag git, PyPI e npm; pagine github.com
  lette con uno strumento di estrazione testo (stato archiviato, date delle release).
- File LICENSE di htmx-extensions: 404 sui percorsi provati.
- Il post del forum Let's Encrypt del 25/06/2026 sul rinvio di DNS-PERSIST-01 non è stato aperto (citato da risultati
  di ricerca).
