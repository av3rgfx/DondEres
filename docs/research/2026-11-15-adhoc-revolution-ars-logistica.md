# Ad Hoc Revolution e ARS Logistica: come si scambiano i dati

Data: 15/11/2026

Legenda: **FATTO** = scritto nella fonte linkata accanto (pagina aperta il 15/11/2026). **DEDUZIONE** = conclusione
nostra a partire dai fatti. **IPOTESI** = da verificare. "Il produttore dichiara" = affermazione commerciale del
produttore, non verificata da terzi. "Fonte secondaria" = non viene dal produttore.

## Domanda

Quali interfacce di scambio offrono Ad Hoc Revolution e ARS Logistica, i due gestionali che il primo magazzino usa già?
Il nostro prodotto dovrà importarne articoli, ordini cliente e ordini fornitore, e restituire i movimenti di magazzino
(decisione 19). Chi produce i due programmi, che cosa fa ciascuno, come si dividono il lavoro, cosa serve per usarne le
interfacce, quali loro concetti si sovrappongono al nostro glossario.

## Sintesi

- **Ad Hoc Revolution** è il gestionale (ERP) di Zucchetti S.p.A. Esiste in due forme: la versione client/server
  classica e **Ad Hoc Revolution Web**, rifatta sulla piattaforma Infinity 4.0. Gestisce articoli, magazzini (anche
  logici), ubicazioni, lotti, matricole, ordini cliente e fornitore, DDT e documenti di magazzino.
- **ARS Logistica** (scritto anche **ARS@Logistica**) è un programma di gestione del magazzino (WMS) con app per
  telefono e tablet. Oggi lo sviluppa e lo vende **Datalite S.r.l.**, partner Zucchetti nata nel 2022 dalla fusione di
  Altaquota e PC System. Prima era un prodotto di **Altaquota**: è lo stesso prodotto, non due. Il produttore dichiara
  che è "nativamente integrato" con la linea Ad Hoc di Zucchetti.
