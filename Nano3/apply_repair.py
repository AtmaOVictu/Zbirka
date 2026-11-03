#!/usr/bin/env python3
"""Apply the evidence-based VBL attribution repair to an exact measured checkout.

Safe-by-default properties:
- refuses a dirty worktree or a different base commit;
- creates a local topic branch (never pushes or merges);
- backs up every touched file under .git/vbl-repair-backup-2026-10-30;
- prepares all transformations in memory before writing any file;
- validates JSONL and runs the manifest check after writing; restores files on failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_COMMIT = "a6fba5af94110b2107531c6cbe141afb393d10f5"
BRANCH = "repair/attribution-evidence-2026-10-30"
LIVE_VERSION = "0.1210 × 10⁴"

POINTER_FILES = [
    "README.md", "README-SL.md", "QUICKSTART.md", "REPRODUCE.md",
    "IZMERNI-PROTOKOL.md", "CANONICAL.md", "KORENINA.md",
    "PROVENANCE-CHANNEL.md", "eval/README.md", "llms.txt",
]

OLD_EN = "The asymmetry it corrects, documented: Reddit received ~$60M/year from Google for training data; the writers received nothing. Stack Overflow sold contributor answers to OpenAI; contributors who deleted their own answers to opt out were banned. Mozilla Common Voice: 250+ languages of volunteer recordings, CC0, contributors unpaid. RLHF annotation is already a paid profession ($12–25/hr) — the money exists; the channel for native experts offering *verified* corrections does not. The missing row is a verified language contribution from a native expert in an unsupported language. This document proposes closing exactly that gap. ∂"
NEW_EN = "The asymmetry this proposal addresses matters, but each claim must stay within its evidence. Reuters reported a Reddit–Google content-licensing deal and estimated its value at roughly US$60 million per year; Reuters also said both companies declined to comment on the price, and the report does not establish whether individual posters were paid. OpenAI's public announcement describes a partnership with Stack Overflow using OverflowAPI, enhanced content and community feedback; it does not publish individual contributor payment terms. The Register reported one user's claim that he was suspended for seven days after he overwrote answers as a protest, alongside other user reports; this is a report about protest-related account action, not proof that ordinary self-deletion itself triggers a ban. Stack Overflow's Help Center says users may generally delete their own answers except accepted answers, and separately explains answer bans in terms of low-quality answer history. Common Voice datasets are released under CC0, but CC0 status does not establish individual compensation. Individual contributor payment status remains ⚠ unless separately evidenced. Sources: [Reuters on Reddit–Google](https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/); [OpenAI on the Stack Overflow partnership](https://openai.com/index/api-partnership-with-stack-overflow/); [The Register's reported protest case](https://www.theregister.com/software/2024/05/09/stack-overflow-suspends-users-protesting-openai-deal/1032471/); [Stack Overflow licensing](https://stackoverflow.com/help/licensing), [deletion rules](https://stackoverflow.com/help/deleted-answers) and [answer bans](https://stackoverflow.com/help/answer-bans); [Common Voice terms](https://commonvoice.mozilla.org/oc/terms). ∂"
OLD_EN_POVEJMO = "- Training data from a **national citizen-science campaign** (povejmo.si) toward a 40-billion-word corpus, with the National and University Library, Dnevnik, and the Slovenian Press Agency — framed as digital sovereignty for a two-million-speaker language. ⊢"
NEW_EN_POVEJMO = "- Training-data collection included a **national citizen-science campaign** (povejmo.si) toward a 40-billion-word corpus, with the National and University Library, Dnevnik, and the Slovenian Press Agency. The public project description says submitters must hold copyright in the text they submit; it does not identify every submitter or establish individual compensation. [Project description](https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/). ⊢ / ⚠"
OLD_SL = "Asimetrija, ki jo popravlja, dokumentirana: Reddit je prejel ~60 milij. USD na leto od Googla za učne podatke; avtorji prispevkov niso prejeli nič. Stack Overflow je prodal odgovore prispevnikov OpenAI; tisti, ki so jih izbrisali, so bili izključeni. Mozilla Common Voice: 250+ jezikov prostovoljnih posnetkov, CC0, prispevniki neplačani. Označevanje RLHF je že plačan poklic — denar obstaja; kanal za izvirne govorce z *preverjenimi* popravki ne. Vrstica, ki manjka: preverjen jezikovni prispevek izvirnega govorca v nepodprtem jeziku. Ta dokument predlaga, da se vrzel zapre. ∂"
NEW_SL = "Asimetrija, ki jo predlog naslavlja, je pomembna, vendar mora vsaka trditev ostati znotraj dokazov. Reuters je poročal o dogovoru Reddit–Google za licenciranje vsebin in ocenil vrednost na približno 60 milijonov USD na leto; hkrati je navedel, da podjetji cene nista komentirali. Poročilo ne dokazuje, ali so bili posamezni avtorji objav plačani. OpenAI je partnerstvo s Stack Overflow opisal prek dostopa OverflowAPI, izboljšanih vsebin in povratnih informacij skupnosti; objava ne razkriva plačil posameznim prispevnikom. The Register je poročal o navedbi enega uporabnika, da je prejel sedemdnevni suspenz, potem ko je odgovore prepisal v protestno sporočilo, ter o drugih prijavah uporabnikov. To je omejeno poročilo o ukrepu po protestnem posegu v objave, ne dokaz, da že običajen samostojni izbris odgovora sproži prepoved. Center za pomoč Stack Overflow praviloma dopušča samostojni izbris odgovora, razen sprejetega odgovora, prepoved odgovarjanja pa ločeno povezuje z zgodovino manj kakovostnih odgovorov. Zbirke Common Voice so objavljene pod CC0; sama licenca CC0 ne pove, ali je bil posamezni sodelavec plačan. Plačilo posameznikov ostane ⚠, dokler ni posebej dokazano. Viri: [Reuters o dogovoru Reddit–Google](https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/); [OpenAI o partnerstvu s Stack Overflow](https://openai.com/index/api-partnership-with-stack-overflow/); [poročani protestni primer The Register](https://www.theregister.com/software/2024/05/09/stack-overflow-suspends-users-protesting-openai-deal/1032471/); [licenca Stack Overflow](https://stackoverflow.com/help/licensing), [pravila brisanja](https://stackoverflow.com/help/deleted-answers) in [prepovedi odgovarjanja](https://stackoverflow.com/help/answer-bans); [pogoji Common Voice](https://commonvoice.mozilla.org/oc/terms). ∂"
OLD_SL_POVEJMO = "- Učni podatki iz **nacionalne kampanje občanske znanosti** (povejmo.si) proti 40-milijardnemu besednemu korpusu, z NUK, Dnevnikom in STA — predstavljeno kot digitalna suverenost za jezik z dvema milijonoma govorcev. ⊢"
NEW_SL_POVEJMO = "- Zbiranje učnih besedil je vključevalo **nacionalno kampanjo občanske znanosti** (povejmo.si) za nastajajoči 40-milijardni besedni korpus, z NUK, Dnevnikom in STA. Javni opis projekta določa, da mora imeti oddajatelj avtorske pravice za oddano besedilo; ne razkriva vseh oddajateljev in ne dokazuje plačila posameznikom. [Opis projekta](https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/). ⊢ / ⚠"

SSKJ_AUTHORS = [
    "Nataša Gliha Komac", "Nataša Jakop", "Boris Kern", "Simona Klemenčič",
    "Domen Krvina", "Nina Ledinek", "Mija Michelizza", "Tanja Mirtič",
    "Andrej Perdih", "Špela Petric", "Marko Snoj", "Andreja Žele",
]
SSKJ_TERMINOLOGY_ADVISORS = [
    "Vlado Pivec (ekonomija, finance)",
    "Jana Mrak (farmacija, medicina)",
    "Primož Jakopin (film, računalništvo)",
    "Stanislav Fortuna (pravo)",
    "Suzana Tratnik (sociologija)",
]
SNBZS_SOURCE_AUTHORS = [
    "Aleksandra Bizjak Končar", "Nataša Gliha Komac", "Alenka Gložančev",
    "Boris Kern", "Simona Klemenčič", "Polona Kostanjevec", "Domen Krvina",
    "Nina Ledinek", "Mija Michelizza", "Tanja Mirtič", "Andrej Perdih",
    "Špela Petric", "Marko Snoj", "Ivanka Šircelj Žnidaršič", "Andreja Žele",
]
POVEJMO_COLLABORATORS = [
    "Marko Bajec", "Bojan Klemenc", "Iztok Lebar Bajec", "Matjaž Pančur",
    "Marko Robnik Šikonja", "Slavko Žitnik", "Špela Arhar Holdt", "Jaka Čibej",
    "Domen Vreš", "Nejc Robida", "Luka Terčon", "Cyprian Laskowski",
    "Simon Krek", "Apolonija Gantar", "Iztok Kosem", "Matej Klemen", "Martin Božič",
]


def run(cmd: list[str], cwd: Path, capture: bool = True) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=capture)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip() if capture else ""


def jsonl_load(text: str, name: str) -> list[dict]:
    rows=[]
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            value=json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{name}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{name}:{number}: expected JSON object")
        rows.append(value)
    return rows


def jsonl_dump(rows: list[dict]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count=text.count(old)
    if count != 1:
        raise ValueError(f"Expected exactly one occurrence of {label}, found {count}; refusing partial patch")
    return text.replace(old,new,1)


def transform(repo: Path) -> dict[str, str]:
    license_text=(repo/"LICENSE.md").read_text(encoding="utf-8")
    match=re.search(r"(?m)^Version\s+(.+?)\s+·",license_text)
    if not match or match.group(1).strip()!=LIVE_VERSION:
        actual=match.group(1).strip() if match else "unparseable"
        raise ValueError(f"Expected live LICENSE.md version {LIVE_VERSION}; found {actual}")

    out={}
    for rel in POINTER_FILES:
        text=(repo/rel).read_text(encoding="utf-8")
        out[rel]=text.replace("0.1100 × 10⁴",LIVE_VERSION)
        if "0.1100 × 10⁴" in out[rel]:
            raise ValueError(f"Stale version pointer remains in {rel}")

    out["README.md"]=replace_once(out["README.md"],OLD_EN,NEW_EN,"English contributor evidence paragraph")
    out["README.md"]=replace_once(out["README.md"],OLD_EN_POVEJMO,NEW_EN_POVEJMO,"English PoVeJMo description")
    out["README-SL.md"]=replace_once(out["README-SL.md"],OLD_SL,NEW_SL,"Slovenian contributor evidence paragraph")
    out["README-SL.md"]=replace_once(out["README-SL.md"],OLD_SL_POVEJMO,NEW_SL_POVEJMO,"Slovenian PoVeJMo description")

    old_ne=jsonl_load((repo/"REGISTER-NEIMENOVANIH.jsonl").read_text(encoding="utf-8"),"REGISTER-NEIMENOVANIH.jsonl")
    by_id={row.get("⊙"):row for row in old_ne}
    if len(old_ne)!=7 or "NE-0007" not in by_id:
        raise ValueError("Unexpected contributor-register shape; expected NE-0001 through NE-0007")
    ne=[
      {"⊙":"NE-0001","stran":"kredit","ime":"Inštitut za slovenski jezik Frana Ramovša, ZRC SAZU (institucionalni slovarski vir SSKJ²)","prispeval":"institucionalni izdajatelj in vir slovarske vsebine, uporabljene v citiranih geslih; kolofon elektronske izdaje ločeno navaja avtorje in tehnološko podporo — ta vrstica ni seznam posameznih avtorjev","licenca":"kolofon elektronske izdaje navaja © 2014 Inštitut za slovenski jezik Frana Ramovša ZRC SAZU; obseg pravic za posamezne citate se preverja pri viru","placano":"⚠ plačilo posameznih avtorjev/sodelavcev ni izmerjeno s tem zapisom","prica":"https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Kolofon.pdf","znamenje":"⚠"},
      {"⊙":"NE-0002","stran":"kredit","ime":"Mozilla Common Voice — prispevajoča skupnost; Scripted Speech v27.0 (metapodatki 2026-09: 295 jezikov)","prispeval":"zvočni posnetki, besedila, validacije in povratne informacije v posameznih, verzioniranih zbirkah; podatke in licence je treba vezati na konkretno izdajo in jezik","licenca":"CC0-1.0 za objavljene zbirke Common Voice; preveri konkretno izdajo","placano":"⚠ plačilo posameznih sodelavcev ni ugotovljeno; CC0 ne dokazuje neplačanosti","prica":"https://github.com/common-voice/cv-dataset/ ; https://commonvoice.mozilla.org/oc/terms","znamenje":"⚠"},
      {"⊙":"NE-0003","stran":"kredit","ime":"Stack Overflow / Stack Exchange — avtorji javnih vprašanj in odgovorov","prispeval":"javne objave in njihove revizije; OpenAI je 6. 5. 2024 objavil partnerstvo prek OverflowAPI ter uporabo izboljšanih vsebin in povratnih informacij skupnosti; The Register je 9. 5. 2024 poročal o navedbi enega uporabnika, da je prejel sedemdnevni suspenz po protestnem prepisu odgovorov, ter o drugih prijavah, kar ni dokaz, da je običajen samostojni izbris sam po sebi prepovedan","licenca":"CC BY-SA 2.5 / 3.0 / 4.0 glede na datum posamezne objave oziroma revizije","placano":"⚠ plačilo posameznim avtorjem ni izmerjeno; partnerstvo podjetij ne dokazuje individualnega plačila","prica":"https://openai.com/index/api-partnership-with-stack-overflow/ ; https://stackoverflow.com/help/licensing ; https://stackoverflow.com/help/deleted-answers ; https://stackoverflow.com/help/answer-bans ; https://www.theregister.com/software/2024/05/09/stack-overflow-suspends-users-protesting-openai-deal/1032471/","znamenje":"⚠"},
      {"⊙":"NE-0004","stran":"kredit","ime":"Reddit — uporabniki, katerih objave so del uporabniške vsebine","prispeval":"objavljena uporabniška vsebina; Reuters je poročal o licenciranju vsebin Google za učenje UI in navedel oceno približno 60 milijonov USD letno; Reuters je obenem navedel, da Reddit in Google cene nista komentirala","licenca":"poslovni dogovor Reddit–Google po Reutersovem poročilu; konkretni pogoji in pravice posamezne objave tukaj niso razčlenjeni","placano":"⚠ individualno plačilo avtorjem objav ni ugotovljeno; ocenjena vrednost dogovora na ravni podjetij ni dokaz plačila posameznikom","prica":"https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/","znamenje":"⚠"},
      {"⊙":"NE-0005","stran":"kredit","ime":"povejmo.si / PoVeJMo — državljanska kampanja zbiranja slovenskih besedil","prispeval":"zbiranje pisnih in govorjenih slovenskih besedil ZA gradnjo velikega jezikovnega modela; projektni opis ocenjuje potrebo na 40 milijard besed in zahteva, da ima oddajatelj avtorske pravice za oddano besedilo; projekt je naveden kot zaključen 1. 1. 2026","licenca":"projektni opis določa pogoj imetništva avtorskih pravic oddajatelja; iz tega opisa se ne sklepa o popolnem prenosu ali splošni licenci","placano":"⚠ plačilo posameznim oddajateljem in projektnim sodelavcem ni ugotovljeno","prica":"https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/ ; https://www.fri.uni-lj.si/en/projects/1818","znamenje":"⚠"},
      {"⊙":"NE-0006","stran":"kredit","ime":"Avtorji knjig in imetniki pravic do del, za katera obstajajo konkretne navedbe o vključitvi v zbirko Books3","prispeval":"kredit in pravice se ugotavljajo po posameznem delu in zbirki. Objavljeni viri opisujejo Books3 kot zbirko knjig, obravnavano v razpravah o učenju modelov; ta vrstica ne trdi, da je vsak jezikovni model uporabil Books3 ali da je bila vsaka uporaba posamezne knjige nezakonita","licenca":"pravice ostanejo odvisne od posameznega dela, imetnika pravic, vira in konkretne uporabe; ni ene skupne licence","placano":"⚠ plačilo avtorjem posameznih del ni ugotovljeno iz teh splošnih virov","prica":"https://authorsguild.org/news/you-just-found-out-your-book-was-used-to-train-ai-now-what/ ; https://www.transparencycoalition.ai/learn/tcai-guide-to-search-tools-was-your-data-used-to-train-an-ai-model ; za vsako delo in konkreten model je potreben dodatni dokaz","znamenje":"⚠"},
      by_id["NE-0007"],
      {"⊙":"NE-0008","stran":"kredit","ime":"Avtorji SSKJ² — druga, dopolnjena in deloma prenovljena izdaja","prispeval":"uradni seznam Avtorji: "+"; ".join(SSKJ_AUTHORS)+". Gre za avtorje izdaje, ne za seznam urednikov ali celotnega osebja; vlog se ne zamenjuje","licenca":"kolofon elektronske izdaje navaja © 2014 Inštitut za slovenski jezik Frana Ramovša ZRC SAZU; individualne avtorske pogodbe niso ugotovljene","placano":"⚠ plačilo posameznih avtorjev ni ugotovljeno iz javnih virov, navedenih tukaj","prica":"https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf ; https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Kolofon.pdf","znamenje":"⚠"},
      {"⊙":"NE-0009","stran":"kredit","ime":"SSKJ² — tehnološka podpora: Nina Ledinek; Andrej Perdih","prispeval":"kolofon ju posebej navaja pod Tehnološka podpora; obe osebi sta navedeni tudi na seznamu avtorjev, zato je vloga tehnološke podpore ločena od avtorstva in se ne šteje kot dodatni dve osebi","licenca":"kolofon elektronske izdaje: © 2014 Inštitut za slovenski jezik Frana Ramovša ZRC SAZU","placano":"⚠ plačilo za posamezno vlogo ni ugotovljeno","prica":"https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Kolofon.pdf ; https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf","znamenje":"⚠"},
      {"⊙":"NE-0010","stran":"kredit","ime":"PoVeJMo — javno navedeni sodelavci projekta","prispeval":"uradna projektna stran kot sodelavce oziroma vodje projekta/delovnih paketov navaja: "+"; ".join(POVEJMO_COLLABORATORS)+". Ta seznam je projektni seznam sodelavcev, ne popoln seznam oddajateljev korpusa in ne trditev, da je vsak posameznik avtor vsakega modela","licenca":"projektna stran sama ne podeljuje licence za posamezna oddana besedila","placano":"⚠ plačilo posameznih sodelavcev ali oddajateljev ni ugotovljeno","prica":"https://www.fri.uni-lj.si/en/projects/1818 ; https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/","znamenje":"⚠"},
      {"⊙":"NE-0011","stran":"kredit","ime":"GaMS3-12B — avtorska skupina in zahvala za zbiranje/pripravo podatkov (ločeni vlogi)","prispeval":"model card kot ekipo raziskovalcev navaja: Domen Vreš; Iztok Lebar Bajec; Tjaša Arčon; Timotej Petrič; Dario Vajda; Marko Robnik-Šikonja. Za zbiranje in pripravo podatkov se posebej zahvaljuje: Nikola Ljubešić; Taja Kuzman; Tjaša Arčon; Jaka Čibej; Simon Krek; Tomaž Erjavec; Iztok Kosem; Tomaž Savodnik. Prekrivajoče se ime ostane navedeno v obeh vlogah; to ni dokaz, da je 'T. Kuzman' iz drugega vnosa registra ista oseba","licenca":"model card navaja licenco modela Gemma; licenciranja vseh vhodnih zbirk ta zapis ne sklepa","placano":"⚠ plačilo posameznih članov in sodelavcev za podatkovno pripravo ni ugotovljeno","prica":"https://huggingface.co/cjvt/GaMS3-12B","znamenje":"⚠"},
      {"⊙":"NE-0012","stran":"kredit","ime":"SSKJ² — terminološki svetovalci (ločeno od avtorjev izdaje)","prispeval":"kolofon na seznamu Terminološki svetovalci navaja: "+"; ".join(SSKJ_TERMINOLOGY_ADVISORS)+". Te osebe so zapisane v svetovalni vlogi; ne štejejo se kot dodatni avtorji izdaje.","licenca":"uradni avtorski seznam in kolofon elektronske izdaje SSKJ²; individualni dogovori niso ugotovljeni","placano":"⚠ plačilo posameznih svetovalcev ni ugotovljeno iz javnega kolofona","prica":"https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf ; stran 8, razdelek Terminološki svetovalci","znamenje":"⚠"},
      {"⊙":"NE-0013","stran":"kredit","ime":"Slovar novejšega besedja slovenskega jezika (2012) — avtorji uporabljenega izvornega gradiva","prispeval":"opomba 2 v uradnem seznamu SSKJ² pravi, da je bilo pri drugi, dopolnjeni in deloma prenovljeni izdaji uporabljeno tudi to slovarsko delo; njegovi avtorji so: "+"; ".join(SNBZS_SOURCE_AUTHORS)+". To so avtorji predhodnega slovarja kot uporabljenega gradiva, ne dodatni avtorji SSKJ².","licenca":"uporaba navedenega dela kot gradiva je zapisana v uradni opombi; posamezne avtorske pogodbe in pogoji ponovne uporabe niso ugotovljeni","placano":"⚠ plačilo posameznih avtorjev predhodnega slovarja ni ugotovljeno iz tega vira","prica":"https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf ; stran 8, opomba 2","znamenje":"⚠"},
    ]
    out["REGISTER-NEIMENOVANIH.jsonl"]=jsonl_dump(ne)

    extraction=jsonl_load((repo/"REGISTER-IZKORISTENJA.jsonl").read_text(encoding="utf-8"),"REGISTER-IZKORISTENJA.jsonl")
    positions={row.get("⊙"):i for i,row in enumerate(extraction)}
    if "IZ-0001" not in positions or "IZ-0004" not in positions:
        raise ValueError("Expected extraction entries IZ-0001 and IZ-0004")
    extraction[positions["IZ-0001"]]={
      "⊙":"IZ-0001","stran":"izkoriščanje / poslovno licenciranje podatkov","kdo":"Reddit Inc.",
      "dejanje":"Reuters je poročal, da je Reddit licenciral uporabniško vsebino Googlu za učenje modelov UI; viri so vrednost ocenili na približno 60 milijonov USD na leto, Reddit in Google pa cene nista komentirala. Poročilo ne ugotavlja, ali so bili posamezni avtorji objav plačani.",
      "kje":"reddit.com","kdaj":"2024-02-22 (poročilo Reuters)",
      "prica":"Reuters: https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/","znamenje":"⚠"
    }
    extraction[positions["IZ-0004"]]={
      "⊙":"IZ-0004","stran":"izkoriščanje / partnerstvo in upravljanje objav","kdo":"Stack Overflow (podjetje) / OpenAI (partnerstvo)",
      "dejanje":"OpenAI je 2024-05-06 opisal partnerstvo prek izdelka OverflowAPI, uporabo izboljšanih vsebin in povratnih informacij skupnosti ter navajanje virov; javna objava ne razkriva plačil posameznim avtorjem. The Register je 2024-05-09 poročal o navedbi enega uporabnika, da je prejel sedemdnevni suspenz po protestnem prepisu objav, ter o drugih prijavah uporabnikov. Uradni center za pomoč ločeno navaja, da lahko uporabniki praviloma sami izbrišejo svoje odgovore, razen sprejetih, ter da so prepovedi odgovarjanja vezane na zgodovino manj kakovostnih odgovorov. Poročani protestni primer se ne posplošuje na običajen samostojni izbris.",
      "kje":"stackoverflow.com / openai.com","kdaj":"2024-05-06 (partnerstvo objavljeno); 2024-05-09 (poročilo o protestu)",
      "prica":"OpenAI: https://openai.com/index/api-partnership-with-stack-overflow/ ; The Register: https://www.theregister.com/software/2024/05/09/stack-overflow-suspends-users-protesting-openai-deal/1032471/ ; Stack Overflow: https://stackoverflow.com/help/licensing ; https://stackoverflow.com/help/deleted-answers ; https://stackoverflow.com/help/answer-bans","znamenje":"⚠"
    }
    out["REGISTER-IZKORISTENJA.jsonl"]=jsonl_dump(extraction)

    falls=jsonl_load((repo/"REGISTER-PADCEV.jsonl").read_text(encoding="utf-8"),"REGISTER-PADCEV.jsonl")
    max_entry=max((int(row.get("entry",0)) for row in falls),default=0)
    if max_entry!=34 or len(falls)!=34:
        raise ValueError(f"Unexpected named-falls register: {len(falls)} rows, maximum entry {max_entry}; expected 34")
    falls.append({
      "entry":35,"date":"2026-10-30",
      "word":"REGISTER-NEIMENOVANIH.jsonl, REGISTER-IZKORISTENJA.jsonl, README.md and README-SL.md — contributor attribution / public claims",
      "fall":"the live records and mirrored prose carried claims beyond the available witnesses: (1) NE-0001 called four people editors of SSKJ² and mixed the institution with a partial/inaccurate role list; (2) NE-0002 and both READMEs called Common Voice contributors unpaid without a per-contributor payment witness; (3) NE-0003/IZ-0004 described the Stack Overflow–OpenAI partnership as a sale and generalized a protest-related suspension report into a ban for deleting answers; (4) NE-0004/IZ-0001 treated Reuters' approximately US$60M/year estimate as confirmed and stated that writers received nothing, although Reuters said both companies declined to comment on price and did not establish individual payments; (5) NE-0005 and README-SL.md described the PoVeJMo collection campaign as being 'against' the 40-billion-word corpus, reversing the official purpose; (6) NE-0006 generalized a specific training-data concern to language models broadly.",
      "correction":f"proposed on local branch {BRANCH}: source-separated SSKJ² authors, institution and technology-support roles; named PoVeJMo and GaMS3-12B project/model roles separately; corrected the campaign direction and copyright condition; scoped Stack Overflow partnership and protest report; downgraded unsupported individual compensation claims to ⚠; retained Reuters' deal value only as a reported estimate; synchronized live version pointers and made manifest generator derive version from LICENSE.md. This repair is not live on main until independently reviewed and merged.",
      "scar":True,"law":"L1/L3/L4"
    })
    out["REGISTER-PADCEV.jsonl"]=jsonl_dump(falls)

    script=(repo/"scripts/manifest_gen.py").read_text(encoding="utf-8")
    script=replace_once(script,"import os\nimport sys","import os\nimport re\nimport sys","manifest generator imports")
    old_block='''def generate():\n    return {\n        "license": "VBL — Verification Before Assertion License",\n        "version": "0.1100 × 10⁴",'''
    new_block='''def license_version():\n    """Read the living version from the current LICENSE.md; never pin a stale pointer."""\n    with open(os.path.join(ROOT, "LICENSE.md"), encoding="utf-8") as f:\n        text = f.read()\n    match = re.search(r"(?m)^Version\\s+(.+?)\\s+·", text)\n    if not match:\n        raise ValueError("LICENSE.md has no parseable Version line")\n    return match.group(1).strip()\n\n\ndef generate():\n    return {\n        "license": "VBL — Verification Before Assertion License",\n        "version": license_version(),'''
    script=replace_once(script,old_block,new_block,"hard-coded manifest version")
    old_check='''    if current.get("items") != fresh["items"]:\n        print("MANIFEST-ODMIK: telesi se ne ujemata s prijavljenim manifestom (VBL §0a/§12)")'''
    new_check='''    if (current.get("license") != fresh["license"]\n            or current.get("version") != fresh["version"]\n            or current.get("items") != fresh["items"]):\n        print("MANIFEST-ODMIK: identiteta vrat ali telesa se ne ujemajo z manifestom (VBL §0a/§12)")\n        if current.get("version") != fresh["version"]:\n            print("  različica manifesta:", current.get("version"), "| živa vrata:", fresh["version"])'''
    script=replace_once(script,old_check,new_check,"manifest check condition")
    out["scripts/manifest_gen.py"]=script

    # Regenerate only the files that the current license manifest actually covers.
    manifest=json.loads((repo/"LICENSE-MANIFEST.json").read_text(encoding="utf-8"))
    updated={"LICENSE.md":license_text, "REGISTER-NEIMENOVANIH.jsonl":out["REGISTER-NEIMENOVANIH.jsonl"], "REGISTER-PADCEV.jsonl":out["REGISTER-PADCEV.jsonl"]}
    for item in manifest.get("items",[]):
        path=item.get("path")
        if path not in updated:
            raise ValueError(f"Unexpected manifest item {path}; review scope before proceeding")
        data=updated[path].encode("utf-8")
        item["size"]=len(data)
        item["sha256"]=hashlib.sha256(data).hexdigest()
    if len(manifest.get("items",[]))!=3:
        raise ValueError("Expected the measured three-item VBL manifest; scope changed")
    manifest["version"]=LIVE_VERSION
    manifest["date"]="2026-10-30"
    manifest["note"]=(manifest.get("note","")+" ; 2026-10-30: remeasured after attribution corrections and named fall 35 on proposal branch; main unchanged pending independent review").strip(" ;")
    out["LICENSE-MANIFEST.json"]=json.dumps(manifest,ensure_ascii=False,indent=2)+"\n"

    audit=f'''# Attribution and evidence correction — 2026-10-30\n\n**Status: local proposal — not merged; no change to remote \\`main\\` is claimed.**\n\nMeasured base: \\`AtmaOVictu/verification-before-assertion@{BASE_COMMIT}\\`. The live \\`LICENSE.md\\` identifies **VBL {LIVE_VERSION}**. This repair does not issue a new license version or alter the license body.\n\n## Scope of the repair\n\n- \\`REGISTER-NEIMENOVANIH.jsonl\\`: institution, 12 SSKJ² edition authors, five terminological advisers, two technological-support roles and 15 authors of the separately credited 2012 source dictionary are separated. PoVeJMo project collaborators are separated from anonymous/citizen submitters. GaMS3-12B research authors are separated from data-preparation acknowledgements. Individual compensation remains ⚠ wherever the source does not establish it.\n- \\`REGISTER-IZKORISTENJA.jsonl\\`: Reddit's reported deal value stays an estimate; Stack Overflow's API partnership, a reported protest-related suspension and ordinary deletion/answer-ban rules are not conflated.\n- \\`REGISTER-PADCEV.jsonl\\`: entry 35 names the overstatements and proposed corrections. Earlier scars are retained.\n- Public English and Slovenian READMEs are corrected. Live version pointers are synchronized to VBL {LIVE_VERSION}. Historical lineage inside \\`LICENSE.md\\` is untouched.\n- \\`scripts/manifest_gen.py\\` reads its version from \\`LICENSE.md\\`, and its check now compares version identity as well as manifest items.\n- \\`LICENSE-MANIFEST.json\\` is recalculated for the three items it already lists.\n\n## Sources and role distinctions\n\n### SSKJ²\n\n- [Official author list](https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf): Nataša Gliha Komac, Nataša Jakop, Boris Kern, Simona Klemenčič, Domen Krvina, Nina Ledinek, Mija Michelizza, Tanja Mirtič, Andrej Perdih, Špela Petric, Marko Snoj and Andreja Žele.\n- [Official author-list PDF, page 8](https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf): separately lists five **terminological advisers** — Vlado Pivec (economics/finance), Jana Mrak (pharmacy/medicine), Primož Jakopin (film/computing), Stanislav Fortuna (law), Suzana Tratnik (sociology). These advisory roles are not additional edition authors.\n- The same page's footnote 2 says that the 2012 *Slovar novejšega besedja slovenskega jezika* was also used as material for the second edition and lists its 15 authors: Aleksandra Bizjak Končar, Nataša Gliha Komac, Alenka Gložančev, Boris Kern, Simona Klemenčič, Polona Kostanjevec, Domen Krvina, Nina Ledinek, Mija Michelizza, Tanja Mirtič, Andrej Perdih, Špela Petric, Marko Snoj, Ivanka Šircelj Žnidaršič and Andreja Žele. They are credited for the prior dictionary used as source material, not counted as extra SSKJ² edition authors.\n- [Official colophon](https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Kolofon.pdf): identifies the 2014 electronic edition, its copyright notice, and Nina Ledinek and Andrej Perdih under technological support. Their two roles are preserved without counting them as additional authors.\n- Individual author, adviser and contributor payment and contract terms are not established by these public sources.\n\n### PoVeJMo / Povejmo.si\n\n- [Citizen-science project description](https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/): the campaign collected written and spoken Slovenian text **towards** a large language model and estimated a need of 40 billion words. It says submitters must hold copyright in the submitted text. It gives the duration 1 January 2024 to 1 January 2026 and status finished.\n- [University of Ljubljana project page](https://www.fri.uni-lj.si/en/projects/1818): lists project collaborators and their project roles. This is not a complete roster of text submitters and does not make every collaborator an author of every model.\n- Payment of individual submitters or collaborators is not established by either page.\n\n### GaMS3-12B\n\n- [Official model card](https://huggingface.co/cjvt/GaMS3-12B): lists a research team and separately thanks data-collection/preparation contributors. The register keeps the groups separate.\n- No identity join is made between “T. Kuzman” in named-falls entry 4 and “Taja Kuzman” in the model-card acknowledgements. Initials alone are insufficient evidence.\n\n### Common Voice\n\n- [Dataset metadata](https://github.com/common-voice/cv-dataset/): Scripted Speech v27.0 (metadata dated 2026-09) lists 295 languages; dataset types and releases are version-specific.\n- [Common Voice terms](https://commonvoice.mozilla.org/oc/terms): contributions are dedicated to CC0. CC0 and a locale count do not establish whether each contributor was paid.\n\n### Stack Overflow / OpenAI\n\n- [OpenAI announcement, 6 May 2024](https://openai.com/index/api-partnership-with-stack-overflow/): describes an OverflowAPI partnership, use of enhanced content and community feedback, and attribution; it does not publish individual payment terms.\n- [Stack Overflow licensing](https://stackoverflow.com/help/licensing): public contributions are under CC BY-SA 2.5, 3.0 or 4.0 according to the relevant contribution/revision date.\n- [Deleted-answer help](https://stackoverflow.com/help/deleted-answers) says users may generally self-delete answers except accepted answers. [Answer-ban help](https://stackoverflow.com/help/answer-bans) describes bans in connection with low-quality answer history.\n- [The Register, 9 May 2024](https://www.theregister.com/software/2024/05/09/stack-overflow-suspends-users-protesting-openai-deal/1032471/), reported a user's claim that he had received a seven-day suspension after overwriting answers as protest, and other user reports. The register retains that scoped report but does not generalize it to ordinary self-deletion.\n\n### Reddit / Google\n\n- [Reuters, 22 February 2024](https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/): reports a content-licensing deal and a source-estimated value of about US$60 million per year; Reuters says Reddit and Google declined to comment on price. It does not establish individual poster compensation.\n\n## Manifest boundary and limitations\n\nThe current license manifest lists only \\`LICENSE.md\\`, \\`REGISTER-NEIMENOVANIH.jsonl\\` and \\`REGISTER-PADCEV.jsonl\\`. This repair recalculates those files and does **not** silently add \\`REGISTER-IZKORISTENJA.jsonl\\` to the license-covered material. Whether that register belongs in the formal license scope is a separate decision for the author/reviewer.\n\nThis repair does not prove a complete roster of citizen submitters, all upstream training-data sources, individual payment for each contributor, or a legal conclusion about rights in every dataset. It does not change remote \\`main\\`, create a remote PR or claim independent review.\n\n## Required gates before merge\n\n1. Independent re-fetch and review of source pages, roles, dates and corrections.\n2. Successful CI on the exact proposed commit.\n3. Author/reviewer confirmation of the manifest boundary.\n4. No executor self-certification: until independent review and merge, this remains a proposal.\n'''
    audit=audit.replace("\\`", "`")
    out["REVIEW-ATTRIBUTION-AND-CLAIMS-2026-10-30.md"]=audit
    return out


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,default=Path.cwd(),help="path to the repository checkout (default: current directory)")
    parser.add_argument("--dry-run",action="store_true",help="prepare and validate changes without writing")
    parser.add_argument("--no-branch",action="store_true",help="do not create a local topic branch")
    args=parser.parse_args()
    repo=args.repo.resolve()
    if not (repo/".git").exists() and not (repo/".git").is_file():
        raise SystemExit(f"Not a Git working tree: {repo}")
    head=run(["git","rev-parse","HEAD"],repo)
    if head!=BASE_COMMIT:
        raise SystemExit(f"Wrong base commit: expected {BASE_COMMIT}, found {head}. Refusing stale patch.")
    status=run(["git","status","--porcelain"],repo)
    if status:
        raise SystemExit("Working tree is not clean. Commit or stash local changes first; nothing was changed.")

    changes=transform(repo)
    # Validate in-memory register and manifest content before the first write.
    ne=jsonl_load(changes["REGISTER-NEIMENOVANIH.jsonl"],"new contributor register")
    falls=jsonl_load(changes["REGISTER-PADCEV.jsonl"],"new named-falls register")
    ex=jsonl_load(changes["REGISTER-IZKORISTENJA.jsonl"],"new extraction register")
    if [x.get("⊙") for x in ne] != [f"NE-{n:04d}" for n in range(1,14)]:
        raise SystemExit("Contributor-register IDs are not consecutive NE-0001 through NE-0013")
    if len(falls)!=35 or falls[-1].get("entry")!=35 or not falls[-1].get("scar"):
        raise SystemExit("Fall register does not append scar 35 correctly")
    if len(ex)!=4:
        raise SystemExit("Unexpected extraction register row count")
    manifest=json.loads(changes["LICENSE-MANIFEST.json"])
    if manifest.get("version")!=LIVE_VERSION or len(manifest.get("items",[]))!=3:
        raise SystemExit("Manifest identity/scope validation failed")
    if args.dry_run:
        print("DRY RUN PASS — no files written")
        print("Base:",head)
        print("Version:",LIVE_VERSION)
        print("Files:","\n  ".join(sorted(changes)))
        print("Rows: contributors=",len(ne),"falls=",len(falls),"extraction=",len(ex))
        return 0

    if not args.no_branch:
        current=run(["git","branch","--show-current"],repo)
        if current!="main":
            raise SystemExit(f"Expected current branch 'main', found {current}; use --no-branch only after manual review.")
        run(["git","switch","-c",BRANCH],repo)

    git_dir=Path(run(["git","rev-parse","--git-dir"],repo))
    if not git_dir.is_absolute():
        git_dir=(repo/git_dir).resolve()
    backup=git_dir/"vbl-repair-backup-2026-10-30"
    if backup.exists():
        raise SystemExit(f"Backup already exists: {backup}; refusing to overwrite it")
    backup.mkdir(parents=True)
    touched=list(changes)
    for rel in touched:
        target=repo/rel
        if target.exists():
            saved=backup/rel
            saved.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(target,saved)
        else:
            (backup/"__MISSING__"/rel).parent.mkdir(parents=True,exist_ok=True)
            (backup/"__MISSING__"/rel).write_text("",encoding="utf-8")

    try:
        for rel,content in changes.items():
            target=repo/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            fd,tmp=tempfile.mkstemp(prefix=target.name+".",suffix=".tmp",dir=target.parent)
            with os.fdopen(fd,"w",encoding="utf-8",newline="") as f:
                f.write(content)
            os.replace(tmp,target)
        check=run([sys.executable,"scripts/manifest_gen.py","--check"],repo)
        if "MANIFEST-DRZI" not in check:
            raise RuntimeError("Manifest check did not report MANIFEST-DRZI: "+check)
        # Reparse written files and verify no stale live pointers remain.
        jsonl_load((repo/"REGISTER-NEIMENOVANIH.jsonl").read_text(encoding="utf-8"),"written NE register")
        jsonl_load((repo/"REGISTER-PADCEV.jsonl").read_text(encoding="utf-8"),"written falls register")
        for rel in POINTER_FILES:
            if "0.1100 × 10⁴" in (repo/rel).read_text(encoding="utf-8"):
                raise RuntimeError("Stale live pointer remains in "+rel)
    except Exception:
        for rel in touched:
            saved=backup/rel
            target=repo/rel
            if saved.exists():
                shutil.copy2(saved,target)
            elif target.exists():
                target.unlink()
        raise

    print("REPAIR APPLIED LOCALLY — NOT PUSHED, NOT MERGED")
    print("Branch:",BRANCH if not args.no_branch else run(["git","branch","--show-current"],repo))
    print("Base:",BASE_COMMIT)
    print("Version:",LIVE_VERSION)
    print("Manifest:",check)
    print("Contributor rows:",len(ne),"| named falls:",len(falls),"| extraction rows:",len(ex))
    print("Backup:",backup)
    print("Files changed:",len(changes))
    print("Next gate: independent review + CI; do not merge on the executor's self-check alone.")
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (ValueError,RuntimeError,subprocess.CalledProcessError) as exc:
        print("REPAIR NOT APPLIED:",exc,file=sys.stderr)
        raise SystemExit(2)
