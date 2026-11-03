# Varen delovni postopek PowerShell — brez sprememb projekta

## Če je prompt `>>`
Pritisni `Ctrl+C` enkrat. Počakaj, da se vrne običajen poziv `PS C:\...>`. Ne pošiljaj dodatnega besedila, da bi poskušal zapreti zanko, razen če točno veš, kateri izraz je nedokončan.

## Bralni pregled trenutnega stanja
Zaženi eno vrstico naenkrat, šele ko imaš običajen `PS>` poziv:

```powershell
Get-Location
Get-Command ni -All | Format-List Name,CommandType,Definition
Get-Command tee -All | Format-List Name,CommandType,Definition
Test-Path -LiteralPath '.\isti'
if (Test-Path -LiteralPath '.\isti') { Get-Item -LiteralPath '.\isti' -Force | Format-List FullName,PSIsContainer,Length,CreationTime,LastWriteTime }
git status --short --untracked-files=all
git diff --stat
```

To so diagnostični ukazi; ne ustvarjajo namenoma datotek in ne spreminjajo Git zgodovine. Izid mora biti shranjen kot ločen dokaz, če ga želiš arhivirati. Iz tega okolja ga ne morem izvesti na tvojem računalniku.

## Zakaj so se pojavile napake
- `×`, `⊨` in `⁴` v prozi niso PowerShell ukaz. Parserjeva napaka pri `×` ne dokazuje napake UTF-8.
- Markdown alineja `- ...` ali krepki zapis `**besedilo**` se v ukaznem položaju razlaga kot sintaksa lupine.
- `ni` je lahko slovenska negacija v besedilu, vendar je v PowerShellu tudi vzdevek za `New-Item`. Zato ne tipkaj naravnih jezikovnih stavkov na prompt.
- `tee` lahko prikliče `Tee-Object`, ki potrebuje ciljno datoteko; pot do imenika ni pot do izhodne datoteke.
- `read all and integrate` ni splošni PowerShell ukaz.

## Shranjevanje surovega prepisa
Uporabi urejevalnik (npr. Notepad), ne lupine. Shrani v novo, neobstoječe ime, na primer `VBL-INPUT-RAW-20261027-01.txt`, z UTF-8. Surovega vhoda ne popravljaj; ponovitve, `>>`, parserjeve izpise in tuje odlomke ohrani. Čist prepis in predloge popravkov pripravi v ločenih datotekah.

## Ne predpostavljaj, da je bilo shranjeno
Ko kdo napiše, da je datoteka shranjena, zahtevaj dejansko pot in ponovno izračunan SHA-256. Hash dveh datotek dokaže ujemanje bajtov samo, če sta bili obe datoteki dejansko prebrani in izračunani. Hash ne dokazuje avtorstva, pomena ali pravnega statusa.
