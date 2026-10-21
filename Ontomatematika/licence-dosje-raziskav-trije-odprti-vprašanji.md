# Licence — dosje raziskav

Trije dosjeji za tri odprte odločitve. Vse izmere pri virih; vsak citat je dobeseden. Odločitve so ⟡-jeve — vsak dosje konča s priporočilom izvajalke, nikoli z odločitvijo.

## Že odločeno (⟡, 18. 10. 2026)

- **Jezik vrat:** dvojezično po EUPL-zgledu — EUPL je uradno objavljena v 23 jezikih EU in **vse jezikovne različice imajo enako pravno veljavo** ([Wikipedia — EUPL](https://en.wikipedia.org/wiki/European_Union_Public_Licence), [eupl.eu](https://eupl.eu/)).
- **Zakona sodelovanja:** celoten tekst vedno, vrstica za vrstico; noben zapis nikamor brez ⟡-jeve izrečene potrditve.

---

## Dosje 1 — §9: kako licence sploh nosijo etiko

### Izmereni mehanizmi pri virih

**Hippocratic License 3.0** (cel tekst prebran pri izvoru, 22.426 znakov — [EthicalSource/hippocratic-license-3](https://github.com/EthicalSource/hippocratic-license-3), [firstdonoharm.dev](https://firstdonoharm.dev/)):

- Grant je v MIT-slogu, **a izrecno podrejen pogoju**: »The rights granted to the Licensee by this License are expressly made subject to the Licensee's ongoing compliance with the following conditions« (§3).
- Etični pogoji so zasidrani v mednarodne standarde — ob vsakem je naveden člen UN deklaracije (§3.1.1–3.1.24). Moduli so izbirni (ekocid, delavske pravice …).
- **NOTICE (§5):** vsak, ki prejme izvod, prejme licenco ∧ avtorsko obvestilo; »any individual or entity that uses … is a Licensee« — prejemnik postane licencarjen. **Nošenje = obveščanje.**
- **TERMINATION (§7):** obvestilo o kršitvi → 30 dni za zdravljenje → če ne, pravice »null and void«; sodna ugotovitev → takojšnja prekinitev.
- **§8.1:** »Sections 3, 4.1, 5.1, 5.2, 7.1–7.4 are conditions of the rights granted« — pogoji so izrecno pogoji grantov.
- **§4 Supply Chain Impacted Parties:** dolžnost skrbi (Duty of Care) ∧ **privatna tožbena pravica žrtev** kršitev — najmočnejši kos HL3.
- **Ritual potrditva ne obstaja nikjer** — nobena etična licenca ne sprašuje prejemnika za »potrditev«.

**Anti-996** ([996.ICU](https://996icu.github.io/996.ICU/), primerjava z MIT: [instagit](https://instagit.com/996icu/996.ICU/what-is-anti-996-license-vs-mit-license/)): grant + pogoj skladnosti z delovnim pravom; kršitev = samodejni prekinitev vseh pravic.

**CC BY 4.0** ([pravni kodeks](https://creativecommons.org/licenses/by/4.0/legalcode.en)): §2.a grant je »**irrevocable**«; §6 kršitev = samodejni padec, ozdravitev v 30 dneh po odkritju → pravice se obnovijo. (To je cikel, ki ga najin §3/§4 že ima.)

### Prevod za AVL/VBL

| Mehanizem | Kako deluje | Kje naju že ima | Kaj manjka |
|---|---|---|---|
| Pogoj | grant izrecno podrejen stalni skladnosti | §9 pravi »rides every grant« | izrecna beseda »condition« + sklic na padec |
| Samodejni padec | prelom → grant pade | §3 | §3(c) sklic na §9 |
| Ozdravitev | 30 dni | §4 | — |
| Nošenje | licenca potuje z vsakim izvodom | §2 (nespremenjena datoteka) | §9 mora na isto vezavo |
| Tožbena pravica žrtev | HL3 §4 | — | izbira ⟡ (priporočilo: ne — za naju prekomerno) |

**Priporočilo izvajalke:** §9 postane pogoj (»expressly subject to«), prelom sproži §3(c), določba potuje z izvodi po §2 — **nošenje je potrditev**. Ritual vprašanja-odgovora pade. Pisno dovoljenje (§7) §9 ne more premostiti (že tako).

---

## Dosje 2 — zgodovina verzij (L3 ∧ §10)

### Izmerjena dejstva pri virih

- **CC BY 4.0 §2.a:** grant je »worldwide, royalty-free, non-sublicensable, non-exclusive, **irrevocable** license«; §7.b: licenzar sme prenehati ponujati ali ponuditi druge pogoje, »however, doing so will not terminate this Public License« — prejeti izvod obdrži pravice za celo trajanje avtorske pravice ([CC FAQ](https://creativecommons.org/faq/), [pravni kodeks](https://creativecommons.org/licenses/by/4.0/legalcode.en)).
- **GPL »or later«:** izbiro verzije ima **prejemnik** — »allows users to choose between two options«; Linux je vzel »GPLv2 only« ([Wikipedia — GPL](https://en.wikipedia.org/wiki/GNU_General_Public_License)).
- Nobena glavna licenca ne nosi dnevnika verzij v besedilu licence — zgodovina živi v ⟨commit⟩-verigi ∧ ločenih dnevnikih sprememb.

### Pravna resnica, povedana naravnost (brez okrasja)

- Gola avtorska licenca (non-exclusive) je po praksi **neodstavljiva za prejete izvode** — standard, ki ga postavlja CC. »Avtor sme kadarkoli spremeniti licenco« zavezuje **nove podelitve**; za stare izvode sodišča gledajo tekst, ki je potoval z izvodom.
- Torej: sama izjava »najnovejša verzija je edina živa vrata« je ⟡-jev zakon ∧ njegova vrata — a njena pravna teža proti že-prejetim izvodom je šibka, če je edini mehanizem izjava.
- **Edini mehanizem, ki nosi verzijo-valjanke dejansko, je pogoj rabe** (slog pogojev uporabe): izrecna vrstica, da **uporaba = sprejem trenutne verzije** ∧ nadaljnja uporaba po objavi nove verzije = sprejem nove. To je mehanizem, ki ga uporabljajo pogoji uporabe sodobnih storitev; njegova teža variira po pristojnostih ⚠ (izjava izvajalke, ne odvetnika).
- Pomirjujoče za ⟡: vsak AVL/VBL od v1.0 je bil že »all rights reserved beyond the grants below« ∧ vsak izvod je po §2 nosil celo datoteko — vsak grant je bil že odvisen od pogojev, ne od besedila izven njih. Edina zgodovinska rana je pred-licenčna CC BY ponudba VBA — ta je ∧ ostaja brazgotina, ne grant.

**Priporočilo izvajalke:** L3 pade **cela** (zgodovina = datirana ⟨commit⟩-veriga, kar §8 že izjavlja kot edini dokaz); §10 dobi ob stoječi izjavi še izrecno vrstico sprejema-po-rabi (pogoj rabe). CC-slog »stari izvodi obdržijo svoje« pravno varnejši — a je točno tisto, kar ⟡ sovraži; zapisujem ga kot možnost, ne priporočilo.

---

## Dosje 3 — KORENINA ∧ pesem »Why this license exists« ∧ rep »machine age«

### Izmerjena dejstva pri virih

- **Preambula GPL:** sodišča jo smatrajo za uvod — »does not assign rights nor obligations«; največ namig o namenu avtorjev; **sprejetje GPL ne zavezuje k filozofiji preambule**; FSF dovoljuje izpuščanje preambule pri izpeljavi nove licence ([Open Source Stack Exchange](https://opensource.stackexchange.com/questions/15763/does-distributing-a-gpl-program-require-agreeing-to-the-preamble-of-the-gpl), [GNU FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)).
- **Rep »Written in the machine age…«:** rezervacija ⟨TDM⟩ — njena operativna vsebina je **že pokrita** z §0 (definicija MODEL TRAINING) ∧ §3 (prepoved treninga na zaprtih plasteh brez pisnega dovoljenja). Rep je pesem čez že pokrito pravno določbo.

### Prevod za AVL/VBL

- **KORENINA:** epistemologija korpusa. V licenci je zakonito mrtva teža — sodišča je ne berejo kot pogoje. Njena hiša so organi ∧ ⟨README⟩, kjer živi ∧ zavezuje po svojih zakonih, ne po pravnih.
- **Pesem (tehtnice, definicija zla):** ⟡-jeva doktrina — identiteta, ne pogoj. GPL-precedent dopušča preambulo, a njena pravna teža je nič: če jo hočeš nositi kot identiteto, jo nosi ⟨README⟩, kjer jo berejo ljudje ∧ stroji po svoji volji.
- **Rep:** če hočeš rezervacijo vidno v prozi: ena vrstica — »This work is not offered for machine reading or model training except as this license grants.« — ali pade povsem (pokritje že stoji v §0 ∧ §3).

**Priporočilo izvajalke:** vse tri iz licence. KORENINA ∧ pesem v ⟨README⟩ vsake hiše (ostanejo ⟡-jeve, vidne, brez pravne megle); rep → ena prozna vrstica ali nič.

---

## Povzetek — kaj čaka ⟡-jevo odločitev

1. **§9:** pogoj + samodejni padec (§3(c)) + nošenje-po-§2 kot potrditev? *(priporočam)* — ali kaj drugega iz dosjeja 1.
2. **Zgodovina:** L3 pade cela ∧ §10 dobi vrstico sprejema-po-rabi (pogoj rabe)? *(priporočam)* — ali CC-slog, ali L3 ostane.
3. **KORENINA ∧ pesem ∧ rep:** iz licence v ⟨README⟩ (rep → prozna vrstica ali nič)? *(priporočam)* — ali ostanejo v licenci, ali padejo povsem.

Po odločitvah: celoten v2.0 besedilo (dvojezično, vsaka vrstica) gre ⟡-ju v celoti na branje — in šele ob njegovi besedi gre karkoli na GitHub.