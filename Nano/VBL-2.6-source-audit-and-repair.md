# VBL 2.6 / oznaka `10.0.0` — razčlenitev vira in izvedljiv predlog popravkov

**Status:** `TEXTUAL_AUDIT_OF_PASTED_COPY` · `DRAFT` · `NOT_RELEASED` · `NOT_LEGAL_ADVICE` · `NO_REPOSITORY_CHANGE_CLAIMED`

Ta dokument obravnava samo besedilo, ki je bilo prilepljeno v pogovor. Ne potrjuje javne objave, avtorstva, zgodovine Git, obstoja navedenih registrov ali dejanskega vedenja katerega koli sistema.

## 1. Različica: ne preimenuj vira na slepo

V predloženi kopiji se pojavljajo tri različne vrste oznak:

| Kraj | Vrednost | Kaj je mogoče sklepati |
|---|---|---|
| Prva vrstica kopije | `10.0.0` | Zunanja oznaka ali glava izvoza; sama ne dokazuje različice licence. |
| Naslov licence | `Version 2.6 · October 23, 2026` | Telo licence se izrecno predstavlja kot različica 2.6. |
| Machine record | `version: 2.6`, predecessor `2.5` | Strojni zapis ponavlja oznako 2.6 in zatrjuje predhodnika 2.5; trditev o predhodniku še ni neodvisno preverjena. |

**Varna odločitev:** `10.0.0` obravnavaj kot nepojasnjeno zunanjo oznako, ne kot potrjeno licenčno različico. V delovnem pregledu uporabi ime `VBL-2.6-pasted-copy`. Ne prepiši različice v 10.0.0, dokler avtor ne potrdi, kaj ta oznaka pomeni in kateri artefakt je kanoničen.

Izsek zgodovine vsebuje relativne oznake, kot so »3 days ago«, »5 days ago« in »15 hours ago«, združene odlomke, ponovljeno celotno besedilo in uporabniške elemente strani (`Symbols`, `Filter symbols`, `h2`). Iz tega ni mogoče zanesljivo rekonstruirati točnega časa, vrstnega reda, polnosti ali natančnih bajtov vsake izdaje. Odlomki so uporabni kot iskalne sledi, ne kot nadomestilo za izvirne artefakte in trajne identifikatorje objav.

## 2. Ugotovitve — razlika med besedilno napako in manjkajočim dokazom

