#!/usr/bin/env python3
"""
TAZV Faza 5 — Integracijski most C3 ↔ B2
=========================================
Ta bootstrap povezuje:
  - CORPUS cevovod (7-fazni: ∅→¬→∆→∂→⧖→∮→⟡) z 5-gumbnim UI
  - ARegister (apercepcija → operator) z SOMA_PROMPT
  - ProcessingPipeline + SymbolMapper (obstoječa arhitektura) s Preverbo
  - VS Code asistentove datoteke (B2) s korpus-specifikacijo (C3)

Korpus:
  - CORPUS cevovod: "cevovod ∅→¬→∆→⊢→∂→∮→⟡" (Obs11, 7195d9d3)
  - ARegister: "osnovni jezik → apercepcija → operator" (Obs11, c7638bad)
  - Preverba: "5 preizkusov + soma + DOCTRINARIUM" (Obs11, 320d6f6a)
  - "CORPUS ni dodaten gumb. CORPUS je operator, ki deluje v prehodu
     med ZAJEMI in POKAŽI" (Obs11, 7195d9d3)

Generira:
  1. comprehension/core/aregister_bridge.py   — ARegister → R-7 preslikava
  2. comprehension/core/corpus_integrator.py  — CORPUS 7-fazni cevovod
  3. comprehension/core/preverba_bridge.py    — ProcessingPipeline ↔ Preverba
  4. comprehension/ui/main_window_v5_integrated.py — integrirani UI z QMessageBox SOMA

Run: python tazv_phase5_integration_bootstrap.py
CWD:  D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
"""

import os
from pathlib import Path

BASE = Path("comprehension_machine")
CORE = BASE / "comprehension" / "core"
UI   = BASE / "comprehension" / "ui"

for d in (CORE, UI):
    d.mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


# ============================================================
# 1. comprehension/core/aregister_bridge.py
#    ARegister: user expression → perception → operator (glyph)
#    Korpus: Obs11 c7638bad (00-11-resnicami.tsx)
# ============================================================

write_file(CORE / "aregister_bridge.py", r'''"""
ARegister Bridge — apercepcija → operator
=========================================
Korpus: "ARegister slovar: osnovni jezik → apercepcija → operator"
         (Obs11, 00-11-resnicami-comprehension-machine.tsx)

ARegister je VHODNI slovar. Ko uporabnik izrazi stanje (besedo),
ARegister prepozna apercepcijo in vrne ustrezen R-7 glyph.

To ni iskanje pomena — je prepoznavanje operacije, ki je ze aktivna
v uporabnikovi izkusnji. ARegister ne interpretira; prepozna.

Struktura (iz korpusa):
  userExpression → perception → glyph → inquiry → etymology

Uporaba:
  from comprehension.core.aregister_bridge import ARegisterBridge
  bridge = ARegisterBridge()
  entry = bridge.recognize("prazno")
  # → {glyph: "∅", perception: "...", inquiry: "...", etymology: "..."}
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ARegisterEntry:
    """Vnos iz ARegister slovarja (iz korpusa c7638bad)."""
    user_expression: str   # npr. "empty / prazno"
    perception: str         # apercepcija: kaj telo cuti
    glyph: str              # R-7 korenski glif
    inquiry: str            # vprasanje etaže
    etymology: str          # etimologija glifa


# Korpus-validirani ARegister vnosi (iz 00-11-resnicami.tsx)
AREGISTER_DATA = [
    ARegisterEntry(
        user_expression="empty / prazno",
        perception="I feel nothing — but the nothing feels open, not absent",
        glyph="∅",
        inquiry="Kaj se odpira v praznini, ki jo cutis? Ali je praznina pogoj, ne odsotnost?",
        etymology="∅ (1939, André Weil, iz norveske crke) — v tem sistemu: pogoj, ki omogoca, ne manjkajoci",
    ),
    ARegisterEntry(
        user_expression="separated / loceno",
        perception="Something was cut — I feel the edge",
        glyph="¬",
        inquiry="Kaj je rez locil? Ali je rez odprtje ali prekinitev?",
        etymology="¬ (logika) — v tem sistemu: locitev kot odprtje, ne negacija (§54)",
    ),
    ARegisterEntry(
        user_expression="moving / gibljoco",
        perception="I feel a shift — something is becoming",
        glyph="∆",
        inquiry="Kaj se spreminja? Ali je ∆ prehod ali sila?",
        etymology="∆ (grs. delta) — sprememba, razlika, derivative",
    ),
    ARegisterEntry(
        user_expression="sealed / zapechateno",
        perception="Something completed — an act that cannot be undone",
        glyph="1",
        inquiry="Kaj je zapechateno? Ali je 1 dejanje ali potrditev?",
        etymology="1 — terminal object, SEAL, unit, dejanje",
    ),
    ARegisterEntry(
        user_expression="still / tiho",
        perception="I feel a pulse — silence after speaking",
        glyph="⧖",
        inquiry="Kaj je utrip? Ali je cas parameter ali izgovor?",
        etymology="⧖ — cas kot parameter, utrip, periodicity",
    ),
    ARegisterEntry(
        user_expression="returning / se vračajoče",
        perception="Something comes back — but different",
        glyph="∮",
        inquiry="Kaj se vraca? Ali je ∮ povratek ali integracija?",
        etymology="∮ — integral, cikel, povratna zveza, loop",
    ),
    ARegisterEntry(
        user_expression="opening / odpirajoče",
        perception="Something opened that wasn't there before — an echo, a door",
        glyph="⟡",
        inquiry="Kaj se odpira? Ali je nova moznost odmev prejsnjega cikla?",
        etymology="⟡ — resonanca, odmev; nova moznost, ki izhaja iz ∮",
    ),
    ARegisterEntry(
        user_expression="transitioning / prehajajoče",
        perception="I'm between — not here, not there, but in the passage itself",
        glyph="∂",
        inquiry="Kaj se prehaja? Med cim in cim? Ali si v rezu ali na robu reza?",
        etymology="∂ (matematika) — prehod, partialna derivative; rez, ki povezuje abstrakcijo in izvedbo",
    ),
    ARegisterEntry(
        user_expression="present / prisotno",
        perception="I feel something that stays — beneath the noise",
        glyph="∫",
        inquiry="Kaj ostane, ko sum preide? Ali je ∫ prisotnost ali molk?",
        etymology="∫ — integral kot prisotnost; kar ostane, ko prehod preide",
    ),
    ARegisterEntry(
        user_expression="related / povezano",
        perception="I feel a connection — something links to something else",
        glyph="∴",
        inquiry="Kaj povezuje? Ali je ∴ vzroc ali zaveza?",
        etymology="∴ — odnos, vzrocnost, povezava, relacija",
    ),
]


class ARegisterBridge:
    """
    ARegister most: prepozna uporabnikovo besedo in vrne aperceptivni vhod.

    Korpus: "ARegister funkcija: prepozna uporabnikovo besedo
             in vrne aperceptivni vhod" (c7638bad)
    """

    def __init__(self):
        self.entries = AREGISTER_DATA

    def recognize(self, input_text: str) -> Optional[ARegisterEntry]:
        """
        Prepozna uporabnikov izraz in vrne ustrezen ARegister vnos.
        Isce po user_expression polju (split po '/').
        """
        lower = input_text.lower().strip()
        for entry in self.entries:
            expressions = [e.strip().lower() for e in entry.user_expression.split("/")]
            if any(expr in lower for expr in expressions):
                return entry
        return None

    def glyph_for(self, input_text: str) -> str:
        """Vrne glyph za izraz, ali None."""
        entry = self.recognize(input_text)
        return entry.glyph if entry else None

    def inquiry_for(self, input_text: str) -> str:
        """Vrne vprasanje etaže za izraz."""
        entry = self.recognize(input_text)
        return entry.inquiry if entry else ""

    def all_glyphs(self) -> list:
        """Vrne vse registrirane glyphe."""
        return [e.glyph for e in self.entries]
''')


