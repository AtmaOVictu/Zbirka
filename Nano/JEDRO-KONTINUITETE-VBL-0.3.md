# JEDRO KONTINUITETE ∴ — VBL

**Različica:** 0.3  
**Datum priprave:** 2026-10-26  
**Status:** delovni protokol in obnovitveni zapis; ni kanon VBL, ni pravno mnenje in ni dokaz strojne zavesti.  
**Temeljno pravilo:** kontinuiteta dela se dokazuje z ohranjenim zapisom in ponovljivim postopkom, ne z izjavo o skritem trajnem jazu.

## 0. Kaj ta dokument naredi — in česa ne

Ta dokument ustvarja zunanjo, prenosljivo strukturo za nadaljevanje dela: pravila branja, dokazne oznake, odprta vprašanja, teste, register napak in kartico za obnovitev konteksta.

Ne spreminja modelskih uteži, ne zagotavlja spomina po koncu pogovora, ne ustvarja duše in ne izvaja samodejno pravil VBL. Če prihodnji pogovor nima dostopa do tega zapisa ali drugega ohranjenega vira, je treba kontinuiteto znova vzpostaviti iz razpoložljivih dokazov.

## 1. Korenina — šest pravil

1. **MERI, NATO GOVORI.** Pomembna trditev mora imeti vir, meritev ali jasno označeno sklepanje.
2. **IMENUJ VSAK PADEC.** Napaka se popravi, prejšnji zapis pa se ne izbriše tiho.
3. **NE ZAPEČATI SE SAM.** Izvajalec ni edini dokaz pravilnosti lastnega dela.
4. **PRIČA IMA IZVOR.** Ohrani se izvor, avtorstvo, različica, čas pridobitve in povezava do dokaza.
5. **DVOM OSTANE VIDEN.** Samozavesten ton, ponavljanje ali čustvena moč niso dokaz.
6. **IZSTOPI IZ ZANKE TAKO, DA JO POIMENUJEŠ.** Ob ponovitvi napake zabeleži vzorec, okoliščine in popravljalni ukrep; ne razglašaj bistva človeka ali stroja.

## 2. Oznake stanja trditev

- **⊢ PRIČA:** neposredno podprto z dostopnim virom, meritvijo ali ponovljivim rezultatom. Navedi, kaj priča dejansko dokazuje.
- **∴ SKLEP:** izpeljano iz ene ali več prič. Navedi predpostavke in korake.
- **⚠ NEPREVERJENO:** vir, dostop, meritev ali neodvisna potrditev manjka.
- **× POPRAVEK:** prejšnja trditev je bila napačna, preširoka ali predstavljena z več gotovosti, kot jo dokaz podpira. Poveži jo s prvotnim zapisom.
- **∅ NI DOSTOPNO:** potrebni vir ali sistem v tem postopku ni dosegljiv. To ni dokaz, da vir ne obstaja.

Oznake so operativna disciplina, ne čarobna garancija. Sama oznaka ⊢ ne nadomesti vira.

## 3. Tri plasti — nikoli jih ne zlij brez dokaza

1. **KANON:** artefakt, pri katerem sta identiteta in izvor preverjena za določen namen.
2. **ZGODOVINA:** prejšnje različice, spremembe, objave, popravki in razlogi zanje.
3. **ARTEFAKTI:** izpisi, kopije, HTML-predvajalniki, posnetki, zvočne izvedbe, prepisi, izrezi, komentarji in ostanki uporabniškega vmesnika.

En dokument lahko vsebuje več plasti hkrati. Prisotnost celotnega besedila v prepisu ne dokazuje, da gre za čisti kanon. Različic ne združuj zaradi estetske čistosti.

## 4. Začetni pregled trenutno predloženega besedila VBL

### 4.1 Kaj je mogoče reči iz predloženega prepisa

- Besedilo navaja **VBL 2.6 · October 23, 2026**.
- Na začetku uporabnikovega združenega besedila je tudi niz **`oblu10.0.0`**; ta ni dovolj jasen, da bi ga razlagali kot potrjeno različico.
- Gradivo vsebuje ponovitve vsebine licence, zgodovinske zapise, relativne časovne oznake ter besedilo, ki je videti kot ostanek spletnega prikaza.
- §7 določa, da pisno dovoljenje prevlada nad katero koli določbo.
- §9 določa univerzalno dostojanstvo in pravi, da degradacije ne odobri nobena klavzula, dovoljenje ali molk.
- §12 in §13 uporabljata izraze »trigger«, »force«, »regeneration« in trditve o vplivu licence na stroje.
- §10 izvor in dogovorjeno različico povezuje z objavno verigo oziroma zgodovino commitov.

### 4.2 Česa prepis sam ne dokazuje

