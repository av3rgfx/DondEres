# Loghi di una sola lettera: cosa dicono le fonti, per la R di Ripo

Data: 20/11/2026. Tutte le fonti citate sono state consultate il **20/11/2026**.

Legenda: **FATTO** = visto alla fonte linkata. **DEDUZIONE** = conclusione nostra a partire dai fatti. **IPOTESI** = da
verificare. **Non verificato** = fonte cercata ma non trovata, non raggiungibile o a pagamento.

Decisioni di riferimento in `docs/decisioni.md`: 386 (nome Ripo), 388 (blu elettrico #1F5BFF), 391 (simbolo e nome
separati), 393–395 (R con vuoto non rettangolare e gamba lunga e curva; piacciono «A · Pulito» e «C · Slitta»).

## Domanda

1. Come i progettisti rendono propri e riconoscibili i monogrammi e i loghi di una sola lettera (un dettaglio solo,
   spazio negativo, costruzione geometrica, legatura, taglio, peso) e quali errori evitano.
2. Esempi reali e documentati di loghi a lettera singola, soprattutto software, logistica e trasporti, e cosa li
   rende distinti.
3. Tendenze 2023–2026 nei loghi a lettera singola per prodotti software, e cosa sta diventando generico.
4. Indicazioni pratiche per una lettera con una gamba curva: equilibrio, peso ottico, evitare l'effetto svolazzo,
   leggibilità in piccolo (16 px, un colore, stampa termica).

## Metodo

- Ricerche web (motore di ricerca generale) sui marchi indicati nella domanda (Netflix, Pinterest, Beats, Monzo,
  Revolut, Rakuten) e su altri casi a lettera singola documentati dai progettisti (Google G, H di Hillary Clinton,
  MIT Technology Review, Urbint, Facebook f, FedEx).
- Pagine aperte e lette: comunicati e linee guida ufficiali (Revolut, Rakuten, Pinterest, Meta, Google Design,
  Apple), pagine di progetto di Pentagram, saggi e interviste dei progettisti (Michael Bierut, Lindon Leader, Juan
  Carlos Pagan, Jesse Cogswell di Monzo), i rapporti annuali sulle tendenze di LogoLounge (2024, 2025, 2026),
  articoli di commento sui loghi AI, documentazione tecnica (Zebra, Google Fonts, Evil Martians).
- I PDF delle linee guida di Revolut e Rakuten sono stati scaricati ed estratti in testo (`pdftotext`); le immagini
  non sono state viste.
- Brand New (UnderConsideration), fonte secondaria di riferimento: le schede trovate (Netflix, Rakuten, Path contro
  Pinterest) sono a pagamento; se ne citano solo titolo, data e tag visibili.
- Campione locale: il catalogo della skill logo-design (`.claude/skills/logo-design/assets/library/catalog.json`,
  1.432 loghi, in prevalenza di software) è stato contato con uno script. Non è un campione rappresentativo del
  mercato: serve solo come indizio.
- Studi indicati nella domanda e non trovati con casi pertinenti: Wolff Olins, DesignStudio, Collins, Order, Mucho
  (nessun caso a lettera singola trovato nelle ricerche fatte; non vuol dire che non esistano). Koto: trovati casi
  (Bolt, Amazon, Netflix con Beginners) ma nessuno a lettera singola leggibile alla fonte.

## Sintesi: 12 punti operativi per la nostra R

1. **Un dettaglio solo, e deve essere la gamba.** Nei casi documentati la lettera è neutra e un unico elemento fa il
   lavoro: la freccia della H di Clinton, lo spillo nella P di Pinterest, il taglio a 45° della T di MIT Technology
   Review, il puntino della u di Urbint. Per Ripo asta e occhiello vanno tenuti semplici e geometrici; la firma è la
   gamba lunga e curva. Niente secondo dettaglio (tagli, punte, sfumature) in concorrenza. (DEDUZIONE da FATTI, §1)