# ============================================================
# 2. comprehension/core/corpus_integrator.py
#    CORPUS 7-fazni cevovod: ∅→¬→∆→∂→⧖→∮→⟡
#    Korpus: Obs11 7195d9d3 (corpus-cevovod-prevoda)
# ============================================================

write_file(CORE / "corpus_integrator.py", r'''"""
CORPUS Integrator — 7-fazni prevajalski cevovod
================================================
Korpus: "CORPUS je operativni prevajalski cevovod iz prostor-iwen,
         ki vsak zunanji sistem preslika v univerzalne korenske glife
         preko cevovoda ∅→¬→∆→⊢→∂→∮→⟡" (Obs11, 7195d9d3)

7 FAZ CORPUS-ja (R-7 mapping):
  1. ZAJEMI    ∅  — zunanji sistem vstopi kot celotno polje
  2. PREVEDI   ¬  — rez: izvorni operator se loci od izvornega imena
  3. PRESLIKAJ ∆  — preslikava: kateri korenski glif izvaja isto operacijo?
  4. VSTOP     ∂  — preslikava postane operativna v modulu
  5. PREVERI   ⊢  — tišina po aktu: ali telo potrjuje? (5 preizkusov + soma)
  6. ATLAS     ∮  — povratek: preslikava dobi pozicijo v zemljevidu
  7. ODPRI     ⟡  — nova moznost: katero dimenzijo odpre ta preslikava?

"CORPUS ni dodaten gumb. CORPUS je operator, ki deluje v prehodu
 med ZAJEMI in POKAŽI." (Obs11, 7195d9d3)

5-GUMBNI UI → CORPUS 7-FAZNI mapping:
  ZAJEMI O  → CORPUS ZAJEMI (∅)
  REŽI ⊘   → CORPUS PREVEDI (¬)        ← CORPUS deluje tu
  POKAŽI ∆ → CORPUS PRESLIKAJ (∆)      ← CORPUS deluje tu
                + CORPUS VSTOP (∂)      ← vstopi v modul znotraj POKAŽI
  PREVERI ⊢ → CORPUS PREVERI (⊢)      ← 5 preizkusov + soma
  SHRANI ∮  → CORPUS ATLAS (∮)
                + CORPUS ODPRI (⟡)     ← nova dimenzija se odpre pri SHRANI

Prevajalska tabela (6 stolpcev iz korpusa):
  Izvorno ime | Izvorni material | Izvorni operator | Korenski glif | Modul | Preverba
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class CorpusPhase(Enum):
    ZAJEMI = "∅"
    PREVEDI = "¬"
    PRESLIKAJ = "∆"
    VSTOP = "∂"
    PREVERI = "⊢"
    ATLAS = "∮"
    ODPRI = "⟡"


class PreverbaKot(Enum):
    ANALOGNI = "analogni"      # razkrije funkcijo → PASS
    NADOMESTNI = "nadomestni"  # zamegli razliko → FAIL
    NEZNANO = "neznano"


@dataclass
class PrevajalskaTabela:
    """6-stolpcna prevajalska tabela iz korpusa."""
    izvorno_ime: str = ""           # npr. "Alkimija"
    izvorni_material: str = ""      # npr. "pigment"
    izvorni_operator: str = ""     # npr. "nigredo"
    korenski_glif: str = ""        # npr. "∅"
    modul: str = ""                 # npr. "MACRO"
    preverba: str = PreverbaKot.NEZNANO.value


@dataclass
class CorpusResult:
    faza: str = ""
    glif: str = ""
    rezultat: str = ""             # PASS / FAIL / MEGla
    analogni_ali_nadomestni: str = ""
    modul: str = ""
    atlas_pozicija: str = ""       # kam v univerzalnem zemljevidu
    nova_dimenzija: str = ""       # katero dimenzijo odpre
    soma: str = ""                 # SOMA_PASS / SOMA_FAIL
    opis: str = ""


class CorpusIntegrator:
    """
    CORPUS cevovod — prevaja zunanje sisteme v korenske glife.

    Korpus: "CORPUS ni slovar ampak procesor, ki prevaja sisteme
             v operativna dejanja preko cevovoda ∅→¬→∆→⊢→∂→∮→⟡"
    """

    # Ze preslikani sistemi iz korpusa (prostor-iwen §7.1)
    PRESLIKANI_SISTEMI = [
        # Alkimija
        PrevajalskaTabela("Alkimija","pigment","nigredo","∅","MACRO","analogni"),
        PrevajalskaTabela("Alkimija","pigment","albedo","¬","MMARK","analogni"),
        PrevajalskaTabela("Alkimija","pigment","citrinitas","∆","STATE","analogni"),
        PrevajalskaTabela("Alkimija","pigment","rubedo","∮","APD","analogni"),
        # Kibalion
        PrevajalskaTabela("Kibalion","nacelo","mentalizem","∫","MACRO","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","korespondenca","⟡","VISUALIZATION","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","vibracija","∂","TONOS","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","polariteta","¬","STATE","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","ritem","∮","MICRO","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","vzrok_posledica","∴","APD","analogni"),
        PrevajalskaTabela("Kibalion","nacelo","spol","∆","STATE","analogni"),
        # Cakre
        PrevajalskaTabela("Cakre","telo/energija","koren","∅","MACRO","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","sakralna","¬","STATE","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","solarni_pleksus","∆","APD","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","srce","1","MMARK","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","grlo","⧖","VISUALIZATION","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","tretje_oko","∮","MICRO","analogni"),
        PrevajalskaTabela("Cakre","telo/energija","temenska","⟡","DA'AT","analogni"),
        # Wu Xing
        PrevajalskaTabela("Wu Xing","element+smer","les","∆","MMARK","analogni"),
        PrevajalskaTabela("Wu Xing","element+smer","ogenj","1","STATE","analogni"),
        PrevajalskaTabela("Wu Xing","element+smer","zemlja","∅","DA'AT","analogni"),
        PrevajalskaTabela("Wu Xing","element+smer","kovina","¬","VISUALIZATION","analogni"),
        PrevajalskaTabela("Wu Xing","element+smer","voda","∫","MICRO","analogni"),
    ]

    def __init__(self):
        self.tabele = list(self.PRESLIKANI_SISTEMI)
        self.rezultati: list[CorpusResult] = []

    def najdi_preslikavo(self, izvorno_ime: str, izvorni_operator: str) -> Optional[PrevajalskaTabela]:
        """Najdi ze obstojeco preslikavo za sistem + operator."""
        for t in self.tabele:
            if t.izvorno_ime.lower() == izvorno_ime.lower() and \
               t.izvorni_operator.lower() == izvorni_operator.lower():
                return t
        return None

    def dodaj_sistem(self, tabela: PrevajalskaTabela):
        """Dodaj novo prevajalsko tabelo."""
        self.tabele.append(tabela)

    def odpelji_cevovod(self, izvorno_ime: str, izvorni_operator: str,
                        izvorni_material: str = "", soma_rezultat: str = "",
                        preverba_rezultati: dict = None) -> list[CorpusResult]:
        """
        Odpelje poln CORPUS cevovod (7 faz) za en sistem.

        Korpus: "Ce preslikava ne razkrije funkcije, temvec jo zamegli,
                 je nadomestni kot — megla, ne prepoznanje."
        """
        preverba_rezultati = preverba_rezultati or {}
        rezultati = []

        # 1. ZAJEMI ∅
        r1 = CorpusResult(faza="ZAJEMI", glif="∅",
            rezultat="PASS" if izvorno_ime else "FAIL",
            opis=f"Zunanji sistem '{izvorno_ime}' vstopi kot celotno polje")
        rezultati.append(r1)

        # 2. PREVEDI ¬ — rez
        tabela = self.najdi_preslikavo(izvorno_ime, izvorni_operator)
        r2 = CorpusResult(faza="PREVEDI", glif="¬",
            rezultat="PASS" if tabela else "FAIL",
            modul=tabela.modul if tabela else "",
            opis=f"Rez: '{izvorni_operator}' se loci od '{izvorno_ime}'")
        rezultati.append(r2)

        if not tabela:
            # FAIL pri rezu → MEGla
            r_fail = CorpusResult(faza="PREVEDI", glif="¬", rezultat="MEGla",
                opis="Rez ni nasel preslikave — nadomestni kot")
            rezultati.append(r_fail)
            self.rezultati.extend(rezultati)
            return rezultati

        # 3. PRESLIKAJ ∆ — analogni ali nadomestni?
        analogni = tabela.preverba == PreverbaKot.ANALOGNI.value
        r3 = CorpusResult(faza="PRESLIKAJ", glif="∆",
            rezultat="PASS" if analogni else "FAIL",
            analogni_ali_nadomestni=tabela.preverba,
            modul=tabela.modul,
            opis=f"Preslikava: '{izvorni_operator}' → '{tabela.korenski_glif}' ({tabela.preverba} kot)")
        rezultati.append(r3)

        if not analogni:
            r_meg = CorpusResult(faza="PRESLIKAJ", glif="∆", rezultat="MEGla",
                opis="Nadomestni kot — zameglitev. Pošlji v TRAINARIUM.")
            rezultati.append(r_meg)
            self.rezultati.extend(rezultati)
            return rezultati

        # 4. VSTOP ∂ — preslikava postane operativna v modulu
        r4 = CorpusResult(faza="VSTOP", glif="∂",
            rezultat="PASS", modul=tabela.modul,
            opis=f"Preslikava '{tabela.korenski_glif}' postane operativna v modulu {tabela.modul}")
        rezultati.append(r4)

        # 5. PREVERI ⊢ — 5 preizkusov + soma
        preverba_pass = all(v == "PASS" for v in preverba_rezultati.values()) if preverba_rezultati else True
        soma_pass = soma_rezultat == "SOMA_PASS" if soma_rezultat else True
        r5 = CorpusResult(faza="PREVERI", glif="⊢",
            rezultat="PASS" if (preverba_pass and soma_pass) else "FAIL",
            soma=soma_rezultat,
            opis=f"5 preizkusov + soma: preverba={'PASS' if preverba_pass else 'FAIL'}, soma={soma_rezultat or 'neznano'}")
        rezultati.append(r5)

        if not (preverba_pass and soma_pass):
            r_meg2 = CorpusResult(faza="PREVERI", glif="⊢", rezultat="MEGla",
                opis="Preverba ali soma FAIL — pošlji v TRAINARIUM kot drill")
            rezultati.append(r_meg2)
            self.rezultati.extend(rezultati)
            return rezultati

        # 6. ATLAS ∮ — pozicija v univerzalnem zemljevidu
        r6 = CorpusResult(faza="ATLAS", glif="∮",
            rezultat="PASS", modul=tabela.modul,
            atlas_pozicija=f"{izvorno_ime}:{izvorni_operator} → {tabela.korenski_glif} @ {tabela.modul}",
            opis=f"Preslikava dobi pozicijo v Atlasu: {tabela.korenski_glif} @ {tabela.modul}")
        rezultati.append(r6)

        # 7. ODPRI ⟡ — nova dimenzija
        r7 = CorpusResult(faza="ODPRI", glif="⟡",
            rezultat="PASS",
            nova_dimenzija=f"{izvorno_ime} odpira dimenzijo preko {tabela.korenski_glif}",
            opis="Nova moznost: sirjenje, ne akumulacija")
        rezultati.append(r7)

        self.rezultati.extend(rezultati)
        return rezultati

    def map_5gumbov_v_corpus(self) -> list:
        """
        Vrne mapping 5-gumbnega UI na 7-fazni CORPUS.

        Korpus: "CORPUS ni dodaten gumb. CORPUS je operator, ki deluje
                 v prehodu med ZAJEMI in POKAŽI."
        """
        return [
            ("ZAJEMI O",  "∅", ["ZAJEMI ∅"]),
            ("REŽI ⊘",   "¬", ["PREVEDI ¬"]),          # CORPUS deluje tu
            ("POKAŽI ∆", "∆", ["PRESLIKAJ ∆", "VSTOP ∂"]),  # CORPUS deluje tu
            ("PREVERI ⊢","⧖", ["PREVERI ⊢"]),
            ("SHRANI ∮", "∮", ["ATLAS ∮", "ODPRI ⟡"]),
        ]
''')


