# Šiv 3 · Znamenje izven tabele
### matematika × jezikoslovje — prvi šiv, izrečen

**Vrstica poti · KAM:** rez med dvema disciplinama, ki sta obe izrekljivi v isti rani: tabela, ki obljublja vse znake, in znamenje, ki obstaja zato, ker ga v tabeli ni. **ZAKAJ:** zemljevid stičišč je obljubil poglavje za vsak šiv; ta šiv je prvi, ker se tesni s telesom, ki ga ravno piševa (UTF-8: prostor 0x10FFFF je tabela, tofu je znamenje brez telesa). **ČEMU:** dar — po tem telesu bralec vidi, da Cantor, Saussure, Gödel in Thompson/Pike niso štirje možje, ampak en rez skozi štiri stoletja.

**Enostavno prvi:** obstaja preprost trik, s katerim iz vsake tabele, ki trdi, da vsebuje vse, narediš eno vrstico, ki je v njej ni. Ta trik so matematiki imenovali diagonalni argument, jezikoslovci pa ga izrekajo vsakič, ko rečejo: pomen ni v znaku, ampak v razliki. To telo pokaže, da je to isti trik.

⧖

## 1. ORGAN — dve rani, en rez

**Cantor (1891):** predpostavi tabelo vseh neskončnih vrstic nič in enck. Nato zgradi novo vrstico: na mestu *n* vzame *n*-ti znak *n*-te vrstice in ga obrne (0↔1). Ta vrstica se od vsake vrstice razlikuje na vsaj enem mestu — torej je ni v tabeli. Tabela, ki je obljubila vse, je izgubila ob prvem dotiku.

**Saussure (1916):** v jeziku ni pozitivnih izrazov — samo razlike. Znak *pes* ne pomeni psa zaradi svoje oblike (oblika bi lahko bila katera koli), ampak zato, ker **ni** *pes, *pes*ma, *pas* (v sosednjem jeziku pas!), *les*. Pomen ni v celici tabele — pomen je razlika, ki jo celica ne more nositi sama.

**Ena poanta:** Cantorjeva diagonalna vrstica »se razlikuje od vsake vrstice« je strukturno enaka Saussurejevi trditvi »znak se razlikuje od vsakega drugega znaka«. Oba sta ista zakona izrekla na svojem substratu: **celoten sistem določajo robove, ne vsebine.**

⧖

## 2. PRAKSA — kje ta rez reže vsak dan

- **Geslo, ki ga ni v slovarju:** pomen nove besede (npr. *zlovenščina* v Lukovem korpusu) ni v nobeni tabeli — obstaja zato, ker se razlikuje od vseh obstoječih. Jezik je Cantorjeva vrstica v nastajanju: vsak nov govor doda znak, ki ga tabela še ni pričakovala. Zato slovarji zaostajajo — ne iz lenkosti, ampak po zakonu: tabela lahko zapiše le preteklo diagonalo.
- **Ime, ki ga podatkovna baza zavrne:** obrazec pravi »to ime že obstaja« — baza je tabela; človek, ki nosi isto ime z drugo življenjsko potjo, je Saussurejeva razlika, ki jo celica ne more izmeriti. Isti niz bajtov, drugi pomen.
- **Emoji, ki ga ni bilo, ko je bil napisan dokument:** 😄 (U+1F604) je bil dodan leta 2010. Dokument iz leta 1999, ki bi ga vseboval, je nemogoč — prostor je imel luknjo, ki jo je šele pozneje napolnil Unicode. Tabela živi: ∂ prostora se premika.

⧖

## 3. MAŠINERIJA — trije izreki istega reza

### 3.1 Cantor (neskončna tabela)
```
za vsako vrstico n:
  novi_znak[n] = obrni(tabela[n][n])
→ novi_znak se razlikuje od vsake vrstice na mestu n
```

### 3.2 Gödel (sistem, ki govori o sebi)
Vsakemu stavku v sistemu priredi številko (kodiranje — prednik UTF-8!). Nato zgradi stavek: »Ta stavek v tem sistemu ni izpeljiv.« Če ga izpelje, je laž; če ga ne, je resnica, ki je sistem ne izreče. Diagonalni trik: vrstica, ki govori o svoji lastni vrstici. Σam\_\_sklic je diagonalna poteza.

