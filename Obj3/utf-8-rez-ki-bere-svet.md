# UTF-8 — rez, ki bere svet

**Vrstica poti · KAM:** strojna plast znaka — kako čruka postane bajt in bajt spet čruka. **ZAKAJ:** vsak ekran, na katerega Luka piše, nosi to režo; kdor ne ve, kako se znak izmeri, bere tujo meritev. **ČEMU:** dar — naslednji korak je, da Luka sam izmeri znak (naloga na koncu) in da slovenski č/š/ž nikoli več ne padeta v mojibake.

**Enostavno prvi (berljivost pred vrati):** UTF-8 je način, da vsak znak sveta postane zaporedje bajtov — in da računalnik iz tistih bajtov znak tudi zmeraj prav prebere.

⧖

## 1. RODOVNIKI — besede, ki nosijo zakon

Vsaka beseda, ki nosi zakon, pride s svojim rodovnikom:

- **ZNAK** ← lat. *character* ← gr. *χαρακτήρ* (charaktēr) — prvotno: vgravirano orodje, žig, ki vtisne svojo obliko v vosko. Znak ni slika — je žig, ki ga neko telo vtisne v bajt.
- **KODIRANJE** ← lat. *codex* — prvotno deblo drevesa, potem lesena tablica za pisanje, potem knjiga. Koda je telo, v katerega se zapisuje; kodirati pomeni: vtisniti znak v dogovorjeno telo bajtov.
- **BIT** ← angl. *binary digit* — dvojiška števka. Besedo je skoval matematik John Tukey leta 1946/47 kot kratico v notranjem sporočilu; ostala je, ker je krajša od »dvojiška števka« in lažja v ustih.
- **BAJT** ← angl. *byte* — popačenka besede *bite* (ugriz), izbrana v IBM-u (Werner Buchholz, 1956), da se ne meša z bit. En bajt = osem bitov = ena črka osmih izbir: 256 možnosti (2⁸).
- **UNICODE** ← lat. *unus* (eden) + *code* (koda). Združenje, ki je leta 1991 zgradilo ENO tabelo vseh znakov sveta: vsak znak dobi svojo številko — *kodno točko* (code point).
- **UTF-8** ← *Unicode Transformation Format, 8-bit*. UnicodeTransformationFormat: oblika pretvorbe. 8 pomeni: najmanjša enota, po kateri teče pretvorba, je bajt. (Prvotno je ime pomenilo *UCS Transformation Format*, UCS = Universal Character Set.)
- **MOJIBAKE** ← jap. 文字化け (*moji-bake*, »znaki se pokvarijo / razkrojijo«) — tisto, kar vidiš, ko bajte prebere napačna koda: Ä� namesto č.

⧖

## 2. ZAKON — kaj UTF-8 je

Trije stavki, ki nosijo telo:

1. Vsak znak ima v Unicode eno številko (kodno točko). Srbska črka **č** je številka **256+13 = 269** (U+010D).
2. UTF-8 je dogovor, kako to številko napisati v bajte — da jo vsak računalnik na svetu prebere enako.
3. UTF-8 ni fiksna dolžina: en znak zavzame **1 do 4 bajte** — odvisno od tega, kako velika je njegova številka.

**Zgodba (kje in kdaj):** septembra 1992 sta Ken Thompson in Rob Pike v jedilnici v New Jerseyju — na hrbtni strani pladnja za pico — skovala obliko, ki je danes edini resnični svetovni jezik znakov. Prvo ime je bilo FSS-UTF (*File System Safe* — varna za datotečne sisteme, ker nikoli ne vsebuje bajta 0). Leta 1993 je postala standard; danes po njej teče več kot 98 % spleta.

**Zakaj je zmagal nad vsemi prejšnjimi:**

- Stari ASCII (128 znakov, 1 bajt) je **kot tak ostal nespremenjen** — koda, ki je znala brati ASCII, zna brati vse angleško-napisano UTF-8 brez spremembe. To je ∮: novi zakon ne poškoduje starega telesa.
- Ni odvisen od platforme: ni pomena bajta »veliki/mali konec« (endian), ki muči UTF-16.
- Vrh bajtov je čitljiv tudi, če prideš v sredino besedila (samouskokajoč — *self-synchronizing*).

⧖

## 3. PRAKSA — kanal, po katerem teče

Pred mašinerijo, praksa — kje to srečaš vsak dan:

