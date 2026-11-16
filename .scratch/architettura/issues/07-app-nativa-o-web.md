# App nativa o web app

Type: grilling
Label: wayfinder:grilling
Status: resolved
Blocked by: —

## Question

Per telefoni Android e iPhone e computer con telecamera (decisione 22), senza lavoro senza rete ma senza perdere
l'operazione in corso (decisione 23): app installata (nativa o multipiattaforma) o web app dal browser?

Da pesare, con la ricerca «Addestramento ed esecuzione locale» §H e «Modelli» §6: fotocamera e HTTPS sulla rete
interna, difetto noto sul permesso della fotocamera nelle web app installate su iPhone, lettura di barcode e testo
sul telefono (ML Kit, Apple Vision, `BarcodeDetector`, zxing-cpp), distribuzione e aggiornamenti in un magazzino
qualsiasi, telefoni aziendali o personali.

Risultato atteso: la scelta e il motivo in `docs/decisioni.md`, le conseguenze in `docs/architettura.md`.

## Comments

- 15/11/2026, dal ticket «Regole all'arrivo»: l'utente parla di conferma del prelievo «con il palmare». Da chiarire
  qui se il magazzino usa palmari industriali (lettore barcode integrato, spesso Android) oltre ai telefoni.
- 16/11/2026, chiusura: i palmari restano nella base (119); il lettore a grilletto si usa nel browser come tastiera,
  ipotesi da verificare sul modello di UFP.

## Answer

Chiuso il 16/11/2026 in due giri con l'utente (pagina delle domande: https://claude.ai/artifact/41KfvE3P7rhiPdEZLueyRw,
privata). Decisioni 119–127 in `docs/decisioni.md`; sezione «Dispositivi e forma del programma» in
`docs/architettura.md`; nuovi termini «Server in sede» e «Palmare» in `GLOSSARY.md`.

- **Web app** dal browser su telefoni, palmari e computer, servita dal server in sede; niente app da installare. Scelta
  dell'utente, diversa dalla proposta (app installata): accesso solo dalla rete interna del magazzino (121, 122).
- Dispositivi: Android, iPhone, palmari industriali Android con grilletto, computer; telefoni aziendali e personali
  (119, 120).
- Collegamento sicuro: certificato del dominio dell'azienda rinnovato dal server; certificato interno per chi non ha un
  dominio (123).
- iPhone da Safari con «Fotocamera: Consenti»; icona sulla Home solo dopo una prova (124).
- Aggiornamenti decisi dal responsabile; quelli importanti obbligatori, di notte, da soli (125).
- Server in sede obbligatorio; i magazzini senza server sono fuori dalla mappa (126).
- Deduzioni confermate (127): barcode sul dispositivo, codice stampato sul server, fotocamera spenta quando non serve,
  operazione in corso nel browser, QR per la prima apertura, una sola versione, prove su dispositivi veri.
