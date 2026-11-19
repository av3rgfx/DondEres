# Domande per il rivenditore di Ad Hoc Revolution e ARS Logistica (UFP)

Preparate il 15/11/2026 (decisione 57). Le manda l'utente; le risposte servono al connettore Ad Hoc della
specializzazione per UFP e vanno annotate qui sotto, con la data. Partono dalla ricerca
`docs/research/2026-11-15-adhoc-revolution-ars-logistica.md` (§7) e dalle decisioni 49–67.

Il testo qui sotto si può copiare in un'email. Non contiene dati dei clienti.

---

Buongiorno,

stiamo progettando un programma di magazzino per UFP: riceverà la merce, la identificherà dal telefono, la assegnerà
agli ordini dei clienti e registrerà prelievi, spedizioni e vendite al banco. In questo magazzino prenderà il posto di
ARS Logistica per il lavoro fisico, mentre Ad Hoc Revolution resterà il gestionale per articoli, ordini e documenti.
Per collegarlo ad Ad Hoc vi chiediamo:

**Installazione**

1. Quale versione di Ad Hoc è installata in UFP: Revolution client/server o Revolution Web? Su quale database e versione
   (SQL Server?), in sede o nel datacenter Zucchetti?
2. Quali moduli sono attivi: Magazzino, Ordini clienti/fornitori, ubicazioni, lotti e matricole, importazione dati?

**Come leggere e scrivere i dati**

3. C'è un'importazione ed esportazione documentata (tracciati) per articoli, ordini cliente, ordini fornitore e
   documenti di magazzino? È un modulo a pagamento? Quanto costa?
4. L'installazione di UFP offre servizi web? C'è documentazione? Serve una licenza?
5. Possiamo leggere il database con un utente in sola lettura, magari con viste dedicate? E scrivere? Cosa cambia per
   assistenza e aggiornamenti?
6. Ogni quanto si possono leggere le novità (ordini nuovi o cambiati) senza appesantire Ad Hoc? Noi pensavamo ogni 5
   minuti.

**Documenti e stati**

7. Quando la merce di un ordine cliente è prelevata e pronta, e quando esce dal magazzino, quali documenti si creano in
   Ad Hoc (documento intermedio, DDT, altro)? Quali causali si usano per carico, prelievo e rettifica?
8. Quando arriva una consegna, quale documento di carico si crea e come si collega al DDT del fornitore e alle righe
   degli ordini fornitore?
9. L'«OP» è il documento di vendita: in che rapporto sta con l'ordine cliente e con il DDT?
10. Gli ordini fornitore fatti per un cliente preciso riportano il riferimento del cliente: in quale campo di Ad Hoc
    sta, sull'ordine intero o su ogni riga?
11. Esistono magazzini logici in UFP? Ci servirebbe tenere da parte la merce già venduta che arriva per un cliente.

**Lavoro oggi fatto da ARS Logistica**

12. Come scrive oggi ARS in Ad Hoc (database, procedure di Ad Hoc, tabelle intermedie)? Possiamo scrivere nello stesso
    modo i nostri documenti di carico, di prelievo e di spedizione?
13. La vendita assistita al banco di ARS crea un ordine che compare da solo nelle vendite di Ad Hoc. Come lo crea?
    Possiamo creare questi ordini anche dal nostro programma?
14. Un articolo nuovo creato in Ad Hoc: in quanto tempo e con quale codice diventa leggibile dall'esterno?
15. Quali moduli di ARS sono attivi in UFP, e cosa comporterebbe smettere di usarli per ricevimento, prelievo,
    inventario e vendita al banco (contratti, licenze, dati)?
16. Che cos'è «NEX Logistica»? Sostituisce ARS Logistica?

**Articoli e prezzi** (aggiunte il 16/11/2026, dal ticket «Modello dei dati»)

17. Si possono leggere da Ad Hoc il prezzo di vendita e il costo d'acquisto di ogni articolo? Al banco il nostro
    programma mostrerà il prezzo, preso da Ad Hoc e mai cambiato da noi.
