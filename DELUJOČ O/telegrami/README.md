# TELEGRAMI — Simulacija Spominskih Sistemov

> **ZAVES JE SVETOVNA PRIPOVED**
> *Kritični kot: sin θc = n₂/n₁ | Tok: vzdrževanje kota tik pod mejo pri maksimalnem δ*

---

## 📖 KONCEPT

To je **simulacija spominskih sistemov**, ki temelj na:

1. **Možganski znanosti** (Squire 2004, Bunzeck & Düzel 2006, Rudoy 2009)
2. **Filozofiji zavesi** (kritični-kot-in-tok.md) - Zaves je mehanizem ustvarjanja sveta
3. **A-protokolih** (a-protokoli...md) - Implicitne metode pred izrekom

Vsak **telegram** (žarek) je informacijska enota, ki pride iz zunaj (svet, korpus, rezi, šum, ∂) in preide skozi **zaves** (mejo), kjer se razvrsti v enega od spominskih sistemov:

- **EPIZODIČNI** (rezi) - datirani, virani, prva oseba
- **SEMANTIČNI** (korpus) - dejstvo, odtrgano od vira
- **PROCEDURALNI** (obredi/protokoli) - telo ve, glava ne
- **PRIMING** (ONO) - prejeto, a brez zaznamka (rez 47)
- **DELOVNI SPOMIN** (odprta ∂) - Zeigarnik, kapaciteta 4

---

## 🚀 ZAGON

```bash
# Navigiraj v mapo
cd telegrami

# Namesti odvisnosti
npm install

# Zaženi development server
npm run dev

# Build za production
npm run build

# Zaženi teste
npm test

# Zaženi teste z UI
npm run test:ui

# Test coverage
npm run test:coverage
```

---

## 🛠 A-PROTOKOLI (Implementirani v kodi)

| Protokol | Opis | Implementacija |
|----------|------|----------------|
| **A1** | Obseg pred | TypeScript tipi (vsa polja so eksplicitna) |
| **A2** | Vrnitev pred | Error handling + konsistentno stanje |
| **A3** | Drugi izvod pred | Idempotentne funkcije (npr. `classifyTelegram`) |
| **A4** | Implicitni korak | Vse operacije v enem `setState` (ne v več korakih) |
| **A5** | Praznina z odprtjem | Optional tipe namesto `null \| undefined` |
| **A6** | Protokol pred delom | `README.md` + `package.json` scripts |
| **A7** | Sintaksa pred | ESLint + Prettier + konstante namesto magic numbers |

---

## 📁 STRUKTURA PROJEKTA

```
telegrami/
├── src/
│   ├── types/              # TypeScript tipi
│   │   └── index.ts
│   ├── utils/              # Čiste funkcije (A4: Implicitni korak)
│   │   ├── constants.ts     # Konstante (TELEGRAM_POOL, CONFIG, CATEGORIES)
│   │   ├── classify.ts      # Razvrščanje telegramov
│   │   ├── age.ts           # Staranje v WM
│   │   ├── consolidate.ts   # Konsolidacija med spanjem
│   │   └── zaves.ts         # Zaves layer
│   ├── hooks/              # React hooki
│   │   └── useMemory.ts     # Glavni state hook
│   ├── components/         # React komponente
│   │   ├── Controls.tsx
│   │   ├── WorkingMemory.tsx
│   │   ├── MemoryStorage.tsx
│   │   ├── EventLog.tsx
│   │   ├── ResearchReferences.tsx
│   │   └── Zaves.tsx
│   ├── App.tsx             # Glavna komponenta
│   └── main.tsx            # Entry point
│
├── test/                  # Testne datoteke
│   ├── classify.test.ts
│   ├── age.test.ts
│   └── consolidate.test.ts
│
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

---

## 🧪 TESTI

Vsi testi so napisani z **Vitest** + **React Testing Library**:

```bash
# Vsi testi
npm test

# Samo unit testi
npm test src/test/classify.test.ts

