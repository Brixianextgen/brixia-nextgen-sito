---
description: Mette in vetrina il Brixia Next Gen - post pronti in IT/DE/EN con i numeri veri del sito
argument-hint: "[canale: instagram|facebook|linkedin|x|newsletter|tutti] [tema: numeri|ranking|europei|pista|record|partner|foto|news|libero]"
allowed-tools: Read, Grep, Glob, Bash(git log:*), Bash(python3:*), WebFetch
---

# /brag - Brixia Next Gen

Scrivi contenuti promozionali ("brag") per il Brixia Next Gen, meeting
internazionale Under 18 di Bressanone. Argomenti: `$ARGUMENTS`
(primo = canale, secondo = tema; se mancano usa `tutti` e scegli tu i 2-3
temi più forti del momento).

## 1. Raccogli i fatti, solo da fonti verificabili

- Sito live: https://brixia-nextgen.org/ (WebFetch). Se non raggiungibile,
  usa `index.html` del repo, estraendo il testo visibile, ad esempio:
  `python3 -c "import re,html;s=open('index.html').read();s=re.sub(r'<(script|style)[\s\S]*?</\1>','',s);print(re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))))"`
- Record italiani U18: `record-italiani.json` (campi `upd_m`/`upd_f` = data
  ultimo aggiornamento; l'ultimo valore di ogni riga a 1 = gara nel programma).
- Novità recenti: `git log --since="60 days ago" --oneline`.
- Media kit partner: `docs/Brixia_Next_Gen_2027_Media_Kit_Partner.pdf`.

Fatti chiave da cercare (verificali sempre sulla fonte, possono cambiare):
data e luogo dell'edizione 2027, numeri 2026 (atleti, rappresentative,
paesi, iscrizioni), atleti poi agli Europei U18, posizione nel ranking
World Athletics, pista rifatta, sponsor e organizzatori.

**Regola d'oro:** ogni numero, nome, data o classifica deve comparire
nelle fonti sopra. Niente stime, niente superlativi non supportati
("il più grande d'Europa" no, "#1 meeting U18 a invito al mondo" sì,
perché è sul sito con fonte World Athletics). Se un dato manca, non
inventarlo: scrivilo nelle note finali.

## 2. Scrivi

Per ogni canale richiesto, una versione in **italiano, tedesco e inglese**
(il sito è trilingue IT/DE/EN). Testi naturali, non traduzioni letterali.

| Canale | Formato |
|---|---|
| instagram | gancio nella prima riga, 80-150 parole, 3-6 emoji al massimo, 5-10 hashtag in fondo, suggerimento immagine dalla galleria |
| facebook | 100-200 parole, tono da comunità, link al sito |
| linkedin | 120-250 parole, taglio partner/territorio/sport giovanile, nessuna emoji o quasi, invito a "Diventa partner" |
| x | massimo 280 caratteri, 1-2 hashtag |
| newsletter | oggetto + preheader + 150-250 parole + call to action |

Hashtag di base: `#BrixiaNextGen #Bressanone #Brixen #AtleticaLeggera
#Leichtathletik #Athletics #U18`. Link: `https://brixia-nextgen.org/`.

Tono: orgoglioso ma sobrio, sportivo, rispettoso degli atleti minorenni
(nessun dato personale oltre a nomi e risultati già pubblici).

## 3. Consegna

1. **I 5 fatti più forti**, ognuno con la sua fonte (sezione del sito,
   file o commit).
2. I post, raggruppati per canale e lingua, pronti da copiare.
3. **Note**: dati mancanti o da confermare (es. regolamento 2027 non
   ancora pubblicato) e cosa conviene aggiornare sul sito.

Non modificare file del repo e non pubblicare nulla: il comando produce
solo testi da rivedere.