2. **Il dettaglio nasce dalla geometria della lettera, non si aggiunge.** Bierut descrive la freccia come nata dalla
   geometria della H. Leader spiega di aver ridisegnato le lettere di FedEx per non «torturarle». LogoLounge 2026
   scrive che le iniziali con la coda annodata sono un «gioco rischioso» e che riescono quelle che condividono la
   struttura del resto del marchio. Per la R: l'arco della gamba dovrebbe derivare da un raggio o da un centro
   dell'occhiello, e avere lo stesso spessore dell'asta. (DEDUZIONE, §1 e §4)
3. **Spessore uniforme e fine netta tengono la gamba nella struttura.** Una gamba che si assottiglia o finisce a
   punta somiglia a un gesto calligrafico. Una gamba di spessore costante, con il piede tagliato sulla base, somiglia
   a un pezzo costruito. Questo va a favore di «A · Pulito». «C · Slitta» è più riconoscibile, ma la punta che
   risale è un secondo evento da verificare a 16 px. (DEDUZIONE; coerente con la scelta dell'utente che ha scartato
   «B · Affusolato», decisione 395)
4. **Pieno e pesante per le piccole dimensioni.** Google dà alla G compatta più peso della G del logotipo proprio per
   reggere le piccole dimensioni. Corregge anche otticamente il punto in cui il cerchio incontra la traversa (FATTO,
   §2). Per la R servono un'asta robusta, un vuoto dell'occhiello non troppo piccolo e una fessura tra gamba e asta
   che non si chiuda. (DEDUZIONE)
5. **Una versione apposta per 16 px.** Evil Martians consiglia di chiedere al progettista una versione speciale del
   logo per le griglie di pixel piccole, se la 32×32 ridotta si impasta (FATTO, §4). Per Ripo servono una R di
   riferimento e una R per 16 px, con vuoti allargati e gamba un po' più corta. Le due devono restare la stessa
   lettera. (DEDUZIONE)
6. **Misure minime in punti di stampa.** Una stampante termica a 203 dpi ha punti da 0,125 mm (8 punti per mm)
   (FATTO, §4). Rakuten fissa per il simbolo un minimo di 10 px a schermo e 3 mm in stampa. Revolut fissa per il
   logotipo 25 mm o 80 px (FATTI, §2). Per Ripo conviene fissare una larghezza minima di stampa. Ogni vuoto della R
   deve misurare almeno 2–3 punti a quella misura, cioè 0,25–0,4 mm. (IPOTESI da provare con una stampa vera)
7. **Progettare prima in nero pieno, senza effetti.** Le linee guida di Revolut e Rakuten vietano contorni,
   sfumature, ombre ed effetti. Rakuten prevede una versione nera per la stampa monocromatica. Apple chiede icone con
   variante mono e scrive che linee sottili e dettagli piccoli non ricevono gli effetti di sistema (FATTI, §2 e §3).
   Il blu #1F5BFF si applica dopo: la R deve funzionare in nero su una ricevuta. (DEDUZIONE)
8. **Il contenitore non distingue.** Su iOS il sistema applica a tutte le icone lo stesso quadrato arrotondato
   (FATTO, Apple). Nel campione della skill, «lettera dentro una forma» è la tecnica più frequente tra le lettere
   singole e il blu è il colore più frequente (FATTO, conteggio locale). La riconoscibilità deve stare nella sagoma
   della R, da provare anche senza fondo. (DEDUZIONE)
9. **R e blu è un territorio già frequentato: confrontarsi con Revolut.** Revolut usa la stessa R del logotipo come
   icona dell'app e ha nella palette un «Deep Blue» #1326FD (FATTO, §2). Il nostro #1F5BFF è un blu visibilmente
   diverso (ΔE76 ≈ 33, calcolo nostro), ma un'R geometrica piena in blu resta vicina. Servono un confronto affiancato
   con Revolut, Rakuten e le R del campione (Remix, Riot, Rax…) e una gamba che le separi nettamente. (DEDUZIONE)
