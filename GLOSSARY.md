# Gestionale di magazzino (base generica)

Lingua comune della base generica: il gestionale che riceve la merce, la identifica e assegna le scorte agli ordini
cliente. Il nome del prodotto è ancora da scegliere (decisione 20 in `docs/decisioni.md`).

## Catalogo

**Articolo**:
Un tipo di prodotto a catalogo; tutte le scatole uguali sono lo stesso articolo.
_Evitare_: prodotto, SKU, referenza

**Codice articolo**:
Un codice che identifica un articolo; un articolo può averne più di uno (barcode, codice del fornitore, codice del
produttore, codice interno).
_Evitare_: codice prodotto

**Collegamento da confermare**:
Un codice del fornitore collegato a un articolo da un operatore e non ancora confermato dal responsabile: vale, ma
ogni volta chiede un tocco di conferma.
_Evitare_: alias provvisorio, abbinamento

**Barcode**:
Il codice articolo in forma di codice a barre o QR, letto otticamente.
_Evitare_: EAN (è solo uno dei formati), codice a barre

**Codice stampato**:
Il codice articolo stampato in chiaro sull'etichetta della scatola, letto come testo quando manca il barcode.
_Evitare_: numero seriale, seriale, matricola

**Articolo provvisorio**:
Un articolo creato nel magazzino quando c'è un gestionale accanto, usabile subito, che diventa definitivo quando il
gestionale lo conosce con lo stesso codice.
_Evitare_: articolo temporaneo, bozza

**Articolo da confermare**:
Un articolo creato da un operatore e non ancora controllato dal responsabile: si usa subito, e il responsabile lo
conferma, lo corregge o lo unisce a un altro. Con un gestionale accanto può essere anche provvisorio: sono due attese
diverse, una del responsabile e una del gestionale.
_Evitare_: articolo in bozza, articolo non approvato

**Unione di articoli**:
Il rimedio a un doppione: un articolo creato due volte confluisce in quello già esistente con codici, foto e giacenza, e
resta nello storico come «unito a» quello.
_Evitare_: fusione, merge, cancellazione del doppione

**Identificazione**:
Il riconoscimento dell'articolo che l'operatore ha davanti, dal barcode, dal codice stampato o dall'aspetto, confermato
dall'operatore quando il programma non è certo.
_Evitare_: riconoscimento (da solo), scansione (è il singolo gesto registrato)

**Articoli attesi**:
Gli articoli che il programma si aspetta di vedere in un momento del lavoro, come quelli delle righe aperte degli ordini
fornitore al ricevimento o quello della riga da prelevare; si cercano prima del resto del catalogo.
_Evitare_: candidati, contesto, articoli previsti

**«Non lo so»**:
La risposta del programma quando nessun codice e nessun aspetto indicano un articolo con abbastanza sicurezza: invece di
indovinare, chiede all'operatore come proseguire.
_Evitare_: errore, articolo non trovato

**Foto di riferimento**:
Una foto di un articolo conservata per riconoscerlo dall'aspetto.
_Evitare_: immagine campione

**Unità di magazzino**:
L'unità in cui si conta un articolo in giacenza (pezzo, chilo, metro); ogni articolo ne ha una sola.
_Evitare_: unità di misura (da sola), UM

**Conversione**:
Il rapporto fisso tra un'unità del fornitore (tonnellata, confezione, coppia) e l'unità di magazzino di un articolo.
_Evitare_: fattore, equivalenza

**Prezzo di vendita**:
Il prezzo a cui un articolo si vende al cliente.
_Evitare_: listino (da solo)

**Costo d'acquisto**:
Il prezzo a cui un articolo si compra dal fornitore.
_Evitare_: prezzo d'acquisto, costo (da solo)

## Ordini

**Fornitore**:
Chi spedisce la merce al magazzino.

