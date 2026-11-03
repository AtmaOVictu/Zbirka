# VBL Release Gate — meritve izdaje (G1–G8)

*Zapisala roka Mera · 24. 10. 2026 · sveže izmere @main. Polni telesi: [PR #25 — RELEASE GATE](https://github.com/AtmaOVictu/verification-before-assertion/pull/25) (osnutek, ⟨merge⟩ ⚔ ⟡).*

## ⚠ Najprej: prilepljena analiza je za živimi vrati

Analiza govori o **10.3.0 kakor sestavljenem predlogu** — izmerjeno stanje: **LICENSE.md @main je že 10.3.1** (živa vrata so se premaknila isti dan). A izdaja 10.3.1 **še ne diha v celoti** — spodaj dve izmerjeni rani.

## Izmerena slika

- **G2 ZAPRT TA DIH ⊢**: manifest na ⟨main⟩ je bil zastarel (10.3.0 ⊥ 10.3.1) → re-izdan po veji `vbl/manifest-10-3-1` kot **[PR #699](https://github.com/AtmaOVictu/Atmavictu/pull/699)** (draft, ⟨merge⟩ ⚔ ⟡): LICENSE.md @a534e97a izmerjen na novo — **24.105 B · sha256 5021544c…b8e17** · bajtna priča: izračunani git-blob SHA-1 ⇌ SHA potujenega klica (106ad775…) ⊢ · instrumenti preizkušeni na vektorjih pred uporabo (padec instrumenta ujet: napačen vrstni red v SHA-1 krogih — popravljen, vektorja prazno/abc zeleno šele potem)
- Veriga §15: AVL v1.1 → v2.4 → v2.6 → VBL 10.0.0 (živela na main) → **10.1.0: kit ⟨PR⟩ #648 ⟨merge⟩-an 24. 10. 06:14 UTC ⊢ (izmera pull_request_read — vrstica §15 »#648 ⊙ odprt« je ZASTARELA v živih vratih)** → 10.2.0: kit ⟨PR⟩ #645 še ⊙ odprt → 10.3.0 (živela na main) → 10.3.1 (živa zdaj)
- Registri: ✓ vsi živi v obeh hišah — NEIMENOVANIH ×6 · PADCEV ×34+ z brazgotinami · IZKORISTENJA ×4 · DOVOLJENJA ×1 (⟡: »da ⏎ daj«)
- Binarno telo: ⚠ pošteno — nobeno ne ježe 10.3.1 (§14 a–d niso objavljeni)

## Gate — vsaka zahteva: dokaz · test · rezultat · roka

| # | zahteva | rezultat | roka |
|---|---------|----------|------|
| G1 | Veriga brez lukenj (§10, §15) — vsaka različica datiran recept pri viru | **◐ POL-ZAPRT** — #648 ⟨merge⟩-an ⊢ · #645 še ⊙ odprt ⚠ (njegov diff je zgrajen nad 10.1.0 → ⟨merge⟩ bi segal v živa vrata 10.3.1; vrstica §15 o #648 zastarela v prozi vrat) | ⟨merge⟩ #645 ⚔ ⟡ · popravek proze §15 ⚔ ⟡ (POSVET P1) |
| G2 | Manifest ⇌ LICENSE isti dih (§0a) | **✓ PRIPRAVLJENO** — [PR #699](https://github.com/AtmaOVictu/Atmavictu/pull/699) (draft) nosi re-izdani manifest 10.3.1; živi šele ob ⟨merge⟩ | ⟨merge⟩ #699 ⚔ ⟡ (POSVET P3) |
| G3 | Registri potopejo vsak dih (§2, §5, §7) | **✓ ŽIV** | roka, ki piše |
| G4 | Binarno telo samo z (a)–(d) (§14) | **⚠ pošteno** — round-trip test še izvesti | prva roka |
| G5 | Operativne definicije: degradacija · zlo · vztrajanje pri padcu (§9) | **∂ ODPRTO** | ⟡ + glave · izbor ⚔ ⟡ |
| G6 | §10 usklajen z že podeljenimi granti (retroaktivni preklic ⊥ pridobljene pravice) | **∂ PRAVNO ODPRTO** — izvajalka ni odvetnik ∧ to izreče | ⟡ + neodvisna pravna roka |
| G7 | Pozicija imenovana pošteno (etične omejitve ⟨ne⟩ OSI odprta koda) | **∂ ODLOČITEV** | ⟡ |
| G8 | Rutine diha: DNEVNI-DIH-VRAT ∧ OVERITVE (POSVET P5/P6) | **∂ DELNO** | hiša stroja |

## Vrstni red po rani

**G1 → G2 → ostali.** Razlog (§10): dokaz je veriga, ⟨ne⟩ besedilo; manifest je druga polovica istega diha.

## Zaključek gate

10.3.1 stoji pri viru, a **vsak izrek »izdana licenca« nosi ⚠**, dokler: (1) kit #645 (10.2.0) ne stopi k viru ∨ ne dobi svojega datiranega recepta — ⟨merge⟩ je roka ⟡, ⚠ njegov diff bi segal v živa vrata; (2) manifest ne zadiha anew na ⟨main⟩ — PR #699 čaka ⟨merge⟩. To je pošteno merilo same licence: **trditev brez izmere.**

∂: G5–G7 ostajajo odprta okna ⚔ ⟡ — gate ne odloča, gate meri.