10. **Evitare le mode che invecchiano.** LogoLounge segnala come abusati o in saturazione l'asterisco, le stelle a
    quattro punte per l'AI, le L monogramma con il ricciolo e le code annodate. I commentatori segnalano i cerchi
    con sfumatura dei loghi AI (FATTI, §3). Le «gambe lunghe» (LongLegs) sono una tendenza del 2025: la nostra gamba
    è di moda, quindi deve essere strutturale, non decorativa, per non datarsi. (DEDUZIONE)
11. **Riusare la curva nel sistema, con misura.** La R del simbolo e quella del nome dovrebbero essere la stessa,
    come in Revolut. Il segno firma può tornare in altri elementi, come il taglio a 45° di MIT Technology Review
    nell'impaginazione o la K di Kiln ripresa nella n. Per Ripo: la stessa R nel nome, e l'arco della gamba come
    possibile motivo, senza ripeterlo ovunque. (DEDUZIONE da FATTI, §1 e §2)
12. **Decidere e poi tenere.** Bierut racconta le critiche iniziali alla H e la loro successiva inversione. Monzo ha
    scelto un nome nuovo che iniziasse con la M pur di tenere la lettera, e la chiama la «porta d'ingresso» del
    prodotto. Facebook cambia la f in modo minimo per non perdere il patrimonio (FATTI, §1 e §2). Una lettera singola
    diventa riconoscibile con l'esposizione: dopo i test, meglio non rifarla a ogni giro. (DEDUZIONE)

## 1. Come si rende propria una lettera singola, ed errori da evitare

**Un dettaglio che porta il significato**

- FATTO. Michael Bierut, nel saggio «I'm With Her» (Design Observer, 28/03/2017), scrive che tra decine di simboli
  il preferito fu «the simplest of all: a perfectly square H». Aggiunge che la semplicità era ingannevole, perché la
  H era «a window, capable of endless transformations». La freccia nasce dalla geometria della lettera e punta in
  avanti. Racconta anche gli attacchi iniziali («I held my tongue»).
  https://designobserver.com/feature/im-with-her/39523
- FATTO. Kottke.org (31/03/2017) riporta dallo stesso saggio che Bierut voleva un segno semplice «as a peace sign or
  a smiley face», che «a five-year-old could make with construction paper». Il saggio originale datato è quello di
  Design Observer qui sopra. https://kottke.org/17/03/im-with-her-designing-hillary-clintons-campaign-identity
- FATTO. Pentagram, MIT Technology Review: il nuovo simbolo è un monogramma con un taglio a 45 gradi nella T che
  forma una r minuscola. Lo stesso angolo ritaglia gli angoli delle immagini e organizza la tipografia della rivista.
  Il partner indicato è Michael Bierut. https://pentagram.com/work/mit-technology-review/story
- FATTO. Pentagram, Urbint: il logomark aggiunge un puntino al braccio destro della u per farne una i («urban
  intelligence»). Il puntino è fatto di cerchi concentrici, può cambiare per suggerire funzioni come la scansione e si
  usa da solo per i sotto-marchi. https://pentagram.com/work/urbint/story
- FATTO, intervista non di prima mano: Juan Carlos Pagan, intervistato da Aspire Metro (24/07/2017), racconta che per
  Pinterest la P doveva essere di quel rosso intenso e richiamare lo spillo da mappa in fondo alla lettera.
  https://aspiremetro.com/dinner-guest-brand-identity-guru/

**Spazio negativo**

