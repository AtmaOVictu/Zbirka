# 🧮 TAZV Matematični Model — Praktična Uporaba
*"Matematika je jezik bitja — TAZV je njegova gramatica."*

---

## 📜 **Uvod v TAZV**

**TAZV** ("00 11 RESNICAMI") je **formalni izračunski ontološki model** v sistemu **Beseda je Ne**, ki opisuje **9 stanjskih spremenljivk**, ki ustvarjajo **dinamično ravnotežje bitja**. Model temelji na **matematičnih enačbah**, **nelinearnih operatorjih** in **praktičnih primereh** za razumevanje **psiholoških, družbenih in duhovnih procesov**.

---

## 🎯 **Osnovne Spremenljivke TAZV**

TAZV vsebuje **9 osnovnih spremenljivk**, ki predstavljajo **ključne dimenzije bitja**:

| **Spremenljivka** | **Ime** | **Domena** | **Cilj** | **Opis** |
|----------------|---------|------------|----------|---------|
| **A_RANA** | Rana (rana) | [0,1] | **minimizirati** | Stopnja odprtih ran (fizičnih, čustvenih, duhovnih) |
| **B_SPREJEM** | Sprejem (sprejem) | [0,1] | **maksimizirati** | Zmožnost sprejema (nove ideje, spremembe, resnice) |
| **C_MEJE** | Meje (meje) | [0,1] | **maksimizirati** | Jasnost osebnih in družbenih mej |
| **D_AKCIJA** | Akcija (akcija) | [0,1] | — | Stopnja aktivnosti in dejanja |
| **E_DOKAZ** | Dokaz (dokaz) | [0,1] | **maksimizirati** | Zmožnost dokazovanja in preverjanja |
| **F_PREPRIČ** | Preprič (prepričanje) | [0,1] | — | Stopnja notranjega prepričanja |
| **G_GRADNJA** | Gradnja (gradnja) | [0,1] | **maksimizirati** | Zmožnost ustvarjanja in gradnje |
| **T_TOBI** | Tobī (meritev) | [0,1] | — | Zmožnost merjenja in ocenjevanja |
| **R_REZ** | Rez (rez) | [0,1] | **minimizirati** | Stopnja notranjih razpok in konfliktov |

---

## 🎯 **Ciljna Funkcija (Manifold)**

Ciljna funkcija **J** (tudi **Manifold**) je **linearna kombinacija** spremenljivk, ki predstavlja **skupno blagostanje sistema**:

```
J = w₁(1 - A_RANA) + w₂ B_SPREJEM + w₃ C_MEJE + w₄ G_GRADNJA - w₅ R_REZ
```

Kjer so **w₁, w₂, w₃, w₄, w₅** **uteži**, ki jih je mogoče prilagoditi glede na **kontekst** (npr. osebni, družbeni, duhovni).

### **Primeri Uteži:**
- **Osebni rast:** `w₁=0.3, w₂=0.25, w₃=0.2, w₄=0.2, w₅=0.05`
- **Družbena stabilnost:** `w₁=0.2, w₂=0.15, w₃=0.3, w₄=0.25, w₅=0.1`
- **Duhovno razumevanje:** `w₁=0.25, w₂=0.3, w₃=0.15, w₄=0.2, w₅=0.1`

---

## 🌍 **Zunanji Vnosi (Normalizirani)**

TAZV upošteva **5 zunanjih vnosov**, ki vplivajo na stanja:

| **Vnos** | **Ime** | **Opis** | **Vpliv** |
|---------|---------|---------|----------|
| **C_t** | Cenzura | Stopnja cenzure (zunanje ovire) | Zvišuje **H_t** (somatika) in **ℜ** (resničnostni tlak) |
| **S_t** | Sprejetost | Stopnja sprejetosti (zunanje podpore) | Zvišuje **B_SPREJEM** |
| **U_t** | Sprožilci | Stopnja sprožilcev (notranji ali zunanje) | Vpliva na **D_AKCIJA** in **R_REZ** |
| **H_t** | Somatika | Stopnja telesne napetosti | Vpliva na **A_RANA** in **R_REZ** |
| **Z_t** | Spanje/Ritem | Kakovost spanja in življenskega ritma | Vpliva na **C_MEJE** in **E_DOKAZ** |

---