**Ordine fornitore**:
La merce chiesta a un fornitore e attesa in magazzino, divisa in righe con quantità ordinata, ricevuta e residua.
_Evitare_: ordine d'acquisto, ordine (da solo)

**Riferimento cliente**:
L'indicazione, su un ordine fornitore o su una sua riga, del cliente per cui la merce è ordinata.
_Evitare_: commessa, rif.

**Proposta d'ordine**:
Un ordine fornitore preparato dal programma e non ancora confermato da una persona.
_Evitare_: bozza d'ordine, suggerimento

**Ordine cliente**:
La merce da consegnare a un cliente, divisa in righe; è aperto finché non è evaso.
_Evitare_: ordine di vendita, ordine (da solo)

**Vendita assistita**:
Un ordine cliente creato sul posto da chi vende, scegliendo cliente, articoli e ubicazione; comprende la vendita al banco
e quella preparata per un agente o da spedire. Con un gestionale accanto, il resto della vendita si fa nel gestionale.
_Evitare_: vendita diretta; «banco» solo per il caso in cui il cliente porta via subito la merce

**Agente**:
Chi ha fatto la vendita per conto dell'azienda e porta gli ordini; in UFP dà il titolo al piano di spedizione.
_Evitare_: venditore, commerciale (da solo)

**In attesa di pagamento**:
Stato di un ordine cliente non ancora pagato, che non riceve merce finché il pagamento non arriva.
_Evitare_: sospeso, bloccato

**Evaso**:
Stato di un ordine cliente la cui merce è stata prelevata ed è pronta a partire.
_Evitare_: completato, chiuso

**Spedito**:
Stato di un ordine cliente la cui merce è uscita dal magazzino; si segna quando la merce parte davvero, non quando è
pronta.
_Evitare_: consegnato

**Piano di spedizione**:
Un gruppo di ordini cliente con un titolo, dato a un preparatore da chi pianifica.
_Evitare_: giro, lista di prelievo, batch

**Coda di prelievo**:
Gli ordini pronti da prelevare in ordine di data, dati uno alla volta a chi preme «Prossimo ordine», quando il
magazzino non usa i piani di spedizione.
_Evitare_: piano automatico

**Corriere**:
Chi ritira i colli e porta la merce al cliente; ogni ordine da spedire ne ha uno.
_Evitare_: vettore, spedizioniere

## Merce e scorte

**DDT**:
Il documento di trasporto che accompagna una consegna del fornitore e rimanda agli ordini fornitore a cui appartiene;
nel programma, la sua registrazione con le righe nate dalle letture.
_Evitare_: bolla (per la registrazione), entrata merci

**Bolla**:
Il foglio di carta (o il PDF) del DDT consegnato dal fornitore; il programma ne conserva la foto con il DDT.
_Evitare_: DDT (per il foglio), documento