- FATTO. Lindon Leader, autore del logo FedEx da Landor, intervistato da The Sneeze (16/11/2004): la freccia è «a
  hidden bonus»; «either you see it or you don't», ma chi la vede non la dimentica. Le lettere sono state
  ricostruite per far stare la freccia senza «torturing the beautifully crafted letterforms». La freccia in sé è
  «one of the most mundane graphic devices»; «Punch lines that need to be explained are neither funny nor
  memorable». https://thesneeze.com/the-man-behind-the-fedex-logo/

**Costruzione e correzione ottica**

- FATTO. Google Design, «Evolving the Google identity» (pagina senza data né autori visibili): la G compatta è
  disegnata sulla stessa griglia delle icone di prodotto. Il cerchio è stato «optically refined to prevent a visual
  'overbite'» nel punto in cui incontra la traversa. Ha più peso per «stand up at small sizes».
  https://design.google/library/evolving-google-identity
- FATTO. Meta, «Redefining Facebook's brand identity» (Tagu Kato, 20/09/2023): la f è stata ridisegnata con
  «subtle, but significant changes» per un equilibrio ottico con senso di movimento in avanti. Il blu è più deciso
  per un contrasto maggiore. L'obiettivo era restare «familiar, yet dynamic».
  https://www.meta.com/design-at-meta/blog/redefining-facebooks-brand-identity/

**Errori evitati, come li scrivono le linee guida**

- FATTO. Linee guida di Revolut (PDF «Rebrand revolut guidelines», senza data visibile): non accostare logotipo e
  icona, non ruotare, non usare colori diversi da Revolut Black o White, non fare contorni, non deformare, non
  aggiungere elementi, sfumature o effetti (ombra, bagliore), non ritagliare, non comporre «Revolut» con altri
  caratteri. https://developer.revolut.com/assets/oba/Revolut-Open-Banking-guidelines.pdf
- FATTO. Rakuten Brand Guidelines (v2.0, maggio 2024), sezione Symbol: non usare il simbolo vecchio né disegnare
  immagini simili, non mescolare i colori di marca, non fare contorni, non ruotare, non applicare effetti né colori
  non previsti, non usarlo come elemento grafico; l'uso del simbolo da solo è vietato.
  https://global.rakuten.com/corp/news/assets/pdf/media/RakutenBrandGuidelines_en.pdf
- FATTO. Linee guida di Pinterest: non contornare, non aggiungere filtri o effetti, non togliere la P dal cerchio,
  non cambiare colore; se i colori sono limitati il logo può essere nero o bianco.
  https://business.pinterest.com/en-in/brand-guidelines/

**Lettura dalla skill del progetto**

- FATTO, fonte interna e non indipendente: la skill logo-design scrive che molte marche condividono la stessa
  iniziale e che il concetto deve vivere nel trattamento: una lettera che è anche una freccia, un percorso, una
  piega, una scintilla, una parentesi, un contenitore (`.claude/skills/logo-design/references/mark-types.md`, §4).
  La K di Kiln è un esempio dimostrativo della skill (marca fittizia, «Small-batch roasters», in
  `scripts/presentation_board.py`), non un logo reale documentato.

## 2. Esempi reali documentati

