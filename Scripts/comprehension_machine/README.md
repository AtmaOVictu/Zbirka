# TAZV Comprehension Machine

Desktop app implementing the R-7 ontological processing pipeline.

## Quick Start

    cd comprehension_machine
    pip install PyQt6
    python -m comprehension.core.processing_pipeline
    python -m comprehension.core.symbol_mapper
    pytest

## Structure

    comprehension_machine/
      comprehension/
        core/        R-7 pipeline, adapters, symbol mapper
        modules/     Module implementations (Phase 1)
        ui/          PyQt6 windows (Phase 1)
        data/        SQLite + exporters
        utils/       Error handler, profiler
      tests/
      docs/
      data/          Runtime: sessions.db