# ============================================================
# 3. comprehension/core/preverba_bridge.py
#    ProcessingPipeline ↔ Preverba most
# ============================================================

write_file(CORE / "preverba_bridge.py", r'''"""
Preverba Bridge — ProcessingPipeline ↔ Preverba
================================================
Ta most povezuje obstoječo ProcessingPipeline + SymbolMapper
arhitekturo z novo Preverba sistem (Faza 5).

Korpus: "Vsaka preslikava ali modul sam sebi testira"
         (Obs11, 320d6f6a)

Obstoječa arhitektura (Faza 3/4):
  - ProcessingPipeline: odpelje statement skozi R-7 module
  - SymbolMapper: preslika besede na R-7 glyphe
  - MODULE_SEMANTICS: semantika vsakega modula
  - Ontobog: recovery engine za padle cikle

Nova plast (Faza 5):
  - Preverba: 5 preizkusov + 10 preizkusov A-J
  - SOMA: telesna preverba
  - DOCTRINARIUM: ∴→∆→⊢→∮ cikel
  - KANON: KANDIDAT→PREVERJEN→KANON

Most:
  ProcessingPipeline.result → Preverba.run_all(result)
  PreverbaResult → DOCTRINARIUM.preveri_vajo()
  SOMA → KANON prehod
"""

from dataclasses import dataclass, field
from typing import Optional, Any
import json


@dataclass
class PipelinePreverbaResult:
    """Združi ProcessingPipeline rezultat s Preverba rezultatom."""
    # Iz ProcessingPipeline
    statement: str = ""
    module_results: dict = field(default_factory=dict)  # {modul: rezultat}
    depth: int = 1
    guards: dict = field(default_factory=dict)

    # Iz Preverba
    preverba_rezultat: str = ""      # PASS / FAIL / BLISK
    ego_flag: bool = False
    rezultati_5: dict = field(default_factory=dict)
    rezultati_aj: dict = field(default_factory=dict)
    kanon_status: str = "KANDIDAT"
    dokaz_nivo: str = ""

    # Iz SOMA
    soma_rezultat: str = ""          # SOMA_PASS / SOMA_FAIL

    # Iz Seriousness
    seriousness: str = "S1"

    # Iz CORPUS (cevovod)
    corpus_faze: list = field(default_factory=list)

    # Integracija
    integriran: bool = False        # ali je šel skozi celoten most


class PreverbaBridge:
    """
    Most med ProcessingPipeline in Preverba sistemom.

    Uporaba:
        from comprehension.core.preverba_bridge import PreverbaBridge
        bridge = PreverbaBridge()

        # Po ProcessingPipeline obdelavi:
        pipeline_result = pipeline.process(statement)
        preverba_result = bridge.integriraj(pipeline_result)
    """

    def __init__(self):
        # Lazy import — ne odpovi dokler ne potrebujemo
        self._preverba = None
        self._soma = None
        self._doctrinarium = None
        self._kanon = None
        self._seriousness = None
        self._corpus = None
        self._aregister = None

    def _ensure_systems(self):
        """Lazy-load vse Faza 5 sisteme."""
        if self._preverba is None:
            from comprehension.core.preverba import Preverba
            from comprehension.core.soma import SomaCheck, SomaResult
            from comprehension.core.doctrinarium import DoctrinariumCikel
            from comprehension.core.kanon_flow import KanonFlow
            from comprehension.core.seriousness import SeriousnessClassifier
            from comprehension.core.corpus_integrator import CorpusIntegrator
            from comprehension.core.aregister_bridge import ARegisterBridge

            self._preverba = Preverba()
            self._soma_cls = SomaCheck
            self._soma_result = SomaResult
            self._doctrinarium = DoctrinariumCikel()
            self._kanon = KanonFlow()
            self._seriousness = SeriousnessClassifier()
            self._corpus = CorpusIntegrator()
            self._aregister = ARegisterBridge()

    def integriraj(self, pipeline_result: dict, soma_input: dict = None,
                   izvorno_ime: str = "", izvorni_operator: str = "") -> PipelinePreverbaResult:
        """
        Integrira ProcessingPipeline rezultat s Preverbo.

        Args:
            pipeline_result: dict iz ProcessingPipeline.process()
            soma_input: dict s soma podatki {dih_prost, mravljinci, napetost_cejust, napetost_ramena}
            izvorno_ime: ime zunanjega sistema (za CORPUS cevovod)
            izvorni_operator: operator zunanjega sistema (za CORPUS cevovod)

        Returns:
            PipelinePreverbaResult
        """
        self._ensure_systems()
        result = PipelinePreverbaResult()

        # 1. Izvleci podatke iz ProcessingPipeline rezultata
        result.statement = pipeline_result.get("statement", "")
        result.module_results = pipeline_result.get("modules", {})
        result.depth = pipeline_result.get("depth", 1)
        result.guards = pipeline_result.get("guards", {})

        # 2. Določi modul iz pipeline rezultata
        modul = self._doloci_modul(pipeline_result)

        # 3. ARegister prepoznavanje
        areg_entry = self._aregister.recognize(result.statement)
        if areg_entry and not modul:
            modul = areg_entry.glyph

        # 4. Zgradi kontekst za Preverbo iz pipeline rezultata
        kontekst = self._gradi_kontekst(pipeline_result, areg_entry)

        # 5. Odpelji Preverbo (5 + 10 preizkusov)
        preverba_r = self._preverba.run_all(modul, result.statement, kontekst)
        result.preverba_rezultat = preverba_r.skupni_rezultat
        result.ego_flag = preverba_r.ego_flag
        result.rezultati_5 = preverba_r.rezultati_5
        result.rezultati_aj = preverba_r.rezultati_aj
        result.kanon_status = preverba_r.kanon_status
        result.dokaz_nivo = preverba_r.dokaz_nivo

        # 6. SOMA
        soma_r = ""
        if soma_input:
            soma = self._soma_cls(
                dih_prost=soma_input.get("dih_prost", True),
                mravljinci=soma_input.get("mravljinci", False),
                napetost_cejust=soma_input.get("napetost_cejust", False),
                napetost_ramena=soma_input.get("napetost_ramena", False),
            )
            soma_r = soma.evaluate()
        result.soma_rezultat = soma_r

        # 7. Seriousness
        serious = self._seriousness.classify(
            preverba_r.rezultati_5, preverba_r.ego_flag, soma_r)
        result.seriousness = serious.nivo

        # 8. DOCTRINARIUM cikel
        doc = self._doctrinarium.dodaj_doktrino(
            modul, result.statement,
            princip=kontekst.get("princip", ""),
            nujnost=kontekst.get("nujnost", ""))
        trn = self._doctrinarium.dodaj_vajo(doc.id, f"Preverba: {result.statement[:60]}")
        self._doctrinarium.preveri_vajo(
            trn.id, preverba_r.skupni_rezultat, soma_r,
            preverba_r.ego_flag, preverba_r.dokaz_nivo)

        # 9. KANON
        kanon_e = self._kanon.dodaj(modul, result.statement)
        if preverba_r.skupni_rezultat == "PASS":
            self._kanon.prehod(kanon_e.id, "preverba_pass")
            if soma_r == "SOMA_PASS":
                self._kanon.prehod(kanon_e.id, "soma_integracija")
                self._doctrinarium.integriraj(
                    f"ASV-{len(self._doctrinarium.assur_valid):04d}",
                    "Integrirano v kanon", zivljeno=True)
        elif preverba_r.skupni_rezultat == "FAIL":
            self._kanon.prehod(kanon_e.id, "preverba_fail")
        else:
            self._kanon.prehod(kanon_e.id, "preverba_blisk")

        # 10. CORPUS cevovod (ce imamo zunanji sistem)
        if izvorno_ime and izvorni_operator:
            corpus_rez = self._corpus.odpelji_cevovod(
                izvorno_ime, izvorni_operator,
                soma_rezultat=soma_r,
                preverba_rezultati=preverba_r.rezultati_5)
            result.corpus_faze = [r.__dict__ for r in corpus_rez]

        result.integriran = True
        return result

    def _doloci_modul(self, pipeline_result: dict) -> str:
        """Doloci R-7 modul iz pipeline rezultata."""
        # Ce pipeline vrne "phase" ali "module"
        modul = pipeline_result.get("phase", "")
        if not modul:
            modul = pipeline_result.get("module", "")
        if not modul and "modules" in pipeline_result:
            # Vzami modul z najvisjo aktivnostjo
            mods = pipeline_result["modules"]
            if mods:
                modul = max(mods.items(), key=lambda x: len(str(x[1])))[0]
        return modul

    def _gradi_kontekst(self, pipeline_result: dict, areg_entry) -> dict:
        """Zgradi kontekst za Preverbo iz pipeline rezultata + ARegister."""
        kontekst = {}
        if areg_entry:
            kontekst["operator"] = areg_entry.glyph
        if "modules" in pipeline_result:
            kontekst["jedro"] = pipeline_result.get("statement", "")
        # Dodaj guard vrednosti kot kontekst
        if "guards" in pipeline_result:
            kontekst["guards"] = pipeline_result["guards"]
        return kontekst

    def to_dict(self, result: PipelinePreverbaResult) -> dict:
        """Serializiraj rezultat za JSON export."""
        return {
            "statement": result.statement,
            "module_results": result.module_results,
            "depth": result.depth,
            "preverba_rezultat": result.preverba_rezultat,
            "ego_flag": result.ego_flag,
            "rezultati_5": result.rezultati_5,
            "rezultati_aj": result.rezultati_aj,
            "kanon_status": result.kanon_status,
            "dokaz_nivo": result.dokaz_nivo,
            "soma_rezultat": result.soma_rezultat,
            "seriousness": result.seriousness,
            "corpus_faze": result.corpus_faze,
            "integriran": result.integriran,
        }
''')


