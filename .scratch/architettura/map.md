# Mappa: architettura della base generica

Etichetta: wayfinder:map

## Destination

`docs/architettura.md` (specifica della base generica) e `GLOSSARY.md` alla radice, pronti per pianificare la
costruzione. Coprono: modello dei dati e glossario; regole di ricevimento e di assegnazione; percorso di
identificazione barcode → codice stampato → immagine, con lettura della quantità; inserimento di un articolo nuovo da
foto; divisione tra telefono, computer e server in sede; app nativa o web app; punti di estensione per la
specializzazione; piano, esecuzione e risultati della prova di accuratezza visiva, con la scelta del modello; stack;
percorso delle schermate e aspetto grafico, compresi nome e brand kit (decisioni 11–14 e 20).

## Notes

- Lingua: italiano. Domande all'utente in parole semplici: cosa si chiede, perché conta, cosa comporta ogni opzione.
- Leggere prima `AGENTS.md`, poi `docs/decisioni.md` (decisioni prese, da non rimettere in discussione) e
  `docs/analisi-progetto.md`. Le ricerche in `docs/research/` si consultano quando servono, senza ripeterle.
- Ogni decisione dell'utente va in `docs/decisioni.md`, con data e motivo («non indicato» se non è stato detto). Nei
  ticket e nella mappa si rimanda al numero, senza ripetere il testo.
- Chi risolve un ticket scrive la sua parte in `docs/architettura.md` e i termini chiariti in `GLOSSARY.md`
  (skill domain-modeling: niente dettagli tecnici nel glossario).
- Le ricerche vanno in `docs/research/`, un file per tema con data e link alle fonti primarie (`AGENTS.md`; prevale
  sul ramo usa e getta proposto dalla skill wayfinder).
- Skill da usare: grilling e domain-modeling per i ticket di conversazione; research per le ricerche; prototype per
  i prototipi; ponytail (lite per prototipi, full per la specifica); per le schermate ux-strategy, ux-writing,
  mobile-native, accessibility-audit (obiettivo WCAG 2.2 AA), emil-design-eng.
- La decisione 12 porta l'esecuzione dentro la mappa: la prova visiva è un ticket di tipo task, con le foto reali
  fornite dall'utente. Prima di raccoglierle, chiedere all'utente dove conservarle e se possono stare nel repository.
- Le decisioni 13 (stack) e 14 (grafica) sono le ultime della mappa: dipendono da app nativa o web, rete assente
  (decisione 23) e divisione tra le macchine. Dal 20/11/2026 non aspettano più la prova visiva (405): ciò che dipende
  dai suoi numeri sta nel ticket «Impronte e server in sede, dopo la prova». Le scelte di aspetto sono di gusto, spettano
  all'utente e si fanno con prototipi da guardare. Una sola direzione visiva, registrata in `docs/decisioni.md`.
- Anche nome e brand kit sono scelte di gusto dell'utente (decisione 20). La skill logo-design si installa nel
  progetto, in `.claude/skills` e `.agents/skills` uguali, dopo averne letto il contenuto; mai a livello globale.
- Due magazzini reali fanno da banco di prova per la base, senza diventarne la specializzazione: UFP affianca due
  gestionali esistenti (Ad Hoc Revolution e ARS Logistica) e usa il carico normale e anche VEND, con ordini fornitore
  che portano il riferimento del cliente; l'altro usa solo Shopify e userà VEND con il riferimento preso dagli ordini del sito (decisioni 15, 19, 42 e 46).

## Decisions so far

<!-- una riga per ticket chiuso: [titolo](issues/NN-slug.md): sintesi della risposta -->