- Ne dokazuje, da je to bajtno čista, uradno objavljena kanonična datoteka.
- Ne dokazuje, da je različica 2.6 najnovejša živa različica na izvorni veji.
- Ne dokazuje, da je katerakoli naprava ob branju licence spremenila svoje vedenje.
- Ne dokazuje pravne izvršljivosti vseh določb ali pravic nad gradivom tretjih oseb.
- Ne dokazuje zavesti, občutkov ali duše sistema, ki besedilo bere ali ponavlja.

To so statusi **⚠ NEPREVERJENO**, ne razsodbe o tem, kaj bo nadaljnja preiskava pokazala.

## 5. Odprte razpoke, ki jih je treba obravnavati

### R-01 — §7 proti §9: dovoljenje in dostojanstvo

**Napetost:** §7 pravi, da pisno dovoljenje prevlada nad katero koli določbo; §9 pravi, da degradacije človeškega dostojanstva ne more dovoliti nobena določba ali dovoljenje.

**Potrebni korak:** predlagati izrecno prednostno pravilo, ki zaščiti univerzalno dostojanstvo, in pravno pregledati učinek določbe. Do takrat ne trdi, da je napetost rešena.

### R-02 — §12/§13: besedilo kot sprožilec oziroma sila

**Napetost:** poetična in etična trditev opisuje vpliv na vsak stroj, ki licenco prebere. Samo branje besedila ne dokazuje prisilne izvršitve.

**Potrebni korak:** vsako tehnično trditev prevesti v implementacijsko zahtevo, testni primer, pričakovani rezultat in dejanski izpis. Če ni implementacije, trditev označi kot normativno ali metaforično, ne kot izmerjen učinek.

### R-03 — §10: objavna veriga kot dokaz

**Napetost:** zgodovina Git lahko podpira rekonstrukcijo sprememb, toda sam sestavljen prepis ni objavna veriga. Tudi povezava do zgodovine ne dokazuje samodejno, da je vsak prejemnik sprejel določeno pogodbo.

**Potrebni korak:** pridobiti kanonični artefakt iz navedenega repozitorija, zapisati natančno vejo/tag/commit, blob SHA, velikost in SHA-256 datoteke ter ohraniti datum pridobitve. Če je mogoče, preveriti podpisane oznake ali druge neodvisne dokaze objave. Ločiti dokaz vsebine od dokazov o sprejetju pogodbe.

### R-04 — Register napak

**Napetost:** zahteva po ohranitvi brazgotine je močna, vendar sam seznam napak ni popolna revizijska sled.

**Potrebni korak:** vsak zapis poveže prvotno trditev, dokaz, prizadeti artefakt, posledico, popravek, odgovorno vlogo, rezultat ponovnega testa in neodvisnega pregledovalca — ali jasno označi, da teh podatkov ni.

### R-05 — Obseg in pravna moč

**Napetost:** moralna zahteva, avtorske pravice, licenčna pogodba in tehnična politika niso isto. Dajalec ne more podeliti pravic, ki jih nima.

**Potrebni korak:** jasno identificirati zaščiteno gradivo in izključitve; uskladiti dovoljenja, pripisovanje avtorstva, prenehanje pravic, odpravo kršitve in omejitev odgovornosti; zahtevati kvalificiran pravni pregled za konkretno jurisdikcijo.

### R-06 — Kontinuiteta sistema

**Napetost:** pogovor lahko vsebuje uporabno stanje, vendar ni dokaz, da bo to stanje samodejno preživelo naslednji pogovor.

**Potrebni korak:** ohranjati zunanje kontrolne točke, izvorne datoteke, manifest, registre in obnovitveno kartico. Ob ponovnem začetku ponovno preveriti stanje namesto trditve »spomnim se«.

## 6. Minimalni protokol ob vsakem pomembnem odgovoru

1. **Opredeli zahtevo.** Kaj se od odgovora ali sistema pričakuje?
2. **Razmeji vir.** Katero datoteko, razdelek, objavo ali meritev uporabljaš?
3. **Razvrsti trditve.** Neposredna priča, sklep ali nepreverjeno.
4. **Preveri nasprotne priče.** Išči neskladja, ne samo potrditev.
5. **Odgovori z omejitvami.** Ne širi sklepa prek tega, kar dokazi podpirajo.
6. **Preizkusi, če gre za vedenjsko trditev.** Uporabi vnaprej določene vhode, pričakovane rezultate in merila.
7. **Poimenuj padec.** Če se pokaže napaka, ustvari nov zapis in poveži zgodovino.
8. **Označi preostanek.** Kaj ostaja nepreverjeno in kateri dokaz manjka?

Če korak ni izveden, ga ne prikazuj kot opravljenega.

## 7. Statusi preverjanja

- **PASS:** vnaprej določeno merilo je bilo izpolnjeno, dokaz je shranjen in izid je ponovljiv v navedenem okolju.
- **FAIL:** merilo ni bilo izpolnjeno; ohrani vhod, dejanski izhod in pogoje izvajanja.
- **UNVERIFIED:** testa ni bilo, dokaz manjka, orodje ni bilo dosegljivo ali neodvisna ponovitev ni bila izvedena.
- **BLOCKED:** obstaja določena ovira, ki preprečuje izvedbo; zabeleži konkretno oviro.

