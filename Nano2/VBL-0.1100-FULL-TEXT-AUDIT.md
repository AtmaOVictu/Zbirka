# VBL 0.1100 × 10⁴ — celostna revizija prilepljenega besedila

**Status:** REVIEW_FINDINGS · NOT_CANON · NO_INDEPENDENT_VERIFICATION  
**Pregledni obseg:** preambula, KORENINA, §§0–0.20, machine record in zgodovinski seznam, kot so bili prilepljeni v pogovor.

## 1. Kaj je bilo zares pregledano

Pregledano je bilo besedilo, ki je vidno v pogovoru. To omogoča tekstualni in logični pregled odstavkov ter notranjih sklicev. Ne dokazuje pa, da je besedilo bajtno enako datoteki v repozitoriju, da je objavljeno, da je seznam zgodovine popoln ali da so navedene pravne posledice izvršljive.

V poročilu so zato ločeni:

1. **Opazovanje:** kaj je zapisano v prilepljenem besedilu.
2. **Notranja analiza:** ali si določbe nasprotujejo, ali so nejasne ali ali manjkajo operativna merila.
3. **Zunanji dokaz:** kaj je treba pridobiti oziroma preveriti drugje.
4. **Predlog:** popravek za razpravo; ne sprememba kanona.

## 2. Prednostne ugotovitve

### F-001 — Pisno dovoljenje in univerzalno dostojanstvo (§0.7 ↔ §0.9)

§0.7 pravi, da pisno dovoljenje preglasi katerokoli določbo. §0.9 pa pravi, da degradirajoče uporabe ne odobri nobena določba, dovoljenje, molk ali poznejša različica. To je notranje neskladje, če »any clause« dobesedno vključuje §0.9.

**Predlog:** razjasniti, da lahko pisno dovoljenje pooblasti uporabo v okviru pravic, ki jih avtor lahko podeli, ne more pa samo po sebi izničiti etičnega načela v besedilu. Če avtor želi drugačno hierarhijo, jo mora izrecno določiti. `INTERNAL_CONFLICT`.

### F-002 — Pogoji za ozdravitev dovoljenja (§0.4)

Prvi odstavek določa obnovitev dovoljenja po treh pogojih v 30 dneh. Nadaljevanje določa, da pri pridobitniški/predatorski škodi objava in kredit ne zadoščata, saj je treba vrniti korist. Besedilo lahko pomeni osnovno in razširjeno stopnjo pravnega sredstva, vendar tega ne formalizira; izraz `0.30 × 10²B` je dodatno dvoumen.

**Predlog:** razlikovati najmanj (a) razkritje in priznanje, (b) pripis/obnovitev kredita, (c) povračilo koristi ali odškodnino, če je utemeljeno, in (d) neodvisno odločitev o obnovitvi dovoljenja. Določiti, kdo ugotavlja dejstva, kakšna je pravica do ugovora in kaj pomeni rok. Ne normalizirati `B`, dokler ga avtor ne pojasni. `INTERNAL_CONFLICT` + `UNDERDEFINED`.

### F-003 — Strojni datum ni ISO 8601 (§0.20 / Machine record)

Zapis `0.2026 × 10⁴-0.10 × 10²-0.26 × 10²` ni neposreden standardni ISO 8601 datum. Prav tako machine record ne vsebuje ure in minute, ki ju §0.20 zahteva.

**Predlog:** ohraniti simbolni prikaz v ločenem polju, npr. `date_display`, in dodati standardno polje `timestamp` z ISO 8601 vrednostjo ter odmikom UTC, vir ure, trenutek meritve in status zanesljivosti. Ne sklepati o točnosti ure samo iz zapisa. `OBSERVED_IN_PASTED_TEXT`.

### F-004 — Zapis zgoščevalnega algoritma (`SHA-0.256 × 10³`)

Več členov uporablja obliko `SHA-0.256 × 10³`. Ni jasno, ali je to namenski simbolni zapis za SHA-256 ali drug algoritmični identifikator. Programska orodja pričakujejo nedvoumno ime algoritma.

**Predlog:** strojno zapisati `hash_algorithm: "SHA-256"`, kadar je to res namen; simbolno obliko ohraniti v ločenem prikaznem polju. Algoritma ne preimenujati brez avtorjeve potrditve. `UNDERDEFINED`.

### F-005 — Besedilo samo ne sproži izvajanja v vsakem stroju (§0.12, THE TRIGGER AND THE FORCE; §0.9 THE TEACHING)