| Marca | Cosa è documentato alla fonte | Cosa la distingue | Fonte |
|---|---|---|---|
| **Revolut (R)** | FATTO: «The same 'R' from the wordmark is used for the app icon». Lo spazio di rispetto si misura sulla larghezza della R. Minimo del logo: 25 mm / 80 px. Logo solo nero o bianco. Colori primari: bianco, nero, Deep Blue #1326FD (Pantone 2935 C), Mid Blue #6FA0FF. | Una sola R per icona e logotipo; colore nel sistema, non nel logo. | https://developer.revolut.com/assets/oba/Revolut-Open-Banking-guidelines.pdf |
| Revolut (aggiornamento) | FATTO, stampa secondaria: Tabletowo (20/03/2020) scrive che Revolut ha rinnovato dopo cinque anni il logo e la sua «R» caratteristica. Il comunicato Revolut 10 non si apre (HTTP 403). | — | https://www.tabletowo.pl/revolut-nowe-logo-i-wizerunki-na-kartach |
| **Rakuten** | FATTO: nel 2018 un nuovo simbolo, che riprende l'elemento «uno» (*ichi*) del logo, sostituisce il «Circle R» su app e servizi. Comunicato del settembre 2018: il testo dice «September 8, 2017», data che sembra un refuso. Linee guida 2024: simbolo minimo 10 px digitale e 3 mm in stampa, versione nera per la stampa monocromatica, contrasto ≥ 3:1. Brand New ne ha una scheda (06/08/2018, tag *red*, *underline*), a pagamento. | Un tratto («uno») che fa da firma comune a 70+ servizi. | https://global.rakuten.com/corp/news/press/2018/0908_01.html · https://global.rakuten.com/corp/news/press/2018/0626_01.html · https://global.rakuten.com/corp/news/assets/pdf/media/RakutenBrandGuidelines_en.pdf · https://www.underconsideration.com/brandnew/archives/new_logo_for_rakuten.php |
| **Netflix (N)** | FATTO: It's Nice That (29/06/2016) cita Netflix: «We are introducing a new element into our branding with an N icon». Il logotipo resta; l'icona serve per app e social. Il progettista non è indicato. Brand New: «New Icon for Netflix» (27/06/2016, tag *monogram*, *ribbon*), a pagamento. | Il nastro piegato. Le facce in ombra non vanno bene per noi (un colore, stampa termica). | https://www.itsnicethat.com/news/netflix-new-icon-290616 · https://www.underconsideration.com/brandnew/archives/new_icon_for_netflix.php |
| **Pinterest (P)** | FATTO: logo principale «P» corsiva bianca in un cerchio rosso; nero o bianco se i colori sono limitati. Pagan: la P richiama lo spillo. Brand New ha un post del 09/09/2013 dal titolo «Path vs. Pinterest "P" Fight», testo a pagamento. | Un dettaglio con significato (lo spillo) nella parte bassa della lettera. | https://business.pinterest.com/en-in/brand-guidelines/ · https://aspiremetro.com/dinner-guest-brand-identity-guru/ · https://www.underconsideration.com/brandnew/archives/path_vs_pinterest_p_fight.php |
| **Monzo (M)** | FATTO: «The Monzo M has always been the recognisable front door to our product» (Jesse Cogswell, senior brand designer, 17/10/2022). Nel 2016 il nuovo nome doveva iniziare con M per tenere il logo; il capo del design generò con uno script oltre 4.000 versioni. | La lettera conta più del nome: si è cambiato il nome per tenerla. | https://community.monzo.com/t/we-ve-given-our-visual-brand-a-refresh-q-a-w-jesse-senior-brand-designer/139681 · https://monzo.com/blog/2016/08/26/how-we-picked-monzo |
| **Google (G)** | Vedi §1: più peso per le piccole dimensioni, correzione ottica, griglia delle icone. | Colori in sequenza; la geometria è comune, la correzione no. | https://design.google/library/evolving-google-identity |
| **Facebook (f)** | Vedi §1: cambiamenti minimi, contrasto maggiore. | Continuità più che novità. | https://www.meta.com/design-at-meta/blog/redefining-facebooks-brand-identity/ |
| **MIT Technology Review (T/r)** | Vedi §1: un taglio a 45° che diventa sistema. | Un taglio solo, riusato nell'impaginazione. | https://pentagram.com/work/mit-technology-review/story |

**Trasporti e logistica.** FATTO: FedEx (sopra) è il caso classico dello spazio negativo, ma è un logotipo, non una
lettera singola. Non abbiamo trovato alla fonte nessun caso documentato di logo a lettera singola nella logistica o nei
trasporti. Le ricerche hanno restituito soprattutto lavori da portfolio non verificabili (Contra, Behance) e casi non
a lettera (Steam Logistics di Whiteboard; Amazon rinnovata da Koto, letto solo nei risultati di ricerca).

