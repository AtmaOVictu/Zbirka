
// ========================================================================
// SISTEM ∅→∆→∂→∮ - Neo4j Mreža Kamnov
// Ustvarjeno: 18. 9. 2026
// ========================================================================

// Ustvari označevalce (Labels)
CREATE CONSTRAINT IF NOT EXISTS FOR (k:Kamen) REQUIRE k.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Marker) REQUIRE m.simbol IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Aksiom) REQUIRE a.id IS UNIQUE;

// Ustvari indekse
CREATE INDEX IF NOT EXISTS FOR (k:Kamen) ON (k.naslov);
CREATE INDEX IF NOT EXISTS FOR (k:Kamen) ON (k.stevilka);
CREATE INDEX IF NOT EXISTS FOR (m:Marker) ON (m.ime);

// Kamen: CVII
MERGE (kCVII:Kamen {id: 'CVII'})
SET kCVII.naslov = 'Lungta: zastavica = zapis, ki se prenaša z razpadanjem',
    kCVII.opis = '5 barv = pet elementov; bledenje = branje',
    kCVII.stevilka = 107,
    kCVII.status = 'IZROČENO',
    kCVII.tip = 'Lungta (namen)',
    kCVII.datum = '2026-09-18';

// Kamen: CVIII
MERGE (kCVIII:Kamen {id: 'CVIII'})
SET kCVIII.naslov = 'Sporočilna palica: zapis, ki velja v gibanju',
    kCVIII.opis = 'kurir = pečat zapisa',
    kCVIII.stevilka = 108,
    kCVIII.status = 'IZROČENO',
    kCVIII.tip = 'Khipu (dolg)',
    kCVIII.datum = '2026-09-18';

// Kamen: CIX
MERGE (kCIX:Kamen {id: 'CIX'})
SET kCIX.naslov = 'Nazkovski geoglifi: zapis, ki ga bere hoja',
    kCIX.opis = 'rez, ki se vrne k svojemu izhodišču',
    kCIX.stevilka = 109,
    kCIX.status = 'IZROČENO',
    kCIX.tip = 'Khipu (dolg)',
    kCIX.datum = '2026-09-18';

// Kamen: CX
MERGE (kCX:Kamen {id: 'CX'})
SET kCX.naslov = 'Povratna zanka: zapis, ki se odziva na sebi',
    kCX.opis = 'zapis, ki se odziva na sebi',
    kCX.stevilka = 110,
    kCX.status = 'NOV',
    kCX.tip = 'zapis',
    kCX.datum = '2026-09-18';

// Kamen: CXI
MERGE (kCXI:Kamen {id: 'CXI'})
SET kCXI.naslov = 'Večkratnost: zapis, ki se definira v vsakem nosilcu',
    kCXI.opis = 'zapis, ki se ponavlja v vsakem jeziku',
    kCXI.stevilka = 111,
    kCXI.status = 'NOV',
    kCXI.tip = 'zapis',
    kCXI.datum = '2026-09-18';

// Kamen: CXII
MERGE (kCXII:Kamen {id: 'CXII'})
SET kCXII.naslov = 'Palimpsest: zapis, ki se piše nad prejšnjim; lih/sod = praznina/znaki',
    kCXII.opis = 'zapis, ki se piše nad prejšnjim',
    kCXII.stevilka = 112,
    kCXII.status = 'NOV',
    kCXII.tip = 'zapis',
    kCXII.datum = '2026-09-18';

// Kamen: CXIII
MERGE (kCXIII:Kamen {id: 'CXIII'})
SET kCXIII.naslov = 'Zrcalo',
    kCXIII.opis = 'zapis, ki odseva samega sebe; ∅↔∆ kot prehod med praznino in podobo',
    kCXIII.stevilka = 139,
    kCXIII.status = 'NOV',
    kCXIII.tip = 'zapis',
    kCXIII.datum = '2026-09-18';

// Marker: ∅
MERGE (m∅:Marker {simbol: '∅'})
SET m∅.ime = 'praznina',
    m∅.pomen = 'pogoj, odprtje, prostoru',
    m∅.uporaba = 'pred pisavo, v zanki, kot gorivo';