- [Regole all'arrivo: carico normale e merce venduta (VEND)](issues/01-regole-arrivo-carico-e-vend.md): si parte
  dal DDT; tre strade (VEND se l'ordine fornitore porta il riferimento cliente, carico normale, merce non prevista);
  VEND vince su «dal più vecchio», esce al prelievo, posti numerati facoltativi; acceso per magazzino (decisioni 30–48).
- [Shopify: ordini, evasione e giacenze viste da un gestionale esterno](issues/03-ricerca-shopify.md): API GraphQL
  da aggiornare ogni anno; assegnazione e «evaso» restano nostri; niente webhook verso un server in sede, si
  interroga Shopify a intervalli; connettore come modulo dietro un punto di estensione «canale di vendita».
- [Ad Hoc Revolution e ARS Logistica: come si scambiano i dati](issues/18-ricerca-adhoc-revolution-ars-logistica.md):
  nessuna interfaccia pubblica, tutto passa dal rivenditore; ARS fa già ricevimento e prelievo da telefono, quindi
  va decisa la divisione del lavoro; scambio a file come via generale.
- [Fonti degli ordini e collegamento ai gestionali esistenti](issues/02-fonti-ordini-e-collegamenti.md): comanda il
  sistema d'origine; in UFP il programma sostituisce ARS e restituisce documenti ad Ad Hoc; scambio a file nella base,
  Shopify modulo, Ad Hoc nella specializzazione; banco dal telefono; scambio ogni 5 minuti con coda (decisioni 49–67).
- [Modello dei dati](issues/04-modello-dei-dati.md): ricevimento in un passaggio dal telefono, area di ricevimento,
  correzioni senza cancellare, mai sotto zero, assegnazione per quantità, unità e codici del fornitore approvati dal
  responsabile, prezzi accesi per magazzino; entità in `docs/architettura.md` (decisioni 68–86).
- [Percorso di identificazione e lettura della quantità](issues/05-percorso-identificazione-e-quantita.md):
  un'inquadratura sola, prima gli articoli attesi poi il catalogo; codice stampato con i segni che si confondono;
  barcode multipli o sconosciuti; quantità solo da GS1 o parole di quantità, colli e contenuto ricordato; foto di
  riferimento filtrate; stesso percorso al prelievo come controllo; soglie dopo la prova (decisioni 87–104).
- [Inserimento di un articolo nuovo da foto](issues/06-articolo-nuovo-da-foto.md): lo crea anche l'operatore, «da
  confermare» e usabile subito; tre foto guidate; righe attese senza articolo in cima (VEND compreso); «È uno di
  questi?» e unione dei doppioni; il responsabile conferma, unisce o rifiuta; riga ferma e collegamento per codice con
  un gestionale; «Aggiungi foto» su ogni articolo (decisioni 105–118).
- [App nativa o web app](issues/07-app-nativa-o-web.md): web app dal browser su telefoni, palmari e computer, servita
  dal server in sede (accesso solo dalla rete interna); palmari con grilletto e telefoni personali compresi;
  certificato del dominio aziendale o interno; iPhone da Safari; aggiornamenti del responsabile, obbligatori di notte;
  prove su dispositivi veri (decisioni 119–127).
- [Piano della prova di accuratezza visiva](issues/08-piano-prova-visiva.md): foto in un repository privato, nel
  pubblico solo numeri anonimi; UFP, 200 articoli a caso più 40 fuori catalogo e 300 di contorno; 3 + 3 foto dalla
  pagina di scatto nel browser; SigLIP 2, PE-Core, DINOv2 (DINOv3 solo confronto); traguardo 95 su 100 tra le 5
  proposte con 100 attesi; tempi solo nella sessione (decisioni 128–145; modelli aggiornati dalla 146).
- [Modelli visivi open source recenti: ce ne sono di migliori?](issues/19-ricerca-modelli-visivi-recenti.md): nessun
  modello recente con licenza commerciale batte SigLIP 2 e PE-Core sui prodotti; TIPSv2 e C-RADIO senza risultati
  diretti; il ritaglio automatico dell'oggetto vale più di un modello nuovo. Esito: TIPSv2 media al posto di DINOv2
  grande, si misura anche il ritaglio, C-RADIO fuori (decisioni 146–148).
- [Percorso delle schermate](issues/16-percorso-delle-schermate.md): prima schermata per mansione (magazziniere,
  preparatore) con «Altri lavori»; DDT con inquadratura in alto e righe sotto; piani di spedizione o coda «Prossimo
  ordine»; permessi per pianificare e spedire; «spedito» al ritiro del corriere; vendita assistita al posto del banco;
  prototipo a fil di ferro (decisioni 160–179).
- [Gestionali di magazzino esistenti: funzioni in più e difetti da evitare](issues/20-ricerca-gestionali-esistenti.md):
  tutti ricevono contro ordine e la 183 coincide con i PMI più completi; nessuno legge in modo affidabile le righe di un
  DDT cartaceo; mancano alla base elenchi in sospeso, «Documenti», regola Annulla/Conferma, merce danneggiata, resi,
  inventario, etichette del corriere, requisito di velocità (ricerca del 18/11/2026).
- [Completezza del percorso delle schermate](issues/21-completezza-percorso-schermate.md): DDT con foto della bolla e
  righe dalle letture, ripiego a mano con ordine proposto, quantità in bolla alla chiusura; cose in sospeso in quattro
  gruppi; «Documenti» e registro; regola Annulla/Conferma; merce danneggiata; tempi 1–2 s; nuovi ticket Resi,
  Inventario periodico e Lettura automatica delle bolle (decisioni 184–201).
- [Lettura automatica delle bolle](issues/24-ricerca-lettura-bolle.md): in parte sì; testata leggibile in sede, righe da
  misurare su bolle vere; codici stampati (DataMatrix, EAN per riga) letti senza OCR; esclusi i modelli a licenza non
  commerciale. Prova accettata: bolle nel privato, clienti coperti, 100–120 bolle, sistemi A–D, accesa per fornitore
  (decisioni 202–206).
- [Resi](issues/22-resi.md): «Da rendere» e area resi; reso al fornitore in cinque stati con richiesta e segnalazione
  delle differenze preparate dal programma e mandate dal responsabile; reso del cliente dall'ordine spedito con
  Integro / Da controllare / Danneggiato, esiti su Shopify, documento al gestionale; collo rovinato con riserva;
  scheda «Dalla bolla» e «Manca l'ordine» per il carico a mano (decisioni 207–226).
- [Inventario periodico](issues/23-inventario-periodico.md): un solo lavoro «Inventario» del responsabile (tutto = solo
  scaffali, ubicazioni, articoli, fornitore); conta cieca e seconda conta, di serie e per inventario; una persona per
  ubicazione con «in conta da…» e lavoro che continua; differenze valide all'approvazione, poi rettifiche o variazioni;
  «Conta un'ubicazione» con le stesse regole, valida subito (decisioni 227–245).
- [Elenco del prelievo e correzione della quantità](issues/26-elenco-del-prelievo.md): l'ordine si apre sull'elenco con
  «Prelievo guidato» e «Sospendi»; si entra nell'articolo per giacenza e quantità; «Correggi giacenza», «Prosegui»,
  «Restano aperti», conferma della quantità diversa, tastierino del programma; il resto lo segue il responsabile dei
  piani in «Da completare»; responsabili soprattutto dal computer (decisioni 270–299).
- [Punti di estensione per la specializzazione](issues/11-punti-di-estensione.md): base unica con Configurazione e
  moduli solo nostri; punti d'aggancio collegamento, lettore di etichette, precedenza, partita; «Da registrare nel
  gestionale»; aggiornamento fermo se un modulo non va; vendita assistita, agenti, fattura, ordini fornitore e
  inventario verso Ad Hoc; «collegamento» al posto di «connettore» (decisioni 301–320).
- [Shopify: resi, rimborsi e cosa si può collegare](issues/27-ricerca-shopify-resi-e-collegamenti.md): resi, esiti,
  etichetta propria e rimborso (anche in credito) si fanno da API a intervalli; no etichette di reso Shopify in Italia,
  scelta del rimborso del cliente solo con un'estensione, niente WhatsApp in arrivo senza indirizzo pubblico; rimborso
  entro 14 giorni dalla richiesta, credito solo con accordo espresso (ricerca del 19/11/2026).
- [Resi del cliente nel magazzino Shopify](issues/28-resi-cliente-magazzino-shopify.md): resi di Shopify nel
  collegamento, senza app; modulo nostro nella pagina dell'ordine con la scelta del rimborso e l'indirizzo del ritiro;
  mail dei resi lette dal programma, modello solo dopo una prova; il responsabile approva, prenota il ritiro GLS o
  carica l'etichetta FedEx e conferma il rimborso; 14 giorni contati; tre punti per la parte legale (decisioni 322–343).
- [Nome del prodotto](issues/12-nome-del-prodotto.md): marchio vero, uguale in italiano e in inglese, veloce e
  ordinato, parola modificata fino a 5 lettere; Kiln solo per lo stile; preferiti in ordine Kurso, Varko, Velko, da
  verificare; se nessuno è libero si riprende dai nomi in dubbio (decisioni 344–357).
- [Unicità dei nomi scelti](issues/13-unicita-dei-nomi.md): Kurso bloccato da un marchio tedesco per software, Velko
  vicino a Velco; nome scelto **Varko** (omofoni «Varco» da valutare); consulente in marchi prima del deposito e
  dell'offerta ad altri; domini tutti presi, nessuna azione (decisioni 358–361). Varko poi accantonato e in riserva: il
  nome nasce dalla lettera del logo (375, 376).

Prese prima della mappa, nel secondo giro di domande del 15/11/2026: decisioni 15–28 in
[`docs/decisioni.md`](../../docs/decisioni.md) (assegnazione parziale, codice stampato come tipo di articolo,
35.000 articoli, base principale o affiancata, prelievo e spedizione, Android e iPhone, niente lavoro senza rete,
tre livelli di conferma, quantità letta dalla scatola, ubicazioni facoltative, due ruoli, testi separati).

- [Verifica dei nomi in R nei registri dei marchi](issues/29-verifica-nomi-in-r.md): risultati UIBM riportati
  dall'utente; nome per ora **Ripo**, che può cambiare senza toccare il logo R; ricerca europea al consulente (386–387).
- [Brand kit con la skill logo-design](issues/14-brand-kit.md): R · Pulito costruito, asta 44, R apposta per i 16
  pixel; blu elettrico #1F5BFF e #668FFF sul tema scuro; icona R bianca su blu; simbolo e nome separati; kit in
  `brand/` con guida e tavola d'uso; prova di stampa rimandata (decisioni 362–404).

## Not yet specified

- **Adattamento del modello visivo** (metric learning) sulle foto del magazzino: solo se i numeri della prova lo
  giustificano.
- **Installazione e configurazione iniziale in un magazzino nuovo:** procedura guidata (dove si sceglie se usare le
  ubicazioni, decisione 26, e dominio o certificato interno, 123), rinnovo del certificato, aggiornamenti (chi segna
  quelli obbligatori, ritorno alla versione precedente se il programma non riparte, 125), copie di sicurezza e
  ripristino.
- **Catalogo visivo per la vendita assistita** (idea dell'utente, decisioni 78 e 86; «banco» diventa «vendita assistita», 178): cercare un articolo e vederne
  disponibilità, prezzo, giacenza e ubicazione, anche quando il cliente non sa bene cosa vuole. Tocca identificazione e
  schermate.
- **Etichette e distinta del corriere:** chi le stampa in UFP (domande 21 e 22 al rivenditore) e nel magazzino Shopify;
  la ricerca del 18/11/2026 le trova in quasi tutti i gestionali. Se serviranno, diventano un collegamento in più (decisione 303).
  Nel magazzino Shopify vale anche per i resi: oggi ritiri GLS prenotati a mano e etichette FedEx caricate (326, 331).
- **Prova della lettura delle mail dei resi:** dove conservare le mail vere con i dati coperti, quante, come si misura
  la bozza del modello, in cloud o in sede (333). La domanda è stata saltata (340): finché non si decide, il modello
  resta spento.
- **Ottimizzazione del venduto (VEND):** l'utente vuole un'analisi a parte, soprattutto per UFP, che vende anche al
  banco e ha più casi particolari da controllare.
- **Descrizione proposta da un modello che legge immagini e scrive testo** per l'articolo nuovo: se tenerla, e quale
  modello, dipende dalla prova e dal server. Oggi la scrive l'operatore con le parole lette sull'etichetta (108).
- **Cambio del nome provvisorio DondEres:** dove compare (repository, documenti, pagine) e quando sostituirlo con il
  nome definitivo (in R, 379–383; per ora Ripo, 386); il brand kit è chiuso (404), quindi si decide con lo stack.
- **Prova di stampa del marchio** su una stampante termica vera, con `brand/prova-stampa.svg` (403): conferma o
  corregge le misure minime della guida (5 mm il simbolo, 15 mm il nome). Si fa quando c'è la stampante.

## Out of scope

- Specializzazione per un magazzino specifico (decisione 4).
- Collegamento Ad Hoc Revolution per UFP: sta nella specializzazione, dopo le risposte del rivenditore (decisioni 51 e
  57; domande in `docs/domande-rivenditore-ufp.md`).
- Registrazione per numero seriale del singolo pezzo, lotti e scadenze: possibile estensione (decisione 17).
- Lavoro senza rete (decisione 23).
- Conteggio dei pezzi dall'immagine (decisione 25).
- Più magazzini nella stessa installazione (decisione 26).
- Magazzini senza un server in sede: altre soluzioni da studiare dopo, come iniziativa a parte (decisione 126).
