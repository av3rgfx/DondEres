# Unicità dei nomi del prodotto: marchi, domini, prodotti simili

Data: 20/11/2026

Legenda: **FATTO** = visto in un registro o su una pagina aperta il 20/11/2026 (link accanto). **DEDUZIONE** =
conclusione nostra a partire dai fatti. **IPOTESI** = da verificare. **Non verificato** = registro o pagina non
raggiungibile dal container, oppure dato letto solo in modo indiretto (es. DNS invece del whois).

**Non è un parere legale.** Questa è una ricerca preliminare fatta con le banche dati pubbliche gratuite. La
valutazione del rischio di confusione tra marchi (somiglianza dei segni e dei prodotti, notorietà, uso effettivo)
spetta a un consulente in marchi. Una ricerca di anteriorità professionale costa e copre più registri (registri
nazionali completi, ragioni sociali, nomi non registrati, ricerca fonetica e figurativa).

Ticket di riferimento: «Unicità dei nomi scelti» (vedi `docs/architettura.md`, sezione «Nome del prodotto»,
decisioni 344–357).

## Domanda

Per i tre preferiti (1. Kurso, 2. Varko, 3. Velko) e per la riserva (Trako, Sorto, Rigo, Movo, Venko, Arvo, Volko;
possibile riserva aggiuntiva Vekto, Kardo, Rivo, Dokra):

