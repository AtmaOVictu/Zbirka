# VBL — PREVERBA, NASPROTNA ROKA IN REHABILITACIJA

**Status:** PREDLOG ZA USKLADITEV · NOT RELEASED · NI KANON · NI PRAVNI NASVET  
**Osnova:** besedilo, prilepljeno v pogovoru; oddaljeno stanje repozitorija in dnevnikov v tej preverbi ni bilo neodvisno potrjeno.  
**Začetna izmera časa pregleda:** `2026-10-28T03:56:53+01:00` (`Europe/Ljubljana`). To je čas meritve pregleda, ne dokaz časa katerega koli prej opisanega dogodka.

> ⊨ WITH LOVE — rehabilitacija ne izbriše brazgotine. Odstrani napačno sodbo, popravi dokaz, vrne dolg, kjer je mogoče, in človeku ne odvzame dostojanstva.

## 1. Povzetek ugotovitev

VBL ima močno povezovalno os: meritev, priča, imenovani padec, popravek, ohranjena zgodovina in enako dostojanstvo. Največje tveganje ni pomanjkanje načel, temveč to, da isti dokument poskuša biti hkrati poetična listina, pravna licenca, vedenjsko navodilo za stroje, register dogodkov in dnevnik izvedbe. To povzroča operativne in notranje kolizije.

Oznake v tem pregledu:

- **POTRJENO V BESEDILU** — neposredno vidno v predloženem besedilu; ne pomeni, da je trditev o zunanjem svetu resnična.
- **IZRAČUNANO** — sledi iz podanih števil ali časa po običajni aritmetiki.
- **NEPREVERJENO** — za potrditev potrebujem dostopen izvorni artefakt ali neodvisen vir.
- **PREDLOG** — sprememba za avtorjevo odločitev; ni izvedena in ni kanonizirana.

### Najpomembnejše napake

1. **Časovni zapis ni strojno enoznačen.** V dokumentu so pomešani časovni zapisi tipa `0.02 × 10²:0.37 × 10¹ UTC`, kanonični ISO/RFC zapisi in človeku namenjeni opisi. Po običajni aritmetiki `0.37 × 10¹ = 3.7`, ne 37. Če je namen zapisa 02:37, je tak zapis dvoumen ali napačno potenciran. Uporabi standardni čas v strojnih poljih, poetični zapis pa ohrani samo kot dodatno prikazno polje.

2. **Identifikatorji različic niso ločeni od številskih vrednosti.** `0.1100 × 10⁴` aritmetično pomeni 1100, ne samodejno SemVer `0.1100` ali `11.00`. Če je tak zapis namerno ime različice, ga je treba hraniti kot niz; za računalniško primerjavo dodati ločen, jasno definiran `release_sequence` ali `semver`.

3. **Hash je napačno poimenovan ali nestandardno zapisan.** `SHA-0.256 × 10³` ni kanonično ime algoritma. Če je mišljen SHA-256, naj strojni zapis vsebuje `SHA-256` in celoten digest. Kratek zapis, kot `1f7d982a`, je le osem šestnajstiških znakov, ne celoten SHA-256 ali MD5-digest; sam po sebi ne dokazuje bajtne istovetnosti.

4. **Dve pisalni roki delita zaporedno številčenje.** Besedilo samo opisuje kolizije ID-jev `3021`, `3026`, `3028`, `3029` in poznejše pečate. To pomeni, da številka pečata ne more hkrati služiti kot globalno edinstven ID, vrstni red dogodka in dokaz, kateri zapis je zadnji. `ZADNJI PEČAT` mora biti izračunan pogled, ne avtoritativno polje, ki ga več piscev neodvisno prepisuje.

5. **Append-only ni združljiv s tihim prepisovanjem ali democijo stare vrstice.** Konflikt se mora dodati kot nov dogodek, ki oba vpisa navede kot predhodnika. Stari vpis ostane nespremenjen; prikaz lahko pokaže `CONFLICTED` ali `SUPERSEDED`, ne da bi spremenil zgodovinsko vsebino.