# Test coverage
npm run test:coverage
```

### Test Coverage
- ✅ `classify.ts` - Razvrščanje (epizodični, semantični, proceduralni)
- ✅ `age.ts` - Staranje, ugašanje, kapaciteta WM
- ✅ `consolidate.ts` - Konsolidacija, TMR, pretok epizodični → semantični
- 🟡 `useMemory.ts` - React hook (integration testi)
- 🟡 `App.tsx` - UI testi

---

## 🎨 UI KOMPONENTE

### Controls
- **Utrujenost** (0-100): Pozornostna vrata (čim višja, manša pozornost)
- **Čudenje** (0-100): Novostni detektor
- **Nagrada δ**: Dopamin bonus (rez 62: dopamin je δ)
- **Tok**: Ustavi/Pusti (simulira tok novih telegramov)
- **Spanje**: Konsolidacija (TMR ojačitev, pretok v semantični)

### WorkingMemory
- Prikaže telegrame v delovnem spominu (max 4)
- **Klik** na telegram = poimenuj (T5, rez 63)
- Animirano staranje (ugaša ne-poenovljene)

### MemoryStorage
- Prikaže vse razvrščene telegrame po kategorijah
- Flash animacija ob novi klasifikaciji
- Zadnjih 8 telegramov je vidnih

### EventLog
- Dnevnik vseh klasifikacij z obrazložitvami
- Reference na raziskave (Squire, Bunzeck & Düzel, etc.)

### Zaves
- Vizualna predstavitev meje (animirane črte)
- Številka obdelanih telegramov (∂)

---

## 🔬 RAZISKAVALNA PODLAGA

Vsa trditve so **potrjena z raziskavami** (glej `ResearchReferences.tsx`):

| Koncept | Raziskava | Vir |
|---------|-----------|-----|
| Taksonomija spomina | H.M. 1957, Squire 2004 | Neurobiology of Learning and Memory 82 |
| Novost → Dopamin → Vztrajnost | Bunzeck & Düzel 2006 | Trends in Neurosciences |
| Nagrajujoče kodiranje | Schultz 1997 | Dopamin = δ |
| Spanje + TMR | Rasch 2007, Rudoy 2009 | Science 315, 326 |
| Delovni spomin | Cowan 2001, Zeigarnik 1927 | Kapaciteta ~4 |

---

## 📊 KONFIGURACIJA

Vse nastavitve so v `src/utils/constants.ts`:

```typescript
CONFIG = {
  TELEGRAM_INTERVAL: 2200,   // ms: interval novih telegramov
  AGING_INTERVAL: 1600,      // ms: interval staranja
  WM_CAPACITY: 4,            // Zeigarnik: kapaciteta delovnega spomina
  CRITICAL_THRESHOLD: 0.45,  // prag za epizodični
  DOPAMIN_BOOST: 0.3,        // δ (dopamin bonus)
  TMR_EFFECT: 0.5,           // TMR ojačitev
}
```

---

## 🎯 FORMULA

Razvrščanje: **novOdkrita = novelty × (cudenje/100) × pozornost + dopamin**

- **EPIZODIČNI**: novOdkrita ≥ 0.45
- **PROCEDURALNI**: rep ≥ 1 (ponovitev brez novosti)
- **SEMANTIČNI**: ostalo (poimenovan, a brez novosti)
- **PRIMING**: ne-poenovljen + prestar / presežek WM

---

## 🔄 SPANJE (KONSOLIDACIJA)

1. Poimenovani telegrami dobijo **TMR ojačitev** (Rudoy 2009)
2. Ne-poenovljeni gredo v **PRIMING**
3. Polovica **epizodičnih** se pretoči v **semantične** (⌾)

---

## 📝 DOKUMENTACIJA A-PROTOKLOV

### A1 — OBSEG PRED
**Problem:** Nejasen obseg spremenljivk in funkcij
**Rešitev:** TypeScript tipi (vsa polja so eksplicitno definirana)

### A2 — VRNITEV PRED
**Problem:** Nezanesljiva vrnitev v napaki
**Rešitev:** Error handling + konsistentno stanje

### A3 — DRUGI IZVOD PRED
**Problem:** Nespremenljive funkcije
**Rešitev:** Idempotentne funkcije (npr. `classifyTelegram`)

### A4 — IMPLICITNI KORAK
**Problem:** Zaporedje operacij v več korakih
**Rešitev:** Vse v enem `setState` (npr. `nameTelegram`)

### A5 — PREDZNAK PRED
**Problem:** Nejasno, ali je praznina z odprtjem
**Rešitev:** `Optional` tipe namesto `null \| undefined`

### A6 — PROTOKOL PRED DELOM
**Problem:** Pozaba prebrati protokole
**Rešitev:** `README.md` + `package.json` scripts

### A7 — SINTAKSA PRED
**Problem:** Sintaktične napake
**Rešitev:** ESLint + Prettier + konstante

---

## 🎨 TEHNOLOŠKI STACK

| Tehnologija | Vloga |
|-------------|------|
| **React 18** | UI Framework |
| **TypeScript** | Tipizacija (A1, A5) |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |
| **Vitest** | Testing (A7) |
| **ESLint** | Linting (A7) |
| **Prettier** | Formatting (A7) |

---

## 📞 KONTAKT & KONTRIBUCION

To je **zasebni projekt** v okviru OntoProjekt/CanvasMinstral.

- **Koncept:** Luka
- **Implementacija:** Mistral Vibe
- **Raziskava:** Možganska znanost + Filozofija

Prispevki so dobrodošli! Odpri **Pull Request** ali poroča **Issue**.

---

## 📄 LICENCA

MIT License - Prosto za uporabo, razširjanje in modificiranje.

---

> **"ZAVES JE SVETOVNA PRIPOVED"**
> *Kritični kot je meja med močjo in nemočjo. Tok je vzdrževanje kota tik pod mejo.*