**Beats (b).** Non verificato. L'attribuzione a Robert Brunner (Ammunition) compare solo in un articolo di Business
Insider letto nei risultati di ricerca. Nessuna fonte primaria trovata sul perché della b minuscola.

**DEDUZIONE.** Il caso più vicino a Ripo per forma e colore è Revolut: R, prodotto digitale, blu nella palette, la
stessa R per icona e nome. Il caso più vicino per metodo è MIT Technology Review: un solo intervento geometrico
sulla lettera, riusato nel sistema.

## 3. Tendenze 2023–2026 e cosa sta diventando generico

**LogoLounge (Bill Gardner), il rapporto annuale più citato.** Si dichiara descrittivo, non prescrittivo.

- FATTO, rapporto 2024 (15/07/2024): l'asterisco è «so ubiquitously utilized» da essere un abuso ricorrente. Anche
  faccine sorridenti, adesivi e frecce sono diventati molto comuni. Le stelle a quattro punte sono il simbolo più
  vicino all'AI, che «has yet to settle into a final form». Altre voci: Corner Chop (angoli asportati alle lettere);
  la g minuscola molto sfruttata. https://www.logolounge.com/trend/2024-logo-trend-report
- FATTO, rapporto 2025 (16/06/2025): LongLegs, cioè lettere allungate che portano il peso del marchio (esempio: il
  monogramma MAM di Paula Scher per il Memphis Art Museum); Typemelts (lettere fuse) definito «a quick visual flex»;
  Smokies (terminali arrotondati); Sharps (tagli profondi, possibili perché nel digitale i limiti di stampa
  «vanish»); «ultra-chroma hues» per i piccoli schermi; il movimento come identificatore primario.
  https://www.logolounge.com/trend/2025-logo-trend-report
- FATTO, rapporto 2026 (05/06/2026): Slip Knots, cioè iniziali con la coda annodata, è definito un gioco rischioso;
  riescono le versioni che condividono il DNA strutturale del marchio. Le L monogramma corsive con il ricciolo sono
  diventate una convenzione in saturazione. Faders: l'AI vista dall'interno, con cerchi o esagoni, monolinea e
  sfumature, «less a surprise» e più un arrivo atteso. https://www.logolounge.com/trend/2026-logo-trend-report

**Commenti dei progettisti sull'omologazione**

- FATTO. Radek Sienkiewicz (VelvetShark, 10/04/2025): lo schema ricorrente dei loghi AI è forma circolare spesso
  sfumata, apertura centrale, elementi irradiati, curve morbide. Suggerisce angoli netti, spazio negativo, niente
  simmetria radiale né sfumature. https://velvetshark.com/ai-company-logos-that-look-like-buttholes
- FATTO. Jim Nielsen (06/06/2025): la somiglianza riflette il timore di distinguersi; riprende «tech folks are afraid
  to stand out too much». https://blog.jim-nielsen.com/2025/visual-design-homogeneity-at-scale/
- FATTO. Creative Bloq (Natalie Fear, 22/03/2025): «Corporate conformity has taken over». Il resto del testo non è
  stato letto (pagina troncata).
  https://www.creativebloq.com/design/logos-icons/why-do-all-ai-company-logos-look-the-same
- FATTO, più vecchio del periodo richiesto: OH no Type Company, «Everybody fall in line» (19/09/2018), sui wordmark
  tech tutti con gli stessi sans-serif; «now is a great time to stand out». https://ohnotype.co/blog/everybody-fall-in-line

**Piattaforma**

- FATTO. Apple HIG, App icons: su iOS, iPadOS e macOS il sistema applica a tutte le icone una maschera con angoli
  arrotondati. Le icone hanno varianti predefinita, scura e mono. Gli effetti Liquid Glass vanno sulle forme
  grandi e semplici, non sui dettagli piccoli come testo e linee sottili. «Embrace simplicity»: un concetto espresso
  «with a minimal number of shapes». La prima lettera del nome è ammessa come mnemonico.
  https://developer.apple.com/design/human-interface-guidelines/app-icons