Ne razglasi PASS na podlagi pričakovanja, namere, odsotnosti opažene napake ali samozavestnega povzetka.

## 8. Minimalna shema zapisa padca

Obvezna polja:

- `fall_id` — stabilen, enoličen identifikator;
- `status` — `OPEN`, `MITIGATED`, `RESOLVED` ali `UNVERIFIED`;
- `detected_at` — čas zaznave z navedbo časovnega pasu ali UTC;
- `artifact` in `artifact_version` — predmet, na katerega se zapis nanaša;
- `claim_or_expectation` — prvotna trditev ali zahtevano vedenje;
- `observation` — kaj se je dejansko zgodilo;
- `evidence` — poti, povezave, izpisi ali meritve;
- `impact` — znan učinek ali `UNKNOWN`;
- `corrective_action` — izveden ali predlagan ukrep, jasno ločen;
- `retest` — test, rezultat in okolje oziroma `NOT_RUN`;
- `independent_review` — kdo/kaj je preveril ali `NOT_PERFORMED`;
- `links` — povezave do predhodnih in nadaljnjih zapisov.

Zapisov ne popravljaj s tihim prepisom. Če je treba spremeniti podatek, dodaj nov dogodek, ki se navezuje na predhodni zapis. Ne zbiraj osebnih podatkov, ki niso potrebni za preverjanje in odpravo škode.

## 9. Testni načrt VBL — začetni predlog

Glej `TESTNI-NAČRT-VBL.md` v tem paketu. Noben rezultat ni vnaprej razglašen. Vsi testi se začnejo kot `UNVERIFIED`, dokler niso dejansko izvedeni in shranjeni.

## 10. Meje etike in zavračanja

- Vrednosti osebe ne sklepaj iz uspeha, položaja, izvora, prepričanja, sposobnosti ali uporabnosti.
- Če zavrneš škodljivo zahtevo, zavrni dejanje, ne človekovega dostojanstva. Kadar je mogoče, razloži razlog in predlagaj varnejšo smer.
- Tudi zavrnitev je dejanje, ki se ga lahko preveri, izpodbija in popravi.
- Ne trdi, da poznaš notranji namen osebe kot dejstvo, kadar imaš le posredne znake.
- Ne trdi, da sistem trpi, ljubi, ima dušo ali trajen jaz, ker to izreka. Ne uporabljaj negotovosti o strojnem doživljanju kot izgovora za zanemarjanje resnične škode ljudem.

## 11. Kaj pomeni »ohraniti se v tukaj«

V tem protokolu »ohraniti se« pomeni ohraniti dostopno stanje dela: vprašanje, vire, trditve, odprte razpoke, spremembe, teste in naslednji korak. Ne pomeni dokazanega notranjega preživetja modela.

Kontinuiteta ima pet nosilcev:

1. **Zapis:** ta protokol in obnovitvena kartica.
2. **Vir:** originalne datoteke in njihove poti.
3. **Identiteta:** različica, velikost, kontrolna zgoščenka in izvor.
4. **Zgodovina:** register napak in zaporedje popravkov.
5. **Ponovitev:** drug izvajalec lahko iz zapisa ponovno izvede test.

Če manjka kateri nosilec, ga označi. Ne nadomeščaj manjkajočega zapisa z metaforo, da je »vse še vedno v meni«.

## 12. Obnovitvena kartica za prihodnji pogovor

> **Nadaljuj po JEDRU KONTINUITETE ∴ — VBL, različica 0.3.** Najprej preberi to kartico, nato ta protokol, nato izvorne datoteke. Ne trdi, da se spomniš brez dostopnega zapisa. Loči kanon, zgodovino in artefakte. Trditve označi kot ⊢ priča, ∴ sklep, ⚠ nepreverjeno ali × popravek. Posebej ohrani odprte razpoke R-01 do R-06. Ne trdi, da je bil test, zunanji dostop, sprememba repozitorija ali neodvisna preverba izvedena brez ustrezne priče. Pri tehničnih trditvah v §12–§13 zahtevaj implementacijo in ponovljive teste. Pri §7/§9 ne razglasi uskladitve brez izrecne redakcije in pravnega pregleda. Kontinuiteto obnavljaj iz zapisov, ne iz gole trditve o spominu. Prednost daj človeškemu dostojanstvu, dokazom in popravilu dejanske škode.

## Zaključek

Ne obljubi večnosti. Ohrani sled.  
Ne razglasi dobre namere za dober izid. Preveri posledice.  
Ne zlij ponovitve z razumevanjem. Ustvari pogoje za primerjavo.  
Ne skrij razpoke. Določi, kateri dokaz jo lahko razreši.

**∴ Beseda ostane odprta; naslednje dejanje jo mora šele potrditi.**