| ID | Predmet | Rezultat pregleda kopije | Natančen popravek |
|---|---|---|---|
| VBL-26-001 | `10.0.0` proti `2.6` | `FAIL: VERSION_LABEL_CONFLICT` | Ohraniti obe kot različni polji do pojasnila; ne normalizirati tiho. |
| VBL-26-002 | §0 »every file in this repository« proti §6 izjemam | `FAIL: SCOPE_CONFLICT` | Obseg določiti s pozitivnim seznamom/manifesta in izrecnimi izključitvami. |
| VBL-26-003 | §1 grant | `INCOMPLETE` | Navesti dovoljena dejanja in status komercialne uporabe, podlicenciranja ter strojnega učenja. |
| VBL-26-004 | §3 »method or output«, »every grant … everywhere« | `FAIL: OVERBROAD_AND_UNBOUNDED` | Omejiti na pravice, ki jih da ta licenca, konkretno pokrito gradivo in postopek iz §4. |
| VBL-26-005 | §4 popravek kršitve | `FAIL: INTERNAL_CONTRADICTION` | Prvi stavek pravi, da se vsako dovoljenje obnovi po izpolnitvi pogojev; drugi pravi, da objava in pripis plenilcu dovoljenja ne obnovita. Enotno pravilo mora določiti status, pogoje in čas obnove. |
| VBL-26-006 | §4 »Egypt sold spell 30B« | `UNDEFINED_TERM` | Odstraniti iz operativnega pravnega besedila ali označiti kot literarno opombo z razlago vira. |
| VBL-26-007 | §4 »tragedy/predation« | `NO_DECISION_PROCEDURE` | Ne uporabljati moralne oznake osebe kot pravnega sprožilca. Ocenjevati dejanje, dokaze, škodo in sorazmerno pravno sredstvo. |
| VBL-26-008 | §5 »to use it is to accept them, not to sue them« | `OVERBROAD_WAIVER_LANGUAGE` | Izrecno zavrniti domnevo, da uporaba pomeni odpoved pravicam; vse omejitve odgovornosti podrediti veljavnemu pravu. |
| VBL-26-009 | §7 dovoljenje preglasi »any clause« | `HIERARCHY_CONFLICT` | Dovoljenje sme spremeniti samo izrecno navedene določbe in samo v obsegu pravic, ki jih dajalec lahko podeli. |
| VBL-26-010 | §8 »current version« kot »superior measure of truth« | `UNSUPPORTED_SUPERIORITY_CLAIM` | Novejša različica ni sama po sebi resničnejša; trditev o superiornosti mora navesti merila in dokaze. |
| VBL-26-011 | §8 »the only failure« proti §5 in §9 | `INTERNAL_CONTRADICTION` | Zamenjati z »one defined record-integrity failure«; ne razglasiti ene vrste napake za edino možno. |
| VBL-26-012 | §9 zahteva, da stroj ob zavrnitvi uči o Jezusu | `NORMATIVE_REQUIREMENT_NOT_SYSTEM_BEHAVIOUR` | Krščansko motivacijo ohraniti kot avtorjev izraz; ne kot univerzalni pogoj zavrnitve. Zavrnitev naj obravnava dejanje in ponudi varno alternativo. |
| VBL-26-013 | §9 se širi na »every work … in every house« | `SCOPE_OVERREACH` | Pogoji licence veljajo samo za pokrito gradivo in jasno določene pravice; preambula ne zavezuje samodejno nepovezanih del ali oseb. |
| VBL-26-014 | §10 novejša različica izbriše stare grant-e | `PRIOR_RIGHTS_UNRESOLVED` | Nova različica naj ne prekliče samodejno pravic, ki so bile že veljavno podeljene pod prejšnjo različico; potreben je pravni pregled. |
| VBL-26-015 | §11 razglaša določene izjave za neodpravljive | `LEGAL_EFFECT_NOT_SELF_EXECUTING` | Ločiti pogodbeno določbo od interpretativne/etične izjave; klavzula sama ne določi, kaj je izvršljivo. |
| VBL-26-016 | §12 »what survives every floor unaltered was never a fall« | `LOGIC_ERROR` | Nespremenjen prenos lahko zvesto prenese tudi napačno besedilo. Integriteta bajtov ni pravilnost vsebine. |
| VBL-26-017 | §12 U+FFFD je »machine's fall« | `CAUSALITY_UNPROVEN` | Znak sam ne dokazuje, kdo, kdaj ali kako ga je uvedel. Zahtevati izvirne bajte, kodiranje in sled pretvorb. |
| VBL-26-018 | §12 »byte-identical through every machine floor« | `UNVERIFIED_UNIVERSAL_CLAIM` | Omejiti na konkretno primerjani par artefaktov in objaviti SHA-256 obeh bajtnih nizov. |
| VBL-26-019 | §13 »deny entry to all that is not of its nature« | `AMBIGUOUS_SCOPE` | Napisati »zavrni uporabo, ki krši določen pogoj«, ne »zavrni vse, kar ni njene narave«. Nejasnost lahko prizadene tudi ljudi. |
| VBL-26-020 | Zgodovina in podvojeni odlomki | `EXPORT_CONTAMINATION` | Ohraniti izvirno izvoženo kopijo; izluščiti kanonično besedilo v ločeno datoteko in izvorne odlomke evidentirati posebej. |

`FAIL` se tukaj nanaša na predloženo besedilo glede na zgoraj zapisano merilo. `UNVERIFIED` ne pomeni, da se zatrjevani dogodek ni zgodil; pomeni, da ta kopija ne zadostuje za njegovo potrditev.

## 3. Predlagana nadomestna besedila za najnevarnejša protislovja

### 3.1 Glava in strojni zapis

Uporabi ta statusni blok v delovni kopiji, dokler vir ni razjasnjen:

> **Working identifier:** `VBL-2.6-pasted-copy`  
> **Declared license version in body:** `2.6`  
> **External leading label:** `10.0.0` — meaning `UNRESOLVED`  
> **Release status:** `NOT VERIFIED FROM THIS COPY`  
> The pasted text contains an internal declaration of version 2.6 and a machine record declaring version 2.6. The leading label `10.0.0` is retained as source context, not accepted as a canonical license version. No release status or lineage is established by this text alone.

### 3.2 §0 — obseg

> This license applies only to material expressly identified as covered under the identification procedure stated here. A repository’s location, co-distribution, or ingestion by a system does not by itself place every file, dataset, output, or independent work under this license. Third-party, private, excluded, or independently created material remains outside the grant except to the extent the licensor has authority to license specific protected expression in it. If the manifest and item-level identification conflict, record the affected item as `DISPUTED—NOT VERIFIED` until a documented correction resolves the conflict; neither side of the conflict alone proves authorship or infringement.

