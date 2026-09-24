# Development Roadmap

## Phase 0 - Foundation DONE
json_safe, module_adapters, processing_pipeline, symbol_mapper, schema, database, error_handler, profiler

## Phase 1 - Core Windows (NEXT)
1. ui/main_window.py - menu, launcher, R-7 progress, status bar
2. ui/module_window.py - base window: input -> process -> results
3. ui/r7_progress.py - 7-segment status widget
4. Wire BIOS + STATE first, then add remaining 5
5. Pipeline runs in QThread - UI stays responsive

## Phase 2 - Inter-Window
Qt Signals/Slots chain, QDockWidget, saveState/restoreState

## Phase 3 - Theming + Export
3 themes, JSON+TXT+HTML export

## Phase 4 - Full Data Layer
History search UI, CSV export, settings management

## Phase 5 - Deployment
PyInstaller --onedir, Windows installer

## Deferred
Body integration (EMG/HRV), custom R-7 designer, per-symbol theming, plugins
