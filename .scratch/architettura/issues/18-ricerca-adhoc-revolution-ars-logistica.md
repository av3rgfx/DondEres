# Ad Hoc Revolution e ARS Logistica: come si scambiano i dati

Type: research
Label: wayfinder:research
Status: resolved
Blocked by: —

## Question

Quali interfacce di scambio offrono Ad Hoc Revolution e ARS Logistica, i due gestionali che il primo magazzino usa
già (informazione dell'utente del 15/11/2026)? Il nostro prodotto dovrà importarne gli ordini (cliente e fornitore)
e gli articoli, e restituire i movimenti di magazzino (decisione 19).

- Chi produce i due programmi, che cosa fa ciascuno (gestionale, logistica di magazzino), e come si dividono di solito
  il lavoro quando convivono.
- Interfacce documentate: API, servizi web, file di scambio (CSV, XML, tracciati fissi), accesso al database,
  moduli di integrazione con magazzini automatici o terminali portatili.
- Cosa serve per usarle: moduli a pagamento, licenze, accesso concesso dal rivenditore.
- Concetti dei due programmi che si sovrappongono al nostro glossario (articolo, ordine, evasione, giacenza, ubicazione).

Risultato atteso: un file in `docs/research/`, con link alle fonti primarie (documentazione dei produttori). Dove le
fonti pubbliche non bastano, dirlo e indicare cosa chiedere al rivenditore.

## Answer

Ricerca completa in
[`docs/research/2026-11-15-adhoc-revolution-ars-logistica.md`](../../../docs/research/2026-11-15-adhoc-revolution-ars-logistica.md),
con le 10 domande da fare al rivenditore (§7). In sintesi:

- **Chi li produce.** Ad Hoc Revolution è di Zucchetti S.p.A., in versione client/server e in versione Web (sulla
  piattaforma Infinity). ARS Logistica (anche «ARS@Logistica») è di Datalite S.r.l., partner Zucchetti nato nel 2022
  dalla fusione di Altaquota e PC System.
- **Divisione del lavoro.** Ad Hoc tiene articoli, ordini e documenti. ARS fa già ricevimento, spostamenti, prelievo
  e inventario da telefono, e scrive direttamente in Ad Hoc.
- **Interfacce.** Per nessuno dei due ci sono API, tracciati o schemi del database pubblici. Zucchetti dichiara solo
  che si possono importare archivi, movimenti e documenti. I servizi web forse esistono solo sulla versione Web (non
  verificato). Il database di Ad Hoc è SQL Server, ma lo dice una fonte secondaria. Per ARS, nella pratica, un
  collegamento è uno sviluppo su misura di Datalite.
- **Costi.** Nessun prezzo pubblico; tutto dipende dai moduli attivati e passa dal rivenditore.
- **Rischio da decidere in
  [Fonti degli ordini e collegamento ai gestionali esistenti](02-fonti-ordini-e-collegamenti.md).** ARS e il nostro
  prodotto fanno in parte lo stesso lavoro: senza una divisione chiara, la stessa merce viene registrata due volte in
  Ad Hoc.
- **Falso amico.** «Evadere» in Ad Hoc e in ARS vuol dire probabilmente emettere un documento (DDT o intermedio);
  nel nostro glossario «evaso» vuol dire merce prelevata e pronta.
- **Per la base** (deduzioni della ricerca, da decidere nei ticket 02 e 11): connettore separato; scambio a file come
  via valida per qualsiasi gestionale; codice d'origine su ogni dato importato; tabelle di corrispondenza
  configurabili per causali e stati.