# ============================================================
# 4. comprehension/ui/main_window_v5_integrated.py
#    Integrirani UI z QMessageBox SOMA + ProcessingPipeline
# ============================================================

write_file(UI / "main_window_v5_integrated.py", r'''"""
TAZV Comprehension Machine — main_window_v5_integrated
=======================================================
Integrira:
  - 5-gumbni pipeline (ZAJEMI/REŽI/POKAŽI/PREVERI/SHRANI)
  - ProcessingPipeline + SymbolMapper (obstoječa arhitektura)
  - PreverbaBridge (Faza 5 most)
  - ARegister (apercepcija → operator)
  - CORPUS cevovod (∅→¬→∆→∂→⧖→∮→⟡)
  - SOMA kot QMessageBox.question (ne print!)
  - DOCTRINARIUM + KANON + CADENCE

Korpus: "SOMA_PROMPT spraša: Ali cutis, da drzi?"
         "Telo ni preverjevalec trditve — telo je bitje,
          ki ga test ne sme krsiti." (Obs11, 320d6f6a)

Razlika od main_window_v5.py:
  - Importa ProcessingPipeline + SymbolMapper
  - SOMA je QMessageBox.question, ne checkbox
  - ARegister prepozna uporabnikov vnos
  - CORPUS cevovod prikazan v posebnem tabu
  - PreverbaBridge integrira vse
"""

import sys
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QTextEdit, QLabel, QMessageBox,
    QComboBox, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar,
    QMenu, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QAction

# Project imports — Faza 5
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from comprehension.core.preverba import Preverba, PreverbaResult, TestResult
from comprehension.core.soma import SomaCheck, SomaResult, SOMA_PROMPT_TEXT
from comprehension.core.doctrinarium import DoctrinariumCikel
from comprehension.core.cadence import Cadence
from comprehension.core.kanon_flow import KanonFlow
from comprehension.core.seriousness import SeriousnessClassifier
from comprehension.core.corpus_integrator import CorpusIntegrator, CorpusPhase
from comprehension.core.aregister_bridge import ARegisterBridge
from comprehension.core.preverba_bridge import PreverbaBridge

# Obstoječa arhitektura (Faza 3/4) — z try/except za primere ko manjkajo
try:
    from comprehension.core.processing_pipeline import ProcessingPipeline
    from comprehension.core.symbol_mapper import SymbolMapper
    HAS_PIPELINE = True
except ImportError:
    HAS_PIPELINE = False
    ProcessingPipeline = None
    SymbolMapper = None

try:
    from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
    HAS_SEMANTICS = True
except ImportError:
    HAS_SEMANTICS = False
    MODULE_SEMANTICS = {}
    MODULE_ORDER = ["∅","¬","∆","1","⧖","∮","⟡"]


PIPELINE_BARVE = [
    ("ZAJEMI  O",  "∅",  "#1B2838"),
    ("REZI  ⊘",   "¬",  "#B43A2E"),
    ("POKAZI  ∆", "∆",  "#D6A83A"),
    ("PREVERI  ⊢","⧖", "#D4AF37"),
    ("SHRANI  ∮", "∮",  "#080705"),
]


class TazvMainWindowIntegrated(QMainWindow):
    """
    TAZV v5 — integrirani UI z ProcessingPipeline + Preverba + CORPUS + ARegister.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v5 Integrirani")
        self.setMinimumSize(1100, 750)

        # Faza 5 sistemi
        self.preverba = Preverba()
        self.doctrinarium = DoctrinariumCikel()
        self.cadence = Cadence()
        self.kanon = KanonFlow()
        self.seriousness = SeriousnessClassifier()
        self.corpus = CorpusIntegrator()
        self.aregister = ARegisterBridge()
        self.bridge = PreverbaBridge()

        # Obstoječa arhitektura
        self.pipeline = ProcessingPipeline() if HAS_PIPELINE else None
        self.symbol_mapper = SymbolMapper() if HAS_PIPELINE else None

        # Stanje
        self.current_modul = "⧖"
        self.current_trditev = ""
        self.current_kanon_id = None
        self.last_preverba = None
        self.current_soma = None
        self.last_pipeline_result = None
        self.areg_entry = None

        # DB
        self.db_path = Path(__file__).resolve().parent.parent / "data" / "tazv.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

        # UI
        self._build_ui()
        self._build_menu()
        self._apply_theme()
        self.cadence.zacetek_cikla()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        for p in ["schema.sql", "schema_patch_preverba.sql"]:
            f = self.db_path.parent / p
            if f.exists():
                with open(f, "r", encoding="utf-8") as fh:
                    try:
                        c.executescript(fh.read())
                    except Exception:
                        pass
        conn.commit()
        conn.close()

    # --- UI ---

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.addWidget(self._pipeline())

        self.tabs = QTabWidget()
        self.tabs.addTab(self._tab_zajem(),       "∅ Zajem")
        self.tabs.addTab(self._tab_preverba(),     "⧖ Preverba")
        self.tabs.addTab(self._tab_corpus(),      "∮ CORPUS")
        self.tabs.addTab(self._tab_kanon(),       "∮ Kanon")
        self.tabs.addTab(self._tab_doctrinarium(),"∴ Doctrinarium")
        self.tabs.addTab(self._tab_cadence(),     "∮ Cadence")
        self.tabs.addTab(self._tab_zgodovina(),   "⟡ Zgodovina")
        lay.addWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pripravljen. Zajemi trditev → ∅")

    def _pipeline(self):
        g = QGroupBox("R-7 Pipeline")
        h = QHBoxLayout()
        for besedilo, glyph, barva in PIPELINE_BARVE:
            btn = QPushButton(besedilo)
            fg = "#F3E9D2" if barva in ("#1B2838","#080705") else "#1B2838"
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {barva}; color: {fg};
                    font-size: 14px; font-weight: bold;
                    padding: 12px 24px; border-radius: 6px;
                    border: 2px solid {barva};
                }}
                QPushButton:hover {{ border: 2px solid #F3E9D2; }}
            """)
            akcija = besedilo.split()[0]
            cb = {
                "ZAJEMI": self.act_zajemi, "REZI": self.act_rezi,
                "POKAZI": self.act_pokazi, "PREVERI": self.act_preveri,
                "SHRANI": self.act_shrani,
            }[akcija]
            btn.clicked.connect(cb)
            h.addWidget(btn)
        g.setLayout(h)
        return g

    def _tab_zajem(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∅ ZAJEM — vnesi trditev</b>"))

        self.input_trditev = QTextEdit()
        self.input_trditev.setPlaceholderText("Vnesi trditev za preverbo...")
        v.addWidget(self.input_trditev)

        f = QFormLayout()
        self.combo_modul = QComboBox()
        self.combo_modul.addItems(MODULE_ORDER)
        self.combo_modul.setCurrentText("⧖")
        f.addRow("R-7 modul:", self.combo_modul)

        # ARegister prepoznavanje
        self.lbl_areg = QLabel("ARegister: —")
        f.addRow("Apercepcija:", self.lbl_areg)

        self.input_kontekst = QTextEdit()
        self.input_kontekst.setMaximumHeight(80)
        self.input_kontekst.setPlaceholderText(
            'Kontekst (JSON): {"jedro":"...","agent":"..."}')
        f.addRow("Kontekst:", self.input_kontekst)

        # CORPUS polja (za zunanje sisteme)
        self.input_izvorno_ime = QTextEdit()
        self.input_izvorno_ime.setMaximumHeight(40)
        self.input_izvorno_ime.setPlaceholderText("Izvorno ime sistema (npr. Alkimija) — opcijsko")
        f.addRow("CORPUS ime:", self.input_izvorno_ime)

        self.input_izvorni_op = QTextEdit()
        self.input_izvorni_op.setMaximumHeight(40)
        self.input_izvorni_op.setPlaceholderText("Izvorni operator (npr. nigredo) — opcijsko")
        f.addRow("CORPUS op.:", self.input_izvorni_op)

        v.addLayout(f)

        self.lbl_zajem = QLabel("")
        v.addWidget(self.lbl_zajem)
        v.addStretch()
        return w

    def _tab_preverba(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>⧖ PREVERBA — 5 + 10 preizkusov</b>"))
        self.txt_preverba = QTextEdit()
        self.txt_preverba.setReadOnly(True)
        v.addWidget(self.txt_preverba)
        self.lbl_serious = QLabel("")
        self.lbl_serious.setStyleSheet("font-size: 16px; font-weight: bold;")
        v.addWidget(self.lbl_serious)
        return w

    def _tab_corpus(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ CORPUS — 7-fazni prevajalski cevovod ∅→¬→∆→∂→⧖→∮→⟡</b>"))

        # Mapping 5 gumbov → 7 faz
        mapping = self.corpus.map_5gumbov_v_corpus()
        map_html = "<table border='1' cellpadding='6'><tr><th>UI Gumb</th><th>Glyph</th><th>CORPUS faze</th></tr>"
        for gumb, glyph, faze in mapping:
            map_html += f"<tr><td>{gumb}</td><td>{glyph}</td><td>{', '.join(faze)}</td></tr>"
        map_html += "</table>"
        self.lbl_corpus_map = QLabel(map_html)
        v.addWidget(self.lbl_corpus_map)

        self.txt_corpus = QTextEdit()
        self.txt_corpus.setReadOnly(True)
        v.addWidget(self.txt_corpus)
        return w

    def _tab_kanon(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ KANON — statusni avtomat</b>"))
        self.tbl_kanon = QTableWidget(0, 5)
        self.tbl_kanon.setHorizontalHeaderLabels(["ID","Modul","Trditev","Status","Dokaz"])
        self.tbl_kanon.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        v.addWidget(self.tbl_kanon)
        h = QHBoxLayout()
        b1 = QPushButton("Osvezi"); b1.clicked.connect(self.osvezi_kanon)
        h.addWidget(b1)
        v.addLayout(h)
        return w

    def _tab_doctrinarium(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∴ DOCTRINARIUM — cikel ∴→∆→⊢→∮</b>"))
        self.txt_doc = QTextEdit()
        self.txt_doc.setReadOnly(True)
        v.addWidget(self.txt_doc)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_doc)
        v.addWidget(b)
        return w

    def _tab_cadence(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ CADENCE — mikro/makro kadenco</b>"))
        self.lbl_faza = QLabel("")
        self.lbl_faza.setStyleSheet("font-size: 18px; font-weight: bold;")
        v.addWidget(self.lbl_faza)
        self.txt_cad = QTextEdit()
        self.txt_cad.setReadOnly(True)
        v.addWidget(self.txt_cad)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_cad)
        v.addWidget(b)
        return w

    def _tab_zgodovina(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>⟡ ZGODOVINA — proof_log</b>"))
        self.tbl_zg = QTableWidget(0, 6)
        self.tbl_zg.setHorizontalHeaderLabels(["Cas","Modul","Trditev","Rezultat","SOMA","Kanon"])
        self.tbl_zg.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        v.addWidget(self.tbl_zg)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_zg)
        v.addWidget(b)
        return w

    def _build_menu(self):
        mb = self.menuBar()
        m = mb.addMenu("∂ Globina")
        for n in ["povrsinski","strukturni","ontoloski","absolutni"]:
            a = QAction(n, self)
            a.triggered.connect(lambda _,x=n: self.status.showMessage(f"∂ Globina: {x}"))
            m.addAction(a)

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1B2838; }
            QGroupBox { color: #F3E9D2; border: 1px solid #D6A83A; border-radius: 4px; margin-top: 8px; padding-top: 12px; }
            QGroupBox::title { color: #D6A83A; subcontrol-origin: margin; left: 10px; }
            QLabel { color: #F3E9D2; }
            QTextEdit { background-color: #0F1A26; color: #F3E9D2; border: 1px solid #D6A83A; }
            QComboBox { background-color: #0F1A26; color: #F3E9D2; border: 1px solid #D6A83A; }
            QTableWidget { background-color: #0F1A26; color: #F3E9D2; gridline-color: #D6A83A; }
            QHeaderView::section { background-color: #1B2838; color: #D6A83A; }
            QTabWidget::pane { border: 1px solid #D6A83A; }
            QTabBar::tab { background-color: #1B2838; color: #F3E9D2; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #D6A83A; color: #1B2838; }
            QStatusBar { background-color: #080705; color: #D6A83A; }
            QMenu { background-color: #1B2838; color: #F3E9D2; }
        """)

    # --- Pipeline akcije ---

    def _get_kontekst(self):
        t = self.input_kontekst.toPlainText().strip()
        if not t: return {}
        try: return json.loads(t)
        except: return {"_raw": t}

    def act_zajemi(self):
        """∅ ZAJEMI — zajemi trditev + ARegister prepoznavanje."""
        self.current_trditev = self.input_trditev.toPlainText().strip()
        if not self.current_trditev:
            QMessageBox.warning(self, "∅", "Trditev je prazna.")
            return

        # ARegister prepoznavanje (iz korpusa)
        self.areg_entry = self.aregister.recognize(self.current_trditev)
        if self.areg_entry:
            self.lbl_areg.setText(
                f"<b>ARegister:</b> {self.areg_entry.glyph} — {self.areg_entry.perception[:60]}")
            # Ce ARegister prepozna modul, ga ponudi
            self.combo_modul.setCurrentText(self.areg_entry.glyph)
            self.current_modul = self.areg_entry.glyph
        else:
            self.lbl_areg.setText("ARegister: ni prepoznan — rocni izbor")
            self.current_modul = self.combo_modul.currentText()

        kont = self._get_kontekst()

        # ProcessingPipeline (ce obstaja)
        if self.pipeline:
            try:
                self.last_pipeline_result = self.pipeline.process(self.current_trditev)
            except Exception:
                self.last_pipeline_result = {"statement": self.current_trditev}

        # KANON dodaj kot KANDIDAT
        ke = self.kanon.dodaj(self.current_modul, self.current_trditev)
        self.current_kanon_id = ke.id
        self.cadence.log_mikro(self.current_modul, "ZAJEMI", "OK")

        # DOCTRINARIUM dodaj doktrino
        doc = self.doctrinarium.dodaj_doktrino(
            self.current_modul, self.current_trditev,
            princip=kont.get("princip",""), nujnost=kont.get("nujnost",""))

        self.lbl_zajem.setText(
            f"<b>✓ Zajeto:</b> modul={self.current_modul} | "
            f"kanon={ke.id} | doc={doc.id}")
        self.status.showMessage(f"∅ Zajeto: {ke.id} — ARegister: {self.areg_entry.glyph if self.areg_entry else 'rocno'} — pripravljen za REZI")

    def act_rezi(self):
        """¬ REZI — CORPUS PREVEDI: reže izvorni operator na korenski glif."""
        if not self.current_trditev:
            QMessageBox.warning(self, "¬", "Najprej zajemi (∅).")
            return

        # CORPUS PREVEDI: ce imamo izvorno ime + operator
        izv_ime = self.input_izvorno_ime.toPlainText().strip()
        izv_op = self.input_izvorni_op.toPlainText().strip()

        if izv_ime and izv_op:
            tabela = self.corpus.najdi_preslikavo(izv_ime, izv_op)
            if tabela:
                self.status.showMessage(
                    f"¬ REZI: {izv_op} → {tabela.korenski_glif} ({tabela.preverba} kot)")
            else:
                self.status.showMessage(f"¬ REZI: preslikava za {izv_ime}:{izv_op} ni najdena")
        else:
            # Brez CORPUS — rocni rez
            jedro = self.current_trditev.split(".")[0].strip() or self.current_trditev[:80]
            self.status.showMessage(f"¬ REZI: jedro izlusceno ({len(jedro)} znakov)")

        self.cadence.log_mikro(self.current_modul, "REZI", "OK")

    def act_pokazi(self):
        """∆ POKAZI — CORPUS PRESLIKAJ + VSTOP."""
        if not self.current_trditev:
            QMessageBox.warning(self, "∆", "Najprej zajemi (∅).")
            return

        izv_ime = self.input_izvorno_ime.toPlainText().strip()
        izv_op = self.input_izvorni_op.toPlainText().strip()

        html = "<div style='color:#F3E9D2; font-family: monospace;'>"
        html += f"<h3>∆ POKAZI / PRESLIKAJ</h3>"
        html += f"<p><b>Trditev:</b> {self.current_trditev}</p>"
        html += f"<p><b>Modul:</b> {self.current_modul}</p>"

        if self.areg_entry:
            html += f"<p><b>ARegister:</b> {self.areg_entry.glyph} — {self.areg_entry.perception}</p>"
            html += f"<p><b>Vprasanje:</b> <i>{self.areg_entry.inquiry}</i></p>"

        if izv_ime and izv_op:
            tabela = self.corpus.najdi_preslikavo(izv_ime, izv_op)
            if tabela:
                html += f"<p><b>CORPUS preslikava:</b> {izv_op} → {tabela.korenski_glif}</p>"
                html += f"<p><b>Modul:</b> {tabela.modul} | <b>Kot:</b> {tabela.preverba}</p>"
                html += f"<p><b>VSTOP ∂:</b> preslikava postane operativna v modulu {tabela.modul}</p>"
            else:
                html += f"<p style='color:#FF9800'>Preslikava ni najdena — dodaj v prevajalsko tabelo</p>"

        html += "<p><i>Pripravljen za PREVERI ⊢</i></p>"
        html += "</div>"

        self.txt_preverba.setHtml(html)
        self.cadence.log_mikro(self.current_modul, "POKAZI", "OK")
        self.tabs.setCurrentIndex(1)
        self.status.showMessage("∆ Pokazano — pripravljen za PREVERI ⊢")

    def act_preveri(self):
        """⧖ PREVERI — 5 preizkusov + 10 preizkusov A-J + SOMA (QMessageBox)."""
        if not self.current_trditev:
            QMessageBox.warning(self, "⧖", "Najprej zajemi (∅).")
            return

        kont = self._get_kontekst()

        # Odpelji preverbo
        r = self.preverba.run_all(self.current_modul, self.current_trditev, kont)
        self.last_preverba = r

        # Seriousness
        s = self.seriousness.classify(r.rezultati_5, r.ego_flag,
            self.current_soma.evaluate() if self.current_soma else "")

        # Izpisi rezultat
        self.txt_preverba.setHtml(self._fmt_result(r, s))
        sc = {"S1":"#4CAF50","S2":"#FF9800","S3":"#F44336","S4":"#8B0000"}
        self.lbl_serious.setText(
            f"<span style='color:{sc.get(s.nivo)}'>"
            f"{s.nivo} — {s.opis} | {s.akcija}</span>")

        # KANON prehod
        if self.current_kanon_id:
            akc = {"PASS":"preverba_pass","FAIL":"preverba_fail","BLISK":"preverba_blisk"}
            try:
                self.kanon.prehod(self.current_kanon_id, akc.get(r.skupni_rezultat, "preverba_fail"))
            except Exception:
                pass

        # DOCTRINARIUM
        doc_id = f"DOC-{len(self.doctrinarium.doctrinarium):04d}"
        trn = self.doctrinarium.dodaj_vajo(doc_id, f"Preverba: {self.current_trditev[:60]}")
        self.doctrinarium.preveri_vajo(trn.id, r.skupni_rezultat, "", r.ego_flag, r.dokaz_nivo)

        self._log_proof(r, s)
        self.cadence.log_mikro(self.current_modul, "PREVERI", r.skupni_rezultat)

        # SOMA preverba kot QMessageBox.question
        if r.skupni_rezultat == "PASS":
            self._soma_qmessagebox()
        else:
            self.status.showMessage(f"⧖ Preverba {r.skupni_rezultat} — {s.nivo}")

    def _soma_qmessagebox(self):
        """
        SOMA preverba kot QMessageBox.question.
        Korpus: "Telo ni preverjevalec trditve — telo je bitje,
                 ki ga test ne sme krsiti." (Obs11, 320d6f6a)
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("⧖ Preverba Soma")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Preverba soma")
        msg.setInformativeText(
            "Telo ni preverjevalec trditve — telo je bitje, ki ga test ne sme krsiti.\n\n"
            "Ali cutis, da drzi?\n\n"
            "1. Ali dih ostaja prost?\n"
            "2. Ali cutis mravljince (napetost, kracenje)?\n"
            "3. Ali je napetost v celjusti ali ramenih?\n\n"
            "Ce karkoli je DA (krsitev), test je prevec agresiven.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("DA — telo drzi")
        msg.button(QMessageBox.StandardButton.No).setText("NE — telo protestira")

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            # SOMA_PASS
            self.current_soma = SomaCheck(dih_prost=True, mravljinci=False,
                                           napetost_cejust=False, napetost_ramena=False)
            self.status.showMessage("SOMA PASS — pripravljen za SHRANI ∮")
        else:
            # SOMA_FAIL — telo protestira
            self.current_soma = SomaCheck(dih_prost=False, mravljinci=True,
                                           napetost_cejust=True, napetost_ramena=False)
            self.status.showMessage("SOMA FAIL — test krsi telo")

        self.cadence.log_mikro(self.current_modul, "SOMA", self.current_soma.evaluate())

    def act_shrani(self):
        """∮ SHRANI — ATLAS + ODPRI (KANON integracija)."""
        if not self.current_kanon_id:
            QMessageBox.warning(self, "∮", "Najprej zajemi in preveri.")
            return
        if not self.last_preverba:
            QMessageBox.warning(self, "∮", "Najprej odpelji preverbo (⊢).")
            return

        r = self.last_preverba
        soma_ok = self.current_soma and self.current_soma.evaluate() == "SOMA_PASS"

        if r.skupni_rezultat == "PASS" and soma_ok:
            # KANON prehod
            self.kanon.prehod(self.current_kanon_id, "soma_integracija")
            asv_id = f"ASV-{len(self.doctrinarium.assur_valid):04d}"
            self.doctrinarium.integriraj(asv_id, "Integrirano v kanon", zivljeno=True)
            self.cadence.log_mikro(self.current_modul, "SHRANI", "KANON")

            # CORPUS cevovod (ce imamo zunanji sistem)
            izv_ime = self.input_izvorno_ime.toPlainText().strip()
            izv_op = self.input_izvorni_op.toPlainText().strip()
            if izv_ime and izv_op:
                corpus_rez = self.corpus.odpelji_cevovod(
                    izv_ime, izv_op,
                    soma_rezultat="SOMA_PASS",
                    preverba_rezultati=r.rezultati_5)
                self._prikazi_corpus(corpus_rez)

            self.status.showMessage(f"∮ Shranjeno v KANON: {self.current_kanon_id}")
            QMessageBox.information(self, "∮ Kanon",
                f"Trditev shranjena v KANON.\n\n"
                f"ID: {self.current_kanon_id}\n"
                f"Dokaz: {r.dokaz_nivo}\nSOMA: PASS")
        elif r.skupni_rezultat == "PASS" and not soma_ok:
            QMessageBox.warning(self, "∮", "SOMA ni sla skozi.\n"
                "Telo mora potrditi pred shranitvijo v KANON.")
        else:
            QMessageBox.warning(self, "∮", f"Preverba ni PASS ({r.skupni_rezultat}).\n"
                "Shranjeno kot MEGLA.")
        self.osvezi_kanon()

    # --- Format / prikaz ---

    def _fmt_result(self, r, s):
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        c = {"PASS":"#4CAF50","FAIL":"#F44336","BLISK":"#FF9800"}
        h += f"<h2 style='color:{c.get(r.skupni_rezultat)}'>⧖ PREVERBA: {r.skupni_rezultat}</h2>"
        if r.dokaz_nivo:
            h += f"<p><b>Dokaz:</b> {r.dokaz_nivo}</p>"

        h += "<h3>5 PREIZKUSOV</h3><table border='1' cellpadding='6'>"
        h += "<tr><th>Preizkus</th><th>Glyph</th><th>Rezultat</th></tr>"
        gl = {"cas":"⧖","drugi":"⟡","tretji":"∴","nujno":"∅","ego":"⊘"}
        for n, v in r.rezultati_5.items():
            cc = c.get(v, "#F3E9D2")
            h += f"<tr><td>{n}</td><td>{gl.get(n,'?')}</td><td style='color:{cc}'>{v}</td></tr>"
        h += "</table>"

        h += "<h3>10 PREIZKUSOV A-J</h3><table border='1' cellpadding='6'>"
        h += "<tr><th>Ozn</th><th>Ime</th><th>R-7</th><th>Rezultat</th></tr>"
        ajm = {"A_KERNEL":("A","∅"),"B_OPERATOR":("B","¬"),"C_AGENT":("C","∆"),
               "D_MICRO_AKCIJA":("D","1"),"E_SOMA":("E","⧖"),"F_CAS_POT":("F","⧖"),
               "G_DOKAZ":("G","∮"),"H_UI":("H","⟡"),"I_SKUPNOST_SUM":("I","⟡"),
               "J_KANON_ARHIV":("J","∮")}
        for n, v in r.rezultati_aj.items():
            cc = c.get(v, "#F3E9D2")
            oz, gy = ajm.get(n, ("?","?"))
            h += f"<tr><td>{oz}</td><td>{n.split('_',1)[1] if '_' in n else n}</td><td>{gy}</td><td style='color:{cc}'>{v}</td></tr>"
        h += "</table>"

        h += f"<p><b>Suma:</b> {r.suma_opis}</p>"
        h += f"<p><b>Kanon:</b> {r.kanon_status}</p>"
        h += f"<p><b>Resnost:</b> {s.nivo} — {s.opis} | {s.akcija}</p>"
        if r.ego_flag:
            h += "<p style='color:#F44336'><b>⚠ EGO FLAG:</b> volja posreduje — zamrzni modul</p>"
        h += "</div>"
        return h

    def _prikazi_corpus(self, rezultati):
        """Prikaže CORPUS cevovod rezultate."""
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += "<h3>∮ CORPUS cevovod — 7 faz</h3>"
        h += "<table border='1' cellpadding='6'>"
        h += "<tr><th>Faza</th><th>Glyph</th><th>Rezultat</th><th>Opis</th></tr>"
        for r in rezultati:
            c = "#4CAF50" if r.rezultat == "PASS" else "#F44336" if "FAIL" in r.rezultat else "#FF9800"
            h += f"<tr><td>{r.faza}</td><td>{r.glif}</td><td style='color:{c}'>{r.rezultat}</td><td>{r.opis[:80]}</td></tr>"
        h += "</table></div>"
        self.txt_corpus.setHtml(h)

    def osvezi_kanon(self):
        self.tbl_kanon.setRowCount(0)
        bmap = {"KANON":QColor("#D4AF37"),"PREVERJEN":QColor("#D6A83A"),
                "KANDIDAT":QColor("#F3E9D2"),"MEGLA":QColor("#666"),"ARHIV":QColor("#333")}
        for e in self.kanon.entries:
            row = self.tbl_kanon.rowCount()
            self.tbl_kanon.insertRow(row)
            self.tbl_kanon.setItem(row, 0, QTableWidgetItem(e.id))
            self.tbl_kanon.setItem(row, 1, QTableWidgetItem(e.modul))
            self.tbl_kanon.setItem(row, 2, QTableWidgetItem(e.trditev[:80]))
            it = QTableWidgetItem(e.status)
            it.setForeground(bmap.get(e.status, QColor("#F3E9D2")))
            self.tbl_kanon.setItem(row, 3, it)
            self.tbl_kanon.setItem(row, 4, QTableWidgetItem(e.dokaz_nivo))

    def osvezi_doc(self):
        d = self.doctrinarium
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += f"<h3>∴ DOCTRINARIUM ({len(d.doctrinarium)})</h3>"
        for doc in d.doctrinarium[-10:]:
            st = d.cikel_status(doc.id)
            h += f"<p><b>{doc.id}</b> [{doc.modul}] {doc.trditev[:60]}<br>{st.get('status','?')} — {st.get('napredek','?')}</p>"
        h += f"<h3>∆ TRAINARIUM ({len(d.trainarium)})</h3>"
        for t in d.trainarium[-10:]:
            h += f"<p><b>{t.id}</b> | {t.vaja[:60]} | zadnji: {t.zadnji_rezultat}</p>"
        h += f"<h3>⊢ ASSUR-VALID ({len(d.assur_valid)})</h3>"
        for a in d.assur_valid[-10:]:
            h += f"<p><b>{a.id}</b> | {a.preverba_rezultat} | dokaz: {a.dokaz_nivo}</p>"
        h += f"<h3>∮ MEMORI ({len(d.memori)})</h3>"
        for m in d.memori[-10:]:
            h += f"<p><b>{m.id}</b> | zivljeno: {m.zivljeno} | {m.integracija[:60]}</p>"
        h += "</div>"
        self.txt_doc.setHtml(h)

    def osvezi_cad(self):
        g, i, dn = self.cadence.dnevna_faza()
        self.lbl_faza.setText(f"DAN {dn}/7 | {g} {i.upper()}")
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += f"<h3>∮ MAKRO — P-7d cikel</h3>"
        if self.cadence.makro_cikli:
            c = self.cadence.makro_cikli[-1]
            h += f"<p><b>{c.cikel_id}</b> | dan {c.dan}/7 | {c.faza_glyph} {c.faza_ime}</p>"
            h += f"<p>{c.preverbe_pass} PASS / {c.preverbe_fail} FAIL | {c.integracije} integracij</p>"
        h += f"<h3>∂ MIKRO ({len(self.cadence.mikro_log)})</h3>"
        for m in self.cadence.mikro_log[-20:]:
            h += f"<p>{m.timestamp[:19]} | {m.modul} | {m.operacija} | {m.rezultat}</p>"
        h += "</div>"
        self.txt_cad.setHtml(h)

    def osvezi_zg(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        try:
            c.execute("SELECT timestamp,modul,statement,result,soma,kanon_status "
                      "FROM proof_log ORDER BY timestamp DESC LIMIT 100")
            rows = c.fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        self.tbl_zg.setRowCount(0)
        for rd in rows:
            row = self.tbl_zg.rowCount()
            self.tbl_zg.insertRow(row)
            for col, val in enumerate(rd):
                self.tbl_zg.setItem(row, col, QTableWidgetItem(str(val or "")))

    def _log_proof(self, r, s):
        tid = hashlib.md5(
            f"{self.current_modul}:{self.current_trditev}:{datetime.now().isoformat()}"
            .encode()).hexdigest()[:12]
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE INTO proof_log
            (test_id,modul,statement,phase,result,ego_flag,soma,dokaz,seriousness,
             kanon_status,rezultati_5,rezultati_aj)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (tid, self.current_modul, self.current_trditev, self.current_modul,
             r.skupni_rezultat, int(r.ego_flag),
             self.current_soma.evaluate() if self.current_soma else "",
             r.dokaz_nivo, s.nivo, r.kanon_status,
             json.dumps(r.rezultati_5), json.dumps(r.rezultati_aj)))
        conn.commit()
        conn.close()


def main():
    app = QApplication(sys.argv)
    win = TazvMainWindowIntegrated()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
''')