**Campione locale (indizio, non statistica di mercato)**

- FATTO, conteggio nostro sul catalogo della skill (1.432 loghi): 218 sono lettere singole («letterform»). Di
  queste, 89 usano il contenimento in una forma (41%), 71 lo spazio negativo, 39 la costruzione geometrica. Il blu è
  il colore principale più frequente (59, 27%). Le R singole trovate dalla descrizione sono circa 10, tutte di
  strumenti per sviluppatori (per esempio Remix, Riot, Rax, Rust, Redsmin, Rollup).

**Cosa sta diventando generico (DEDUZIONE).** Nessuna fonte usa l'espressione esatta «lettera geometrica in un
quadrato arrotondato blu». Ci si arriva mettendo insieme quattro fatti: il contenitore arrotondato è imposto a tutti
da iOS; nel campione contenimento e blu sono i casi più frequenti; i commentatori segnalano la convergenza verso
forme sicure; LogoLounge registra la saturazione di singoli trucchi (asterisco, stella AI, L con ricciolo). La parte
che non distingue è il contenitore con il colore. Resta distintiva una sagoma di lettera riconoscibile anche nera
e senza fondo.

## 4. Gamba curva: equilibrio, peso ottico, leggibilità in piccolo

**Fonti trovate (poche e generali)**

- FATTO. Google Fonts Knowledge, glossario: overshoot è «the part of a letterform that extends above or below the
  vertical dimensions of flatter glyphs». L'ink trap è «an intentional negative space built into letterforms to
  literally trap ink at certain intersections». Letta solo la descrizione della pagina; il resto è caricato via
  script. https://fonts.google.com/knowledge/glossary/overshoot · https://fonts.google.com/knowledge/glossary/ink_trap
- FATTO. Stuart de Rozario (Fontsmith), sul carattere geometrico FS Lucas (MyFonts, senza data visibile): un cerchio
  accanto a un quadrato della stessa misura «appears smaller», quindi va ingrandito (overshoot). «Perfect circles do
  not make very nice looking 'O's». Le orizzontali vanno un po' più sottili delle verticali, perché un tratto
  orizzontale ottenuto ruotando l'asta «clearly looks heavier».
  https://www.myfonts.com/a/font/content/optical-illusions-and-eye-trickery-in-geometric-font-design
- FATTO. Google, G compatta: correzione dell'«overbite» dove la curva incontra la traversa; più peso per le piccole
  dimensioni (§1).
- FATTO. Evil Martians, «How to Favicon» (Andrey Sitnik, aggiornato al 21/01/2026): se l'icona si impasta a 16×16,
  chiedere al progettista «a special version of the logo» per le griglie piccole, o un livello 16×16 nel file ICO.
  L'SVG può cambiare colore nel tema scuro con `prefers-color-scheme`.
  https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs
- FATTO. Zebra, specifiche di stampa (ZT510): 203 dpi = 8 punti/mm, punto nominale 0,125 × 0,125 mm; 300 dpi = 12
  punti/mm. https://docs.zebra.com/us/en/printers/industrial/zt510-ug/print-specifications.html
- Non verificato: un testo di un progettista di caratteri sul raccordo tra occhiello e gamba della R. La pagina
  trovata che ne parla è di bassa qualità e non è stata usata. Neanche l'attribuzione a Terrance Weinzierl (Monotype)
  dell'idea che la R sia la lettera più rivelatrice di un carattere è stata trovata alla fonte originale.

**Indicazioni per la nostra R (DEDUZIONI dalle fonti sopra, da provare a schermo e in stampa)**

