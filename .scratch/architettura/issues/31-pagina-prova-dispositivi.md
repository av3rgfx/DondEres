# Pagina di prova dei dispositivi

Type: task
Label: wayfinder:task
Status: open
Blocked by: nessuno (15 chiuso il 20/11/2026)

## Question

Su un iPhone, un telefono Android e un palmare di UFP reggono le ipotesi su cui poggia lo stack (127, 429, 430)?
Lavoro: scrivere una pagina di prova statica, pubblicarla nel ramo `gh-pages` nella sottocartella `prova-dispositivi`
(come la pagina di scatto, 149), farla aprire all'utente sui tre dispositivi e raccogliere i risultati che la pagina
mostra da copiare in chat. Il palmare la apre solo come link pubblico, senza installare nulla (430). Nessun dato
lascia il telefono; le foto della prova restano nella memoria del browser e si cancellano alla fine.

Prove (una schermata ciascuna, guidate):
1. Permesso della fotocamera in Safari su iPhone: resta dopo ricarica, dopo schermo spento e riacceso, e dall'icona
   sulla schermata Home (124).
2. Lettore del barcode: quale lettore usa (del browser o zxing-cpp, 425), tempo di lettura su barcode di scatole vere.
3. Grilletto del palmare: arriva come da una tastiera in un campo pronto, e in quanto tempo (119, 410).
4. Scatto da solo dopo circa mezzo secondo di immagine ferma (409): soglia da tarare.
5. Peso della foto ferma alla risoluzione prevista (408, stima 0,3–0,6 MB).
6. Operazione in attesa con la foto in IndexedDB: resta dopo ricarica e dopo chiusura del browser; il browser concede
   la memoria persistente? (127, 201)
7. Pagina nascosta e di nuovo visibile: l'evento arriva (serve alla 434).

Restano alla prima versione, sul computer di casa dell'utente (143): canale aperto con più telefoni, fascia dei 3
secondi, certificato con un router vero, prova di carico.

Risultato atteso: i risultati per dispositivo in `docs/architettura.md` (sezione «Stack», «Prove su dispositivi veri»)
e le eventuali decisioni in `docs/decisioni.md`; soglie (mezzo secondo, peso della foto) annotate per la costruzione.

## Comments
