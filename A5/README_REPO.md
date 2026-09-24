# UNIVERZALNO — LUKA: CILJI · MOTIVACIJE · AGENTI

Operativni paket (plakati, podatki, prepress). Privzeta licenca: **CC BY-NC 4.0** (glej `LICENSE`).

## Struktura map
```
.
├── README.md
├── LICENSE                           # CC BY-NC 4.0 (privzeto) – zamenjaj po potrebi
├── docs/
│   └── LUKA_PRIROCNIK.md
├── data/
│   ├── LUKA_CILJI.csv
│   ├── LUKA_MOTIVACIJE.csv
│   ├── LUKA_OMEJITVE.csv
│   ├── LUKA_AGENTI.csv
│   ├── LUKA_CHECKLIST.csv
│   └── LUKA_META.json
├── design/
│   ├── svg/
│   └── pdf/
│       ├── vector/                   # besedilo ostane vektor
│       └── outlined/                 # obrisano besedilo (paths)
├── print/
│   ├── a3/
│   ├── a4/
│   └── packs/                        # zip paketi za tisk
├── raster/
│   ├── cmyk/
│   ├── k-only/
│   └── rich-black/
└── prepress/
    ├── ATTRIBUTION_FOOTER.svg
    ├── PDFX1a_Preflight_Checklist.txt
    ├── LUKA_PDFX1a_ISOcoatedV2.joboptions
    └── LICENSE_OPTIONS/
```
## Git LFS (priporočeno)
Za velike TIFF/PDF datoteke uporabi Git LFS:
```
git lfs install
echo "*.tif filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.pdf filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
```

## Attribution (zahteva licence)
Uporabi spodnjo vrstico kjerkoli objaviš ali predelaš material:

> © 2025 JEWIK / DAJ — UNIVERZALNO · Licensed CC BY-NC 4.0

Lahko tudi prilepiš `prepress/ATTRIBUTION_FOOTER.svg` na dno plakata.

## PDF/X
- Prednastavitve v `prepress/LUKA_PDFX1a_ISOcoatedV2.joboptions`
- Checklist v `prepress/PDFX1a_Preflight_Checklist.txt`

## Kontakt/izvoz
Za posebne dimenzije, CMYK profile ali stabilno *rich black* shemo v prepressu, odpri issue ali povej “RICH/VEKTOR/IDML”.

— JEWIK / DAJ · 2025
