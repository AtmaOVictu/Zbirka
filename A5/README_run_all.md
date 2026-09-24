# run_all.sh — JEWIK one-click
**Kaj nardi:** normalizira LUFS (TP zaščita), požene auto-merge grafe, zapakira rezultate.

## Uporaba
```bash
cd "$(dirname "$0")"
chmod +x run_all.sh
./run_all.sh
```

### Opcije (prek okolja)
```bash
TARGETS="-14 -16 -23" TRUEPEAK="--tp8 --limiter" GLOB="🜂_AUDIOMANDALA_*.wav" ./run_all.sh
```

**Izhod:** ZIP paket `JEWIK_RUN_ALL_*.zip` + mapa z artefakti.
— 2025-08-14 11:44:26
