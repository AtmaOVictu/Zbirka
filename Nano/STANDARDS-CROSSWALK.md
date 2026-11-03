# VBL — zunanja primerjava okvirov (orientacijska, ne certifikacijska)

**Status:** `CROSSWALK_DRAFT` · 2026-10-25

| Vir | Kaj vir zares določa | Kje se VBL trenutno dotika teme | Neusklajena vrzel | Kaj bi dokazovalo zaprtje |
|---|---|---|---|---|
| NIST AI RMF 1.0 | Funkcije Govern, Map, Measure, Manage; tveganja obravnava skozi življenjski cikel; spodbuja različne perspektive in neodvisno preverjanje. | Verifikacija, dokazni register, validator, zunanji pregled kot zahteva. | Ni dokončnega crosswalk-a od vsake VBL kontrole do dokaza, ownerja, metrike, residual risk in cikla ponovitve. | Usklajen kontrolni zemljevid, run ID, ponovljivi testi, preostalo tveganje in časovni načrt ponovne ocene. |
| ISO/IEC 42001:2023 | Organizacijski sistem upravljanja AI; politika, odgovornosti, tveganja, monitoring in stalno izboljševanje. Standard ne nadomesti zakona. | VBL predlaga odgovornost, release gates in evidence. | Ni organizacijskega obsega, imenovanih odgovornih vlog, vodstvene odobritve, notranje revizije, CAPA oziroma cikla izboljševanja. | Obseg sistema upravljanja, imenovane vloge, vodstvena odobritev, notranji audit in sled popravnih ukrepov. |
| EU AI Act (obseg je odvisen od dejanske vloge in uporabe) | Pravne obveznosti so odvisne od tega, ali dejavnost/sistem spada v področje uredbe, vrste akterja in tveganja. Časovnica je postopna. | VBL se nanaša na AI/agentne prototipe in dokazljivost. | Ni analizirano, ali je vsak konkretni sistem ponudnik/deployer, GPAI akter, visokorizičen sistem ali zunaj posameznega področja; VBL sam ne dokazuje skladnosti. | Pravna klasifikacija konkretnega sistema, vloge, uporabe in jurisdikcije ter obveznosti, ki se nanj dejansko nanašajo. |
| Konvencija Sveta Evrope o AI | Načela človekovega dostojanstva in avtonomije, enakosti/nediskriminacije, zasebnosti, preglednosti/nadzora, odgovornosti, zanesljivosti in varnih inovacij; postopkovne varovalke in možnosti pritožbe. | Absolutna enakost, pravica do ugovora, neodvisen pregled, poprava škode. | Pojmi so delno normativni slogani; ni dovolj definiranih postopkovnih jamstev, eskalacije, pritožbe in presoje učinkov. | Testni primeri za ranljive osebe, proces pritožbe, dokumentirani remedies, neodvisni pregled in izsledki. |
| GDPR, zlasti 5. člen; pravice posameznikov vključujejo tudi vprašanja izbrisa po 17. členu | Načela zakonitosti, pravičnosti, preglednosti, omejitve namena, najmanjšega obsega, točnosti in omejitve hrambe. Pravica do izbrisa ni absolutna v vseh okoliščinah; veljajo pogoji in izjeme. | Dnevnik append-only, evidence, redakcija, popravljanje zgodovine. | Napetost med »ne briši zgodovine« in zasebnostjo/zakonskim izbrisom; ni dokončane politike namena, roka, pravne podlage in redakcije. | Ocena zasebnosti, pravila hrambe, test dostopa, pot za popravek/izbris, najmanjši zakonito dopusten revizijski zapis. |
| Slovenska uradna razlaga avtorskega prava | Varuje konkretno izražena avtorska dela v obsegu prava; sama ideja, načelo ali odkritje ni avtorsko varovano kot tako. | VBL poskuša hkrati licencirati besedilo in razširiti etične principe. | Ni jasnega razreza pravnega predmeta; ni potrjen imetnik pravic ali pooblastilo za izdajo. | Komponentni manifest, dovoljenja in pravni pregled po posameznem predmetu. |
| Creative Commons | Standardne CC licence so določena pravna orodja za varovana dela/pravice; pogoje treba izbrati in pravilno uporabiti. FAQ obravnava omejitve, dovoljenja in posledice kršitev. | VBL preučuje javno licenco in ponovno uporabo. | Še ni izbrana licenca. Če VBL doda vedenjske pogoje, ne sme prikazati spremenjenega pravnega teksta kot nespremenjeno standardno CC licenco. | Odhodna odločitev imetnika pravic, analiza primernosti CC za vsak predmet in pravni pregled posebnih pogojev. |

## Varnost pri uporabi zunanjih okvirov

1. »Mapirano na« pomeni, da obstaja primerjava; ni sinonim za »skladno« ali »certificirano«.
2. NIST AI RMF je okvir upravljanja tveganj, ne zakon in ne avtomatična licenca.
3. ISO/IEC 42001 je standard sistema upravljanja; omemba v VBL ne daje certifikata.
4. EU AI Act velja po dejanskem področju, vlogi, uporabi in prehodnih datumih. Pravna klasifikacija mora biti specifična za sistem.
5. Evidenčni integritetni mehanizem nikoli ne sme biti razlaga za shranjevanje osebnih podatkov brez časovne meje ali podlage.

## Uradni viri

- NIST AI RMF Core (opisuje funkcije Govern, Map, Measure, Manage in kontinuirano upravljanje tveganj): https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- ISO/IEC 42001:2023: https://www.iso.org/standard/42001
- EU AI Act implementation timeline: https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline
- Council of Europe Framework Convention on AI: https://www.coe.int/en/web/artificial-intelligence/the-framework-convention-on-artificial-intelligence
- GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- GOV.SI: https://www.gov.si/teme/avtorska-in-sorodne-pravice/
- Creative Commons FAQ: https://creativecommons.org/faq/
