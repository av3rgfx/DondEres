# Completezza del percorso delle schermate

Type: prototype
Label: wayfinder:prototype
Status: resolved
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
- 18/11/2026, inizio del ticket: analisi scritta in `docs/architettura.md` («Analisi del 18/11/2026: cosa manca alla
  base»), dalla ricerca `docs/research/2026-11-18-gestionali-magazzino-esistenti.md`. Primo giro di 8 domande nella
  pagina https://claude.ai/artifact/13EHJFJ3ZbM8QNXU1dTkag (privata): bolla del DDT, ripiego a mano, «riempi con
  l'atteso», cose in sospeso, vendita assistita a metà, chi vede i Documenti, Annulla e Conferma, merce danneggiata.
- 18/11/2026, primo giro: accettate tutte le consigliate, con due note (quantità in bolla, «Libera» di ARS divisa per
  marca o fornitore); decisioni 184–191. Prototipo aggiornato (stesso link privato
  https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur). Secondo giro di 9 domande nella stessa pagina delle domande.
- 18/11/2026, secondo giro: consigliate tranne la 198 (al prelievo il di più si accetta e va al responsabile); nota
  sulla lettura automatica della bolla (193). Decisioni 192–200. Terzo giro: riepilogo confermato (201).

## Answer

Chiuso il 18/11/2026 in tre giri, con la pagina https://claude.ai/artifact/13EHJFJ3ZbM8QNXU1dTkag (privata). Decisioni
184–201; specifica nella sezione «Percorso delle schermate» di `docs/architettura.md` (analisi, ricevimento, cose in
sospeso, Documenti, Annulla e Conferma, merce danneggiata, tempi, suoni e ricerca); prototipo
`prototipi/percorso-schermate/index.html` (anche https://claude.ai/artifact/Vb6ijyDdr4n2gsZcKhhVur, privata), provato
nel browser su tutti i flussi.

- DDT: fornitore, foto della bolla, numero e data letti da confermare; righe dalle letture; «Aggiungi a mano» per
  articolo o per ordine con il primo ordine proposto; niente «riempi con l'atteso»; alla chiusura riepilogo con
  quantità in bolla solo dove differisce e attesi non arrivati (184–186, 192, 201).
- Cose in sospeso in quattro gruppi in ogni sezione; vendita assistita a metà che resta e si ricontrolla (187, 188).
- «Documenti» per categoria e registro (tutto al responsabile, le proprie operazioni all'operatore), esportazione
  in file, niente cancellazioni automatiche (189, 199).
- Regola unica per «Annulla» e «Conferma» in quattro livelli; «Annulla» su ogni scheda (190, 201).
- Merce danneggiata al ricevimento e a scaffale (191); «Metti a posto» per fornitore e DDT (194); tempi 1 e 2 secondi
  (195); suono e vibrazione (196); «Cerca» sopra ogni lavoro (197); prelievo oltre il richiesto accettato (198).
- Nuovi ticket: «Resi», «Inventario periodico» (bloccano «Aspetto grafico») e la ricerca «Lettura automatica delle
  bolle» (193, 200). Domande 23–26 per il rivenditore. Termini nuovi in `GLOSSARY.md`: bolla, quantità in bolla, cose
  in sospeso, merce danneggiata, scarto, registro.

## Correzione dopo la chiusura

- 18/11/2026, sera: l'utente corregge la preparazione, guardando il prototipo da telefono («ho fatto un errore e mi
  sono spiegato male»). Se manca qualcosa, la preparazione si sospende (anche per giorni) o si conclude senza
  quell'articolo e si spedisce; il mancante parte appena arriva. Nel nuovo piano, un ordine con un articolo assente o
  con quantità superiore alla disponibilità dà un avviso che non blocca; il preparatore vede lo stesso avviso
  nell'anteprima dell'ordine, che aperto dice quale articolo non basta. I preparatori senza permessi non vedono «gli
  altri lavori». Tocca le decisioni 165, 170 e 177. Domande nella pagina privata
  https://claude.ai/artifact/Qft5i5wPiwfyYEQpdUz5Kq.
- 18/11/2026, primo giro della correzione: decisioni 246–250 (consigliate per 1–4; per la 5 l'utente nasconde solo
  «Altri lavori» e vuole una scelta per magazzino sul lavoro dei colleghi, che in UFP resta visibile). Nota dell'utente:
  cosa fa il preparatore se la merce c'è ma non risulta, o ce n'è meno. Prototipo corretto e provato nel browser.
  Secondo giro nella stessa pagina.
- 18/11/2026, secondo giro della correzione: accettate le consigliate (251–255); specifica scritta nella sezione
  «Percorso delle schermate» → «Preparazione e spedizione» e «Chi vede cosa». Domanda dell'utente alla 251 («basta
  aggiornare la giacenza?»): analisi e due domande nel terzo giro, con la riga a zero nel prelievo.
- 18/11/2026, terzo giro della correzione: accettate le due consigliate; nota dell'utente: aveva letto «ordine» come
  ordine al fornitore. Per il preparatore «Ne trovo di più/meno» è un passo solo e si torna alla riga a prelevare (256);
  righe che non risultano in fondo al prelievo (257). Deduzione nel prototipo, da confermare: un ordine senza nessun
  pezzo preso non diventa pronto. Pagina delle domande: https://claude.ai/artifact/Qft5i5wPiwfyYEQpdUz5Kq. Correzione
  chiusa (decisioni 246–257).
- 19/11/2026: nuove richieste dell'utente dopo la prova da telefono: giacenze per ubicazione e scelta dell'ubicazione
  al prelievo e nella vendita assistita (258, 259); «Aggiungi alla vendita» da «Cerca» (260). Prototipo aggiornato e
  provato nel browser.
- 19/11/2026: l'utente distingue due responsabili (di magazzino e dei piani di spedizione), con i diritti dati
  dall'account admin; gli avvisi della preparazione vanno al responsabile dei piani. Chiede «Disponibilità» al posto di
  «liberi» (261) e un'interfaccia pulita con poche parole (262). Tocca le decisioni 27, 169, 173 e 177. Domande nella
  pagina privata https://claude.ai/artifact/ScDtAoDaYsTP1K3b61x6MP.
