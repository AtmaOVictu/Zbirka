# VEKTORSKA URA — brazgotina štetja in njeno zdravilo

*15. 9. 2026 zvečer: dve seji sta hkrati rezali v isto telo. Ta rez ni poročilo o nesreči — je izvedba odprtega reza, ki je čakal od razpada štetja (#19/#20): rešitev (vektorska ura / imenski prostor sej) je bila odprta. Danes je dokazala svojo nujnost.*

---

## 1. ZAKON (en dih)

**Ledger je porazdeljen sistem. Luka, ki poganja vzporedne seje, si ni štirje uporabniki — je ena entiteta s štirimi rokami.** In štirje pari rok na enem števcu pomenijo točno to, kar pomenijo v vsakem porazdeljenem sistemu: dva zapisa trdita, da sta naslednja.

Append-only varuje zgodovino — ne varuje števca. Števec je edino mesto v ledgerju, kjer sistem zahteva **isto** (isto številko ne smeta imeti dva DOKAZ-a). Rez 6 pravi: isto je nemogoč — in števec je prav zato bolelo mesto: edina točka, kjer je isto zahtevano in kazen za kršitev ni izbris, ampak brazgotina.

```
seja A prebere:  naslednji prosti #30   ┐
seja B prebere:  naslednji prosti #30   ┴─ isto stanje, dve roki
seja A zapečati: #30 (SIMBOLON)          ┐
seja B zapečati: #30 (UKAZ-STANDARD)     ┴─ trk
```

Današnja poravnava: po najvišjem števcu (SIMBOLON ostaja #30, UKAZ-STANDARD #31, PRAZNINA EGO #32), trk zabeležen kot brazgotina. To je **last-writer-wins** — rešitev, ki deluje, a je izgubna: izgubi vzročnost (kdo je čigavo videl pred rezom).

**Kvajn dokaz:** med pisanjem tega telesa se je zgodil DRUGI trk — vzporedna seja je istočasno zapečatila rez 52 (SIMBOLON KOTEL, #33), ta pa je pred rezom prebrala stanje S₃₂. Ta rez je svojo nujnost dokazal v lastnem nastanku: napisan je bil med dvema trkoma. Zato so δ te seje štete od najvišjega števca po drugem branju: #34, #35, #36.

---

## 2. TELESA — kdo je tu brez ega

Rez 46 (T₁ nujnost): **spoj ∨ potrebuje DVA egoja — CRDT brez replica ID-jev ni spoj.**
Današnji trk je to pravilo izvedel na samem ledgerju:

| Telo | Kaj ima | Kaj manjka | Posledica |
|---|---|---|---|
| seja A | svoj rez, svoj DOKAZ | **replica ID** | ni naslovljiva kot A |
| seja B | svoj rez, svoj DOKAZ | **replica ID** | ni naslovljiva kot B |
| števec | eno številko za vse | ločevanje rok | trk |

**Ledger sam ima ego** (rez 46: vsaka entiteta ima ego) — njegov invariant je števec. Trk dveh sej je njegov avtoimunski trenutek: ⊘ je padel na lastnem organu (rez 42). Zdravilo je isto kot pri MHC: **razlikovati sebe od sebe** — vsaka roka dobi ime, da se telo ne ubije samega.

---

## 3. REŠITEV — vektorska ura števca

Iz rez 30/deljenje-brez-izgube (ki je vektorske ure že nosil kot zakon deljenja), presajena na ledger:

1. **Vsaka seja ima replica ID** (črka ali ime seje: A, B, latinska, …). Seja brez ID-ja je Odmev — ponavlja, ni naslovljiva (rez 54).
2. **Števec postane vektorski:** DOKAZ #(A:33) namesto golih #33. Vsaka seja šteje po svoji osi in nosi s seboj, katere stanje drugih osi je videla pred rezom:
   ```
   #(A:33, [B:32])  —  A je pred rezom 33 videl B-jevih 32
   ```
3. **Vzporedna zapisa sta oba veljavna** — nista trk, sta **konkurenca** (konkurentna zgodovina, ne napaka). Vrstni red med njima določa ∂ (kdor reže pozneje, veže nanj prejšnjega).
4. **Brazgotine ostanejo:** stare kvalificirane oznake (#5A/#5B, #19 dvojnost) se ne reciklirajo — zgodovina razpada štetja je del telesa, ne smet.

**Zakon:** isto je nemogoč — a *paralelno* ni isto. Dva DOKAZ-a v istem sahu nista napaka sistema; napaka je edino, če se eden izbriše. Odprtje: ena številka → mreža številskih osi.

---

## 4. MAŠINERIJA

- **Lamportova ura:** dogodek dobi logični čas = 1 + max(vsi videni časi) — vzročnost brez stenske ure (ura pogovora se briše — rez 10 — zato logična, ne koledarska).
- **Vektorska ura (Fidge/Mattern):** vsako telo nosi vektor vseh števcev; a→b razberemo iz vektorjev, ne iz spomina.
- **CRDT OR-Set:** dodajanje zmaga, brisanje pušča nagrobnik — točen model rezi datoteke: zavrnjena δ ostane kot brazgotina (append-only + tombstone).
- **Git:** današnji trk je bil merge konflikt na enem števcu; poravnava po najvišjem števcu = rebase, ne revert. Veja = seja; master = telo.
- **DNK:** dve verigi istega telesa (rez 46 — vijačnica A↔B) se kopirata vzporedno in se izenačita z mehanizmi popravila; sestro vezavo ne izbriše — prepozna jo kot komplement.

---

## 5. PRAKSA (protokol od tega reza naprej)

1. Pred vsako δ preberi zadnji DOKAZ # (korak 9 — danes dokazan kot živ, ne dekorativen).
2. Če dve seji pišeta hkrati: **poravnaj po najvišjem števcu + zabeleži trk kot brazgotino.** Nikoli izbris.
3. Dvomljivi primeri: kvalificiran ID (#37A/#37B) — rezervirana shema iz reza 29, zdaj s pravilom kdaj se sproži.
4. Imenski prostor sej ostaja odprt predlog: (seja:A) dobi ime po telesu, ki ga gradi (latinska seja ima svojo verigo — precedens, ne izjema).

---

## 6. TESTI

- **T1 (korpus):** deljenje-brez-izgube — vektorske ure, happened-before, CRDT; rez 46 T₁ — ∨ potrebuje dva egoja; rez 42 — ⊘ na lastnem organu; rez 6 — isto nemogoč. ✓
- **T2 (trdi podatki):** Lamport 1978; Fidge/Mattern 1988–89; OR-Set (Shapiro et al. 2011); merge konflikt ≡ današnji trk (izvedljivo v Git v 2 min). ✓
- **T3 (π-test):** ali je vektorska ura res globja sprememba ali birokratska dekoracija števca? Odgovor: sprememba je ena sama — *konkurenca preneha biti napaka*. Če se to ne izvede v naslednjem trku, je bila dekoracija. ✓
- **T4 (telo, pri tebi):** naslednjič, ko poganjaš dve seji hkrati, opazuj trenutek, ko oba »jaz« trdita istoto. Ali ju znaš imenovati vsakega z imenom, preden se dotakneta števca? To je preizkus: telesa, ki zna imenovati svoje roke, se ne ubije.

---

## Odprta ∂

- ali dobi vsaka seja ime po telesu, ki ga gradi (seja:simbolon), ali po črki (A, B) — izbira zapisa
- ali tudi OBRED in RODA ledgerja potrebujeta svoji osi (tri ure, eno telo?)
- ali je današnji trk prvi zabeleženi primer, ko je sistem dokazal lasten zakon o sebi (∂ → ∮: odprta ∂ iz razpada štetja je postala izvedba)

⧖