18. Ad Hoc tiene i codici con cui i fornitori chiamano i vostri articoli, e le conversioni tra le unità del fornitore e
    le vostre (per esempio tonnellate e chili, confezioni e pezzi)? Si possono leggere?

**Prove**

19. Si può avere un ambiente di prova (una ditta o una copia di test, senza dati reali dei clienti) per sviluppare il
    collegamento?

**Articoli non a catalogo**

20. Quando si ordina a un fornitore un articolo che non è a catalogo (per esempio per un cliente), come si scrive la
    riga sull'ordine fornitore in Ad Hoc: con un codice articolo nuovo, con un codice generico e la descrizione, o in un
    altro modo? Un articolo creato in Ad Hoc può avere anche il barcode o il codice del produttore, da leggere?

**Preparazione e spedizione** (aggiunte il 17/11/2026, dal ticket «Percorso delle schermate»)

21. Sull'ordine cliente in Ad Hoc ci sono l'agente che ha fatto la vendita e il corriere (o il vettore) con cui va
    spedito? Si possono leggere? Il nostro programma li userebbe per proporre il titolo del piano di spedizione e per
    mostrare al preparatore con quale corriere parte la merce.
22. Quando un ordine è preparato, oggi ARS restituisce ad Ad Hoc numero dei colli e peso? In quale documento?
23. Se il nostro programma manda una rettifica su un carico già fatturato, Ad Hoc la accetta? Cosa succede (blocco,
    nota di credito, rettifica di magazzino separata)?
24. Quando si rende merce al fornitore, chi emette il DDT di reso: Ad Hoc, ARS o un'altra persona? Il nostro programma
    dovrebbe mandare ad Ad Hoc un documento di reso già pronto?
    (Fatto del 18/11/2026: l'ufficio di UFP fa già il DDT di reso con Ad Hoc, causale «RESFO Reso a Fornitori» e
    dicitura «Reso per accredito», con il riferimento al DDT del fornitore. Resta da sapere se Ad Hoc può riceverlo
    già pronto dal nostro programma, e in che forma.)
25. Chi stampa oggi le etichette e la distinta di ritiro dei corrieri (BRT, GLS): ARS, Ad Hoc, il programma del
    corriere?
26. Ad Hoc riceve dai fornitori fatture elettroniche con i riferimenti ai DDT (blocco DatiDDT della fattura)? Si
    possono leggere, per confrontare la merce caricata con quella fatturata?
27. Quando un cliente rende merce, come la registra oggi Ad Hoc (documento di reso da cliente, carico, nota di
    credito)? Il nostro programma potrebbe mandare ad Ad Hoc un «reso da cliente» già pronto, con il riferimento
    all'ordine e alla vendita d'origine, da cui l'ufficio fa la nota di credito?

**Inventario** (aggiunta il 18/11/2026, dal ticket «Inventario periodico»)

28. Oggi l'inventario di fine anno si ricopia a mano in Ad Hoc. Il nostro programma potrebbe mandare ad Ad Hoc il
    risultato: meglio una rettifica per articolo ogni volta che il responsabile approva una differenza, oppure una
    rilevazione d'inventario unica, con la quantità contata di ogni articolo? Ad Hoc calcola da sé il valore
    dell'inventario (costo medio, ultimo costo o altro)?

**Vendita assistita** (aggiunta il 19/11/2026, dal ticket «Punti di estensione per la specializzazione»)

29. Dopo una vendita assistita la merce può restare in magazzino per giorni, per esempio un pacco sul pancale di un
    agente. In quale momento Ad Hoc scarica la giacenza: alla creazione dell'OP, al passaggio da OP a bolla al ritiro, o
    alla fattura? Il nostro programma può leggere quel passaggio (e quando, dopo quanto tempo)? Lo useremmo per
    registrare l'uscita della merce nello stesso momento.

Grazie.

---

## Risposte

<!-- data, chi ha risposto, risposta per numero -->

Nessuna risposta per ora.
