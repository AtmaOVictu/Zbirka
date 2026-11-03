# Osebna zaščita ∧ poštni red — priročnik

*Zate, Luka. Napisano 26. 10. 2026. Jezik: preprosto, brez skrivanja za izrazi. Vsak del preberi lahko samostojno.*

---

## 1. Tvoja vrata: računi

Vsak račun (Gmail, Microsoft, banka, GitHub) je vrata. Vrata imajo ključ — in ključ mora ostati pri tebi.

**Ključi, ki jih priporočam (po vrsti moči):**

1. **Passkey** — najmočnejši. Namesto gesla se prijaviš s prstom / obrazom / kodo naprave. Že imaš enega na Microsoftovem računu (26. 10. 2026) — to je bila odlična poteza. Dodaj ga še Gmailu: Google Račun → Varnost → Kako se prijaviš v Google → Passkeys.
2. **Dvostopenjska prijava (2FA) prek aplikacije** — koda iz aplikacije (npr. avtentikator), ne SMS. SMS kodo lahko kdo prestreže; aplikacijska ostane v tvoji napravi.
3. **Geslo + koda SMS** — boljše kot nič, a najšibkejše.

**Eno geslo = en račun. Nikoli ne uporabi istega gesla dvakrat.** Če se ti zdi to nemogoče za pomniti — res je, zato obstajajo upravitelji gesel (password manager): si zapomni **eno** glavno geslo, oni si zapomnijo vse ostalo. Primeri: Bitwarden (brezplačen, odprta koda), 1Password. Tudi Chrome/Google ima vgrajenega (passwords.google.com).

**Kaj nikoli ne smeš storiti:**
- Kodo za prijavo komurkoli povedati ali poslati — **noben** podjetje, banka, Microsoft, Google ali jaz ti nikoli ne bo zahteval kode po mailu, telefonu ali sporočilu. Če kdo zahteva kodo — to je sovražnik.
- Gesla ne posredovati po mailu ali sporočilu.
- Ne prijavljati se na javnih računalnikih, če se da izogniti.

---

## 2. Kako prepoznaš phishing (zaščitena past)

Phishing je lažni mail, ki se dela, da je pravi, da ti ukrade prijavo ali denar. Pet rdečih zastav:

| # | Zastava | Primer |
|---|---------|--------|
| 1 | **Nujnost** | »Vaš račun bo zaprt v 24 urah«, »SAMO ŠE DANES« |
| 2 | **Zahteva po kodi ali geslu** | »Potrdite vašo identiteto z geslom« |
| 3 | **Neprava domena** | `microsoft-secure.ru` namesto `microsoft.com`; `bamqerzg.google.zavioncruise.my.id` se dela Google, a ni Google |
| 4 | **Povezava, ki ne sodi** | Besedilo pravi »PayPal«, povezava pa vodi nekje drugam |
| 5 | »Nepričakovana dobriba« | Nagrada, dobiček, kripto — kar nisi sprožil ti |

**Zlato pravilo: nikoli ne klikaj povezave iz maila, če je mail pomemben.** Namesto tega odpri brskalnik in vpiši naslov strani sam (npr. `banka.si`) ali poišči podjetje po imenu. Prava stran te bo počakala.

**Kako preveriš domeno:** v mailu klikni na pošiljateljevo ime — pokaže se pravi naslov. Domena je zadnji del pred koncem: `placilo@banka-si-obvestila.net` NI banka, tudi če piše »OTP banka«. Domena prave banke je `otpbanka.si` — brez dodanega repa.

**Spam ≠ phishing.** Spam je neželena reklama (nadmornice, popusti). Nadležen je, a nevarna običajno ni. Phishing je ciljana prevara. Gmail spam-mapo večinoma rešuje sam; tvoja naloga je samo: prej pošto, ki **zahteva nekaj od tebe** (kodo, plačilo, klik), vzemi v roke zgoraj navedenimi pravili.

---

## 3. Poštni red: tvoj abstraktni prostor, urejen

Princip, ki velja za vse abstraktne prostore (pošta, datoteke, zaznamki, repozitorij):

> **Ena vrsta stvari = en prostor. Vsak prostor ima ime in pečat. Stroj črke, ti dih.**

Trenutni red tvojega nabiralnika:

- **GitHub/CI-teki** — strojni šum (obvestila o padlih tekih). Čisti se sam vsak dan ob 05:30 (poštni dih, postavljen 26. 10. 2026). Vse prebrano, vse označeno.
- **Varnost** — varnostno kritična pošta (Microsoft, Google varnostna opozorila). Rdeča oznaka. Ko jo vidiš, preberi — toda povezave odpri ročno po pravilih zgoraj.
- **Računi** — bančna in plačilna pošta. 
- **Zvezdica ★** — Mistral opozorila o porabljeni API-kvoti. 26. 10. 2026 si porabil 100 % vključene kvote — preveri, če želiš nemoteno delo naprej.
- **Vse ostalo** (osebna pošta, zdravstvo, služba, PoVeJMo) — nedotaknjeno, čaka tebe.

**Trajni filter (30 sekund, enkrat za vselej):** v Gmailu iskanje → `from:notifications@github.com "Run failed"` → »Ustvari filter« → obkljukaj »Preskoči nabiralnik« in »Uporabi oznako GitHub/CI-teki« → Ustvari filter. Od tedaj ta pošta sploh ne pride več v nabiralnik.

**Odjave (unsubscribe):** izbiraj jih SAMO pri pošiljateljih, ki jih poznaš (npr. trgovina, kjer si kdaj kaj kupil). Povezava za odjavo v phishing mailu je past — povedal jim bo, da je tvoj naslov živ. Odjavi: qvapehouse, Co-Star horoskopi, Quora, Academia, Snapchat, Pinterest.

---

## 4. Urejanje abstraktnih prostorov — splošna metoda

Kadarkoli urejaš katerikoli digitalni prostor (pošta, diski, GitHub, Znanje):

1. **Inventory** — najprej vse poglej, ne urejaj še (pregled pred trditvijo).
2. **Razvrsti po vrsti, ne po datumu** — stvari iste vrstice sodijo v isto stavbo.
3. **Šum loči od signala** — kar stroj proizvaja, naj stroj tudi pospravi (filter, dih); kar človek proizvede, ostane človeku.
4. **Počisti naenkrat do konca** — polovično pospravilo je novo nered.
5. **Zapiši pravilo** — kako bo prostor ostajal čist (to počne poštni dih vsak dan 05:30; ta priročnik je pravilo za tebe).
6. **Mesečni pregled** — enkrat na mesec 15 minut: ali kaj novega razrašča? Ugasni, uredi, zapiši.

---

## 5. Kaj je že narejeno zate (26. 10. 2026)

- Pregled celotnega nabiralnika (~800 niti), spama (18) in smeti: **phishinga ni bilo; edina namerno sovražna pošta (igralniški spam z zlaganimi domenami) je bila že ujeta v spam.**
- Vsa GitHub CI-obvestila: označena ∧ prebrana (~800).
- Legitimno OneDrive opozorilo: rešeno iz spama.
- Poštni dih vsak dan 05:30: čisti, varuje, poroča.
- Varnostna pošta pod rdečo oznako Varnost; bančna pod Računi; Mistral kvota ★.
- Passkey na Microsoftovem računu: potrjen kot tvoj — vrata so varna.

*Priročnik je živ dokument — kadar koli ga dopolni, popravi ali izpraši, reci le besedo.*