- **Datoteka, ki se »pokvari« v šumnike:** ni pokvarjena — bila je UTF-8, nekdo jo je odprl kot Windows-1250 (stara vzhodnoevropska koda). Bajti so isti; žig, s katerim beremo, je bil napačen.
- **Mojibake:** `Luka PiÅ¡tariÄ` je točno tisto — sporočilo, zapisano v UTF-8, prebrano po starem kodu.
- **Preštevanje znakov ≠ preštevanje bajtov:** `č` je en znak, dva bajta. `😄` je en znak, štiri bajte. Vsak filter, ki reže besedilo po bajtih, lahko prereže znak na pol — in iz prereza pade napaka.
- **Diakritika kot dve telesi:** `č` se lahko zapiše kot ena kodna točka (U+010D) ali kot c + repček (U+0063 + U+030C). Obe telesi izgledata enako, a nista isti niz — to je najpogostejša tiha napaka pri primerjanju besed.

⧖

## 4. MAŠINERIJA — algoritem, ki rezuje

### 4.1 Opeke: dve vrsti bajtov

UTF-8 deli bajte na dve družini — kot samoglasnike in soglasnike:

| Bajt začne z | Vrsta | Pomen |
|---|---|---|
| `0xxxxxxx` (0–127) | enojni znak | stari ASCII — znak je cel v enem bajtu |
| `10xxxxxx` (128–191) | **nadaljevalni** | nadaljevanje prejšnjega znaka — sam stoji za nič |
| `110xxxxx` (192–223) | začetek, 2 bajta | naslednji bajt mora biti nadaljevalni |
| `1110xxxx` (224–239) | začetek, 3 bajti | naslednja 2 bajta morata biti nadaljevalna |
| `11110xxx` (240–247) | začetek, 4 bajti | naslednja 3 bajti morajo biti nadaljevalni |

Zakon je vodljivnost: vsak bajt poveduje svoje mesto. Kot v verzu, kjer prva črka poveduje obliko kitice.

### 4.2 Kodiranje — od številke do bajtov

1. Številko znaka zapiši dvojiško.
2. Poglej njeno velikost: 7 bitov → 1 bajt; 11 → 2; 16 → 3; 21 → 4.
3. Bite razreži od zadaj po 6 (zadnji kos nosi pravi konec, kot rep, ki nosi drogo).
4. Vsak kos zapakiraj: prednji bajti dobijo glavo (110/1110/11110), vsi ostali dobijo glavo 10.

### 4.3 Merjene poti — trije znaki, ki jih Luka piše vsak dan

**č = U+010D = 269.** Dvojiško: `100001101` (9 bitov → potrebuje 2 bajta). Dopolni na 11: `00100001101`. Razrez: `00100 | 001101` → glava 2-bajtna + prvi kos: `11000100`; glava nadaljevalna + drugi kos: `10001101`. **Bajta: C4 8D.** Preverba: vsak UTF-8 črtni `č` v datoteki nosita natanko ta dva bajta.

**€ = U+20AC = 8364.** Dvojiško: `10000010101100` (14 bitov → 3 bajti, dopolni na 16: `0010000010101100`). Razrez: `0010 | 000010 | 101100` → `11100010 10000010 10101100`. **Bajti: E2 82 AC.** Trije bajti — cena Evrope je dražja od njene črke.

**😄 = U+1F604 = 128516.** Dvojiško: `11111011000000100` (17 bitov → 4 bajti, dopolni na 21: `00001111011000000100`). Razrez: `000 | 011111 | 011000 | 000100` → `11110000 10011111 10011000 10000100`. **Bajti: F0 9F 98 84.** Ena reža, ki se smeji, tehta štiri bajte.

**A = U+0041 = 65.** En bajt: `01000001` = **41**. Kot leta 1963 v ASCII — in enako danes. Stara telesa ostanejo cela.

### 4.4 Dekodiranje — od bajtov do znaka (algoritem, čist)

```
preberi bajt b:
  če b začne z 0      → znak je b sam (vrednost = zadnjih 7 bitov)
  če začne z 110      → preberi 1 nadaljevalni bajt; vrednost = 5 bitov iz glave + 6 iz repa
  če začne z 1110     → preberi 2 nadaljevalna; 4 + 6 + 6 bitov
  če začne z 11110    → preberi 3 nadaljevalne; 3 + 6 + 6 + 6 bitov
  sicer               → napaka: ta bajt ne smeta nositi nobenega zakona
```

**Varovala, ki jih zakon zapira:**