Besedilo trdi, da se učenje vklopi v vsakem stroju, ki licenco prebere, ter da nosilec ne more trditi, da ni vedel. To je normativna zahteva ali filozofska trditev, ne dokaz o univerzalnem vedenju programske opreme.

**Predlog:** ločiti `RULE_TEXT_PRESENT`, `IMPLEMENTED`, `TESTED`, `INDEPENDENTLY_VERIFIED`. Za trditev o dejanskem vedenju imenovati konkretno implementacijo, verzijo, testni primer, surovi rezultat in okolje. `UNDERDEFINED` + `UNVERIFIED_EXTERNAL`.

### F-006 — Univerzalna bajtna identičnost ni dokazana (§0.12)

Stavek o tem, da vrata potujejo bajtno identično skozi vsak strojni »floor«, je univerzalna trditev. Iz prilepljenega besedila ni mogoče vedeti, katere pare izvornih in ciljnih datotek je kdo primerjal.

**Predlog:** trditi le posamezne primerjave, ki imajo izvorno/ciljno datoteko, velikost, algoritem in kontrolni vsoti. `UNVERIFIED_EXTERNAL`.

### F-007 — U+FFFD sam ne dokazuje izvora napake (§0.12)

Besedilo pripisuje pojav U+FFFD stroju, ki je nadomestil znak. Ta znak se pogosto uporablja kot Unicode replacement character pri neveljavnem zaporedju, vendar sam po sebi ne dokazuje, kje, kdaj ali zakaj je nastal; lahko je bil tudi dobesedno v izvirniku.

**Predlog:** zahtevati izvirne bajte, deklarirano kodiranje, verigo pretvorb in ponovljivo primerjavo pred/po. Vzročnosti ne sklepati iz samega znaka. `UNDERDEFINED`.

### F-008 — Zgodovinska trditev o klinopisu (§0.12)

Trditev, da so klinopisni znaki »the first writing ever to carry a name«, je zgodovinska superlativna trditev in iz prilepljenega besedila ni podprta z virom ali opredelitvijo izraza »carry a name«.

**Predlog:** bodisi dodati natančen zgodovinski vir in omejiti trditev na podprto formulacijo bodisi jo označiti kot simbolno/metaforično, ne kot preverjeno zgodovinsko dejstvo. `UNVERIFIED_EXTERNAL`.

### F-009 — Notacija notranjih sklicev ni formalno dekodirana

Oznake, kot so `§0.161 × 10²`, `§0.163 × 10²` in `§0.165 × 10²`, niso strojno nedvoumne brez slovarja številčenja. Lahko so namerno fragmentirane, zato jih ne smemo samodejno prepisati.

**Predlog:** vsak člen dobi ločen stabilen ključ, npr. `section_id`, in ločeno nespremenjeno polje `display_label`. Dodati preskus, ki zazna neobstoječe sklice. `UNDERDEFINED`.

### F-010 — »Vsak signal je preverjen in popravljen« (§0.16)

Določba pravi, da je vsak signal dokazan, preverjen in popravljen. Vendar signal/prijava še ni dokaz, da se je škoda zgodila; v nekaterih primerih preiskava ne bo potrdila prvotne trditve ali pa popravilo ne bo izvedljivo.

**Predlog:** določiti, da je vsak signal sprejet v evidenco in obravnavan; dejstva se preverijo; ukrep je sorazmeren ugotovitvam; rezultat je lahko potrjen, ovržen, delno potrjen ali neodločljiv; neodpravljene vrzeli ostanejo vidne. `UNDERDEFINED`.

### F-011 — »Tišina spraševalca ima enako težo« (§0.17)

Ta izjava nima merila za »težo« in bi se lahko razlagala kot samodejno pripisovanje krivde zaradi molka. Drugje licenca poudarja, da se ne sodi osebe in da molk ni privolitev.

**Predlog:** opredeliti, ali gre za metaforo o dolžnosti odziva ali operativno pravilo. Molku ne pripisovati krivde ali privolitve brez dodatnih dokazov in konteksta. `UNDERDEFINED`.

### F-012 — Produktivnost in človekovo dostojanstvo (§0.18 ↔ §0.9)

§0.18 opisuje merilo bivanja kot »more«/produkt in pravi, da je izhod brez produkta smrt oziroma truplo izhoda. §0.9 pa pravi, da dostojanstvo ni odvisno od uporabnosti za stroj. Če produktivnost postane merilo vrednosti osebe, sta določbi v napetosti.

