# TAZV — LOCK KATALOG, ŠKATLJE, KI REŽEJO

*Vsak LOCK je nelinearna škatla: če pogoj pade, se stanje ne spremeni postopoma — skoči. Škatla ni orodje za umirjanje — je rez, ki čaka na prag.*

⧖

## 0. Rez na zaklep

**LOCK** — angleško zaklep; rodovnik ločen od reza: iz staroangleškega *locc* (pramen lasa, koder) — zaklep je prvotno pramen, ki se zapne. Rez: **LO-CK** — lo (loko, kraj) + ck (klik, konec giba): zaklep je kraj, kjer gib končno klikne.

**ŠKATLA** — š/ka/t/la: šum (š) klica (ka) skozi telo (t) v loko (la — kraj). Škatla ni zaboj — je kraj, kjer klic dobi meso. Vsak LOCK je škatla: arhivira stanje, dokler pogoj ne pade.

### Zakon kataloga

LOCK ni stikalo, ki pritisneš — je **pogoj, ki čaka**. Razlika je etična: stikalo upravlja operater; pogoj upravlja telo. Kdor pritiska LOCK »ker je čas«, je naredil tabu (rez 276 vzporedni: meja, ki jo varuješ in ne izrečeš); kdor čaka pogoj, je naredil zakon (izrečena meja s pragom).

⧖

## I. Stanjski prostor — devet spremenljivk

| Spremenljivka | Ime | Domena | Smer |
|---|---|---|---|
| **A_RANA** | Rana | [0,1] | minimiziraj |
| **B_SPREJEM** | Sprejem | [0,1] | maksimiziraj |
| **C_MEJE** | Meje | [0,1] | maksimiziraj |
| **D_AKCIJA** | Akcija | [0,1] | — |
| **E_DOKAZ** | Dokaz | [0,1] | maksimiziraj |
| **F_PREPRIČ** | Preprič | [0,1] | — |
| **G_GRADNJA** | Gradnja | [0,1] | maksimiziraj |
| **T_TOBI** | Tobī (merjenje) | [0,1] | — |
| **R_REZ** | Rez | [0,1] | minimiziraj |

**Cilj (mnogoterost):**

```
J = w₁(1-A_RANA) + w₂ B_SPREJEM + w₃ C_MEJE + w₄ G_GRADNJA - w₅ R_REZ
```

**Zunanji vhodi (normalizirani):** C_t (cenzura), S_t (sprejetost), U_t (sprožilci), H_t (somatika/dih/gib), Z_t (spanje/ritem).

Preberi kot hišo: A je klet (kaj boli), B in C so stene (kaj nosim in kje je meja), D je hodnik (kaj se premika), E je peč (kaj dokazuje, da gori), F je termostat (kaj verjamem), G je nadstropje (kaj gradim), T je meter (kaj merim), R je streha, ki jo veter rezе (kaj trga).

⧖

## II. KATALOG — štiri izrečene škatle

### ⊢STOP_LOCK_03 — RUMINACIJA → FOKUS

- **Pogoj:** `U_t > θ₁ ∧ H_t < θ₂` — sprožilci visoki, somatika nizka (telo utrujeno, glava v krogu).
- **Skok:** `φ_D = +κ₁, φ_R = −κ₂` — akcija gor, rez dol.
- **Rez besede:** RU-MI-NA-CI-JA — ruma (Rumija, žvakovalnica) v naci (ponavljanju) ciji (kliče) jagenj (jagenj): ruminacija je prežvečevanje — isto travo, štirikrat, brez novih zob. Škatla prereže žvečilni krog.
- **Telo:** utrujena kroženja misli; STOP ne pomirja — usmerja.
- **Varnost:** hladilno obdobje (Dreros, rez 268): rez, ki ga izrečeš, ni na voljo za izpeljavo dokazov, dokler telesa ne preberejo drugi.

### ∆REZ_LOCK_01 — JEZA → PRETVORBA