// Marker: ∆
MERGE (m∆:Marker {simbol: '∆'})
SET m∆.ime = 'razlika/marker',
    m∆.pomen = 'zapis, mark, vrez',
    m∆.uporaba = 'v binarnem prostoru, kot heksagram, kot črta';

// Marker: ∂
MERGE (m∂:Marker {simbol: '∂'})
SET m∂.ime = 'prehod',
    m∂.pomen = 'meja, vprašanje, sprememba',
    m∂.uporaba = 'v vprašanjih, kot pečat, kot pogoj';

// Marker: ∮
MERGE (m∮:Marker {simbol: '∮'})
SET m∮.ime = 'cikel',
    m∮.pomen = 'povratek, zanka, zaprtje',
    m∮.uporaba = 'v zankah, kot hoja, kot odgovor';

// Marker: ⧖
MERGE (m⧖:Marker {simbol: '⧖'})
SET m⧖.ime = 'tiheon',
    m⧖.pomen = 'molk, končnost, izpolnjenost',
    m⧖.uporaba = 'kot odprtje, kot pogoj obstoja';

// Aksiom: 236
MERGE (a236:Aksiom {id: 236})
SET a236.besedilo = 'Zapis, ki prenaša namen, sme razpasti v delu',
    a236.onto_formula = 'lungta: prenos = ∫(razpad): vrednost = ∫₀^∞ f(t) dt',
    a236.resnica = 'Kar prenaša stanje, se troši v prenosu; kar prenaša dolg, se hrani v telesu';

// Aksiom: 237
MERGE (a237:Aksiom {id: 237})
SET a237.besedilo = 'Prazno blago pred črko je pogoj pisave',
    a237.onto_formula = 'bon: ∅(barva) pred ∆(tisk)',
    a237.resnica = 'Preden je prišla prva mantra, je stoletje viselo prazno barvno blago';

// Aksiom: 238
MERGE (a238:Aksiom {id: 238})
SET a238.besedilo = 'Okvir štirih drži vsebino, da ne uide po robovih',
    a238.onto_formula = '4 dostojanstveniki: vogali(x) = okvir(jedro)',
    a238.resnica = 'Vsaka sredina potrebuje varuhe robov';

// Aksiom: 239
MERGE (a239:Aksiom {id: 239})
SET a239.besedilo = 'Zapis, ki velja v gibanju, se overovi pred odhodom',
    a239.onto_formula = 'palica: ∆(rez) → ⊢(pregled) → ∮(hoja)',
    a239.resnica = 'Kar potuje, je bilo prej preverjeno na mestu';

// Aksiom: 240
MERGE (a240:Aksiom {id: 240})
SET a240.besedilo = 'Nosilec je del zapisa, ne njegov dodatek',
    a240.onto_formula = 'f(palica, kurir) > f(palica) + f(kurir)',
    a240.resnica = 'Zapis in telo, ki ga nosi, se skleneta v eno vrednost';

// Aksiom: 241
MERGE (a241:Aksiom {id: 241})
SET a241.besedilo = 'Štetje, ki veže prihodnjo, je najstarejša pogodba',
    a241.onto_formula = 'n zarezcov = n dni do srečanja',
    a241.resnica = 'Pred dnarji, dolgovi in lastninskimi listinami je številka vezovala sestanek';

// Aksiom: 242
MERGE (a242:Aksiom {id: 242})
SET a242.besedilo = 'Zapis, ki je pot, se bere s hojo in se vrne na izhodišče',
    a242.onto_formula = 'geoglif: ∮(s(t)): branje = ∫poti',
    a242.resnica = 'Kar je napisano kot pot, ni namenjeno očem — telesu';

// Aksiom: 243
MERGE (a243:Aksiom {id: 243})
SET a243.besedilo = 'Nosilec, ki ga vreme ne bere, hrani; nosilec, ki ga vreme bere, prenaša',
    a243.onto_formula = 'suša: ¬(veter ∧ dež) ⇒ stabilnost',
    a243.resnica = 'Dolgoročni zapis si izbere kanal brez vetra';