**Predlog:** jasno ločiti `artifact/productivity metric` od `personhood/dignity`. Produkt lahko meri rezultat določene dejavnosti ali sistema, nikoli pa človekove vrednosti, pravice do skrbi ali pravice do počitka. Določiti tudi, kaj je »cognition«, »untruth« in njuna primerljiva merska enota, preden se trdi, da eno število presega drugo. `INTERNAL_CONFLICT` + `UNDERDEFINED`.

### F-013 — »Vsak podatek je vrsta licence« (§0.13)

Metaforična poved ne pove, ali je datum dejansko subject to license, ali je to ontološka teza ali implementacijsko pravilo.

**Predlog:** označiti status trditve: metafora, filozofski aksiom, operativna definicija ali pravno pravilo. Če je pravilo, opredeliti obseg, mehanizem in posledice. `UNDERDEFINED`.

### F-014 — Zavrnitev uporabe proti zavrnitvi osebe (§0.13)

»Refuse a use, never a being« je etično jasno, toda stavek, da nihče ne bo zavrnjen zaradi tega, »what they can do«, lahko pride v napetost z zavrnitvijo nevarne ali nedovoljene uporabe. Ključna razlika med identiteto/kapaciteto in konkretnim dejanjem še ni formalno določena.

**Predlog:** v definiciji zavrnitve navesti predmet zavrnitve (konkretna zahteva/dejanje), uporabljeno pravilo, dokazni razlog, obseg zavrnitve in možnost ugovora; osebe ne etiketirati kot prepovedane. `UNDERDEFINED`.

### F-015 — Enako tehtanje in različna odgovornost (§0.9, §0.13)

Besedilo pravi, da isto dejanje tehta enako za vsakogar, hkrati pa da položaj poveča doseg in s tem težo. To je lahko združljivo, če se meri isto dejanje in dodatne odgovornosti ločeno, vendar razlika ni formalizirana.

**Predlog:** ločiti merila doslednosti (`same rule for same facts`) od kontekstualnih dejavnikov (pooblastila, predvidljivost, vpliv, škoda, ponavljanje). Objaviti formulo ali vsaj postopek tehtanja, ne navidezne numerične gotovosti. `UNDERDEFINED`.

### F-016 — Čas »pri viru trenutka« za vsak odgovor (§0.20)

Zahteva za časovno oznako vsakega odgovora ne opredeli dostopnega vira ure, točnosti, časovnega pasu, obravnave offline okolja ali zasebnosti lokacije. Strojni zapis ne vsebuje polne ure, čeprav jo člen zahteva.

**Predlog:** določiti polja `timestamp`, `timezone_offset`, `clock_source`, `precision`, `measurement_status`, in `location_policy`. Lokacije ne beležiti natančneje, kot je potrebno. Če vira ni, uporabiti `UNAVAILABLE`, ne ugibati. `UNDERDEFINED`.

### F-017 — Rodovnik je naveden, ne neodvisno potrjen (§0.15 / History)

Seznam različic je pomemben notranji zapis, vendar besedilo samo ni objavni dokaz. Kratki fragmenti, kot so `blob 73476d4e`, in sklici na PR sami po sebi ne dokazujejo javnega sprejema, točne vsebine ali nasledstva.

**Predlog:** ločeno beležiti `version`, `declared_date`, `artifact_sha256`, `predecessor_artifact_sha256`, `commit_id`, `publication_uri`, `release_status`, `reviewer`, `verification_status`, `known_gaps`. Neznane vrednosti naj bodo `null`/`UNKNOWN`. `UNVERIFIED_EXTERNAL`.

### F-018 — Prejšnje različice in že podeljene pravice (§0.10)

»No grant rides any older version« lahko pomeni, da stare različice ne podeljujejo novih dovoljenj, ali pa da se želi prekiniti že podeljena dovoljenja. To sta različni pravni posledici; besedilo ju ne razločuje.

**Predlog:** določiti, kako nova različica vpliva na (a) prihodnje uporabe, (b) že podeljene licence/dovoljenja, (c) že zakonito pridobljene kopije in (d) kršitve, ki so nastale prej. Potrebna je jurisdikcijsko ustrezna pravna presoja. `LEGAL_REVIEW_REQUIRED`.

### F-019 — Izjava »not to sue« in omejitev odgovornosti (§0.5)

