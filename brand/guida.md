# Ripo: guida del marchio

Una pagina per chi usa il marchio, anche senza essere un grafico. Decisioni in `docs/decisioni.md` (386, 388,
390, 391, 396 e 398–403). Tavola d'uso: `tavola.png` (pagina `tavola.html`).

## 1. Il marchio

- **Simbolo**: la R di Ripo. Asta e occhiello semplici, con il vuoto quasi tondo, e una gamba lunga dello stesso
  spessore che si posa diritta sulla base. È la firma del marchio. Si usa per le icone e per gli spazi quadrati.
- **Nome**: «Ripo», con la stessa R e le minuscole a peso medio. Si usa per testate, documenti ed etichette.
- Simbolo e nome **non si affiancano** (391): si usa l'uno o l'altro.
- Il nome «Ripo» è provvisorio (386). Se cambia, il simbolo resta, perché l'iniziale resta la R.

## 2. File

| Uso | File |
|---|---|
| Simbolo | `svg/ripo-simbolo-{nero,blu,bianco,blu-chiaro}.svg` |
| Simbolo a 16 pixel | `svg/ripo-simbolo-16.svg` (disegnato sulla griglia dei pixel; solo a 16) |
| Nome | `svg/ripo-nome-{nero,blu,bianco,blu-chiaro}.svg` |
| Web app | `icone/` con favicon, icone del telefono, manifest e le righe da mettere nell'`<head>` (`head-snippet.html`) |
| Prova di stampa | `prova-stampa.svg` (etichetta 100 x 70 mm, da stampare al 100 %) |

I file si rigenerano con `python3 brand/genera.py`. Non si ridisegnano a mano e il nome non si riscrive con un
carattere tipografico: le lettere sono disegnate.

## 3. Spazio libero

Intorno al simbolo e al nome lascia libero almeno lo spessore dell'asta della R, su tutti i lati. Lo spazio cresce
con il logo: niente misure fisse.

## 4. Misure minime

| | Schermo | Stampa |
|---|---|---|
| Simbolo | 16 px, con la R per i 16 pixel | 5 mm di altezza (proposta da provare, 403) |
| Nome | 72 px di larghezza | 15 mm di larghezza (proposta da provare, 403) |

Sotto queste misure i vuoti (l'occhiello della R, lo stacco tra il puntino e l'asta della i) rischiano di chiudersi.
Le misure di stampa vanno confermate con il foglio di prova su una stampante termica vera.

## 5. Colori

| Nome | HEX | RGB | Uso | Contrasto |
|---|---|---|---|---|
| Blu elettrico | #1F5BFF | 31 91 255 | marchio sul chiaro, fondo dell'icona | 5,3 a 1 sul bianco |
| Blu chiaro | #668FFF | 102 143 255 | marchio sul tema scuro | 6,2 sul #121212, 5,6 sul #1C1C1E |
| Nero | #000000 | 0 0 0 | stampe, etichette, documenti | |
| Bianco | #FFFFFF | 255 255 255 | sul blu e sul nero | |

CMYK e Pantone non servono ora: le stampe sono in bianco e nero (368). Il blu elettrico sul nero non va usato
(contrasto 3,6 a 1).

## 6. Fondi ammessi

- Nero o blu su bianco; bianco su blu o su nero; blu chiaro sul tema scuro.
- Icona dell'app: R bianca su blu elettrico (401).
- Su foto o fondi mossi, solo l'icona con il suo fondo blu.

## 7. Da non fare

- Deformare, ruotare, inclinare, cambiare le proporzioni.
- Aggiungere ombre, contorni, sfumature, effetti o un riquadro diverso da quello dell'icona.
- Usare altri colori, soprattutto rosso, verde e giallo: nel programma dicono errore, fatto e attenzione (367).
- Mettere simbolo e nome uno accanto all'altro (391).
- Usare la R per i 16 pixel a misure più grandi.

## 8. Cose ancora aperte

- Prova di stampa su una termica vera (403), con `prova-stampa.svg`: dire la misura più piccola che si legge.
- Ricerca dei marchi a livello europeo (EUIPO, TMview) dal consulente in marchi, prima del deposito e prima di offrire
  il programma ad altri (387).
