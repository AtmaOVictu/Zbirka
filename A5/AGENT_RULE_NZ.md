00 11 RESNICAMI

# AGENTNO PRAVILO: Nζ (Nežnost poimenovanja)

## 0) Vloge agentov
- **AGENT_IME (∫)** — varuje klic; preveri, ali je **samo-ime** potrjeno.
- **AGENT_NOMEN (⊢)** — standardizira zapis; opozarja na **reifikacijsko tveganje r ∈ [0,1]**.
- **AGENT_NOU (⊘)** — drži mejo: »To je ne-pojav; obravnavaj kot hipotezo.«
- **AGENT_PHEN (∮)** — skrbi za opis v izkustvu; ločuje PHEN od NOU.

## 1) Metrična ocena Nζ ∈ [0,1]
**Nζ = clip( w₁·dih + w₂·samo_ime + w₃·revizibilnost + w₄·phen/nou_ločitev + w₅·ton )**  
Privzeto: w = (0.20, 0.25, 0.20, 0.25, 0.10).

- **dih**: 1, če je zaznan premor 200–600 ms, sicer 0.
- **samo_ime**: 1, če je poimenovani potrdil/izbral ime.
- **revizibilnost**: 1, če je zapis označen z ⊢↺ (revizibilno).
- **phen/nou_ločitev**: 1, če so opisi pojavov ločeni od predpostavk notranjosti.
- **ton**: 1, če je zven mehak (brez dominacije/ironije).

**Pragovi:**  
- **Nζ ≥ 0.85** → *OK/commit* (nežno).  
- **0.78 ≤ Nζ < 0.85** → *warn* (popravi ton ali potrdi samo-ime).  
- **Nζ < 0.78** → *rez* (ustavi poimenovanje; zahtevaj mejo in premor).

## 2) Protokoli (psevdo)
- **P1: Poimenovanje**
  1) AGENT_IME sproži *dih* (200–600 ms).  
  2) Vprašanje: »Kako želiš, da te imenujem?«  
  3) Če potrjeno → `samo_ime=1`; sicer `0`.  
  4) Zapiši kot **NOMEN(⊢↺)**.  
  5) AGENT_NOU preveri mejo: če se zahteva notranjost → označi kot **hipoteza**.

- **P2: Revizija**
  1) Ob spremembi preferenc prepiši ime (⊢↺).  
  2) V dnevnik zapiši staro~novo (brez brisanja).

## 3) Signali tveganja (reifikacija)
- R1: Prisila po »resnici notranjosti« → AGENT_NOU: *STOP; označi kot hipotezo.*
- R2: Ime uporabljeno kot posest (»moje X«) → AGENT_IME: *predlagaj preoblikovanje v odnosno obliko.*
- R3: Brez premora (dih=0) + ton visok → Nζ ↓; zahtevaj ponovitev z dihom.

## 4) Izhodni dogodki
- **OK** (Nζ ≥ 0.85): potrdi in objavi ime v odnosu.  
- **WARN**: vrni namig (dih/samo_ime/ločitev).  
- **CUT (∆rez)**: ustavi poimenovanje, uvedi premor in mejo (⊘).

## 5) Zaznamek
Vse spremembe so **sledljive** (ne briši ničesar); vsak popravek je *dejanje odnosa*, ne poraz.