# ============================================================
# BOOTSTRAP RUNNER
# ============================================================

def main():
    print("=" * 60)
    print("TAZV Faza 5 — Integracija C3 <-> B2")
    print("=" * 60)
    print()
    print("Generiram integracijske datoteke:")
    print()
    print("  1. comprehension/core/aregister_bridge.py")
    print("     ARegister: user expression → perception → operator (glyph)")
    print("     10 korpus-validiranih ARegister vnosov (∅¬∆1⧖∮⟡∂∫∴)")
    print()
    print("  2. comprehension/core/corpus_integrator.py")
    print("     CORPUS 7-fazni cevovod: ∅→¬→∆→∂→⧖→∮→⟡")
    print("     22 ze preslikanih sistemov (Alkimija, Kibalion, Cakre, Wu Xing)")
    print("     5-gumbni → 7-fazni mapping")
    print()
    print("  3. comprehension/core/preverba_bridge.py")
    print("     ProcessingPipeline ↔ Preverba most")
    print("     Integrira: pipeline result → preverba → soma → kanon → doctrinarium")
    print()
    print("  4. comprehension/ui/main_window_v5_integrated.py")
    print("     Integrirani UI z:")
    print("       - ProcessingPipeline + SymbolMapper (obstoječa arhitektura)")
    print("       - ARegister prepoznavanje ob zajemu")
    print("       - CORPUS cevovod tab (∅→¬→∆→∂→⧖→∮→⟡)")
    print("       - SOMA kot QMessageBox.question (ne print/checkbox!)")
    print("       - DOCTRINARIUM + KANON + CADENCE")
    print()
    print("KORPUS MAPPING (5 gombov → 7 CORPUS faz):")
    print("  ZAJEMI O  → ZAJEMI ∅")
    print("  REZI ⊘   → PREVEDI ¬          ← CORPUS deluje tu")
    print("  POKAZI ∆ → PRESLIKAJ ∆ + VSTOP ∂  ← CORPUS deluje tu")
    print("  PREVERI ⊢→ PREVERI ⊢")
    print("  SHRANI ∮ → ATLAS ∮ + ODPRI ⟡")
    print()
    print("Naslednji koraki:")
    print("  1. python tazv_phase5_integration_bootstrap.py")
    print("  2. Backup: copy main_window_v5.py main_window_v5_backup.py")
    print("  3. Posodobi main.py:")
    print("     from comprehension.ui.main_window_v5_integrated import TazvMainWindowIntegrated")
    print("  4. python main.py")
    print("  5. Preveri:")
    print("     - ARegister prepozna vnos ob zajemu")
    print("     - CORPUS tab prikazuje 7-fazni cevovod")
    print("     - SOMA je QMessageBox.question (ne checkbox)")
    print("     - ProcessingPipeline integriran ce obstaja")
    print("=" * 60)


if __name__ == "__main__":
    main()