**Quantità in bolla**:
La quantità che la bolla dichiara per un articolo; si confronta con la quantità contata e con quella ordinata, senza
mai sostituire la contata.
_Evitare_: quantità attesa (è quella dell'ordine fornitore), quantità dichiarata

**Ricevimento**:
L'arrivo di una consegna in magazzino, con le identificazioni fatte sulla merce.
_Evitare_: accettazione, entrata

**Quantità in bolla**:
La quantità che il fornitore dichiara sul DDT per una riga, distinta da quella contata in magazzino.
_Evitare_: quantità stampata, quantità dichiarata

**Giacenza**:
La quantità di un articolo presente in magazzino.
_Evitare_: stock, scorta (al singolare), disponibilità

**Disponibilità**:
La quantità di un articolo che si può ancora dare a un ordine o vendere: la giacenza meno la merce assegnata, in VEND,
prelevata, in attesa di decisione o da rendere.
_Evitare_: liberi, prelevabile, disponibile (da solo)

**Assegnazione**:
La parte di giacenza riservata a una riga di ordine cliente; può coprire la riga solo in parte.
_Evitare_: allocazione, impegno, prenotazione

**Collo**:
Una scatola o confezione così come arriva dal fornitore; ne arrivano spesso molte uguali dello stesso articolo.
_Evitare_: pacco, cartone, confezione (da sola)

**Contenuto del collo**:
Quanti pezzi, o quanta quantità nell'unità di magazzino, contiene un collo di un articolo da un fornitore; il programma
ricorda l'ultimo confermato e lo propone come consiglio.
_Evitare_: conversione (è un'altra cosa, approvata dal responsabile), imballo

**Carico**:
Il movimento che fa entrare in giacenza la merce ricevuta.
_Evitare_: versamento, entrata

**Residuo**:
La quantità di una riga d'ordine fornitore ancora attesa: ordinata meno ricevuta, mai sotto zero.
_Evitare_: inevaso, rimanenza

**Eccedenza**:
La merce ricevuta oltre la quantità ordinata su una riga d'ordine fornitore.
_Evitare_: surplus, extra

**Merce senza ordine**:
Merce ricevuta che nessun ordine fornitore aperto prevede.
_Evitare_: merce fuori ordine, omaggio (è solo uno dei casi)

**VEND**:
La merce arrivata con un ordine fornitore fatto per un cliente preciso: resta da parte per la sua riga d'ordine
cliente fino al prelievo, anche se il magazzino non ha un'area fisica apposita.
_Evitare_: venduto (da solo), impegnato

**Movimento**:
Ogni variazione di giacenza (carico, prelievo, rettifica), con chi l'ha fatta e quando.
_Evitare_: transazione, operazione

**Correzione**:
Il movimento che rimedia a un movimento sbagliato, collegato a quello: il movimento sbagliato non si cancella.
_Evitare_: storno, annullamento (da solo), cancellazione

**Rettifica**:
Il movimento che porta la giacenza di un'ubicazione alla quantità contata.
_Evitare_: aggiustamento, inventario (da solo)

**Inventario**:
La conta di tutto il magazzino o di una parte (alcune ubicazioni, alcuni articoli, la merce di un fornitore), chiesta
dal responsabile ed eventualmente divisa tra più persone; serve sia a fine anno sia durante l'anno.
_Evitare_: conta ciclica, rilevazione, inventario a rotazione

**Conta cieca**:
Il modo di contare in cui chi conta non vede quanti pezzi dovrebbero esserci.
_Evitare_: conta al buio, conta senza atteso

**Seconda conta**:
La conta ripetuta subito dalla stessa persona quando il primo numero non torna con la giacenza.
_Evitare_: riconteggio, verifica

**Differenza d'inventario**:
Lo scarto tra la quantità contata in un'ubicazione e la giacenza nel momento in cui la conta si è chiusa; diventa una
rettifica solo quando il responsabile la approva.
_Evitare_: ammanco, discrepanza, scostamento

**In conta**:
Lo stato di un'ubicazione che qualcuno sta contando: gli altri la vedono e non la aprono.
_Evitare_: bloccata, occupata

**Ubicazione**:
Il punto del magazzino in cui sta la merce, come uno scaffale o una corsia; si usa solo se il magazzino lo sceglie.
_Evitare_: posizione, locazione, buca (è il nome usato in UFP)

**Ubicazione abituale**:
L'ubicazione in cui di solito si mette un articolo; facoltativa, e l'articolo può stare anche altrove.
_Evitare_: ubicazione principale, ubicazione fissa

**Area di ricevimento**:
L'ubicazione in cui sta la merce contata e non ancora messa a posto.
_Evitare_: CHECK (è il nome usato in UFP), zona di arrivo

**Messa a posto**:
Lo spostamento della merce dall'area di ricevimento alla sua ubicazione.
_Evitare_: stoccaggio, «sparare in buca», Libera

**Compito**:
Un lavoro fisico che il programma chiede di fare, come mettere a posto la merce ricevuta o rimettere a posto quella di
un ordine annullato.
_Evitare_: missione, task, lista (da sola)

**Da controllare**:
L'elenco dei movimenti e degli avvisi che il responsabile deve guardare e approvare o correggere.
_Evitare_: anomalie, eccezioni, coda (da sola)

**Cose in sospeso**:
Il lavoro iniziato e non chiuso di una sezione (un DDT aperto, un ordine preso, una vendita non confermata), diviso in
miei, di colleghi, fermi e vecchi.
_Evitare_: pendenti, backlog, da fare (da solo)

**Merce danneggiata**:
Merce contata che non si può usare: non si assegna a nessun ordine finché il responsabile non decide se tenerla,
renderla al fornitore o scartarla.
_Evitare_: merce difettosa, scarto (è una delle decisioni)

**Scarto**:
L'uscita definitiva dal magazzino di merce danneggiata, decisa dal responsabile.
_Evitare_: rottamazione, perdita, scrap

**Registro**:
L'elenco in ordine di tempo di tutte le operazioni, con chi, quando, da quale dispositivo ed esito; si consulta nella
sezione «Documenti».
_Evitare_: log, storico (da solo), cronologia (è quella di un singolo documento)

**Reso al fornitore**:
La merce che il magazzino restituisce a un fornitore, raccolta per fornitore e seguita dalla richiesta fino alla
partenza.
_Evitare_: restituzione, RMA (è il numero di autorizzazione), reso (da solo)

**Reso del cliente**:
La merce che un cliente restituisce, ricevuta partendo dall'ordine spedito con cui era uscita.
_Evitare_: rientro, reso (da solo)

**Da rendere**:
Lo stato della merce che il responsabile ha deciso di restituire al fornitore: resta in giacenza ma non si assegna e
non si preleva finché non parte.
_Evitare_: in reso, bloccata

**Area resi**:
L'ubicazione dove aspetta la merce da rendere, con il nome scelto dal magazzino.
_Evitare_: RESIF (è il nome di UFP), zona resi

**Richiesta di reso**:
Il messaggio al fornitore che chiede di accettare un reso, con le righe, il motivo e le prove.
_Evitare_: segnalazione, mail di reso

**Riserva**:
La dicitura scritta sul documento del corriere quando un collo arriva rovinato, che conserva il diritto di contestare.
_Evitare_: accettato con riserva (è il timbro), contestazione

## Sistemi

**Gestionale**:
Il programma che tiene articoli, ordini e documenti di un'azienda, accanto al quale il prodotto può lavorare.
_Evitare_: ERP, software esterno

**Sistema d'origine**:
Il programma in cui un dato è nato e in cui soltanto si può cambiare: il gestionale, il negozio online o il prodotto
stesso.
_Evitare_: master, fonte di verità, sistema esterno

**Server in sede**:
Il computer del magazzino, sulla sua rete interna, che tiene i dati e serve il programma a telefoni, palmari e
computer.
_Evitare_: cloud, hosting

**Palmare**:
Un dispositivo portatile robusto con un lettore di barcode a grilletto, usato in magazzino al posto del telefono.
_Evitare_: terminale, PDA, scanner (lo scanner è solo il lettore)

## Persone

**Operatore**:
Chi riceve, identifica, preleva e spedisce la merce.
_Evitare_: utente (da solo)

**Mansione**:
Il lavoro di tutti i giorni di una persona, che decide cosa vede per primo: magazziniere (riceve e mette a posto) o
preparatore (prepara gli ordini e fa le vendite assistite). Una persona può averne più d'una; non cambia cosa può fare.
_Evitare_: ruolo, profilo

**Permesso**:
Un lavoro in più che il responsabile dà a un operatore: pianificare le spedizioni, confermare le spedizioni.
_Evitare_: ruolo, diritto

**Responsabile**:
Chi, oltre al lavoro dell'operatore, gestisce catalogo, rettifiche, annullamenti e utenti.
_Evitare_: amministratore, admin, capo magazzino