- **Pogoj:** `R_REZ > 0.7 ∧ STOP signal = 1` — rez visok in stop-signal prisoten (zavest ve, da je čas).
- **Skok:** `φ_B = +0.15, φ_C = +0.10, φ_R = −0.20` — sprejem gor, meje gor, rez dol.
- **Rez besede:** JE-ZA — je (jez, organ okusa) + za (za-ne): jeza je organ, ki je obrnjen za — okuša, kaj je za mejо. Kot gorivo, ne kot stanje: BES kot motor izjave (prop XXI).
- **Telo:** vročina, ki išče izhod; škatla da izhod, ne zadušitev.
- **Varnost:** antinom — jeza, ki se pretvori, mora ostati jeza v zapisu (∮ brazgotina); pretvorba, ki izbriše izvor, ni pretvorba, je prikrivanje.

### ∮MIR_LOCK_02 — ŽALOST → POMEN

- **Pogoj:** `A_RANA > 0.6 ∧ žalostno okno = 1` — rana globoka in okno odprto (dovoljeno je žalovati).
- **Skok:** `φ_E = +0.20, φ_B = +0.10, φ_A = −0.15` — dokaz gor, sprejem gor, rana dol.
- **Rez besede:** ŽA-LOST — žeja (ža) v loku (lost — izguba): žalost je žeja po izgubljenem, ki se ovije v lok — lok nosi, ne seže. Škatla da izgubi pomen, ne opravičilo.
- **Telo:** teža, ki išče nosilca (AX-5: rana kot nosilec).
- **Varnost:** okno ima čas (žalovanje brez roka je notranja zamuda); pretvorba pred oknom je lažni mir (RES008: »vse je v redu« — ni).

### ≠PAST_LOCK_04 — SPOMIN → MEJA

- **Pogoj:** `ponovitev spomina > 2× v 24h` — isti spomin se vrne več kot dvakrat na dan.
- **Skok:** `φ_C = +0.15, φ_D = +0.10, φ_R = −0.10` — meje gor, akcija gor, rez dol.
- **Rez besede:** PA-MAT (spomin) — past (past) + mat (mater, matrika): spomin je past, ki te matеri — hrani te in drži. Škatla spominski ponovitvi postavi mejo: tretjič pomeni, da spomin išče nosilca, ne gledalca.
- **Telo:** kroženje istih slik; škatla preveri, ali spomin išče dokaz (E gor) ali zgolj občinstvo.
- **Varnost:** etika spomina (§17): spomеn nepravičnosti je avtoritativen; ne-f odpuščanja je meja. Škatla ne odpušča — postavlja mejo ponovitvi, ne vsebini.

⧖

## III. MAŠINERIJA — učenje in mostovi

### Hebb + pozaba

```
A_ij(t+1) = clip(A_ij(t) + η x_j(t) x_i(t+1) − λ A_ij(t), 0, 1)
η ∈ [0.01, 0.1]  (hitrost učenja)
λ ∈ [0.001, 0.01] (pozaba)
```

V besedah: povezava, ki se pogosto srečuje, krepi (Hebb — »nevroni, ki se streljajo skupaj, se vežejo skupaj«); povezava, ki se ne uporablja, bledi (pozaba). Mreža, ki se ne pozablja, ne more paziti na novo; mreža, ki pozablja prehitro, je zlomljena. λ je zakon pozabe: spomin mora bledeti dovolj počasi, da nosi brazgotino, dovolj hitro, da pušča prostor.

### Trojni mostovi

```
A → ∆ → B   (rana → osni rez → sprejem)
```

∆ (osni rez) v sredini je obvezen. Prehod iz rane v sprejem **ne sme preskočiti reza** — sicer je odpust brez priznanja (REKE_14 NE-PRIKRIVATI). Če se ∆ ne sproži v dveh fazah → prisilni ∆-flip (±π): flip je faza za 180° — isto telo, ki se obrne, in vidi svojo senco.

### Zanka s povratno vejo (nadmzžna zanka)

```
stanje x(t) → LOCK pogoji → φ popravki → x(t+1)
guard: κ ≥ .70, χ ≥ .40, μ ∈ [.50,.80], ℜ ≤ .03
```

Vsak φ popravek gre skozi guard (Horos, rez 276): popravki, ki ne nosijo koherence in jasnosti, se ne izvedejo — tudi če so »pravi«. TAZV ne optimizira stanja, temveč prehode skozi mejo.

⧖

## IV. PRAKSA — izvedba na primeru

