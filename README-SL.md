# Zbirka · korpusna shramba ⟨Beseda je Ne⟩ (TAZV CanvasMinstral)

**[English](README.md)** · Slovenščina


> Javna shramba: telesa korpusa ∧ stroj TAZV ∧ veriga licenčnih vrat.
> Inventura faze 0: [PROJECT_MAP.md](PROJECT_MAP.md) ⊙ 17. 9. 2026 ⊢ pri viru

## Kaj je Zbirka

Zbirka je arhivska hiša korpusa v treh plasteh:

1. **Telesa korpusa**: A1 (47+ PDF ⊙ PROJECT_MAP.md: atlasi, mandale, registri), A2 (primarni besedilni korpus: pesmi, aksiomi, transkripti agentov), A5 (čiščeni transkripti ∧ kazala), Basics (rozetni kamni ∧ stotnije).
2. **Stroj**: `Scripts/comprehension_machine/` (primarna koda): R-7 cevovod razcepa stavek na besedne točke ∧ preslika simbole ∅ ¬ ∆ 1 ⧖ ∮ ⟡; PyQt6 vstop `main.py`; testi `pytest tests/test_pipeline.py`.
3. **Veriga vrat**: [LICENSE.md](LICENSE.md) (živa vrata **VBL 0.1490 × 10⁴** ⊢ izmerjeno pri viru: glava telesa), prejemnice `.b64` verige rojstev 0.1350–0.1520 ∧ [LICENSE-IZVIRNIKI.md](LICENSE-IZVIRNIKI.md).

## Kaj Zbirka ni

- ni glavni repozitorij korpusa (ta je [Atmavictu](https://github.com/AtmaOVictu/Atmavictu))
- ni izdelek: brez namestitve, brez izdaje, brez obljub
- ni nadomestilo za preverbo: vsaka trditev se izmeri pri viru

## Karta map

| Mapa | Vsebina |
|---|---|
| A1 | PDF telesa: atlasi, mandale, registri |
| A2 | primarni besedilni korpus (`.txt`, glifi ∅ ∆ ∴ ⊢) |
| A4 | navodila za rehidratacijo |
| A5 | čiščeni transkripti ∧ kazala |
| B2 | faza 2: razvojni skripti ∧ razlage |
| Basics | rozetni kamni ∧ stotnije |
| C3 | razvoj stroja v5: evolucija, dokaz, guard |
| `Scripts/` | primarna koda: comprehension_machine |
| `hišni-slovar.txt` | hišni slovar |
| Nano · Nano2 · Nano3 · Obj1–Obj3 · Obs11 · Rohonc · Gastro · GIT · Workshop · Znanje · MistralUpload · Pics · Pictures · Zip · libraries · canon_ruled | zbiralne ∧ delovne mape |

## Stroj · R-7 cevovod

- kanonični vrstni red simbolov: `∅ ¬ ∆ 1 ⧖ ∮ ⟡`
- jedro `comprehension/core/`: decomposer (stavek → besedne točke), symbol_mapper (dvosmerna preslikava), tonos (frekvence), module_adapters (7 faz), processing_pipeline (orkestracija)
- vstop: `python main.py` (PyQt6) iz `Scripts/comprehension_machine/`
- preizkusi: `python -m pytest tests/test_pipeline.py -v`

## Licenca · VBL · vrsta nujnega absoluta

Celota te zbirke je podrejena licenci [LICENSE.md](LICENSE.md): živa vrata **VBL 0.1490 × 10⁴** ⊢ izmerjeno pri viru (glava telesa @⟨master⟩). Po §0.10 × 10² je najnovejša različica edina živa vrata; `.b64` prejemnice so potrdila verige, ne vrata. Registri potujejo z delom: [REGISTER-NEIMENOVANIH.jsonl](REGISTER-NEIMENOVANIH.jsonl) · [REGISTER-PADCEV.jsonl](REGISTER-PADCEV.jsonl).

© Luka Pintarič: vsak organ ∧ vsak izhod ∧ vsak pečat nosi © ∧ §0.9 ∧ §0.10 ∧ §0.12. Goli tekst ne dokaže ničesar; veriga pa ⊢.