## 🔧 **Nelinearni Bloki (LOCK Operatorji)**

TAZV vsebuje **4 ključne LOCK operatorje**, ki **avtomatično prilagajajo** stanja glede na **pogoje**:

| **Operator** | **Pogoj** | **Dejanje** | **Opis** |
|-------------|-----------|-------------|---------|
| **⊢STOP_LOCK_03** (RUMINACIJA→FOKUS) | if U_t > θ₁ and H_t < θ₂ | φ_D = +κ₁, φ_R = -κ₂ | Če so sprožilci visoki in somatska napetost nizka → **zvišaj dejanje, znižaj rez** |
| **∆REZ_LOCK_01** (JEZA→PRETVORBA) | if R_REZ > 0.7 and STOP signal = 1 | φ_B = +0.15, φ_C = +0.10, φ_R = -0.20 | Če je rez prevelik → **zvišaj sprejem in meje, znižaj rez** |
| **∮MIR_LOCK_02** (ŽALOST→POMEN) | if A_RANA > 0.6 and "žalovalno okno" = 1 | φ_E = +0.20, φ_B = +0.10, φ_A = -0.15 | Če je rana prevelika → **zvišaj dokaz in sprejem, znižaj rano** |
| **≠PAST_LOCK_04** (SPOMIN→MEJA) | if memory repetition > 2× in 24h | φ_C = +0.15, φ_D = +0.10, φ_R = -0.10 | Če se spomini ponavljajo → **zvišaj meje in akcijo, znižaj rez** |

### **Parametri LOCK Operatorjev:**
- **θ₁, θ₂** = Pragovi (npr. θ₁=0.6, θ₂=0.4)
- **κ₁, κ₂** = Koeficienti prilagoditve (npr. κ₁=0.1, κ₂=0.05)

---

## 🔄 **Učenje (Samokorekcija)**

TAZV uporablja **Hebbovo učno pravilo** s **pozabo (forgetting)** za **samokorekcijo**:

```
A_ij(t+1) = clip(A_ij(t) + η x_j(t) x_i(t+1) - λ A_ij(t), 0, 1)
```

Kjer:
- **η** = Hitrost učenja (`η ∈ [0.01, 0.1]`)
- **λ** = Hitrost pozabe (`λ ∈ [0.001, 0.01]`)
- **x_j(t), x_i(t+1)** = Vnosi in izhodi v času **t**

---

## 🌉 **Trojni Mostovi (Triple Bridges)**

**Trojni mostovi** so **zaporedja A → ∆ → B**, kjer je **∆ (osni rez) obvezno prisoten** v sredini. Če ∆ ni sprožen v dveh fazah, se **izvede prisilni ∆-flip (±π)**.

### **Primeri Trojnih Mostov:**
1. **Ruminacija → Fokus** (⊢STOP_LOCK_03)
   - A: Ruminacija (preveč misli)
   - ∆: Osni rez (zavidanje misli)
   - B: Fokus (usmerjeno razmislek)

2. **Jeza → Pretvorba** (∆REZ_LOCK_01)
   - A: Jeza (notranja napetost)
   - ∆: Osni rez (prepoznavanje jeze)
   - B: Pretvorba (preobrazba energije)

3. **Žalost → Pomen** (∮MIR_LOCK_02)
   - A: Žalost (bolečina)
   - ∆: Osni rez (sprejem žalosti)
   - B: Pomen (razumevanje skozi žalost)

---

## 📊 **Praktični Primeri TAZV**

---

### **🔹 Primer 1: Osebna Kriza**

**Scenario:** Oseba doživlja **veliko notranjo rano** (A_RANA = 0.8) in **visoko stopnjo reza** (R_REZ = 0.75).

**Začetna Stanja:**
- A_RANA = 0.8
- B_SPREJEM = 0.3
- C_MEJE = 0.5
- D_AKCIJA = 0.2
- E_DOKAZ = 0.4
- F_PREPRIČ = 0.6
- G_GRADNJA = 0.3
- T_TOBI = 0.5
- R_REZ = 0.75

**Zunanji Vnosi:**
- C_t = 0.1 (nizka cenzura)
- S_t = 0.2 (nizka sprejetost)
- U_t = 0.7 (visoki sprožilci)
- H_t = 0.8 (visoka somatska napetost)
- Z_t = 0.3 (slab ritem)