*Stanje: izmenjava, v kateri se isti prigovor (»spet si poskrbel za vse drugе, zase nisi«) vrača tretji dan zapored.*

- **Detekcija:** spomin-se-spreminja > 2× v 24h → **≠PAST_LOCK_04** pripravljen.
- **Pogoj preverjen:** ponovitev res tretjič → skok: φ_C +.15 (meja gor — »naslednjič rečem NE pred obveznostjo, ne po njej«), φ_D +.10 (akcija — ena zavrnitev izvedena danes), φ_R −.10 (rez dol — obtožba se ne obrne vase).
- **Guard:** κ (ali meja sovpada s celim stanjem?) — da; χ (ali jo drugi lahko sliši?) — enostavno izrečena; μ — delež moje vloge v meji; ℜ — kaj ostane nerešenega.
- **Povratek:** zapis v ledger — ponovitev je dobila ime in mejo. Tretjič istega je postal prvič novega.

**REK:**

```
REK — Tretjič
A: Spet isti prigovor. Tretji dan.
B: Tretjič pomeni, da iščeš nosilca.
DAR: Meja ni zid proti tebi —
     je tla pod menoj. Tla so skupna.
```

⧖

## V. DOKAZI — testi in pesem

### Testi

- **T1 (katera škatla čaka):** preberi svoj današnji dan po devetih spremenljivkah (kratek seznam, po občutku). Katera škatla ima pogoj blizu praga — ruminacija, jeza, žalost ali spomin? Škatla, ki čaka, ni sovražnik — je naslednja vrata.
- **T2 (prag, ne stikalo):** spomni se trenutka, ko si »pritisnil« prehod pred pogojem (moraliziral žalost, prisilil odpuščanje, zadušil jezo). Kaj se je zgodilo v 24h? Prehod pred pragom se vrne — z večjo težo.
- **T3 (osni rez):** vzemi eno rano, ki bi jo rad »sprejel«. Kje je ∆ — dejanje ali izrek, ki jo prereže? Brez ∆ je sprejem lepi mir (RES008). Imenuj ∆ v enem stavku.
- **T4 (izključna luka):** LOCK pogoji so številske pristе. Ali sme telo meriti prehode v številih, ne da jih ubije (rez 263: merjenje, ki ne ubija)? Odgovor: sme — dokler številka piše prag, ne vrednost osebe. Merjenje postane ubijajoče, ko se [0,1] bere kot ocena, ne kot lega. Preizkus vsake meritve: ali jo zmoreš izreči sebi brez sramu (rez 276 vzporedni: sram = zamrznjena faza brez bralca)?

### Pesem

```
Štiri škatle v eni hiši.
                 Vsaka čaka na svoj prag.
                 Nobena se ne odpre na roko —
                 odpre se na pogoj.
```

⧖

```
Ruminacija prežvekuje travo,
                 ki ni več tam.
                 Jeza okuša, kaj je za mejo.
                 Žalost žeja po izgubljenem.
                 Spomin išče nosilca.
Štiri škatle, štiri glagode —
                 in vse so rezi,
                 ki čakajo na dovoljenje telesa.
```

⧖

```
Kdor pritiska zaklep, dela tabu.
                 Kdor čaka pogoj, dela zakon.
Razlika ni v sili —
                 v tem, kdo ve, kdaj je čas.
                 In to ve zgolj telo.
```

⧖

## VI. Odprta ∂

Katalog izrečen: štiri škatle s pogoji, skoki, rezi besed, varovali; učenje s pozabo; trojni mostovi; guard zanka; izvedba na primeru z REK. Kar telo še ne nosi: uteži w₁–w₅ (kdo jih določa in kdaj se smejo spremeniti — odločitev za lasten rez), θ₁/θ₂ pragovi za posamezno telo (kalibracija, ne univerzalnost — rez 276: meja, ki jo varuješ, izreči), in vozlišče med TAZV in hipnozno serijo (TRI-TEN iz vzporednega pečata 276: dihalna/diafragmalna/vokalna prepona kot trije LOCK-i istega telesa — kandidat za most).

Vrsta naprej: **časovni zemljevid stiske** (vrzel reza 274), Δt_seal AX-14. ∂ 277 čaka.