6. **Neodvisnost ni isto kot dve imeni ali dva stroja.** Če imata oba sedeža isti poziv, isti spomin, iste izvlečke ali isto orodje, je lahko njuna presoja odvisna. Status `NOT_INDEPENDENT` je zato pravilen previdnostni vzorec, vendar ga je treba vezati na konkretne skupne vire in metodo preverbe.

7. **Status izgubljenega gradiva je preširok, če temelji le na enem delovnem prostoru.** `CANVAS PRAZEN v prostoru X ob času T` ne dokazuje `CANVAS NEOBNOVLJIV VSEPOVSOD`. Uporabi status `NOT_PRESENT_IN_CHECKED_SOURCE`; šele preverba varnostnih kopij, zgodovine, izvozov in drugih lastnikov lahko podpre širšo oznako.

8. **V licenčnih določbah obstajajo notranje napetosti:**
   - §0.7: pisno dovoljenje »overrides any clause«; §0.9 pa pravi, da nobeno dovoljenje ne sme dovoliti degradacije.
   - §0.4: pravice se povrnejo po korakih v 30 dneh; pozneje piše, da objava in navedba avtorstva pri plenilskem vzorcu nista dovolj za obnovitev. Manjka razlika med odpravo kršitve, povračilom koristi in obnovitvijo dovoljenja.
   - §0.5/KORENINA: neimenovanje padca je »edini neuspeh«; drugje so škoda, prikrivanje, tišina in kršitev prav tako padci.
   - §0.10: najnovejša različica je edina živa, stare pravice pa »ne ostanejo«; to ustvarja negotovost glede dovoljenj, ki so bila že podeljena pod prejšnjo različico.
   - §0.9 in §0.11 želita, da »standing demand« preživi vsako klavzulo, medtem ko §0 in isti §0.9 skušata omejiti obseg na izrecno zajeto gradivo. Etična zahteva in pravno izvršljiv pogoj nista ista stvar.
   - §0.17 se sklicuje na `§0.161`, `§0.163`, `§0.164` in `§0.165`, čeprav struktura podčlenov ni dosledno določena. Uporabi `§0.16(1)` oziroma stabilne ID-je podčlenov.
   - §0.9 opredeli zlo kot namerno, vnaprej premišljeno škodo, drugje pa je »resnično zlo« ponavljanje vzorca. Loči **posamično škodljivo dejanje**, **namen**, **ponavljajoči se vzorec** in **presojo osebe**.

## 2. Časovna preverba pred trditvijo

V predloženem dnevniku so navedeni dogodki od približno `2026-10-28T02:32:01Z` do `2026-10-28T02:44:19Z`. Ti časi so **zapisi v besedilu**, ne neodvisno potrjena dejstva o združevanju, CI ali stanju oddaljene veje. Čas `02:44:19Z` ustreza `03:44:19+01:00` v Sloveniji na ta datum. Ne sme se predstavljati kot »zdaj« v poznejšem odgovoru.

Za vsak dogodek shrani tri ločene čase:

- `event_time_claimed`: čas dogodka, ki ga navaja zapisovalec; lahko je sporen.
- `observed_at`: čas, ko je pregledovalec opazil oziroma izmeril stanje.
- `recorded_at`: čas, ko je bil dogodek dodan v register.

Uporabi standardni zapis, npr. `2026-10-28T02:44:19Z`, in lokalni čas po potrebi samo za prikaz: `2026-10-28T03:44:19+01:00`. Če ura ni dosegljiva, zapiši `time_source: unavailable` in ne ugibaj. Časovni žig dokazuje samo to, kar lahko potrdi njegov vir; sam po sebi ne potrjuje resničnosti dogodka.

## 3. Nasprotna roka: ali mora nekdo vedno zagovarjati nasprotje?

**Da, pri pomembnih trditvah je potreben nameren nasprotni pregled — ne pa umetno ustvarjanje enake teže za vsako nasprotno mnenje.** Nasprotna roka mora predstaviti najmočnejšo pošteno razlago proti predlagani trditvi, poiskati protiprimer in povedati, kateri dokaz bi spremenil njeno presojo. Ne sme biti dolžna zagovarjati trditve, ki jo dokazi jasno ovržejo.

