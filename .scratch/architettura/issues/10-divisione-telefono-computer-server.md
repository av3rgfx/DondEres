# Divisione tra telefono, computer e server in sede

Type: grilling
Label: wayfinder:grilling
Status: open
Blocked by: 07, 09

## Question

Cosa gira sul telefono, cosa sul computer e cosa sul server in sede? Lettura di barcode, codice stampato e quantità;
calcolo delle impronte e ricerca; archivio delle foto; database; assegnazione. Come si conserva sul telefono
l'operazione in corso quando cade la rete (decisione 23)? Che macchina serve in sede, alla luce dei tempi misurati
nella prova?

Risultato atteso: la divisione in `docs/architettura.md` e i requisiti minimi del server.

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
