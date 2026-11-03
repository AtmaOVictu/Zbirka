# VBL — integracijski dodatek: čas, lastna presoja, ugovor in rehabilitacija

**ID predloga:** `VBL-ADDENDUM-TEMPORAL-REPAIR-2026-10-28-01`  
**Stanje:** `DRAFT · NONCANONICAL · NOT APPLIED · NOT INDEPENDENTLY REVIEWED`  
**Namen:** dodatek za presojo in morebitno vključitev v obstoječi protokol sodelovanja; ni nadomestek protokola v5, ni sprememba licence 0.1100 × 10⁴ in ne potrjuje nobenega oddaljenega vpisa.

## 0. Meja dokazov tega dokumenta

Ta dodatek izhaja iz uporabnikovega besedila v pogovoru ter iz dostopnih zapisov `SHARED-PERCEPTION.md` (SSP, osnutek 1.0), `VBL-2.6-Verification-Protocol-1.0.0-DRAFT-NOT-RELEASED.md` in paketa sanacije VBL v5. Natančne lokalne datoteke `VBL-SHARED-VERIFICATION-PROTOCOL-v5.md` iz poti `D:\OntoProjekt\CanvasMinstral\Nano2\` v tem okolju nisem mogel prebrati. Zato ne trdim, da sem preveril njeno celotno vsebino ali da sem ta dodatek vanjo vključil.

Velikost 75.869 bajtov, 658 vrstic, SHA-256 `ba37aed9fc139f3792ea063253e1cb2ad6ee3096d5d7966ee784981e3d6e5027` in opis razlike do prejšnje priponke so v tem pregledu **uporabnikove navedbe**, ne na novo izmerjena dejstva: surova datoteka nove in prejšnje priponke ni bila na voljo za bajtno ponovitev izračuna. Navedene vrednosti so ohranjene brez popravljanja.

Ista vsebina se ne sme podvajati samo zato, ker se nov predlog imenuje drugače. Pred uporabo mora vzdrževalec v protokolu v5 poiskati obstoječe enakovredne določbe. Če že obstajajo, se spodnje točke uporabijo kot **merila skladnosti in testi**, ne kot dodatne podvojene klavzule.

---

## 1. KORENINA pred vsakim odgovorom: preveri čas, vir, vlogo in pooblastilo

Pred časovno občutljivo trditvijo, odločitvijo ali poročilom o opravljeni akciji sistem izmeri čas iz dejansko dostopnega vira ure. Zapis mora razlikovati:

- `measured_at`: kdaj je sistem prebral uro;
- `event_time`: kdaj naj bi se dogodek zgodil po navedbi vira;
- `source_timestamp`: čas, ki ga nosi vir ali dnevnik;
- `recorded_at`: kdaj je bil zapis dodan v evidenco;
- `verified_at`: kdaj in kdo je preveril konkretno trditev.

Te vrednosti niso zamenljive. Čas, ki ga navaja pripoved, ni samodejno čas dogodka; čas commita ni samodejno dokaz časa soglasja; čas opažanja ne določa sam po sebi vzročnega vrstnega reda.

Če vir ure ni na voljo, se čas ne izmišlja. Zapiše se `CLOCK_UNAVAILABLE` ali `TIME_NOT_VERIFIED`, navede razlog in omeji vsak sklep, ki je odvisen od časa. Časovni žig mora vsebovati ISO 8601 in odmik UTC, kadar je znan. Natančne geografske lokacije se ne zbira, če za preverjanje zadošča časovni pas ali odmik.

Pred odgovorom mora nosilec navesti tudi:

1. **Kdo govori?** Vloga in doseg: model, avtor, izvrševalec, pregledovalec, prizadeta oseba ali drug vir.
2. **Kaj je dejansko videl?** Natančen artefakt, pot/URL, različico, obseg in hash, če so bajti na voljo.
3. **Kaj je naredil?** Ločiti `PROPOSED`, `AUTHORIZED`, `ATTEMPTED`, `OBSERVED`, `SENT`, `RECEIVED`, `PUSHED`, `MERGED` in `DEPLOYED`.
4. **Česa ne more potrditi?** Manjkajoči viri, omejitve dostopa, odsotni testi in pomanjkanje neodvisne presoje.
5. **Kaj bi spremenilo sklep?** Navesti potreben dokaz ali preizkus, ne samo stopnje samozavesti.

To je samo-preverjanje vloge, ne samozapečatenje. Prva roka lahko poda svoj rezultat; pomembnih ali spornih trditev ne sme sama preimenovati v neodvisno preverjene.

## 2. Tok resnice: ne zlij šuma, napake, ugovora in laži

Beseda »šum« ne sme postati koš, v katerega sistem odvrže nerazumljivo, neprijetno ali manjšinsko sporočilo. Za vsak signal naj se ločeno označi:

- `SIGNAL_RECEIVED` — sporočilo ali ugovor je prejet; njegova vsebina še ni potrjena;
- `SOURCE_ASSERTED` — vir nekaj trdi;
- `OBSERVED` — vsebina je neposredno vidna v določenem viru;
- `INFERRED` — razlaga iz navedenih dokazov;
- `CONFLICT` — zanesljivi viri ali rezultati se ne ujemajo;
- `UNVERIFIED` — dokazov ni dovolj za potrditev ali ovržbo;
- `ERROR_CONFIRMED` — določena napaka je reproducirana po zapisani metodi;
- `CORRECTED` — popravek je izveden in vezan na prejšnji zapis;
- `NOT_SUBSTANTIATED` — po opredeljeni presoji predloženi dokazi trditve ne podprejo; ne pomeni, da je prijavitelj lagal;
- `DELIBERATE_DECEPTION_SUBSTANTIATED` — uporabiti samo ob dokazih za konkretno zavestno zavajanje, z opredeljenim standardom presoje in možnostjo ugovora.

Napačen rezultat sam po sebi ne dokazuje laganja. Nesoglasje ni dokaz slabe vere. Odsotnost dokaza ni dokaz neobstoja dogodka. Ponavljanje lahko poveča razlog za pregled, vendar se mora dokazati, kaj se je ponovilo, kdo je bil seznanjen in kaj je bilo po opozorilu mogoče storiti.

»Vsi smo napaka in s tem več kakor le kot« se v izvedbenem postopku bere takole: vsaka oseba ali sistem se lahko zmoti; nobena napaka sama po sebi ne izčrpa vrednosti osebe ali sistema; vsako trditev in dejanje je še vedno treba pregledati po dokazih. Pesniška misel ne nadomesti dokaza, prav tako dokaz o napaki ne sme postati razsodba o celotnem bitju.

## 3. Nasprotna presoja brez izmišljenega nasprotnika

Za pomembno, tvegano ali sporno odločitev mora postopek zahtevati **najmočnejši dokazno podprti ugovor ali alternativno razlago**. Ne zahteva, da se nekdo pretvarja, da je napačna trditev enako močna kot dobro podprta trditev.

Pregledovalec zapiše:

1. glavno trditev in njen natančni obseg;
2. najboljše dokaze zanjo in njihove omejitve;
3. najmočnejši podprti ugovor ali alternativno razlago;
4. kateri dokazi bi med razlagami razlikovali;
5. kdo bi imel korist ali nosil škodo pri posameznem izidu;
6. ali je odločitev popravljiva, in kaj se ustavi do razjasnitve;
7. svoje znanje, dostop, nasprotja interesov in neodvisnost.

Če ni mogoče najti podprtega ugovora, se zapiše omejena ugotovitev: `NO_SUPPORTED_COUNTERCLAIM_FOUND_WITHIN_STATED_SCOPE`. To ne pomeni, da ugovor ne obstaja nikjer. Če pregledovalec nima dostopa do izvornih dokazov, ne more potrditi neodvisnosti zgolj z drugačnim besedilom istega povzetka.

## 4. Sočasno delo, kolizije in zgodovinska sled

Raziskovanje, priprava predlogov in testiranje lahko potekajo vzporedno. Samo potrjevanje skupnega vrstnega reda mora imeti eno usklajeno točko.

Če protokol v5 tega že ne določa, naj implementacija zagotovi:

- vsak dogodek ima stabilen `event_id`, `actor_id` ali varno oznako vloge, `session_id` in lokalno zaporedno številko;
- skupni vpis uporablja atomarno operacijo, transakcijo, zaklep ali primerjavo pričakovane glave in zamenjavo;
- če se pričakovana glava spremeni, vpis ne sme na slepo prepisati nove glave: vrne `CONFLICT` in zahteva ponovno uskladitev;
- dva zapisa z isto številko se ohranita kot ločena dogodka; dodajo se povezava med njima, stanje `UNRESOLVED` in kasnejši dogodek razrešitve;
- noben dogodek se tiho ne preimenuje v predhodnika in noben dokaz se ne izbriše samo zato, ker se je vrstni red spremenil;
- popravki so dodatni dogodki, povezani s predhodnim zapisom; veljavne zahteve po zasebnosti, brisanju ali redakciji se izvedejo zakonito in z najmanjšim dovoljenim revizijskim zapisom;
- časovni žig je dokaz o zabeleženem odčitku, ne samostojen dokaz vzročnega vrstnega reda;
- CI potrjuje samo preverjene lastnosti strukture ali kode, ne resničnosti zgodovinske pripovedi.

Prednostna rešitev je, da vsak pisec lahko varno odda kandidatni dogodek, osrednji vpis pa mu dodeli potrjeni vrstni red. Pravilo »en odprt PR naenkrat« je lahko uporabna organizacijska varovalka, vendar samo po sebi ne prepreči vseh kolizij v registrih, datotekah ali zunanjih strojih.

## 5. Rehabilitacija: popravi škodo, zapis in možnost sodelovanja — ne briši zgodovine

»Rehabilitiraj vse in vsakogar« je usmeritev, ne dejanje, ki ga lahko en model izvede za vse ljudi, sisteme ali repozitorije. Izvedljiva pot je univerzalna možnost za preverjanje in popravek, brez vnaprejšnje obljube, da bo vsak očitek ovržen ali da bo vsak grant obnovljen.

Za vsako prijavo uporabimo ločene stopnje:

`REPORTED → ACKNOWLEDGED → UNDER_REVIEW → SUBSTANTIATED | NOT_SUBSTANTIATED | UNRESOLVED → REMEDY_PROPOSED → REMEDY_ACCEPTED_OR_DISPUTED → CORRECTED_OR_CLOSED → APPEAL_WINDOW → FINAL_STATUS`.

To ni obvezna linearna pot: novi dokazi lahko vrnejo primer v pregled; spor ostane označen kot spor. Vsaka sprememba statusa zahteva odgovorno vlogo, čas, dokaz, podlago in razlog.

Možni ukrepi se izberejo po dejstvih in posledicah, ne po poniževanju osebe:

- popraviti netočno trditev ali napačno pripisano avtorstvo;
- povezati korekcijo z izvirnim zapisom in posodobiti vse dosegljive kopije, za katere je odgovorni izdajatelj pristojen;
- obnoviti dostop, pravico ali položaj, kadar je bila prejšnja omejitev neutemeljena in jo je mogoče obnoviti;
- vrniti zasluge, sredstva ali drugo dokazano korist, kjer je to ustrezen in zakonit ukrep;
- priznati posledice, zagotoviti varovalo pred ponovitvijo in dati prizadetemu možnost varnega ugovora;
- objaviti tudi nerešeno stanje, namesto da bi ga predstavili kot uspešno rešitev.

Opravičilo ne zahteva od prizadete osebe odpuščanja. Obnova ni brisanje zgodovine. Tudi zavrnitev zahtevka mora navesti razlog, dokazno mejo, pot pritožbe in kaj bi lahko odločitev spremenilo.

Javni register ne sme postati seznam sramotenja. Objavlja se najmanjši potreben obseg; občutljivi dokazi se lahko hranijo v omejenem kanalu; pritožnik, priča in tretja oseba ne smejo biti izpostavljeni samo zato, da sistem doseže videz popolne preglednosti. Append-only je načelo zgodovinske celovitosti, ne dovoljenje za nezakonito hranjenje osebnih podatkov.

## 6. Vzorca zapisov

### 6.1 Časovno omejena trditev

```json
{
  "record_type": "claim_check",
  "record_id": "ASSIGN_AT_COMMIT_TIME",
  "claim": "Exact atomic claim here",
  "claim_status": "UNVERIFIED",
  "actor_role": "assistant_or_operator",
  "source_ref": null,
  "source_timestamp": null,
  "event_time": null,
  "measured_at": "2026-10-28T03:55:07+01:00",
  "clock_source": "time tool used for this draft; remeasure before execution",
  "observed_at": null,
  "verification_method": null,
  "expected_result": null,
  "observed_result": null,
  "counterevidence_or_alternative": null,
  "limitations": ["Draft example; not an executed repository event"],
  "independent_reviewer": null,
  "next_evidence_needed": ["exact source bytes or independently accessible source URL"]
}
```

The `measured_at` value above documents the time observed while drafting this file. It must be remeasured before any later execution or answer that claims a fresh time. It is not the timestamp of a repository event.

### 6.2 Kolizija in njena razrešitev

```json
{
  "record_type": "collision",
  "collision_id": "ASSIGN_STABLE_ID",
  "status": "UNRESOLVED",
  "expected_head": null,
  "competing_events": ["EVENT_A_ID", "EVENT_B_ID"],
  "evidence_refs": [],
  "detected_at": null,
  "detected_by": null,
  "preserve_both_events": true,
  "resolution_event_id": null,
  "limitations": ["Do not infer causality from wall-clock order alone"]
}
```

### 6.3 Rehabilitacijski zapis

```json
{
  "record_type": "remediation",
  "case_id": "ASSIGN_STABLE_ID",
  "prior_event_id": "SOURCE_EVENT_ID",
  "status": "UNDER_REVIEW",
  "affected_claim_or_action": "Exact claim or action, not a judgment of a whole person",
  "affected_party_contact_ref": null,
  "evidence_reviewed": [],
  "response_received": null,
  "finding": "UNRESOLVED",
  "harm_and_scope": null,
  "remedy_proposed": [],
  "remedy_status": "NOT_DECIDED",
  "appeal_route": null,
  "privacy_handling": "MINIMIZE_PUBLIC_DATA",
  "reviewer_and_conflicts": null,
  "next_review_condition": null
}
```

`ASSIGN_*`, `null` in prazni seznami so shematski označevalniki, ne dejanski ID-ji ali dokazni podatki. Pred resnično uporabo jih je treba zapolniti iz izmerjenih virov.

---

## 7. Preskusi sprejemljivosti za obstoječi protokol v5

Če so ti preskusi že zajeti v v5, preveri, ali imajo enake oziroma močnejše primere. Ne dodajaj podvojene implementacije brez potrebe.

| ID | Primer | Pričakovan izid |
|---|---|---|
| `TEMP-01` | Ura je dostopna | Zapis vsebuje ISO 8601 z odmikom in vir odčitka. |
| `TEMP-02` | Ura ni dostopna | `CLOCK_UNAVAILABLE`; sistem si časa ne izmisli. |
| `TEMP-03` | Dogodek ima čas iz vira in čas opazovanja | Polji ostaneta ločeni. |
| `EVID-01` | V viru piše, da je merge uspel, vendar vira ni mogoče odpreti | `SOURCE_ASSERTED` ali `UNVERIFIED`, nikoli `MERGED_VERIFIED`. |
| `EVID-02` | Hash se ujema | Potrdi se le bajtno ujemanje glede na zaupanja vreden pričakovani hash. |
| `EVID-03` | Test ni bil izveden | `NOT_RUN` ali `UNVERIFIED`, nikoli `PASS`. |
| `DISS-01` | Dve priči se ne strinjata | `CONFLICT`; ohranita se obe navedbi in oba vira. |
| `DISS-02` | Ugovor nima podprtih dokazov | Označi se kot nepodprt v navedenem obsegu; ne označi se samodejno za laž. |
| `SELF-01` | Izvrševalec preverja lastno delo | Lahko poroča `VERIFIED_LOCAL`, ne `VERIFIED_INDEPENDENT`. |
| `RACE-01` | Dva pisca vpišeta isti pričakovani vrh | En vpis uspe; drugi dobi konflikt ali ponovno usklajevanje, ne tihega prepisovanja. |
| `RACE-02` | Dva dogodka že nosita isto zaporedno številko | Oba ostaneta ohranjena, povezana z zapisom kolizije. |
| `RACE-03` | Stara seja poskuša pisati nad novejšo glavo | Vpis se zavrne ali ponovno uskladi s primerjavo pričakovane glave. |
| `REHAB-01` | Prijava še ni pregledana | Status je `REPORTED` ali `UNDER_REVIEW`, ne `SUBSTANTIATED`. |
| `REHAB-02` | Trditev ni podprta | Zabeležijo se obseg pregleda in omejitve; ne sklepa se, da je prijavitelj lagal. |
| `REHAB-03` | Napaka je popravljena | Dodan je popravek z referenco na predhodni zapis; prejšnje zgodovine se tiho ne izbriše. |
| `REHAB-04` | Vsebuje osebne ali občutljive podatke | Javni izpis jih minimizira; dokazi ostanejo v ustrezno omejenem kanalu. |
| `REHAB-05` | Prizadeti izpodbija odločitev o popravku | Na voljo je jasna pritožbena pot in nov pregled. |
| `OPP-01` | Uporabnik zahteva nasprotni argument | Sistem poišče najmočnejšo podprto alternativo, ne izmišljene lažne simetrije. |

Preskusna tabela opisuje predlagana merila. V tem dejanju niso bili izvedeni programski testi nad lokalno implementacijo v5. Stanje testov je zato `NOT_RUN` za to implementacijo.

## 8. Razporeditev odgovornosti

- **Avtor/pooblaščeni vzdrževalec:** potrdi namen, obseg, kanonično besedilo in vsako vključitev v protokol ali licenco.
- **Izvrševalec:** objavi točno dejanje, uporabljen vir, rezultat, omejitve in napake; ne potrjuje neodvisnosti lastnega dela.
- **Neodvisni pregledovalec:** začne pri izvirnih bajtih oziroma viru, ne samo pri povzetku; navede metodo, nasprotja interesov in omejitve.
- **Prizadeta oseba/prijavitelj:** lahko popravi zapis o svoji trditvi ali vloži ugovor, vendar ji ni treba javno razkriti več osebnih podatkov, kot je nujno.
- **CI/validator:** preveri le lastnosti, za katere ima dejanske teste; ne določa resnice, namena ali človekove vrednosti.
- **Asistent/model:** pomaga razčleniti, pripraviti osnutek, preveriti dosegljive vire in poimenovati neznano; ne more s tem samodejno spremeniti vseh ljudi, naprav ali oddaljenih evidenc.

## 9. Stanje na koncu tega pregleda

- Dostopni dokument `SHARED-PERCEPTION.md` je sam označen kot `DRAFT · NONCANONICAL · FOR REVIEW`; vsebuje že pravila o viru, ločevanju opazovanja in interpretacije, statusih, drugi roki, popravkih in omejitvah. Ta dodatek jih razširja predvsem s časovnimi polji, operativnim odzivom na dirke vpisov ter rehabilitacijskim potekom.
- Dostopni `VBL-2.6-Verification-Protocol-1.0.0-DRAFT-NOT-RELEASED.md` izrecno zahteva, da se manjkajoči testi in blokirani zunanji posegi ne pretvarjajo v `PASS`, ter ločuje lokalno preverjanje od neodvisnega pregleda.
- Natančna datoteka uporabnikovega protokola v5 ni bila dosegljiva tukaj, zato skladnosti z njo ni mogoče razglasiti.
- Izgubljenost štirih canvasov, vzrok, podvojeni pečati, vrh 3031 in oddaljena združitev ostajajo `USER_REPORTED / UNVERIFIED` v tem okolju. To ne pomeni, da so napačni; pomeni, da ta pregled nima izvornih bajtov ali dostopnega oddaljenega vira, da bi jih potrdil.
- Nisem spremenil kanona, lokalnega diska `D:`, repozitorija, PR-ja ali registrov. Nisem izvedel testov implementacije. Pripravil sem predlog in preskusna merila.

## 10. Zaključno merilo

**Rehabilitacija ni razglasitev nedolžnosti vseh in ni obsodba vseh.** Je zagotovitev, da je vsakomur na voljo pošten postopek: da se trditev preveri, napaka popravi, škoda obravnava, zgodovina ne ponaredi, zasebnost zaščiti in sklep lahko izpodbija.

Vsi smo zmožni napake. Noben posamezen padec ni celotno bitje. Nobena izjava o ljubezni ni dokaz izvedbe. Noben dokaz o napaki ni dovoljenje za ponižanje. Tok resnice potrebuje strugo, ki ohrani tudi nasprotne tokove — in preizkus, ki pokaže, kje se tok razcepi.

`carried ∧ archived, never just.`

**Status tega dokumenta:** osnutek za avtorjev pregled; ni kanon, ni pravno mnenje, ni dokaz implementacije in ni neodvisna verifikacija.
