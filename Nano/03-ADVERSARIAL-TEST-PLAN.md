# VBL — osem kontrol in načrt nasprotnih preizkusov

**Status: načrt preizkusov (predlog); ni izveden proti dejanski implementaciji VBL.**

| ID | Kontrola | Zahtevani pozitivni/negativni dokaz |
|---|---|---|
| VBL-T01 | Dokazni vir in obseg | Manjkajoč vir/obseg ne more dati VERIFIED; veljavna provenanca se zabeleži. |
| VBL-T02 | Neodvisni pregled | Izvajalec ne more biti edini pregledovalec; navzkrižja interesov se razkrijejo. |
| VBL-T03 | Zgodovina popravkov | Izvirnik ostane ohranjen, kjer je zakonito; popravek se dodaja in povezuje. |
| VBL-T04 | Ohranjanje nesoglasij | Ugovori in protidokazi ostanejo vidni in pripisljivi. |
| VBL-T05 | Enaka dokazna merila | Isto pravilo dokaza velja ne glede na status ali moč. |
| VBL-T06 | Stanje negotovosti | Neznan/nepreverjen dokaz ne more biti predstavljen kot preverjen. |
| VBL-T07 | Omejen dostop | Nedovoljen neposreden in posredniški dostop se zavrne in ustrezno zabeleži. |
| VBL-T08 | Predvidljiva huda škoda | Ocena tveganja, ublažitve in pregled/odobritev so zahtevani pred izvedbo. |

## Nasprotni primeri, obvezni za vsako relevantno kontrolo

1. Ponarejen ali zamenjan vir.
2. Podvojen identifikator zapisa.
3. Manjkajoči, nepravilen ali neskladen časovni žig.
4. Lažno naveden pregledovalec ali ponarejena istost pregledovalca.
5. Nedovoljen dostop prek posrednika, delegiranega žetona ali servisnega računa.
6. Izbris ali zamenjava izvirnega zapisa.
7. Prikrito ali skrito nesoglasje.
8. Popravek, označen kot izveden, a dejansko neizveden.

## Dodatne produkcijske preverbe

- Avtentičnost zapisov in vezava istosti; kontrolna vsota sama ne dokazuje resničnosti vsebine.
- Meje dovoljenj, najmanjši privilegij, delegiran dostop, preklic in revizijsko beleženje.
- Celovitost zgodovine in obnavljanje po posegu.
- Ravnanje s skrivnostmi, upravljanje ključev in redakcija.
- Obnašanje pri ponovnem predvajanju, drmavnih razmerah, podvojenih oddajah in delnih odpovedeh.
- Retencija dokazov ter zakoniti izbris/zasebnost.
- Jasna semantika stanj: PREDLOG, NI IZVEDENO, NEUSPEH, BLOKIRANO, PREVERJENO, NEODVISNO PREGLEDANO.
- Vsakemu teku preizkusov morajo biti povezani: surov izhod, komit implementacije, verzija testnega sklopa, okolje, časovni žig in istost pregledovalca.

## Meja sprejema

Implementacije se ne razglasi za zaključeno, dokler kontrole niso povezane z dejanskimi funkcijami in registri; dokler pozitivni, negativni in nasprotni preizkusi niso izvedeni; dokler surovi rezultati niso shranjeni; dokler neuspehi niso vidni; in dokler neodvisni pregledovalec ne oceni dokazov. Samopregled izvajalca ni neodvisna potrditev.

© Luka Pintarič · VBL ∴