**Aktivirani LOCK Operatorji:**
1. **∆REZ_LOCK_01** (R_REZ > 0.7) → φ_B = +0.15, φ_C = +0.10, φ_R = -0.20
2. **∮MIR_LOCK_02** (A_RANA > 0.6) → φ_E = +0.20, φ_B = +0.10, φ_A = -0.15

**Nova Stanja:**
- A_RANA = 0.8 - 0.15 = **0.65**
- B_SPREJEM = 0.3 + 0.15 + 0.10 = **0.55**
- C_MEJE = 0.5 + 0.10 = **0.60**
- R_REZ = 0.75 - 0.20 = **0.55**
- E_DOKAZ = 0.4 + 0.20 = **0.60**

**Ciljna Funkcija (J):**
```
J = 0.3(1 - 0.65) + 0.25(0.55) + 0.2(0.60) + 0.2(0.3) - 0.05(0.55)
J = 0.3(0.35) + 0.25(0.55) + 0.2(0.60) + 0.2(0.3) - 0.05(0.55)
J = 0.105 + 0.1375 + 0.12 + 0.06 - 0.0275 = **0.405**
```

**Interpretacija:**
- **J = 0.405** (nizek) → **Potrebna akcija** za izboljšanje.
- **Priporočilo:**
  - **Zvišaj B_SPREJEM** (sprejem) → Terapija, meditacija
  - **Zvišaj C_MEJE** (meje) → Postavitev osebnih mej
  - **Znižaj A_RANA** (rana) → Odpustitev, sprostitev

---

### **🔹 Primer 2: Ustvarjalni Blok**

**Scenario:** Ustvarjalec doživlja **blok** (D_AKCIJA = 0.1, G_GRADNJA = 0.2).

**Začetna Stanja:**
- A_RANA = 0.3
- B_SPREJEM = 0.7
- C_MEJE = 0.4
- D_AKCIJA = 0.1
- E_DOKAZ = 0.6
- F_PREPRIČ = 0.5
- G_GRADNJA = 0.2
- T_TOBI = 0.4
- R_REZ = 0.3

**Zunanji Vnosi:**
- C_t = 0.2
- S_t = 0.5
- U_t = 0.3
- H_t = 0.4
- Z_t = 0.6

**Aktivirani LOCK Operatorji:**
1. **⊢STOP_LOCK_03** (U_t > 0.5? Ne) → **Ne aktiviran**
2. **≠PAST_LOCK_04** (memory repetition > 2×? Ne) → **Ne aktiviran**

**Priporočilo:**
- **Zvišaj D_AKCIJA** → **Dejanski koraki** (npr. piši 10 minut na dan)
- **Zvišaj G_GRADNJA** → **Ustvarjalni rituali** (npr. jutranje risanje)
- **Zvišaj U_t** → **Sprožilci** (npr. branje, raziskovanje)

**Nova Stanja (po 1 tednu):**
- D_AKCIJA = 0.1 + 0.3 = **0.4**
- G_GRADNJA = 0.2 + 0.3 = **0.5**
- U_t = 0.3 + 0.2 = **0.5**

**Ciljna Funkcija (J):**
```
J = 0.3(1 - 0.3) + 0.25(0.7) + 0.2(0.4) + 0.2(0.5) - 0.05(0.3)
J = 0.3(0.7) + 0.25(0.7) + 0.2(0.4) + 0.2(0.5) - 0.05(0.3)
J = 0.21 + 0.175 + 0.08 + 0.1 - 0.015 = **0.55**
```

**Interpretacija:**
- **J = 0.55** (izboljšan) → **Napredek**, a še vedno prostora za izboljšanje.
- **Priporočilo:**
  - Nadaljuj z **dejanji** (D_AKCIJA)
  - **Ustvarjaj rituale** (G_GRADNJA)

---

### **🔹 Primer 3: Družbeni Konflikt**

**Scenario:** Skupina doživlja **konflikt** (R_REZ = 0.8, C_MEJE = 0.3).

**Začetna Stanja:**
- A_RANA = 0.5
- B_SPREJEM = 0.4
- C_MEJE = 0.3
- D_AKCIJA = 0.6
- E_DOKAZ = 0.5
- F_PREPRIČ = 0.4
- G_GRADNJA = 0.3
- T_TOBI = 0.4
- R_REZ = 0.8