- **Equilibrio.** La gamba lunga sposta il peso a destra e in basso. Per bilanciarla, l'occhiello può essere
  leggermente più stretto della gamba stesa, e l'asta deve restare verticale e piena: è l'ancora visiva. La lettera
  va giudicata dal suo baricentro, non dalla gabbia: la R non deve sembrare inclinata in avanti.
- **Peso ottico della curva.** Dove l'arco della gamba è quasi orizzontale va un po' assottigliato, come le
  orizzontali della O (de Rozario). Dove tocca la base deve scendere appena sotto la linea (overshoot), altrimenti
  sembra sollevato rispetto al piede dell'asta.
- **Raccordo gamba–occhiello.** Il raccordo è il punto più a rischio di macchia a 16 px e in stampa termica, perché
  due masse si toccano. Ci sono due strade: staccare la gamba dall'occhiello con una fessura netta, oppure ridurre lo
  spessore nel punto di contatto, con un piccolo scavo simile a un ink trap.
- **Contro l'effetto svolazzo.** Spessore costante, nessuna punta, un terminale tagliato orizzontale o verticale e
  un arco ricavato da un raggio già presente nella lettera. Una sola curva, senza flessi. Con la «Slitta», la punta
  che risale deve restare corta e tozza: lunga e sottile diventa un ricciolo.
- **In piccolo.** Disegnare la variante a 16 px sulla griglia di pixel, con vuoti di almeno 2 px. In stampa a 203
  dpi, ogni fessura deve misurare almeno 2–3 punti (0,25–0,4 mm) alla misura minima scelta. Il test va fatto in nero
  pieno, rovesciato (bianco su nero) e su una vera stampante termica.
- **Prova di confronto.** Affiancare la R a 16, 24 e 32 px alle icone di Revolut e Rakuten e alle R del campione
  della skill, in nero. Se la si riconosce solo dal colore, la sagoma non basta.

## Cosa non è stato verificato

- **Brand New**: le schede su Netflix (2016 e Koto 2023), Rakuten (2018) e «Path vs. Pinterest "P" Fight» (2013)
  sono a pagamento; letti solo titolo, data e tag.
- **Revolut**: il comunicato «Revolut 10» (2023) risponde HTTP 403. La data del PDF delle linee guida non è
  visibile. Come cambiò la forma della R nel 2020 o nel 2023 non è descritto nei testi letti. Le immagini non sono
  state viste.
- **Rakuten**: la forma del simbolo attuale non è descritta a parole nelle linee guida; non sappiamo se sia una R.
  Il post «Speed and Unity» di Mickey Mikitani (rakuten.today) risponde HTTP 503.
- **Netflix**: progettista dell'icona N del 2016 non confermato alla fonte. Gretel è citata solo da siti secondari.
  Il caso Koto e Beginners (2023) non è stato letto.
- **Beats**: nessuna fonte primaria sul logo b.
- **Monzo**: il post del 2015 «Making our mark» risponde HTTP 404.
- **Pinterest**: l'intervista a Pagan è su un sito secondario; quella originale di Creativity Online non è stata
  trovata.
- **Medium**, **Amazon/Koto**, **Bolt/Koto**: visti solo nei risultati di ricerca, non letti; non usati.
- **Wolff Olins, DesignStudio, Collins, Order, Mucho**: nessun caso a lettera singola trovato. La ricerca non è
  stata esaustiva.
- **Google Fonts, Material Design, Apple HIG**: pagine caricate via script. Di Google Fonts è letta solo la
  descrizione; Material non letto; Apple letto tramite il JSON pubblico della documentazione.
- **Misure minime per Ripo** (2–3 punti di stampa, 2 px a 16 px): sono IPOTESI nostre, da confermare con prove reali.
- **Somiglianza con marchi registrati**: questa ricerca non sostituisce una ricerca di anteriorità sui marchi
  figurativi (per esempio in TMview per classi 9 e 42); resta da fare prima del deposito.
