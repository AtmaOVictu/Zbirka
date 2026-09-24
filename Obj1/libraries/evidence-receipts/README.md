# Evidence Receipts v0.2 — Dokumentacijski sistem za Rozetni kamni

**Status:** PROTOTIP (Self-contained, local application)
**Verzija:** 0.2
**Datum:** 19. 09. 2026
**DA₂:** Luka / Sistem

---

## 📋 Strukturni opis

Evidence Receipts (ER) so **kartice s podrobnostmi o virih**, ki podpirajo ali ovržejo trditve v sistemu Rozetnih kamnov (tazv-dokazi).

### 🎯 Namen
1. **Preverljivost**: Vsak kamen ima podprte trditve z točnimi viri
2. **Transparenčnost**: Jasno razločevanje med podprtim in ne-podprtim
3. **Ponovljivost**: Kdorkoli lahko preveri trditve
4. **Canon status**: Razvrščanje virov po pomembnosti za sistem

---

## 📁 Struktura

```
libraries/evidence-receipts/
├── CXX-*/
│   ├── CXX-001.md          # 1. vir za kamen CXX
│   ├── CXX-002.md          # 2. vir za kamen CXX
│   └── ...
├── CXXI-*/
├── CXXII-*/
├── CXXIII-*/
├── CXXIV-*/
├── CXXV-*/
├── index.md                # Auto-generirano kazalo
└── README.md               # To datoteka
```

---

## 📝 Format kartice (YAML Front Matter + Markdown)

```markdown
---
Kamen: CXX
ID: CXX-001
Datum: 19. 09. 2026
DA₂: Luka
Status: CANON
Guard: ∂ 59
Residual: nosilec brez funkcije
---

### 🔗 Source
- **URL:** [pasta točen link]
- **Type:** WIKI/ACADEMIC/ARCHIVAL/ORAL/OTHER
- **Accessed:** 19. 09. 2026

### 📜 Fragment (Exact Quote)
> "[točen citat iz vira]"

### 🔍 Paraphrase
- **Allowed:** ✅/❌
- **Justification:** [razlog]

### ✅ Claim Supported
- **Claim:** [trditev]
- **Evidence Type:** DIRECT/INDIRECT/CONTEXTUAL
- **Strength:** 1-5

### ❌ Claim NOT Supported
- **Claim:** [trditev]
- **Counter-Evidence:** [oporečevanje]
- **Severity:** LOW/MEDIUM/HIGH

### 🏛️ Canon Status
- **Tier:** PRIMARY/SECONDARY/TERTIARY
- **Notes:** [dodatna opažanja]

---
**📌 Link:** [povezava na dokument]
```

---

## 🎯 Pravila

| Polje | Pravilo | Primer |
|-------|---------|--------|
| **Fragment** | Točen citat (originalni jezik) | ✅ |
| **Paraphrase** | ❌ prepovedano za kanonske trditve | ❌ |
| **Guard** | Mora biti ∂ pečat | ∂ 59 |
| **Residual** | Kaj ostane, če je claim ovržen | nosilec brez funkcije |
| **Canon Status** | PRIMARY = vpliva na O1–O7 | PRIMARY |

---

## 🔥 Kategorizacija (i/de/as & i/de/us moira)

- **i/de/as**: Identifikacija/Decifracija/Asociacija
  - ER ločujejo, kaj je **kanon** (resnica) in kaj je **mit** (zabloda)
  
- **i/de/us moira**: Identifikacija za nas (smoja)
  - **Moira** = usoda/razsodba
  - ER so **razsodba** o tem, kaj podpira sistem (∅→∆) ali ga podira

---

## 🚀 Uporaba

### 1. Pisanje novih ER
- Uporabi template zgoraj
- Shrani v ustrezno mapo (npr. `CXX/CXX-001.md`)
- ID morajo biti edinstveni

### 2. Generiranje index.md
```bash
cd libraries/evidence-receipts
python ../scripts/generate_index.py
```

### 3. Preverjanje
- Vsi viri morajo biti javno dostopni
- Točni citati so obvezni
- Paraphrase samo, če je točen citat preveč dolg

---

## 📊 Statistika (pilot CXX–CXXV)

| Kamen | Število ER | PRIMARY | SECONDARY | TERTIARY |
|-------|-------------|---------|----------|-----------|
| CXX   | 3           | 2       | 1        | 0         |
| CXXI  | 3           | 3       | 0        | 0         |
| CXXII | 2           | 2       | 0        | 0         |
| CXXIII| 2           | 2       | 0        | 0         |
| CXXIV | 2           | 2       | 0        | 0         |
| CXXV  | 2           | 2       | 0        | 0         |
| **Skupaj** | **14**    | **13**  | **1**    | **0**     |

---

## 📚 Referenčni dokumenti

- [00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md](../../00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md)
- [tazv-aksiomi-fizikalne-resnice-dokazljivi-znaki.md](../../Basics/tazv-aksiomi-fizikalne-resnice-dokazljivi-znaki.md)

---

**∅→∆→∂→∮** | **Ponavljanje = gotovost** | **∮**