- **Come convivono**: Ad Hoc Revolution tiene anagrafiche, ordini e documenti. ARS Logistica fa il lavoro fisico in
  magazzino (ricevimento, spostamenti, prelievo, inventario) e scrive il risultato direttamente nel gestionale sotto
  forma di documenti (documenti di carico, DDT, documenti intermedi, rilevazioni d'inventario).
- **Interfacce pubbliche**: nessuno dei due produttori pubblica API, servizi web, tracciati di file o schema del
  database. Zucchetti dichiara soltanto che Ad Hoc Revolution "importa direttamente archivi, movimenti contabili di
  magazzino e documenti" e che si integra "con altri software". Datalite dichiara lo scambio "in tempo reale" con il
  gestionale, senza dire come.
- **Vie possibili** (da confermare col rivenditore): file di import/export di Ad Hoc; accesso al database Microsoft SQL
  Server di Ad Hoc (lo usa almeno un partner Zucchetti, fonte secondaria); servizi web, ma solo sulla piattaforma
  Infinity (quindi forse su Revolution Web, non verificato); un'interfaccia fatta da Datalite su ARS Logistica.
- **Costi e licenze**: nessun prezzo pubblico per nessuno dei due. Moduli e funzioni dipendono da cosa il cliente ha
  attivato.
- **Attenzione a ARS Logistica**: fa già, su telefono, buona parte di ciò che farà il nostro prodotto (ricevimento,
  prelievo, inventario). Nel primo magazzino va chiarito chi fa cosa, altrimenti la stessa merce viene registrata due
  volte.
- **Parola ingannevole**: in Ad Hoc e in ARS "evadere" un ordine vuol dire, con buona probabilità, trasformarlo in un
  documento (DDT o documento intermedio). Nel nostro glossario "evaso" vuol dire "merce prelevata e pronta". Va
  verificato prima di mappare gli stati.

## 1. Chi produce i due programmi

### Ad Hoc Revolution (Zucchetti)
- FATTO: "Ad Hoc Revolution è il gestionale Zucchetti, modulare e scalabile"; copre "amministrazione, contabilità,
  controllo di gestione, vendite, acquisti, logistica e produzione"; si sceglie "tra 40 moduli disponibili".
  [zucchetti.it, descrizione](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-descrizione.html)
- FATTO: Zucchetti lo colloca tra i "gestionali client-server" (percorso della pagina) e lo rivolge alla "media o
  grande impresa"; la pagina delle funzioni e il partner Datalite parlano invece di PMI.
  [zucchetti.it, funzionalità](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-funzionalit.html),
  [datalite.it, Ad Hoc Revolution](https://datalite.it/soluzioni-software/software-zucchetti/ad-hoc-revolution/)
- FATTO: produttore Zucchetti S.p.A., P.IVA 05006900962 (piè di pagina del sito).
  [zucchetti.it](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-descrizione.html)
- FATTO: la brochure ufficiale scaricabile è "DAHR 5.1 – St. 10/2018" e ripete i testi del sito.
  [brochure AHR (PDF)](https://www.zucchetti.it/website/dms/website/prodotti/sw/Gestionali/brochure/AHR_Software_gestionale.pdf)

### Come distinguere i prodotti "Ad Hoc" di Zucchetti
Il nome "Ad Hoc" copre una famiglia. Al rivenditore va chiesto quale dei seguenti è installato.

| Prodotto | Cosa dice la fonte |
|---|---|
| Ad Hoc Revolution | Client/server, oltre 40 moduli ([zucchetti.it](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-descrizione.html)) |
| Ad Hoc Revolution Web | "Basata interamente su tecnologia Infinity 4.0", usabile da browser e da app, installabile "in azienda o nel Datacenter Zucchetti" ([zucchetti.it, AHRW](https://www.zucchetti.it/website/cms/ITA/prodotto/8314-ad-hoc-revolution-web.html)) |
| Ad Hoc Enterprise, Ad Hoc Infinity | Altri gestionali della stessa linea, citati da Altaquota come compatibili con ARS@Logistica ([aquota.net](https://www.aquota.net/prodotti/ars-logistica/)) |

- FATTO: Zucchetti ha anche un proprio WMS, separato dalla linea Ad Hoc, sviluppato su Infinity, che "communicates with
  the leading ERP systems on the market through standard interfaces or specific integration modules".
  [digitalsupplychain.zucchetti.it](https://digitalsupplychain.zucchetti.it/web/cms/ENG/digital-supply-chain.html)
  Non è ARS Logistica.

### ARS Logistica (Datalite, già Altaquota)
- FATTO: "ARS Logistica è il software sviluppato da Datalite per la gestione operativa e digitale del magazzino";
  "nativamente integrato con i gestionali Zucchetti".
  [datalite.it, ARS Logistica](https://datalite.it/soluzioni-software/suite-ars/ars-logistica/)
- FATTO: "La suite ARS, sviluppata da Datalite" comprende ARS Produco (MES), ARS Logistica (WMS), ARS Cantina, ARS
  Monitor; installazione "on-premise o in ambienti virtualizzati"; "interfaccia web e mobile".
  [datalite.it, Suite ARS](https://datalite.it/soluzioni-software/suite-ars/)
- FATTO: "Datalite nasce nel 2022, dall'incontro di Altaquota e PC System", due "storici partner Zucchetti del
  territorio toscano". Datalite si presenta come "Top Partner Zucchetti". Sede legale a Bientina (PI), sede operativa
  in Loc. Drove – Campomaggio 18, Poggibonsi (SI).
  [datalite.it, la nostra storia](https://datalite.it/chi-siamo/datalite-la-nostra-storia/)
- FATTO: il sito di Altaquota (Altaquota S.r.l., P.IVA 03761830961, stesso indirizzo di Poggibonsi, "Gruppo Ars
  Network") descrive ARS@Logistica con le stesse funzioni e la dichiara "totalmente integrato con la linea Ad Hoc
  Zucchetti (Ad Hoc Revolution, Ad Hoc Enterprise, Ad Hoc Infinity)".
  [aquota.net, ARS@Logistica](https://www.aquota.net/prodotti/ars-logistica/)
- DEDUZIONE: ARS Logistica e ARS@Logistica sono lo stesso prodotto, passato da Altaquota a Datalite con la fusione del
  2022 (stesso nome, stesse funzioni, stesso indirizzo, brochure Datalite che usa ancora la grafia "ARS@Logistica").
  Il rivenditore di entrambi i programmi nel primo magazzino potrebbe quindi essere Datalite: IPOTESI da verificare.

### Nomi simili da non confondere
- **ARSinform S.r.l.** (Milano): produce MAG-Net Enterprise, un sistema per magazzini automatici "interfacciabile con
  tutti i sistemi gestionali ERP". Azienda e prodotto diversi.
  [arsinform.it](https://www.arsinform.it/portfolio-articoli/controllo-e-gestione-di-magazzini-automatici/)
- **"NEX Logistica"**: compare nell'elenco delle soluzioni Zucchetti integrabili con Ad Hoc Revolution sulla pagina di
  Datalite, accanto a "NEX Fabrica" e "NEX Cantina".
  [datalite.it, Ad Hoc Revolution](https://datalite.it/soluzioni-software/software-zucchetti/ad-hoc-revolution/)
  Non abbiamo trovato altre informazioni. IPOTESI: un nuovo nome della suite ARS (i tre nomi corrispondono a ARS
  Logistica, ARS Produco/Fabrica, ARS Cantina) oppure un altro prodotto. Da chiedere.
- Una ricerca generica di "ARS Logistica" / "ARS Logistics" come software non ha dato altri prodotti.

## 2. Che cosa fa ciascuno e come si dividono il lavoro

### Ad Hoc Revolution: area logistica
- FATTO: "Cuore dell'area è il modulo Magazzino, che consente di gestire diversi magazzini (fisici o logici)", con
  tracciabilità "attraverso le dimensioni lotti, unità logistiche, ubicazioni o matricole"; "rileva le rettifiche
  inventariali"; collegamento "con registratori di cassa e lettori ottici".
  [zucchetti.it, funzionalità](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-funzionalit.html)
- FATTO: ciclo vendite e acquisti con "ordini clienti e fornitori, D.D.T., fatture", "proposte di acquisto con riordino
  automatico ai fornitori". [stessa pagina](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-funzionalit.html)
- FATTO (Revolution Web): il modulo "Ordini clienti/fornitori" è separato dal modulo "Magazzino e vendite"; gli ordini
  "diventano immediatamente visibili ed evadibili dal menù ordini delle vendite".
  [zucchetti.it, AHRW funzionalità](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-in-cloud/ad-hoc-revolution-web/software-gestionale-cloud-funzionalita.html)

### ARS Logistica: moduli
Fonte per tutto il blocco: [aquota.net](https://www.aquota.net/prodotti/ars-logistica/),
[datalite.it](https://datalite.it/soluzioni-software/suite-ars/ars-logistica/),
[brochure Datalite (PDF, v4)](https://datalite.it/wp-content/uploads/2024/07/Brochure_ArsLogistica_v4.pdf).

| Modulo | FATTO: cosa fa secondo il produttore |
|---|---|
| Logistica ingresso | L'operatore acquisisce da app i documenti di carico, "che vengono automaticamente memorizzati nel software gestionale aziendale" |
| Logistica interna | Spostamenti tra ubicazioni e depositi, guidati o liberi; invio merce ai terzisti (conto lavoro) |
| Logistica spedizioni | Liste di picking o packing, lettura barcode o percorso guidato per ubicazione; lotti e matricole "in funzione della configurazione dell'anagrafica presente nel software gestionale"; foto dell'articolo; stampa etichette colli. "La chiusura della lista di prelievo produce direttamente un documento gestionale (ddt o documento intermedio)" |
| Vendita assistita | Lista di prelievo per la vendita al banco; il documento di consegna si genera poi dal gestionale |
| Inventario | Rilevazioni inserite "direttamente nel software gestionale"; versione con rete e versione senza rete |
| Modula | "Consente di interfacciarsi con i magazzini automatici" |

- FATTO: Datalite dichiara anche l'"integrazione nativa con gli scanner Zebra".
  [datalite.it](https://datalite.it/soluzioni-software/suite-ars/ars-logistica/)
- FATTO: Modula S.p.A. (Salvaterra di Casalgrande, RE) "progetta e produce magazzini automatici verticali e
  orizzontali". [modula.eu](https://www.modula.eu/it/) DEDUZIONE: il modulo "Modula" di ARS serve a collegare questi
  magazzini automatici.
- DEDUZIONE sulla divisione del lavoro: ARS Logistica non ha anagrafiche proprie. Legge articoli, lotti, giacenze e
  ordini da Ad Hoc e vi scrive documenti (carico, DDT, documento intermedio, inventario). Ad Hoc resta il punto di
  riferimento per i dati; ARS è l'interfaccia di magazzino su telefono.
- IPOTESI: ARS legge e scrive direttamente nel database di Ad Hoc, o usa procedure di Ad Hoc. Nessuna fonte lo dice.

## 3. Interfacce di scambio

### Ad Hoc Revolution
- FATTO: "è possibile importare direttamente archivi, movimenti contabili di magazzino e documenti, tutto in maniera
  automatica"; esporta "verso i più diffusi programmi di produttività individuale e verso altri applicativi Zucchetti";
  "aggiornamento diretto dei dati tra il gestionale e il sito di e-commerce collegato".
  [zucchetti.it, funzionalità](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-funzionalit.html)
  Formati, tracciati e nome del modulo non sono indicati.
- FATTO: Revolution Web è "sviluppato con le tecnologie più avanzate per [...] poter integrare facilmente qualsiasi
  servizio/soluzione di Zucchetti o di terze parti". Nessun dettaglio tecnico.
  [zucchetti.it, AHRW](https://www.zucchetti.it/website/cms/ITA/prodotto/8314-ad-hoc-revolution-web.html)
- FATTO (documento Zucchetti del 2014 sulla piattaforma di sviluppo Sitepainter Infinity): le applicazioni Infinity
  seguono un'architettura SOA "per utilizzare come servizio le singole applicazioni anche attraverso appositi Web
  Service"; sono in Java (J2EE) e supportano "Microsoft SQL Server, Oracle, DB2, PostgreSQL, MySql".
  [strumenti di sviluppo (PDF)](https://zucchetti.it/website/dms/website/prodotti/sw/Tool%20sviluppo/strumenti_sviluppo.pdf)
  DEDUZIONE: Revolution Web, basato su Infinity 4.0, potrebbe esporre servizi web. Non verificato per questo prodotto,
  e non vale per la versione client/server.
- Fonte secondaria (tesi di laurea, Università di Padova, 2022, stage presso un partner Zucchetti): "Ad Hoc Revolution
  [...] si appoggia al DBMS Microsoft Sql Server"; il programma sviluppato "comunica direttamente con la banca dati
  gestionale" in rete locale, con servizio web solo se fuori rete.
  [tesi (PDF)](https://thesis.unipd.it/retrieve/c2defdcf-9610-416c-bb36-017830fbb8eb/Fichera_Jacopo%20%281%29.pdf)
  DEDUZIONE: l'accesso diretto al database è una via usata in pratica dai partner. Versione del database, schema e
  regole d'uso non sono pubblici.
- Non trovato: documentazione pubblica di API, servizi web, tracciati di import, schema del database, manuali
  scaricabili. Le schede Zucchetti rimandano al modulo di contatto e ai rivenditori.

### ARS Logistica
- FATTO: "Scambiare dati in tempo reale tra magazzino e amministrazione"; "allineare il magazzino con gli ordini e i
  documenti gestionali"; "ogni dato è sincronizzato con il gestionale".
  [datalite.it](https://datalite.it/soluzioni-software/suite-ars/ars-logistica/)
- FATTO: "Si può interfacciare con i principali software gestionali in commercio".
  [brochure (PDF)](https://datalite.it/wp-content/uploads/2024/07/Brochure_ArsLogistica_v4.pdf),
  [aquota.net](https://www.aquota.net/prodotti/ars-logistica/)
- FATTO: Datalite offre "personalizzazione e sviluppi ad hoc" e dice che "la suite ARS è sviluppata internamente".
  [datalite.it](https://datalite.it/soluzioni-software/suite-ars/ars-logistica/)
- Non trovato: API, servizi web, file di scambio, accesso al database per terzi. DEDUZIONE: un'interfaccia verso ARS si
  ottiene solo come sviluppo su richiesta di Datalite.

### Riepilogo delle vie possibili

| Via | Ad Hoc Revolution | ARS Logistica | Stato |
|---|---|---|---|
| API o servizi web | Forse su Revolution Web (piattaforma Infinity) | Non documentati | Da chiedere |
| File di import/export | Import di archivi, movimenti e documenti dichiarato | Non documentati | Tracciati da chiedere |
| Database | Microsoft SQL Server (fonte secondaria) | Ignoto | Permesso e schema da chiedere |
| Sviluppo su misura del partner | Possibile tramite rivenditore | Dichiarato da Datalite | Costo da chiedere |

## 4. Cosa serve per usarle

- FATTO: in Revolution Web le aree CRM e Portale "sono disponibili se risultano attivati i moduli" corrispondenti; gli
  ordini sono un modulo a sé ("Ordini clienti/fornitori").
  [zucchetti.it, AHRW](https://www.zucchetti.it/website/cms/ITA/prodotto/8314-ad-hoc-revolution-web.html)
  DEDUZIONE: anche l'import e gli ordini sono moduli che il cliente può non avere.
- FATTO: nessuna delle pagine consultate (Zucchetti, Datalite, Altaquota) riporta prezzi o condizioni di licenza.
- DEDUZIONE: con prodotti venduti tramite partner, accesso ai tracciati, al database o ai servizi web passa dal
  rivenditore. Un accesso diretto non concordato può creare problemi di assistenza e di aggiornamento.

## 5. Concetti che si sovrappongono al nostro glossario

| Nostro termine | Ad Hoc Revolution / ARS Logistica | Nota |
|---|---|---|
| Articolo | "Articoli (e servizi)", anagrafica articoli ([AHRW](https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-in-cloud/ad-hoc-revolution-web/software-gestionale-cloud-funzionalita.html)) | In Ad Hoc un articolo può essere un servizio: va filtrato |
| Ordine cliente / ordine fornitore | Modulo "Ordini clienti/fornitori" | Stesso concetto |
| Evaso | "Evadibili" (Ad Hoc); "evasione degli ordini" e lista di prelievo che "produce [...] ddt o documento intermedio" (ARS) | IPOTESI: in Ad Hoc "evadere" = generare il documento successivo all'ordine. Può corrispondere al nostro "evaso" (documento intermedio) o al nostro "spedito" (DDT). Da verificare |
| Giacenza | "Giacenze" in entrambi | Ad Hoc gestisce più magazzini, "fisici o logici" |
| Ubicazione | "Ubicazioni" in entrambi | Ad Hoc la tratta come una dimensione accanto a lotti, unità logistiche e matricole |
| Movimento | "Movimenti di magazzino", "documenti" (DDT, documenti interni, documenti di carico) | DEDUZIONE: per Ad Hoc un movimento nasce da un documento con una causale. "Restituire i movimenti" vorrà dire probabilmente creare documenti |
| Rettifica | "Rettifiche inventariali", "rilevazioni inventariali" | Stesso concetto |
| Ricevimento | "Logistica ingresso", "documenti di carico" (ARS) | ARS lo fa già su telefono |
| (fuori dalla base) | Lotti, matricole, unità logistiche | Corrispondono alle estensioni previste dalla decisione 17 |
| Giacenza «VEND» (decisione 15) | Magazzino "logico" di Ad Hoc | IPOTESI: VEND potrebbe corrispondere a un magazzino logico. Da chiedere |

## 6. Conseguenze per la base e i punti di estensione (ticket 02 e 11)

Tutte DEDUZIONI, da confermare con le risposte del rivenditore.

- Il collegamento ad Ad Hoc Revolution sta in un **connettore** fuori dal cuore della base: non c'è un'interfaccia
  pubblica stabile da trattare come standard, e la via concreta (file, database o servizi web) si saprà solo dal
  rivenditore.
- Il contratto del connettore deve permettere sia di **leggere a intervalli** (le fonti non parlano di notifiche
  automatiche verso l'esterno) sia di **scrivere il risultato** come documento con causale, non solo come movimento.
- La base dovrebbe avere uno **scambio a file** (CSV o simile) per articoli, ordini e movimenti. Serve come via di
  riserva per qualunque gestionale e come primo passo se Ad Hoc ha solo l'import da file.
- Ogni dato importato deve conservare il **codice del sistema d'origine** (codice articolo, numero e riga d'ordine) per
  evitare doppioni e per restituire i movimenti alla riga giusta.
- Servono **tabelle di corrispondenza** configurabili per connettore: magazzini e magazzini logici, causali, stati
  dell'ordine ("evaso" e "spedito" contro i documenti di Ad Hoc).
- Quando la base affianca un gestionale, chi comanda su articoli e ordini è il gestionale. La base non dovrebbe
  modificarli, o dovrebbe segnalare le differenze.
- Con **ARS Logistica** presente, prima di progettare il connettore va deciso con l'utente quale programma registra
  ricevimento, prelievo e inventario in quel magazzino. Se lo fanno entrambi, la stessa merce entra due volte in Ad Hoc.
  IPOTESI: il nostro prodotto si collega solo ad Ad Hoc e prende il posto di alcune funzioni di ARS; in alternativa
  ARS resta per prelievo e spedizione e il nostro prodotto copre ricevimento e identificazione.

## 7. Cosa chiedere al rivenditore

Le fonti pubbliche non bastano. Domande da fare al rivenditore di Ad Hoc Revolution e a Datalite (forse sono la stessa
azienda).

1. Quale prodotto e quale versione sono installati: Ad Hoc Revolution client/server o Revolution Web? Su quale database
   e versione (SQL Server?), in sede o nel datacenter Zucchetti?
2. Quali moduli sono attivi: Magazzino, Ordini clienti/fornitori, ubicazioni, lotti e matricole, import dati?
3. Esiste un import/export documentato (tracciati) per articoli, ordini cliente, ordini fornitore e documenti di
   magazzino? È un modulo a pagamento? Quanto costa?
4. Revolution Web, o la vostra installazione, espone servizi web? C'è documentazione? Serve una licenza?
5. È consentito leggere il database con un utente in sola lettura, magari con viste dedicate? E scrivere? Cosa
   cambia per assistenza e aggiornamenti?
6. Come si rappresentano "merce prelevata e pronta" e "merce uscita" in Ad Hoc: documento intermedio, DDT, altro?
   Quali causali si usano per carico, prelievo e rettifica? Esistono magazzini logici?
7. ARS Logistica: quali moduli sono attivi in questo magazzino? Come scrive in Ad Hoc (database, procedure di Ad Hoc,
   tabelle intermedie)? Ha un'interfaccia per programmi di terzi? Quanto costa svilupparla?
8. Cosa fa oggi ARS in questo magazzino e cosa dovrà fare dopo l'arrivo del nostro prodotto?
9. Si può avere un ambiente di prova (una ditta o una copia di test, senza dati reali dei clienti) per sviluppare il
   collegamento?
10. Che cos'è "NEX Logistica"? Sostituisce ARS Logistica?

## Fonti

Zucchetti (produttore di Ad Hoc Revolution)
- https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-descrizione.html
- https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-client-server/ad-hoc-revolution/software-gestionale-piccole-medie-imprese-funzionalit.html
- https://www.zucchetti.it/website/cms/ITA/prodotto/8314-ad-hoc-revolution-web.html
- https://www.zucchetti.it/it/cms/soluzioni/software-gestionali/tecnologia/gestionali-in-cloud/ad-hoc-revolution-web/software-gestionale-cloud-funzionalita.html
- https://www.zucchetti.it/website/dms/website/prodotti/sw/Gestionali/brochure/AHR_Software_gestionale.pdf (DAHR 5.1, 10/2018)
- https://zucchetti.it/it/dms/zucchetti-it/aziende/gestionali/ad-hoc-revolution-web/brochure/Brochure_AHRW.pdf (DAHRW 1.0, 07/2020)
- https://zucchetti.it/website/dms/website/prodotti/sw/Tool%20sviluppo/strumenti_sviluppo.pdf (Sitepainter Infinity, 2014)
- https://digitalsupplychain.zucchetti.it/web/cms/ENG/digital-supply-chain.html

Datalite e Altaquota (produttore di ARS Logistica)
- https://datalite.it/soluzioni-software/suite-ars/ars-logistica/
- https://datalite.it/soluzioni-software/suite-ars/
- https://datalite.it/wp-content/uploads/2024/07/Brochure_ArsLogistica_v4.pdf
- https://datalite.it/blog/arslogistica-il-software-per-la-digital-transformation-del-tuo-magazzino/ (06/06/2023)
- https://datalite.it/chi-siamo/datalite-la-nostra-storia/
- https://datalite.it/soluzioni-software/software-zucchetti/ad-hoc-revolution/
- https://www.aquota.net/prodotti/ars-logistica/

Altre
- https://www.modula.eu/it/
- https://www.arsinform.it/portfolio-articoli/controllo-e-gestione-di-magazzini-automatici/
- https://thesis.unipd.it/retrieve/c2defdcf-9610-416c-bb36-017830fbb8eb/Fichera_Jacopo%20%281%29.pdf (fonte secondaria, 2022)
