"""
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