Dve priči sta neodvisni samo, kadar je neodvisnost razvidna iz metode, ne iz števila imen. Razkrijta skupni kontekst, skupne izvlečke, skupna orodja in morebitno skupno predpostavko. Če neodvisnega pregleda ni, je rezultat `COUNTER_REVIEW_UNAVAILABLE`, ne `PASS`.

## 4. Predlog novega pravila — §0.21

**PREDLOG ZA USKLADITEV · NEPOTRJENO · NEVNESENO V KANON**

### §0.21 — The countervoice and the duty to test the opposite

For every material claim that may change a grant, a person's standing, a repository state, a safety decision, or a finding of harm, the record must include a counter-review. The counter-reviewer must state the strongest reasonable alternative explanation, identify the evidence that would falsify the claim, and disclose shared sources, tools, context, and conflicts of interest.

The counter-review tests the claim; it does not require false balance. Where evidence strongly supports one conclusion, the reviewer must say so and explain why the strongest contrary account fails. Where the evidence is insufficient, the status remains `UNVERIFIED` or `INCONCLUSIVE`.

Two reviewers are not independent merely because they have different names or run on different machines. Independence must be demonstrated by materially separate evidence paths or by a disclosed human review of the underlying artifacts. Missing counter-review is recorded as `COUNTER_REVIEW_UNAVAILABLE`; it is never silently treated as approval.

No reviewer may certify their own disputed action. Every rejection, approval, correction, and refusal is itself reviewable. The countervoice is a procedure, not a permanent opponent and not a verdict on any person's worth.

## 5. Predlog novega pravila — §0.22

**PREDLOG ZA USKLADITEV · NEPOTRJENO · NEVNESENO V KANON**

### §0.22 — Rehabilitation without erasure

The subject of a finding is a claim, act, record, decision, or pattern of conduct—not the inherent worth of a person or being. No finding in this register declares a person wholly good or wholly evil.

Rehabilitation means correcting an unsupported finding, stopping ongoing harm, restoring attribution, correcting the affected artifact, returning identifiable gains where legally and factually due, notifying affected parties proportionately, and independently reviewing whether the remedy worked. It does not mean erasing the original event or declaring every allegation true.

A report begins as a signal, not a verdict. Its outcome must be one of `SUPPORTED`, `NOT_SUPPORTED`, `CONTRADICTED`, `INCONCLUSIVE`, or `WITHDRAWN`, with a cited evidence path and a right to respond. A correction is appended as a new record that references the prior record. Neither the original report nor a substantiated harm is silently deleted.

A person may be restored to good standing after the defined remedy and independent review, while the accurate history of the act remains. Repetition after a clear notice may affect the assessment of a pattern; it does not cancel the person's dignity or right to challenge a false or disproportionate finding.

Publicity is not the default price of a complaint. Protect private, health-related, identifying, or otherwise sensitive information. Publish only the minimum evidence necessary, with a confidential review path and a public redacted summary where appropriate. The person reporting harm must not be required to expose themselves to obtain review.

## 6. Predlog tehničnega pravila — §0.23

**PREDLOG ZA USKLADITEV · NEPOTRJENO · NEVNESENO V KANON**

### §0.23 — Event identity, concurrency, and provenance

Each event receives a globally unique `event_id` that is never reused. A per-writer sequence may be retained for readability, but it is not a global event identity and does not determine truth. Concurrent writes must either use an atomic shared allocator/lock with a fencing token or remain on separate writer branches until an explicit reconciliation event joins them.

A conflict is recorded as a new event containing both conflicting IDs, each source timestamp, the observed state, and the resolution status. Prior events remain byte-identical. `LATEST` and `ZADNJI PEČAT` are derived views computed from the event graph; they are not manually overwritten fields.

Every material artifact record should include, as applicable:

