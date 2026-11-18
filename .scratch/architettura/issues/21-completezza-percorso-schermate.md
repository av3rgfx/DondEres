# Completezza del percorso delle schermate

Type: prototype
Label: wayfinder:prototype
Status: in corso
Assignee: sessione del 18/11/2026 con l'utente
Blocked by: 20

## Question

Il percorso deciso nel ticket «Percorso delle schermate» (decisioni 160–179) copre tutti i casi che succedono davvero in
magazzino? Dopo la ricerca sui gestionali esistenti, cosa si aggiunge e cosa si corregge (decisione 180)?

Da coprire di sicuro, su richiesta dell'utente:

- tasti «Annulla» e «Conferma» dove servono, con le conferme prima delle azioni che non si possono disfare;
- l'elenco delle cose in sospeso in ogni sezione: vendita assistita, ingresso merci, spedizioni e le altre (181);
- la sezione «Documenti»: storico di tutto ciò che è stato fatto, per categoria, con i log (182);
- il DDT creato scegliendo il fornitore, con le righe create dalle letture e abbinate agli ordini aperti; il ripiego a
  mano per articolo (tutti gli ordini che lo contengono) o per ordine (gli articoli dell'ordine); lo studio di soluzioni
  migliori (183);
- i casi reali che la ricerca mostra mancanti nella base.

Si prova con il prototipo `prototipi/percorso-schermate/index.html`, reso più completo (stati, conferme, errori, elenchi
vuoti e pieni) ma ancora senza aspetto grafico, che resta al ticket «Aspetto grafico» (14).

Risultato atteso: la sezione «Percorso delle schermate» di `docs/architettura.md` aggiornata, con il link al prototipo.

## Comments

- 18/11/2026, dalla prova del prototipo: l'utente lo trova giusto ma grezzo e teme che non copra tutte le dinamiche
  dell'azienda (180). L'utente può mandare un video di come si prepara oggi con ARS Logistica (nota alla 161): se
  mostra nomi di clienti o altri dati reali non entra nel repository; si annotano solo i fatti.
- Punto aperto dal ticket precedente: cosa succede nel programma alla merce di una vendita assistita che non parte
  subito (178).