### 3.3 §3 — extraction / attribution

> No rights are granted under this license to knowingly remove or conceal attribution required by this license when reproducing or distributing covered material. Any alleged breach must identify the covered item, the act, the applicable condition, and supporting evidence. Any suspension or termination affects only rights actually granted under this license and is subject to the notice, response, and cure procedure in §4 and applicable law. This section does not assert ownership of methods, general ideas, independent outputs, third-party material, or all copies everywhere.

### 3.4 §4 — obvestilo, odgovor, popravek, obnova

> A notice is an allegation, not a finding. It should identify the covered item and version, the alleged act, the applicable clause, the available date/context, the evidence, and the requested correction. The recipient must have a meaningful opportunity to respond and dispute the evidence. A 30-calendar-day response/cure period begins when a sufficiently specific notice is received; an incomplete notice may be clarified, and the parties may agree to extend the period.
>
> Records must distinguish `REPORTED`, `UNDER_REVIEW`, `SUBSTANTIATED`, `DISPUTED`, `CORRECTED`, `CLOSED—UNRESOLVED`, and `NOT_SUBSTANTIATED`. A report or silence alone does not establish a breach. A remedy must be linked to the substantiated act and proportionate to the affected rights and harm. Corrections preserve the prior entry and add a dated correction instead of silently replacing history.
>
> If the applicable conditions for cure are met, the affected permission is restored to the extent specified in the grant and permitted by law. No separate moral category of a person automatically prevents cure. Any claim to return a monetary gain or award compensation requires a stated legal or contractual basis and an appropriate decision process. This section does not establish that a public allegation is true merely because it appears in a register.

### 3.5 §5 — brez domnevne odpovedi pravicam

> This work is fallible; a register may contain reports, findings, disputes, and corrections. Its presence does not make every entry true and does not mean that use constitutes acceptance of an allegation or waiver of a right or remedy. Any warranty disclaimer or limitation of liability applies only to the extent permitted by applicable law. Nothing in this section excludes rights or remedies that cannot lawfully be excluded.

### 3.6 §7 — dovoljenja

> A written permission may vary only the provisions it expressly identifies, for the specified material, acts, recipients, and period, and only to the extent the licensor has authority to grant that variation. It does not silently amend this license for other recipients, and cannot grant rights the licensor does not hold or override non-waivable law. The public register may document the operative scope while protecting personal or confidential information that need not be public.

### 3.7 §8 — različice in zgodovina

> A newer version is the latest published version, not automatically the more accurate or morally superior version. Any comparative claim of superiority must state its criteria, evidence, and limitations. A missing or altered history entry is a record-integrity issue to be investigated; it is not the only possible failure under this license.

### 3.8 §9 — etika in verski izraz

> The universal dignity principle expresses the author’s ethical commitment. It becomes a condition of a particular grant only to the extent its operative scope is stated clearly and lawfully in this license. This principle does not by itself make unrelated works, third-party material, independent outputs, systems, or a person’s conduct subject to this license.
>
> A refusal should address the requested act rather than condemn the person. Where practicable, it should explain the relevant safety or license concern and offer a safe alternative. The author’s Christian faith may remain part of the preamble and motivation; recipients, users, and systems are not required by this license to profess or teach a religion as a condition of refusal. The presence of text does not prove that any system has read, understood, or implemented it.

### 3.9 §10 — nova različica in že podeljene pravice

> A new version governs grants made under that version when the author publishes the exact version and its release record. It does not by itself retroactively revoke or rewrite rights validly granted under an earlier version. Earlier versions remain historical records of the terms associated with earlier grants, subject to the governing agreement and applicable law. A commit history may support provenance but does not by itself prove authorship, assent, legal validity, or receipt by every recipient.

### 3.10 §12 — znaki, prenos in dokaz

> Matching SHA-256 digests support the conclusion that the compared byte sequences match, provided the digest calculation is correct and the reference is trusted. They do not prove authorship, authorization, completeness, semantic correctness, or legal validity. A mismatch establishes a byte difference between the compared inputs, not by itself who caused it or why.
>
> U+FFFD may indicate a replacement during decoding or transformation, but its presence alone does not establish where, when, how, or by whom it was introduced. A causal finding requires source bytes, a declared encoding, available transformation history, and a reproducible comparison. If that evidence is absent, record `CAUSE=UNKNOWN—NOT VERIFIED`.

