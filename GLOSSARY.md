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

**Barcode**:
Il codice articolo in forma di codice a barre o QR, letto otticamente.
_Evitare_: EAN (è solo uno dei formati), codice a barre

**Codice stampato**:
Il codice articolo stampato in chiaro sull'etichetta della scatola, letto come testo quando manca il barcode.
_Evitare_: numero seriale, seriale, matricola

**Foto di riferimento**:
Una foto di un articolo conservata per riconoscerlo dall'aspetto.
_Evitare_: immagine campione

## Ordini

**Fornitore**:
Chi spedisce la merce al magazzino.

**Ordine fornitore**:
La merce chiesta a un fornitore e attesa in magazzino, divisa in righe con quantità ordinata, ricevuta e residua.
_Evitare_: ordine d'acquisto, ordine (da solo)

**Ordine cliente**:
La merce da consegnare a un cliente, divisa in righe; è aperto finché non è evaso.
_Evitare_: ordine di vendita, ordine (da solo)

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

**Ubicazione**:
Il punto del magazzino in cui sta la merce, come uno scaffale o una corsia; si usa solo se il magazzino lo sceglie.
_Evitare_: posizione, locazione

## Persone

**Operatore**:
Chi riceve, identifica, preleva e spedisce la merce.
_Evitare_: magazziniere, utente (da solo)

**Responsabile**:
Chi, oltre al lavoro dell'operatore, gestisce catalogo, rettifiche, annullamenti e utenti.
_Evitare_: amministratore, admin, capo magazzino