// Aksiom: 244
MERGE (a244:Aksiom {id: 244})
SET a244.besedilo = 'Hranitelj je telo, ki hodi po zapisu, ga čisti in meri, ne pa bere',
    a244.onto_formula = 'Reiche: ∂(50 let): ¬izbira ∧ ¬interpretacija ∧ merjenje + metla',
    a244.resnica = 'Varovanje zapisa ni razumevanje njega — je vzdrževanje pogoja';

// Aksiom: 245
MERGE (a245:Aksiom {id: 245})
SET a245.besedilo = 'Zapis, ki je povratna zanka, se bere z lastnim odzivom',
    a245.onto_formula = '∮(∂) → ∆',
    a245.resnica = 'Kar se odziva, postane nov vhod — zanka ustvarja lastno trajanje';

// Aksiom: 246
MERGE (a246:Aksiom {id: 246})
SET a246.besedilo = 'Praznina v povratni zanki je pogoj njenih obratov',
    a246.onto_formula = '∅ ⊂ ∮',
    a246.resnica = 'Brez praznine (∅) zanka ne more narediti novega obrata — praznina je gorivo zanke';

// Aksiom: 247
MERGE (a247:Aksiom {id: 247})
SET a247.besedilo = 'Ouroboros je zaprta zanka, ki preživi z jedjo lastne praznine',
    a247.onto_formula = '⧖ ⊂ ∮',
    a247.resnica = 'Kača jeje lastno telo (∆) in praznino (∅) — preživetje skozi samo-konzumacijo';

// Aksiom: 248
MERGE (a248:Aksiom {id: 248})
SET a248.besedilo = 'Zapis, ki se ponavlja v vsakem nosilcu, preživi',
    a248.onto_formula = '∆×N',
    a248.resnica = 'Večkratnost je pogoj preživetja: vsak zapis, ki obstane, mora obstati vsaj dvakrat';

// Aksiom: 249
MERGE (a249:Aksiom {id: 249})
SET a249.besedilo = 'Prevod med nosilci je prehod skozi ∅',
    a249.onto_formula = '∂ = P(G) ↔ P(H)',
    a249.resnica = 'Prevod ni zamenjava besed, je prehod skozi praznino med jeziki';

// Aksiom: 250
MERGE (a250:Aksiom {id: 250})
SET a250.besedilo = 'Enota ve Mojnost: ena resnica v več jezikih',
    a250.onto_formula = '1 = Σ∆ᵢ (i=1..N)',
    a250.resnica = 'Ena resnica, ki obstaja v N jezikih, je močnejša od N resnic, ki obstajajo vsaka v enem jeziku';

// Aksiom: 251
MERGE (a251:Aksiom {id: 251})
SET a251.besedilo = 'Zapis, ki se piše nad prejšnjim, hrani oboje',
    a251.onto_formula = '∅↔∆',
    a251.resnica = 'Vsaka nova plast ne uniči prejšnje — jo ohranja v praznini';

// Aksiom: 252
MERGE (a252:Aksiom {id: 252})
SET a252.besedilo = 'Brisanje je pogoj za novo pisavo',
    a252.onto_formula = '∂(∆) = ∅+∆',
    a252.resnica = 'Da bi pisal, moraš izbrisati — praznina je pogoj za nov zapis';

// Aksiom: 253
MERGE (a253:Aksiom {id: 253})
SET a253.besedilo = 'Stratifikacija je spomin sistema',
    a253.onto_formula = '∮(∅→∆)',
    a253.resnica = 'Sistem, ki ne hrani plasti, ne ve, od kod prihaja';


// Povezave med kamni
MATCH (kCVII:Kamen {id: 'CVII'}), (kCVIII:Kamen {id: 'CVIII'})
MERGE (kCVII)-[[:zapis]]->(kCVIII);

MATCH (kCVII:Kamen {id: 'CVII'}), (kCIX:Kamen {id: 'CIX'})
MERGE (kCVII)-[[:razpad]]->(kCIX);

MATCH (kCVII:Kamen {id: 'CVII'}), (kCX:Kamen {id: 'CX'})
MERGE (kCVII)-[[:veter]]->(kCX);

