"""
Comprehension Machine Core Module
ONTOMATEMATIKA Evolution Engine
"""

from evolution_ledger import (
    EvolutionLedger,
    SystemState,
    UpgradeEvent,
    seed_first_evolution,
    DEFAULT_LEDGER_DIR,
)
from guard import Guard, GuardResult, GuardStatus
from dokaz import DokazTrace, DokazCreator
from upgrade_protocol import evolution_valid, classify_change

__all__ = [
    'EvolutionLedger',
    'SystemState',
    'UpgradeEvent',
    'seed_first_evolution',
    'DEFAULT_LEDGER_DIR',
    'Guard',
    'GuardResult',
    'GuardStatus',
    'DokazTrace',
    'DokazCreator',
    'evolution_valid',
    'classify_change',
]