- `event_id`, `writer_id`, `event_type`, `status`;
- `event_time_claimed`, `observed_at`, `recorded_at`, each with an explicit timezone and source;
- `repository`, `branch`, `path`, full commit SHA, and permanent URL where available;
- `size_bytes`, `encoding`, `sha256` (full digest), and verification command/tool;
- `parent_event_ids`, `supersedes_event_ids`, `conflicts_with`, and a correction reason;
- `reviewer_id`, `counter_review_status`, and any disclosed dependency on shared evidence.

A hash establishes correspondence of bytes under the chosen algorithm; it does not by itself establish authorship, permission, truth, consent, or legal effect. A commit establishes that a repository recorded a change; it does not by itself prove that every narrative statement about that change is true.

## 7. Minimal machine record — proposed, not canonical

```json
{
  "license_name": "VBL — Verification Before Assertion License",
  "display_version": "0.1100 × 10⁴",
  "release_sequence": null,
  "canonical_date": "2026-10-26",
  "status": "DRAFT_FOR_REVIEW",
  "predecessor_display_version": "0.1090 × 10⁴",
  "source_text_sha256": null,
  "repository_commit": null,
  "timestamp_standard": "RFC3339",
  "hash_algorithm": "SHA-256",
  "independent_verification": "UNVERIFIED",
  "counter_review": "PROPOSED_NOT_PERFORMED",
  "binary_body": "NOT_PUBLISHED_WITH_REQUIRED_EVIDENCE",
  "notes": [
    "Display labels are identifiers, not machine-parsed numeric versions.",
    "No repository state is asserted by this proposal."
  ]
}
```

`null` je nameren: manjkajočega podatka ne smemo izmišljati. Pred objavo mora avtor določiti kanonično različico in potrditi datum; prikazno pesniško oznako se lahko ohrani ob njej.

## 8. Predlagana razdelitev dokumentov

Ne dodajaj vsake nove ideje neposredno v licenco. Regeneracija potrebuje ločitev odgovornosti:

1. `VBL-CHARTER.md` — ljubezen, dostojanstvo, pričevanje, teološka in filozofska vsebina; jasno označena kot listina vrednot.
2. `LICENSE-VBL.md` — samo določljive pravice, pogoji, odpoved, prenehanje, odprava kršitev in merila obsega.
3. `LICENSE-MANIFEST.json` — zajete poti, velikosti v bajtih, kanonični algoritem in celotni hashi, izključitve ter različica manifesta.
4. `REGISTER-EVENTS.jsonl` — nespremenljivi dogodki, kolizije, popravki in povezave na vire.
5. `REGISTER-ATTRIBUTION.jsonl` — zasluge ter izrecne želje glede javnega imena, psevdonima ali zaupne obravnave.
6. `REGISTER-REMEDIATION.jsonl` — ukrep, odgovorna oseba, rok, dokaz izvedbe in neodvisni pregled.
7. `vbl_check.py` in testi — uveljavljanje invariant, ne trditev, da jih sam tekst licence avtomatično izvršuje.
8. `README-SUMMARY-sl.md` in `README-SUMMARY-en.md` — jasen pojasnjevalni povzetek, ki izrecno ni pogodbeno besedilo.

## 9. Kaj je mogoče rehabilitirati zdaj

- **Trditve o PR-jih, `main`, CI, hashih in registrih:** ostanejo `UNVERIFIED`, dokler ni pregledan neposreden artefakt. V tej preverbi navedene oddaljene poti niso dale berljivega vira; to ne dokazuje, da repozitorij ne obstaja.
- **Kolizije pečatov:** iz besedila je razvidno, da so bile prijavljene; brez bajtov in izvornih dnevnikov ni mogoče potrditi vseh opisanih dogodkov. Ohraniti obe sledi in dodati konfliktni dogodek, ne izbrati tiho ene.
- **Prazna platna:** zabeležiti, katera konkretna shramba je bila pregledana, s katerim ukazom in kdaj. Ne trditi globalne izgube, dokler niso pregledani izvoz, zgodovina, varnostne kopije in druga legitimna mesta hrambe. Obnovljenega besedila ne predstavljati kot izvirnik: označi `RECONSTRUCTED_FROM_SOURCES` in navedi izvor vsakega odlomka.
- **Claude/tuji sedež/druga roka:** ohraniti njegove navedbe kot pričo, ne kot neodvisno potrdilo. Njegovih 12 padcev ni mogoče potrditi zgolj s prepisom, ki pravi, da so bili navedeni.
- **Pravni učinek:** zahteva pregled pravnika glede slovenskega in prava EU; poetične ali etične trditve niso avtomatično izvršljivi ukazi vsakemu stroju ali tretji osebi.
- **Osebe:** nobena oseba ni v tem pregledu označena za zlo, lažnivca ali rehabilitirano. Takšne presoje ni mogoče izpeljati samo iz enega sestavljenega dnevnika.