1. ci sono marchi vivi (registrati o in domanda) identici o molto simili nelle classi di Nizza 9 (software), 35
   (gestione commerciale, servizi d'ufficio), 39 (trasporto, magazzinaggio), 42 (SaaS, sviluppo software), validi in
   UE o in Italia?
2. i domini `.com`, `.it`, `.eu` (per i preferiti anche `.io` e `.app`) sono già registrati, e cosa c'è sopra?
3. esistono prodotti con quel nome nel software, nella logistica, nei gestionali?

## Metodo

Tutte le interrogazioni sono del 20/11/2026.

**Marchi.**

- **TMview** (https://www.tmdn.org/tmview/), che raccoglie EUIPO (marchi UE), UIBM (Italia), WIPO Madrid (WO) e
  molti uffici nazionali. Il sito blocca i client automatici: le ricerche sono state fatte con un browser
  automatizzato (Playwright) che chiama la stessa API del sito (`/tmview/api/search/results`), con questi filtri:
  uffici EM, IT, WO; classi 9, 35, 39, 42; stato «Filed» e «Registered» (cioè vivi). Tre modalità:
  - «Is» (identico) per ogni nome e per le varianti con C al posto di K (Curso, Corso, Kursor, Varco, Velco,
    Traco, Venco, Volco, Vecto, Cardo, Docra);
  - «Contains» (contiene) e «Fuzzy» (ricerca approssimata di TMview) per gli stessi nomi;
  - «Is» su **tutti gli uffici** (filtro classi e stato uguale), per vedere i marchi nazionali dei paesi UE
    (Germania, Francia, Benelux, Polonia…) e di paesi extra UE.
  Sui risultati approssimati abbiamo tenuto quelli con distanza di una lettera o identici «a orecchio» (C=K, W=V,
  Y=I). Per i marchi più rilevanti abbiamo letto la scheda completa (prodotti e servizi) dall'API di dettaglio.
- **WIPO Global Brand Database** (https://branddb.wipo.int/en/similarname): ricerca per nome con la strategia
  predefinita della pagina («Embedded», risultati che contengono il termine), senza filtri, per ogni nome. Copre
  anche registri nazionali che TMview non ha (es. Brasile, India, Indonesia); in questa banca dati non abbiamo visto
  i marchi UE (EM) comparire direttamente, per quelli vale TMview.
- **DPMA** (registro tedesco), aperto direttamente per il marchio KURSO tedesco.
- **Non raggiungibili dal container**: euipo.europa.eu (eSearch) e uibm.gov.it / uibm.mise.gov.it non hanno
  risposto; i dati EUIPO e UIBM qui riportati vengono da TMview (TMview segnala per EUIPO l'aggiornamento del
  19/11/2026). INPI (Francia, data.inpi.fr) ha bloccato l'accesso: i marchi francesi sono letti da TMview.

Per ripetere a mano: aprire https://www.tmdn.org/tmview/, scrivere il nome, scegliere «Is» (o «Fuzzy search»),
poi nei filtri: uffici EM, IT, WO (o nessuno), classi 9, 35, 39, 42, stato Filed e Registered. Ogni scheda si apre
anche da `https://www.tmdn.org/tmview/#/tmview/detail/<ST13>` (ST13 riportato sotto; formato del link non
verificato perché a fine giornata TMview rifiutava le richieste del container). Per WIPO: https://branddb.wipo.int/en/similarname, campo «Brand name».

**Domini.** RDAP (https://rdap.org e, per `.io`, https://rdap.identitydigital.services) per `.com`, `.app`, `.io`:
registrato sì/no e data di creazione. Per `.it` il registro (RDAP di nic.it) non era raggiungibile e il web whois
di nic.it chiede un reCAPTCHA; per `.it` e `.eu` abbiamo usato il DNS (Google e Cloudflare DNS‑over‑HTTPS): se il
dominio ha server dei nomi è registrato (FATTO); se il registro risponde «NXDOMAIN» è **probabilmente libero**, ma
un dominio `.it` può essere registrato e non attivo nel DNS, quindi va confermato sul whois di nic.it (non
verificato). Abbiamo aperto la home dei domini registrati.

**Prodotti.** Ricerca web, App Store (API pubblica di ricerca di Apple, negozio italiano e statunitense), GitHub
(ricerca repository per nome), siti dei domini. Product Hunt non è stato consultato.

## Sintesi

Il giudizio è una **DEDUZIONE** nostra, in tre livelli: «sembra libero», «ostacoli da valutare», «ostacolo forte».
«Identici» = stesso nome (anche con grafica) in classe 9/35/39/42, vivo, valido in UE o in Italia (EUIPO, UIBM,
Madrid con designazione UE/IT, oppure un registro nazionale di un paese UE).

| Nome | Identici vivi 9/35/39/42 in UE/IT | Simili rilevanti | .com / .it / .eu | Prodotti con quel nome | Giudizio (DEDUZIONE) |
|---|---|---|---|---|---|
| **Kurso** | **1**: KURSO (DE), software e SaaS, in uso (kurso.de); più Kurso (FR) in 35 | CURSOR (Anysphere, 9/42), kruso (42), KURO (9/35/42), Kursolino, KURSOHEY | preso / probabilmente libero / preso | kurso.de (gestione corsi online, DE), kurso.app (siti per centri di formazione) | **ostacolo forte** |
| **Varko** | **0** (unico VARKO UE: FR, classe 9 ma paradenti da boxe) | VARCO (EM, strumenti di perforazione, 7/9), LOG. VARCO (IT, 35/39, concessionaria), VARCO (IT, domanda 2026, 42) | preso / preso / preso | app fitness (varko.app), strumento SEO (varko.io); nulla nella logistica | **ostacoli da valutare** (i più bassi dei tre) |
| **Velko** | **1**: Velko (EM, figurativo, classe 9: batterie e caricatori) | VELCO (FR, 9/39/42, software di geolocalizzazione e flotte, in uso), VELCO (IT, 35/42), DELKO, VELMO | preso / preso / preso (in vendita) | velko.io (IA per il contatto clienti, NL), velko.app (app MCP), app IPTV | **ostacoli da valutare** (alti) |
| Trako | 2: TRAKO (EM, domanda, 35/41, fiere) e TRAKO (PL, 35), stesso titolare; TRAKO (BG, 7/12/35) | TRACO (IT, 39), TRACO (WO, 9), TRAKO (CH, 42 SaaS, fuori UE) | preso / probabilmente libero / preso | app «Trako» (Business), Trako GPS | ostacoli da valutare |
| Sorto | 0 | Forto (WO con designazione UE, 9/39/42, logistica digitale), KORTO (9/42); SORTO (UK, 42, fuori UE) | preso / preso / preso | app «Sorto» (Lifestyle) | ostacoli da valutare |
| Rigo | 5 (EM, WO, IT: 35, 42…) | DE RIGO (9/35), BRIGO (35/39/42) | preso / preso / preso | RigoHR e altre app | ostacolo forte |
| Movo | 10 (EM, IT, WO), tra cui MOVO (EM, domanda 2026, 9/35/39/42, SaaS parcheggi) | MOVO (JP, 39/42, logistica, fuori UE) | preso / preso / preso (in vendita) | molte app «Movo» (mobilità, consegne) | ostacolo forte |
| Venko | 5 (EM, WO), tra cui VENKO (EM, 9/35/42) | WENKO (35), venko (WO, 42) | preso / preso / preso | app «Venko Practice» | ostacolo forte |
| Arvo | 3 in EM/WO, altri nazionali (DE 9…) | AIRVO, ARAVO (42) | preso / preso / preso | app «Arvo» (fitness, assistente IA) | ostacolo forte |
| Volko | **0** | WOLCO (EM, 42: controllo qualità di utensili da taglio), VALCO, VELCO | preso / probabilmente libero / preso | nessuno trovato nel settore | **sembra libero** |
| Vekto | 1: Vekto (BX, domanda 16/10/2026, 9/35/42, servizi IT) | VECTO (EM, 7/9) | preso / preso / preso | app «VEKTO» (to‑do) | ostacolo forte |
| Kardo | 2: Kardo (EM, 35/42, **gestione scorte, ERP, supply chain**), KARDO (DE, 9/35/41) | CARDO (EM, 9) | preso / preso / preso (in vendita) | app Kardo POS / HR (gestionali) | ostacolo forte |
| Rivo | 6 (EM, WO), tra cui RIVO (EM, 42, SaaS per la finanza del commercio) | Arivo (9/39/42), RIVOS | preso / preso / preso (in vendita) | molte app «Rivo» | ostacolo forte |
| Dokra | 1: DOKRA (CZ, domanda 06/10/2026, 9/35/42, software e SaaS) | DEKRA (EM, molte classi) | preso / probabilmente libero / preso | nessuno nel settore | ostacolo forte |

In breve (DEDUZIONE): dei tre preferiti **Varko** è quello con meno ostacoli; **Kurso** ha un marchio identico per
software in uso in Germania; **Velko** ha un omofono forte (Velco) nel software in Francia e in Italia. Nella
riserva solo **Volko** sembra libero nei registri consultati; **Sorto** e **Trako** hanno ostacoli da valutare;
gli altri hanno marchi identici nelle classi del prodotto. Nessun `.com` è libero.

## Kurso

### Marchi

- Identici in EM/IT/WO, classi 9/35/39/42, vivi: **nessuno** (TMview «Is», 20/11/2026). Anche «Curso» e «Kursor»
  identici: nessuno. (FATTO)
- **KURSO**, Germania, n. 302017231600, marchio denominativo, titolare **Henke Informatik GmbH** (Stoccarda),
  classe 9 «Computer-Software; Software für Lehrer», classe 42 SaaS, sviluppo e noleggio di software; registrato il
  27/10/2017, senza opposizioni, protezione fino al 31/10/2027 (rinnovabile). (FATTO,
  [DPMAregister](https://register.dpma.de/DPMAregister/marke/register/3020172316000/DE); in TMview ST13
  DE503020172316000). Il marchio è usato: https://www.kurso.de è «Die Online-Kursverwaltung – für Kurse und
  Seminare – KURSO, Henke Informatik GmbH». (FATTO)
- **Kurso**, Francia, n. 4973718, denominativo, titolare una persona fisica «per conto di Kurso», classi 35
  (gestione degli affari commerciali, consulenza di organizzazione e direzione…) e 41, registrato (deposito
  30/06/2023). (FATTO, da TMview, ST13 FR500000004973718; la scheda INPI https://data.inpi.fr/marques/FR4973718
  non si è aperta dal container)
- Simili trovati (FATTO, TMview):
  - CURSOR, EM 019211546, Anysphere, Inc., classi 9 e 42 (software con IA per scrivere codice), registrato;
    CURSOR, EM 018998105 (9/41/42) e EM 019363918 (9), Cursor Software AG; CURSOR, IT 1998900653102, Iveco (7/9/12).
  - kruso, EM 016147316, Kruso A/S, classe 42 (progettazione e programmazione, consulenza IT), registrato fino al
    2036.
  - KURO, EM 018920087, MYDIGIT, 9/35/42 (software e servizi informatici); altri KURO in classe 9 (EM e IT).
  - Kursolino, EM 018568761, Kutego GmbH, 9/35/41/42; KURSOHEY, EM 018962777, classe 9.
  - CORSO, EM 010951556, titolare «CORSO 1», 9/42/43; CORSO, EM 008997462, Verlagshaus Römerweg, 9/16/38/41.
- DEDUZIONE: KURSO tedesco è lo stesso nome, per software e SaaS, in uso in un paese UE. Un marchio UE «Kurso» per
  un gestionale rischierebbe l'opposizione di quel titolare, e l'uso in Germania sarebbe esposto. In più «Kurso»
  letto all'inglese si avvicina a «Cursor», nome noto nel software (somiglianza fonetica da valutare).

### Domini

| Dominio | Registrato | Creato | Cosa c'è |
|---|---|---|---|
| kurso.com | sì | 01/11/2005 | pagina di parcheggio di Hostinger |
| kurso.it | probabilmente no (NXDOMAIN) | – | non verificato sul whois di nic.it |
| kurso.eu | sì (DNS) | non letto | «Kursy i szkolenia UDT» – corsi in Polonia, tra cui carrellisti e gruisti |
| kurso.io | sì | 09/11/2017 | il sito risponde 503 |
| kurso.app | sì | 16/08/2026 | «Kurso – votre site de formation»: siti web per centri di formazione (Marocco) |

### Prodotti

- kurso.de: software online di gestione corsi (Germania). kurso.app: siti per centri di formazione. (FATTO)
- App Store: «Kurso: Currency Converter» (Finance), «Kurso: Antidepressant Tracker» (Medical). (FATTO,
  [1](https://apps.apple.com/it/app/kurso-convertitore-valute/id6765615636),
  [2](https://apps.apple.com/it/app/kurso-antidepressivi-e-umore/id6821469023))
- GitHub: soprattutto corsi di esperanto («kurso» = corso). Nessun prodotto di logistica o magazzino trovato.
  (FATTO per quanto cercato)

## Varko

### Marchi

- Identici in EM/IT/WO, classi 9/35/39/42, vivi: **nessuno** (TMview «Is»). (FATTO)
- Su tutti gli uffici TMview e su WIPO, gli unici VARKO in paesi UE: **VARKO**, Francia, n. 5275053, persona
  fisica, classi 9, 25, 28, registrato (deposito 04/07/2026); in classe 9 solo «protège‑dents, casques protecteurs
  pour la boxe». (FATTO, TMview ST13 FR500000005275053). Fuori UE: VARKÔ (Argentina, 42), VARKO (Cina, 9), domande
  in Indonesia (35 e 9), Brasile e USA (classe 21). (FATTO, TMview e WIPO). Un VARKO tedesco (classe 20) è scaduto
  nel 1992.
- Omofoni «Varco» (FATTO, TMview):
  - VARCO, EM 002739928, Grant Prideco, Inc., classi 7 e 9 (strumentazione elettronica per impianti di
    perforazione, ispezione di tubazioni), registrato fino al 2032; lo stesso titolare ha VARCO in molti paesi.
  - LOG. VARCO (IT 2001900901885) e LOGOTIPO VARCO (IT 2001900901886), Varco Vendita Autoveicoli Ricambi Compagnia
    S.p.A., classi 12, 35 (servizi di concessionari d'auto), 39 (trasporto, noleggio di veicoli). TMview li dà
    «Registered»; sono depositi del 2001, il rinnovo non è verificato.
  - «VARCO: DISEGNIAMO IL CONFINE» (IT 2026000155578) e un marchio figurativo con la parola VARCO
    (IT 2026000155617), One More Step S.r.l., domande del 09/09/2026, classi 6, 19, 37, 42. Prodotti non letti
    (scheda non scaricata: errore 502).
  - WARCO, EM, domanda 2026, classi 6/9/17 (sistemi per fluidi). VARCO, UK 4377803, classe 42 (rilievi
    di edifici; Regno Unito, fuori UE).
- Simili per una lettera, classi 9/35/42 (FATTO, TMview): VARJO (Varjo Technologies, visori, 9/28/42), VARTO
  (Varto AI, WO 1948039, 42, verifica formale del software), VARSKO (Varsko AS, allarmi, 9/42), VERKO (EM
  019353790, agenzia digitale, 35/42), VARK (Siemens, WO, 42), VARO (diversi titolari, 9/42), VAKKO (9/35/42).
- DEDUZIONE: nessun marchio identico per software o gestione in UE. Il rischio più vicino sono i marchi «Varco»:
  pronuncia identica in italiano, ma prodotti lontani (perforazione petrolifera, concessionaria d'auto) o da
  leggere (One More Step, classe 42). «Varco» è anche una parola italiana comune, il che di solito indebolisce i
  marchi che la usano: da far valutare al consulente.

### Domini

| Dominio | Registrato | Creato | Cosa c'è |
|---|---|---|---|
| varko.com | sì | 08/11/2004 | pagina «Squarespace – Website Expired» |
| varko.it | sì (DNS) | non letto | pagina «dominio già registrato» di Aruba |
| varko.eu | sì (DNS, server home.pl) | non letto | il sito non risponde |
| varko.io | sì | 28/03/2026 | strumento SEO in sviluppo (connettore MCP per Claude) |
| varko.app | sì | 14/07/2026 | programma di allenamento in palestra (in francese) |

### Prodotti

- App Store: «Varko», Health & Fitness, Black Octopus SA (FATTO,
  [link](https://apps.apple.com/it/app/varko/id6799035670)); probabilmente è la stessa di varko.app (IPOTESI).
- varko.io: analisi SEO per agenzie. GitHub: progetti minori (un bot Telegram, un progetto universitario).
- Nessun software di logistica, magazzino o gestionale con questo nome trovato. (FATTO per quanto cercato)

## Velko

### Marchi

- Identici in EM/IT/WO, classi 9/35/39/42, vivi: **1**. **Velko**, EM 019038932, marchio **figurativo**, titolare
  una persona fisica con indirizzo negli Emirati Arabi, classi 4 e 9; in classe 9: batterie, batterie per sigarette elettroniche,
  caricabatterie, adattatori, regolatori di luce, rilevatori, pellicole per schermi. Depositato il 10/06/2024,
  registrato il 15/09/2026 (più di due anni dopo il deposito; TMview collega al numero una voce della giurisprudenza EUIPO, non letta), scadenza 10/06/2034.
  (FATTO, TMview ST13 EM500000019038932,
  [EUIPO eSearch](https://euipo.europa.eu/eSearch/#details/trademarks/019038932), non aperto dal container)
- Altri VELKO fuori UE: Messico (9, domanda 2026), Corea (35), Turchia (25/35, Velko Tekstil). (FATTO)
- Omofoni «Velco» (FATTO, TMview):
  - VELCO, FR 4516847, VELCO SAS, classi 9, 12, 36, 39 («repérage, localisation et surveillance de véhicules»), 42
    (sviluppo e manutenzione di applicazioni); VELCO, FR 4299223, Vel'Co SAS (combinato), 9/12/36/42. L'azienda è
    attiva: https://velco.tech, dispositivi IoT e software di gestione flotte per biciclette elettriche (Nantes).
    (FATTO)
  - VELCO, IT 2003901168666, VELCO SPA, classi 35 (messa a disposizione di prodotti elettronici) e 42 (studio e
    progettazione di componenti elettronici), «Registered» secondo TMview (deposito 2003; rinnovo non verificato).
  - VELCO, BX 730180, Velco Brandblusmateriaal B.V., 9/37 (antincendio).
  - WELKO, WO 474023, Bossard Group AG, 6/9/14/20 (del 1982).
- Simili per una lettera in 35/39/42 (FATTO): DELKO (Delko Europe, EM e WO, 35/37/39/42), VELMO (EM 019346495,
  KERYON, 35/42), VEKO (9), NELKO (9), TELKO (WO, 9/42), VELLO (IDEXX, WO, 9/42).
- DEDUZIONE: il Velko identico riguarda prodotti lontani (batterie), ma è nella stessa classe 9 e va valutato. Più
  serio è Velco: si pronuncia come Velko, ha software e localizzazione di veicoli (39) in Francia, con un'azienda
  che vende software per flotte. Per questo il giudizio è «ostacoli da valutare» vicino a «ostacolo forte».

### Domini

| Dominio | Registrato | Creato | Cosa c'è |
|---|---|---|---|
| velko.com | sì | 03/02/1999 | Velko Hinge Inc., cerniere industriali (USA) |
| velko.it | sì (DNS) | non letto | pagina «dominio già registrato» di Aruba |
| velko.eu | sì (DNS) | non letto | «velko.eu is for sale!» |
| velko.io | sì | 05/12/2025 | Velko: agenti IA per telefono e chat per piccole imprese (Paesi Bassi) |
| velko.app | sì | 02/03/2026 | «Velko – ChatGPT MCP App» |

### Prodotti

- velko.io (assistenti IA per il contatto clienti), velko.app (app MCP). (FATTO)
- App Store: «Velko: IPTV Player & TV Guide» (sviluppatore individuale), «Velko» (Health & Fitness). (FATTO,
  [link](https://apps.apple.com/it/app/velko-lettore-iptv-tv/id6775969853))
- Nessun software di magazzino con questo nome trovato. (FATTO per quanto cercato)

## Riserva (verifica rapida)

Per la riserva: TMview «Is», «Contains» e «Fuzzy» su EM/IT/WO, «Is» su tutti gli uffici, WIPO per nome, domini
`.com`/`.app` con RDAP e `.it`/`.eu` con DNS, App Store e GitHub. Prodotti e servizi letti solo per i marchi più
rilevanti.

### Trako

- TRAKO, EM 019417745, Międzynarodowe Targi Gdańskie S.A., domanda del 04/09/2026 in esame, classi 35
  (organizzazione di fiere, pubblicità, marketing) e 41. Stesso titolare: TRAKO, PL Z.177431, classe 35, registrato
  fino al 2037. TRAKO, Bulgaria, 7/12/35, persona fisica, registrato 2026. Fuori UE: TRAKO, Svizzera 11542/2026,
  classe 42 (SaaS, cartografia, hosting di applicazioni), persona fisica. (FATTO, TMview)
- Simili: TRACO, IT 2006901394723, classe 39; TRACO e TRACO POWER, TracoPower (WO, 9); TRACO, Saferoad Traffic
  (EM, 6/9/11). (FATTO)
- Domini: trako.com registrato dal 11/05/2000 (non risponde); trako.it NXDOMAIN (probabilmente libero); trako.eu
  registrato (reindirizza); trako.app registrato il 04/11/2026.
- Prodotti: app «Trako» (Business, Visen Tech Ltd), «Trako GPS». (FATTO, App Store)
- DEDUZIONE: identico in classe 35 in UE, ma per fiere e pubblicità (TRAKO è anche il nome della fiera ferroviaria
  di Danzica, IPOTESI da confermare); ostacoli da valutare.

### Sorto

- Nessun identico vivo in EM/IT/WO né su altri uffici UE. SORTO, Regno Unito UK00003894220, Circletek Ltd,
  classe 42 «SaaS», registrato fino al 2033 (fuori UE, conta se si vende nel Regno Unito); domanda SORTO nelle
  Filippine (9/35/42, Sorto Solutions Co.). (FATTO, TMview e WIPO). Nota: la ricerca approssimata di TMview per
  «sorto» si è fermata ai primi 1000 risultati su 7866; la ricerca «identico» ne dà 0.
- Simili: **Forto**, WO 1513928, Forto Logistics SE & Co. KG, classi 9, 39 (trasporto, spedizioni) e 42 (sviluppo
  software, SaaS), con designazione UE. KORTO (EM, 9/42), NORTO, CORTO, SOPTO. (FATTO)
- Domini: sorto.com dal 13/04/2000 (rimanda a un accesso Google), sorto.it registrato (parcheggio), sorto.eu
  registrato, sorto.app dal 23/06/2022.
- Prodotti: app «Sorto» (Lifestyle, Sorto Solutions Co.). (FATTO)
- DEDUZIONE: nessun identico in UE; Forto è un'azienda di logistica digitale con SaaS, a una lettera di distanza:
  ostacoli da valutare.

### Rigo

- Identici vivi: Rigo, EM 012275798 (Burgess Furniture, 20/35); RIGO, EM 013298096 (RIGO Verffabriek, 35/40);
  RIGO, WO 1313567 (Rigo Trading, 35/36/45); RIGO, IT 2022000027104 (RIGO PUTTERS S.R.L.S., 12/28/42); RIGO, IT
  2020000104192 (persona fisica, 35/37/40/42). Anche DE RIGO (De Rigo S.p.A., 9/35). (FATTO, TMview)
- Domini: rigo.com dal 07/03/1997 (Autogru Rigo, gru), rigo.it e rigo.eu registrati (rigo.eu in vendita), rigo.app
  dal 08/05/2018.
- Prodotti: RigoHR (Productivity) e altre app. DEDUZIONE: ostacolo forte.

### Movo

- Dieci identici vivi in EM/IT/WO, tra cui: MOVO, EM 019451607 e "MOVO" EM 019451776, Movo Mobility AB, domande
  del 18/11/2026, classi 9/35/39/42 (software e SaaS per parcheggi); MOVO, EM 017993319/017993323, 9/39; MOVO,
  EM 019271779, MOVOPACK, 39; MOVO, IT 2012902071019, EXO Automotive, 9. Fuori UE: MOVO, Giappone, Hacobu, 39/42
  (logistica). (FATTO, TMview e WIPO)
- Domini: movo.com dal 29/07/1995 (Interactive Voice), movo.it registrato (parcheggio), movo.eu in vendita,
  movo.app dal 08/10/2022. Molte app «Movo» (mobilità, consegne). DEDUZIONE: ostacolo forte.

### Venko

- Identici vivi: VENKO, EM 019368269, Venko sp. z o.o., 9/35/42 (apparecchi per prove ad alta tensione, vendita,
  collaudi), registrato 2026; VENKO, EM 018080773 (9/28/41/43); VENKO, EM 018597867 (35/41); VENKO, EM 012537817
  (35/37/40); venko, WO 1770034, Rivero AG, 36/42, con designazione UE. (FATTO, TMview)
- Domini: venko.com dal 12/06/2005 (consulenza HR in Brasile), venko.it e venko.eu registrati, venko.app dal
  13/10/2026. App «Venko Practice». DEDUZIONE: ostacolo forte.

### Arvo

- Identici vivi: ARVO, EM 019441947 (domanda 2026, classe 9); ARVO, EM 018383817, Peili Vision Oy (10/42/44); ARVO,
  WO 1783446 (35; designazioni IN, CN, GB, FR, CA). Su tutti gli uffici 46 risultati, tra cui ARVO in Germania
  (classe 9, Turtle Beach, da WIPO), Finlandia, Estonia, Spagna, Francia. (FATTO)
- Domini: arvo.com dal 09/12/1995 (503), arvo.it registrato (in vendita), arvo.eu registrato, arvo.app dal
  05/07/2022. App «Arvo» (fitness, assistente IA). DEDUZIONE: ostacolo forte.

### Volko

- Nessun identico vivo in EM/IT/WO, né «Volco». Su tutti gli uffici: solo volko in Ucraina (35). WIPO: anche
  «volko telecom» (Brasile, 35). (FATTO)
- Simili: WOLCO, EM 001402619, Talleres Wolco S.L., 6/7/42 (in 42: controllo qualità e studi di ingegneria su
  utensili da taglio), registrato fino al 2029; VALCO (EM, 9), VELCO (IT, 35/42), VOLCOM (9). (FATTO)
- Domini: volko.com dal 30/07/1997 (Volko Supply, comignoli, USA); volko.it NXDOMAIN (probabilmente libero);
  volko.eu registrato (403); volko.app dal 06/05/2026.
- Prodotti: nessuno trovato nel settore (App Store USA: 0; quello italiano non ha risposto). GitHub: VolkovLabs
  (plugin Grafana), non pertinente.
- DEDUZIONE: sembra libero nei registri consultati; da valutare solo Wolco (in tedesco W si legge V, servizi
  lontani).

### Vekto

- Nessun identico in EM/IT/WO; **Vekto**, Benelux 1560421, Vekto B.V., domanda del 16/10/2026 pubblicata, classi
  9, 35 (assistenza e gestione commerciale, servizi amministrativi), 42 (servizi IT). VECTO, EM 006141501 e
  013937073, Prospect i Kristianstad AB, 7/9. (FATTO, TMview)
- Domini: vekto.com dal 11/07/2011 (non risponde), vekto.it registrato, vekto.eu registrato (sito lituano «Vekto»
  in costruzione), vekto.app dal 16/05/2025. App «VEKTO: To‑Do List». DEDUZIONE: ostacolo forte.

### Kardo

- **Kardo**, EM 019341171, Kardo Europe B.V., registrato 2026, classi 35 (tra l'altro «inventory management»,
  gestione amministrativa degli ordini) e 42 (SaaS, software ERP, POS, **supply chain management**, gestione
  ordini). KARDO, Germania 302022111131, XWAVE Germany UG, 9/35/41. KARDO (BX, SE), Lincoln Smitweld, 9; KARDO
  (CZ), 16/39/40. CARDO, EM 009687294, Cardo Systems, 9. (FATTO, TMview e WIPO)
- Domini: kardo.com dal 15/12/1999, kardo.it registrato, kardo.eu in vendita, kardo.app dal 28/08/2025. App Kardo
  POS, Kardo HR, Kardo Boss (Eyosoft). DEDUZIONE: ostacolo forte (stesso settore).

### Rivo

- Identici vivi: RIVO, EM 018738769, Surecomp Services, classe 42 (SaaS per la finanza del commercio, anche per
  spedizionieri); RIVO, WO 1693521, Tokenpay, 9/35/36/42, con designazione UE e IT; RIVO, EM 018683104 e WO
  1756443, Evoqua, 9; RIVO, EM 019147245 e WO 1877282, SARL RIVO, 9/35/…; «SD Worx Rivo», EM 019356855, 9/35/36/41/42/45.
  WIPO: RIVO TECNOLOGIA LOGISTICA (Brasile, domanda, 9). (FATTO). La ricerca approssimata di TMview per «rivo» non
  è riuscita (blocco del sito): non verificato.
- Domini: rivo.com dal 17/01/1998, rivo.it registrato (in costruzione), rivo.eu in vendita, rivo.app dal
  09/05/2018. Molte app «Rivo». DEDUZIONE: ostacolo forte.

### Dokra

- Nessun identico in EM/IT/WO; **DOKRA**, Repubblica Ceca 614369, DOKRA s.r.o., domanda del 06/10/2026, classi 9
  (software, app, API), 35, 37, 38, 41, 42 (sviluppo software, SaaS). Simile: **DEKRA** (DEKRA e.V.), molti marchi
  EM e WO, anche in 9/35/42 e in tutte le classi (EM 018974336). (FATTO, TMview)
- Domini: dokra.com dal 14/04/2011 (pagina vuota), dokra.it NXDOMAIN (probabilmente libero), dokra.eu registrato
  (403), dokra.app dal 22/01/2026.
- DEDUZIONE: ostacolo forte (identico per software in un paese UE, più la vicinanza a DEKRA, marchio molto
  diffuso; la notorietà è da valutare).

## Limiti della ricerca

- **Registri consultati in modo indiretto.** EUIPO e UIBM non erano raggiungibili: i loro dati vengono da TMview
  (copia aggiornata periodicamente). Le domande depositate negli ultimi giorni o non ancora pubblicate possono
  mancare.
- **Blocchi e tagli.** TMview ha bloccato a tratti le richieste automatiche: la ricerca approssimata di «rivo» non
  c'è, quella «contiene» di «cardo» è parziale, e le ricerche approssimate di «sorto», «rigo», «movo», «corso»,
  «varco» e «cardo» si fermano ai primi 1000 risultati. Le ricerche «identico» sono complete per tutti i nomi.
- **Ricerca fonetica non completa.** Abbiamo coperto le varianti C/K, W/V e quelle a una lettera di distanza
  restituite da TMview; non le trascrizioni in altri alfabeti, né le pronunce delle altre lingue UE oltre a
  quelle citate.
- **Marchi figurativi.** Non abbiamo confrontato loghi e immagini.
- **Prodotti e servizi** letti solo per i marchi più rilevanti; per gli altri riportiamo solo le classi.
- **Non coperto:** diritti non registrati (uso di fatto di un nome, che in Italia e in altri paesi UE può dare
  diritti), ragioni sociali e insegne (registro delle imprese), nomi a dominio come diritto anteriore, registri
  nazionali extra UE oltre a quelli in TMview/WIPO, Regno Unito solo dove è comparso per caso.
- **Domini `.it` e `.eu`** letti dal DNS: «probabilmente libero» va confermato sul whois di nic.it
  (https://www.nic.it/it/trova-il-tuo-it/web-whois) prima di registrarlo. Le date di creazione di `.it` e `.eu` non
  sono state lette.
- **Stato dei vecchi marchi italiani** (depositi 2001–2003 dati «Registered» da TMview): il rinnovo non è stato
  verificato su UIBM.
- **Prodotti simili:** la ricerca web ha dato pochi risultati utili; App Store e GitHub sono parziali (l'App Store
  ha rifiutato alcune richieste per troppe chiamate). Product Hunt e Google Play non sono stati consultati.

## Fonti

- TMview, ricerca e schede (API del sito): https://www.tmdn.org/tmview/ (consultato il 20/11/2026).
- WIPO Global Brand Database: https://branddb.wipo.int/en/similarname (20/11/2026).
- DPMAregister, marchio KURSO 302017231600:
  https://register.dpma.de/DPMAregister/marke/register/3020172316000/DE (20/11/2026).
- EUIPO eSearch (link alle schede EM; non raggiungibile dal container): https://euipo.europa.eu/eSearch/
- UIBM banca dati (non raggiungibile dal container): https://www.uibm.gov.it/bancadati/
- WIPO Madrid Monitor (schede WO): https://www.wipo.int/madrid/monitor/en/
- RDAP: https://rdap.org/ e https://rdap.identitydigital.services/rdap/ (`.io`).
- DNS‑over‑HTTPS: https://dns.google/ e https://cloudflare-dns.com/dns-query
- Siti aperti: https://www.kurso.de, https://kurso.app, https://kurso.eu, https://varko.io, https://varko.app,
  https://www.velko.com, https://velko.io, https://velko.app, https://velco.tech e le home dei domini citati.
- App Store (API di ricerca): https://itunes.apple.com/search
- GitHub, ricerca repository: https://github.com/search
