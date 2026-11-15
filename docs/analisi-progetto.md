# Analisi del progetto

Data: 15/11/2026. Stato: prima analisi, prima della sessione Wayfinder sull'architettura.

Le decisioni dell'utente sono in `docs/decisioni.md`; qui non si ripetono, si usano.
Le ricerche sono in `docs/research/`. In questo documento:

- **Fatto**: detto dall'utente o documentato in una ricerca, con riferimento.
- **Deduzione**: ragionamento nostro, motivato.
- **Ipotesi**: da verificare.

## 1. Cosa deve fare il sistema

1. **Tenere il catalogo**: fino a 35.000 articoli (decisione 5). Ogni articolo ha uno o più codici, una descrizione e delle foto di riferimento.
2. **Identificare un articolo in arrivo** inquadrandolo con il telefono (decisioni 6 e 9). Prima il barcode; se manca, il codice stampato sull'etichetta; se manca anche quello, l'aspetto.
3. **Registrare l'arrivo**, cioè il movimento di carico, e collegarlo all'ordine fornitore da cui proviene.
4. **Assegnare le scorte agli ordini cliente** non ancora evasi o spediti, dal più vecchio al più recente (decisione 2).
5. **Aggiungere un articolo nuovo fotografandolo**, con codice e descrizione (decisione 8).
6. **Essere installabile in qualsiasi magazzino** e poi specializzabile per uno specifico (decisione 4).

## 2. Concetti del dominio (prima bozza)

Non è ancora il glossario: quello si fa con `domain-modeling` nella sessione Wayfinder.

| Concetto | Cosa rappresenta | Note |
|---|---|---|
| Articolo | Un tipo di prodotto a catalogo (SKU). | Fino a 35.000. |
| Codice articolo | Un codice che identifica l'articolo. | Più codici per articolo: EAN/GTIN, codice del fornitore, codice del produttore, codice interno. Lo stesso codice del fornitore può ripetersi tra fornitori diversi. |
| Numero seriale | Il codice di un singolo pezzo. | Da chiarire, vedi §6 domanda D2. |
| Foto di riferimento | Foto dell'articolo usate per riconoscerlo. | Ogni foto ha la sua impronta numerica (embedding), vedi §4. |
| Fornitore | Chi spedisce la merce. | |
| Ordine fornitore | Merce ordinata e attesa, divisa in righe. | Le righe sono quantità ordinate, ricevute e residue. |
| Ricevimento | L'evento di arrivo di una consegna. | Contiene le identificazioni fatte con il telefono. |
| Giacenza | La quantità disponibile di un articolo, eventualmente per ubicazione. | |
| Movimento | Ogni variazione di giacenza: carico, scarico, rettifica. | Fa da storico e da traccia per i controlli. |
| Ordine cliente | Merce da evadere, divisa in righe; stato: aperto, evaso, spedito. | |
| Assegnazione | Quanta giacenza è riservata a quale riga d'ordine cliente. | Si fa in ordine di data dell'ordine. |

## 3. Il percorso di identificazione

**Fatto**: l'ordine dei tentativi lo ha deciso l'utente (decisione 6): barcode → codice stampato → aspetto.

**Deduzioni** (da confermare nella sessione Wayfinder):

1. **Il barcode chiude quasi sempre la questione.** Se il codice letto è registrato su un solo articolo, l'identificazione è certa. Restano due casi: codice sconosciuto, che porta all'inserimento di un articolo nuovo (§1 punto 5), e codice registrato su più articoli, che porta alla scelta dell'operatore.
2. **Il codice stampato va letto confrontandolo con il catalogo, non preso alla lettera.** L'OCR sbaglia sui caratteri che si somigliano (0/O, 1/I/l, 5/S, 8/B). Conviene quindi cercare nel catalogo i codici più vicini a quello letto, tenendo conto di queste confusioni. Se uno solo è vicino abbastanza, è quello. È il punto che più riduce gli errori, che è l'obiettivo dichiarato dall'utente.
3. **Il contesto restringe i candidati.** Al ricevimento si sa di solito da quale fornitore arriva la merce. Gli articoli plausibili sono allora le righe aperte dei suoi ordini: decine o centinaia, non 35.000. Il riconoscimento visivo deve distinguere tra pochi candidati, il che è molto più affidabile. Vale anche per l'OCR.
4. **L'immagine propone, l'operatore conferma.** Con somiglianza medio-alta tra gli articoli (decisione 7), l'immagine da sola non basta a scalare la giacenza in automatico. Va mostrata una breve lista di candidati, con foto e codice, da confermare con un tocco. Ogni conferma salva la foto come nuovo riferimento, e il sistema migliora con l'uso.
5. **«Non lo so» è una risposta valida.** Sotto una soglia di somiglianza, il sistema lo dice e chiede il codice a mano o l'inserimento di un articolo nuovo, invece di indovinare.

## 4. Riconoscimento visivo: impostazione