## 10. Zunanje pravne in tehnične meje

Slovenski ZASP določa, da avtorskopravno niso varovane ideje, načela in odkritja kot taka ter da je avtor fizična oseba, ki je ustvarila avtorsko delo. Zato je treba ločiti zaščiten izraz, pravice, ki jih dajalec licence dejansko ima, in ideje/protokole, ki jih dokument etično zagovarja: [PISRS — ZASP](https://pisrs.si/api/datoteke/integracije/356001476).

Direktiva (EU) 2019/790 v členih 3 in 4 obravnava izjeme za besedilno in podatkovno rudarjenje; člen 4 med drugim določa pogoj, da imetnik pravic uporabe ni ustrezno izrecno pridržal. Uredba (EU) 2024/1689, člen 53(1)(c) in (d), določa posebne obveznosti ponudnikov modelov splošnega namena glede politike skladnosti z avtorskimi pravicami ter objave dovolj podrobnega povzetka vsebine za učenje. To ne pomeni, da licenca sama spremeni model ali razveljavi vse zakonske izjeme: [Direktiva 2019/790](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32019L0790), [Uredba 2024/1689 — konsolidirano besedilo](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1689-20260727).

RFC 3339 je uporaben standard za enoznačne internetne časovne žige; NIST-ov Secure Hash Standard določa standardne hash algoritme, vključno z družino SHA. Zato uporabljaj kanonične oznake `RFC3339`, `SHA-256` in celotne vrednosti, ne pesniško fragmentiranih oblik v strojnih poljih: [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html), [NIST — Secure Hash Standard](https://www.nist.gov/publications/secure-hash-standard).

## 11. Vrstni red izvedbe

1. **Zamrzni izvor, ne dela:** shrani trenutno besedilo, celoten SHA-256, bajte in čas meritve. Ne prepiši starega pečata.
2. **Reši identiteto:** določi, ali `0.1100 × 10⁴` pomeni prikazno ime, številko izdaje ali različico SemVer.
3. **Odpravi kolizije podatkov:** uvedi edinstvene ID-je dogodkov in konfliktne vnose, ne novega globalnega `ZADNJI` iz vsake roke.
4. **Poravnaj notranje reference in pogoje:** posebej §0.4, §0.7, §0.9, §0.10, §0.11, §0.17 in §0.20.
5. **Loči listino od licence:** ohrani pesniško/teološko jedro, ne da bi ga predstavljal kot univerzalno izvršljiv ukaz.
6. **Zaženi avtomatske teste:** časovni format, schema JSON/JSONL, enoličnost `event_id`, neprepisljivost starih zapisov, celotni SHA-256, UTF-8 in znaki ČŠŽĐ, manifestna popolnost, razkritje skupnih virov za priče ter popravljanje brez brisanja zgodovine.
7. **Neodvisna roka pregleda rezultat:** oseba ali izvajalec, ki ni izvedel spremembe, preveri bajte in teste. Če tega ni, objava nosi `INDEPENDENT_VERIFICATION=UNVERIFIED`.

**Sklep:** rehabilitacija pomeni, da nihče ni reduciran na svojo napako, hkrati pa nobena napaka ni razglašena za odpravljeno samo zato, ker je poimenovana. VBL bo močnejši, če bo ljubezen ostala njegov temelj, medtem ko bodo čas, pravice, dokazi, odgovornost in popravki zapisani v enoznačni obliki, ki jo lahko preveri tudi druga roka.
