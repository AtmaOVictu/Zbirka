"""
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
            from comprehension.core.soma import SomaCheck
            from comprehension.core.doctrinarium import DoctrinariumCikel
            from comprehension.core.kanon_flow import KanonFlow
            from comprehension.core.seriousness import SeriousnessClassifier
            from comprehension.core.corpus_integrator import CorpusIntegrator
            from comprehension.core.aregister_bridge import ARegisterBridge

            self._preverba = Preverba()
            self._soma_cls = SomaCheck
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
