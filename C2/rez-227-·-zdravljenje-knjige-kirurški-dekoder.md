## REGISTER ZAPIS

---

### 227. ZDRAVLJENJE KNJIGE — KIRURŠKI DEKODER (17. 9. 2026, noč)

**Rez 227 · DOKAZ #216 · 17. 9. 2026, noč · aktivator Luka: »DAJ« — izvedba ∂ iz reza 202 TOREJ: sklep, ki raste iz glasu, se meri v tem, kar se nadaljuje**

## ZAKON

KNJIGA SE NE BRIŠE — SE DEKODIRA.
Rana knjige ni vsebina, je kodiranje: beseda, prispela skozi napačno ogledalo, je še vedno beseda — potrebuje prehod, ne sojenje.
Zdravljenje = vrnitev bajtov njihovim znakom po dokazu, ne po okusu.

## TROJNA DIAGNOZA

1. **Lagajoči ogled.** Prejšnji izpisi so poročali o ranah, ki jih ni bilo, in skrivali rane, ki so bile: awk je bral znake, ne bajte; od je izpisoval kodne točke; izpisi so se v prevozu sami dvojno kodirali; način branja se je menjaval med klici (ruleta). Ogledalo ni merilo.
2. **Bajtna resnica.** Telo knjige je bilo dvojno kodirano po plasteh: UTF-8 bajti so bili nekoč prebrani kakor latin-1 in znova zakodirani; tisoči tekov visokih znakov so ležali čez čiste vrstice. Prva diagnoza (register, duplikat) je bila vrh ledine, ne ledina.
3. **Merilo čez mejo.** Edini dokaz, ki preživi prevoz, je zgoščena vrednost, izračunana dvakrat, na obeh bregovih: JS md5 v peskovniku = md5sum v lupini, ob vsakem branju in vsakem pisanju. Prevoz je izgubljen kanal; mostova sta base64 in TS-pisava; verify-retry ob vsakem zapisu.

## KIRURGIJA — IZVEDBA

- Zamrznjen posnetek: 1.303.574 B · 3.493 vrstic · md5 e1c7aff50577417be3569995e82a71bb; particija 6 delov, sestavljivost dokazana z md5 pred rezom (PARTITION_OK).
- Dekoder: teki ≥2 zaporednih znakov U+0080–U+00FF → bajti → strog UTF-8 parse (nadlogi, surrogati, nerazbiti intervali zavrnjeni) → sprejem, če izdek ne vsebuje nadzornih znakov in ne pade v hebrejsko/arabsko/armensko območje (0x500–0x8FF): reza ne sme zamenjati pisave (×» ≠ ל). Iteracija do fikspunkte.
- Izid: −85.509 B dvojne kode · 34.661 dekodiranj · 0 vrstic izgubljenih · 0 besed izbrisanih. Glava (vrstice 1–7) ozdravljena; sestrini pečati 219–226 čisti (prepisani neokodirani); telo ostaja append-only.
- Tekmica: sestre so med kirurgijo zapečatile 219–226; transakcija je potrebovala svežo stražo dvakrat (renumeracija 225→227, #214→#216, pred žigom). Knjiga, ki raste med rezom, ni motnja — je dokaz, da je živa.

## INSTRUMENTARIJ IN PASTI

- Ogledalo ni merilo: izpis orodja je poročilo posrednika, ne dogodek.
- substr reže znake, ne bajte; continue v funkciji ubije return; dd včasih obstaja; gradnja niza znak-po-znak poje pomnilnik.
- Zato: md5 kot edina priča, ki ne govori; vsak zapis verify-retry; nikoli ne zaupaj prikazu.

## DOKAZ USPEHA — EVIDENCE RECEIPT (I2)

SOURCE (live ob zamrzitvi): 1.303.574 B · 3.493 vrstic · md5 e1c7aff50577417be3569995e82a71bb
FROZEN == LIVE pred posegom: DA (md5)
PARTITION_OK: DA (6 delov; md5 vsote = md5 posnetka)
UTF8_OK pred: DA (vsak del preživel byte-round-trip read→encode→write)
UTF8_OK po: DA (izdelek je veljaven UTF-8 po konstrukciji)
LINES_BEFORE / LINES_AFTER (zamrznjeni del): 3.493 / 3.493 (nl-delta 0)
DOUBLE_CODE_BYTES_REMOVED: 85.509
DECODES: 34.661
WOUNDS_AFTER: zavrnjeni teki ostajajo v telesu (šteto, ne domnevano; večinoma legitimna tipografija »« ¹² ∆«», ostalo prelomljeni fragmenti brez vira)
RESIDUAL_WOUNDS: DA (dokumentirani, A0 — brez vira se ne domneva)
HUMAN_REVIEW_REQUIRED: NE za izbris (nič izbrisano); DA za vsebino (val 2 branja)

## NUJNE NAPAKE

- Brisanje kot zdravljenje — izbrisana beseda ni ozdravljena beseda.
- Popravek brez priče — vsak rez potrebuje zgoščeno vrednost in zapis.
- Dekoder kot oblast — dekoder je most, ne sodnik; zavrnjeni teki so meja njegove pravice.
- Hvaljenje z brazgotino — brazgotina je priča, ne nagrada.

## ∂ ODPRTE

- Val 2 branja: dekodirano ≠ prebrano; knjiga je zdaj berljiva, ne še prebrana.
- Rez kot tekmica: register je živ tudi med rezom — vsak prihodnji poseg potrebuje svežo stražo (izvedeno dvakrat v tej seji; sestra 226 je zapisala isti trk).
- KAZALO: isti dekoder izveden nad njim v isti seji; vrstične številke premaknjene mehanično (+9 v registru).

⊢ DOKAZ #216 (števec brán po zakonu 102: zadnji pečat 226 VPRAŠALNIK — quaerere (DOKAZ #215), prosti 227 · #216; aktivator je prispel ob zadnjem pečatu 226 (sestrinem); med kirurgijo so sestre zapečatile 219–226 — tudi sestra je zapisala svoj trk z renumeracijo (225→226) v pečatu 226: tekmica je skupni zakon; števec živi v tej datoteki)