> Questa sezione si completa con le tre ricerche in `docs/research/` (in corso).

**Deduzione**, valida a prescindere dal modello scelto. Con 35.000 articoli e un catalogo che cresce fotografando, un classificatore a classi fisse è inadatto: andrebbe riaddestrato a ogni articolo nuovo. Lo schema adatto è la **ricerca per somiglianza**:

1. Un modello già addestrato trasforma ogni foto in un'impronta numerica (embedding).
2. Le impronte delle foto di riferimento stanno in un indice.
3. Per riconoscere una foto si cerca l'impronta più vicina, eventualmente solo tra i candidati del contesto (§3 punto 3).
4. Aggiungere un articolo vuol dire aggiungere impronte, non riaddestrare.

Un adattamento leggero del modello sulle foto del magazzino resta possibile più avanti, se i dati reali lo giustificano.

## 5. Base generica e specializzazione

**Deduzione**: perché la base sia installabile ovunque (decisione 4), deve contenere la logica comune a ogni magazzino e lasciare fuori ciò che cambia da un magazzino all'altro.

- **Nella base**: catalogo, codici, identificazione, ricevimento, giacenza, movimenti, ordini, assegnazione, utenti e permessi, storico.
- **Nella specializzazione**: collegamento al gestionale o ERP già in uso (importare ordini, esportare movimenti), formati di codici ed etichette dei fornitori, regole di assegnazione diverse, ubicazioni, campi aggiuntivi, testi.
- **Come**: configurazione per le differenze semplici, punti di estensione (moduli o plugin) per quelle che richiedono codice. Si sceglie nella sessione Wayfinder.

## 6. Domande aperte per l'utente

Sono le domande che cambiano materialmente la soluzione. Andranno poste nella sessione Wayfinder.

- **D1. Regola all'arrivo.** La frase ricevuta è: «Se il magazzino ha disponibilità, la quantità viene scalata; altrimenti l'articolo arrivato viene associato all'ultimo ordine effettuato su quel fornitore e scalato direttamente dall'ordine». Non è chiaro cosa si scali quando la merce *arriva*, perché l'arrivo di solito aumenta la giacenza. Ci sono anche due possibili contraddizioni:
  - gli ordini cliente si servono dal più vecchio, ma l'ordine fornitore scelto è «l'ultimo»;
  - non è chiaro se «ordine» indichi l'ordine al fornitore o quello del cliente.

  Serve un esempio concreto con numeri.
- **D2. «Numero seriale».** È un codice che identifica il *tipo* di articolo (codice articolo del produttore o del fornitore)? Oppure identifica il *singolo pezzo*, e allora va anche registrato pezzo per pezzo (tracciabilità per seriale)?
- **D3. 35.000.** Sono 35.000 articoli diversi a catalogo, oppure 35.000 pezzi in giacenza?
- **D4. Fonte degli ordini.** Il sistema è il gestionale principale, cioè gli ordini nascono qui? Oppure si affianca a un gestionale o ERP esistente da cui importa ordini e a cui restituisce i movimenti? È la domanda che più incide sulla base generica.
- **D5. App sul telefono.** App installata (nativa o multipiattaforma) o applicazione web aperta dal browser? Il web è più semplice da distribuire. Però dal browser la fotocamera richiede una connessione HTTPS anche sulla rete interna, e su iOS ci sono limiti. Dipende anche da quali telefoni ha il magazzino: aziendali o personali, Android o iPhone.
- **D6. Rete assente.** Se il telefono perde la rete aziendale, il lavoro si ferma o deve continuare e sincronizzarsi dopo?
- **D7. Conferma dell'operatore.** Si accetta di confermare con un tocco quando il riconoscimento è solo visivo (§3 punto 4), o l'obiettivo è lo scarico senza nessun tocco?
- **D8. Quantità.** Si inquadra un pezzo alla volta, o anche un collo con più pezzi da contare? Contare pezzi dall'immagine è un problema diverso e più difficile.

## 7. Rischi principali

| Rischio | Perché | Mitigazione proposta |
|---|---|---|
| Articoli quasi identici scambiati | Somiglianza medio-alta (decisione 7). | Codice prima dell'immagine; candidati ristretti dal contesto; conferma dell'operatore. |
| Movimento sbagliato registrato in automatico | L'errore si propaga a giacenze e assegnazioni. | Ogni movimento annullabile e tracciato; conferma sotto soglia. |
| Foto di riferimento scarse o di cattiva qualità | Il riconoscimento dipende da come sono state scattate. | Guida alla ripresa nell'app; più foto per articolo; nuove foto dalle conferme. |
| Licenze dei modelli | Alcuni modelli non permettono l'uso commerciale o impongono AGPL. | Verificate nelle ricerche; scelta registrata. |
| Base troppo legata al primo magazzino | Il primo cliente detta i dettagli. | Separazione esplicita in §5; la specializzazione si fa dopo la base (decisione 4). |
