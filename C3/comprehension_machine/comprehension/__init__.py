"""
TAZV Comprehension Machine — Main Package
===========================================

This package implements the TAZV Comprehension Layer based on:
  - SO-OBSTAJANJE Protocol (P1-P7)
  - ANTINOM OPERATOR Protocol (A0-A6)
  - R-7 phase system (∅ → ¬ → ∆ → ⊢ → ⧖ → ∮ → ⟡)

Core module: comprehension.core
  - decomposer.py: Decomposes statements into RelationEvents
  - graph_store.py: RelationField with Resonances
  - contention_mapper.py: Reveals contention (P2)
  - transformation_tracer.py: Traces DOKAZ (P6/P7)
  - self_protocol.py: Model's own operating protocol

Bridge modules:
  - aregister_bridge.py: ARegister word→glyph mapping
  - corpus_integrator.py: 7-phase R-7 pipeline
  - preverba_bridge.py: Pipeline→Preverba integration

The comprehension layer implements:
  "Word is not a node on a line. Word is a relation-event with:
    - Internal division (divider/divided)
    - Antinom (counter-statement, always already present)
    - Resistance field (what it pushes against)
    - Co-existing phases (so-obstajanje)"

Usage:
    from comprehension.core import run_comprehension_layer
    result = run_comprehension_layer("The word is no")

    # Or use individual components:
    from comprehension.core.decomposer import decompose_statement
    events = decompose_statement("The word is no")

    from comprehension.core.graph_store import RelationField
    field = RelationField()
    field.build_from_events(events)

    from comprehension.core.contention_mapper import ContentionMapper
    mapper = ContentionMapper(field)
    report = mapper.reveal()

    from comprehension.core.transformation_tracer import TransformationTracer
    tracer = TransformationTracer(field)
    dokaz = tracer.trace_statement("The word is no")
"""

# Re-export everything from core
from .core import (
    # Decomposer
    decompose_statement,
    get_symbol_sequence,
    get_antinom_sequence,
    get_mapped_ratio,
    RelationEvent,
    DECOMPOSITION_TABLE,
    SLOVENIAN_MAP,
    SYMBOL_PHASE,
    # Graph Store
    RelationField,
    Resonance,
    ContentionMark,
    RelationType,
    Severity,
    RELATION_TYPE_LABELS,
    SYMBOL_OPPOSITIONS,
    # Contention Mapper
    ContentionMapper,
    ContentionReport,
    PHASE_TENSIONS,
    # Transformation Tracer
    TransformationTracer,
    DOKAZ,
    ResonanceStep,
    JEWIK_AXIOMS,
    RESONANCE_OPERATORS,
    # Bridges
    ARegisterBridge,
    ARegisterEntry,
    AREGISTER_DATA,
    CorpusIntegrator,
    CorpusPhase,
    PreverbaKot,
    PrevajalskaTabela,
    CorpusResult,
    PreverbaBridge,
    PipelinePreverbaResult,
    # Gnosis Bridge
    GnosisBridge,
    YggdrasilLevel,
    YggdrasilState,
    create_api_router,
    ZODIAC_SIGNS,
    ELEMENT_MODIFIERS,
    MODALITY_MODIFIERS,
    # Main integration function
    run_comprehension_layer,
)

__all__ = [
    'decompose_statement',
    'get_symbol_sequence',
    'get_antinom_sequence',
    'get_mapped_ratio',
    'RelationEvent',
    'DECOMPOSITION_TABLE',
    'SLOVENIAN_MAP',
    'SYMBOL_PHASE',
    'RelationField',
    'Resonance',
    'ContentionMark',
    'RelationType',
    'Severity',
    'RELATION_TYPE_LABELS',
    'SYMBOL_OPPOSITIONS',
    'ContentionMapper',
    'ContentionReport',
    'PHASE_TENSIONS',
    'TransformationTracer',
    'DOKAZ',
    'ResonanceStep',
    'JEWIK_AXIOMS',
    'RESONANCE_OPERATORS',
    'ARegisterBridge',
    'ARegisterEntry',
    'AREGISTER_DATA',
    'CorpusIntegrator',
    'CorpusPhase',
    'PreverbaKot',
    'PrevajalskaTabela',
    'CorpusResult',
    'PreverbaBridge',
    'PipelinePreverbaResult',
    # Gnosis Bridge
    'GnosisBridge',
    'YggdrasilLevel',
    'YggdrasilState',
    'create_api_router',
    'ZODIAC_SIGNS',
    'ELEMENT_MODIFIERS',
    'MODALITY_MODIFIERS',
    'run_comprehension_layer',
]
