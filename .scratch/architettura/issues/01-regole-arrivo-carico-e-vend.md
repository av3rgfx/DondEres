# Regole all'arrivo: carico normale e merce venduta (VEND)

Type: grilling
Label: wayfinder:grilling
Status: claimed
Blocked by: —

## Question

Come funzionano, nella base, le due regole all'arrivo della decisione 15?

- **Carico normale**: la merce entra in giacenza, scala il residuo dell'ordine fornitore e poi si assegna agli
  ordini cliente dal più vecchio (decisione 16).
- **Merce venduta, con la giacenza «VEND»**: la merce che arriva va subito a un ordine cliente.

Da chiarire con esempi numerici:

- Nella merce venduta, come si sa a quale ordine cliente va il pezzo arrivato? Esiste un legame tra la riga
  d'ordine cliente e l'ordine fornitore? Cosa vuol dire «l'ultimo ordine effettuato su quel fornitore»?
- «VEND» è una giacenza separata o un'assegnazione con un nome proprio? Quando la merce esce da VEND?
- Le due regole convivono nello stesso magazzino? Chi decide quale si applica: l'articolo, l'ordine, il fornitore o
  una scelta di configurazione?
- Cosa succede se arriva più merce di quella venduta, o meno? E se arriva merce senza ordine fornitore?
- Le due regole stanno entrambe nella base, come configurazione, oppure la merce venduta è un'estensione?
- Quale dei due magazzini reali usa quale regola (informazione, non decisione)?

Risultato atteso: le regole di ricevimento e di assegnazione in `docs/architettura.md` e i termini nuovi (VEND,
carico, residuo) in `GLOSSARY.md`.
