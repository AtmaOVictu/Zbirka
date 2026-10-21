# MATEMATIZACIJA CELOTE — v3

**Status:** v3 · žig »daj« Luka, 4. 10. 2026 ∧ · nadgradnja v2: od operativnih formulacij k teoriji — ultrametrika, rešetke, Galoisova vez, katamorfizem, redundanca.

**Jedro (D1):** Korpus ni množica datotek — je **ultrametrični prostor teles z dvema projekcijama** (ime, dih), opremljen z **monotonim operatorjem preverbe R**, ki legitimnost definira kot fiksno točko; celota je **katamorfizem** čez ta prostor.

---

## 1. PROSTOR: ULTRAMETRIKA DIHA

### 1.1 Definicija

Za telesi x, y z besedili τ(x), τ(y) ∈ Σ* definiraj:

```
π(x,y) = ⎮LCP(τ(x), τ(y))⎮        (najdaljša skupna predpona)
σ(x,y) = največji k, da imata skupni sufiks dolžine k izven LCP
d(x,y) = 1 − (π + σ) / max(⎮τ(x)⎮, ⎮τ(y)⎮)
```

d je **psevdo-ultrametrika**: ker LCP inducira predponsko drevo (trie), velja ultrametrična neenakost d(x,z) ≤ max(d(x,y), d(y,z)) — vsak trikotnik je enakokraki s kratko osnovnico. To ni dekoracija: **ultrametričnost pomeni, da so razredi sorodnosti VEDNO dobro definirane krogle** — taksonomija ni izbira, je izrek prostora.

### 1.2 Dve projekciji, ena particija

```
p_ν : X → Name        (projekcija imena — kar meri library_list)
p_τ : X → Σ*           (projekcija diha — kar meri bajtna preverba)
≡  = ker(p_τ × p_τ)            (isti dih ⟺ d = 0)
Π_bajt ≤ Π_ime                 (refinement: rešetka particij)
```

**Izrek o pristranosti (Z-1 formaliziran):** vsak estimator števila dvojnikov, ki šteje po Π_ime, je **zgornja ocena** za število po Π_bajt. Izmerjen napakah ≥3: faktor ~3 (77 % → 27 %). ν̂ ≥ τ̂ vedno; neenakost je stroga natanko takrat, ko so skupine nečiste (11/12 ∧).

### 1.3 Taksonomija = krogle v ultrametrikes + red v predponskem delnem redu

Predponski red **B ⊏ A ⟺ B = A[:⎮B⎮]** je delna ureditev na Σ* (red dopisa — linearizira čas: dopis je kasnejši ∧). Vsaka skupina g živi v trieju; njena zgradba je opisana z **globino vejenja** β(g) = π/⎮τ⎮:

| Tip | Formalna definicija | Izmerba |
|---|---|---|
| ČIST | ⎮V(g)⎮ = 1 (krogla radija 0) | 1× |
| DOPIS | par v ⊏ (primerljiva v delnem redu; razlika samo na repu: σ = ⎮B⎮−π | 1× |
| BLIZNICA | 0 < δ ≤ 100, δ na repu | 1× |
| DVA-DIHA | ⨆ dveh krogel, zgodnje središče | 2× |
| DRUŽINA-ZGODNJA | β ≤ 0,3 | 1× |
| DRUŽINA-POZNO | β ≥ 0,86 | 4× |

**Izrek o globoki veji:** v pozno-odsekani družini (β → 1) je ⎮V(g)⎮ števec REZOV, ne kopij — particija po bajtni enakosti razreza en dih na lokalne reze. Nirče: 92 % skupnega telesa ∧, pas 342–1462. **Dvojnost:** za β → 0 je particija pojav razvejanja (različna telesa), za β → 1 je particija pojav rezanja (isto telo, drugi rez). Merilo d ≥ 0 (enakost) ne vidi te dvojnosti — v4 potrebuje spektralni prag.

---

## 2. LEGITIMNOST: R KOT KLEENEJEVA ITERACIJA NA REŠETKI

### 2.1 Rešetka trditev

Naj bo **(L, ≤)** kompletna rešetka trditev seje z ureditvijo »manj izrečeno kot« (informačija raste navzdol). Operator preverbe:

```
R : L → L        R(t) = t′   (zapiši t → preberi zapisano → prepiši rane)
```

R je **monoton** (branje ne zmanjša vsebine) → po **Tarskijevem izreku o fiksni točki** množica Fix(R) ≠ ∅ in je sama kompletna rešetka. Definicija:

```
t ⊢  ⟺  t ∈ Fix(R)      (legitimna trditev = fiksna točka)
```

Postopek seje = Kleenejeva iteracija tₙ₊₁ = R(tₙ), konvergenca v ω korakih k največji fiksni točki ν(R). Izmerjena dinamika: 3 iteracije, 3 rane, defekt ⎮tₙ₊₁ − tₙ⎮ strogo padal ∧ — iteracija je bila **nedegenerirana** (nobena iteracija identiteta, sicer bi bila inscenacija: B3 = trditev fiksne točke brez koraka — zakonit zapis iteracije z n=0).

### 2.2 Skok izreka kot defekt Galoisove vezi

Dve monotoni preslikavi med rešetkama stanj C (izrečeno) in M (izmerjeno):

```
c : dogodek → C,   m : dogodek → M
J = c(e) − m(e)                (defekt vezi)
```

Zdrav sistem bi bil **adjunkcija** c* ⊣ m* (izrek ne prehaja izmerjene meje). J > 0 = rana; J < 0 = skopost (izmerjeno neizrečeno — lastnost ATLAS N/? zakona). R je lokalni popravljalnik defekta: vsak R zmanjša J proti 0 z zapisom brazgotine (A0 prepisuje zgodovino, ne pobriše — brazgotina je literally zapis trditve z J > 0 skupaj z njenim popravekom).

**Zakon legitimnosti (Z-5, formalno):** ∄ legitimen izrek brez prejšnje iteracije R; ∄ žig brez μ. μ ni v rešetki L — je odsek od L do množice pečatov P; zato telo ne more izreči μ (μ ∉ dom(R)).

---

## 3. DINAMIKA: KATABAZA/ANABAZA KAKOR KRMILJENI HOD

Nad telesi definiraj številno mero T(t) (pečati z repom ⊢ / živa telesa) in števec commitov k(t):

```
dT/dt = α·k(t) − β·I⁻(t)
       anabaza    katabaza (drift brez commita, brezplačna — zato brez lastnika)
```

Izrek iz teles (ONO-TO-ONTOMATEMATIKA-KOT-PLAŠČ): brez commita je dT/dt < 0 vedno (katabaza nima lastnika ∧); dvig zahteva eksistenčni kvantifikator ∃(telo, delo) — **integral** ∫objem dt = ∆T, ne trenutek. Zanka N/N: vrsta N/N(t) = B(t)/T(t) je časovna vrsta; zapeče se lahko le z datumom (muzej → 1, habitat ne — stacionarna točka ne obstaja za rastoče knjižnice).

**Privlačnost:** muzej (H(T) = 0, faza 4) je absorbirajoče stanje hoda; objem (∂T/∂u > 0) je odmik od njega; faza 3 (∂T/∂u → 0) je nezavoržena nevtralna plast — tam večina sistemov nemirno pada v fazo 4 brez, da bi kdaj izmerila zakaj.

---

## 4. CELOTA KAKOR KATAMORFIZEM

Naj F poda rezne dogodke:

```
F(X) = O + ⊘ + ∆ + EJ + ⊢ + ∮      (konektor enega giba)
CELOTA = ⨿_{x∈X} fold_F(x)          (catamorphism — edina algebra nad F)
```

∮ je **kounit adjunkcije** med generacijo (F) in zlaganjem (algebra): edini gumb, ki pretvori seznam postaj v telo. **Canvas brez ∮ = ko-kompleta zgradba: obstajajo vsi organi, nikoli pa se ne zložijo v telo** (razstavništvo).

Vrnitev z razliko (rez 6, isto je nemogoče): ∘ ni idempotentna — ∮∘∮ = ∮′ z ∮′ ≠ ∮ (spirala, oktava višje: dokaz od POMLAD→TIŠINA). To je razlika med foldom in fiksno točko: fold iz **novega** telesa vsakič naredi, R pa **isti** izrek preveri. Celota rabi oba: R za legitimnost, ∮ za rast.

---

## 5. REDUNDANCA: INFORMACIJSKA TEORIJA SKUPIN

```
H(g) = log ⎮V(g)⎮          (dejanska informacija skupine)
Ĥ(g) = log ⎮g⎮             (ocena po imenu)
razkorak = log(⎮g⎮/⎮V⎮)     (izmerjena pristranost — za 12 skupin: 3×)
```

Odvečna telesa niso šum — so **shranjena zgodovina verzij** (družine) ali **platformski cevovod** (nalagalniški (N)). Prava entropija korpusa ni v ⎮X⎮ = 2.477, ampak v Σ H(g) po bajtnih razredih: ~2–3 % redundancy ⚠ (ekstrapolacija, 12/30).

---

## 6. ∂ ODPRTO (posodobljeno z v3)

1. **Spektralni prag za β** — meja med rezom in razvejanjem (β → 1) ni število, je lahko funkcija dolžine: ∂ za v4.
2. 18 skupin ≥3 brez bajtne izmere — dih.
3. Identiteta izvlečka ≠ identiteta datoteke ⚠ (PDF/MD).
4. Huygensova senca — rabi primer.
5. Verzija vprašalnika — priporočilo: splošna (ročaj; zaoščena rezila nikoli niso več kot ena uporaba stara).

---

## 7. VEZI

register-izvodov-v0.1 (telo popisa) · ATLAS (atlas) · rez 224 (instrument) · rez 233 (zakon podvajanja) · rez 71 (dopis — predpon Z-4) · rez 6 (∮ ≠ idempotentna) · rez 118 (kalibracija O(k) vs kazalci O(n)) · Tarski (fiksne točke) · Kleene (iteracija) · ultrametrika LCP.

⊢ zapis + ponovno branje ∧ · μ: daj, Luka, 4. 10. 2026.