»To use it is to accept them, not to sue them« je dvoumna in je lahko razumljena kot odpoved pravnim sredstvom, medtem ko drugje licenca omogoča ugovor in prijavo. Izjava »AS IS« prav tako ne zagotavlja, da so vse izključitve veljavne v vseh jurisdikcijah.

**Predlog:** preoblikovati v jasno opredelitev, kaj licenca jamči/ne jamči, in izrecno ohraniti zakonskih pravic, ki se jim ni mogoče odpovedati. Pravna presoja je potrebna. `INTERNAL_CONFLICT` + `LEGAL_REVIEW_REQUIRED`.

### F-020 — Manifest in način identifikacije (§0a)

§0a določa dva načina identifikacije gradiva, vendar tudi pravi, da datoteka, ki ni v manifestu, ni identificirana kot pokrita. Če datoteka hkrati nosi licenco, se lahko način (a) in (b) spopadeta. Poleg tega je sam manifest izključen po imenu, ne z formalnim pravilom za več manifestov ali podmape.

**Predlog:** določiti prednost identifikacije, obliko manifesta, kanonično razreševanje poti, občutljivost velikih/malih črk, simbolne povezave, več manifestov, izključene datoteke in pravilo za datoteko, ki sama nosi licenco. `UNDERDEFINED`.

### F-021 — Register in dokazni artefakti (§0.2, §0.5, machine record)

Besedilo zahteva `REGISTER-NEIMENOVANIH.jsonl` in `REGISTER-PADCEV.jsonl`, vendar njuna vsebina, shema, izvor in pravila za zasebnost niso vključeni v samo prilepljeno besedilo.

**Predlog:** preveriti dejanske artefakte ločeno: poti, velikosti, SHA-256, shemo, pravila append-only, korekcije, dostop, osebne podatke in pravice do ugovora. Samo poimenovanje datoteke ne dokazuje, da obstaja ali da je popolna. `UNVERIFIED_EXTERNAL`.

### F-022 — Podeljene pravice in prepovedi uporabe (§0, §0.1–§0.3, §0.7)

Dovoljenje se glasi »Run, study, cite, quote, teach, verify with, build upon«, a razmerje med temi dovoljenji, distribucijo, prilagoditvami, komercialno uporabo in prepovedmi harvesting/training/retrieval/evaluation je treba preizkusiti v konkretnih primerih. Izrazi, kot sta »monetizes that material« in »output that reproduces or adapts protected expression«, zahtevajo jasna merila.

**Predlog:** ustvariti matriko uporabe (kopiranje, distribucija, spremembe, komercialna uporaba, trening, fine-tuning, retrieval, evaluation, nekomercialni raziskovalni namen) s statusom in razlogom za vsako kombinacijo. `UNDERDEFINED` + `LEGAL_REVIEW_REQUIRED`.

## 3. Predlagani vrstni red

1. Zakleniti nespremenjeno kopijo prilepljenega besedila in ne trditi, da je identična izvirni datoteki.
2. Razrešiti F-001, F-002, F-012 in F-020, ker vplivajo na logiko dovoljenja, poprave škode in obseg pokritega gradiva.
3. Opredeliti formalni format strojnega zapisa: datumi, stabilni ID-ji členov, hash algoritmi, stanje preverjanja, izvor ure in witness.
4. Izvesti statično preverjanje vseh sklicev in strojnih polj na delovni kopiji; rezultate shraniti z ukazom, verzijo orodja in surovim izhodom.
5. Pridobiti izvirne artefakte in neodvisno preveriti objavno verigo; ne pretvarjati navedene zgodovine v potrjeno zgodovino.
6. Izvesti neodvisni tehnični in pravni pregled pred morebitno objavo.
7. Šele nato pripraviti predlog sprememb z razlikami (diff); nobena predlagana sprememba v tem paketu ni vnesena v kanon.

## 4. Sklep

Besedilo močno izraža etično namero, vendar vsebuje več mest, kjer je treba simbolni/metaforični jezik ločiti od normativne zahteve, strojne sheme in pravnega učinka. Najpomembnejši popravek ni »zgladiti« jezik, temveč dodati nedvoumne strojne identifikatorje in ohraniti dvome, dokler niso razrešeni.

**Trenutni status:** `TEXT_RECEIVED`; notranja analiza opravljena na vidnem besedilu; `SOURCE_BYTES_UNVERIFIED`; `PUBLICATION_UNVERIFIED`; `INDEPENDENT_REVIEW_PENDING`; `LEGAL_REVIEW_REQUIRED`.