### 3.3 Saussure (tabela pomenov)
```
pomen(znak) = ∅ − vsi ostali znaki
pomen ni vsebina celice; pomen je ∆ med celico in obodom
```
Izrek v simbolu sistema: **pomen = ∆(znak, obod)** — pomen je vektor od znaka proti vsem, kar znak ni. Znak je ∅ brez svojega oboda: tabela sama po sebi je tišina ⧖, ki čaka prve sosede.

### 3.4 Turing (tabela vseh programov)
Predpostavi tabelo vseh programov. Zgradi program D, ki na programu št. *n* stori nasprotno od programske št. *n* (če se ta ustavi, D teče večno; če ta teče, D se ustavi). D ni v tabeli. Stop-problem je diagonalni argument, izrečen v bajtih.

⧖

## 4. DOKAZI — naloge, ki jih telo izmeri

**N1. Cantor peš na treh vrsticah.** Tabela: `010`, `101`, `110`. Zgradi diagonalno vrstico in preveri, da ni nobena od treh.
*Rešitev:* diagonala = 0., 0., 0. → obrnjeno: `111`. Ali se razlikuje od `010`? Da (mesto 1). Od `101`? Da (mesto 2). Od `110`? Da (mesto 3). **Ni v tabeli.** ⊢

**N2. Saussure na slovenskih besedah.** Izreči pomen besede *svet* (kot nasprotje *tema*) in nato *svet* (kot nasprotje *vojna*). Kje je pomen?
*Rešitev:* isti niz bajtov (73 76 65 74), dva pomena — pomen nosi obod (sosedi), ne celica. Ena beseda, dve diagonali: dokaz, da pomena ni v bajtih.

**N3. UTF-8 kot Gödelovo kodiranje.** Stavek »to število ni v tabeli« zapiši kot številko (npr. po seštevanju kodnih točk). Kaj je skupnega Gödelovem kodiranju in UTF-8?
*Rešitev:* oba preslikata jezik v številke, da bi sistem lahko govoril o sistemu: Gödel — aritmetika o ariitmetiki; UTF-8 — računalnik o vsem jeziku sveta. Skupni prednik: **beseda, ki postane številka, da jo stroj lahko odpre nazaj.**

**N4. Anti-represijska preverba (A9).** Kaj prereže diagonalni argument, kar bi spoznal brez njega? *Rešitev:* nič — kdor ne ve za diagonalni argument, verjame, da lahko popolna tabela obstaja (katalog vseh znakov, slovar vseh pomenov, seznam vseh resnic). Po tem telesu ve: vsaka tabela je diagonalno ranljiva — in to ni napaka tabel, ampak njihova življenjska meja.

⧖

## 5. ODPRTA ∂ — kje šiv ostaja šivalen

Diagonalni argument odpira vprašanje, ki ga sam ne more zapreti: **če se vsak sistem razlikuje od sebe po diagonali, kje je tedaj identiteta?** Ontofíza odgovarja: JAZ = fix(∫∘T∘W) — identiteta kot fiksna točka navitosti, ne vrstica v tabeli. A odprto ostaja: ali je tudi fiksna točka le še ena vrstica, ki čaka svojo obrnjeno kopijo? To je naslednji šiv: **ontomatematika × matematika** — fiksna točka, ki se zna sama nositi.

⧖

## 6. VIRI

- Cantor, G. (1891) — »Über eine elementare Frage der Mannigfaltigkeitslehre«: rojstvo diagonalnega argumenta.
- Saussure, F. de (1916) — *Cours de linguistique générale*: pomen kot razlika, brez pozitivnih izrazov.
- Gödel, K. (1931) — nepopolnost: samosklic kot diagonalna poteza.
- Turing, A. (1936) — stop-problem: diagonalni argument, izveden v programih.
- Ontofíza (korpus Self): diagonale kot jedro argumentacije; pomen = ∆(znak, obod); JAZ = fix(∫∘T∘W).