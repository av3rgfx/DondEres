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
  (decisione 23), divisione tra le macchine e risultati della prova. Le scelte di aspetto sono di gusto, spettano
  all'utente e si fanno con prototipi da guardare. Una sola direzione visiva, registrata in `docs/decisioni.md`.
- Anche nome e brand kit sono scelte di gusto dell'utente (decisione 20). La skill logo-design si installa nel
  progetto, in `.claude/skills` e `.agents/skills` uguali, dopo averne letto il contenuto; mai a livello globale.
- Due magazzini reali fanno da banco di prova per la base, senza diventarne la specializzazione: uno affianca due
  gestionali esistenti (Ad Hoc Revolution e ARS Logistica) e usa solo il carico normale; l'altro usa solo Shopify e anche la giacenza «VEND»
  (decisioni 15 e 19).

## Decisions so far

<!-- una riga per ticket chiuso: [titolo](issues/NN-slug.md): sintesi della risposta -->

Prese prima della mappa, nel secondo giro di domande del 15/11/2026: decisioni 15–28 in
[`docs/decisioni.md`](../../docs/decisioni.md) (assegnazione parziale, codice stampato come tipo di articolo,
35.000 articoli, base principale o affiancata, prelievo e spedizione, Android e iPhone, niente lavoro senza rete,
tre livelli di conferma, quantità letta dalla scatola, ubicazioni facoltative, due ruoli, testi separati).

## Not yet specified

- **Server in sede: requisiti minimi.** Scheda grafica sì o no, memoria, sistema operativo: si chiarisce con i
  risultati della prova e la divisione tra le macchine.
- **Adattamento del modello visivo** (metric learning) sulle foto del magazzino: solo se i numeri della prova lo
  giustificano.
- **Installazione e configurazione iniziale in un magazzino nuovo:** procedura guidata (dove si sceglie se usare le
  ubicazioni, decisione 26), certificato HTTPS sulla rete interna, aggiornamenti, copie di sicurezza e ripristino.
- **Inventario e rettifiche:** conta periodica, correzione delle giacenze, annullamento dei movimenti e loro effetto
  sulle assegnazioni.
- **Descrizione proposta da un modello che legge immagini e scrive testo** per l'articolo nuovo: se tenerla, e quale
  modello, dipende dalla prova e dal server.

## Out of scope

- Specializzazione per un magazzino specifico (decisione 4).
- Registrazione per numero seriale del singolo pezzo, lotti e scadenze: possibile estensione (decisione 17).
- Lavoro senza rete (decisione 23).
- Conteggio dei pezzi dall'immagine (decisione 25).
- Più magazzini nella stessa installazione (decisione 26).
