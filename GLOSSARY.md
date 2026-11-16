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

**Vendita al banco**:
Un ordine cliente creato nel momento in cui il cliente è in magazzino e porta via subito la merce.
_Evitare_: vendita assistita, vendita diretta

**In attesa di pagamento**:
Stato di un ordine cliente non ancora pagato, che non riceve merce finché il pagamento non arriva.
_Evitare_: sospeso, bloccato

**Evaso**:
Stato di un ordine cliente la cui merce è stata prelevata ed è pronta a partire.
_Evitare_: completato, chiuso

**Spedito**:
Stato di un ordine cliente la cui merce è uscita dal magazzino.
_Evitare_: consegnato

## Merce e scorte

**DDT**:
Il documento di trasporto che accompagna una consegna del fornitore e rimanda agli ordini fornitore a cui appartiene.
_Evitare_: bolla

**Ricevimento**:
L'arrivo di una consegna in magazzino, con le identificazioni fatte sulla merce.
_Evitare_: accettazione, entrata

**Quantità in bolla**:
La quantità che il fornitore dichiara sul DDT per una riga, distinta da quella contata in magazzino.
_Evitare_: quantità stampata, quantità dichiarata

**Giacenza**:
La quantità di un articolo presente in magazzino.
_Evitare_: stock, scorta (al singolare), disponibilità

**Assegnazione**:
La parte di giacenza riservata a una riga di ordine cliente; può coprire la riga solo in parte.
_Evitare_: allocazione, impegno, prenotazione

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

## Sistemi

**Gestionale**:
Il programma che tiene articoli, ordini e documenti di un'azienda, accanto al quale il prodotto può lavorare.
_Evitare_: ERP, software esterno

**Sistema d'origine**:
Il programma in cui un dato è nato e in cui soltanto si può cambiare: il gestionale, il negozio online o il prodotto
stesso.
_Evitare_: master, fonte di verità, sistema esterno

## Persone

**Operatore**:
Chi riceve, identifica, preleva e spedisce la merce.
_Evitare_: magazziniere, utente (da solo)

**Responsabile**:
Chi, oltre al lavoro dell'operatore, gestisce catalogo, rettifiche, annullamenti e utenti.
_Evitare_: amministratore, admin, capo magazzino
