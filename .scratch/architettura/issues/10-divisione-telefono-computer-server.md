# Divisione tra telefono, computer e server in sede

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sessione del 20/11/2026 con l'utente
Blocked by: 07 (chiuso). Non aspetta più la prova visiva (decisione 405).

## Question

Cosa gira sul telefono, cosa sul computer e cosa sul server in sede? Lettura di barcode, codice stampato e quantità;
ricerca tra le impronte; archivio delle foto; database; assegnazione. Come si conserva sul telefono l'operazione in
corso quando cade la rete (decisione 23)? Cosa viaggia in rete per ogni inquadratura?

Fuori da questo ticket (decisione 405): dove si calcolano le impronte (nel browser o sul server) e che macchina serve
in sede. Dipendono dai numeri della prova visiva e stanno nel ticket «Impronte e server in sede, dopo la prova».

Risultato atteso: la divisione in `docs/architettura.md`.

## Comments

- 16/11/2026, dal ticket «Percorso di identificazione»: un'inquadratura sola prova barcode, codice stampato e aspetto in
  fila (87); le foto confermate diventano foto di riferimento (96) e ogni identificazione si registra con il suo metodo
  (104). Va deciso dove gira ogni passo e cosa viaggia in rete per ogni inquadratura.
- 16/11/2026, dal ticket «App nativa o web app»: web app servita dal server in sede, su tutti i dispositivi (121, 122,
  126). Già deciso: il barcode si legge sul dispositivo (lettore di Chrome, libreria nella pagina o grilletto), il
  codice stampato sul server, con la foto che viaggia in rete interna (127). L'operazione in corso senza rete resta nella
  memoria del browser (127). Restano da decidere qui l'aspetto (impronte nel browser o sul server) e cosa viaggia per
  ogni inquadratura.
- 17/11/2026, dal ticket «Piano della prova di accuratezza visiva»: la prova misura i tempi solo nella sessione di
  Claude, per confrontare i modelli; computer e server aziendali non si usano finché non c'è una versione da provare, e
  l'utente potrà fare una prima misura sul suo computer fisso (143). I tempi della macchina vera e della rete vanno
  presi altrove: prove su dispositivi veri (127) e scelta del server.
- 20/11/2026: diviso in due (405); qui la parte che si decide senza i numeri della prova.
- 20/11/2026, giro 1 (pagina https://claude.ai/artifact/YbyLuy2kMFmVgEH5xdBPXu): accettate le consigliate, senza
  note (406–415): dati solo sul server; confronto dell'aspetto sul server; codice letto più foto a ogni inquadratura;
  scatto da solo; grilletto senza foto; schermi condivisi aggiornati da soli; altre foto 30 giorni; fascia «Senza rete»;
  operazione in attesa a nome di chi l'ha fatta; stampa dal browser.
- 20/11/2026, giro 2: accettate le consigliate, senza note (416–420): operazione che arriva tardi torna a chi l'ha
  fatta; fascia dopo 3 secondi; due messaggi (Wi-Fi o server); copie di sicurezza senza le foto dei 30 giorni; punto per
  la parte legale.
- 20/11/2026, riepilogo: confermato con le deduzioni (421).

## Answer

Chiuso il 20/11/2026 in due giri più il riepilogo, con la pagina https://claude.ai/artifact/YbyLuy2kMFmVgEH5xdBPXu
(copia in `prototipi/divisione/index.html`). Decisioni 406–421; specifica nella sezione «Divisione tra telefono,
computer e server in sede» di `docs/architettura.md`; termini nuovi in `GLOSSARY.md` (inquadratura, impronta,
operazione in attesa).

- Telefono e palmare: fotocamera, lettura del barcode, scatto da solo, operazioni in attesa senza rete; nessun dato a
  bordo (406, 409, 410, 413).
- Server in sede: database, assegnazione, significato del barcode, codice stampato e quantità scritta, elenco delle
  impronte e confronto, archivio delle foto, avvisi ai dispositivi aperti, scambi e lavori automatici (406–408, 411, 412).
- Computer: lo stesso browser; stampa dei PDF dal dispositivo (415).
- Per ogni inquadratura: codice letto più una foto ferma; di ritorno articolo, quantità, proposte, esito (408).
- Rete assente: fascia dopo 3 secondi con due messaggi; operazione a nome di chi l'ha fatta; se arriva tardi torna a
  lui (e al responsabile se il DDT è chiuso) (413, 414, 416–418).
- Foto: di riferimento finché il responsabile le toglie, bolle con il DDT, le altre 30 giorni e fuori dalle copie di
  sicurezza; un punto per la parte legale (412, 419, 420).
- Resta al ticket «Impronte e server in sede, dopo la prova»: dove si calcolano le impronte, programma del modello,
  macchina in sede (405).