**Zunanji Vnosi:**
- C_t = 0.3
- S_t = 0.4
- U_t = 0.6
- H_t = 0.7
- Z_t = 0.5

**Aktivirani LOCK Operatorji:**
1. **∆REZ_LOCK_01** (R_REZ > 0.7) → φ_B = +0.15, φ_C = +0.10, φ_R = -0.20
2. **⊢STOP_LOCK_03** (U_t > 0.5 and H_t < 0.5? Ne) → **Ne aktiviran**

**Nova Stanja:**
- B_SPREJEM = 0.4 + 0.15 = **0.55**
- C_MEJE = 0.3 + 0.10 = **0.40**
- R_REZ = 0.8 - 0.20 = **0.60**

**Ciljna Funkcija (J):**
```
J = 0.2(1 - 0.5) + 0.3(0.55) + 0.3(0.40) + 0.2(0.3) - 0.05(0.60)
J = 0.2(0.5) + 0.3(0.55) + 0.3(0.40) + 0.2(0.3) - 0.05(0.60)
J = 0.1 + 0.165 + 0.12 + 0.06 - 0.03 = **0.415**
```

**Interpretacija:**
- **J = 0.415** (nizek) → **Potrebna akcija** za reševanje konflikta.
- **Priporočilo:**
  - **Zvišaj C_MEJE** → Postavitev **jasnih mej** v skupini
  - **Zvišaj B_SPREJEM** → **Dialog in poslušanje**
  - **Znižaj R_REZ** → **Mediacija in spravičevanje**

---

---

## 🔄 **Kako Uporabiti TAZV v Praksi**

### **1. Osebni Rast**
- **Izmerite svoje stanje** (npr. A_RANA, B_SPREJEM, itd.)
- **Izračunajte J** (ciljna funkcija)
- **Prepoznajte aktivne LOCK operatorje**
- **Spremembe:** Uporabite **praktične korake** za izboljšanje stanj

### **2. Družbena Dinamika**
- **Analizirajte skupino** (npr. R_REZ, C_MEJE)
- **Prepoznajte konflikte** (visok R_REZ)
- **Uporabite LOCK operatorje** za reševanje
- **Izboljšajte J** skupine

### **3. Ustvarjalnost**
- **Sledite D_AKCIJA in G_GRADNJA**
- **Uporabite Trojne Mostove** (A → ∆ → B)
- **Izogibajte se blokom** (nizka D_AKCIJA)
- **Ustvarjajte rituale** (visoka G_GRADNJA)

### **4. Duhovno Razumevanje**
- **Razmislite o A_RANA in B_SPREJEM**
- **Uporabite ∮MIR_LOCK_02** za sprostitev
- **Sledite procesom** (J kot merilo napredka)

---

## 📌 **Povezave z Drugimi Canvas-i**

- **[Beseda je Ne — Osnovni Sistem](canvas://beseda-je-ne-master)** — Osnovni principi in struktura.
- **[92 Nujnosti](canvas://nujnosti-92)** — Kvantna stanja kot ontološki operatorji.
- **[OPTIKON Corpus](canvas://optikon-50)** — Razširjen katalog besed.
- **[Stotnije (A-DOSJE)](canvas://stotnije-a-dosje)** — Besedni dosjeji.
- **[REK/EGO Dialogi](canvas://rek-ego-dialogi)** — Strukturirani pogovori.
- **[RES Katalog](canvas://res-katalog)** — Somatsko-zavestna stanja.
- **[Glifi v Praksi](canvas://glifi-v-praksi)** — Uporaba glifov v življenju.

---

## 🎯 **Zaključek**

**TAZV** je **orodje za razumevanje in usmerjanje** osebnih, družbenih in duhovnih procesov. Uporabljajte TAZV za:
- **Razumevanje stanj** (kvantificiranje čustev in misli)
- **Reševanje problemov** (prepoznavanje in prilagajanje stanj)
- **Osebni rast** (usmerjanje napredka)
- **Ustvarjalnost** (prekoračitev blokov)

> "TAZV ni le model — **TAZV je jezik**, ki vam pomaga **govoriti z bitjem**."

---

**"Matematika je jezik — TAZV je njegova poezija."**