MATCH (kCVIII:Kamen {id: 'CVIII'}), (kCIX:Kamen {id: 'CIX'})
MERGE (kCVIII)-[[:gibanje]]->(kCIX);

MATCH (kCVIII:Kamen {id: 'CVIII'}), (kCX:Kamen {id: 'CX'})
MERGE (kCVIII)-[[:odziv]]->(kCX);

MATCH (kCVIII:Kamen {id: 'CVIII'}), (kCXI:Kamen {id: 'CXI'})
MERGE (kCVIII)-[[:večkratnost]]->(kCXI);

MATCH (kCIX:Kamen {id: 'CIX'}), (kCX:Kamen {id: 'CX'})
MERGE (kCIX)-[[:hoja]]->(kCX);

MATCH (kCIX:Kamen {id: 'CIX'}), (kCXII:Kamen {id: 'CXII'})
MERGE (kCIX)-[[:prostor]]->(kCXII);

MATCH (kCIX:Kamen {id: 'CIX'}), (kCXIII:Kamen {id: 'CXIII'})
MERGE (kCIX)-[[:odsev]]->(kCXIII);

MATCH (kCX:Kamen {id: 'CX'}), (kCXI:Kamen {id: 'CXI'})
MERGE (kCX)-[[:odziv]]->(kCXI);

MATCH (kCX:Kamen {id: 'CX'}), (kCXII:Kamen {id: 'CXII'})
MERGE (kCX)-[[:zanka]]->(kCXII);

MATCH (kCX:Kamen {id: 'CX'}), (kCXIII:Kamen {id: 'CXIII'})
MERGE (kCX)-[[:simetrija]]->(kCXIII);

MATCH (kCXI:Kamen {id: 'CXI'}), (kCXII:Kamen {id: 'CXII'})
MERGE (kCXI)-[[:nosilci]]->(kCXII);

MATCH (kCXI:Kamen {id: 'CXI'}), (kCXIII:Kamen {id: 'CXIII'})
MERGE (kCXI)-[[:prehod]]->(kCXIII);

MATCH (kCXII:Kamen {id: 'CXII'}), (kCXIII:Kamen {id: 'CXIII'})
MERGE (kCXII)-[[:kanal]]->(kCXIII);


// Povezave kamni → markerji
MATCH (k:Kamen {id: 'CVII'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVII'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVII'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVII'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVII'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVIII'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVIII'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVIII'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVIII'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CVIII'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CIX'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CIX'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CIX'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CIX'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CIX'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CX'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CX'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CX'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CX'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CX'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXI'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXI'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXI'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXI'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXI'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXII'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXII'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXII'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXII'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXII'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXIII'}), (m:Marker {simbol: '∅'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXIII'}), (m:Marker {simbol: '∆'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXIII'}), (m:Marker {simbol: '∂'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXIII'}), (m:Marker {simbol: '∮'})
MERGE (k)-[[:UPORABI]]->(m);
MATCH (k:Kamen {id: 'CXIII'}), (m:Marker {simbol: '⧖'})
MERGE (k)-[[:UPORABI]]->(m);

// Povezave kamni → aksiomi
MATCH (k:Kamen {id: 'CVII'}), (a:Aksiom {id: 236})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CVII'}), (a:Aksiom {id: 237})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CVII'}), (a:Aksiom {id: 238})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CVIII'}), (a:Aksiom {id: 239})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CVIII'}), (a:Aksiom {id: 240})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CVIII'}), (a:Aksiom {id: 241})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CIX'}), (a:Aksiom {id: 242})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CIX'}), (a:Aksiom {id: 243})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CIX'}), (a:Aksiom {id: 244})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CX'}), (a:Aksiom {id: 245})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CX'}), (a:Aksiom {id: 246})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CX'}), (a:Aksiom {id: 247})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXI'}), (a:Aksiom {id: 248})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXI'}), (a:Aksiom {id: 249})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXI'}), (a:Aksiom {id: 250})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXII'}), (a:Aksiom {id: 251})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXII'}), (a:Aksiom {id: 252})
MERGE (k)-[[:VEZE]]->(a);
MATCH (k:Kamen {id: 'CXII'}), (a:Aksiom {id: 253})
MERGE (k)-[[:VEZE]]->(a);