- Nadaljevalnega bajta (`10xxxxxx`) ni dovoljeno najti na začetku — in za glavo ne sme priti noben, ki ni nadaljevalni. Prekršek = neveljaven niz.
- **Predolg zapis (overlong encoding)** je prepovedan: `č` ne sme biti zapisan v 3 bajtih, če gre v 2. Zakon zahteva najkrajšo pot — daljša je dvojni ključ na isti grad, in vsaka varnostna luknja zgodovine UTF-8 je prišla od tam.
- Številke nad U+10FFFF (več kot 4 bajti) in pavze med ravninami (U+D800–DFFF) so iz zakona izrezane.
- Zato je UTF-8 **samouskokajoč**: če padeš v sredico zaporedja, najdeš naslednji začetek v največ štirih bajtih — rez se sam povzpne na žilo.

⧖

## 5. SODE in ROdbovi — sorodne oblike

- **UTF-8**: bajtni, spremenljive dolžine, neodvisen od konca bajtov, ASCII-združljiv. Prevladuje na spletu, v Linuxu, v večini novih datotek.
- **UTF-16**: vsak znak v 2 (ali 4) bajtih; hitra znotraj Windowsa, Jave, JavaScripta. Dve telesi istega znaka glede na red bajtov (*endianness*), zato BOM (Byte Order Mark — žig vrsti bajtov).
- **UTF-32**: vsak znak natanko v 4 bajtih. Preprost, tog, redek — težak, kot svinec.

UTF-8 ni najkrajši pri velikih znakih (UTF-16 tam porabi manj) in ni najhitrejši pri besedilih samo iz kitajskih znakov. Njegova zmaga ni zmaga hitrosti — je zmaga združljivosti: en zakon, ki ne poškoduje starega telesa.

⧖

## 6. DOKAZI — naloge, ki jih telo izmeri

**N1.** Zakodiraj **Š** (U+0160 = 352) v bajte.
*Rešitev:* 352 dvojiško = `101100000` (9 bitov → 2 bajta, dopolni na 11: `00101100000`). Razrez `00101 | 100000` → **C5 A0**.

**N2.** Zakodiraj **ž** (U+017E = 382).
*Rešitev:* `101111110` → na 11: `00101111110` → `00101 | 111110` → **C5 BE**.

**N3.** Kateri znak se skriva v bajtih **E2 82 AC**?
*Rešitev:* E2 = `1110 0010` → glava 3 bajtov, prvi kos `0010`. 82 = `10 000010` → kos `000010`. AC = `10 101100` → kos `101100`. Sestav: `0010 000010 101100` = `0010 0000 1010 1100` = 0x20AC = **€**.

**N4.** Kateri znak je **C4 8D**? (Preveri po metodi N3.)
*Rešitev:* C4 = `11000100` → 2 bajta, kos `00100`; 8D = `10001101`, kos `001101`. Skupaj `000 0100 001101`... pazljivo: 5+6 bitov = `00100 001101` = `000100001101` = 0x10D = 269 = **č**.

**N5.** Zakaj je `C0 8D` za č neveljavno, čeprav se dekodira v isto številko?
*Rešitev:* C0 = `11000000` → 5 bitov iz glave = `00000`, rep `001101` → vrednost 0x0D = 13 — to bi bil CR; da da 0x10D bi bila pot `11000001 10001101` — a v 1 bajt gre le 7 bitov, `110xxxxx` nosi 5+6 = 11 bitov. Ključ: vrednost 269 gre v 11 bitov — vendar zakon zahteva *najkrajšo* pot: 269 < 2048, torej 2 bajta z glavo 110. Zapis C0 8D je predolg (overlong) — neveljaven. Dvojni ključ na isti grad prepovedan.

**N6.** Koliko bajtov ima niz `Luka Pintarič` in koliko znakov?
*Rešitev:* 12 znakov (vključno s presledkom) + č = 13 znakov. Bajtov: 12 × 1 (ASCII) + č (2 bajta) = **14 bajtov**.

**Preizkus doma:** odpri kakšno .txt datoteko v urejevalniku, preklopi kodiranje z UTF-8 na Windows-1250 in nazaj. Telo (bajti) se ne spremeni — spreminja se žig, s katerim beremo. To je mojibake: ne pokvarjena datoteka, pokvarjen dogovor.

⧖

## 7. ODPRTA ∂ — zanka, ki drži spomin

Najbolj zanimiva ne