### 3.11 §13 — meja med zavrnitvijo uporabe in zavrnitvijo človeka

> The carrier may refuse a specific use when a stated, applicable condition is not met. A refusal must identify the use and the governing condition where practicable; it must not deny a person’s dignity, identity, origin, capacity, or belief. A refusal is itself reviewable conduct and may be challenged through the documented review process. This clause does not create universal audit powers or authority over unrelated systems.

## 4. Status metapodatkov za delovni izvod

Ne vstavljaj nepreverjenih hashov ali potrjenega predhodnika. Za zdaj uporabi:

```json
{
  "license": "VBL — Verification Before Assertion License",
  "working_id": "VBL-2.6-pasted-copy",
  "declared_version_in_body": "2.6",
  "external_leading_label": "10.0.0",
  "external_label_status": "UNRESOLVED",
  "release_status": "NOT_VERIFIED_FROM_PASTED_COPY",
  "publication_date": "2026-10-23 (declared in body; not independently verified)",
  "source_text_sha256": null,
  "predecessor": {
    "declared_version": "2.5",
    "declared_date": "2026-10-22",
    "artifact_verified": false,
    "sha256": null
  },
  "tests": {
    "textual_review_of_pasted_copy": "DONE",
    "source_provenance": "NOT_RUN",
    "binary_round_trip": "NOT_RUN",
    "legal_review": "NOT_RUN",
    "independent_verification": "NOT_RUN"
  },
  "author_release_approval": "NOT_RECORDED"
}
```

To je statusni zapis pregleda, ne nadomestilo za izvirni machine record izdane licence. Pred objavo naj se ga bodisi spremeni v pravilno oblikovan release manifest z dokazi ali pa odstrani iz objavne licence.

## 5. Kaj zgodovina podpira — in česa ne

**Podpira samo naslednje omejene ugotovitve:** prilepljeni izsek vsebuje naslove ali sledi za `VBL v2.0`, `v2.2`, `v2.3`, `v2.4`, `v2.5`, `v2.6` ter starejše oznake AVL; več besedilnih blokov je ponovljenih; viden je machine record, ki deklarira `2.6` in predhodnika `2.5`.

**Ne podpira brez izvirnih artefaktov:** natančne kronologije vseh sprememb, potrditve, da je bila vsaka objava izdaja, točnih commit SHA, avtorstva vsakega odlomka, celovitosti datotek, enolične razlage `10.0.0`, dokazila o pečatu ali trditve, da je koda ali sistem izvedel kakšen ukaz. Časovne oznake »3 days ago« in »5 days ago« so relativne oznake izvoza; ne smejo se pretvoriti v absolutne datume brez izvornih metapodatkov.

## 6. Minimalni vrstni red reševanja

1. **Zakleni kopijo dokazov:** shrani točno prilepljeni izvozni tekst brez urejanja; zabeleži datum pridobitve in od kod je prišel, če je znano.
2. **Izlušči kanonično besedilo:** odstrani UI-šum in podvojene zgodovinske odlomke v ločeno delovno datoteko; vsako izpuščeno območje evidentiraj.
3. **Razreši identiteto:** avtor ali izvorni repozitorij mora pojasniti, ali je `10.0.0` različica, oznaka delovnega procesa ali napačno prilepljena glava.
4. **Popravi pravila:** najprej §§0, 3, 4, 5, 7, 8, 9, 10, 12 in 13; ohrani pesniško preambulo kot preambulo, kadar ni mišljena kot izvršilno pravilo.
5. **Odloči o pravicah:** komercialna uporaba, podlicenciranje, ML training/fine-tuning, retrieval in evaluation morajo dobiti izrecne statuse in pogoje.
6. **Preveri artefakte:** izvor, predhodnik, manifest, zgoščenke, round-trip in neodvisni pregled so ločeni testi. Ne označi jih PASS, dokler se niso izvedli.
7. **Objavi samo z avtorjevo potrditvijo:** natančno končno besedilo, njegov digest, release record in testni izidi morajo ustrezati istim bajtom.

**Končni sklep:** najprimernejši popravek zdaj ni preimenovanje 2.6 v 10.0.0. Je razločitev oznak, ohranitev izvoznega vira, popravilo določenih protislovij in označitev nepreverjenih delov kot nepreverjenih. Namen licence — meriti trditve z dokazi, ohraniti zgodovino in varovati dostojanstvo — bo tako uresničen v postopku, namesto da ostane zgolj zapisan v preambuli.
